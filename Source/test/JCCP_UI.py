# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'JCCP.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import  QMessageBox
import serial
import serial.tools.list_ports
import Data

Serial_Port = serial.Serial()
Timer_ReadMessage = QTimer()
Timer_Measurement = QTimer()

Par_Charge_Flag = 0

Measurement_Step = 0
Measurement_Status = 0
Communicate_Count = 0
Uart_Buffer = [0 for i in range(512)]
Uart_Buffer_Count = 0

Hex_Dict = {
    '0':0,
    '1':1,
    '2':2,
    '3':3,
    '4':4,
    '5':5,
    '6':6,
    '7':7,
    '8':8,
    '9':9,
    'A':10,
    'B':11,
    'C':12,
    'D':13,
    'E':14,
    'F':15
}

def Hex2Dec(x):
    num = 0
    x = str(x)
    # MainWindows.Data_Show.append(str(len(x)))
    for i in range(len(x)):
        str2 = x[i]
        str2 = str2.upper()
    #     MainWindows.Data_Show.append(str(str2))
        try:
            num += Hex_Dict[str2]*pow(16,(len(x)-i-1))
        except:
            return u'NULL'
        # MainWindows.Data_Show.append(str(str2))
    return num

def Dec2Hex(str):
    num = hex(str)[2:]
    return num

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1031, 793)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_10.addWidget(self.label_23)
        self.label_37 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_37.setFont(font)
        self.label_37.setText("")
        self.label_37.setObjectName("label_37")
        self.horizontalLayout_10.addWidget(self.label_37)
        self.label_35 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_35.setFont(font)
        self.label_35.setText("")
        self.label_35.setObjectName("label_35")
        self.horizontalLayout_10.addWidget(self.label_35)
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_10.addWidget(self.label_24)
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_10.addWidget(self.label_25)
        self.gridLayout.addLayout(self.horizontalLayout_10, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout.addWidget(self.label_15)
        self.lineEdit_15 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_15.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_15.setFont(font)
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.horizontalLayout.addWidget(self.lineEdit_15)
        self.label_26 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.horizontalLayout.addWidget(self.label_26)
        self.label_34 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_34.setFont(font)
        self.label_34.setAutoFillBackground(True)
        self.label_34.setObjectName("label_34")
        self.horizontalLayout.addWidget(self.label_34)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_2.addWidget(self.lineEdit_4)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_2.addWidget(self.lineEdit_3)
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_2.addWidget(self.label_16)
        self.lineEdit_16 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_16.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_16.setFont(font)
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.horizontalLayout_2.addWidget(self.lineEdit_16)
        self.label_27 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_2.addWidget(self.label_27)
        self.label_36 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_36.setFont(font)
        self.label_36.setAutoFillBackground(True)
        self.label_36.setObjectName("label_36")
        self.horizontalLayout_2.addWidget(self.label_36)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_8.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.horizontalLayout_3.addWidget(self.lineEdit_8)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_3.addWidget(self.label_8)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_7.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.horizontalLayout_3.addWidget(self.lineEdit_7)
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_3.addWidget(self.label_18)
        self.lineEdit_18 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_18.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_18.setFont(font)
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.horizontalLayout_3.addWidget(self.lineEdit_18)
        self.label_28 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_3.addWidget(self.label_28)
        self.label_38 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_38.setFont(font)
        self.label_38.setAutoFillBackground(True)
        self.label_38.setObjectName("label_38")
        self.horizontalLayout_3.addWidget(self.label_38)
        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.horizontalLayout_4.addWidget(self.lineEdit_6)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_4.addWidget(self.lineEdit_5)
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_4.addWidget(self.label_19)
        self.lineEdit_19 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_19.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_19.setFont(font)
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.horizontalLayout_4.addWidget(self.lineEdit_19)
        self.label_29 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.horizontalLayout_4.addWidget(self.label_29)
        self.label_40 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_40.setFont(font)
        self.label_40.setAutoFillBackground(True)
        self.label_40.setObjectName("label_40")
        self.horizontalLayout_4.addWidget(self.label_40)
        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_5.addWidget(self.label_9)
        self.lineEdit_10 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_10.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_10.setFont(font)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.horizontalLayout_5.addWidget(self.lineEdit_10)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_5.addWidget(self.label_10)
        self.lineEdit_9 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_9.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_9.setFont(font)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.horizontalLayout_5.addWidget(self.lineEdit_9)
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_5.addWidget(self.label_20)
        self.lineEdit_20 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_20.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_20.setFont(font)
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.horizontalLayout_5.addWidget(self.lineEdit_20)
        self.label_30 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.horizontalLayout_5.addWidget(self.label_30)
        self.label_42 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_42.setFont(font)
        self.label_42.setAutoFillBackground(True)
        self.label_42.setObjectName("label_42")
        self.horizontalLayout_5.addWidget(self.label_42)
        self.gridLayout.addLayout(self.horizontalLayout_5, 5, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_6.addWidget(self.label_11)
        self.lineEdit_12 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_12.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_12.setFont(font)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.horizontalLayout_6.addWidget(self.lineEdit_12)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_6.addWidget(self.label_12)
        self.lineEdit_11 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_11.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_11.setFont(font)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.horizontalLayout_6.addWidget(self.lineEdit_11)
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_6.addWidget(self.label_21)
        self.lineEdit_21 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_21.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_21.setFont(font)
        self.lineEdit_21.setObjectName("lineEdit_21")
        self.horizontalLayout_6.addWidget(self.lineEdit_21)
        self.label_31 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.horizontalLayout_6.addWidget(self.label_31)
        self.label_44 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_44.setFont(font)
        self.label_44.setAutoFillBackground(True)
        self.label_44.setObjectName("label_44")
        self.horizontalLayout_6.addWidget(self.label_44)
        self.gridLayout.addLayout(self.horizontalLayout_6, 6, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_7.addWidget(self.label_13)
        self.lineEdit_14 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_14.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_14.setFont(font)
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.horizontalLayout_7.addWidget(self.lineEdit_14)
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_7.addWidget(self.label_14)
        self.lineEdit_13 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_13.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_13.setFont(font)
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.horizontalLayout_7.addWidget(self.lineEdit_13)
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_7.addWidget(self.label_22)
        self.lineEdit_22 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_22.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_22.setFont(font)
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.horizontalLayout_7.addWidget(self.lineEdit_22)
        self.label_32 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.horizontalLayout_7.addWidget(self.label_32)
        self.label_46 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_46.setFont(font)
        self.label_46.setAutoFillBackground(True)
        self.label_46.setObjectName("label_46")
        self.horizontalLayout_7.addWidget(self.label_46)
        self.gridLayout.addLayout(self.horizontalLayout_7, 7, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_8.addWidget(self.label_17)
        self.lineEdit_17 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_17.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_17.setFont(font)
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.horizontalLayout_8.addWidget(self.lineEdit_17)
        self.lineEdit_23 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_23.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_23.setFont(font)
        self.lineEdit_23.setObjectName("lineEdit_23")
        self.horizontalLayout_8.addWidget(self.lineEdit_23)
        self.label_33 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_33.setFont(font)
        self.label_33.setText("")
        self.label_33.setObjectName("label_33")
        self.horizontalLayout_8.addWidget(self.label_33)
        self.label_48 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_48.setFont(font)
        self.label_48.setAutoFillBackground(True)
        self.label_48.setObjectName("label_48")
        self.horizontalLayout_8.addWidget(self.label_48)
        self.gridLayout.addLayout(self.horizontalLayout_8, 8, 0, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_9.addWidget(self.checkBox)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_9.addWidget(self.comboBox)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_9.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_9.addWidget(self.pushButton_2)
        self.gridLayout.addLayout(self.horizontalLayout_9, 9, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1031, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_CSSZ = QtWidgets.QAction(MainWindow)
        self.action_CSSZ.setObjectName("action_CSSZ")
        self.menu.addAction(self.action_CSSZ)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.Data_Init()
        self.pushButton.clicked.connect(self.Open_COM)
        self.pushButton_2.clicked.connect(self.Start_Measurement)
        Timer_ReadMessage.timeout.connect(self.Uart_Data_Receive)
        Timer_Measurement.timeout.connect(self.Start_Measurement)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def Data_Init(self):
        line_num = 0
        try:
            f = open(".\Deault_Par.txt")  # 返回一个文件对象
            for line in f.readlines():
                CurLine = line
                temp = int(CurLine)
                Data.Standard_Dict_Write(line_num,temp)
                line_num += 1
                if line_num> 14:
                    break
            f.close()

        except:
            QMessageBox.information(self,"错误信息","打开配置文件失败，使用默认配置参数",QMessageBox.Yes )

        self.lineEdit.setText(str(Data.Standard_Dict_Read(0)))
        self.lineEdit_2.setText(str(Data.Standard_Dict_Read(1)))
        self.lineEdit_4.setText(str(Data.Standard_Dict_Read(2)))
        self.lineEdit_3.setText(str(Data.Standard_Dict_Read(3)))
        self.lineEdit_8.setText(str(Data.Standard_Dict_Read(4)))
        self.lineEdit_7.setText(str(Data.Standard_Dict_Read(5)))
        self.lineEdit_6.setText(str(Data.Standard_Dict_Read(6)))
        self.lineEdit_5.setText(str(Data.Standard_Dict_Read(7)))
        self.lineEdit_10.setText(str(Data.Standard_Dict_Read(8)))
        self.lineEdit_9.setText(str(Data.Standard_Dict_Read(9)))
        self.lineEdit_12.setText(str(Data.Standard_Dict_Read(10)))
        self.lineEdit_11.setText(str(Data.Standard_Dict_Read(11)))
        self.lineEdit_14.setText(str(Data.Standard_Dict_Read(12)))
        self.lineEdit_13.setText(str(Data.Standard_Dict_Read(13)))
        self.lineEdit_17.setText(str(Data.Standard_Dict_Read(14)))

    def Show_ComList(self):
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        i = 0
        for Port_Com in port_list:
            i += 1
            self.Com_Dict["%s" % Port_Com[0]] = "%s" % Port_Com[1]
        if len(port_list) == 0:
            QMessageBox.information(self,"错误信息","无可用串口，请检查",QMessageBox.Yes )
            return 'None'
        if len(port_list) == 1:
                return  Port_Com[0]
        if len(port_list) > 1:
            QMessageBox.information(self,"错误信息","含有多个可用串口："
                                                "请用手动选择模式",QMessageBox.Yes )
            return 'None'

    def Open_COM(self):
        global SeralPor_OpenFlag
        global SerialPort_Information
        if self.checkBox.isChecked() == True:
           COM_Port = self.comboBox.currentText()
        else:
           COM_Port = self.Show_ComList()
        if COM_Port == 'None':
            return
        if self.pushButton.text() == "打开串口":
            Serial_Port.baudrate = 9600
            Serial_Port.port = str(COM_Port)
            Serial_Port.bytesize = 8
            Serial_Port.stopbits = 1
            Serial_Port.parity = 'N'

            try:
                Serial_Port.open()
                Timer_ReadMessage.start(10)
            except:
                QMessageBox.information(self,"错误信息","打开失败",QMessageBox.Yes )
                return None

            if Serial_Port.isOpen():
                self.pushButton.setText(QtCore.QCoreApplication.translate("Form", "关闭串口"))
                Timer_ReadMessage.start(300)
                SeralPor_OpenFlag = 1
                SerialPort_Information = '串口' + str(Serial_Port.port) + '  波特率：' + str(Serial_Port.baudrate)
        elif self.pushButton.text() == "关闭串口":
            self.Close_Com()

    def Close_Com(self):
        Serial_Port.close()
        self.pushButton.setText(QtCore.QCoreApplication.translate("Form", "打开串口"))
        Timer_ReadMessage.stop()

    def Measurement_ModuleVoltage(self):
        send_list = []
        Str_Send = "46 16 01 09 04 6A"
        while Str_Send != '':
            num = int(Str_Send[0:2], 16)
            Str_Send = Str_Send[2:].strip()
            send_list.append(num)
        send_list = bytes(send_list)
        try:
            Serial_Port.write(send_list)  # item.encode('utf-8'))
        except Exception as e:
            pass

    def Measurement_CellVoltage(self):
        send_list = []
        Str_Send = "46 16 01 24 20 A1"
        while Str_Send != '':
            num = int(Str_Send[0:2], 16)
            Str_Send = Str_Send[2:].strip()
            send_list.append(num)
        send_list = bytes(send_list)
        try:
            Serial_Port.write(send_list)  # item.encode('utf-8'))
        except Exception as e:
            pass

    def Measurement_CellTemperture(self):
        send_list = []
        Str_Send = "46 16 01 08 20 85"
        while Str_Send != '':
            num = int(Str_Send[0:2], 16)
            Str_Send = Str_Send[2:].strip()
            send_list.append(num)
        send_list = bytes(send_list)
        try:
            Serial_Port.write(send_list)  # item.encode('utf-8'))
        except Exception as e:
            pass

    def Measurement_SOC(self):
        send_list = []
        Str_Send = "46 16 01 0D 04 6E"
        while Str_Send != '':
            num = int(Str_Send[0:2], 16)
            Str_Send = Str_Send[2:].strip()
            send_list.append(num)
        send_list = bytes(send_list)
        try:
            Serial_Port.write(send_list)  # item.encode('utf-8'))
        except Exception as e:
            pass

    def Measurement_FullChargeCap(self):
        send_list = []
        Str_Send = "46 16 01 10 04 71"
        while Str_Send != '':
            num = int(Str_Send[0:2], 16)
            Str_Send = Str_Send[2:].strip()
            send_list.append(num)
        send_list = bytes(send_list)
        try:
            Serial_Port.write(send_list)  # item.encode('utf-8'))
        except Exception as e:
            pass

    def Measurement_RemainCap(self):
        send_list = []
        Str_Send = "46 16 01 0F 04 70"
        while Str_Send != '':
            num = int(Str_Send[0:2], 16)
            Str_Send = Str_Send[2:].strip()
            send_list.append(num)
        send_list = bytes(send_list)
        try:
            Serial_Port.write(send_list)  # item.encode('utf-8'))
        except Exception as e:
            pass

    def Measurement_Current(self):
        send_list = []
        Str_Send = "46 16 01 0A 04 6B"
        while Str_Send != '':
            num = int(Str_Send[0:2], 16)
            Str_Send = Str_Send[2:].strip()
            send_list.append(num)
        send_list = bytes(send_list)
        try:
            Serial_Port.write(send_list)  # item.encode('utf-8'))
        except Exception as e:
            pass

    def Measurement_Version(self):
        send_list = []
        Str_Send = "46 16 01 1A 08 7F"
        while Str_Send != '':
            num = int(Str_Send[0:2], 16)
            Str_Send = Str_Send[2:].strip()
            send_list.append(num)
        send_list = bytes(send_list)
        try:
            Serial_Port.write(send_list)  # item.encode('utf-8'))
        except Exception as e:
            pass

    def Start_Measurement(self):
        global Measurement_Step
        global Communicate_Count
        global Measurement_Status
        global Par_Charge_Flag
        if Measurement_Status == 0:
            Measurement_Status = 1
            Timer_Measurement.start(500)
            if Par_Charge_Flag == 1:
                self.Data_Init()
            palette = QPalette()
            palette.setColor(QPalette.Window, Qt.blue)
            self.label_34.setPalette(palette)
            self.label_36.setPalette(palette)
            self.label_38.setPalette(palette)
            self.label_40.setPalette(palette)
            self.label_42.setPalette(palette)
            self.label_44.setPalette(palette)
            self.label_46.setPalette(palette)
            self.label_48.setPalette(palette)
            self.label_47.setPalette(palette)
            self.label_53.setPalette(palette)
            self.lineEdit_15.setText("")
            self.lineEdit_16.setText("")
            self.lineEdit_18.setText("")
            self.lineEdit_19.setText("")
            self.lineEdit_20.setText("")
            self.lineEdit_21.setText("")
            self.lineEdit_22.setText("")
            self.lineEdit_23.setText("")

        self.Uart_Data_Deal()

        Communicate_Count += 1

        if Communicate_Count > 10:
            self.Stop_Measurement()
            QMessageBox.information(self,"错误信息","通讯失败",QMessageBox.Yes )


        if Serial_Port.isOpen():
            if Measurement_Step == 0:
                self.Measurement_ModuleVoltage()
            elif Measurement_Step == 1:
                self.Measurement_CellVoltage()
            elif Measurement_Step == 2:
                self.Measurement_CellTemperture()
            elif Measurement_Step == 3:
                self.Measurement_SOC()
            elif Measurement_Step == 4:
                self.Measurement_FullChargeCap()
            elif Measurement_Step == 5:
                self.Measurement_RemainCap()
            elif Measurement_Step == 6:
                self.Measurement_Current()
            elif Measurement_Step == 7:
                self.Measurement_Version()
            elif Measurement_Step == 8:
                self.Stop_Measurement()
                QMessageBox.information(self,"信息","测试成功",QMessageBox.Yes )
        else:
            self.Stop_Measurement()
            QMessageBox.information(self,"错误信息","未打开串口",QMessageBox.Yes )

    def Stop_Measurement(self):
        global Measurement_Status
        global Measurement_Step
        global Communicate_Count
        if Measurement_Status == 1:
            Measurement_Status = 0
            Timer_Measurement.stop()
        Measurement_Step = 0
        Communicate_Count = 0

    def Uart_Data_Receive(self):
        global Uart_Buffer
        global Uart_Buffer_Count
        if Serial_Port.isOpen():
            try:
                num = Serial_Port.inWaiting()
            except:
                return None
            if num<1:
                return
            data = Serial_Port.read(num)
            num = len(data)
            for i in range(len(data)):
                Uart_Buffer[Uart_Buffer_Count] = ((hex(data[i])[2:]))
                Uart_Buffer_Count += 1
                if Uart_Buffer_Count > 511:
                    Uart_Buffer_Count = 0
            Serial_Port.flushInput()
            Serial_Port.flushOutput()

    def Uart_Data_Deal(self):
        global Uart_Buffer
        global Uart_Buffer_Count
        global Measurement_Step
        global Communicate_Count
        Upper_Value = 0
        Lower_Value = 0
        if Uart_Buffer[0] == '47' and Uart_Buffer[1] == '16' and Uart_Buffer[2] == '1':
            if Uart_Buffer[3] == '9':
                Lower_Value = Data.Standard_Dict_Read(0)
                Upper_Value = Data.Standard_Dict_Read(1)
                temp = Hex2Dec(Uart_Buffer[5]) + Hex2Dec(Uart_Buffer[6])*256
                if temp > Lower_Value and temp < Upper_Value :#通过
                    Measurement_Step = 1
                    Communicate_Count = 0
                    palette = QPalette()
                    palette.setColor(QPalette.Window, Qt.green)
                    self.label_34.setPalette(palette)
                    self.lineEdit_15.setText(str(temp))
                else:
                    self.lineEdit_15.setText(str(temp))
                    palette = QPalette()
                    palette.setColor(QPalette.Window, Qt.red)
                    self.label_34.setPalette(palette)
                    self.Stop_Measurement()
                    QMessageBox.information(self,"错误信息","总压检测失败"
                                                        "实际值："+str(temp),QMessageBox.Yes )

            if Uart_Buffer[3] == '24':
                Lower_Value = Data.Standard_Dict_Read(2)
                Upper_Value = Data.Standard_Dict_Read(3)
                for i in range(10):
                    temp = Hex2Dec(Uart_Buffer[5+i*2]) + Hex2Dec(Uart_Buffer[6+i*2])*256
                    if temp > Lower_Value and temp < Upper_Value:#通过
                        if i == 9:
                            Measurement_Step = 2
                            Communicate_Count = 0
                            palette = QPalette()
                            palette.setColor(QPalette.Window, Qt.green)
                            self.label_36.setPalette(palette)
                            self.lineEdit_16.setText(str(temp))
                    else:
                        self.lineEdit_16.setText(str(temp))
                        palette = QPalette()
                        palette.setColor(QPalette.Window, Qt.red)
                        self.label_36.setPalette(palette)
                        self.Stop_Measurement()
                        QMessageBox.information(self,"错误信息","单体电压检测失败"
                                                            "实际值："+str(temp),QMessageBox.Yes )
                        break

            if Uart_Buffer[3] == '8':
                Lower_Value = Data.Standard_Dict_Read(4)
                Upper_Value = Data.Standard_Dict_Read(5)
                temp = Hex2Dec(Uart_Buffer[5])
                if temp > Lower_Value and temp < Upper_Value :#通过
                    Measurement_Step = 3
                    Communicate_Count = 0
                    palette = QPalette()
                    palette.setColor(QPalette.Window, Qt.green)
                    self.label_38.setPalette(palette)
                    self.lineEdit_18.setText(str(temp))
                else:
                    self.lineEdit_18.setText(str(temp))
                    palette = QPalette()
                    palette.setColor(QPalette.Window, Qt.red)
                    self.label_38.setPalette(palette)
                    self.Stop_Measurement()
                    QMessageBox.information(self,"错误信息","温度检测失败"
                                                        "实际值："+str(temp),QMessageBox.Yes )

            if Uart_Buffer[3] == 'd':
                Lower_Value = Data.Standard_Dict_Read(6)
                Upper_Value = Data.Standard_Dict_Read(7)
                temp = Hex2Dec(Uart_Buffer[5])
                if temp > Lower_Value and temp < Upper_Value :#通过
                    Measurement_Step = 4
                    Communicate_Count = 0
                    palette = QPalette()
                    palette.setColor(QPalette.Window, Qt.green)
                    self.label_40.setPalette(palette)
                    self.lineEdit_19.setText(str(temp))
                else:
                    self.lineEdit_19.setText(str(temp))
                    palette = QPalette()
                    palette.setColor(QPalette.Window, Qt.red)
                    self.label_40.setPalette(palette)
                    self.Stop_Measurement()
                    QMessageBox.information(self,"错误信息","SOC检测失败"
                                                        "实际值："+str(temp),QMessageBox.Yes )

            if Uart_Buffer[3] == '10':
                Lower_Value = Data.Standard_Dict_Read(8)
                Upper_Value = Data.Standard_Dict_Read(9)
                temp = Hex2Dec(Uart_Buffer[5]) + Hex2Dec(Uart_Buffer[6])*256
                if temp > Lower_Value and temp < Upper_Value :#通过
                    Measurement_Step = 5
                    Communicate_Count = 0
                    palette = QPalette()
                    palette.setColor(QPalette.Window, Qt.green)
                    self.label_42.setPalette(palette)
                    self.lineEdit_20.setText(str(temp))
                else:
                    self.lineEdit_20.setText(str(temp))
                    palette = QPalette()
                    palette.setColor(QPalette.Window, Qt.red)
                    self.label_42.setPalette(palette)
                    self.Stop_Measurement()
                    QMessageBox.information(self,"错误信息","满充容量检测失败"
                                                        "实际值："+str(temp),QMessageBox.Yes )

            if Uart_Buffer[3] == 'f':
                Lower_Value = Data.Standard_Dict_Read(10)
                Upper_Value = Data.Standard_Dict_Read(11)
                temp = Hex2Dec(Uart_Buffer[5]) + Hex2Dec(Uart_Buffer[6])*256
                if temp > Lower_Value and temp < Upper_Value :#通过
                    Measurement_Step = 6
                    Communicate_Count = 0
                    palette = QPalette()
                    palette.setColor(QPalette.Window, Qt.green)
                    self.label_44.setPalette(palette)
                    self.lineEdit_21.setText(str(temp))
                else:
                    self.lineEdit_21.setText(str(temp))
                    palette = QPalette()
                    palette.setColor(QPalette.Window, Qt.red)
                    self.label_44.setPalette(palette)
                    self.Stop_Measurement()
                    QMessageBox.information(self,"错误信息","剩余容量检测失败"
                                                        "实际值："+str(temp),QMessageBox.Yes )

            if Uart_Buffer[3] == 'a':
                Lower_Value = Data.Standard_Dict_Read(12)
                Upper_Value = Data.Standard_Dict_Read(13)
                temp = Hex2Dec(Uart_Buffer[5]) + Hex2Dec(Uart_Buffer[6])*0x100
                if temp > 0x7FFF:
                    temp = temp - 0x10000
                if temp > Lower_Value and temp < Upper_Value :#通过
                    Measurement_Step = 7
                    Communicate_Count = 0
                    palette = QPalette()
                    palette.setColor(QPalette.Window, Qt.green)
                    self.label_46.setPalette(palette)
                    self.lineEdit_22.setText(str(temp))
                else:
                    self.lineEdit_22.setText(str(temp))
                    palette = QPalette()
                    palette.setColor(QPalette.Window, Qt.red)
                    self.label_46.setPalette(palette)
                    self.Stop_Measurement()
                    QMessageBox.information(self,"错误信息","电流检测失败"
                                                        "实际值："+str(temp),QMessageBox.Yes )

            if Uart_Buffer[3] == '1a':
                Lower_Value = Data.Standard_Dict_Read(14)
                temp = Hex2Dec(Uart_Buffer[8]) + Hex2Dec(Uart_Buffer[7])*10  + Hex2Dec(Uart_Buffer[6])*100  + Hex2Dec(Uart_Buffer[5])*1000

                if temp == Lower_Value:#通过
                    Measurement_Step = 8
                    Communicate_Count = 0
                    palette = QPalette()
                    palette.setColor(QPalette.Window, Qt.green)
                    self.label_48.setPalette(palette)
                    self.lineEdit_23.setText(str(temp))
                else:
                    self.lineEdit_23.setText(str(temp))
                    palette = QPalette()
                    palette.setColor(QPalette.Window, Qt.red)
                    self.label_48.setPalette(palette)
                    self.Stop_Measurement()
                    QMessageBox.information(self,"错误信息","版本检测失败"
                                                        "实际值："+str(temp),QMessageBox.Yes )

        Uart_Buffer[0] = 0
        Uart_Buffer[1] = 0
        Uart_Buffer[2] = 0
        Uart_Buffer_Count = 0

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "嘉策成品测试上位机"))
        self.label_23.setText(_translate("MainWindow", "标准值                                      "))
        self.label_24.setText(_translate("MainWindow", "实际值"))
        self.label_25.setText(_translate("MainWindow", "结果"))
        self.label.setText(_translate("MainWindow", "总电压     "))
        self.label_2.setText(_translate("MainWindow", "-"))
        self.label_15.setText(_translate("MainWindow", "mV         "))
        self.label_26.setText(_translate("MainWindow", "mV "))
        self.label_34.setText(_translate("MainWindow", "通过/不通过"))
        self.label_3.setText(_translate("MainWindow", "单体电压"))
        self.label_4.setText(_translate("MainWindow", "-"))
        self.label_16.setText(_translate("MainWindow", "mV        "))
        self.label_27.setText(_translate("MainWindow", "mV "))
        self.label_36.setText(_translate("MainWindow", "通过/不通过"))
        self.label_7.setText(_translate("MainWindow", "单体温度"))
        self.label_8.setText(_translate("MainWindow", "-"))
        self.label_18.setText(_translate("MainWindow", "℃       "))
        self.label_28.setText(_translate("MainWindow", " ℃"))
        self.label_38.setText(_translate("MainWindow", "通过/不通过"))
        self.label_5.setText(_translate("MainWindow", "SOC              "))
        self.label_6.setText(_translate("MainWindow", "-"))
        self.label_19.setText(_translate("MainWindow", "%         "))
        self.label_29.setText(_translate("MainWindow", "   %"))
        self.label_40.setText(_translate("MainWindow", "通过/不通过"))
        self.label_9.setText(_translate("MainWindow", "设计容量"))
        self.label_10.setText(_translate("MainWindow", "-"))
        self.label_20.setText(_translate("MainWindow", "mAh      "))
        self.label_30.setText(_translate("MainWindow", "mAh"))
        self.label_42.setText(_translate("MainWindow", "通过/不通过"))
        self.label_11.setText(_translate("MainWindow", "剩余容量"))
        self.label_12.setText(_translate("MainWindow", "-"))
        self.label_21.setText(_translate("MainWindow", "mAh      "))
        self.label_31.setText(_translate("MainWindow", "mAh"))
        self.label_44.setText(_translate("MainWindow", "通过/不通过"))
        self.label_13.setText(_translate("MainWindow", "总电流     "))
        self.label_14.setText(_translate("MainWindow", "-"))
        self.label_22.setText(_translate("MainWindow", "mA       "))
        self.label_32.setText(_translate("MainWindow", "  mA"))
        self.label_46.setText(_translate("MainWindow", "通过/不通过"))
        self.label_17.setText(_translate("MainWindow", "版本号     "))
        self.label_48.setText(_translate("MainWindow", "通过/不通过"))
        self.checkBox.setText(_translate("MainWindow", "手动打开串口"))
        self.comboBox.setItemText(0, _translate("MainWindow", "COM1"))
        self.comboBox.setItemText(1, _translate("MainWindow", "COM2"))
        self.comboBox.setItemText(2, _translate("MainWindow", "COM3"))
        self.comboBox.setItemText(3, _translate("MainWindow", "COM4"))
        self.comboBox.setItemText(4, _translate("MainWindow", "COM5"))
        self.comboBox.setItemText(5, _translate("MainWindow", "COM6"))
        self.comboBox.setItemText(6, _translate("MainWindow", "COM7"))
        self.comboBox.setItemText(7, _translate("MainWindow", "COM8"))
        self.comboBox.setItemText(8, _translate("MainWindow", "COM9"))
        self.comboBox.setItemText(9, _translate("MainWindow", "COM10"))
        self.comboBox.setItemText(10, _translate("MainWindow", "COM11"))
        self.comboBox.setItemText(11, _translate("MainWindow", "COM12"))
        self.comboBox.setItemText(12, _translate("MainWindow", "COM13"))
        self.comboBox.setItemText(13, _translate("MainWindow", "COM14"))
        self.comboBox.setItemText(14, _translate("MainWindow", "COM15"))
        self.pushButton.setText(_translate("MainWindow", "打开串口"))
        self.pushButton_2.setText(_translate("MainWindow", "开始测试"))
        self.menu.setTitle(_translate("MainWindow", "参数设置"))
        self.action_CSSZ.setText(_translate("MainWindow", "参数设置"))


