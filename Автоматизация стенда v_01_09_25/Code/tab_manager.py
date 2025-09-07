import sys
import os
import pathlib
from PyQt5 import QtWidgets
from Code import MainWindow_CloseEvent
from Code import Tab_Logger, Tab_Device_Connections
from Code import Tab_Graph_with_previous_data

def addGraph(logger, x_name, y_name, filename = None):
    Graph = Tab_Graph_with_previous_data.Tab_Graph_with_previous_data(
        X_Axis_Variable_Name = x_name, Y_Axis_Variable_Name = y_name,
        filename = filename)
    logger.DataPieceListeners.append(Graph.addDataPiece)
    logger.StartLogListeners.append(Graph.startPlotUpdate)
    logger.StopLogListeners.append(Graph.stopPlotUpdate)
    return Graph

class Tab_Manager:
    def __init__(self):
        self.chosen_auth = None

    def start_auth_tab(self):
        path = pathlib.Path('User Configs')
        folder_names = [folder.name for folder in path.iterdir()
               if folder.is_dir()]
        print(folder_names)
    
        self.app = QtWidgets.QApplication(sys.argv)
        self.AuthWindow = MainWindow_CloseEvent.MainWindow_withCloseEvent()
        self.QCB = QtWidgets.QComboBox()
        self.QCB.addItems(folder_names)
        QPB = QtWidgets.QPushButton()
        QPB.setText("Вход")
        QPB.clicked.connect(self.auth_chosen)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.QCB)
        vbox.addWidget(QPB)
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(vbox)
        self.AuthWindow.setCentralWidget(central_widget)
        self.AuthWindow.show()
        sys.exit(self.app.exec_())

    def auth_chosen(self):
        if not(self.chosen_auth is None):
            return
        self.chosen_auth = self.QCB.currentText()
        print(self.chosen_auth)
        try:
            self.start_app()
        except Exception as e:
            print(e)

    def start_app(self):
        connections = Tab_Device_Connections.TabDeviceConnections()
        logger = Tab_Logger.TabLogger(lcard_device = connections.myLcard_Device,
                                      korad_device = connections.myKorad_Device,
                                      CVL_filename = "Code/sympy parse.txt")
        Graph1 = addGraph(logger, "U_anode", "I_anode",
                          filename = "User Configs/setup - graph previous data - 1.csv")
        Graph2 = addGraph(logger, "LCARD_COMP_TIME", "U_anode",
                          filename = "User Configs/setup - graph previous data - 1.csv")

        self.MainWindow = MainWindow_CloseEvent.MainWindow_withCloseEvent()
        tabs = QtWidgets.QTabWidget(self.MainWindow)
        tabs.addTab(connections.setupUi(), "Connections")
        tabs.addTab(logger.setupUi(), "Logger")
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(Graph2.setupUi())
        hbox.addWidget(Graph1.setupUi())

        hbox_widget = QtWidgets.QWidget(self.MainWindow)
        hbox_widget.setLayout(hbox)
        tabs.addTab(hbox_widget, "VAC")
        centralwidget = tabs
        self.MainWindow.setCentralWidget(centralwidget)
        self.MainWindow.CloseEventListeners.append(connections.onCloseEvent)
        self.MainWindow.CloseEventListeners.append(logger.onCloseEvent)
        self.MainWindow.show()


if __name__ == "__main__":
    t = Tab_Manager()
    t.start_auth_tab()
