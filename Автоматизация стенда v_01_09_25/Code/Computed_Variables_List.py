import sympy as smp
import pandas as pd
import queue
from sympy.parsing.sympy_parser import parse_expr

class Computed_Variables_List:
    def __init__(self, k = 1):
        self.__variables = list()

    def __apply_function(self, f, values, var_name):
        try:
            value = float(f.evalf(subs = values))
        except Exception as e:
            value = None
        values[var_name] = value

    def __call__(self, values):
        values = values.dropna().to_dict()
        
        for (var_name, f) in self.__variables:
            self.__apply_function(f, values, var_name)
            
        return pd.Series(values)

    def from_txt(self, filename):
        file = open(filename)
        for str_function in file.readlines():
            if str_function[0] == "#":
                continue
            try:
                # let str_function = "V = function(values)"
                eq_index = str_function.find("=")
                var_name = str_function[:eq_index - 1]    # var_name = "V"
                f = parse_expr(str_function[eq_index+1:]) # f = function
                self.__variables.append((var_name, f))
            except Exception as e:
                print('"'+str_function+'"', "ошибка:", e)
        file.close()
        return

def from_txt(filename):
    cvl = Computed_Variables_List()
    cvl.from_txt(filename)
    return cvl

if __name__ == "__main__":
    import sys
    from PyQt5 import QtWidgets
    import MainWindow_CloseEvent
    from Device_Korad_with_str_columns import KORAD_NAMES
    cvl = from_txt("sympy parse.txt")
    print("created CVL")
    values =  {"KORAD_TIME": 0.3832838535308838,
               "<KORAD_NAMES.VOLTAGE: 'Korad_U'>": None,
               "<KORAD_NAMES.CURRENT: 'Korad_I'>": None,
               'LCARD_CH0MEAN': 2.5384615384615383,'LCARD_CH1MEAN': 8.307692307692308, 'LCARD_CH2MEAN': None, 'LCARD_CH3MEAN': None,
               'LCARD_CH0STD' : 3.6080121229410995,'LCARD_CH1STD' : 9.007557642033506, 'LCARD_CH2STD': None, 'LCARD_CH3STD': None,
               'LCARD_CH0MIN': 1.0, 'LCARD_CH1MIN': 0.0, 'LCARD_CH2MIN': None, 'LCARD_CH3MIN': None,
               'LCARD_CH0MAX': 11.0, 'LCARD_CH1MAX': 33.0, 'LCARD_CH2MAX': None, 'LCARD_CH3MAX': None,
               'LCARD_COMP_TIME': 0.3877394199371338}#,
               #'k1': 3200.00000000000, 'k2': 100.000000000000,
               #'U_anode': None, 'I_anode': None, 'I_min': None, 'I_sigma': None}
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow_CloseEvent.MainWindow_withCloseEvent()
    tabs = QtWidgets.QTabWidget()
    hbox = QtWidgets.QHBoxLayout()
    """
    
    hbox.addWidget(Graph2.setupUi())
    hbox.addWidget(Graph1.setupUi())
    hbox.addWidget(LVAC2.setupUi())
    hbox.addWidget(LVT.setupUi())
        tabs.addTab(connections.setupUi(), "Connections")
    tabs.addTab(logger.setupUi(), "Logger")
        MainWindow.CloseEventListeners.append(connections.onCloseEvent)
    MainWindow.CloseEventListeners.append(logger.onCloseEvent)
    """
    hbox_widget = QtWidgets.QWidget()
    hbox_widget.setLayout(hbox)
    tabs.addTab(hbox_widget, "VAC")
    centralwidget = tabs
    MainWindow.setCentralWidget(centralwidget)
    MainWindow.show()
    
    sys.exit(app.exec_())
    print(cvl(pd.Series(values)))
