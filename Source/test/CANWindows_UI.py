# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CANWindows.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from ctypes import *
from PyQt5.QtCore import QTimer
from CKPZ_UI import Timer_ReadMessage
import time
import CKPZ_UI

CAN_OpenFlag = 0
CANPort_Information = ''
CANDeviceNameNumber = 3
CANDeviceIndexNumber = 0
CANDeviceChannelNumber = 0
CANSendTime = QTimer()
CANReceiveTime = QTimer()

CANBuffer = [[0 for x in range(10)] for y in range(50)]#50帧的数据缓存

class _VCI_INIT_CONFIG(Structure):
    _fields_ = [('AccCode', c_ulong),
                ('AccMask', c_ulong),
                ('Reserved', c_ulong),
                ('Filter', c_ubyte),
                ('Timing0', c_ubyte),
                ('Timing1', c_ubyte),
                ('Mode', c_ubyte)]

def crc16(self, x):
    Crc_Reg = 0xFFFF
    temp = 0 & 0xFFFF
    while x != '':
        Data = x[:2]
        x = x[2:].strip()
        byte = self.HexToDec(Data)
        Crc_Reg ^= byte
        for i in range(8):
            if Crc_Reg & 0x0001 == 1:
                Crc_Reg >>= 1
                Crc_Reg ^= 0xA001  # 0xA001是0x8005循环右移16位的值
            else:
                Crc_Reg >>= 1

    return hex(Crc_Reg)


class _VCI_CAN_OBJ(Structure):
    _fields_ = [('ID', c_uint),
                ('TimeStamp', c_uint),
                ('TimeFlag', c_byte),
                ('SendType', c_byte),
                ('RemoteFlag', c_byte),
                ('ExternFlag', c_byte),
                ('DataLen', c_byte),
                ('Data', c_byte*8),
                ('Reserved', c_byte*3)]


class CAN_Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(487, 213)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(250, 60, 181, 31))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.comboBox_4 = QtWidgets.QComboBox(self.widget)
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.gridLayout.addWidget(self.comboBox_4, 0, 1, 1, 1)
        self.widget1 = QtWidgets.QWidget(Form)
        self.widget1.setGeometry(QtCore.QRect(10, 20, 221, 121))
        self.widget1.setObjectName("widget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.widget1)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.widget1)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_2.addWidget(self.comboBox, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget1)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(self.widget1)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_3, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.widget1)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_2, 2, 1, 1, 1)
        self.widget2 = QtWidgets.QWidget(Form)
        self.widget2.setGeometry(QtCore.QRect(220, 160, 241, 30))
        self.widget2.setObjectName("widget2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton = QtWidgets.QPushButton(self.widget2)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_3.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.pushButton_2, 0, 1, 1, 1)

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(self.CAN_Init)
        self.pushButton_2.clicked.connect(self.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def ShowErrorInfor(self,ErrorFlag):
        if ErrorFlag == 0:
            QMessageBox.information(self,  # 使用infomation信息框
                                    "错误信息",
                                    "CAN打开失败,请检查配置参数",
                                    QMessageBox.Yes | QMessageBox.No)
        elif ErrorFlag == 1:
            QMessageBox.information(self,  # 使用infomation信息框
                                    "错误信息",
                                    "无法打开动态链接库文件",
                                    QMessageBox.Yes | QMessageBox.No)
        elif ErrorFlag == 2:
            QMessageBox.information(self,  # 使用infomation信息框
                                    "错误信息",
                                    "CAN未打开",
                                    QMessageBox.Yes | QMessageBox.No)
        elif ErrorFlag == 3:
            QMessageBox.information(self,  # 使用infomation信息框
                                    "错误信息",
                                    "已打开其余通讯工具",
                                    QMessageBox.Yes | QMessageBox.No)

    def CAN_SendData(self,CAN_ID,CAN_ExternFlag,Data):
        if CAN_OpenFlag == 0:
            self.ShowErrorInfor(2)
            self.CAN_Close()
            return
        canLib = windll.LoadLibrary('..\DLL\ControlCAN.dll')
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global CANDeviceChannelNumber
        vco = _VCI_CAN_OBJ()
        vco.ID = CAN_ID
        vco.SendType = 0
        vco.RemoteFlag = 0
        vco.ExternFlag = CAN_ExternFlag
        vco.DataLen = 8
        vco.Data = Data#(1, 2, 3, 4, 5, 6, 7, 8)
        ReturnFlag = canLib.VCI_Transmit(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber, pointer(vco), 1)

    def CAN_Init(self):
        if CKPZ_UI.SeralPor_OpenFlag == 1:
            self.ShowErrorInfor(3)
            return
        vic = _VCI_INIT_CONFIG()
        vic.AccCode = 0x00000000
        vic.AccMask = 0xffffffff
        vic.Filter = 0
        global CAN_OpenFlag
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global CANDeviceChannelNumber
        global CANPort_Information
        CANDeviceName = self.comboBox.currentText()
        if CANDeviceName == 'USBCAN1':
            CANDeviceNameNumber = 3
        elif CANDeviceName == 'USBCAN2':
            CANDeviceNameNumber = 4
        CANDeviceIndex = self.comboBox_3.currentText()
        CANDeviceIndexNumber = int(CANDeviceIndex)
        CANDeviceChannel = self.comboBox_4.currentText()
        CANDeviceChannelNumber = int(CANDeviceChannel)
        BoundRate = self.comboBox_2.currentText()
        if BoundRate == '10Kbps':
            vic.Timing0 = 0x31
            vic.Timing1 = 0x1C
        elif BoundRate == '50Kbps':
            vic.Timing0 = 0x09
            vic.Timing1 = 0x1C
        elif BoundRate == '100Kbps':
            vic.Timing0 = 0x04
            vic.Timing1 = 0x1C
        elif BoundRate == '125Kbps':
            vic.Timing0 = 0x03
            vic.Timing1 = 0x1C
        elif BoundRate == '200Kbps':
            vic.Timing0 = 0x81
            vic.Timing1 = 0xFA
        elif BoundRate == '250Kbps':
            vic.Timing0 = 0x01
            vic.Timing1 = 0x1C
        elif BoundRate == '500Kbps':
            vic.Timing0 = 0x00
            vic.Timing1 = 0x1C
        elif BoundRate == '1000Kbps':
            vic.Timing0 = 0x09
            vic.Timing1 = 0x14
        vic.Mode = 0

        if self.pushButton.text() == "确认并打开":
            try:
                canLib = windll.LoadLibrary('..\DLL\ControlCAN.dll')
                ReturnData = canLib.VCI_OpenDevice(CANDeviceNameNumber, CANDeviceIndexNumber, 0)
                if ReturnData != 1:
                    self.ShowErrorInfor(0)
                    return
                # ReturnData = canLib.VCI_SetReference(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber, 0, pointer(c_int(0x060003)))
                # if ReturnData != 1:
                #     self.ShowErrorInfor(0)
                #     return
                ReturnData = canLib.VCI_InitCAN(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber, pointer(vic))
                if ReturnData != 1:
                    self.ShowErrorInfor(0)
                    return
                ReturnData = canLib.VCI_StartCAN(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber)
                if ReturnData != 1:
                    self.ShowErrorInfor(0)
                    return
                self.pushButton.setText(QtCore.QCoreApplication.translate("Form", "关闭CAN"))
                self.comboBox.setEnabled(False)
                self.comboBox_2.setEnabled(False)
                self.comboBox_3.setEnabled(False)
                self.comboBox_4.setEnabled(False)
                self.comboBox.setEnabled(False)
                CKPZ_UI.Timer_ReadMessage.start(100)
                CAN_OpenFlag = 1
                CANPort_Information = CANDeviceName + '  波特率：' + BoundRate + '  通道号：' + CANDeviceChannel
            except:
                self.ShowErrorInfor(1)
        elif self.pushButton.text() == "关闭CAN":
            self.CAN_Close()

    def CAN_Close(self):
        global CAN_OpenFlag
        canLib = windll.LoadLibrary('..\DLL\ControlCAN.dll')
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        canLib.VCI_CloseDevice(CANDeviceNameNumber, CANDeviceIndexNumber)
        self.pushButton.setText(QtCore.QCoreApplication.translate("Form", "确认并打开"))
        self.comboBox.setEnabled(True)
        self.comboBox_2.setEnabled(True)
        self.comboBox_3.setEnabled(True)
        self.comboBox_4.setEnabled(True)
        self.comboBox.setEnabled(True)
        CAN_OpenFlag = 0

    def CAN_Request_ModuleVoltage(self,BMS_ID):
        BMS_ID = 0x1800FF01 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x02,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_Request_ModuleCurrent(self,BMS_ID):
        BMS_ID = 0x1800FF01 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x02,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_Request_ModuleSOC(self,BMS_ID):
        BMS_ID = 0x1800FF01 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x03,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_Request_RemainCap(self,BMS_ID):
        BMS_ID = 0x1800FF01 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x04,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_Request_FullChargeCap(self,BMS_ID):
        BMS_ID = 0x1800FF01 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x05,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_Request_DesignedCap(self,BMS_ID):
        BMS_ID = 0x1800FF01 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x06,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_Request_CellCycle(self,BMS_ID):
        BMS_ID = 0x1800FF01 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x07,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_Request_BMSStatus(self,BMS_ID):
        BMS_ID = 0x1800FF01 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x08,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_Request_CellVoltage(self,BMS_ID):
        BMS_ID = 0x1800FF01 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x09,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_Request_CellTemperature(self,BMS_ID):
        BMS_ID = 0x1800FF01 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x0A,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_Request_RTCTime(self,BMS_ID):
        BMS_ID = 0x1800FF01 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x0B,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_Request_AllInformation(self,BMS_ID):
        BMS_ID = 0x1800FF01 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x0F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_Request_SH367309Parameter(self,BMS_ID):
        BMS_ID = 0x1800FF02 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x01,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_Request_BMSParameter(self,BMS_ID):
        BMS_ID = 0x1800FF02 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x02,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_Set_SH367309Parameter(self,BMS_ID,Data,CRC16):
        BMS_ID = 0x1800FF03 + BMS_ID*0x10000
        self.CAN_SendData(BMS_ID,1,(0x01,0x00,CRC16//256,CRC16%256,0xFF,0xFF,0xFF,0xFF))#开始下发参数
        time.sleep(0.01)
        self.CAN_SendData(BMS_ID,1,(0x01,0x01,Data[0],Data[1],Data[2],Data[3],Data[4],Data[5]))#SCONF1/SCONF2/OVT/OVL/UVT/OVRL
        time.sleep(0.01)
        self.CAN_SendData(BMS_ID,1,(0x01,0x02,Data[6],Data[7],Data[8],Data[9],Data[10],Data[11]))#UV/UVR/BALV/PREV/L0V/PFV
        time.sleep(0.01)
        self.CAN_SendData(BMS_ID,1,(0x01,0x03,Data[12],Data[13],Data[14],Data[15],Data[16],Data[17]))#OCD1V/OCD2V/SCV/OCCV/MOST/OTC
        time.sleep(0.01)
        self.CAN_SendData(BMS_ID,1,(0x01,0x04,Data[18],Data[19],Data[20],Data[21],Data[22],Data[23]))#OTCR/UTC/UTCR/OTD/OTDR/UTD
        time.sleep(0.01)
        self.CAN_SendData(BMS_ID,1,(0x01,0x05,Data[24],Data[25],0xFF,0xFF,0xFF,0xFF))#UTDR/TR
        time.sleep(0.01)
        self.CAN_SendData(BMS_ID,1,(0x01,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))#结束下发参数
        time.sleep(0.01)

    def CAN_Set_RTC(self,BMS_ID):
        BMS_ID = 0x1800FF03 + BMS_ID*0x10000
        Year = int(time.strftime('%Y', time.localtime(time.time())))-2000
        Mouth = int(time.strftime('%m', time.localtime(time.time())))
        Day = int(time.strftime('%d', time.localtime(time.time())))
        Hour = int(time.strftime('%H', time.localtime(time.time())))
        Min = int(time.strftime('%M', time.localtime(time.time())))
        Sec = int(time.strftime('%S', time.localtime(time.time())))
        self.CAN_SendData(BMS_ID,1,(0x03,Year,Mouth,Day,Hour,Min,Sec,0xFF))


    def CAN_ReceiveData(self):
        if CAN_OpenFlag == 0:
            return 0
        canLib = windll.LoadLibrary('..\DLL\ControlCAN.dll')
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global CANDeviceChannelNumber
        Voc = _VCI_CAN_OBJ()
        Num = canLib.VCI_GetReceiveNum(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber)
        if Num>0:
            if Num < 50:
                for i in range(Num):
                    ret = canLib.VCI_Receive(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber, byref(Voc), 1, 0)
                    CANBuffer[i][0] = Voc.ID
                    CANBuffer[i][1] = Voc.ExternFlag
                    for j in range(8):
                        if  Voc.Data[j]>=0:
                            CANBuffer[i][2+j] = Voc.Data[j]
                        else:
                            CANBuffer[i][2+j] = Voc.Data[j]+256

            else:
                Num = 50
                for i in range(Num):
                    ret = canLib.VCI_Receive(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber, byref(Voc), 1, 0)
                    CANBuffer[i][0] = Voc.ID
                    CANBuffer[i][0] = Voc.ExternFlag
                    for j in range(8):
                        CANBuffer[i][2+j] = Voc.Data[j]
        canLib.VCI_ClearBuffer(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber)
        return Num


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "CAN通讯配置"))
        Form.setWindowIcon(QIcon("..\Picture\CANWindowsTitle.jpg"))
        self.label_4.setText(_translate("Form", "通道号"))
        self.comboBox_4.setItemText(0, _translate("Form", "0"))
        self.comboBox_4.setItemText(1, _translate("Form", "1"))
        self.label.setText(_translate("Form", "can设备"))
        self.comboBox.setItemText(0, _translate("Form", "USBCAN2"))
        self.comboBox.setItemText(1, _translate("Form", "USBCAN1"))
        self.label_3.setText(_translate("Form", "设备索引号"))
        self.comboBox_3.setItemText(0, _translate("Form", "0"))
        self.comboBox_3.setItemText(1, _translate("Form", "1"))
        self.comboBox_3.setItemText(2, _translate("Form", "2"))
        self.comboBox_3.setItemText(3, _translate("Form", "3"))
        self.comboBox_3.setItemText(4, _translate("Form", "4"))
        self.comboBox_3.setItemText(5, _translate("Form", "5"))
        self.comboBox_3.setItemText(6, _translate("Form", "6"))
        self.comboBox_3.setItemText(7, _translate("Form", "7"))
        self.label_2.setText(_translate("Form", "波特率"))
        self.comboBox_2.setItemText(0, _translate("Form", "10Kbps"))
        self.comboBox_2.setItemText(1, _translate("Form", "50Kbps"))
        self.comboBox_2.setItemText(2, _translate("Form", "100Kbps"))
        self.comboBox_2.setItemText(3, _translate("Form", "125Kbps"))
        self.comboBox_2.setItemText(4, _translate("Form", "200Kbps"))
        self.comboBox_2.setItemText(5, _translate("Form", "250Kbps"))
        self.comboBox_2.setItemText(6, _translate("Form", "500Kbps"))
        self.comboBox_2.setItemText(7, _translate("Form", "1000Kbps"))
        self.pushButton.setText(_translate("Form", "确认并打开"))
        self.pushButton_2.setText(_translate("Form", "取消"))

