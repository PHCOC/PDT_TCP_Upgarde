# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CSPZ.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from CKPZ_UI import Ui_Form,Timer_ReadMessage,Serial_Port,Timer_500ms,Timer_SendMessage
from PyQt5.QtCore import QTimer

import CANWindows_UI
from CANWindows_UI import CAN_Ui_Form
import  CKPZ_UI

i=0

SH367309_Show_500ms = QTimer()
RTC_Flag = 0
Sh309_Flag = 0
SH367309_EE = ['0a','11','01','0a','11','01','0a','11','01','0a','11','01','0a','11','01','0a','11','01','0a','11','01','0a','11','01','0F','26']
RTC_EE = [19,12,2,2,2,22]

Hex_Dict_Own = {
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


def SH367309_EE_Write(Index, Data):
    SH367309_EE[Index] = Data

def SH367309_EE_Read(Index):
    return SH367309_EE[Index]


class Ui_CSPZ(object):
    def setupUi(self, CSPZ):
        CSPZ.setObjectName("CSPZ")
        CSPZ.resize(724, 657)
        self.tableWidget = QtWidgets.QTableWidget(CSPZ)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 411, 661))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(26)
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
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(19, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(20, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(21, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(22, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(23, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(24, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(25, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.pushButton = QtWidgets.QPushButton(CSPZ)
        self.pushButton.setGeometry(QtCore.QRect(450, 550, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(CSPZ)
        self.pushButton_2.setGeometry(QtCore.QRect(580, 550, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(CSPZ)
        self.pushButton_3.setGeometry(QtCore.QRect(580, 590, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(CSPZ)
        self.pushButton_4.setGeometry(QtCore.QRect(450, 590, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(CSPZ)
        self.pushButton_5.setGeometry(QtCore.QRect(590, 280, 93, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(CSPZ)
        self.pushButton_6.setGeometry(QtCore.QRect(430, 280, 93, 28))
        self.pushButton_6.setObjectName("pushButton_6")
        self.line = QtWidgets.QFrame(CSPZ)
        self.line.setGeometry(QtCore.QRect(410, 320, 311, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.tableWidget_2 = QtWidgets.QTableWidget(CSPZ)
        self.tableWidget_2.setGeometry(QtCore.QRect(410, 0, 311, 261))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        self.line_2 = QtWidgets.QFrame(CSPZ)
        self.line_2.setGeometry(QtCore.QRect(408, 500, 311, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.pushButton_7 = QtWidgets.QPushButton(CSPZ)
        self.pushButton_7.setGeometry(QtCore.QRect(610, 380, 93, 28))
        self.pushButton_7.setObjectName("pushButton_7")
        self.lineEdit = QtWidgets.QLineEdit(CSPZ)
        self.lineEdit.setGeometry(QtCore.QRect(440, 340, 271, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_8 = QtWidgets.QPushButton(CSPZ)
        self.pushButton_8.setGeometry(QtCore.QRect(450, 630, 241, 28))
        self.pushButton_8.setObjectName("pushButton_8")
        self.line_3 = QtWidgets.QFrame(CSPZ)
        self.line_3.setGeometry(QtCore.QRect(410, 410, 311, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(CSPZ)
        self.lineEdit_2.setGeometry(QtCore.QRect(440, 430, 271, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_9 = QtWidgets.QPushButton(CSPZ)
        self.pushButton_9.setGeometry(QtCore.QRect(610, 470, 93, 28))
        self.pushButton_9.setObjectName("pushButton_9")
        self.label_7 = QtWidgets.QLabel(CSPZ)
        self.label_7.setGeometry(QtCore.QRect(463, 520, 60, 21))
        self.label_7.setObjectName("label_7")
        self.comboBox_5 = QtWidgets.QComboBox(CSPZ)
        self.comboBox_5.setGeometry(QtCore.QRect(530, 520, 153, 21))
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
        self.comboBox_5.addItem("")


        self.retranslateUi(CSPZ)
        self.Copy_DefaultValue()
        self.pushButton.clicked.connect(self.Read_309Register)
        self.pushButton_2.clicked.connect(self.Write_309Register)
        self.pushButton_4.clicked.connect(self.Copy_Value)
        self.pushButton_5.clicked.connect(self.Write_RTC)
        self.pushButton_6.clicked.connect(self.Read_RTC)
        QtCore.QMetaObject.connectSlotsByName(CSPZ)

    def Windows_Put(self,Error_Flag):
        if Error_Flag == 1:
            reply = QMessageBox.information(self,  # 使用infomation信息框
                                            "错误信息",
                                            "未打开串口",
                                            QMessageBox.Yes)
        elif Error_Flag == 2:
            reply = QMessageBox.information(self,  # 使用infomation信息框
                                            "错误信息",
                                            "无有效通讯工具",
                                            QMessageBox.Yes)

    def HexToDec(self,x):
        num = 0
        x = str(x)
        # MainWindows.Data_Show.append(str(len(x)))
        for i in range(len(x)):
            str2 = x[i]
            str2 = str2.upper()
            #     MainWindows.Data_Show.append(str(str2))
            num += Hex_Dict_Own[str2] * pow(16, (len(x) - i - 1))
            # MainWindows.Data_Show.append(str(str2))
        return num

    def crc16(self,x):
        Crc_Reg = 0xFFFF
        temp = 0&0xFFFF
        # reply = QMessageBox.information(self,"错误信息",str(x),QMessageBox.Yes | QMessageBox.No)
        # return
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

    def Read_309Register(self):
        global Sh309_Flag
        Sh309_Flag = 1
        SH367309_Show_500ms.start(500)
        SH367309_Show_500ms.timeout.connect(self.Set_Talbe)
        if CANWindows_UI.CAN_OpenFlag == 1:
            BMS_ID = self.comboBox_5.currentText()
            BMS_ID = self.HexToDec(BMS_ID[2:])
            CAN_Ui_Form2 = CAN_Ui_Form()
            CAN_Ui_Form2.CAN_Request_SH367309Parameter(BMS_ID)
        elif CKPZ_UI.SeralPor_OpenFlag == 1:
            if Serial_Port.isOpen():
                send_list = []
                Str_Send = "03 03 76 5C 00 0F"  # DE 76"
                Str_Send = Str_Send.replace(" ", "")
                CRC_Data = str(self.crc16(Str_Send))
                Str_Send = Str_Send + CRC_Data[4:6] + CRC_Data[2:4]
                while Str_Send != '':
                    num = int(Str_Send[0:2], 16)
                    Str_Send = Str_Send[2:].strip()
                    send_list.append(num)
                send_list = bytes(send_list)
                try:
                    Serial_Port.write(send_list)  # item.encode('utf-8'))
                except Exception as e:
                    reply = QMessageBox.information(self, "错误信息", str(e), QMessageBox.Yes | QMessageBox.No)
            else:
                self.Windows_Put(1)
        else:
            self.Windows_Put(2)


    def Write_309Register(self):
        if CANWindows_UI.CAN_OpenFlag == 1:
            BMS_ID = self.comboBox_5.currentText()
            BMS_ID = int(BMS_ID[2:3])*16 + int(BMS_ID[3:])
            send_list = []
            Str_Send = ""
            RowCount = self.tableWidget.rowCount()
            for i in range(RowCount):
                try:
                    Str_Send = Str_Send + self.tableWidget.item(i, 1).text() + " "
                except:
                    reply = QMessageBox.information(self,  # 使用infomation信息框
                                                    "错误信息",
                                                    "有寄存器为空",
                                                    QMessageBox.Yes | QMessageBox.No)
                    return
            Str_Send = Str_Send.upper()
            Str_Send = Str_Send.replace(" ", "")
            CRC16 = self.crc16(Str_Send)
            while Str_Send != '':
                num = int(Str_Send[0:2], 16)
                Str_Send = Str_Send[2:].strip()
                send_list.append(num)
            CAN_Send = CAN_Ui_Form()
            CRC16 = self.HexToDec(CRC16[2:])
            CAN_Send.CAN_Set_SH367309Parameter(BMS_ID,send_list,CRC16)
        elif CKPZ_UI.SeralPor_OpenFlag == 1:
            if Serial_Port.isOpen():
                send_list = []
                Str_Send = "03 10 76 5C 00 0E"
                RowCount = self.tableWidget.rowCount()
                for i in range(RowCount):
                    try:
                        Str_Send = Str_Send + " " + self.tableWidget.item(i, 1).text()
                    except:
                        reply = QMessageBox.information(self,  # 使用infomation信息框
                                                        "错误信息",
                                                        "有寄存器为空",
                                                        QMessageBox.Yes | QMessageBox.No)
                        return
                Str_Send = Str_Send.upper()
                Str_Send = Str_Send.replace(" ", "")
                CRC_Data = str(self.crc16(Str_Send))
                CRC_Data = CRC_Data[2:]
                for i in range(4-len(CRC_Data)):
                    CRC_Data = '0' + CRC_Data
                Str_Send = Str_Send  + CRC_Data[0:2]+ CRC_Data[2:4]
                while Str_Send != '':
                    num = int(Str_Send[0:2], 16)
                    Str_Send = Str_Send[2:].strip()
                    send_list.append(num)
                send_list = bytes(send_list)
                try:
                    Serial_Port.write(send_list)  # item.encode('utf-8'))
                except Exception as e:
                    reply = QMessageBox.information(self,  # 使用infomation信息框
                                                    "错误信息",
                                                    str(e),
                                                    QMessageBox.Yes | QMessageBox.No)
            else:
                self.Windows_Put(1)
        else:
            self.Windows_Put(2)

    def Read_RTC(self):
        global RTC_Flag
        RTC_Flag = 1
        SH367309_Show_500ms.start(500)
        SH367309_Show_500ms.timeout.connect(self.Set_Talbe)
        if CANWindows_UI.CAN_OpenFlag == 1:
            BMS_ID = self.comboBox_5.currentText()
            BMS_ID = self.HexToDec(BMS_ID[2:])
            CAN_Ui_Form2 = CAN_Ui_Form()
            CAN_Ui_Form2.CAN_Request_RTCTime(BMS_ID)
        # elif CKPZ_UI.SeralPor_OpenFlag == 1:
            # if Serial_Port.isOpen():
                # send_list = []
                # Str_Send = "03 03 76 5C 00 0F"  # DE 76"
                # Str_Send = Str_Send.replace(" ", "")
                # CRC_Data = str(self.crc16(Str_Send))
                # Str_Send = Str_Send + CRC_Data[4:6] + CRC_Data[2:4]
                # while Str_Send != '':
                #     num = int(Str_Send[0:2], 16)
                #     Str_Send = Str_Send[2:].strip()
                #     send_list.append(num)
                # send_list = bytes(send_list)
                # try:
                #     Serial_Port.write(send_list)  # item.encode('utf-8'))
                # except Exception as e:
                #     reply = QMessageBox.information(self, "错误信息", str(e), QMessageBox.Yes | QMessageBox.No)
            # else:
            #     self.Windows_Put(1)
        else:
            self.Windows_Put(2)

    def Write_RTC(self):
        if CANWindows_UI.CAN_OpenFlag == 1:
            BMS_ID = self.comboBox_5.currentText()
            BMS_ID = int(BMS_ID[2:3])*16 + int(BMS_ID[3:])
            CAN_Send = CAN_Ui_Form()
            CAN_Send.CAN_Set_RTC(BMS_ID)
        elif CKPZ_UI.SeralPor_OpenFlag == 1:
            if Serial_Port.isOpen():
                send_list = []
                Str_Send = "03 10 76 5C 00 0E"
                RowCount = self.tableWidget.rowCount()
                for i in range(RowCount):
                    try:
                        Str_Send = Str_Send + " " + self.tableWidget.item(i, 1).text()
                    except:
                        reply = QMessageBox.information(self,  # 使用infomation信息框
                                                        "错误信息",
                                                        "有寄存器为空",
                                                        QMessageBox.Yes | QMessageBox.No)
                        return
                Str_Send = Str_Send.upper()
                Str_Send = Str_Send.replace(" ", "")
                CRC_Data = str(self.crc16(Str_Send))
                Str_Send = Str_Send + CRC_Data[4:6] + CRC_Data[2:4]
                while Str_Send != '':
                    num = int(Str_Send[0:2], 16)
                    Str_Send = Str_Send[2:].strip()
                    send_list.append(num)
                send_list = bytes(send_list)
                try:
                    Serial_Port.write(send_list)  # item.encode('utf-8'))
                except Exception as e:
                    reply = QMessageBox.information(self,  # 使用infomation信息框
                                                    "错误信息",
                                                    str(e),
                                                    QMessageBox.Yes | QMessageBox.No)
            else:
                self.Windows_Put(1)
        else:
            self.Windows_Put(2)


    def Copy_DefaultValue(self):
        line_num = 0
        try:
            f = open(".\Deault_Par.txt")  # 返回一个文件对象
            # line = f.readlines()  # 调用文件的 readline()方法
            for line in f.readlines():
                item = QtWidgets.QTableWidgetItem()
                CurLine = line#.strip().split("\t")
                Data = str(CurLine)[0:2]
                item.setText(str(Data))
                self.tableWidget.setItem(int(line_num),0,item)
                line_num = line_num+1
                if line_num> 25:
                    return
            f.close()
        except:
            return

    def Set_Talbe(self):
        global SH367309_EE
        global Sh309_Flag
        global RTC_Flag
        global RTC_EE

        SH367309_Show_500ms.stop()
        if Sh309_Flag == 1:
            for i in range(26):
                item = QtWidgets.QTableWidgetItem()
                item.setText(SH367309_EE[i])
                self.tableWidget.setItem(i, 0, item)
        elif RTC_Flag ==1:
            for i in range(6):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(RTC_EE[i]))
                self.tableWidget_2.setItem(i, 0, item)

        RTC_Flag = 0
        Sh309_Flag = 0


    def Copy_Value(self):
        RowCount = self.tableWidget.rowCount()#读取行数
        for i in range(0,RowCount):
            try:
                item = QtWidgets.QTableWidgetItem()
                Data = self.tableWidget.item(i,0).text()
                item.setText(Data)
                self.tableWidget.setItem(i,1,item)
            except:
                return


    def retranslateUi(self, CSPZ):
        _translate = QtCore.QCoreApplication.translate
        CSPZ.setWindowTitle(_translate("CSPZ", "参数设置"))
        CSPZ.setWindowIcon(QIcon("..\Picture\CSPZWindowsTitle.jpg"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("CSPZ", "SCONF1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("CSPZ", "SCONF2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("CSPZ", "OVT/LDRT /OVH"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("CSPZ", "OVL"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("CSPZ", "UVT/OVRH"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("CSPZ", "OVRL"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("CSPZ", "UV"))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("CSPZ", "UVR"))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("CSPZ", "BALV"))
        item = self.tableWidget.verticalHeaderItem(9)
        item.setText(_translate("CSPZ", "PREV"))
        item = self.tableWidget.verticalHeaderItem(10)
        item.setText(_translate("CSPZ", "L0V"))
        item = self.tableWidget.verticalHeaderItem(11)
        item.setText(_translate("CSPZ", "PFV"))
        item = self.tableWidget.verticalHeaderItem(12)
        item.setText(_translate("CSPZ", "OCD1V/OCD1T"))
        item = self.tableWidget.verticalHeaderItem(13)
        item.setText(_translate("CSPZ", "OCD2V/OCD2T"))
        item = self.tableWidget.verticalHeaderItem(14)
        item.setText(_translate("CSPZ", "SCV/SCT"))
        item = self.tableWidget.verticalHeaderItem(15)
        item.setText(_translate("CSPZ", "OCCV/OCCT"))
        item = self.tableWidget.verticalHeaderItem(16)
        item.setText(_translate("CSPZ", "MOST/OCRT/PFT"))
        item = self.tableWidget.verticalHeaderItem(17)
        item.setText(_translate("CSPZ", "OTC"))
        item = self.tableWidget.verticalHeaderItem(18)
        item.setText(_translate("CSPZ", "OTCR"))
        item = self.tableWidget.verticalHeaderItem(19)
        item.setText(_translate("CSPZ", "UTC"))
        item = self.tableWidget.verticalHeaderItem(20)
        item.setText(_translate("CSPZ", "UTCR"))
        item = self.tableWidget.verticalHeaderItem(21)
        item.setText(_translate("CSPZ", "OTD"))
        item = self.tableWidget.verticalHeaderItem(22)
        item.setText(_translate("CSPZ", "OTDR"))
        item = self.tableWidget.verticalHeaderItem(23)
        item.setText(_translate("CSPZ", "UTD"))
        item = self.tableWidget.verticalHeaderItem(24)
        item.setText(_translate("CSPZ", "UTDR"))
        item = self.tableWidget.verticalHeaderItem(25)
        item.setText(_translate("CSPZ", "TR"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("CSPZ", "读取值"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("CSPZ", "设置值"))
        self.pushButton.setText(_translate("CSPZ", "读取309"))
        self.pushButton_2.setText(_translate("CSPZ", "设置309"))
        self.pushButton_3.setText(_translate("CSPZ", "关闭"))
        self.pushButton_4.setText(_translate("CSPZ", "复制读取值"))
        self.pushButton_5.setText(_translate("CSPZ", "设置RTC"))
        self.pushButton_6.setText(_translate("CSPZ", "读取RTC"))
        item = self.tableWidget_2.verticalHeaderItem(0)
        item.setText(_translate("CSPZ", "年"))
        item = self.tableWidget_2.verticalHeaderItem(1)
        item.setText(_translate("CSPZ", "月"))
        item = self.tableWidget_2.verticalHeaderItem(2)
        item.setText(_translate("CSPZ", "日"))
        item = self.tableWidget_2.verticalHeaderItem(3)
        item.setText(_translate("CSPZ", "时"))
        item = self.tableWidget_2.verticalHeaderItem(4)
        item.setText(_translate("CSPZ", "分"))
        item = self.tableWidget_2.verticalHeaderItem(5)
        item.setText(_translate("CSPZ", "秒"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("CSPZ", "RTC时间"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("CSPZ", "当前时间"))
        self.pushButton_7.setText(_translate("CSPZ", "SN码写入"))
        self.pushButton_8.setText(_translate("CSPZ", "309寄存器参考文档"))
        self.pushButton_9.setText(_translate("CSPZ", "版本号读取"))
        self.label_7.setText(_translate("CSPZ", "BMS地址"))
        self.comboBox_5.setItemText(0, _translate("CSPZ", "0x80"))
        self.comboBox_5.setItemText(1, _translate("CSPZ", "0x81"))
        self.comboBox_5.setItemText(2, _translate("CSPZ", "0x82"))
        self.comboBox_5.setItemText(3, _translate("CSPZ", "0x83"))
        self.comboBox_5.setItemText(4, _translate("CSPZ", "0x84"))
        self.comboBox_5.setItemText(5, _translate("CSPZ", "0x85"))
        self.comboBox_5.setItemText(6, _translate("CSPZ", "0x86"))
        self.comboBox_5.setItemText(7, _translate("CSPZ", "0x87"))
        self.comboBox_5.setItemText(8, _translate("CSPZ", "0x88"))
        self.comboBox_5.setItemText(9, _translate("CSPZ", "0x89"))
        self.comboBox_5.setItemText(10, _translate("CSPZ", "0x8A"))
        self.comboBox_5.setItemText(11, _translate("CSPZ", "0x8B"))
        self.comboBox_5.setItemText(12, _translate("CSPZ", "0x8C"))
        self.comboBox_5.setItemText(13, _translate("CSPZ", "0x8D"))
        self.comboBox_5.setItemText(14, _translate("CSPZ", "0x8E"))
        self.comboBox_5.setItemText(15, _translate("CSPZ", "0x8F"))
        self.comboBox_5.setItemText(16, _translate("CSPZ", "0xFF"))
