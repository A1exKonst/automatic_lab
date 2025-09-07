from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, pyqtSignal

class MainWindow_withCloseEvent(QtWidgets.QMainWindow):
        def __init__(self):
                super().__init__()
                self.CloseEventListeners = []
        
        def closeEvent(self, event):
                for listener in self.CloseEventListeners:
                        listener()
                event.accept()


def p():
    print("slot executed")

if __name__ == "__main__":
    import sys 
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow_withCloseEvent()
    MainWindow.closing.connect(p)
    MainWindow.show()
    sys.exit(app.exec_())
