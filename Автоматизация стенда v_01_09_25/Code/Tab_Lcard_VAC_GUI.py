from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import numpy as np
from datetime import datetime
import time
from threading import Lock

if __name__ == "__main__":
    import Updatable_QTCanvas
    import Lcard_IF_FullBuffers_with_DataChunks as Lcard_IF_FullBuffers
else:
    from . import Updatable_QTCanvas
    from . import Lcard_IF_FullBuffers as Lcard_IF_FullBuffers # _with_DataChunks

dstr_to_channel = {"Индекс" : -1,
                   "Канал 0" : 0,
                   "Канал 1" : 1,
                   "Канал 2" : 2,
                   "Канал 3" : 3}

def str_to_channel_data(data, column_name):
    try:
        ind = dstr_to_channel[column_name]
        if ind == -1:
            return np.arange(data.shape[1])
        return data[ind, :]
    except Exception as e:
        return np.arange(data.shape[1])

class LcardVACPlot_Interface(object):
        def __init__(self, Lcard_device):
            self.myLcard_IFFB = Lcard_IF_FullBuffers.Lcard_Interface_FullBuffers(Lcard_device)
            self.BufferUpdateTimePeriod = 0.1
            self.PlotFullBuffersUpdateTimePeriod = 1

            self.LastData = None
            self.IsPlotFullBuffersUpdateActive = False
            self.QTimer_updateFullBuffersPlot = QtCore.QTimer()
            self.QTimer_updateFullBuffersPlot.setInterval(1000*self.PlotFullBuffersUpdateTimePeriod) # argument required in msec
            self.QTimer_updateFullBuffersPlot.timeout.connect(self._updateFullBuffersPlot)
            self.Y_x_plot = None

        def _getStartEndIndex(self):
            start = 0
            end = -1
            try:
                start = int(self.QLineEdit_ShownData_StartIndex.text())
                end = int(self.QLineEdit_ShownData_EndIndex.text())
            except Exception as e:
                pass
            return start, end

        def _updateFullBuffersPlot(self):
            self.LastData = self.myLcard_IFFB.getNumpyData()
            self._updatePlot()

        def _updatePlot(self):
            if self.Y_x_plot is None:
                return
            try:
                x_label = self.PlotXAxis_ComboBox.currentText()
                y_label = self.PlotYAxis_ComboBox.currentText()
                start, end = self._getStartEndIndex()
                self.QLineEdit_ShownData_StartIndex.setText(str(start))
                self.QLineEdit_ShownData_EndIndex.setText(str(end))
                x_data = str_to_channel_data(self.LastData, x_label)[start:end]
                y_data = str_to_channel_data(self.LastData, y_label)[start:end]
                self.Y_x_plot.update_plot(x_data, y_data)
                self.Y_x_plot.setAxisLabel(x_label, y_label)
            except Exception as e:
                print("LVAC._updatePlot:", e)
            return

        def setIsPlotTimerActive(self, active_state : bool):
            try:
                if self.IsPlotFullBuffersUpdateActive == active_state:
                    return
                self.IsPlotFullBuffersUpdateActive = active_state
                if active_state:
                    self.QTimer_updateFullBuffersPlot.start()
                else:
                    self.QTimer_updateFullBuffersPlot.stop()
            except Exception as e:
                print(e)

        def _updateIsActiveInterface(self):
            b = self.myLcard_IFFB.getIsActiveInterface()
            self.QpushButton_Start.setEnabled(not(b))
            self.QpushButton_Stop.setEnabled(b)
            self.setIsPlotTimerActive(b)

        def pushStartButton(self):
            print("LVAC.pushStartButton call")
            self.myLcard_IFFB.startFullBuffersRead(self.BufferUpdateTimePeriod)
            self._updateIsActiveInterface()
            print("LVAC.pushStartButton executed")
            
        def pushStopButton(self):
            print("LVAC.pushStopButton call")
            self.myLcard_IFFB.finishFullBuffersRead()
            self._updateIsActiveInterface()
            print("LVAC.pushStopButton executed")

        def pushSingleBufferButton(self):
            self.LastData, syncd_value = self.myLcard_IFFB.myLcardController.myLcardDevice.readBuffer()
            self._updatePlot()

        def pushSaveButton(self):
            print("LVAC.pushSaveButton call")
            s = self.QLineEdit_Save.text()
            start,end = self._getStartEndIndex()
            try:
                try:
                    writer = pd.ExcelWriter(s, mode = "a", if_sheet_exists = 'new')
                except Exception as e:
                    writer = pd.ExcelWriter(s, mode = "w")
                
                d = self.myLcard_IFFB.getParameters()
                Lcard_description = pd.Series(list(d.values()),index=d.keys())
                Lcard_description.to_frame().to_excel(writer, sheet_name = "Параметры Lcard")
                
                df = pd.DataFrame(self.LastData,
                                  columns = ["Канал 0", "Канал 1", "Канал 2", "Канал 3"])
                df.to_excel(writer, sheet_name = "Данные Lcard")
                writer.close()
            except Exception as e:
                print("LVAC.pushSaveButton", e)
            print("LVAC.pushSaveButton executed")
            return

        def pushClearButton(self):
            self.myLcard_IFFB.clearData()
            #self._updatePlot()
            print(type(self.Y_x_plot))
            self.Y_x_plot.axes.cla()
            self.Y_x_plot.draw()
            return

        def setupUI(self):
            self.centralwidget = QtWidgets.QWidget()
            self._translate = QtCore.QCoreApplication.translate
        # --- Plot ---
            self.myPlotWidget = QtWidgets.QWidget(self.centralwidget)
            self.myPlotWidget.setGeometry(QtCore.QRect(0, 0, 900, 900))
            self.Y_x_plot = Updatable_QTCanvas.PyplotWidget(parent = self.myPlotWidget)
            self.Y_x_plot.axes.set_title("Lcard")
            vbox_plot = QtWidgets.QVBoxLayout()
            vbox_plot.addWidget(self.Y_x_plot)
            self.myPlotWidget.setLayout(vbox_plot)
            self.myPlotWidget.setMinimumSize(700,700)
            self.Y_x_plot.setObjectName("Y(x) plot")

            self.PlotXAxis_Label = QtWidgets.QLabel("Ось X", self.centralwidget)
            self.PlotXAxis_ComboBox = QtWidgets.QComboBox(self.centralwidget)
            self.PlotXAxis_ComboBox.addItems(dstr_to_channel.keys())

            self.PlotYAxis_Label = QtWidgets.QLabel("Ось Y", self.centralwidget)
            self.PlotYAxis_ComboBox = QtWidgets.QComboBox(self.centralwidget)
            self.PlotYAxis_ComboBox.addItems(dstr_to_channel.keys())
            self.PlotYAxis_ComboBox.setCurrentText("Канал 0")

            self.QLayout_PlotComboBoxes = QtWidgets.QGridLayout()
            self.QLayout_PlotComboBoxes.addWidget(self.PlotXAxis_Label, 1,0)
            self.QLayout_PlotComboBoxes.addWidget(self.PlotXAxis_ComboBox, 1,1)
            self.QLayout_PlotComboBoxes.addWidget(self.PlotYAxis_Label, 0,0)
            self.QLayout_PlotComboBoxes.addWidget(self.PlotYAxis_ComboBox, 0,1)

        # --- Plot Start End indexes ---
            self.QLineEdit_ShownData_StartIndex = QtWidgets.QLineEdit(parent = self.centralwidget)
            self.QLineEdit_ShownData_StartIndex.setStyleSheet("font: 30 12pt \"Tahoma\";")
            self.QLineEdit_ShownData_EndIndex = QtWidgets.QLineEdit(parent = self.centralwidget)
            self.QLineEdit_ShownData_EndIndex.setStyleSheet("font: 30 12pt \"Tahoma\";")

            self.QLabel_StartIndex = QtWidgets.QLabel("Индекс начала выбранных данных", parent = self.centralwidget)
            self.QLabel_StartIndex.setStyleSheet("font: 30 12pt \"Tahoma\";")
            self.QLabel_EndIndex = QtWidgets.QLabel("Индекс конца выбранных данных", parent = self.centralwidget)
            self.QLabel_EndIndex.setStyleSheet("font: 30 12pt \"Tahoma\";")

            self.QLayout_StartEndIndex = QtWidgets.QGridLayout()
            self.QLayout_StartEndIndex.addWidget(self.QLabel_StartIndex,0,0)
            self.QLayout_StartEndIndex.addWidget(self.QLineEdit_ShownData_StartIndex,0,1)
            self.QLayout_StartEndIndex.addWidget(self.QLabel_EndIndex,1,0)
            self.QLayout_StartEndIndex.addWidget(self.QLineEdit_ShownData_EndIndex,1,1)

        # --- SingleBuffer Button ---
            self.QpushButton_SingleBuffer = QtWidgets.QPushButton(self.centralwidget)
            self.QpushButton_SingleBuffer.setStyleSheet("font: 30 12pt \"Tahoma\";")
            self.QpushButton_SingleBuffer.setText(self._translate("MainWindow", "Прочитать одиночный буфер"))
            self.QpushButton_SingleBuffer.setEnabled(True)

        # --- Start Button ---
            self.QpushButton_Start = QtWidgets.QPushButton(self.centralwidget)
            self.QpushButton_Start.setStyleSheet("font: 30 12pt \"Tahoma\";")
            self.QpushButton_Start.setText(self._translate("MainWindow", "Старт"))
            self.QpushButton_Start.setEnabled(True)

        # --- Stop Button ---
            self.QpushButton_Stop = QtWidgets.QPushButton(self.centralwidget)
            self.QpushButton_Stop.setStyleSheet("font: 30 12pt \"Tahoma\";")
            self.QpushButton_Stop.setObjectName("Stop")
            self.QpushButton_Stop.setText(self._translate("MainWindow", "Стоп"))
            self.QpushButton_Stop.setEnabled(False)

        # --- Save Button --- 
            self.QpushButton_Save = QtWidgets.QPushButton(self.centralwidget)
            self.QpushButton_Save.setStyleSheet("font: 30 12pt \"Tahoma\";")
            self.QpushButton_Save.setObjectName("Save Button")
            self.QpushButton_Save.setText(self._translate("MainWindow", "Сохранить как"))
            self.QpushButton_Save.setEnabled(True)
        # --- Save Filename Line ---
            self.QLineEdit_Save = QtWidgets.QLineEdit(parent = self.centralwidget)
            self.QLineEdit_Save.setStyleSheet("font: 30 12pt \"Tahoma\";")
            self.QLineEdit_Save.setText(("Lcard ВАХ " + str(datetime.now()) + ".xlsx").replace(":","_"))
            self.QLineEdit_Save.setObjectName("Save Line")

        # --- Clear ---
            self.QpushButton_Clear = QtWidgets.QPushButton(self.centralwidget)
            self.QpushButton_Clear.setStyleSheet("font: 30 12pt \"Tahoma\";")
            self.QpushButton_Clear.setObjectName("Очистить")
            self.QpushButton_Clear.setText(self._translate("MainWindow", "Очистить"))
            self.QpushButton_Clear.setEnabled(True)

        # --- Layout ---
            hbox_Start_Stop = QtWidgets.QHBoxLayout()
            hbox_Start_Stop.addWidget(self.QpushButton_Start)
            hbox_Start_Stop.addWidget(self.QpushButton_Stop)

            hbox_Save = QtWidgets.QHBoxLayout()
            hbox_Save.addWidget(self.QpushButton_Save)
            hbox_Save.addWidget(self.QLineEdit_Save)

            vbox_Controls = QtWidgets.QVBoxLayout()
            vbox_Controls.addLayout(self.QLayout_PlotComboBoxes)
            vbox_Controls.addLayout(self.QLayout_StartEndIndex)
            vbox_Controls.addLayout(hbox_Start_Stop)
            vbox_Controls.addWidget(self.QpushButton_SingleBuffer)
            vbox_Controls.addLayout(hbox_Save)
            vbox_Controls.addWidget(self.QpushButton_Clear)

            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(self.myPlotWidget, 1)
            hbox.addLayout(vbox_Controls, 0)

            self.centralwidget.setLayout(hbox)

        # --- Connections ---
            self.QpushButton_Start.clicked.connect(self.pushStartButton)
            self.QpushButton_Stop.clicked.connect(self.pushStopButton)
            self.QpushButton_Save.clicked.connect(self.pushSaveButton)
            self.QpushButton_Clear.clicked.connect(self.pushClearButton)
            self.QpushButton_SingleBuffer.clicked.connect(self.pushSingleBufferButton)
                
            self.QLineEdit_ShownData_StartIndex.editingFinished.connect(self._updatePlot)
            self.QLineEdit_ShownData_EndIndex.editingFinished.connect(self._updatePlot)
            self.PlotXAxis_ComboBox.currentTextChanged.connect(self._updatePlot)
            self.PlotYAxis_ComboBox.currentTextChanged.connect(self._updatePlot)
            return self.centralwidget

        def onCloseEvent(self):
                self.myLcard_IFFB.finishFullBuffersRead()

        """
        def setArePlotUpdatesLive(self, value):
            self.ArePlotUpdatesLive = value
            self.QCheckbox_ArePlotUpdatesLive.setCheckState(value)
            if self.ArePlotUpdatesLive:
                try:
                    self._updatePlot()
                except Exception as e:
                    print(e)
        """
        """
        # --- ArePlotUpdatesLive ---
            self.QCheckbox_ArePlotUpdatesLive = QtWidgets.QCheckBox(text = "Live")
            self.QCheckbox_ArePlotUpdatesLive.setCheckState(self.ArePlotUpdatesLive)
            self.QCheckbox_ArePlotUpdatesLive.setTristate(False)
            self.QCheckbox_ArePlotUpdatesLive.stateChanged.connect(self.onPushArePlotUpdatesLive)
            #vbox_Controls.addWidget(self.QCheckbox_ArePlotUpdatesLive)

            
            def onPushArePlotUpdatesLive(self):
                self.setArePlotUpdatesLive(self.QCheckbox_ArePlotUpdatesLive.checkState())
        """



def test():
    print("Lcard VAC GUI test")
    import sys
    import Lcard_EmptyDevice
    import MainWindow_CloseEvent
    
    Lcard_Device = Lcard_EmptyDevice.LcardE2010B_EmptyDevice("LcardE2010B.ini")
    Lcard_Device.connectToPhysicalDevice()
    
    ui = LcardVACPlot_Interface(Lcard_Device)
    if not(Lcard_Device.IsConnected):
        ui.myLcard_IFFB.myDataChunks = [np.random.random((10,4)),np.random.random((8,4)),np.random.random((8,4))]
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow_CloseEvent.MainWindow_withCloseEvent()
    MainWindow.CloseEventListeners.append(ui.onCloseEvent)
    LVACwidget = ui.setupUI()
    MainWindow.setCentralWidget(LVACwidget)
    MainWindow.show()
    app.exec_()
    
if __name__ == "__main__":
    try:
        test()
        print(">> success")
        print()
    except Exception as e:
        print(">>", e)
        a = input()
