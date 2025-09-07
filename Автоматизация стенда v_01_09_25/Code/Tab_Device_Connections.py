#------------------------ general imports -----------------------------------
import time
import pandas as pd
import numpy as np
import configparser
import serial.tools.list_ports

#------------------------ Qt and GUI imports --------------------------------
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from .MainWindow_CloseEvent import MainWindow_withCloseEvent

#------------------------ Device imports ------------------------------------
from . import Device_Korad as DKorad
from . import Lcard_EmptyDevice

FOLDER_USER_CONFIGS = "Пользовательские конфигурации/"

DEFAULT_KORAD_FILENAME = "Korad.ini"
DEFAULT_LCARD_FILENAME = "LcardE2010B.ini"

TEXT_CONNECT_KORAD = "Подключить Korad"
TEXT_DISCONNECT_KORAD = "Отключить Korad"
TEXT_START_KORAD = "Запустить Korad"
TEXT_STOP_KORAD = "Остановить Korad"
TEXT_KORAD_FILENAME_LABEL = "Файл параметров Korad"
TEXT_KORAD_SET_I = "Установить I"
TEXT_KORAD_SET_U = "Установить U"
TEXT_NO_COMPORTS = "Нет доступных COM-портов"

TEXT_CONNECT_LCARD = "Подключить Lcard"
TEXT_DISCONNECT_LCARD = "Отключить Lcard"
TEXT_START_LCARD = "Запустить Lcard"
TEXT_STOP_LCARD = "Остановить Lcard"
TEXT_LCARD_FILENAME_LABEL = "Файл параметров Lcard"

LCARD_PARAMETER_NAMES = ["FIFO", "IrqStep", "Pages", "AutoInit", "dRate", "dKadr",
                        "SynchroType","SynchroSrc","AdcIMask","NCh","IrqEna","AdcEna"]

class TabDeviceConnections(object):
        def __init__(self,
                     korad_ini, lcard_ini):
                # devices with hardcoded default ini:
                self.myLcard_Device = Lcard_EmptyDevice.LcardE2010B_EmptyDevice(lcard_ini)
                self.myKorad_Device = DKorad.Korad(korad_ini)
                try:
                        config = configparser.ConfigParser()
                        config.read(korad_ini)
                        self.korad_ini_comport = config["COM settings"]["com port"]
                except Exception as e:
                        print("В файле ", korad_ini, "предоставленном как конфигурационный файл Корада, не найден параметр com port:", e)

        def __del__(self):
                #self.myLcard_Device.disconnectFromPhysicalDevice()
                #self.myKorad_Device.DisconnectFromPhysicalDevice()
                # По просьбе Николая Николаевича Чадаева выключать при выходе ничего не надо.
                return

        def onAppStart(self):
                self.connectKorad()
                self.startKorad()
                self.connectLcard()
                self.startLcard()
                
        def setupUi(self):
                self.centralwidget = QtWidgets.QWidget()
                # Korad : Connect Button
                self.QpButton_connectKorad = QtWidgets.QPushButton(self.centralwidget)
                self.QpButton_connectKorad.setStyleSheet("font: 75 18pt \"Tahoma\";")
                self.QpButton_connectKorad.setText(TEXT_CONNECT_KORAD)
                self.QpButton_connectKorad.clicked.connect(self.onPushConnectKorad)
                # Korad : Config filename choice
                self.QLabel_FilenameKorad_ini = QtWidgets.QLabel(TEXT_KORAD_FILENAME_LABEL, self.centralwidget)
                self.QLabel_FilenameKorad_ini.setStyleSheet("font: 75 15pt \"Tahoma\";")
                self.QLineEdit_FilenameKorad_ini = QtWidgets.QLineEdit(parent = self.centralwidget)
                self.QLineEdit_FilenameKorad_ini.setStyleSheet("font: 75 12pt \"Tahoma\";")
                self.QLineEdit_FilenameKorad_ini.setText(DEFAULT_KORAD_FILENAME)
                self.QLineEdit_FilenameKorad_ini.setMaximumHeight(200)
                # Korad : COM-port choice:
                self.qcb_possible_comports = QtWidgets.QComboBox()
                self.qcb_possible_comports.setMinimumHeight(40)
                # Korad : Start - Stop Button
                self.QpButton_StartStopKorad = QtWidgets.QPushButton(self.centralwidget)
                self.QpButton_StartStopKorad.setStyleSheet("font: 75 18pt \"Tahoma\";")
                self.QpButton_StartStopKorad.setText(TEXT_START_KORAD)
                self.QpButton_StartStopKorad.clicked.connect(self.onPushStartStopKorad)
                # Korad : Set_I 
                self.QpButton_Korad_Set_I = QtWidgets.QPushButton(self.centralwidget)
                self.QpButton_Korad_Set_I.setStyleSheet("font: 75 18pt \"Tahoma\";")
                self.QpButton_Korad_Set_I.setText(TEXT_KORAD_SET_I)
                self.QLineEdit_Korad_Set_I = QtWidgets.QLineEdit(parent = self.centralwidget)
                self.QLineEdit_Korad_Set_I.setStyleSheet("font: 75 18pt \"Tahoma\";")
                self.QpButton_Korad_Set_I.clicked.connect(self.onPushKoradSetI)
                self.QLineEdit_Korad_Set_I.editingFinished.connect(self.onPushKoradSetI)
                # Korad : Set_U
                self.QpButton_Korad_Set_U = QtWidgets.QPushButton(self.centralwidget)
                self.QpButton_Korad_Set_U.setStyleSheet("font: 75 18pt \"Tahoma\";")
                self.QpButton_Korad_Set_U.setText(TEXT_KORAD_SET_U)
                self.QLineEdit_Korad_Set_U = QtWidgets.QLineEdit(parent = self.centralwidget)
                self.QLineEdit_Korad_Set_U.setStyleSheet("font: 75 18pt \"Tahoma\";")
                self.QpButton_Korad_Set_U.clicked.connect(self.onPushKoradSetU)
                self.QLineEdit_Korad_Set_U.editingFinished.connect(self.onPushKoradSetU)
                # Korad : Layout
                self.QLayout_Korad = QtWidgets.QVBoxLayout()
                self.QLayout_Korad.addWidget(self.QLabel_FilenameKorad_ini)
                self.QLayout_Korad.addWidget(self.QLineEdit_FilenameKorad_ini)
                self.QLayout_Korad.addWidget(self.qcb_possible_comports)
                self.QLayout_Korad.addWidget(self.QpButton_connectKorad)
                self.QLayout_Korad.addWidget(self.QpButton_StartStopKorad)
                QL_set_U_I = QtWidgets.QGridLayout()
                QL_set_U_I.addWidget(self.QpButton_Korad_Set_I, 0, 0)
                QL_set_U_I.addWidget(self.QLineEdit_Korad_Set_I, 0, 1)
                QL_set_U_I.addWidget(self.QpButton_Korad_Set_U, 1, 0)
                QL_set_U_I.addWidget(self.QLineEdit_Korad_Set_U, 1, 1)
                self.QLayout_Korad.addLayout(QL_set_U_I)
                self.QLayout_Korad.addStretch()
                # Korad : first update
                self.updateKoradGUI()
                
                # Lcard : Connect Button
                self.QpButton_connectLcard = QtWidgets.QPushButton(self.centralwidget)
                self.QpButton_connectLcard.setStyleSheet("font: 75 18pt \"Tahoma\";")
                self.QpButton_connectLcard.setText(TEXT_CONNECT_LCARD)
                self.QpButton_connectLcard.clicked.connect(self.onPushConnectLcard)
                # Lcard : Start Stop Button
                self.QpButton_StartStopLcard = QtWidgets.QPushButton(self.centralwidget)
                self.QpButton_StartStopLcard.setStyleSheet("font: 75 18pt \"Tahoma\";")
                self.QpButton_StartStopLcard.setText(TEXT_START_LCARD)
                self.QpButton_StartStopLcard.clicked.connect(self.onPushStartStopLcard)
                # Lcard : Config filename choice
                self.QLabel_FilenameLcard_ini = QtWidgets.QLabel(TEXT_LCARD_FILENAME_LABEL, self.centralwidget)
                self.QLabel_FilenameLcard_ini.setStyleSheet("font: 75 15pt \"Tahoma\";")
                self.QLabel_FilenameLcard_ini.setMaximumHeight(50)
                self.QLineEdit_FilenameLcard_ini = QtWidgets.QLineEdit(parent = self.centralwidget)
                self.QLineEdit_FilenameLcard_ini.setStyleSheet("font: 75 12pt \"Tahoma\";")
                self.QLineEdit_FilenameLcard_ini.setText(DEFAULT_LCARD_FILENAME)
                self.QLineEdit_FilenameLcard_ini.setMaximumHeight(50)
                
                self.qlbe_daq_parameters = {}
                self.qlayout_daq_parameters = QtWidgets.QVBoxLayout()
                def createDAQParameterGUI(name):
                        qlb = QtWidgets.QLabel(name, self.centralwidget)
                        qle = QtWidgets.QLineEdit(parent = self.centralwidget)
                        self.qlbe_daq_parameters[name] = (qlb, qle)
                        qle.editingFinished.connect(self.set_lcard_parameter)
                        qle.setEnabled(False)
                        hbox = QtWidgets.QHBoxLayout()
                        hbox.addWidget(qlb)
                        hbox.addWidget(qle)
                        self.qlayout_daq_parameters.addLayout(hbox)
                        
                for name in LCARD_PARAMETER_NAMES:
                        createDAQParameterGUI(name)
                
                # Lcard : Layout
                self.QLayout_Lcard = QtWidgets.QVBoxLayout()
                self.QLayout_Lcard.addWidget(self.QLabel_FilenameLcard_ini)
                self.QLayout_Lcard.addWidget(self.QLineEdit_FilenameLcard_ini)
                self.QLayout_Lcard.addWidget(self.QpButton_connectLcard)
                self.QLayout_Lcard.addWidget(self.QpButton_StartStopLcard)
                self.QLayout_Lcard.addLayout(self.qlayout_daq_parameters)
                self.QLayout_Lcard.addStretch()
                # Lcard : first update
                self.updateLcardGUI()
                
                # Layout
                self.QLayout_General = QtWidgets.QHBoxLayout()
                self.QLayout_General.addLayout(self.QLayout_Lcard)
                self.QLayout_General.addStretch()
                self.QLayout_General.addLayout(self.QLayout_Korad)
                self.QLayout_General.addStretch()
                self.centralwidget.setLayout(self.QLayout_General)

                return self.centralwidget

        def onCloseEvent(self):
                #print("Disconnecting from all devices")
                #self.disconnectKorad()
                #self.disconnectLcard()
                # По просьбе Николая Николаевича Чадаева выключать при выходе ничего не надо.
                return
        
        # ------------ Korad --------------------
        def onPushConnectKorad(self):
            if self.myKorad_Device.IsConnected:
                self.disconnectKorad()
            else:
                self.connectKorad()
            return

        def onPushStartStopKorad(self):
            print("onPushStartStopKorad call", self.myKorad_Device.IsActiveMeasurements)
            if self.myKorad_Device.IsActiveMeasurements:
                self.stopKorad()
            else:
                self.startKorad()
            return

        def onPushKoradSetI(self):
            self.myKorad_Device.set_uncheckedI(self.QLineEdit_Korad_Set_I.text())

        def onPushKoradSetU(self):
            self.myKorad_Device.set_uncheckedU(self.QLineEdit_Korad_Set_U.text())

        def updateKoradGUI(self):
            self.QLineEdit_FilenameKorad_ini.setEnabled(not(self.myKorad_Device.IsConnected))
            self.QpButton_connectKorad.setEnabled(not(self.myKorad_Device.IsActiveMeasurements))
            self.QpButton_StartStopKorad.setEnabled(self.myKorad_Device.IsConnected)
            self.QpButton_Korad_Set_I.setEnabled(self.myKorad_Device.IsActiveMeasurements)
            self.QpButton_Korad_Set_U.setEnabled(self.myKorad_Device.IsActiveMeasurements)
            self.QLineEdit_Korad_Set_I.setEnabled(self.myKorad_Device.IsActiveMeasurements)
            self.QLineEdit_Korad_Set_U.setEnabled(self.myKorad_Device.IsActiveMeasurements)
            self.possible_comports = [str(_) for _ in serial.tools.list_ports.comports()]
            self.possible_comports.insert(0, (self.korad_ini_comport + " - параметр конфигурационного файла"))
            self.qcb_possible_comports.clear()
            if self.myKorad_Device.IsConnected:
                    self.qcb_possible_comports.addItem(str(self.myKorad_Device.ser.port))
            elif len(self.possible_comports) > 0:
                    self.qcb_possible_comports.addItems(self.possible_comports)
            else:
                self.qcb_possible_comports.addItem(TEXT_NO_COMPORTS)
            self.qcb_possible_comports.setEnabled(not(self.myKorad_Device.IsConnected))

            if self.myKorad_Device.IsConnected:
                self.QpButton_connectKorad.setText(TEXT_DISCONNECT_KORAD)
            else:
                self.QpButton_connectKorad.setText(TEXT_CONNECT_KORAD)

            if self.myKorad_Device.IsActiveMeasurements:
                self.QpButton_StartStopKorad.setText(TEXT_STOP_KORAD)
            else:
                self.QpButton_StartStopKorad.setText(TEXT_START_KORAD)

        def connectKorad(self):
            self.myKorad_Device.DisconnectFromPhysicalDevice()
            self.myKorad_Device.ConfigFilename = FOLDER_USER_CONFIGS + self.QLineEdit_FilenameKorad_ini.text()
            config_dict = self.myKorad_Device.LoadConfiguration()
            if self.qcb_possible_comports.currentText() != TEXT_NO_COMPORTS:
                    config_dict['com port'] = self.qcb_possible_comports.currentText().split()[0]
            self.myKorad_Device.ConnectToPhysicalDevice(config_dict = config_dict)
            self.updateKoradGUI()

        def disconnectKorad(self):
            self.myKorad_Device.DisconnectFromPhysicalDevice()
            self.updateKoradGUI()

        def startKorad(self):
            print("DeviceConnections.startKorad call")
            self.myKorad_Device.StartExperiment()
            self.updateKoradGUI()

        def stopKorad(self):
            self.myKorad_Device.FinishExperiment()
            self.updateKoradGUI()

        # ------------ Lcard --------------------
        def onPushConnectLcard(self):
            if self.myLcard_Device.IsConnected:
                self.disconnectLcard()
            else:
                self.connectLcard()
            return

        def onPushStartStopLcard(self):
            try:
                    if self.QpButton_StartStopLcard.text() == TEXT_START_LCARD:
                        self.startLcard()
                    else:
                        self.stopLcard()
                    
            except Exception as e:
                    print(e)

        def connectLcard(self):
            self.myLcard_Device.disconnectFromPhysicalDevice()
            self.myLcard_Device.ConfigFilename = FOLDER_USER_CONFIGS + self.QLineEdit_FilenameLcard_ini.text()
            self.myLcard_Device.connectToPhysicalDevice()
            try:
                self.updateLcardGUI()
            except Exception as e:
                print(e)
        
        def disconnectLcard(self):
            self.myLcard_Device.disconnectFromPhysicalDevice()
            self.updateLcardGUI()

        def startLcard(self):
            self.myLcard_Device.addListener()
            self.updateLcardGUI()

        def stopLcard(self):
            self.myLcard_Device.finishMeasurements()
            self.updateLcardGUI()

        def set_lcard_parameter(self):
            try:
                    parameters = self.myLcard_Device.getDAQPAR()
                    for name in ["FIFO", "IrqStep", "Pages", "AutoInit", "dRate","dKadr","NCh","IrqEna","AdcEna"]:
                        parameters[name] = self.qlbe_daq_parameters[name][1].text()
                    self.myLcard_Device.setDAQPAR(parameters)
                    self.updateLcardGUI()
            except Exception as e:
                    print("set_lcard_parameter error: ", e)

        def updateLcardGUI(self):
            try:
                    parameters = self.myLcard_Device.getDAQPAR()
                    for name in LCARD_PARAMETER_NAMES:
                            self.qlbe_daq_parameters[name][1].setText(str(parameters[name]))
            except Exception as e:
                    print("updateLcardGUI: ", e)
                
            self.QLineEdit_FilenameLcard_ini.setEnabled(not(self.myLcard_Device.IsConnected))
            self.QpButton_connectLcard.setEnabled(not(self.myLcard_Device.IsActiveMeasurements))
            self.QpButton_StartStopLcard.setEnabled(self.myLcard_Device.IsConnected)

            if self.myLcard_Device.IsConnected:
                self.QpButton_connectLcard.setText(TEXT_DISCONNECT_LCARD)
            else:
                self.QpButton_connectLcard.setText(TEXT_CONNECT_LCARD)

            if self.myLcard_Device.IsActiveMeasurements:
                    self.QpButton_StartStopLcard.setText(TEXT_STOP_LCARD)
            else:
                    self.QpButton_StartStopLcard.setText(TEXT_START_LCARD)

            self.myLcard_Device
                


def test():
    print("TabDeviceConnections test")
    import sys 
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow_withCloseEvent()
    ui = TabDeviceConnections()
    centralwidget = ui.setupUi()
    MainWindow.setCentralWidget(centralwidget)
    MainWindow.CloseEventListeners.append(ui.onCloseEvent)
    MainWindow.show()
    app.exec_()

    print(ui.myKorad_Device.ConfigFilename)
    print(ui.myLcard_Device.ConfigFilename)

if __name__ == "__main__":
    try:
        test()
        print(">> success")
    except Exception as e:
        print(e)
        a = input()
    
