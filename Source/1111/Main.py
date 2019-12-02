# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QMainWindow, QApplication,QWidget,QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from BBXX_UI import Ui_Form2
from JCCP_UI import Ui_MainWindow
from CSPZ_UI import Ui_Form
from Data import Standard_Dict,Password
import datetime
import sys

ReadBuff = []

COM_Status = 0
Send_Delay = 500
Serial_Used_Flag = 0
Clear_ModBusDict_Count = 0


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

Modbus_Dict = {
    '30001' : 'NULL',
    '30002' : 'NULL',
    '30003' : 'NULL',
    '30004' : 'NULL',
    '30005' : 'NULL',
    '30006' : 'NULL',
    '30007' : 'NULL',
    '30008' : 'NULL',
    '30009' : 'NULL',
    '30010' : 'NULL',
    '30011' : 'NULL',
    '30012' : 'NULL',
    '30013' : 'NULL',
    '30014' : 'NULL',
    '30015' : 'NULL',
    '30016' : 'NULL',
    '30017' : 'NULL',
    '30018' : 'NULL',
    '30019' : 'NULL',
    '30020' : 'NULL',
    '30021' : 'NULL',
    '30022' : 'NULL',
    '30023' : 'NULL',
    '30024' : 'NULL',
    '30025' : 'NULL',
    '30026' : 'NULL',
    '30027' : 'NULL',
    '30028' : 'NULL',
    '30029' : 'NULL',
    '30030' : 'NULL',
    '30031' : 'NULL',
    '30032' : 'NULL',
    '30033' : 'NULL',
    '30034' : 'NULL',
    '30035' : 'NULL',
    '30036' : 'NULL',
    '30037' : 'NULL',
    '30038' : 'NULL',
    '30039' : 'NULL',
    '30040' : 'NULL',#均衡
    '30041' : 'NULL',
    '30042' : 'NULL',
    '30043' : 'NULL',
    '30044' : 'NULL',
    '30045' : 'NULL',
    '30046' : 'NULL',
    '30047' :  2000,   #绝缘电阻R+
    '30048' :  2000    #绝缘电阻R-
}

COM_Dict = {
    'TOOL_Name':'NULL',
    'TOOL_Describe':'NULL',
    'TOOL_Velocity':'NULL',
    'TOOL_Channel':'NULL',
    'TOOL_SerNum':'NULL'
}

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
    def Warning(self,Flag):
        if Flag ==1 :
            QMessageBox.information(self,"错误信息","失败",QMessageBox.Yes )
        elif Flag == 0:
            QMessageBox.information(self,"错误信息","写入成功",QMessageBox.Yes)
        elif Flag == 2:
            QMessageBox.information(self,"错误信息","写入失败",QMessageBox.Yes)

class BBXX(QMainWindow, Ui_Form2):
    def __init__(self):
        super(BBXX, self).__init__()
        self.setupUi(self)

    def Open(self):
        self.show()

    def Close(self):
        self.close()

class CSPZ(QWidget, Ui_Form):
    def __init__(self):
        super(CSPZ, self).__init__()
        self.setupUi(self)

    def Open(self):
        self.show()

    def Close(self):
        self.close()


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

def HexToDec(x):
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

def DecToHex(str):
    num = hex(str)[2:]
    return num



def Message_Deal():
    if CKPZ_UI.SeralPor_OpenFlag == 1:
        try:
            num = Serial_Port.inWaiting()
        except:
            return None
        if num > 0:
            data = Serial_Port.read(num)
            num = len(data)
            global ReadBuff
            dealStr = ""
            for i in range(len(data)):
                # print(hex(data[i])[2:])
                dealStr += hex(data[i])[2:]
                dealStr += ' '
                ReadBuff.append(hex(data[i])[2:])
            dealStr.rstrip(' ')  # 删除末尾符号
            # MainWindows.Data_Show.append(str(dealStr))
            # 处理数据

            if ReadBuff[0] == '80':
                try:
                    Bootload_UI = Bootload()
                    Bootload_UI.Upgrade_BMS_UARTResponse(ReadBuff)
                except:
                    i = 0
                Serial_Port.flushInput()
                Serial_Port.flushOutput()
                ReadBuff = []
                return
            if len(ReadBuff) < 4:
                Serial_Port.flushInput()
                Serial_Port.flushOutput()
                ReadBuff = []
                return
            Num = ReadBuff[4]
            Num = HexToDec(Num)
            if Num + 7 > len(ReadBuff):
                return
            elif Num + 7 < len(ReadBuff):
                Serial_Port.flushInput()
                Serial_Port.flushOutput()
                ReadBuff = []
                return
            # if ReadBuff[0] == "47" and ReadBuff[1] == "16":# and ReadBuff[2] == "1" and ReadBuff[3] == "24" and ReadBuff[1] == "20" and :
            #     Register_Addr = 30011
            #     i = 0
            #     for i in range(int(Num / 2)):
            #         try:
            #             if len(ReadBuff[5 + i * 2]) == 1:
            #                 ReadBuff[5 + i * 2] = "0" + ReadBuff[5 + i * 2]
            #             if len(ReadBuff[6 + i * 2]) == 1:
            #                 ReadBuff[6 + i * 2] = "0" + ReadBuff[6 + i * 2]
            #             Modbus_Dict[str(Register_Addr + i)] = ReadBuff[5 + i * 2] + ReadBuff[6 + i * 2]
            #         except:
            #             MainWindows.Data_Show.append("数据无效")
            #             break
            # MainWindows = Main()
            # MainWindows.Data_S("数据无效")
            #MainWindows.Data_S(str(data))
            # return
            if ReadBuff[0] == "3":  # 首地址
                # MainWindows.Data_Show.append("OK")
                if ReadBuff[1] == "3":  # 读取保持寄存器
                    Register_Addr = ReadBuff[2] + ReadBuff[3]
                    Register_Addr = HexToDec(Register_Addr)
                    if Register_Addr >= 30300 and Register_Addr <= 30312:  # SH367309
                        for i in range(Num):
                            try:
                                if len(ReadBuff[5 + i * 2]) == 1:
                                    ReadBuff[5 + i * 2] = "0" + ReadBuff[5 + i * 2]
                                Sh367309_Register_H = ReadBuff[5 + i * 2]
                                if len(ReadBuff[6 + i * 2]) == 1:
                                    ReadBuff[6 + i * 2] = "0" + ReadBuff[6 + i * 2]
                                Sh367309_Register_L = ReadBuff[6 + i * 2]
                                item = QtWidgets.QTableWidgetItem()
                                item.setText(Sh367309_Register_H)
                                CSPZWindows.tableWidget.setItem(i * 2, 1, item)
                                item = QtWidgets.QTableWidgetItem()
                                item.setText(Sh367309_Register_L)
                                CSPZWindows.tableWidget.setItem(i * 2 + 1, 1, item)
                            except:
                                MainWindows.Data_Show.append("数据无效")
                                break
                    elif Register_Addr >= 30001 and Register_Addr <= 30039:  # 概要信息
                        i = 0
                        for i in range(int(Num / 2)):
                            try:
                                if len(ReadBuff[5 + i * 2]) == 1:
                                    ReadBuff[5 + i * 2] = "0" + ReadBuff[5 + i * 2]
                                if len(ReadBuff[6 + i * 2]) == 1:
                                    ReadBuff[6 + i * 2] = "0" + ReadBuff[6 + i * 2]
                                Modbus_Dict[str(Register_Addr + i)] = ReadBuff[5 + i * 2] + ReadBuff[6 + i * 2]
                            except:
                                MainWindows.Data_Show.append("数据无效")
                                break

                elif ReadBuff[1] == "10":  # 写入
                    # MainWindows.Warning(0)
                    i = 0  # 需要增加弹出窗口显示写入成功失败

                ReadBuff = []
        else:
            pass
    elif CANWindows_UI.CAN_OpenFlag == 1:
        CAN_Windows = USBCAN()
        Num = CAN_Windows.CAN_ReceiveData()#接收数据
        if Num < 1:
            return
        MainWindows = Main()
        BMS_ID = MainWindows.comboBox_5.currentText()
        BMS_ID = int(BMS_ID[2:3])*16 + int(BMS_ID[3:])
        BMS_ID = 0x18FF0001 + BMS_ID * 0x100
        for i in range(Num):
            if CANWindows_UI.CANBuffer[i][0] == BMS_ID:#数据读取
                if CANWindows_UI.CANBuffer[i][2] == 1:
                    Modbus_Dict["30001"] = DecToHex(CANWindows_UI.CANBuffer[i][3] * 256 + CANWindows_UI.CANBuffer[i][4])
                if CANWindows_UI.CANBuffer[i][2] == 2:
                    Modbus_Dict["30002"] = DecToHex(CANWindows_UI.CANBuffer[i][3] * 256 + CANWindows_UI.CANBuffer[i][4])
                if CANWindows_UI.CANBuffer[i][2]  == 3:
                    Modbus_Dict["30003"] = DecToHex(CANWindows_UI.CANBuffer[i][3] * 256 + CANWindows_UI.CANBuffer[i][4])
                if CANWindows_UI.CANBuffer[i][2]  == 4:
                    Modbus_Dict["30004"] = DecToHex(CANWindows_UI.CANBuffer[i][3] * 256 + CANWindows_UI.CANBuffer[i][4])
                if CANWindows_UI.CANBuffer[i][2]  == 5:
                    Modbus_Dict["30005"] = DecToHex(CANWindows_UI.CANBuffer[i][3] * 256 + CANWindows_UI.CANBuffer[i][4])
                if CANWindows_UI.CANBuffer[i][2]  == 6:
                    Modbus_Dict["30006"] = DecToHex(CANWindows_UI.CANBuffer[i][3] * 256 + CANWindows_UI.CANBuffer[i][4])
                if CANWindows_UI.CANBuffer[i][2]  == 7:
                    Modbus_Dict["30007"] = DecToHex(CANWindows_UI.CANBuffer[i][3] * 256 + CANWindows_UI.CANBuffer[i][4])
                if CANWindows_UI.CANBuffer[i][2]  == 8:
                    Modbus_Dict["30008"] = DecToHex(CANWindows_UI.CANBuffer[i][3] * 256 + CANWindows_UI.CANBuffer[i][4])
                    Modbus_Dict["30009"] = DecToHex(CANWindows_UI.CANBuffer[i][5] * 256 + CANWindows_UI.CANBuffer[i][6])
                    Modbus_Dict["30010"] = DecToHex(CANWindows_UI.CANBuffer[i][7] * 256 + CANWindows_UI.CANBuffer[i][8])
                if CANWindows_UI.CANBuffer[i][2]  == 9:
                    Num_Index = CANWindows_UI.CANBuffer[i][3]-1
                    if Num_Index <6 and Num_Index>=0:
                        Modbus_Dict[str(30011+Num_Index*3)] = DecToHex(CANWindows_UI.CANBuffer[i][4] * 256 + CANWindows_UI.CANBuffer[i][5])
                        Modbus_Dict[str(30011+Num_Index*3+1)] = DecToHex(CANWindows_UI.CANBuffer[i][6] * 256 + CANWindows_UI.CANBuffer[i][7])
                        Modbus_Dict[str(30011+Num_Index*3+2)] = DecToHex(CANWindows_UI.CANBuffer[i][8] * 256 + CANWindows_UI.CANBuffer[i][9])
                    elif Num_Index == 6:
                        Modbus_Dict[str(30011+Num_Index*3)] = DecToHex(CANWindows_UI.CANBuffer[i][4] * 256 + CANWindows_UI.CANBuffer[i][5])
                        Modbus_Dict[str(30011+Num_Index*3+1)] = DecToHex(CANWindows_UI.CANBuffer[i][6] * 256 + CANWindows_UI.CANBuffer[i][7])
                if CANWindows_UI.CANBuffer[i][2] == 10:
                    Num_Index = CANWindows_UI.CANBuffer[i][3]-1
                    if Num_Index <3 and Num_Index>=0:
                        Modbus_Dict[str(30031+Num_Index*3)] = DecToHex(CANWindows_UI.CANBuffer[i][4] * 256 + CANWindows_UI.CANBuffer[i][5])
                        Modbus_Dict[str(30031+Num_Index*3+1)] = DecToHex(CANWindows_UI.CANBuffer[i][6] * 256 + CANWindows_UI.CANBuffer[i][7])
                        Modbus_Dict[str(30031+Num_Index*3+2)] = DecToHex(CANWindows_UI.CANBuffer[i][8] * 256 + CANWindows_UI.CANBuffer[i][9])
                if CANWindows_UI.CANBuffer[i][2] == 11:
                    for k in range(6):
                        CSPZ_UI.RTC_EE[k] = CANWindows_UI.CANBuffer[i][3+k]
                    Modbus_Dict[str(30037)] = DecToHex(CANWindows_UI.CANBuffer[i][3] * 256 + CANWindows_UI.CANBuffer[i][4])
                    Modbus_Dict[str(30038)] = DecToHex(CANWindows_UI.CANBuffer[i][5] * 256 + CANWindows_UI.CANBuffer[i][6])
                    Modbus_Dict[str(30039)] = DecToHex(CANWindows_UI.CANBuffer[i][7] * 256 + CANWindows_UI.CANBuffer[i][8])
                if CANWindows_UI.CANBuffer[i][2] == 12:
                    for k in range(7):
                        Modbus_Dict[str(30040+k)] = CANWindows_UI.CANBuffer[i][k+3]
                if CANWindows_UI.CANBuffer[i][2] == 13:
                    Modbus_Dict[str(30047)] = CANWindows_UI.CANBuffer[i][3]*256+CANWindows_UI.CANBuffer[i][4]
                    Modbus_Dict[str(30048)] = CANWindows_UI.CANBuffer[i][5]*256+CANWindows_UI.CANBuffer[i][6]
            elif CANWindows_UI.CANBuffer[i][0] == BMS_ID + 1: #参数读取
                if CANWindows_UI.CANBuffer[i][2] == 1:#SH367309数据
                    #CSPZ_UI = Ui_CSPZ()
                    if CANWindows_UI.CANBuffer[i][3] == 0:
                        pass
                    elif CANWindows_UI.CANBuffer[i][3] < 5:
                        j = 0
                        for j in range(6):
                            try:
                                Sh367309_Register = hex(CANWindows_UI.CANBuffer[i][4+j])[2:]
                                if len(Sh367309_Register) == 1:
                                    Sh367309_Register = "0" + Sh367309_Register
                                Num = (CANWindows_UI.CANBuffer[i][3]-1)*6+j
                                CSPZ_UI.SH367309_EE[Num] = Sh367309_Register
                            except:
                                MainWindows.Data_Show.append("数据无效")
                                break
                    elif CANWindows_UI.CANBuffer[i][3] == 5:
                        j = 0
                        for j in range(2):
                            try:
                                Sh367309_Register = hex(CANWindows_UI.CANBuffer[i][4+j])[2:]
                                if len(Sh367309_Register) == 1:
                                    Sh367309_Register = "0" + Sh367309_Register
                                Num = (CANWindows_UI.CANBuffer[i][3]-1)*6+j
                                CSPZ_UI.SH367309_EE[Num] = Sh367309_Register
                                #CSPZWindows = CSPZ()
                                #CSPZWindows.Set_Talbe(Sh367309_Register , Num , 0 )
                            except:
                                MainWindows.Data_Show.append("数据无效")
                                break
                elif CANWindows_UI.CANBuffer[i][2] == 2:#模块参数
                    global Module_ParameterBuffer
                    if CANWindows_UI.CANBuffer[i][3] == 1:
                        for j in range(4):
                            Module_ParameterBuffer[j] = CANWindows_UI.CANBuffer[4+j][i]
                    if CANWindows_UI.CANBuffer[i][3] == 2:
                        for j in range(6):
                            Module_ParameterBuffer[4+j] = CANWindows_UI.CANBuffer[4+j][i]
                    if CANWindows_UI.CANBuffer[i][3] == 3:
                        for j in range(6):
                            Module_ParameterBuffer[10+j] = CANWindows_UI.CANBuffer[4+j][i]
                    if CANWindows_UI.CANBuffer[i][3] == 4:
                        for j in range(6):
                            Module_ParameterBuffer[16+j] = CANWindows_UI.CANBuffer[4+j][i]
                    if CANWindows_UI.CANBuffer[i][3] == 5:
                        for j in range(2):
                            Module_ParameterBuffer[22+j] = CANWindows_UI.CANBuffer[4+j][i]
                    pass
            elif CANWindows_UI.CANBuffer[i][0] == BMS_ID + 2: #参数设置
                CSPZWindows = CSPZ()
                if CANWindows_UI.CANBuffer[i][2] == 1:
                    if CANWindows_UI.CANBuffer[i][3] == 0:
                        CSPZWindows.Windows_Put(1)
                    elif CANWindows_UI.CANBuffer[i][3] == 1:
                        CSPZWindows.Windows_Put(2)
                if CANWindows_UI.CANBuffer[i][2] == 2:
                    if CANWindows_UI.CANBuffer[i][3] == 0:
                        CSPZWindows.Windows_Put(3)
                    elif CANWindows_UI.CANBuffer[i][3] == 1:
                        CSPZWindows.Windows_Put(4)
            elif CANWindows_UI.CANBuffer[i][0] == BMS_ID + 3: #履历读取
                pass
            elif (CANWindows_UI.CANBuffer[i][0] >= BMS_ID + 0xEF) & (CANWindows_UI.CANBuffer[i][0] <= BMS_ID + 0xF3): #Boot升级
                Bootload_UI = Bootload()
                Bootload_UI.Upgrade_BMS_CANResponse(CANWindows_UI.CANBuffer,i)
            else:
                pass


def MainWindows_Data_Show():
    # 电压显示
    Voltage_Register_Addr = 30011
    EQUI_Register_Addr = 30040
    Start_Register_Addr2 = "30018"
    Start_Register_Addr3 = "30025"
    for i in range(20):
        if Modbus_Dict[str(Voltage_Register_Addr+i)] == "NULL":
            Voltage_N = Modbus_Dict[str(Voltage_Register_Addr+i)]
        else:
            Voltage_N = HexToDec(Modbus_Dict[str(Voltage_Register_Addr+i)])
        item = QtWidgets.QTableWidgetItem()
        Data = str(Voltage_N)
        item.setText(Data)
        if Modbus_Dict[str(EQUI_Register_Addr+i//4)] == "NULL":
            EQUI_N = 00
        else:
            EQUI_N = HexToDec(Modbus_Dict[str(EQUI_Register_Addr+i//4)])
        Index = i%4*2
        if (EQUI_N>>Index) & 0x01:
            item.setBackground(QColor(255,255,0))#Yellow
        else:
            item.setBackground(QColor(255,255,255))#White
        MainWindows.tableWidget.setItem(i//7*2+1, i%7+1, item)
    # for i in range(1, 8):
    #     if Modbus_Dict[str(Start_Register_Addr1)] == "NULL":
    #         Voltage_N = Modbus_Dict[str(Start_Register_Addr1)]
    #     else:
    #         Voltage_N = HexToDec(Modbus_Dict[str(Start_Register_Addr1)])
    #     item = QtWidgets.QTableWidgetItem()
    #     Data = str(Voltage_N)
    #     item.setText(Data)
    #     MainWindows.tableWidget.setItem(1, i, item)
    #     Start_Register_Addr1 = int(Start_Register_Addr1)
    #     Start_Register_Addr1 = Start_Register_Addr1 + 1
    #
    #     if Modbus_Dict[str(Start_Register_Addr2)] == "NULL":
    #         Voltage_N = Modbus_Dict[str(Start_Register_Addr2)]
    #     else:
    #         Voltage_N = HexToDec(Modbus_Dict[str(Start_Register_Addr2)])
    #     item = QtWidgets.QTableWidgetItem()
    #     Data = str(Voltage_N)
    #     item.setText(Data)
    #     MainWindows.tableWidget.setItem(3, i, item)
    #     Start_Register_Addr2 = int(Start_Register_Addr2)
    #     Start_Register_Addr2 = Start_Register_Addr2 + 1
    #
    #     if Modbus_Dict[str(Start_Register_Addr3)] == "NULL":
    #         Voltage_N = Modbus_Dict[str(Start_Register_Addr3)]
    #     else:
    #         Voltage_N = HexToDec(Modbus_Dict[str(Start_Register_Addr3)])
    #     if i < 7:
    #         item = QtWidgets.QTableWidgetItem()
    #         Data = str(Voltage_N)
    #         item.setText(Data)
    #         MainWindows.tableWidget.setItem(5, i, item)
    #     Start_Register_Addr3 = int(Start_Register_Addr3)
    #     Start_Register_Addr3 = Start_Register_Addr3rt_Register_Addr3 + 1
    # 温度显示
    Start_Register_Addr = "30031"
    for i in range(1, 7):
        if Modbus_Dict[str(Start_Register_Addr)] == "NULL":
            Voltage_N = Modbus_Dict[str(Start_Register_Addr)]
            item = QtWidgets.QTableWidgetItem()
            Data = str(Voltage_N)
            item.setText(Data)
            MainWindows.tableWidget.setItem(7, i, item)
        else:
            Voltage_N = HexToDec(Modbus_Dict[str(Start_Register_Addr)])
            Voltage_N = (Voltage_N - 400)/10
            item = QtWidgets.QTableWidgetItem()
            Data = str(Voltage_N)
            item.setText(Data)
            MainWindows.tableWidget.setItem(7, i, item)
        Start_Register_Addr = int(Start_Register_Addr)
        Start_Register_Addr = Start_Register_Addr + 1
    # rtc显示
    Start_Register_Addr = "30037"
    Time = ""
    for i in range(0, 3):
        if Modbus_Dict[str(Start_Register_Addr)] == "NULL":
            Time = "2000-01-01 01:01:02"
            MainWindows.dateTimeEdit.setDate(QtCore.QDate(2008, 1, 1))  # 设置日期
            MainWindows.dateTimeEdit.setTime(QtCore.QTime(1, 1, 20))  # 设置时间11:00
            break
        else:
            if i == 2:
                Voltage_N = HexToDec(Modbus_Dict[str("30037")])
                Year = Voltage_N // 256 + 2000
                Mouth = Voltage_N % 256
                Voltage_N = HexToDec(Modbus_Dict[str("30038")])
                Day = Voltage_N // 256
                Hour = Voltage_N % 256
                Voltage_N = HexToDec(Modbus_Dict[str("30039")])
                Min = Voltage_N // 256
                Sec = Voltage_N % 256
                try:
                    MainWindows.dateTimeEdit.setDate(QtCore.QDate(Year, Mouth, Day))  # 设置日期
                    MainWindows.dateTimeEdit.setTime(QtCore.QTime(Hour, Min, Sec))  # 设置时间11:00
                except:
                    pass
        Start_Register_Addr = int(Start_Register_Addr)
        Start_Register_Addr = Start_Register_Addr + 1
    #MainWindows.dateTimeEdit.setDate(QtCore.QDate(2008, 1, 1))  # 设置日期
    #MainWindows.dateTimeEdit.setTime(QtCore.QTime(1, 1, 20))  # 设置时间11:00

    # MainWindows.dateTimeEdit.setDisplayFormat(Time)
    # 组端电压
    Start_Register_Addr = "30001"
    if Modbus_Dict[str(Start_Register_Addr)] == "NULL":
        Voltage_N = Modbus_Dict[str(Start_Register_Addr)]
    else:
        Voltage_N = HexToDec(Modbus_Dict[str(Start_Register_Addr)]) * 10
    MainWindows.lineEdit.setText(str(Voltage_N))
    # 组端电流
    Start_Register_Addr = "30002"
    if Modbus_Dict[str(Start_Register_Addr)] == "NULL":
        Current = Modbus_Dict[str(Start_Register_Addr)]
        Data = str(Current)
    else:
        Current = HexToDec(Modbus_Dict[str(Start_Register_Addr)])
        if Current > 32768:
            Current = Current - 65536
            Data = str(Current) + "0"
        else:
            Data = str(Current) + "0"
    MainWindows.lineEdit_2.setText(str(Data))
    # SOC
    Start_Register_Addr = "30003"
    if Modbus_Dict[str(Start_Register_Addr)] == "NULL":
        Register_Data = Modbus_Dict[str(Start_Register_Addr)]
    else:
        Register_Data = HexToDec(Modbus_Dict[str(Start_Register_Addr)])
    MainWindows.lineEdit_3.setText(str(Register_Data))
    # 剩余容量
    Start_Register_Addr = "30004"
    if Modbus_Dict[str(Start_Register_Addr)] == "NULL":
        Register_Data = Modbus_Dict[str(Start_Register_Addr)]
    else:
        Register_Data = HexToDec(Modbus_Dict[str(Start_Register_Addr)])
    MainWindows.lineEdit_4.setText(str(Register_Data))
    # 满充容量
    Start_Register_Addr = "30005"
    if Modbus_Dict[str(Start_Register_Addr)] == "NULL":
        Register_Data = Modbus_Dict[str(Start_Register_Addr)]
    else:
        Register_Data = HexToDec(Modbus_Dict[str(Start_Register_Addr)])
    MainWindows.lineEdit_5.setText(str(Register_Data))
    # 循环次数
    Start_Register_Addr = "30007"
    if Modbus_Dict[str(Start_Register_Addr)] == "NULL":
        Register_Data = Modbus_Dict[str(Start_Register_Addr)]
    else:
        Register_Data = HexToDec(Modbus_Dict[str(Start_Register_Addr)])
    MainWindows.lineEdit_6.setText(str(Register_Data))
    # 设计容量
    Start_Register_Addr = "30006"
    if Modbus_Dict[str(Start_Register_Addr)] == "NULL":
        Register_Data = Modbus_Dict[str(Start_Register_Addr)]
    else:
        Register_Data = HexToDec(Modbus_Dict[str(Start_Register_Addr)])
    MainWindows.lineEdit_7.setText(str(Register_Data))
    #MOS状态
    Start_Register_Addr = "30010"
    if Modbus_Dict[str(Start_Register_Addr)] == "NULL":
        MainWindows.checkBox_2.setCheckState(False)
        MainWindows.checkBox_3.setCheckState(False)
    else:
        Register_Data = HexToDec(Modbus_Dict[str(Start_Register_Addr)])
        Register_Data = bin(Register_Data)
        Register_Data = "0"*(18-len(Register_Data))+Register_Data[2:]
        # Register_Data2 = ""
        # for i in range(16):
        #     Register_Data2 += Register_Data[15-i]
        # MainWindows.Data_Show.append(Register_Data2)
        # MainWindows.Data_Show.append(Register_Data2[14:])
        # MainWindows.Data_Show.append(Register_Data2[12:14])
        # MainWindows.Data_Show.append(Register_Data)#0x5A [低位]0B(0)1011010[高位]
        # if Register_Data[]
        if Register_Data[:2] == "01":
            MainWindows.checkBox_3.setCheckState(True)
        else:
            MainWindows.checkBox_3.setCheckState(False)

        if Register_Data[2:4] == "01":
            MainWindows.checkBox_2.setCheckState(True)
        else:
            MainWindows.checkBox_2.setCheckState(False)

        if Register_Data[4:6] == "01":
            MainWindows.checkBox_4.setCheckState(True)
        else:
            MainWindows.checkBox_4.setCheckState(False)
#绝缘电阻
    Start_Register_Addr = "30047"
    if Modbus_Dict[str(Start_Register_Addr)] == "NULL":
        i = 0
        Register_Data = "NULL"
    else:
        Register_Data = (Modbus_Dict[str(Start_Register_Addr)])
    MainWindows.lineEdit_8.setText(str(Register_Data))
    Start_Register_Addr = "30048"
    if Modbus_Dict[str(Start_Register_Addr)] == "NULL":
        i = 0
        Register_Data = "NULL"
    else:
        Register_Data = (Modbus_Dict[str(Start_Register_Addr)])
    MainWindows.lineEdit_9.setText(str(Register_Data))

    #告警
    Start_Register_Addr = "30008"
    Alarm_Time = datetime.datetime.now().strftime('%H:%M:%S')
    if Modbus_Dict[str(Start_Register_Addr)] == "NULL":
        MainWindows.checkBox_2.setCheckState(False)
        MainWindows.checkBox_3.setCheckState(False)
    else:
        Register_Data = HexToDec(Modbus_Dict[str(Start_Register_Addr)])
        Register_Data = bin(Register_Data)
        Register_Data = "0" * (18 - len(Register_Data)) + Register_Data[2:]
        if Register_Data[10:12] == "10":
            if Alarm_Flag[10] == 0:
                Alarm_Flag[10] = 1
                Append_Str = str(Alarm_Time) + ":" + "采集前端通讯异常"
                MainWindows.Data_Show.append(Append_Str)
        elif Register_Data[10:12] == "00":
            if Alarm_Flag[10] == 1:
                Alarm_Flag[10] = 0
                Append_Str = str(Alarm_Time) + ":" + "采集前端通讯异常恢复"
                MainWindows.Data_Show.append(Append_Str)

        if Register_Data[12:14] == "10":
            if Alarm_Flag[9] == 0:
                Alarm_Flag[9] = 1
                Append_Str = str(Alarm_Time) + ":" + "单体电池过压"
                MainWindows.Data_Show.append(Append_Str)
        elif Register_Data[12:14] == "00":
            if Alarm_Flag[9] == 1:
                Alarm_Flag[9] = 0
                Append_Str = str(Alarm_Time) + ":" + "单体电池过压恢复"
                MainWindows.Data_Show.append(Append_Str)
        if Register_Data[14:] == "10":
            if Alarm_Flag[8] == 0:
                Alarm_Flag[8] = 1
                Append_Str = str(Alarm_Time) + ":" + "单体电池欠压"
                MainWindows.Data_Show.append(Append_Str)
        elif Register_Data[14:] == "00":
            if Alarm_Flag[8] == 1:
                Alarm_Flag[8] = 0
                Append_Str = str(Alarm_Time) + ":" + "单体电池欠压恢复"
                MainWindows.Data_Show.append(Append_Str)
    Start_Register_Addr = "30009"
    if Modbus_Dict[str(Start_Register_Addr)] == "NULL":
        i= 0
        # MainWindows.checkBox_2.setCheckState(False)
        # MainWindows.checkBox_3.setCheckState(False)
    else:
        Register_Data = HexToDec(Modbus_Dict[str(Start_Register_Addr)])
        Register_Data = bin(Register_Data)
        Register_Data = "0" * (18 - len(Register_Data)) + Register_Data[2:]
        Register_Data = Register_Data[::-1]
        if Register_Data[14:] == "10":
            if Alarm_Flag[7] == 0:
                Alarm_Flag[7] = 1
                Append_Str = str(Alarm_Time) + ":" + "充电温度过高"
                MainWindows.Data_Show.append(Append_Str)
        elif Register_Data[14:] == "00":
            if Alarm_Flag[7] == 1:
                Alarm_Flag[7] = 0
                Append_Str = str(Alarm_Time) + ":" + "充电温度过高恢复"
                MainWindows.Data_Show.append(Append_Str)
        if Register_Data[12:14] == "10":
            if Alarm_Flag[6] == 0:
                Alarm_Flag[6] = 1
                Append_Str = str(Alarm_Time) + ":" + "充电温度过低"
                MainWindows.Data_Show.append(Append_Str)
        elif Register_Data[12:14] == "00":
            if Alarm_Flag[6] == 1:
                Alarm_Flag[6] = 0
                Append_Str = str(Alarm_Time) + ":" + "充电温度过低恢复"
                MainWindows.Data_Show.append(Append_Str)
        if Register_Data[10:12] == "10":
            if Alarm_Flag[5] == 0:
                Alarm_Flag[5] = 1
                Append_Str = str(Alarm_Time) + ":" + "放电温度过高"
                MainWindows.Data_Show.append(Append_Str)
        elif Register_Data[10:12] == "00":
            if Alarm_Flag[5] == 1:
                Alarm_Flag[5] = 0
                Append_Str = str(Alarm_Time) + ":" + "放电温度过高恢复"
                MainWindows.Data_Show.append(Append_Str)
        if Register_Data[8:10] == "10":
            if Alarm_Flag[4] == 0:
                Alarm_Flag[4] = 1
                Append_Str = str(Alarm_Time) + ":" + "放电温度过低"
                MainWindows.Data_Show.append(Append_Str)
        elif Register_Data[8:10] == "00":
            if Alarm_Flag[4] == 1:
                Alarm_Flag[4] = 0
                Append_Str = str(Alarm_Time) + ":" + "放电温度过低恢复"
                MainWindows.Data_Show.append(Append_Str)
        if Register_Data[6:8] == "10":
            if Alarm_Flag[3] == 0:
                Alarm_Flag[3] = 1
                Append_Str = str(Alarm_Time) + ":" + "充电电流过大"
                MainWindows.Data_Show.append(Append_Str)
        elif Register_Data[6:8] == "00":
            if Alarm_Flag[3] == 1:
                Alarm_Flag[3] = 0
                Append_Str = str(Alarm_Time) + ":" + "充电电流过大恢复"
                MainWindows.Data_Show.append(Append_Str)
        if Register_Data[4:6] == "10":
            if Alarm_Flag[2] == 0:
                Alarm_Flag[2] = 1
                Append_Str = str(Alarm_Time) + ":" + "放电电流过大1级"
                MainWindows.Data_Show.append(Append_Str)
        elif Register_Data[4:6] == "00":
            if Alarm_Flag[2] == 1:
                Alarm_Flag[2] = 0
                Append_Str = str(Alarm_Time) + ":" + "放电电流过大1级恢复"
                MainWindows.Data_Show.append(Append_Str)
        if Register_Data[2:4] == "10":
            if Alarm_Flag[1] == 0:
                Alarm_Flag[1] = 1
                Append_Str = str(Alarm_Time) + ":" + "放电电流过大2级"
                MainWindows.Data_Show.append(Append_Str)
        elif Register_Data[2:4] == "00":
            if Alarm_Flag[1] == 1:
                Alarm_Flag[1] = 0
                Append_Str = str(Alarm_Time) + ":" + "放电电流过大2级恢复"
                MainWindows.Data_Show.append(Append_Str)
        if Register_Data[0:2] == "10":
            if Alarm_Flag[0] == 0:
                Alarm_Flag[0] = 1
                Append_Str = str(Alarm_Time) + ":" + "短路"
                MainWindows.Data_Show.append(Append_Str)
        elif Register_Data[0:2] == "00":
            if Alarm_Flag[0] == 1:
                Alarm_Flag[0] = 0
                Append_Str = str(Alarm_Time) + ":" + "短路恢复"
                MainWindows.Data_Show.append(Append_Str)


def Timer_500ms_Deal():
    if Serial_Port.isOpen():
        MainWindows_Data_Show()


if __name__ == "__main__":
    COM_Status = 0
    app = QApplication(sys.argv)
    MainWindows = Main()
    CSPZWindows = CSPZ()
    BBXXWindows = BBXX()

    MainWindows.show()
    MainWindows.action_CSSZ.triggered.connect(CSPZWindows.Open)

    sys.exit(app.exec_())
