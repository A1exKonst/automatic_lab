from PyQt5 import QtCore, QtGui, QtWidgets

class LCD_Filament(object):

        def __init__(self, centralwidget):
                self._translate = QtCore.QCoreApplication.translate



        def SetupUI(self, centralwidget):
                self.centralwidget = centralwidget
                
                self.label_light_gray_filament = QtWidgets.QLabel(self.centralwidget)
                self.label_light_gray_filament.setGeometry(QtCore.QRect(0, 0, 241, 321))
                self.label_light_gray_filament.setStyleSheet("background-color: rgb(200, 200, 200);")
                self.label_light_gray_filament.setText("")
                self.label_light_gray_filament.setObjectName("label_light_gray_filament")
                self.label_filament = QtWidgets.QLabel(self.centralwidget)
                self.label_filament.setGeometry(QtCore.QRect(84, 0, 140, 51))
                self.label_filament.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                  "color:rgb(255, 255, 255)")
                self.label_filament.setObjectName("label_filament")
                self.label_dark_gray_filament = QtWidgets.QLabel(self.centralwidget)
                self.label_dark_gray_filament.setGeometry(QtCore.QRect(0, 0, 241, 51))
                self.label_dark_gray_filament.setStyleSheet("background-color: rgb(134, 134, 134);")
                self.label_dark_gray_filament.setText("")
                self.label_dark_gray_filament.setObjectName("label_dark_gray_filament")
                self.label_I_filament = QtWidgets.QLabel(self.centralwidget)
                self.label_I_filament.setGeometry(QtCore.QRect(20, 70, 31, 31))
                self.label_I_filament.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                    "color: rgb(231, 76, 76)")
                self.label_I_filament.setObjectName("label_I_filament")
                self.line_filament = QtWidgets.QFrame(self.centralwidget)
                self.line_filament.setGeometry(QtCore.QRect(0, 42, 241, 20))
                self.line_filament.setFrameShape(QtWidgets.QFrame.HLine)
                self.line_filament.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_filament.setObjectName("line_filament")
                self.label_A_filament = QtWidgets.QLabel(self.centralwidget)
                self.label_A_filament.setGeometry(QtCore.QRect(180, 70, 21, 31))
                self.label_A_filament.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                    "color: rgb(231, 76, 76)")
                self.label_A_filament.setObjectName("label_A_filament")
                self.lcdNumber_I_filament = QtWidgets.QLCDNumber(self.centralwidget)
                self.lcdNumber_I_filament.setGeometry(QtCore.QRect(70, 70, 101, 31))
                self.lcdNumber_I_filament.setStyleSheet("background-color: rgb(59, 59, 59);\n"
                                                        "color: rgb(255, 0, 0);")
                self.lcdNumber_I_filament.setObjectName("lcdNumber_I_filament")
                self.label_B_filament = QtWidgets.QLabel(self.centralwidget)
                self.label_B_filament.setGeometry(QtCore.QRect(180, 120, 21, 31))
                self.label_B_filament.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                    "color: rgb(231, 76, 76)")
                self.label_B_filament.setObjectName("label_B_filament")
                self.label_U_filament = QtWidgets.QLabel(self.centralwidget)
                self.label_U_filament.setGeometry(QtCore.QRect(15, 120, 31, 31))
                self.label_U_filament.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                    "color: rgb(231, 76, 76)")
                self.label_U_filament.setObjectName("label_U_filament")
                self.label_mO_filament = QtWidgets.QLabel(self.centralwidget)
                self.label_mO_filament.setGeometry(QtCore.QRect(177, 170, 81, 31))
                self.label_mO_filament.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                     "color: rgb(231, 76, 76)")
                self.label_mO_filament.setObjectName("label_mO_filament")
                self.label_R_filament = QtWidgets.QLabel(self.centralwidget)
                self.label_R_filament.setGeometry(QtCore.QRect(18, 170, 31, 31))
                self.label_R_filament.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                    "color: rgb(231, 76, 76)")
                self.label_R_filament.setObjectName("label_R_filament")
                self.label_W_filament = QtWidgets.QLabel(self.centralwidget)
                self.label_W_filament.setGeometry(QtCore.QRect(180, 220, 41, 31))
                self.label_W_filament.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                    "color: rgb(231, 76, 76)")
                self.label_W_filament.setObjectName("label_W_filament")
                self.label_P_filament = QtWidgets.QLabel(self.centralwidget)
                self.label_P_filament.setGeometry(QtCore.QRect(19, 220, 31, 31))
                self.label_P_filament.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                    "color: rgb(231, 76, 76)")
                self.label_P_filament.setObjectName("label_P_filament")
                self.label_K_filament = QtWidgets.QLabel(self.centralwidget)
                self.label_K_filament.setGeometry(QtCore.QRect(180, 270, 21, 31))
                self.label_K_filament.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                    "color: rgb(231, 76, 76)")
                self.label_K_filament.setObjectName("label_K_filament")
                self.label_T_filament = QtWidgets.QLabel(self.centralwidget)
                self.label_T_filament.setGeometry(QtCore.QRect(18, 270, 31, 31))
                self.label_T_filament.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                    "color: rgb(231, 76, 76)")
                self.label_T_filament.setObjectName("label_T_filament")

                self.lcdNumber_U_filament = QtWidgets.QLCDNumber(self.centralwidget)
                self.lcdNumber_U_filament.setGeometry(QtCore.QRect(70, 120, 101, 31))
                self.lcdNumber_U_filament.setStyleSheet("background-color: rgb(59, 59, 59);\n"
                                                        "color: rgb(255, 0, 0);")
                self.lcdNumber_U_filament.setObjectName("lcdNumber_U_filament")
                self.lcdNumber_R_filament = QtWidgets.QLCDNumber(self.centralwidget)
                self.lcdNumber_R_filament.setGeometry(QtCore.QRect(70, 170, 101, 31))
                self.lcdNumber_R_filament.setStyleSheet("background-color: rgb(59, 59, 59);\n"
                                                        "color: rgb(255, 0, 0);")
                self.lcdNumber_R_filament.setObjectName("lcdNumber_R_filament")
                self.lcdNumber_P_filament = QtWidgets.QLCDNumber(self.centralwidget)
                self.lcdNumber_P_filament.setGeometry(QtCore.QRect(70, 220, 101, 31))
                self.lcdNumber_P_filament.setStyleSheet("background-color: rgb(59, 59, 59);\n"
                                                        "color: rgb(255, 0, 0);")
                self.lcdNumber_P_filament.setObjectName("lcdNumber_P_filament")
                self.lcdNumber_T_filament = QtWidgets.QLCDNumber(self.centralwidget)
                self.lcdNumber_T_filament.setGeometry(QtCore.QRect(70, 270, 101, 31))
                self.lcdNumber_T_filament.setStyleSheet("background-color: rgb(59, 59, 59);\n"
                                                        "color: rgb(255, 0, 0);")
                self.lcdNumber_T_filament.setObjectName("lcdNumber_T_filament")

                #self.label_light_gray_anode.raise_()
                self.label_light_gray_filament.raise_()
                self.label_dark_gray_filament.raise_()
                self.label_filament.raise_()
                self.label_I_filament.raise_()
                self.line_filament.raise_()
                self.label_A_filament.raise_()
                self.lcdNumber_I_filament.raise_()
                self.label_B_filament.raise_()
                self.label_U_filament.raise_()
                self.label_mO_filament.raise_()
                self.label_R_filament.raise_()
                self.label_W_filament.raise_()
                self.label_P_filament.raise_()
                self.label_K_filament.raise_()
                self.label_T_filament.raise_()

                self.lcdNumber_U_filament.raise_()
                self.lcdNumber_R_filament.raise_()
                self.lcdNumber_P_filament.raise_()
                self.lcdNumber_T_filament.raise_()
                
                self.label_filament.setText(self._translate("MainWindow", "Накал"))
                self.label_I_filament.setText(self._translate("MainWindow", "I"))
                self.label_A_filament.setText(self._translate("MainWindow", "A"))
                self.label_B_filament.setText(self._translate("MainWindow", "B"))
                self.label_U_filament.setText(self._translate("MainWindow", "U"))
                self.label_mO_filament.setText(self._translate("MainWindow", "mO"))
                self.label_R_filament.setText(self._translate("MainWindow", "R"))
                self.label_W_filament.setText(self._translate("MainWindow", "W"))
                self.label_P_filament.setText(self._translate("MainWindow", "P"))
                self.label_K_filament.setText(self._translate("MainWindow", "K"))
                self.label_T_filament.setText(self._translate("MainWindow", "T"))

        def Update_U_I(self, U = None, I = None):
                i = str(I)
                if (i.isnumeric()):
                        self.lcdNumber_I_filament.display("{:05.3f}".format(float(i)))
                u = str(U)
                if (u.isnumeric()):
                        self.lcdNumber_U_filament.display("{:05.3f}".format(float(u)))
                if (u.isnumeric() and i.isnumeric()):
                        if (float(i) != 0):
                                self.lcdNumber_R_filament.display("{:05.3f}".format(float(u) / float(i)))
                        self.lcdNumber_P_filament.display("{:05.3f}".format(float(u)*float(i)))

