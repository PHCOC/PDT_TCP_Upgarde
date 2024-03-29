# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindows.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from CKPZ_UI import Ui_Form,Timer_ReadMessage,Serial_Port,Timer_500ms,Timer_SendMessage
from CANWindows_UI import CAN_Ui_Form
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
import CKPZ_UI
import Data
import CANWindows_UI

Graph_ReflshTime = QTimer()
Graph_Init_Flag = 0


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.desktop = QApplication.desktop()#获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(int(975/1920*self.width), int(875/1080*self.height))
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.splitter)
        self.pushButton.setMaximumSize(QtCore.QSize(93, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.splitter)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 3, 0, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout.addWidget(self.lineEdit_5, 3, 1, 1, 1)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.gridLayout.addWidget(self.lineEdit_8, 2, 11, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 3, 2, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 2, 3, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 2, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 2, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 0, 1, 12)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 5, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 2, 7, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 6, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 2, 8, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 9, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 3, 9, 1, 1)
        self.lineEdit_9 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.gridLayout.addWidget(self.lineEdit_9, 3, 11, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setEnabled(True)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 6, 0, 1, 12)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout.addWidget(self.lineEdit_6, 3, 3, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 3, 4, 1, 2)
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit.setAutoFillBackground(False)
        self.dateTimeEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dateTimeEdit.setCalendarPopup(False)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.gridLayout.addWidget(self.dateTimeEdit, 3, 7, 1, 2)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout.addWidget(self.lineEdit_7, 3, 6, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setCheckable(False)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout.addWidget(self.checkBox_3, 4, 1, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setCheckable(False)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 4, 0, 1, 1)
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setCheckable(False)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout.addWidget(self.checkBox_4, 4, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 4, 9, 1, 1)
        self.comboBox_5 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.gridLayout.addWidget(self.comboBox_5, 4, 11, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(8)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setUnderline(False)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(0, 6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(0, 7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        item.setFont(font)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(2, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(2, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(2, 5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(2, 6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(2, 7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(3, 7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(4, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(4, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(4, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(4, 5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(4, 6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(4, 7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(5, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(5, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(5, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(5, 5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(5, 6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsTristate)
        self.tableWidget.setItem(5, 7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(6, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(6, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(6, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(6, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(6, 5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(6, 6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(6, 7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        self.tableWidget.setItem(7, 0, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(118)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(13)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableWidget)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Graph = QtWidgets.QTabWidget(self.centralwidget)
        self.Graph.setObjectName("Graph")
        self.Current = QtWidgets.QWidget()
        self.Current.setObjectName("Current")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Current)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        # self.verticalLayout_2.addWidget(self.widget_3)
        self.Graph.addTab(self.Current, "")
        self.SOC = QtWidgets.QWidget()
        self.SOC.setObjectName("SOC")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.SOC)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Graph.addTab(self.SOC, "")
        self.Voltage = QtWidgets.QWidget()
        self.Voltage.setObjectName("Voltage")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.Voltage)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Graph.addTab(self.Voltage, "")
        self.gridLayout_2.addWidget(self.Graph, 1, 0, 1, 1)
        self.Data_Show = QtWidgets.QTextBrowser(self.centralwidget)
        self.Data_Show.setEnabled(True)
        self.Data_Show.setSizeIncrement(QtCore.QSize(521, 301))
        self.Data_Show.setToolTipDuration(-1)
        self.Data_Show.setOverwriteMode(False)
        self.Data_Show.setObjectName("Data_Show")
        self.gridLayout_2.addWidget(self.Data_Show, 1, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Clear_DataShow = QtWidgets.QPushButton(self.centralwidget)
        self.Clear_DataShow.setObjectName("Clear_DataShow")
        self.horizontalLayout.addWidget(self.Clear_DataShow)
        self.AutoRead_Checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.AutoRead_Checkbox.setObjectName("AutoRead_Checkbox")
        self.horizontalLayout.addWidget(self.AutoRead_Checkbox)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.read_pushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.read_pushbutton.setObjectName("read_pushbutton")
        self.horizontalLayout.addWidget(self.read_pushbutton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.TimeofPlot = QtWidgets.QComboBox(self.centralwidget)
        self.TimeofPlot.setMaximumSize(QtCore.QSize(87, 22))
        self.TimeofPlot.setObjectName("TimeofPlot")
        self.TimeofPlot.addItem("")
        self.TimeofPlot.addItem("")
        self.TimeofPlot.addItem("")
        self.TimeofPlot.addItem("")
        self.gridLayout_2.addWidget(self.TimeofPlot, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 975, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menuBOOT = QtWidgets.QMenu(self.menubar)
        self.menuBOOT.setObjectName("menuBOOT")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setCheckable(False)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action309_RTC = QtWidgets.QAction(MainWindow)
        self.action309_RTC.setObjectName("action309_RTC")
        self.action_LvLi = QtWidgets.QAction(MainWindow)
        self.action_LvLi.setObjectName("action_LvLi")
        self.action_Upgrade = QtWidgets.QAction(MainWindow)
        self.action_Upgrade.setObjectName("action_Upgrade")
        self.action_Samlltool = QtWidgets.QAction(MainWindow)
        self.action_Samlltool.setObjectName("action_Samlltool")
        self.actionCAN = QtWidgets.QAction(MainWindow)
        self.actionCAN.setObjectName("actionCAN")
        self.menu.addAction(self.action_2)
        self.menu.addSeparator()
        self.menu.addAction(self.actionCAN)
        self.menu.addSeparator()
        self.menu_2.addAction(self.action_Samlltool)
        self.menu_2.addAction(self.action_3)
        self.menu_2.addSeparator()
        self.menu_3.addAction(self.action309_RTC)
        self.menu_3.addSeparator()
        self.menu_3.addAction(self.action_LvLi)
        self.menuBOOT.addAction(self.action_Upgrade)
        self.menuBOOT.addSeparator()
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menuBOOT.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        self.Graph_Show_Timer_Start()
        self.AutoRead_Checkbox.stateChanged.connect(self.Send_Continuous)
        self.Clear_DataShow.clicked.connect(self.Data_Show.clear)
        #self.LineEdit.textChanged.connect(self.Set_Send_Delay)
        Timer_SendMessage.timeout.connect(self.Message_Send)
        self.read_pushbutton.clicked.connect(self.Message_Send)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def Graph_Show_Timer_Start(self):
        Graph_ReflshTime.start(1000)
        Graph_ReflshTime.timeout.connect(self.Graph_Show)

        pg.setConfigOption('background', 'w')
        plt = pg.PlotWidget()
        plt.setMaximumSize(QtCore.QSize(472, 264))
        plt.setMouseEnabled(False, False)
        plt.setMenuEnabled(False)
        plt.showGrid(x=True, y=True)
        plt.setRange(xRange=[0, 299], yRange=[-30000, 30000], padding=0, disableAutoRange=True)
        plt.setLabels(left='mA', bottom='/*S', title='Current')
        self.curve = plt.plot(pen='r')

        plt2 = pg.PlotWidget()
        plt2.setMaximumSize(QtCore.QSize(472, 264))
        plt2.setMouseEnabled(False, False)
        plt2.setMenuEnabled(False)
        plt2.showGrid(x=True, y=True)
        plt2.setRange(xRange=[0, 299], yRange=[0, 100], padding=0, disableAutoRange=True)
        plt2.setLabels(left='%', bottom='/*S', title='SOC')
        self.curve2 = plt2.plot(pen='r')

        plt3 = pg.PlotWidget()
        plt3.setMaximumSize(QtCore.QSize(472, 264))
        plt3.setMouseEnabled(False, False)
        plt3.setMenuEnabled(False)
        plt3.showGrid(x=True, y=True)
        plt3.setRange(xRange=[0, 299], yRange=[4000, 8000], padding=0, disableAutoRange=True)
        plt3.setLabels(left='10mV', bottom='/*S', title='Voltage')
        self.curve3 = plt3.plot(pen='r')

        self.verticalLayout_2.addWidget(plt)
        self.verticalLayout_3.addWidget(plt2)
        self.verticalLayout_4.addWidget(plt3)


    def Graph_Show(self):
        Time_Text = self.TimeofPlot.currentText()
        if Time_Text == "1S":
            # temp = Data.Read_Data(1,1)
            self.curve.setData(Data.Read_Data(1,1))
            self.curve2.setData(Data.Read_Data(2,1))
            self.curve3.setData(Data.Read_Data(3,1))
        elif Time_Text == "5S":
            self.curve.setData(Data.Read_Data(1,5))
            self.curve2.setData(Data.Read_Data(2,5))
            self.curve3.setData(Data.Read_Data(3,5))
        elif Time_Text == "10S":
            self.curve.setData(Data.Read_Data(1,10))
            self.curve2.setData(Data.Read_Data(2,10))
            self.curve3.setData(Data.Read_Data(3,10))
        elif Time_Text == "30S":
            self.curve.setData(Data.Read_Data(1,30))
            self.curve2.setData(Data.Read_Data(2,30))
            self.curve3.setData(Data.Read_Data(3,30))

    def Send_Continuous(self):
        global Send_Delay
        if CKPZ_UI.SeralPor_OpenFlag == 1 or CANWindows_UI.CAN_OpenFlag == 1:
            if self.AutoRead_Checkbox.isChecked() == True:
                # self.str = self.Read_Time.text()
                # if len(self.str)>1:
                #     Send_Delay = int(self.str)
                    #self.Read_Time.setEnabled(False)
                self.read_pushbutton.setEnabled(False)
                    #Timer_SendMessage.start(int(Send_Delay))
                Timer_SendMessage.start(1000)
            else:
                # self.Read_Time.setEnabled(True)
                self.read_pushbutton.setEnabled(True)
                #Timer_SendMessage.start(int(Send_Delay))
                Timer_SendMessage.stop()


        else:
            self.Data_Show.append("未打开通讯工具")
            self.AutoRead_Checkbox.setCheckState(False)

    def Message_Send(self):
        if CKPZ_UI.SeralPor_OpenFlag == 1:
            if Serial_Port.isOpen():
                send_list = []
                Str_Send = "03 03 75 31 00 24 0F F0"
                # Str_Send = "46 16 01 24 20 A1"
                while Str_Send != '':
                    num = int(Str_Send[0:2], 16)
                    Str_Send = Str_Send[2:].strip()
                    send_list.append(num)
                send_list = bytes(send_list)
                try:
                    Serial_Port.write(send_list)  # item.encode('utf-8'))
                except Exception as e:
                    self.Data_Show.append(str(e))
                    self.AutoRead_Checkbox.setCheckState(False)
        elif CANWindows_UI.CAN_OpenFlag == 1:
            BMS_ID = self.comboBox_5.currentText()
            BMS_ID = int(BMS_ID[2:3])*16 + int(BMS_ID[3:])
            CAN_Ui_Form2 = CAN_Ui_Form()
            CAN_Ui_Form2.CAN_Request_AllInformation(BMS_ID)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "已打开设备信息"))
        self.pushButton.setText(_translate("MainWindow", "表格模式"))
        self.label_10.setText(_translate("MainWindow", "满充容量"))
        self.label_11.setText(_translate("MainWindow", "循环次数"))
        self.label_3.setText(_translate("MainWindow", "组端电流"))
        self.label_2.setText(_translate("MainWindow", "组端电压"))
        self.label_4.setText(_translate("MainWindow", "组端SOC"))
        self.label_9.setText(_translate("MainWindow", "剩余容量"))
        self.label_8.setText(_translate("MainWindow", "绝缘电阻+"))
        self.label_13.setText(_translate("MainWindow", "绝缘电阻-"))
        self.label_12.setText(_translate("MainWindow", "设计容量"))
        self.dateTimeEdit.setDisplayFormat(_translate("MainWindow", "yyyy/M/d H:mm:ss"))
        self.checkBox_3.setText(_translate("MainWindow", "充电MOS"))
        self.checkBox_2.setText(_translate("MainWindow", "放电MOS"))
        self.checkBox_4.setText(_translate("MainWindow", "预充电MOS"))
        self.label_7.setText(_translate("MainWindow", "BMS地址"))
        self.comboBox_5.setItemText(0, _translate("MainWindow", "0x80"))
        self.comboBox_5.setItemText(1, _translate("MainWindow", "0x81"))
        self.comboBox_5.setItemText(2, _translate("MainWindow", "0x82"))
        self.comboBox_5.setItemText(3, _translate("MainWindow", "0x83"))
        self.comboBox_5.setItemText(4, _translate("MainWindow", "0x84"))
        self.comboBox_5.setItemText(5, _translate("MainWindow", "0x85"))
        self.comboBox_5.setItemText(6, _translate("MainWindow", "0x86"))
        self.comboBox_5.setItemText(7, _translate("MainWindow", "0x87"))
        self.comboBox_5.setItemText(8, _translate("MainWindow", "0x88"))
        self.comboBox_5.setItemText(9, _translate("MainWindow", "0x89"))
        self.comboBox_5.setItemText(10, _translate("MainWindow", "0x8A"))
        self.comboBox_5.setItemText(11, _translate("MainWindow", "0x8B"))
        self.comboBox_5.setItemText(12, _translate("MainWindow", "0x8C"))
        self.comboBox_5.setItemText(13, _translate("MainWindow", "0x8D"))
        self.comboBox_5.setItemText(14, _translate("MainWindow", "0x8E"))
        self.comboBox_5.setItemText(15, _translate("MainWindow", "0x8F"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "单体电压"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "单体电压"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "单体电压"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "单体温度"))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "#1"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "#2"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "#3"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "#4"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "#5"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "#6"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "#7"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "#8"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("MainWindow", "单体电压#1~#7"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("MainWindow", "#1"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("MainWindow", "#2"))
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("MainWindow", "#3"))
        item = self.tableWidget.item(0, 4)
        item.setText(_translate("MainWindow", "#4"))
        item = self.tableWidget.item(0, 5)
        item.setText(_translate("MainWindow", "#5"))
        item = self.tableWidget.item(0, 6)
        item.setText(_translate("MainWindow", "#6"))
        item = self.tableWidget.item(0, 7)
        item.setText(_translate("MainWindow", "#7"))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("MainWindow", "mV"))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("MainWindow", "单体电压#8~#14"))
        item = self.tableWidget.item(2, 1)
        item.setText(_translate("MainWindow", "#8"))
        item = self.tableWidget.item(2, 2)
        item.setText(_translate("MainWindow", "#9"))
        item = self.tableWidget.item(2, 3)
        item.setText(_translate("MainWindow", "#10"))
        item = self.tableWidget.item(2, 4)
        item.setText(_translate("MainWindow", "#11"))
        item = self.tableWidget.item(2, 5)
        item.setText(_translate("MainWindow", "#12"))
        item = self.tableWidget.item(2, 6)
        item.setText(_translate("MainWindow", "#13"))
        item = self.tableWidget.item(2, 7)
        item.setText(_translate("MainWindow", "#14"))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("MainWindow", "mV"))
        item = self.tableWidget.item(4, 0)
        item.setText(_translate("MainWindow", "单体电压#15~#21"))
        item = self.tableWidget.item(4, 1)
        item.setText(_translate("MainWindow", "#15"))
        item = self.tableWidget.item(4, 2)
        item.setText(_translate("MainWindow", "#16"))
        item = self.tableWidget.item(4, 3)
        item.setText(_translate("MainWindow", "#17"))
        item = self.tableWidget.item(4, 4)
        item.setText(_translate("MainWindow", "#18"))
        item = self.tableWidget.item(4, 5)
        item.setText(_translate("MainWindow", "#19"))
        item = self.tableWidget.item(4, 6)
        item.setText(_translate("MainWindow", "#20"))
        item = self.tableWidget.item(4, 7)
        item.setText(_translate("MainWindow", "#21"))
        item = self.tableWidget.item(5, 0)
        item.setText(_translate("MainWindow", "mV"))
        item = self.tableWidget.item(6, 0)
        item.setText(_translate("MainWindow", "单体温度#1~#7"))
        item = self.tableWidget.item(6, 1)
        item.setText(_translate("MainWindow", "#1"))
        item = self.tableWidget.item(6, 2)
        item.setText(_translate("MainWindow", "#2"))
        item = self.tableWidget.item(6, 3)
        item.setText(_translate("MainWindow", "#3"))
        item = self.tableWidget.item(6, 4)
        item.setText(_translate("MainWindow", "#4"))
        item = self.tableWidget.item(6, 5)
        item.setText(_translate("MainWindow", "#5"))
        item = self.tableWidget.item(6, 6)
        item.setText(_translate("MainWindow", "#6"))
        item = self.tableWidget.item(6, 7)
        item.setText(_translate("MainWindow", "#7"))
        item = self.tableWidget.item(7, 0)
        item.setText(_translate("MainWindow", "℃"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.Graph.setTabText(self.Graph.indexOf(self.Current), _translate("MainWindow", "Current"))
        self.Graph.setTabText(self.Graph.indexOf(self.SOC), _translate("MainWindow", "SOC"))
        self.Graph.setTabText(self.Graph.indexOf(self.Voltage), _translate("MainWindow", "Voltage"))
        self.Clear_DataShow.setText(_translate("MainWindow", "清除显示"))
        self.AutoRead_Checkbox.setText(_translate("MainWindow", "定时读取"))
        self.checkBox.setText(_translate("MainWindow", "存储"))
        self.read_pushbutton.setText(_translate("MainWindow", "读取"))
        self.TimeofPlot.setItemText(0, _translate("MainWindow", "1S"))
        self.TimeofPlot.setItemText(1, _translate("MainWindow", "5S"))
        self.TimeofPlot.setItemText(2, _translate("MainWindow", "10S"))
        self.TimeofPlot.setItemText(3, _translate("MainWindow", "30S"))
        self.menu.setTitle(_translate("MainWindow", "&开始"))
        self.menu_2.setTitle(_translate("MainWindow", "帮助"))
        self.menu_3.setTitle(_translate("MainWindow", "参数配置"))
        self.menuBOOT.setTitle(_translate("MainWindow", "BOOT升级"))
        self.action_2.setText(_translate("MainWindow", "串口设置"))
        self.action_3.setText(_translate("MainWindow", "版本信息"))
        self.action309_RTC.setText(_translate("MainWindow", "309_RTC参数"))
        self.action_LvLi.setText(_translate("MainWindow", "履历"))
        self.action_Upgrade.setText(_translate("MainWindow", "BOOT升级"))
        self.action_Samlltool.setText(_translate("MainWindow", "小工具"))
        self.actionCAN.setText(_translate("MainWindow", "CAN配置"))
