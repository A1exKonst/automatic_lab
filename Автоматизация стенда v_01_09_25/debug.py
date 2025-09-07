import sys
import os
import pathlib
import configparser
import pandas as pd
from PyQt5 import QtWidgets
from Code import (Tab_Logger, Tab_Device_Connections,
                  Tab_Graph_with_previous_data, tab_graph_running,
                  MainWindow_CloseEvent)
from Code.CommandTable import device_controller, device_controller_gui
from Code import Tab_Lcard_VAC_GUI as l_vac_gui

app = QtWidgets.QApplication(sys.argv)
MainWindow = MainWindow_CloseEvent.MainWindow_withCloseEvent()


graph = tab_graph_running.TabGraphRunning("x", "y")
k = graph.setupUi()

MainWindow.setCentralWidget(k)
MainWindow.show()

sys.exit(app.exec_())


