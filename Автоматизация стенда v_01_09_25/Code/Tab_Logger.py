#------------------------ general imports -----------------------------------
import time
import threading
import pandas as pd
import numpy as np
from datetime import datetime
import configparser
import os

#------------------------ Qt and GUI imports --------------------------------
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
if __name__ != "__main__":
    from .MainWindow_CloseEvent import MainWindow_withCloseEvent
else:
    from MainWindow_CloseEvent import MainWindow_withCloseEvent

#------------------------ Korad imports ------------------------------------
if __name__ != "__main__":
    from . import Device_Korad as DKorad
else:
    import Device_Korad as DKorad

#------------------------ Lcard imports ------------------------------------
if __name__ != "__main__":
    from . import LcardDataInterface as LDIF
else:
    import LcardDataInterface as LDIF

#------------------------ Other imports ----------------------------------
from threading import Lock

if __name__ != "__main__":
    from . import Computed_Variables_List as CVL
else:
    import Computed_Variables_List as CVL


def columns_to_csv_string(columns):
    s = ""
    for column in columns:
        s += str(column) + ";"
    return (s + ";CommandTable\n")

def dict_parameters_to_csv(file, parameters):
    s1 = ""
    s2 = ""
    for i in parameters.keys():
        s1 += str(i) + ";"
        s2 += str(parameters[i]) + ";"
    file.write(str.encode(s1 + "\n"))
    file.write(str.encode(s2 + "\n"))
    return file

class TabLogger(object):
        def __init__(self,
                     config_filename,
                     lcard_device, korad_device,
                     CVL_filename):
                self.IsActiveLogger = False
                self.IsThreadUpdateActive = False
                self.UpdateThread = None
                self._LogFile = None
                self.has_ever_log_started = False # unused
                self.is_log_written_to_file = True
                self.LogStartTime = 0

                f = open(config_filename)
                config = configparser.ConfigParser()
                config.read_file(f)
                self.lcard_dots_per_average = config["Logger"].getint("Lcard_dots_per_average")
                self.timer_sleep_time = config["Logger"].getfloat("TimerSleepTime")
                self.os_fsync_period_time = config["OS"].getfloat("SavePeriodTime")
                self.last_os_fsync_time = 0
                f.close()

                """Warning check:"""
                lcard_config = configparser.ConfigParser()
                lcard_config.read(lcard_device.ConfigFilename)
                IrqStep = lcard_config["ADC_Parameters"].getint("IrqStep")
                dKadr = lcard_config["ADC_Parameters"].getfloat("dKadr")
                NCh = lcard_config["ADC_Parameters"].getint("NCh")
                dRate = lcard_config["ADC_Parameters"].getfloat("dRate")
                if self.timer_sleep_time < (2*IrqStep*(dKadr/1000 + NCh/(dRate*1000))):
                    print("\n \n USER WARNING: Лог.TimerSleepTime < (2*IrqStep*(dKadr/1000 + NCh/(dRate*1000)))")
                    print("Такие параметры могут привести к тому, что Lcard не будет успевать обновляться между запросами лога !!! \n \n")
                if self.lcard_dots_per_average > IrqStep:
                    print("\n \n USER WARNING: Лог.Lcard_dots_per_average > IrqStep")
                    print("Такие параметры могут привести к тому, что предыдущие значения с Lcard будут влиять на текущие значения с Lcard !!! \n \n")
                """
                devices:
                """
                self.myLcardIF = LDIF.LcardDataInterface(lcard_device)
                self.myKorad = korad_device
                """
                data processing:
                """
                self.myCVL = CVL.from_txt(CVL_filename) # synthetic Computed Variables List
                
                """
                default user input filenames:
                """
                #self.__LogFilename = ("Данные/Лог " + str(datetime.now()) + ".csv").replace(":","_")
                self.__LogFilename = "Лог отсутствует."
                self.LogFilename = None

                self.DataPieceListeners = []
                self.StopLogListeners = []
                self.StartLogListeners = []
                self.list_qpb_start_stop_log = []

        def setupUi(self):
                self.centralwidget = QtWidgets.QWidget()
                # Log : Label
                self.QLabel_LogFilename = QtWidgets.QLabel("Файл логирования:", self.centralwidget)
                self.QLabel_LogFilename.setStyleSheet("font: 75 15pt \"Tahoma\";")
                # Log : Filename
                self.QLineEdit_LogFilename = QtWidgets.QLineEdit(parent = self.centralwidget)
                self.QLineEdit_LogFilename.setStyleSheet("font: 75 12pt \"Tahoma\";")
                self.QLineEdit_LogFilename.setText(self.__LogFilename)
                self.QLineEdit_LogFilename.setEnabled(False)
                # Log : Start - Stop Buttons
                self.QpButton_startLog = QtWidgets.QPushButton(self.centralwidget)
                self.QpButton_startLog.setStyleSheet("font: 75 18pt \"Tahoma\";")
                self.QpButton_startLog.setText("Запустить логгер")
                """
                # Log : is_log_written_to_file QCheckBox
                self.qch_is_log_written_to_file = QtWidgets.QCheckBox("Ведется запись в файл")
                self.qch_is_log_written_to_file.setChecked(2)
                self.qch_is_log_written_to_file.stateChanged.connect(self.set_log_written_to_file)
                """
                # Connections:
                self.QpButton_startLog.clicked.connect(self.on_push_start_log)
                self.list_qpb_start_stop_log.append(self.QpButton_startLog)
                # Layout:
                self.QLayout_General = QtWidgets.QVBoxLayout()
                self.QLayout_General.addWidget(self.QLabel_LogFilename)
                self.QLayout_General.addWidget(self.QLineEdit_LogFilename)
                self.QLayout_General.addWidget(self.QpButton_startLog)
                #self.QLayout_General.addWidget(self.qch_is_log_written_to_file)
                self.QLayout_General.addStretch()
                self.centralwidget.setLayout(self.QLayout_General)

                self.update_gui()
                return self.centralwidget

        def setup_qpb_start_log(self):
            qpb_start_log = QtWidgets.QPushButton(self.centralwidget)
            qpb_start_log.setStyleSheet("font: 75 18pt \"Tahoma\";")
            qpb_start_log.setText("Запустить логгер")
            qpb_start_log.clicked.connect(self.on_push_start_log)
            self.list_qpb_start_stop_log.append(qpb_start_log)
            return qpb_start_log

        def set_log_written_to_file(self, is_log_written_to_file):
            self.is_log_written_to_file = bool(is_log_written_to_file)
            self.qch_is_log_written_to_file.setChecked(is_log_written_to_file)

        
        def on_push_start_log(self):
            if self.IsActiveLogger:
                self.stopLog()
            else:
                self.startLog()
            self.update_gui()

        def update_gui(self):
            state = self.IsActiveLogger
            if state:
                text = "Остановить логгер"
            else:
                text = "Запустить логгер"
            for qpb in self.list_qpb_start_stop_log:
                qpb.setText(text)

        def setIsActiveLogger(self, IsActiveLogger: bool):
            self.IsActiveLogger = IsActiveLogger
            self.update_gui()
            return

        def startLog(self):
                if self.IsActiveLogger:
                        return
                print("startLog call")
                self.setIsActiveLogger(True)
                self.__LogFilename = ("Данные/Лог " + datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ".csv")
                self.LogFilename = self.__LogFilename
                self.QLineEdit_LogFilename.setText(self.__LogFilename)
                try:
                        self._LogFile = open(self.LogFilename, "ab")
                        # initiating Data Columns by requesting device data and copying their columns:
                        korad_data = self.myKorad.TakeMeasurements()
                        self.myLcardIF.readBuffer()
                        LDIF.calculateAverage(self.myLcardIF)
                        self.DataColumns = (self.myCVL(pd.concat([korad_data, self.myLcardIF.data]))).to_frame().T.columns
                        print("Logger.DataColumns: ", self.DataColumns)
                        self.Data = pd.DataFrame(columns = self.DataColumns)
                        #write down Data Columns into Log File:
                        self._LogFile.write(str.encode(columns_to_csv_string(self.DataColumns)))
                except Exception as e:
                        print(e)
                        self.setIsActiveLogger(False)
                        return
                for listener in self.StartLogListeners:
                    listener()
                try:
                    self.myLcardIF.myLcardDevice.addListener()
                except Exception as e:
                    print(e)
                try:
                    self.myKorad.StartExperiment()
                    if not(self.has_ever_log_started):
                        print("Первый запуск логгера. Время начала лога установлено.")
                        self.has_ever_log_started = True
                        self.LogStartTime = time.time()
                    self.UpdateThread = threading.Thread(target = self.updateLogInThread)
                    self.IsThreadUpdateActive = True
                    self.UpdateThread.start()
                except Exception as e:
                    print(e)
                self.last_os_fsync_time = time.time()
                print("startLog executed")

        def updateLogInThread(self):
            while self.IsThreadUpdateActive:
                self.updateLog()
                time.sleep(self.timer_sleep_time)
            return

        def updateLog(self):
                #UpdateStartTime = time.time()
                # receive data
                korad_data = self.myKorad.TakeMeasurements()
                self.myLcardIF.readBuffer()
                
                # data processing
                korad_data["KORAD_TIME"] -= self.LogStartTime
                LDIF.cropToRequestedBuffer(
                    self.myLcardIF, 
                    requested_buffer_size = self.lcard_dots_per_average
                    )
                LDIF.calculateAverage(self.myLcardIF)
                lcard_data = self.myLcardIF.data
                lcard_data["LCARD_COMP_TIME"] -= self.LogStartTime
                
                #myDataPiece = lcard_data
                myDataPiece = (pd.concat([korad_data, lcard_data]))
                myDataPiece = self.myCVL(myDataPiece).to_frame().T
                
                # data processing : update synth channel
                #self.Data = pd.concat([self.Data, myDataPiece])
                # data processing : save to file
                if self.is_log_written_to_file and not(self._LogFile.closed):
                    np.savetxt(self._LogFile, myDataPiece, fmt = '%s', delimiter = ";")
                if time.time() - self.last_os_fsync_time > self.os_fsync_period_time:
                    os.fsync(self._LogFile)
                    self.last_os_fsync_time = time.time()

                for listener in self.DataPieceListeners:
                    listener(myDataPiece)
                

                

        def onCloseEvent(self):
                print("Disconnecting from all devices")
                try:
                        self.stopLog()
                        if self.myKorad:
                                self.myKorad.DisconnectFromPhysicalDevice()
                        if self.myLcardIF and self.myLcardIF.myLcardDevice:
                                self.myLcardIF.myLcardDevice.disconnectFromPhysicalDevice()
                except Exception as e:
                        print(e)
                print("Logger onCloseEvent executed")

        def stopLog(self):
            print("stopLog call")
            try:
                    if self.IsActiveLogger:
                            self.IsActiveLogger = False
                    if self.IsThreadUpdateActive:
                            self.IsThreadUpdateActive = False
                            self.UpdateThread.join()
                    self.setIsActiveLogger(False)
                    if self._LogFile and not(self._LogFile.closed):
                            os.fsync(self._LogFile) # before closing
                            self._LogFile.close()
                    if self.myKorad:
                            self.myKorad.FinishExperiment()
                    if self.myLcardIF and self.myLcardIF.myLcardDevice:
                            self.myLcardIF.myLcardDevice.removeListener()
                    for listener in self.StopLogListeners:
                        listener()
            except Exception as e:
                    print(e)
            print("stopLog executed")




def test():
    print("tab logger test")
    import sys 
    import Lcard_EmptyDevice
    
    myLcard = Lcard_EmptyDevice.LcardE2010B_EmptyDevice("LcardE2010B.ini")
    myKorad = DKorad.Korad('Korad.ini')
    myKorad.ConnectToPhysicalDevice()
    myKorad.StartExperiment()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow_withCloseEvent()
    ui = TabLogger(lcard_device = myLcard, 
                   korad_device = myKorad)
    centralwidget = ui.setupUi()
    MainWindow.setCentralWidget(centralwidget)
    MainWindow.CloseEventListeners.append(ui.onCloseEvent)
    MainWindow.resize(1300,1000)
    MainWindow.show()
    app.exec_()

if __name__ == "__main__":
    try:
        test()
        print(">> success")
    except Exception as e:
        print(e)
        a = input()
    
