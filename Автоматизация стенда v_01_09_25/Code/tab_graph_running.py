#------------------------ general imports -----------------------------------
import time
import pandas as pd
import numpy as np
import configparser
import multiprocessing
import threading
from datetime import datetime

#------------------------ Qt and GUI imports --------------------------------
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from .Updatable_QTCanvas import PyplotWidget
from .MainWindow_CloseEvent import MainWindow_withCloseEvent

matplotlib_colors = ["green", "blue", "red", "black", "yellow"]

def color_index_to_color(index):
        return matplotlib_colors[index%len(matplotlib_colors)]




class TabGraphRunning(object):
        def __init__(self,
                     X_Axis_Variable_Name, Y_Axis_Variable_Name,
                     displayed_dots_amount = 30):
                # Parameters:
                self.X_Axis_Variable_Name = X_Axis_Variable_Name
                self.Y_Axis_Variable_Name = Y_Axis_Variable_Name
                self.displayed_dots_amount = displayed_dots_amount
                # matplotlib variables: 
                self.CurrentArtist_ColorIndex = None
                # data processing:
                self.df = pd.DataFrame()
                self.YetNotDrownDataChunks = multiprocessing.Queue()
                self.is_displayed = False
                self.PlotUpdateThread = None
                self.is_data_chunk_written = False
                
        #---------------------------------- draw Data -----------------------------------------------------

        def drawDataPieces(self):
                size = self.YetNotDrownDataChunks.qsize() - int(bool(self.is_data_chunk_written)) # -1, чтобы не начать читать еще записываемые данные, если данные еще передаются  
                if size <= 0:
                        return False
                df_arr = [0]*(size+1)
                for i in range(1,size+1):
                        df_arr[i] = self.YetNotDrownDataChunks.get()
                df_arr[0] = self.df
                self.df = pd.concat(df_arr)
                if self.df.shape[0] > self.displayed_dots_amount:
                        self.df = self.df.iloc[self.df.shape[0]-self.displayed_dots_amount : ]
                self.drawDataPiece(self.df)
                return True

        def drawDataPiece(self, df):
                if not(self.X_Axis_Variable_Name in df.columns) or not(self.Y_Axis_Variable_Name in df.columns):
                        return
                my_df = df[[self.X_Axis_Variable_Name, self.Y_Axis_Variable_Name]].dropna()
                self.Plot.axes.cla()
                self.Plot.axes.set_xlabel(self.X_Axis_Variable_Name)
                self.Plot.axes.set_ylabel(self.Y_Axis_Variable_Name)
                self.Plot.update_plot(my_df[self.X_Axis_Variable_Name], my_df[self.Y_Axis_Variable_Name], s = 5, color = "blue")
                return
        
        def setupUi(self, add_buttons = True, color = 'red'):
                self.centralwidget = QtWidgets.QWidget()
                
                self.Plot = PyplotWidget()
                self.color = color
                
                self.Plot.update_plot([],[])
                self.Plot.setAxisLabel(self.X_Axis_Variable_Name, self.Y_Axis_Variable_Name)

                self.qch_is_trace_left = QtWidgets.QCheckBox(text = "Оставлять след")
                self.qch_is_trace_left.setCheckState(2)
                self.qch_is_trace_left.stateChanged.connect(self.on_push_is_trace_left)
                self.qpb_savefig = QtWidgets.QPushButton(text = "Сохранить график")
                self.qpb_savefig.clicked.connect(self.on_push_save_png)
                self.qhbl_buttons = QtWidgets.QHBoxLayout()
                self.qhbl_buttons.addWidget(self.qch_is_trace_left)
                self.qhbl_buttons.addWidget(self.qpb_savefig)
                
                self.QLayout_General = QtWidgets.QVBoxLayout()
                self.QLayout_General.addWidget(self.Plot)
                if add_buttons:
                        self.QLayout_General.addLayout(self.qhbl_buttons)
                
                self.centralwidget.setLayout(self.QLayout_General)
                return self.centralwidget

        def on_push_save_png(self):
                self.Plot.fig.savefig(("Данные/График " + str(datetime.now()) + ".png").replace(":","_"))

        def on_push_is_trace_left(self, args):
                self.is_trace_left = bool(args)

        # listener function
        def addDataPiece(self, df):
                self.is_data_chunk_written = True
                self.YetNotDrownDataChunks.put_nowait(df)
                self.is_data_chunk_written = False

        # ------------------------------------------------- Plot Thread Update ----------------------------
        def startPlotUpdate(self):
                self.IsPlotUpdateActive = True
                self.PlotUpdateThread = threading.Thread(target = self.updatePlot)
                self.PlotUpdateThread.start()


        def updatePlot(self):
                while self.IsPlotUpdateActive:
                        if self.is_displayed:
                                self.drawDataPieces()
                        time.sleep(0.1)
                return

        def stopPlotUpdate(self):
                self.IsPlotUpdateActive = False
                if not(self.PlotUpdateThread is None):
                        self.PlotUpdateThread.join()
                
        def onCloseEvent(self):
                print("Tab_Graph_withPreviousData.onCloseEvent call")
                
"""

def test():
    print("Tab_Graph_withPreviousData test")
    import sys
    import Tab_Logger_with_sympy_parse
    import Lcard_EmptyDevice
    import Device_Korad as DKorad

    myLcard = Lcard_EmptyDevice.LcardE2010B_EmptyDevice("LcardE2010B.ini")
    myKorad = DKorad.Korad('Korad.ini')

    logger = Tab_Logger.TabLogger(lcard_device = myLcard, korad_device = myKorad)
    ui = TabLcardVAC_withPreviousData()
    logger.DataPieceListeners.append(ui.drawDataPiece)
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow_withCloseEvent()
    tabs = QtWidgets.QTabWidget()
    tabs.addTab(ui.setupUi(), "Lcard VAC 2")
    tabs.addTab(logger.setupUi(), "Logger")
    centralwidget = tabs
    MainWindow.setCentralWidget(centralwidget)
    MainWindow.CloseEventListeners.append(ui.onCloseEvent)
    MainWindow.show()
    app.exec_()

if __name__ == "__main__":
    try:
        test()
        print(">> success")
    except Exception as e:
        print(e)
        a = input()
"""
