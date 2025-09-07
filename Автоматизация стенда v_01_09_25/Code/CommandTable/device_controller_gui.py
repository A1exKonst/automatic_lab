from PyQt5 import QtWidgets, QtCore

class DeviceControllerGui:
    def __init__(self, device_controller, logger = None):
        self.device_controller = device_controller
        self.dc_on_finish = self.device_controller.on_finish
        self.device_controller.on_finish = self.on_finish
        self.logger = logger
        
    def setup_ui(self):
        self.centralwidget = QtWidgets.QWidget()
        # CommandTable : Start-Stop Buttons
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setStyleSheet("font: 75 18pt \"Tahoma\";")
        self.pushButton_start.setObjectName("pushButton_start")
        self.pushButton_start.setGeometry(QtCore.QRect(400, 850, 500, 50))
        # CommandTable : Filename
        self.QLabel_CommandTableFilename = QtWidgets.QLabel("Файл командной таблицы:", self.centralwidget)
        self.QLabel_CommandTableFilename.setGeometry(QtCore.QRect(270, 750, 500, 40))
        self.QLabel_CommandTableFilename.setStyleSheet("font: 75 15pt \"Tahoma\";")
        self.QLineEdit_CommandTableFilename = QtWidgets.QLineEdit(parent = self.centralwidget)
        self.QLineEdit_CommandTableFilename.setGeometry(QtCore.QRect(650, 750, 500, 50))
        self.QLineEdit_CommandTableFilename.setStyleSheet("font: 75 12pt \"Tahoma\";")
        self.QLineEdit_CommandTableFilename.setText("Пользовательские конфигурации/Пример_управляющей_таблицы.csv")
        # Connections
        self.pushButton_start.clicked.connect(self.click)
        # Layout
        self.QLayoutCommandTable = QtWidgets.QVBoxLayout(self.centralwidget)
        self.QLayoutCommandTable.addWidget(self.QLabel_CommandTableFilename)
        self.QLayoutCommandTable.addWidget(self.QLineEdit_CommandTableFilename)
        self.QLayoutCommandTable.addWidget(self.pushButton_start)
        self.centralwidget.setLayout(self.QLayoutCommandTable)
        # first update
        self.update_gui()
        return self.centralwidget

    def update_gui(self):
        state = self.device_controller.is_active_execution
        self.QLineEdit_CommandTableFilename.setEnabled(not(state))
        if state:
            self.pushButton_start.setText("Стоп таблицы команд")
        else:
            self.pushButton_start.setText("Старт таблицы команд")

    def click(self):
        print("DeviceControllerGui.click call")
        if self.device_controller.is_active_execution:
            self.device_controller.interrupt_table_execution()
        else:
            try:
                filename = self.QLineEdit_CommandTableFilename.text()
                self.device_controller.add_commands_from_csv(filename)
                self.device_controller.start_table_execution()
            except Exception as e:
                print(e)
        self.update_gui()
        
    def on_finish(self):
        self.dc_on_finish()
        self.update_gui()
