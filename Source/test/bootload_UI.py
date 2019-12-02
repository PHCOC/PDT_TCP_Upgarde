# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bootload.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from CKPZ_UI import Ui_Form,Timer_ReadMessage,Serial_Port,Timer_SendMessage
from CANWindows_UI import CAN_Ui_Form
import CKPZ_UI
import CANWindows_UI
import time
import binascii
from PyQt5.QtCore import QTimer

File_Data = ""
File_Name = ""
File_ByteNum = 0

File_CRC = 0
BMS_ID = 0
BMS_Version = 0
Upgrade_Step = 0
Upgrade_Count = 0
Upgrade_PackIndex = 0
Upgrade_Pack_OK = 0
FileOpen_Flag = 0
g_Str_CRC = 0
g_Str_Index = 0

Upgrade_Timer_500ms = QTimer()

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

class Bootloader(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(780, 364)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(0, 110, 781, 251))
        self.textBrowser.setObjectName("textBrowser")
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(130, 80, 316, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 95, 100))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setGeometry(QtCore.QRect(130, 10, 631, 31))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label_2 = QtWidgets.QLabel(self.splitter)
        self.label_2.setObjectName("label_2")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(140, 50, 221, 23))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.comboBox = QtWidgets.QComboBox(self.widget)
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
        self.horizontalLayout.addWidget(self.comboBox)

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(self.OpenFile)
        Upgrade_Timer_500ms.timeout.connect(self.UpgardeStep)
        self.pushButton_2.clicked.connect(self.Upgrade_Start)
        self.pushButton_3.clicked.connect(self.Upgrade_Stop)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def OpenFile(self):
        global File_Data
        global File_ByteNum
        global File_CRC
        global FileOpen_Flag
        # directory1 = QFileDialog.getExistingDirectory(self,
        #                                               "选取文件夹",
        #                                               "./")  # 起始路径
        # print(directory1)

        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "./",
                                                          "Bin Files (*.bin)")  # 设置文件扩展名过滤,注意用双分号间隔
        # print(fileName1, filetype)
        # str = fileName1
        File_Data = ""
        if fileName1 == "":
            FileOpen_Flag = 0
            pass
        else:
            file = open(fileName1,'rb')
            i = 0
            while 1:
                Data = file.read(1)
                if i> 60000:
                    break
                if Data == b'':
                    break
                sss = str(binascii.b2a_hex(Data))
                sss = str(binascii.b2a_hex(Data))[2:-1]
                File_Data = File_Data + sss
                i+= 1
            File_ByteNum = i
            file.close()
            self.textBrowser.append(File_Data)
            self.label_2.setText(fileName1)
            File_CRC = self.crc16(File_Data)
            FileOpen_Flag = 1

    def crc16(self, x):
        Crc_Reg = 0xFFFF
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

    def crc16_List(self,x,Num):
        Crc_Reg = 0xFFFF
        for i in range(Num):
            Data = x[i]
            Crc_Reg ^= Data
            for i in range(8):
                if Crc_Reg & 0x0001 == 1:
                    Crc_Reg >>= 1
                    Crc_Reg ^= 0xA001  # 0xA001是0x8005循环右移16位的值
                else:
                    Crc_Reg >>= 1

        return hex(Crc_Reg)

    def HexToDec(self,x):
        num = 0
        x = str(x)
        # MainWindows.Data_Show.append(str(len(x)))
        for i in range(len(x)):
            str2 = x[i]
            str2 = str2.upper()
            #     MainWindows.Data_Show.append(str(str2))
            num += Hex_Dict[str2] * pow(16, (len(x) - i - 1))
            # MainWindows.Data_Show.append(str(str2))
        return num

    def Windows_Put(self,Error_Flag):
        if Error_Flag == 1:
            reply = QMessageBox.information(self,  # 使用infomation信息框
                                            "错误",
                                            "无法进入BOOT",
                                            QMessageBox.Yes)
        elif Error_Flag == 2:
            reply = QMessageBox.information(self,  # 使用infomation信息框
                                            "错误",
                                            "检验信息失败",
                                            QMessageBox.Yes)
        elif Error_Flag == 3:
            reply = QMessageBox.information(self,  # 使用infomation信息框
                                            "错误",
                                            "包数据CRC 校验失败",
                                            QMessageBox.Yes)
        elif Error_Flag == 4:
            reply = QMessageBox.information(self,  # 使用infomation信息框
                                            "错误",
                                            "总 CRC 校验失败",
                                            QMessageBox.Yes)

    def Windows_Print(self,Data):
        reply = QMessageBox.information(self,  # 使用infomation信息框
                                        "提示",
                                        Data,
                                        QMessageBox.Yes)

    def Upgrade_Start(self):
        global BMS_ID
        global Upgrade_Step
        global Upgrade_PackIndex
        global FileOpen_Flag
        if (CANWindows_UI.CAN_OpenFlag == 1) :
            BMS_ID = self.comboBox.currentText()
            BMS_ID = int(BMS_ID[2:3])*16 + int(BMS_ID[3:])
            Upgrade_Timer_500ms.start(500)
            Upgrade_Step = 0
            Upgrade_PackIndex = 1
        elif (CKPZ_UI.SeralPor_OpenFlag == 1):
            Timer_SendMessage.stop()
            if Serial_Port.isOpen():
                send_list = [128,240,1,245,232]
                #Str_Send = "80 F0 01 F5 E8"
                send_list = bytes(send_list)
                try:
                    Serial_Port.write(send_list)  # item.encode('utf-8'))
                except Exception as e:
                    pass

            Upgrade_Timer_500ms.start(500)
            Upgrade_Step = 0
            Upgrade_PackIndex = 1
        elif FileOpen_Flag == 0:
            self.Windows_Print("未打开升级文件")
        else:
            self.Windows_Print("未打开通讯工具")

    def Upgrade_Stop(self):
        global Upgrade_Step
        global Upgrade_PackIndex
        global FileOpen_Flag
        Upgrade_Timer_500ms.start(500)
        Upgrade_Step = 3
        Upgrade_PackIndex = 1
        FileOpen_Flag = 0

    def UpgardeStep(self):
        global Upgrade_Step
        global Upgrade_Count
        if Upgrade_Step == 0:#开始升级
            if Upgrade_Count < 5:
                if (CANWindows_UI.CAN_OpenFlag == 1) :
                    self.CAN_UpgradeStart()
                    Upgrade_Count += 1
                elif (CKPZ_UI.SeralPor_OpenFlag == 1):
                    self.UART_UpgradeStart()
                    Upgrade_Count += 1

            else:
                Upgrade_Count = 0
                Upgrade_Step = 3
                pass
        if Upgrade_Step == 1:#校验信息
            if Upgrade_Count < 5:
                if (CANWindows_UI.CAN_OpenFlag == 1) :
                    self.CAN_UpgradeCheckInformation()
                    Upgrade_Count += 1
                elif (CKPZ_UI.SeralPor_OpenFlag == 1):
                    self.UART_UpgradeCheckInformation()
                    Upgrade_Count += 1
            else:
                Upgrade_Count = 0
                Upgrade_Step = 3
        if Upgrade_Step == 2:#文件
            if Upgrade_Count < 5:
                if (CANWindows_UI.CAN_OpenFlag == 1) :
                    self.CAN_UpgradeData()
                    Upgrade_Count += 1
                elif (CKPZ_UI.SeralPor_OpenFlag == 1):
                    self.UART_UpgradeData()
                    Upgrade_Count += 1
            else:
                Upgrade_Count = 0
                Upgrade_Step = 3
        if Upgrade_Step == 3:#结束
            Upgrade_Count += 1
            if Upgrade_Count % 3 == 1:
                if (CANWindows_UI.CAN_OpenFlag == 1) :
                    self.CAN_UpgradeStop()
                    Upgrade_Count += 1
                elif (CKPZ_UI.SeralPor_OpenFlag == 1):
                    self.UART_UpgradeStop()
                    Upgrade_Count += 1
            elif Upgrade_Count > 20:
                Upgrade_Count = 0
                Upgrade_Timer_500ms.stop()
                self.Windows_Print("升级失败")
                self.comboBox.setEnabled(True)

    def CAN_UpgradeStart(self):
        global BMS_ID
        Temp = 0x1800FFF0 + BMS_ID*0x10000
        CAN_Ui_Form2 = CAN_Ui_Form()
        CAN_Ui_Form2.CAN_SendData(Temp,1,(0x01,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def CAN_UpgradeCheckInformation(self):
        global File_CRC
        global BMS_ID
        global File_ByteNum
        Temp = 0x1800FFF0 + BMS_ID*0x10000
        File_ByteNum_H = File_ByteNum // 256
        File_ByteNum_L = File_ByteNum % 256
        File_CRC_H = self.HexToDec(File_CRC[2:])//256
        File_CRC_L = self.HexToDec(File_CRC[2:])%256
        File_PackNum_L = File_ByteNum // 256+1

        CAN_Ui_Form2 = CAN_Ui_Form()

        CAN_Ui_Form2.CAN_SendData(Temp+1,1,(0x01,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))#开始
        time.sleep(0.03)
        CAN_Ui_Form2.CAN_SendData(Temp+1,1,(0x01,0x01,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))#开始
        time.sleep(0.03)
        CAN_Ui_Form2.CAN_SendData(Temp+1,1,(0x01,0x02,File_ByteNum_H,File_ByteNum_L,0x00,File_PackNum_L,File_CRC_H,File_CRC_L))#开始
        time.sleep(0.03)
        CAN_Ui_Form2.CAN_SendData(Temp+1,1,(0x01,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))#开始

    def CAN_UpgradeData(self):
        global Upgrade_PackIndex
        global Upgrade_Step
        global File_Data
        global File_ByteNum
        global BMS_ID
        global Upgrade_Pack_OK
        global g_Str_CRC
        global g_Str_Index

        CAN_Ui_Form2 = CAN_Ui_Form()
        Temp = 0x1800FFF0 + BMS_ID*0x10000
        if Upgrade_Pack_OK != 1:
            CAN_Ui_Form2.CAN_SendData(Temp + 2, 1, (g_Str_Index,0xFF,g_Str_CRC//256,g_Str_CRC%256,0xFF,0xFF,0xFF,0xFF))
            return

        Data = [0 for i in range(1024)]
        Temp_Str = ""
        Send_ByteNum = 0
        Pack_Byte_Num = 256
        if Upgrade_PackIndex/File_ByteNum*256*100 > 100:
            self.progressBar.setValue(100)
        else:
            self.progressBar.setValue(Upgrade_PackIndex / File_ByteNum * 256 * 100)
        if Upgrade_PackIndex*Pack_Byte_Num < File_ByteNum:
            Temp_Str = File_Data[Upgrade_PackIndex*Pack_Byte_Num*2-Pack_Byte_Num*2:Pack_Byte_Num*2+Upgrade_PackIndex*Pack_Byte_Num*2-Pack_Byte_Num*2]
            for i in range(Pack_Byte_Num):
                sdgsd = self.HexToDec(File_Data[i*2+Upgrade_PackIndex*2*Pack_Byte_Num-Pack_Byte_Num*2:i*2+2+Upgrade_PackIndex*Pack_Byte_Num*2-Pack_Byte_Num*2])
                Data[i] = sdgsd
        elif Upgrade_PackIndex*Pack_Byte_Num > File_ByteNum+Pack_Byte_Num:
            return
        else:
            Temp_Str = File_Data[Upgrade_PackIndex*Pack_Byte_Num*2-Pack_Byte_Num*2:File_ByteNum*2]
            for i in range(File_ByteNum+Pack_Byte_Num-Upgrade_PackIndex*Pack_Byte_Num):
                Data[i] = self.HexToDec(File_Data[i*2+Upgrade_PackIndex*Pack_Byte_Num*2-Pack_Byte_Num*2:i*2+2+Upgrade_PackIndex*Pack_Byte_Num*2-Pack_Byte_Num*2])
        Send_ByteNum = i+1
        Temp_Str = self.crc16(Temp_Str)
        Temp_Str = self.HexToDec(Temp_Str[2:])

        CAN_Ui_Form2.CAN_SendData(Temp + 2, 1, (Upgrade_PackIndex,0x00,Temp_Str//256,Temp_Str%256,0xFF,0xFF,0xFF,0xFF))  # 开始
        time.sleep(0.2)

        if Upgrade_PackIndex <= 240:
            i=0
            Temp_Data = [0 for i in range(6)]
            for i in range(Send_ByteNum // 6):
                CAN_Ui_Form2.CAN_SendData(Temp + 2, 1, (Upgrade_PackIndex, i+1, Data[i*6], Data[i*6+1],  Data[i*6+2],  Data[i*6+3],  Data[i*6+4],  Data[i*6+5]))  # 开始
                time.sleep(0.01)
            for j in range(Send_ByteNum % 6):
                Temp_Data[j] =  Data[(i+1)*6+j]
            for j in range(6 - Send_ByteNum % 6):
                Temp_Data[5-j] = 0
            CAN_Ui_Form2.CAN_SendData(Temp + 2, 1, (Upgrade_PackIndex, i+2, Temp_Data[0], Temp_Data[1],  Temp_Data[2],  Temp_Data[3],  Temp_Data[4],  Temp_Data[5]))  # 开始
            time.sleep(0.01)
            Upgrade_Pack_OK = 0
            CAN_Ui_Form2.CAN_SendData(Temp + 2, 1, (Upgrade_PackIndex,0xFF,Temp_Str//256,Temp_Str%256,0xFF,0xFF,0xFF,0xFF))
            g_Str_Index = Upgrade_PackIndex
            g_Str_CRC = Temp_Str
        else:
            Upgrade_PackIndex = 1
            Upgrade_Pack_OK = 0
            Upgrade_Step = 3

    def CAN_UpgradeStop(self):
        global BMS_ID
        Temp = 0x1800FFF0 + BMS_ID*0x10000
        CAN_Ui_Form2 = CAN_Ui_Form()
        CAN_Ui_Form2.CAN_SendData(Temp+3,1,(0x01,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF))

    def Upgrade_BMS_CANResponse(self,Data,Index):
        global BMS_ID
        global Upgrade_Step
        global Upgrade_PackIndex
        global Upgrade_Pack_OK
        global Upgrade_Count

        Temp = 0x18FF00F0 + BMS_ID*0x100
        if Data[Index][0] == Temp:#开始升级
            Upgrade_Count = 0
            if Data[Index][3] == 1:#成功
                if  Upgrade_Step == 0:
                    self.comboBox.setEnabled(False)
                    Upgrade_Step = 1
            elif Data[Index][3] == 0:
                self.Windows_Put(1)
                Upgrade_Step = 3
        elif Data[Index][0] == Temp+1:#下发校验
            Upgrade_Count = 0
            if Data[Index][3] == 1 and Upgrade_Step == 1:#成功
                Upgrade_Pack_OK = 1
                Upgrade_Step = 2
            elif Data[Index][3] == 0:
                self.Windows_Put(2)
                Upgrade_Step = 3
        elif Data[Index][0] == Temp+2:
            Upgrade_Count = 0
            if Data[Index][3] == 2:
                i = 1
            if Data[Index][4] == Upgrade_PackIndex:
                if Data[Index][3] == 1 and Upgrade_Step == 2:#成功
                    Upgrade_Pack_OK = 1
                    Upgrade_PackIndex += 1
                elif Data[Index][3] == 2:
                    Upgrade_Pack_OK = 1#添加重发
                elif Data[Index][3] == 3:
                    Upgrade_Step = 3
                elif Data[Index][3] == 4:
                    self.Windows_Put(4)
                    Upgrade_Step = 3
        elif Data[Index][0] == Temp+3:
            Upgrade_Count = 0
            if Data[Index][3] == 1 and Upgrade_Step == 3:#成功
                Upgrade_Timer_500ms.stop()
                Upgrade_Step = 4
                self.comboBox.setEnabled(True)
                str2 = "升级成功，版本号："+str(Data[Index][4])+str(Data[Index][5])+str(Data[Index][6])+str(Data[Index][7])
                self.Windows_Print(str2)
            elif Data[Index][3] == 0:#失败
                self.Windows_Print("进入APP失败")
                Upgrade_Step = 4

    def UART_UpgradeStart(self):
        Timer_SendMessage.stop()
        if Serial_Port.isOpen():
            send_list = [128,240,1,245,232]
            #Str_Send = "80 F0 01 F5 E8"
            send_list = bytes(send_list)
            try:
                Serial_Port.write(send_list)  # item.encode('utf-8'))
            except Exception as e:
                pass

    def UART_UpgradeCheckInformation(self):
        global File_CRC
        global File_ByteNum
        Timer_SendMessage.stop()
        if Serial_Port.isOpen():
            send_list = [128,241,1,8]
            send_list.append(1)
            send_list.append(1)
            send_list.append(self.HexToDec(File_CRC[2:])//256)
            send_list.append(self.HexToDec(File_CRC[2:])%256)
            send_list.append(File_ByteNum // 256+1)
            send_list.append(0)
            send_list.append(File_ByteNum % 256)
            send_list.append(File_ByteNum // 256)
            CRC16 = self.crc16_List(send_list,12)
            send_list.append(self.HexToDec(CRC16[2:])%256)
            send_list.append(self.HexToDec(CRC16[2:])//256)
            send_list = bytes(send_list)
            try:
                Serial_Port.write(send_list)  # item.encode('utf-8'))
            except Exception as e:
                pass

    def UART_UpgradeData(self):
        global Upgrade_PackIndex
        global Upgrade_Step
        global File_Data
        global File_ByteNum
        global BMS_ID
        global Upgrade_Pack_OK

        if Upgrade_Pack_OK != 1:
            return

        Data = [0 for i in range(299)]
        Data[0] = 0x80
        Data[1] = 0xF2
        Data[2] = 0x01

        Pack_Byte_Num = 256
        i = 0
        if Upgrade_PackIndex / File_ByteNum * 256 * 100 > 100:
            self.progressBar.setValue(100)
        else:
            self.progressBar.setValue(Upgrade_PackIndex / File_ByteNum * 256 * 100)
        if Upgrade_PackIndex * Pack_Byte_Num < File_ByteNum:
            Temp_Str = File_Data[
                       Upgrade_PackIndex * Pack_Byte_Num * 2 - Pack_Byte_Num * 2:Pack_Byte_Num * 2 + Upgrade_PackIndex * Pack_Byte_Num * 2 - Pack_Byte_Num * 2]
            for i in range(Pack_Byte_Num):
                sdgsd = self.HexToDec(File_Data[
                                      i * 2 + Upgrade_PackIndex * 2 * Pack_Byte_Num - Pack_Byte_Num * 2:i * 2 + 2 + Upgrade_PackIndex * Pack_Byte_Num * 2 - Pack_Byte_Num * 2])
                Data[i+6] = sdgsd
        elif Upgrade_PackIndex * Pack_Byte_Num > File_ByteNum + Pack_Byte_Num:
            return
        else:
            Temp_Str = File_Data[Upgrade_PackIndex * Pack_Byte_Num * 2 - Pack_Byte_Num * 2:File_ByteNum * 2]
            for i in range(File_ByteNum + Pack_Byte_Num - Upgrade_PackIndex * Pack_Byte_Num):
                Data[i+6] = self.HexToDec(File_Data[
                                        i * 2 + Upgrade_PackIndex * Pack_Byte_Num * 2 - Pack_Byte_Num * 2:i * 2 + 2 + Upgrade_PackIndex * Pack_Byte_Num * 2 - Pack_Byte_Num * 2])
        Data[3] = Upgrade_PackIndex
        Data[4] = (i + 1) % 256
        Data[5] = (i + 1) // 256
        CRC16 = self.crc16_List(Data,i + 7)
        Data[i + 7] = self.HexToDec(CRC16[2:])//256
        Data[i + 8] = self.HexToDec(CRC16[2:])%256

        Upgrade_Pack_OK = 0
        send_list = bytes(Data)
        try:
            Serial_Port.write(send_list)  # item.encode('utf-8'))
        except Exception as e:
            Upgrade_Pack_OK = 1

    def UART_UpgradeStop(self):
        Timer_SendMessage.stop()
        if Serial_Port.isOpen():
            send_list = [128,243,1,245,24]
            #Str_Send = "80 F3 01 F5 18"
            send_list = bytes(send_list)
            try:
                Serial_Port.write(send_list)  # item.encode('utf-8'))
            except Exception as e:
                pass

    def Upgrade_BMS_UARTResponse(self, Data):
        global Upgrade_Step
        global Upgrade_PackIndex
        global Upgrade_Pack_OK
        global Upgrade_Count

        if Data[1] == 'f0':  # 开始升级
            Upgrade_Count = 0
            if Data[2] == '1':  # 成功
                if Upgrade_Step == 0:
                    self.comboBox.setEnabled(False)
                    Upgrade_Step = 1
            elif Data[2] == '0':
                self.Windows_Put(1)
                Upgrade_Step = 3
        elif Data[1] == 'f1':  # 下发校验
            if len(Data)<5:
                return
            Upgrade_Count = 0
            if Data[4] == '1' and Upgrade_Step == 1:  # 成功
                Upgrade_Pack_OK = 1
                Upgrade_Step = 2
            elif Data[4] == '0':
                self.Windows_Put(2)
                Upgrade_Step = 3
        elif Data[1] == 'f2':
            if len(Data)<5:
                Upgrade_Pack_OK = 1
                return
            Upgrade_Count = 0
            if Data[4] == '1' and Upgrade_Step == 2:  # 成功
                Upgrade_Pack_OK = 1
                Upgrade_PackIndex += 1
            elif Data[4] == '2':
                Upgrade_Pack_OK = 1  # 添加重发
        elif Data[1] == 'f3':
            if len(Data)<6:
                return
            Upgrade_Count = 0
            if Data[4] == '1' and Upgrade_Step == 3:  # 成功
                Upgrade_Timer_500ms.stop()
                Upgrade_Step = 4
                self.comboBox.setEnabled(True)
                str2 = "升级成功"
                self.Windows_Print(str2)
                # str2 = "升级成功，版本号："+str(Data[4])+str(Data[5])
                # self.Windows_Print(str2)
            # elif Data[4] == 1:  # 失败
            #     self.Windows_Print("校验错误")
            #     Upgrade_Step = 4

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "升级界面"))
        Form.setWindowIcon(QIcon("..\Picture\BootWindowsTitle.jpg"))
        self.pushButton.setText(_translate("Form", "打开文件"))
        self.pushButton_2.setText(_translate("Form", "开始升级"))
        self.pushButton_3.setText(_translate("Form", "停止升级"))
        self.label_2.setText(_translate("Form", "文件名"))
        self.label_3.setText(_translate("Form", "BMS地址"))
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.comboBox.setItemText(0, _translate("Form", "0x80"))
        self.comboBox.setItemText(1, _translate("Form", "0x81"))
        self.comboBox.setItemText(2, _translate("Form", "0x82"))
        self.comboBox.setItemText(3, _translate("Form", "0x83"))
        self.comboBox.setItemText(4, _translate("Form", "0x84"))
        self.comboBox.setItemText(5, _translate("Form", "0x85"))
        self.comboBox.setItemText(6, _translate("Form", "0x86"))
        self.comboBox.setItemText(7, _translate("Form", "0x87"))
        self.comboBox.setItemText(8, _translate("Form", "0x88"))
        self.comboBox.setItemText(9, _translate("Form", "0x89"))
