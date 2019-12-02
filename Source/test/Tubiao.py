# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Tubiao.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from test import BarGraphView

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(957, 742)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 60, 931, 651))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 1, 1, 1)
        self.grapView_Current = QtWidgets.QGraphicsView(self.widget)
        self.grapView_Current.setObjectName("grapView_Current")
        self.gridLayout.addWidget(self.grapView_Current, 1, 0, 1, 1)
        self.grapView_Voltage = QtWidgets.QGraphicsView(self.widget)
        self.grapView_Voltage.setObjectName("grapView_Voltage")
        self.gridLayout.addWidget(self.grapView_Voltage, 3, 0, 1, 1)
        self.graphicsView_Temperature = QtWidgets.QGraphicsView(self.widget)
        self.graphicsView_Temperature.setObjectName("graphicsView_Temperature")
        self.gridLayout.addWidget(self.graphicsView_Temperature, 5, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.graphicsView_SOC = QtWidgets.QGraphicsView(self.widget)
        self.graphicsView_SOC.setObjectName("graphicsView_SOC")
        self.gridLayout.addWidget(self.graphicsView_SOC, 5, 1, 1, 1)
        self.grapView_Alarm = QtWidgets.QGraphicsView(self.widget)
        self.grapView_Alarm.setObjectName("grapView_Alarm")
        self.gridLayout.addWidget(self.grapView_Alarm, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_4.setText(_translate("MainWindow", "SOC"))
        self.label.setText(_translate("MainWindow", "电压"))
        self.label_2.setText(_translate("MainWindow", "温度"))
        self.label_3.setText(_translate("MainWindow", "电流"))
        self.label_5.setText(_translate("MainWindow", "告警"))
        self.label_6.setText(_translate("MainWindow", "Movie"))
        self.label_7.setText(_translate("MainWindow", "状态图"))

