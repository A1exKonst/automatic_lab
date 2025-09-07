from PyQt5 import QtCore, QtGui, QtWidgets

class LCD_Anode(object):

        def __init__(self, centralwidget):
                self._translate = QtCore.QCoreApplication.translate



        def SetupUI(self, centralwidget):
                self.centralwidget = centralwidget
                self.label_dark_gray_anode = QtWidgets.QLabel(self.centralwidget)
                self.label_dark_gray_anode.setGeometry(QtCore.QRect(0, 0, 241, 51))
                self.label_dark_gray_anode.setStyleSheet("background-color: rgb(134, 134, 134);")
                self.label_dark_gray_anode.setText("")
                self.label_dark_gray_anode.setObjectName("label_dark_gray_anode")
                self.label_mA_for_Ia_anode = QtWidgets.QLabel(self.centralwidget)
                self.label_mA_for_Ia_anode.setGeometry(QtCore.QRect(180, 120, 51, 31))
                self.label_mA_for_Ia_anode.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                         "color: rgb(231, 76, 76)")
                self.label_mA_for_Ia_anode.setObjectName("label_mA_for_Ia_anode")
                self.label_mA_for_sigmaI = QtWidgets.QLabel(self.centralwidget)
                self.label_mA_for_sigmaI.setGeometry(QtCore.QRect(180, 270, 51, 31))
                self.label_mA_for_sigmaI.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                       "color: rgb(231, 76, 76)")
                self.label_mA_for_sigmaI.setObjectName("label_mA_for_sigmaI")
                self.label_mA_for_Imin_anode = QtWidgets.QLabel(self.centralwidget)
                self.label_mA_for_Imin_anode.setGeometry(QtCore.QRect(180, 170, 81, 31))
                self.label_mA_for_Imin_anode.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                           "color: rgb(231, 76, 76)")
                self.label_mA_for_Imin_anode.setObjectName("label_mA_for_Imin_anode")
                self.label_anode = QtWidgets.QLabel(self.centralwidget)
                self.label_anode.setGeometry(QtCore.QRect(83, 0, 91, 51))
                self.label_anode.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                               "color:rgb(255, 255, 255)")
                self.label_anode.setObjectName("label_anode")
                self.label_Ia_anode = QtWidgets.QLabel(self.centralwidget)
                self.label_Ia_anode.setGeometry(QtCore.QRect(16, 120, 21, 31))
                self.label_Ia_anode.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                  "color: rgb(231, 76, 76)")
                self.label_Ia_anode.setObjectName("label_Ia_anode")
                self.line_anode = QtWidgets.QFrame(self.centralwidget)
                self.line_anode.setGeometry(QtCore.QRect(0, 42, 241, 20))
                self.line_anode.setFrameShape(QtWidgets.QFrame.HLine)
                self.line_anode.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_anode.setObjectName("line_anode")
                self.label_sigmaI_anode = QtWidgets.QLabel(self.centralwidget)
                self.label_sigmaI_anode.setGeometry(QtCore.QRect(15, 270, 21, 31))
                self.label_sigmaI_anode.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                      "color: rgb(231, 76, 76)")
                self.label_sigmaI_anode.setObjectName("label_sigmaI_anode")
                self.label_B_for_Ua_anode = QtWidgets.QLabel(self.centralwidget)
                self.label_B_for_Ua_anode.setGeometry(QtCore.QRect(180, 70, 21, 31))
                self.label_B_for_Ua_anode.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                        "color: rgb(231, 76, 76)")
                self.label_B_for_Ua_anode.setObjectName("label_B_for_Ua_anode")
                self.label_light_gray_anode = QtWidgets.QLabel(self.centralwidget)
                self.label_light_gray_anode.setGeometry(QtCore.QRect(0, 0, 241, 321))
                self.label_light_gray_anode.setStyleSheet("background-color: rgb(200, 200, 200);")
                self.label_light_gray_anode.setText("")
                self.label_light_gray_anode.setObjectName("label_light_gray_anode")
                self.label_Imax_anode = QtWidgets.QLabel(self.centralwidget)
                self.label_Imax_anode.setGeometry(QtCore.QRect(17, 220, 21, 31))
                self.label_Imax_anode.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                    "color: rgb(231, 76, 76)")
                self.label_Imax_anode.setObjectName("label_Imax_anode")
                self.label_mA_for_Imax_anode = QtWidgets.QLabel(self.centralwidget)
                self.label_mA_for_Imax_anode.setGeometry(QtCore.QRect(180, 220, 51, 31))
                self.label_mA_for_Imax_anode.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                           "color: rgb(231, 76, 76)")
                self.label_mA_for_Imax_anode.setObjectName("label_mA_for_Imax_anode")
                self.label_Imin_anode = QtWidgets.QLabel(self.centralwidget)
                self.label_Imin_anode.setGeometry(QtCore.QRect(17, 170, 21, 31))
                self.label_Imin_anode.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                    "color: rgb(231, 76, 76)")
                self.label_Imin_anode.setObjectName("label_Imin_anode")
                self.label_Ua_anode = QtWidgets.QLabel(self.centralwidget)
                self.label_Ua_anode.setGeometry(QtCore.QRect(11, 70, 31, 31))
                self.label_Ua_anode.setStyleSheet("font: 500 18pt \"Tahoma\";\n"
                                                  "color: rgb(231, 76, 76)")
                self.label_Ua_anode.setObjectName("label_Ua_anode")
                self.label_28 = QtWidgets.QLabel(self.centralwidget)
                self.label_28.setGeometry(QtCore.QRect(30, 130, 31, 31))
                self.label_28.setStyleSheet("font: 500 10pt \"Tahoma\";\n"
                                            "color: rgb(231, 76, 76)")
                self.label_28.setObjectName("label_28")
                self.label_a_for_U_anode = QtWidgets.QLabel(self.centralwidget)
                self.label_a_for_U_anode.setGeometry(QtCore.QRect(31, 80, 31, 31))
                self.label_a_for_U_anode.setStyleSheet("font: 500 10pt \"Tahoma\";\n"
                                                       "color: rgb(231, 76, 76)")
                self.label_a_for_U_anode.setObjectName("label_a_for_U_anode")
                self.label_30 = QtWidgets.QLabel(self.centralwidget)
                self.label_30.setGeometry(QtCore.QRect(30, 180, 41, 31))
                self.label_30.setStyleSheet("font: 500 10pt \"Tahoma\";\n"
                                            "color: rgb(231, 76, 76)")
                self.label_30.setObjectName("label_30")
                self.label_31 = QtWidgets.QLabel(self.centralwidget)
                self.label_31.setGeometry(QtCore.QRect(30, 230, 41, 31))
                self.label_31.setStyleSheet("font: 500 10pt \"Tahoma\";\n"
                                            "color: rgb(231, 76, 76)")
                self.label_31.setObjectName("label_31")
                self.label_32 = QtWidgets.QLabel(self.centralwidget)
                self.label_32.setGeometry(QtCore.QRect(33, 280, 16, 31))
                self.label_32.setStyleSheet("font: 500 10pt \"Tahoma\";\n"
                                            "color: rgb(231, 76, 76)")
                self.label_32.setObjectName("label_32")

                self.lcdnumber_sigmaI_anode = QtWidgets.QLCDNumber(self.centralwidget)
                self.lcdnumber_sigmaI_anode.setGeometry(QtCore.QRect(70, 270, 101, 31))
                self.lcdnumber_sigmaI_anode.setStyleSheet("background-color: rgb(59, 59, 59);\n"
                                                          "color: rgb(255, 0, 0);")
                self.lcdnumber_sigmaI_anode.setObjectName("lcdnumber_sigmaI_anode")
                self.lcdnumber_Ua_anode = QtWidgets.QLCDNumber(self.centralwidget)
                self.lcdnumber_Ua_anode.setGeometry(QtCore.QRect(70, 70, 101, 31))
                self.lcdnumber_Ua_anode.setStyleSheet("background-color: rgb(59, 59, 59);\n"
                                                      "color: rgb(255, 0, 0);")
                self.lcdnumber_Ua_anode.setObjectName("lcdnumber_Ua_anode")
                self.lcdnumber_Imin_anode = QtWidgets.QLCDNumber(self.centralwidget)
                self.lcdnumber_Imin_anode.setGeometry(QtCore.QRect(70, 170, 101, 31))
                self.lcdnumber_Imin_anode.setStyleSheet("background-color: rgb(59, 59, 59);\n"
                                                        "color: rgb(255, 0, 0);")
                self.lcdnumber_Imin_anode.setObjectName("lcdnumber_Imin_anode")
                self.lcdnumber_Imax_anode = QtWidgets.QLCDNumber(self.centralwidget)
                self.lcdnumber_Imax_anode.setGeometry(QtCore.QRect(70, 220, 101, 31))
                self.lcdnumber_Imax_anode.setStyleSheet("background-color: rgb(59, 59, 59);\n"
                                                        "color: rgb(255, 0, 0);")
                self.lcdnumber_Imax_anode.setObjectName("lcdnumber_Imax_anode")
                self.lcdnumber_Ia_anode = QtWidgets.QLCDNumber(self.centralwidget)
                self.lcdnumber_Ia_anode.setGeometry(QtCore.QRect(70, 120, 101, 31))
                self.lcdnumber_Ia_anode.setStyleSheet("background-color: rgb(59, 59, 59);\n"
                                                      "color: rgb(255, 0, 0);")
                self.lcdnumber_Ia_anode.setObjectName("lcdnumber_Ia_anode")
                
                self.label_light_gray_anode.raise_()
                self.label_dark_gray_anode.raise_()
                self.label_mA_for_Ia_anode.raise_()
                self.label_mA_for_sigmaI.raise_()
                self.label_mA_for_Imin_anode.raise_()
                self.label_anode.raise_()
                self.label_Ia_anode.raise_()
                self.line_anode.raise_()
                self.label_sigmaI_anode.raise_()
                self.label_B_for_Ua_anode.raise_()
                self.label_Imax_anode.raise_()
                self.label_mA_for_Imax_anode.raise_()
                self.label_Imin_anode.raise_()
                self.label_Ua_anode.raise_()
                self.label_28.raise_()
                self.label_a_for_U_anode.raise_()
                self.label_30.raise_()
                self.label_31.raise_()
                self.label_32.raise_()
                self.lcdnumber_sigmaI_anode.raise_()
                self.lcdnumber_Ua_anode.raise_()
                self.lcdnumber_Imin_anode.raise_()
                self.lcdnumber_Imax_anode.raise_()
                self.lcdnumber_Ia_anode.raise_()
                
                _translate = QtCore.QCoreApplication.translate
                
                self.label_mA_for_Ia_anode.setText(_translate("MainWindow", "mA"))
                self.label_mA_for_sigmaI.setText(_translate("MainWindow", "mA"))
                self.label_mA_for_Imin_anode.setText(_translate("MainWindow", "mA"))
                self.label_anode.setText(_translate("MainWindow", "Анод"))
                self.label_Ia_anode.setText(_translate("MainWindow", "I"))
                self.label_sigmaI_anode.setText(_translate("MainWindow", "o"))
                self.label_B_for_Ua_anode.setText(_translate("MainWindow", "B"))
                self.label_Imax_anode.setText(_translate("MainWindow", "I"))
                self.label_mA_for_Imax_anode.setText(_translate("MainWindow", "mA"))
                self.label_Imin_anode.setText(_translate("MainWindow", "I"))
                self.label_Ua_anode.setText(_translate("MainWindow", "U"))
                self.label_28.setText(_translate("MainWindow", "a"))
                self.label_a_for_U_anode.setText(_translate("MainWindow", "a"))
                self.label_30.setText(_translate("MainWindow", "min"))
                self.label_31.setText(_translate("MainWindow", "max"))

        def Display(self, Ua, Ia, Imin, sigmaI):
                if (isinstance(Ua, float) or isinstance(Ua, int)):
                        self.lcdnumber_Ua_anode.display("{:05.3f}".format(Ua))
                s = str(Ia)
                if (s.isnumeric()):
                        self.lcdnumber_Ia_anode.display("{:05.3f}".format(float(s)))
                s = str(Imin)
                if (s.isnumeric()):
                        self.lcdnumber_Imin_anode.display("{:05.3f}".format(float(s)))
                s = str(sigmaI)
                if (s.isnumeric()):
                        self.lcdnumber_sigmaI_anode.display("{:05.3f}".format(float(s)))
                return
        
