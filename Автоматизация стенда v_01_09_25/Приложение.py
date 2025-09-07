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

def addGraph(logger, x_name, y_name, old_data = None):
    Graph = Tab_Graph_with_previous_data.Tab_Graph_with_previous_data(
        X_Axis_Variable_Name = x_name, Y_Axis_Variable_Name = y_name,
        old_data = old_data)
    logger.DataPieceListeners.append(Graph.addDataPiece)
    logger.StartLogListeners.append(Graph.startPlotUpdate)
    logger.StopLogListeners.append(Graph.stopPlotUpdate)
    return Graph

def add_running_graph(logger, x_name, y_name, displayed_dots_amount = 30):
    graph = tab_graph_running.TabGraphRunning(
        X_Axis_Variable_Name = x_name, Y_Axis_Variable_Name = y_name,
        displayed_dots_amount = displayed_dots_amount)
    logger.DataPieceListeners.append(graph.addDataPiece)
    logger.StartLogListeners.append(graph.startPlotUpdate)
    logger.StopLogListeners.append(graph.stopPlotUpdate)
    return graph

if __name__ == "__main__":

    # Заготовка для выбора ini файлов в зависимости от пользователя.
    path = pathlib.Path('Пользовательские конфигурации')
    folders = [folder.name for folder in path.iterdir()
               if folder.is_dir()]
    print(folders)
    chosen_folder = 'Пользовательские конфигурации'
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow_CloseEvent.MainWindow_withCloseEvent()
    tabs = QtWidgets.QTabWidget()
    #__________________________________________TAB 0_______________________________________________
    connections = Tab_Device_Connections.TabDeviceConnections(
        korad_ini = chosen_folder + "/Korad.ini",
        lcard_ini = chosen_folder + "/LcardE2010B.ini")

    my_device_controller = device_controller.create_command_table_with_device_commands(
        korad_device = connections.myKorad_Device,
        lcard_device = connections.myLcard_Device)
    my_device_controller_gui = device_controller_gui.DeviceControllerGui(my_device_controller)

    logger = Tab_Logger.TabLogger(
        config_filename = chosen_folder + "/Лог.ini",
        lcard_device = connections.myLcard_Device,
        korad_device = connections.myKorad_Device,
        CVL_filename = chosen_folder + "/Формулы.txt"
        )
    
    tab1 = QtWidgets.QWidget()
    vbox1 = QtWidgets.QVBoxLayout()
    vbox1.addWidget(connections.setupUi())
    hbox1 = QtWidgets.QHBoxLayout()
    hbox1.addWidget(logger.setupUi())
    hbox1.addStretch()
    hbox1.addWidget(my_device_controller_gui.setup_ui())
    vbox1.addLayout(hbox1)
    tab1.setLayout(vbox1)
    tabs.addTab(tab1, "Настройки")

    #______________________________TAB 1________________________________________
    config = configparser.ConfigParser()
    config.read(chosen_folder + "/Графики_ВАХ.ini", encoding="utf-8")
    Graph11 = addGraph(logger, config["График 1"]["X"], config["График 1"]["Y"],
                      old_data = config["График 1"]["Старые_данные"])
    Graph12 = addGraph(logger, config["График 2"]["X"], config["График 2"]["Y"],
                      old_data = config["График 2"]["Старые_данные"])
    tab1 = QtWidgets.QWidget()
    hbox1 = QtWidgets.QHBoxLayout()
    gr12 = Graph12.setupUi()
    gr11 = Graph11.setupUi()
    gr11.setMinimumSize(400, 700)
    gr12.setMinimumSize(400, 700)
    hbox1.addWidget(gr12)
    hbox1.addWidget(gr11)
    vbox1 = QtWidgets.QVBoxLayout()
    vbox1.addLayout(hbox1)
    hbox1_buttons = QtWidgets.QHBoxLayout()
    hbox1_buttons.addWidget(logger.setup_qpb_start_log())

    vbox1.addLayout(hbox1_buttons)
    #vbox2.addStretch() - чтобы графики были больше
    tab1.setLayout(vbox1)
    tabs.addTab(tab1, "ВАХи")
    tabs.setStyleSheet("font: 35 12pt \"Tahoma\";")
    #tabs.setStyleSheet("background-color: gray;")
    #tabs.setFont()

    def set_is_tab_1_updated(is_updated):
        Graph11.is_displayed = is_updated
        Graph12.is_displayed = is_updated
        return
    
    #_________________________________TAB 2_____________________________________
    config = configparser.ConfigParser()
    config.read(chosen_folder + "/Графики_от_времени.ini", encoding="utf-8")
    Graph21 = addGraph(logger, config["График 1"]["X"], config["График 1"]["Y"],
                      old_data = config["График 1"]["Старые_данные"])
    Graph22 = addGraph(logger, config["График 2"]["X"], config["График 2"]["Y"],
                      old_data = config["График 2"]["Старые_данные"])
    Graph23 = addGraph(logger, config["График 3"]["X"], config["График 3"]["Y"],
                      old_data = config["График 3"]["Старые_данные"])
    Graph24 = addGraph(logger, config["График 4"]["X"], config["График 4"]["Y"],
                      old_data = config["График 4"]["Старые_данные"])
    #Graph21 = addGraph(logger, "KORAD_TIME", "KORAD_U")
    #Graph22 = addGraph(logger, "KORAD_TIME", "KORAD_I")
    #Graph23 = addGraph(logger, "KORAD_TIME", "U_anode_V")
    #Graph24 = addGraph(logger, "KORAD_TIME", "I_anode_uA")

    from datetime import datetime 
    def on_push_save_tab2(self):
        try:
            Graph21.Plot.fig.savefig(("Данные/График_от_времени_1 " + str(datetime.now()) + ".png").replace(":","_"))
            Graph22.Plot.fig.savefig(("Данные/График_от_времени_2 " + str(datetime.now()) + ".png").replace(":","_"))
            Graph23.Plot.fig.savefig(("Данные/График_от_времени_3 " + str(datetime.now()) + ".png").replace(":","_"))
            Graph24.Plot.fig.savefig(("Данные/График_от_времени_4 " + str(datetime.now()) + ".png").replace(":","_"))
        except Exception as e:
            print(e)
    qpb_save_tab2 = QtWidgets.QPushButton(text = "Сохранить графики")
    qpb_save_tab2.clicked.connect(on_push_save_tab2)
    
    vbox2 = QtWidgets.QVBoxLayout()
    vbox2.addWidget(Graph21.setupUi(add_buttons = False))
    vbox2.addWidget(Graph22.setupUi(add_buttons = False))
    vbox2.addWidget(Graph23.setupUi(add_buttons = False))
    vbox2.addWidget(Graph24.setupUi(add_buttons = False))
    vbox2.addWidget(qpb_save_tab2)
    tab2 = QtWidgets.QWidget()
    tab2.setLayout(vbox2)
    tabs.addTab(tab2, "Графики от времени")

    def set_is_tab_2_updated(is_updated):
        Graph21.is_displayed = is_updated
        Graph22.is_displayed = is_updated
        Graph23.is_displayed = is_updated
        Graph24.is_displayed = is_updated
        return

    #_________________________________TAB 3_____________________________________
    #Graph31 = add_running_graph(logger, "KORAD_TIME", "KORAD_U", displayed_dots_amount = 500)
    #Graph32 = add_running_graph(logger, "KORAD_TIME", "KORAD_I", displayed_dots_amount = 500)
    #Graph33 = add_running_graph(logger, "KORAD_TIME", "U_anode_V", displayed_dots_amount = 500)
    #Graph34 = add_running_graph(logger, "KORAD_TIME", "I_anode_uA", displayed_dots_amount = 500)

    Graph31 = add_running_graph(logger, config["График 1"]["X"], config["График 1"]["Y"], displayed_dots_amount = 20)
    Graph32 = add_running_graph(logger, config["График 2"]["X"], config["График 2"]["Y"], displayed_dots_amount = 20)
    Graph33 = add_running_graph(logger, config["График 3"]["X"], config["График 3"]["Y"], displayed_dots_amount = 20)
    Graph34 = add_running_graph(logger, config["График 4"]["X"], config["График 4"]["Y"], displayed_dots_amount = 20)
    gbox3 = QtWidgets.QGridLayout()
    gbox3.addWidget(Graph31.setupUi(add_buttons = False), 0,0)
    gbox3.addWidget(Graph32.setupUi(add_buttons = False), 0,1)
    gbox3.addWidget(Graph33.setupUi(add_buttons = False), 1,0)
    gbox3.addWidget(Graph34.setupUi(add_buttons = False), 1,1)
    vbox3 = QtWidgets.QVBoxLayout()
    vbox3.addLayout(gbox3)
    vbox3.addWidget(logger.setup_qpb_start_log())
    tab3 = QtWidgets.QWidget()
    tab3.setLayout(vbox3)
    tabs.addTab(tab3, "Текущие данные")

    def set_is_tab_3_updated(is_updated):
        Graph31.is_displayed = is_updated
        Graph32.is_displayed = is_updated
        Graph33.is_displayed = is_updated
        Graph34.is_displayed = is_updated
        return

    def set_is_default_tab_updated(is_updated):
        return
    
    #___________________________________ALL TABS________________________________
    
    lvac_full_buffers_gui = l_vac_gui.LcardVACPlot_Interface(connections.myLcard_Device)
    tabs.addTab(lvac_full_buffers_gui.setupUI(), "Данные с Lcard")
    
    global current_tab_index
    current_tab_index = 0
    all_tab_updates = [
        set_is_default_tab_updated, set_is_tab_1_updated, set_is_tab_2_updated,
        set_is_tab_3_updated, set_is_default_tab_updated]
    
    def on_tab_changed(new_tab_index):
        global current_tab_index
        all_tab_updates[current_tab_index](False)
        current_tab_index = new_tab_index
        all_tab_updates[current_tab_index](True)
    
    tabs.currentChanged.connect(on_tab_changed)
    
    centralwidget = tabs
    MainWindow.setCentralWidget(centralwidget)
    MainWindow.CloseEventListeners.append(connections.onCloseEvent)
    MainWindow.CloseEventListeners.append(logger.onCloseEvent)
    MainWindow.show()

    connections.onAppStart()
    
    sys.exit(app.exec_())
    
"""
    def update_is_log_written_to_file():
        logger.set_log_written_to_file(Graph1.is_trace_left or Graph2.is_trace_left)
    Graph1.qch_is_trace_left.stateChanged.connect(update_is_log_written_to_file)
    Graph2.qch_is_trace_left.stateChanged.connect(update_is_log_written_to_file)
    QpB_AddPermanentGraphData = QtWidgets.QPushButton()
    QpB_AddPermanentGraphData.setText("Добавить данные \n в постоянно отображаемые")
    QpB_AddPermanentGraphData.setMinimumSize(100, 110)
    def onPush_AddPermanentGraphData():
        try:
            print("call onPush_AddPermanentGraphData")
            if not(isinstance(logger.LogFilename, str)):
                return
            for gfn in Graph_filenames:
                idf = pd.read_csv(gfn, delimiter = ";")
                if logger.LogFilename in idf["New Version Data Filenames List"]:
                    continue
                s = pd.Series({"New Version Data Filenames List" : logger.LogFilename})
                idf = pd.concat([idf, s.to_frame().T], ignore_index = True)
                idf.drop(idf.columns[idf.columns.str.contains('unnamed', case = False)], axis = 1, inplace = True)
                idf.drop_duplicates(inplace = True, ignore_index = True)
                idf.to_csv(gfn,sep = ";")
        except Exception as e:
            print(e)
    QpB_AddPermanentGraphData.clicked.connect(onPush_AddPermanentGraphData)
    hbox2_buttons.addWidget(QpB_AddPermanentGraphData)
"""
