from PyQt5 import QtWidgets
class Button:
    def __init__(on_click, update_ui, update_ui_event):
        qpushbutton = QtWidgets.QPushButton()
        qpushbutton.clicked.connect(on_click)
        update_ui_event

    def on_click(self):
        pass

    def update_ui(self):
        pass

def createButton():
    
    
    
    
