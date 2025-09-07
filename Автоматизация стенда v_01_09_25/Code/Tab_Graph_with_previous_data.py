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




class Tab_Graph_with_previous_data(object):
        def __init__(self,
                     X_Axis_Variable_Name, Y_Axis_Variable_Name,
                     old_data = None):
                # Parameters:
                self.X_Axis_Variable_Name = X_Axis_Variable_Name
                self.Y_Axis_Variable_Name = Y_Axis_Variable_Name
                self.is_trace_left = True
                
                # matplotlib variables: 
                self.last_dot = None
                self.CurrentArtist = None
                self.CurrentArtist_ColorIndex = None
                self.IsPlotBoundsUpdateActive = False
                self.initial_xy_lims = {"x" : (np.inf,-np.inf), "y" : (np.inf,-np.inf)}

                # data processing:
                self.PreviousDataFilenamesList_old = [] # not used
                self.PreviousDataFilenamesList_new = []
                self.x = []
                self.y = []
                self.is_displayed = False
                self.is_data_chunk_written = False
                self.YetNotDrownDataChunks = multiprocessing.Queue()
                self.PlotUpdateThread = None
                self.was_no_data_warning_shown = False # a warning about no such axis in data
                if old_data:
                        self.PreviousDataFilenamesList_new.append(old_data)

        def read_csv_withPreviousData(self, filename):
                df = pd.read_csv(filename, delimiter = ";")
                self.PreviousDataFilenamesList_old = list(df["Old Version Data Filenames List"].dropna())
                self.PreviousDataFilenamesList_new = list(df["New Version Data Filenames List"].dropna())
                
        #---------------------------------- draw Data -----------------------------------------------------

        def drawPreviousFileData(self, filename, color = "blue", alpha = 0.5, s=1):
                try: # тк работаем с пользовательским файлом.
                        df = pd.read_csv(filename, delimiter = ";")
                        if not(self.X_Axis_Variable_Name in df.columns):
                                print("ABORT: При попытке отобразить график со старыми данными - столбец", self.X_Axis_Variable_Name, "не найден.")
                                return
                        if not(self.Y_Axis_Variable_Name in df.columns):
                                print("ABORT: При попытке отобразить график со старыми данными - столбец", self.Y_Axis_Variable_Name, "не найден.")
                                return
                        self.Plot.draw_scatter(
                                df[self.X_Axis_Variable_Name], df[self.Y_Axis_Variable_Name],
                                color = color, alpha = alpha, s=s
                                )
                        self.initial_xy_lims = self.get_xy_lims(df[self.X_Axis_Variable_Name], df[self.Y_Axis_Variable_Name])
                except Exception as e:
                        print("ABORT: При попытке отобразить график со старыми данными:", e)

        def get_xy_lims(self, x, y):
                d = { "x": self.get_x_lims(x),
                      "y": self.get_y_lims(y)
                      }
                return d

        def get_x_lims(self, x):
                if x.size == 0:
                        return (0,1)
                range_x = np.max(x) - np.min(x)
                return (min(np.min(x) - range_x/12, self.initial_xy_lims["x"][0]),
                        max(np.max(x) + range_x/12, self.initial_xy_lims["x"][1]))
        
        def get_y_lims(self, y):
                if y.size == 0:
                        return (0,1)
                range_y = np.max(y) - np.min(y)
                return (min(np.min(y) - range_y/12, self.initial_xy_lims["y"][0]),
                        max(np.max(y) + range_y/12, self.initial_xy_lims["y"][1]))
                
        def set_xy_lims(self, xy_lims : dict):
                if (xy_lims["x"][0] is np.inf) or (xy_lims["x"][0] == xy_lims["x"][1]):
                        self.Plot.axes.set_xlim(0,1)
                else:
                        self.Plot.axes.set_xlim(xy_lims["x"][0],xy_lims["x"][1])
                if (xy_lims["y"][0] is np.inf) or (xy_lims["y"][0] == xy_lims["y"][1]):
                        self.Plot.axes.set_ylim(0,1)
                else:
                        self.Plot.axes.set_ylim(xy_lims["y"][0],xy_lims["y"][1])

        def unite_xy_lims(self, xy_lims1, xy_lims2):
                d = { "x" : (min(xy_lims1["x"][0], xy_lims2["x"][0]), max(xy_lims1["x"][1], xy_lims2["x"][1])),
                      "y" : (min(xy_lims1["y"][0], xy_lims2["y"][0]), max(xy_lims1["y"][1], xy_lims2["y"][1]))
                      }
                return d

        def set_xy_lims_with_last_dots(self, x, y, x_last_dots, y_last_dots):
                self.set_xy_lims(self.unite_xy_lims(self.get_xy_lims(x,y), self.get_xy_lims(x_last_dots, y_last_dots)))
                        
        def drawPreviousFileData_new(self, filename, color = "blue", alpha = 0.5, s=1):
                self.drawPreviousFileData(filename, color = color, alpha = alpha, s=s)

        def drawPreviousFileData_old(self, filename, color = "blue", alpha = 0.5, s=1):
                self.drawPreviousFileData(filename, color = color, alpha = alpha, s=s)

        def drawDataPieces(self):
                size = self.YetNotDrownDataChunks.qsize() - int(bool(self.is_data_chunk_written)) # -1, чтобы не начать читать еще записываемые данные, если данные еще передаются 
                if size <= 0:
                        return False
                df_arr = [0]*size
                for i in range(size):
                        df_arr[i] = self.YetNotDrownDataChunks.get()
                df = pd.concat(df_arr)
                self.drawDataPiece(df)
                return True

        def drawDataPiece(self, df):
                if not(self.X_Axis_Variable_Name in df.columns) or not(self.Y_Axis_Variable_Name in df.columns) and not(self.was_no_data_warning_shown):
                        self.was_no_data_warning_shown = True
                        s = ("\n\nUSER WARNING: Один или оба столбца с данными " + str(self.X_Axis_Variable_Name) +
                             " " + str(self.Y_Axis_Variable_Name) +
                             " не найдены. Невозможно построить график, требующий такое название столбцов с данными." +
                             " Проверьте конфигурационные файлы Формулы.txt, Графики_ВАХ.ini, Графики_от_времени.ini\n\n")
                        print(s)
                        return
                if not(self.X_Axis_Variable_Name in df.columns) or not(self.Y_Axis_Variable_Name in df.columns):
                        return
                my_df = df[[self.X_Axis_Variable_Name, self.Y_Axis_Variable_Name]].dropna()
                self.update_last_dot(my_df[self.X_Axis_Variable_Name], my_df[self.Y_Axis_Variable_Name])
                if self.is_trace_left:
                        self.x = np.concatenate([self.x, my_df[self.X_Axis_Variable_Name]])
                        self.y = np.concatenate([self.y, my_df[self.Y_Axis_Variable_Name]])
                        self.scatter.set_offsets(np.column_stack((self.x, self.y)))
                self.set_xy_lims_with_last_dots(self.x, self.y, my_df[self.X_Axis_Variable_Name].tail(), my_df[self.Y_Axis_Variable_Name].tail())
                self.Plot.draw_idle() # draw() вызывает слишком частое мерцание экрана
                return

        def update_last_dot(self, x, y):
                if not(self.last_dot is None):
                        self.last_dot.remove()
                self.last_dot = self.Plot.draw_scatter(
                        x.tail(), y.tail(), #.iloc[-1]
                        color = "red", s = 10)

        
        def setupUi(self, add_buttons = True):
                self.centralwidget = QtWidgets.QWidget()
                
                self.Plot = PyplotWidget()
                for i in range(len(self.PreviousDataFilenamesList_old)):
                        self.drawPreviousFileData_old(filename = self.PreviousDataFilenamesList_old[i],
                                                  color = color_index_to_color(i), alpha = 0.2, s=6)
                for i in range(len(self.PreviousDataFilenamesList_new)):
                        self.drawPreviousFileData_new(filename = self.PreviousDataFilenamesList_new[i],
                                                  color = color_index_to_color(len(self.PreviousDataFilenamesList_old) + i), alpha = 0.2, s=6)
                
                if len(self.PreviousDataFilenamesList_new) + len(self.PreviousDataFilenamesList_old) > 0:
                        self.initial_xy_lims = {"x" : self.Plot.axes.get_xlim(), "y" : self.Plot.axes.get_ylim()}
                
                self.CurrentArtist_ColorIndex = len(self.PreviousDataFilenamesList_old) + len(self.PreviousDataFilenamesList_new)
                self.Plot.setAxisLabel(self.X_Axis_Variable_Name, self.Y_Axis_Variable_Name)
                self.scatter = self.Plot.draw_scatter([],[])

                self.qch_is_trace_left = QtWidgets.QCheckBox(text = "Оставлять след")
                self.qch_is_trace_left.setCheckState(2)
                self.qch_is_trace_left.stateChanged.connect(self.on_push_is_trace_left)
                self.qpb_savefig = QtWidgets.QPushButton(text = "Сохранить график")
                self.qpb_savefig.clicked.connect(self.on_push_save_png)
                self.qhbl_buttons = QtWidgets.QHBoxLayout()
                self.qhbl_buttons.addWidget(self.qch_is_trace_left)
                self.qhbl_buttons.addWidget(self.qpb_savefig)

                #self.qcb_x_label = QtWidgets.QComboBox()
                
                
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
                self.was_no_data_warning_shown = False # a warning about no such axis in data
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
    
