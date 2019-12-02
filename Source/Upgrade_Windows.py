# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Upgrade_Windows.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


import threading
import sys
import os
import struct
import time
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMessageBox,QFileDialog
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, QTimer,QDateTime

#TCP模块的import
import socket
import struct
import time

#CAN模块的import
from ctypes import *

#Port模块的import

import serial
import serial.tools.list_ports
from  PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo


Communication_Information = ''
Communication_Index = 0
UpgradeModule_List = [0 for i in range(20)]
Upgrade_RepeatList =  [0 for i in range(20)]
UpgradeModule_SendFileIndexList = [0 for i in range(20)]
Upgrade_Struct_Dict = {
    'Upgrade_Step' : 0,#升级步骤
    'Start_Flag' : 0,#开始标志
    'Step_Count' : 0,#升级计时
    'UpgradeFile_Size' : 0,#文件大小
    'UpgradePack_Num' : 0,#总包数
    'UpgradeFile_Index' : 1,#第几包
    'UpgradeFile_PaintIndx':1,#每包里面的帧数 计数
    '重发计次':0,
    'CRC校验' : 0,#文件CRC校验
    'BMS_BaseID':0x80,#初始ID，用来分主控从控
    'Upgrade_Num':1,#1:单个升级;2:全部升级
    '升级状态':'无'
}
Upgrade_File = [0 for i in range(128000)]    #96K缓存

#TCP/IP升级相关的变量
TCP_RunTimer = QTimer()
socket.setdefaulttimeout(0.1)
tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPMOBUS_PDT_Header = [0x55,0xAA,0x00,0x01,0x00,0x06]

#CAN的数据
CAN_RunTimer = QTimer()
CANDeviceNameNumber = 3
CANDeviceIndexNumber = 0
CANDeviceChannelNumber = 0
CANDeviceBoundRate = 0x011C
CANBuffer = [[0 for x in range(10)] for y in range(50)]#50帧的数据缓存

class _VCI_INIT_CONFIG(Structure):
    _fields_ = [('AccCode', c_ulong),
                ('AccMask', c_ulong),
                ('Reserved', c_ulong),
                ('Filter', c_ubyte),
                ('Timing0', c_ubyte),
                ('Timing1', c_ubyte),
                ('Mode', c_ubyte)]

class _VCI_CAN_OBJ(Structure):
    _fields_ = [('ID', c_uint),
                ('TimeStamp', c_uint),
                ('TimeFlag', c_byte),
                ('SendType', c_byte),
                ('RemoteFlag', c_byte),
                ('ExternFlag', c_byte),
                ('DataLen', c_byte),
                ('Data', c_byte * 8),
                ('Reserved', c_byte * 3)]

#Port的数据
Port_RunTimer = QTimer()
Port = QSerialPort()
Serial_Port = serial.Serial()

###################################################################

def crc16(x, Start_Num,length):
    Crc_Reg = 0xFFFF
    temp = 0 & 0xFFFF
    for i in range(length):
        # Data = x[:2]
        # x = x[2:].strip()
        # byte = self.HexToDec(Data)
        byte = x[i+Start_Num]
        Crc_Reg ^= byte
        for i in range(8):
            if Crc_Reg & 0x0001 == 1:
                Crc_Reg >>= 1
                Crc_Reg ^= 0xA001  # 0xA001是0x8005循环右移16位的值
            else:
                Crc_Reg >>= 1

    return Crc_Reg  # hex(Crc_Reg)

def Gloabl_CAN_Init():
    global CANDeviceNameNumber
    global CANDeviceIndexNumber
    global CANDeviceChannelNumber
    global Communication_Information
    global Communication_Index
    global CANDeviceBoundRate

    vic = _VCI_INIT_CONFIG()
    vic.AccCode = 0x00000000
    vic.AccMask = 0xffffffff
    vic.Filter = 0
    vic.Timing0 = CANDeviceBoundRate//256
    vic.Timing1 = CANDeviceBoundRate%256
    vic.Mode = 0

    canLib = windll.LoadLibrary('.\DLL\ControlCAN.dll')
    returnFlag = canLib.VCI_OpenDevice(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber)
    if returnFlag == -1:
        return -1#returnFlag
    returnFlag = canLib.VCI_InitCAN(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber, pointer(vic))
    if returnFlag == -1:
        return -2#returnFlag
    returnFlag = canLib.VCI_StartCAN(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber)
    if returnFlag == -1:
        return -3#returnFlag
    return 1

def Gloabl_CAN_Close():
    global CANDeviceNameNumber
    global CANDeviceIndexNumber
    global CANDeviceChannelNumber
    global CANDeviceBoundRate

    canLib = windll.LoadLibrary('.\DLL\ControlCAN.dll')
    canLib.VCI_CloseDevice(CANDeviceNameNumber, CANDeviceIndexNumber)


#############################数据升级类###################################
class StoppableThread(threading.Thread):
    def __init__(self, daemon=None):
        super(StoppableThread, self).__init__(daemon=daemon)
        self.CommIndex_CANUART = 0
        self.__is_running = True
        self.daemon = daemon
    def terminate(self):
        self.__is_running = False
    def run(self):
        global Upgrade_Struct_Dict
        global Upgrade_File
        global UpgradeModule_List

        self.Time_Delay = 0.5
        Gloabl_CAN_Init()#因为不同CLASS，在这个线程中需要初始化CAN
        while self.__is_running:
            if self.CommIndex_CANUART == 0:#无初始化
                self.__is_running = False
            elif self.CommIndex_CANUART == 1:#CAN升级
                self.__is_running = self.CAN_Upgrade()
            elif self.CommIndex_CANUART == 2:#UART升级
                self.__is_running = self.Port_Upgrade()
            time.sleep(self.Time_Delay)
            self.CAN_ReceiveBMS()

        Upgrade_Struct_Dict['Upgrade_Step'] = 99
        Gloabl_CAN_Close()
#################################CAN升级#################################
    def CAN_Upgrade(self):
        global Upgrade_Struct_Dict
        global Upgrade_File
        global UpgradeModule_List
        global UpgradeModule_SendFileIndexList
        global Upgrade_RepeatList

        Return_Result = True

        if Upgrade_Struct_Dict['Upgrade_Num'] == 1:#单个升级
            for UpgradeIndex in range(20):#一个一个升级
                if UpgradeModule_List[UpgradeIndex] == 1:#复位模块
                    self.Time_Delay = 0.5#500ms运行一次
                    self.CAN_ResetBMS(UpgradeIndex+Upgrade_Struct_Dict['BMS_BaseID'])
                    Upgrade_Struct_Dict['Step_Count'] +=1
                    if Upgrade_Struct_Dict['Step_Count'] > 5/self.Time_Delay:#5S没有回复
                        UpgradeModule_List[UpgradeIndex] = 99
                        Upgrade_Struct_Dict['Step_Count'] = 0
                        Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(UpgradeIndex+1) + \
                                                      '号模块复位失败....\n'
                    break
                elif UpgradeModule_List[UpgradeIndex] == 2:#发送校验
                    self.Time_Delay = 0.5#500ms运行一次
                    self.CAN_SendCI(UpgradeIndex+Upgrade_Struct_Dict['BMS_BaseID'])
                    Upgrade_Struct_Dict['Step_Count'] +=1
                    if Upgrade_Struct_Dict['Step_Count'] > 5/self.Time_Delay:#5S没有回复
                        UpgradeModule_List[UpgradeIndex] = 99
                        Upgrade_Struct_Dict['Step_Count'] = 0
                    break
                elif UpgradeModule_List[UpgradeIndex] == 3:#发送数据
                    self.Time_Delay = 0.01#5ms运行一次
                    self.CAN_SendFile(UpgradeIndex+Upgrade_Struct_Dict['BMS_BaseID'])
                    Upgrade_Struct_Dict['Step_Count'] +=1
                    if Upgrade_Struct_Dict['Step_Count'] > 5/self.Time_Delay:#5S没有回复
                        Upgrade_Struct_Dict['重发计次'] = Upgrade_Struct_Dict['重发计次'] + 1
                        if Upgrade_Struct_Dict['重发计次'] > 3:#最大重发三次
                            UpgradeModule_List[UpgradeIndex] = 99
                            Upgrade_Struct_Dict['Step_Count'] = 0
                            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + \
                                                          '第'+str(Upgrade_Struct_Dict['UpgradeFile_Index']+1)+'包没有回复....\n'
                            Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] = 0
                            Upgrade_Struct_Dict['UpgradeFile_Index'] = 0
                        else:
                            Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] = 0
                            Upgrade_Struct_Dict['UpgradeFile_Index'] = Upgrade_Struct_Dict['UpgradeFile_Index']
                            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] +  \
                                                          '第'+str(Upgrade_Struct_Dict['UpgradeFile_Index']+1)+'包重发....\n'
                            Upgrade_Struct_Dict['Step_Count'] = 0
                    break
                elif UpgradeModule_List[UpgradeIndex] == 4:#升级结束
                    self.Time_Delay = 0.5#500ms运行一次
                    self.CAN_StopUpgrade(UpgradeIndex+Upgrade_Struct_Dict['BMS_BaseID'])
                    Upgrade_Struct_Dict['Step_Count'] +=1
                    if Upgrade_Struct_Dict['Step_Count'] > 5/self.Time_Delay:#5S没有回复
                        UpgradeModule_List[UpgradeIndex] = 99
                        Upgrade_Struct_Dict['Step_Count'] = 0
                        Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(UpgradeIndex+1) + \
                                                      '号模块进入APP失败....\n'
                    break
        elif Upgrade_Struct_Dict['Upgrade_Num'] == 2:#全部升级
            temp_Min = 99
            for UpgradeIndex in range(20):#获取最慢的模块状态
                if UpgradeModule_List[UpgradeIndex] > 0 and UpgradeModule_List[UpgradeIndex] < temp_Min:
                    temp_Min = UpgradeModule_List[UpgradeIndex]
            if temp_Min == 1:#复位模块
                self.Time_Delay = 0.5  # 500ms运行一次
                self.CAN_ResetBMS(0xFF)
            elif temp_Min == 2:#校验信息
                self.Time_Delay = 0.5  # 500ms运行一次
                self.CAN_SendCI(0xFF)
            elif temp_Min == 3:#文件
                self.Time_Delay = 0.015  # 10ms运行一次
                temp = False
                for i in range(20):
                    #处于发文件的状态,返回的状态为不成功或者没有返回
                    if UpgradeModule_List[i] == 3 and UpgradeModule_SendFileIndexList[i] != (Upgrade_Struct_Dict['UpgradeFile_Index']+1):
                        if Upgrade_Struct_Dict['重发计次'] > 3:
                            UpgradeModule_List[i] == 99#设置为失败
                        else:
                            temp = True
                temp2 = 0
                if temp:
                    #延时
                    Upgrade_Struct_Dict['Step_Count'] += 1
                    if Upgrade_Struct_Dict['Step_Count'] > 5 / self.Time_Delay:  # 5S没有回复
                        #重发机制
                        Upgrade_Struct_Dict['重发计次'] = Upgrade_Struct_Dict['重发计次'] + 1
                        Upgrade_Struct_Dict['Step_Count'] = 0
                        Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + \
                                                      '第'+str(Upgrade_Struct_Dict['UpgradeFile_Index']+1)+'包重发....\n'
                else:
                    Upgrade_Struct_Dict['UpgradeFile_Index'] = Upgrade_Struct_Dict['UpgradeFile_Index'] + 1
                    self.CAN_SendFile(0xFF)
            elif temp_Min == 4:#结束
                self.Time_Delay = 0.01  # 10ms运行一次
                self.CAN_StopUpgrade(0xFF)
            elif temp_Min == 5:#成功
                i = 0
            Upgrade_Struct_Dict['Step_Count'] += 1
            if Upgrade_Struct_Dict['Step_Count'] > 5 / self.Time_Delay:  # 5S没有回复
                for UpgradeIndex in range(20):#时间到，最慢的模块转为99，升级失败
                    if UpgradeModule_List[UpgradeIndex] == temp_Min:
                        UpgradeModule_List[UpgradeIndex] = 99
                Upgrade_Struct_Dict['Step_Count'] = 0

        Return_Result = False
        for i in range(20):#任何一个模块在升级步骤中，线程继续
            if UpgradeModule_List[i] < 5 and UpgradeModule_List[i] > 0:
                Return_Result = True
        return Return_Result

    # 复位模块
    def CAN_ResetBMS(self, BMS_Index):
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global CANDeviceChannelNumber
        vco = _VCI_CAN_OBJ()
        vco.ID = 0x18F000FF + BMS_Index * 0x100
        vco.SendType = 0
        vco.RemoteFlag = 0
        vco.ExternFlag = 1
        vco.DataLen = 8
        vco.Data = (1, 0, 0, 0, 0, 0, 0, 0)
        canLib = windll.LoadLibrary('.\DLL\ControlCAN.dll')
        ReturnFlag = canLib.VCI_Transmit(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber,pointer(vco), 1)
        print(ReturnFlag)
        return ReturnFlag

    #CAN发送检验信息
    def CAN_SendCI(self, BMS_Index):
        global Upgrade_Struct_Dict

        canLib = windll.LoadLibrary('.\DLL\ControlCAN.dll')
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global CANDeviceChannelNumber

        File_ByteNum_HH = Upgrade_Struct_Dict['UpgradeFile_Size'] // 65535
        File_ByteNum_H = Upgrade_Struct_Dict['UpgradeFile_Size'] % 65535 // 256
        File_ByteNum_L = Upgrade_Struct_Dict['UpgradeFile_Size'] % 256
        File_CRC_H = Upgrade_Struct_Dict['CRC校验'] // 256
        File_CRC_L = Upgrade_Struct_Dict['CRC校验'] % 256
        File_PackNum_L = Upgrade_Struct_Dict['UpgradePack_Num']

        vco = _VCI_CAN_OBJ()
        vco.ID = 0x18F100FF + BMS_Index * 0x100
        vco.SendType = 0
        vco.RemoteFlag = 0
        vco.ExternFlag = 1
        vco.DataLen = 8
        vco.Data = (1, 0, 0, 0, 0, 0, 0, 0)
        ReturnFlag = canLib.VCI_Transmit(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber,
                                         pointer(vco), 1)
        time.sleep(0.01)
        vco.Data = (1, 1, 0, 0, 0, 0, 0, 0)
        ReturnFlag = canLib.VCI_Transmit(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber,
                                         pointer(vco), 1)
        time.sleep(0.01)
        vco.Data = (0x01, 0x02, File_ByteNum_HH, File_ByteNum_H, File_ByteNum_L, File_PackNum_L, File_CRC_H, File_CRC_L)
        ReturnFlag = canLib.VCI_Transmit(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber,
                                         pointer(vco), 1)
        time.sleep(0.01)
        vco.Data = (0x01, 0xFF, 0, 0, 0, 0, 0, 0)
        ReturnFlag = canLib.VCI_Transmit(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber,
                                         pointer(vco), 1)
        time.sleep(0.01)

    #CAN发送升级文件
    def CAN_SendFile(self,BMS_Index):
        global Upgrade_Struct_Dict
        global Upgrade_File
        canLib = windll.LoadLibrary('.\DLL\ControlCAN.dll')
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global CANDeviceChannelNumber

        vco = _VCI_CAN_OBJ()
        vco.ID = 0x18F200FF + BMS_Index * 0x100
        vco.SendType = 0
        vco.RemoteFlag = 0
        vco.ExternFlag = 1
        vco.DataLen = 8
        Data = (Upgrade_Struct_Dict['UpgradeFile_Index'], Upgrade_Struct_Dict['UpgradeFile_PaintIndx'])
        # vco.Data = (Upgrade_Struct_Dict['UpgradeFile_Index'], Upgrade_Struct_Dict['UpgradeFile_PaintIndx'])
        if Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] < 170 :#1~1020个字节数据
            for i in range(6):
                temp = Upgrade_File[1024*Upgrade_Struct_Dict['UpgradeFile_Index']+Upgrade_Struct_Dict['UpgradeFile_PaintIndx']*6+i]
                Data = Data +(temp,)
            vco.Data = Data
            Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] = Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] + 1
            ReturnFlag = canLib.VCI_Transmit(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber,pointer(vco), 1)
        elif Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] == 170:  #最后的数据，最后会带2个字节CRC校验
            for i in range(4):
                temp = Upgrade_File[1024*Upgrade_Struct_Dict['UpgradeFile_Index']+Upgrade_Struct_Dict['UpgradeFile_PaintIndx']*6+i]
                Data = Data +(temp,)
            temp_crc = crc16(Upgrade_File,1024*Upgrade_Struct_Dict['UpgradeFile_Index'],1024)
            Data = Data +(temp_crc//256,)
            Data = Data +(temp_crc%256,)
            vco.Data = Data
            Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] = Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] + 1
            ReturnFlag = canLib.VCI_Transmit(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber,pointer(vco), 1)
        elif Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] < 175:
            for i in range(4):
                temp = Upgrade_File[1024*Upgrade_Struct_Dict['UpgradeFile_Index']+170*6+i]
                Data = Data +(temp,)
            temp_crc = crc16(Upgrade_File,1024*Upgrade_Struct_Dict['UpgradeFile_Index'],1024)
            Data = Data +(temp_crc//256,)
            Data = Data +(temp_crc%256,)
            vco.Data = Data
            Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] = Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] + 1
            ReturnFlag = canLib.VCI_Transmit(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber,pointer(vco), 1)
        else:
            i = 0#无动作

    #CAN发送升级结束
    def CAN_StopUpgrade(self, BMS_Index):
        canLib = windll.LoadLibrary('.\DLL\ControlCAN.dll')
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global CANDeviceChannelNumber
        vco = _VCI_CAN_OBJ()
        vco.ID = 0x18F300FF + BMS_Index * 0x100
        vco.SendType = 0
        vco.RemoteFlag = 0
        vco.ExternFlag = 1
        vco.DataLen = 8
        vco.Data = (0, 0, 0, 0, 0, 0, 0, 0)
        ReturnFlag = canLib.VCI_Transmit(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber,
                                         pointer(vco), 1)

    #CAN发送数据
    def CAN_Send(self, CAN_ID, Data):
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global CANDeviceChannelNumber

        canLib = windll.LoadLibrary('.\DLL\ControlCAN.dll')
        vco = _VCI_CAN_OBJ()
        vco.ID = CAN_ID
        vco.SendType = 0
        vco.RemoteFlag = 0
        vco.ExternFlag = 1
        vco.DataLen = 8
        vco.Data = Data
        ReturnFlag = canLib.VCI_Transmit(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber,
                                         pointer(vco), 1)

    #CAN接收数据
    def CAN_ReceiveBMS(self):
        canLib = windll.LoadLibrary('.\DLL\ControlCAN.dll')
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global CANDeviceChannelNumber
        Voc = _VCI_CAN_OBJ()
        Num = canLib.VCI_GetReceiveNum(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber)
        if Num > 0:
            for i in range(Num):
                ret = canLib.VCI_Receive(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber,
                                         byref(Voc), 1, 0)
                self.CAN_DataDeal(Voc.ID, list(Voc.Data))
                # print(Voc.ID)

        canLib.VCI_ClearBuffer(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber)

    #CAN数据处理
    def CAN_DataDeal(self, ID, Data):
        global UpgradeModule_List
        global Upgrade_Struct_Dict
        global UpgradeModule_SendFileIndexList

        if (ID & 0x00FF0000) == 0x00F00000:  # 复位
            BMS_Index = ID & 0xFF
            BMS_Index = BMS_Index - Upgrade_Struct_Dict['BMS_BaseID']
            if BMS_Index >= 0 and BMS_Index < 21 and UpgradeModule_List[BMS_Index] != 99:
                if UpgradeModule_List[BMS_Index] != 2:
                    UpgradeModule_List[BMS_Index] = 2
                    Upgrade_Struct_Dict['Step_Count'] = 0
                    Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + '号模块进入BOOT....\n'

        elif (ID & 0x00FF0000) == 0x00F10000:  # 校验信息
            BMS_Index = ID & 0xFF
            BMS_Index = BMS_Index - Upgrade_Struct_Dict['BMS_BaseID']
            if BMS_Index >= 0 and BMS_Index < 21 and UpgradeModule_List[BMS_Index] != 99:
                if UpgradeModule_List[BMS_Index] != 3:
                    UpgradeModule_List[BMS_Index] = 3
                    Upgrade_Struct_Dict['Step_Count'] = 0
                    Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + '号模块校验信息接收完成....\n'

        elif (ID & 0x00FF0000) == 0x00F20000:  # 升级文件
            BMS_Index = ID & 0xFF
            BMS_Index = BMS_Index - Upgrade_Struct_Dict['BMS_BaseID']
            if BMS_Index >= 0 and BMS_Index < 21 and UpgradeModule_List[BMS_Index] != 99:
                if Upgrade_Struct_Dict['Upgrade_Num'] == 1:#单个升级时的重发机制
                    if Data[1] == 1 or Data[1] == 3:
                        Upgrade_Struct_Dict['重发计次'] = 0
                        Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] = 0
                        Upgrade_Struct_Dict['UpgradeFile_Index'] = Upgrade_Struct_Dict['UpgradeFile_Index'] + 1
                        Upgrade_Struct_Dict['Step_Count'] = 0
                        Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + '号模块第'+str(Upgrade_Struct_Dict['UpgradeFile_Index'])+'包接收完成....\n'
                        if Upgrade_Struct_Dict['UpgradeFile_Index'] == Upgrade_Struct_Dict['UpgradePack_Num']:#最后一包，跳转到结束
                            if UpgradeModule_List[BMS_Index] != 4:
                                UpgradeModule_List[BMS_Index] = 4
                                Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + '号模块升级文件接收完成....\n'
                    else:#if Data[1] == 2:
                        Upgrade_Struct_Dict['重发计次'] = Upgrade_Struct_Dict['重发计次'] + 1
                        if Upgrade_Struct_Dict['重发计次'] > 3:#最大重发三次
                            UpgradeModule_List[BMS_Index] = 99
                            Upgrade_Struct_Dict['Step_Count'] = 0
                            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + '号模块升级文件接收失败....\n'
                            Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] = 0
                            Upgrade_Struct_Dict['UpgradeFile_Index'] = 0
                        else:
                            Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] = 0
                            Upgrade_Struct_Dict['UpgradeFile_Index'] = Upgrade_Struct_Dict['UpgradeFile_Index']
                            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + \
                                                          '号模块第'+str(Upgrade_Struct_Dict['UpgradeFile_Index']+1)+'包重发....\n'
                            Upgrade_Struct_Dict['Step_Count'] = 0
                elif Upgrade_Struct_Dict['Upgrade_Num'] == 2:#同时升级时的重发机制
                    if Data[1] == 1 or Data[1] == 3:
                        Upgrade_RepeatList[BMS_Index] = 0
                        Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] = 0
                        UpgradeModule_SendFileIndexList[BMS_Index] = UpgradeModule_SendFileIndexList[BMS_Index] + 1
                        Upgrade_Struct_Dict['Step_Count'] = 0
                        Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + '号模块第'+str(Upgrade_Struct_Dict['UpgradeFile_Index'])+'包接收完成....\n'
                        if UpgradeModule_SendFileIndexList[BMS_Index] == Upgrade_Struct_Dict['UpgradePack_Num']:#最后一包，跳转到结束
                            if UpgradeModule_List[BMS_Index] != 4:
                                UpgradeModule_List[BMS_Index] = 4
                                Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + '号模块升级文件接收完成....\n'
                    else:
                        Upgrade_RepeatList[BMS_Index] = Upgrade_RepeatList[BMS_Index] + 1

        elif (ID & 0x00FF0000) == 0x00F30000:  # 升级结束
            BMS_Index = ID & 0xFF
            BMS_Index = BMS_Index - Upgrade_Struct_Dict['BMS_BaseID']
            BMS_Version = "升级成功，版本号：" + str(Data[4]) +'.'+ str(Data[5])
            if BMS_Index >= 0 and BMS_Index < 21 and UpgradeModule_List[BMS_Index] != 99:
                if UpgradeModule_List[BMS_Index] != 5:
                    UpgradeModule_List[BMS_Index] = 5
                    Upgrade_Struct_Dict['Step_Count'] = 0
                    Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + '号模块升级完成....\n' + BMS_Version + '\n'

#################################UART Port升级#################################
    def Port_Upgrade(self):
        global Upgrade_Struct_Dict
        global Upgrade_File
        global UpgradeModule_List
        global UpgradeModule_SendFileIndexList
        global Upgrade_RepeatList


        if Upgrade_Struct_Dict['Upgrade_Num'] == 1:#单个升级
            for UpgradeIndex in range(20):#一个一个升级
                if UpgradeModule_List[UpgradeIndex] == 1:
                    self.Time_Delay = 0.3 #300ms执行一次
                    Return_Flag = self.Upgrade_BMS_UARTResponse()
                    if Return_Flag != True:
                        Upgrade_Struct_Dict['Step_Count'] = Upgrade_Struct_Dict['Step_Count'] + 1
                        self.UART_UpgradeStart(UpgradeIndex)
                        if  Upgrade_Struct_Dict['Step_Count'] > 10:
                            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(UpgradeIndex+1) + \
                                                          '号模块复位失败....\n'
                            Upgrade_Struct_Dict['Step_Count'] = 0
                            UpgradeModule_List[UpgradeIndex] = 99
                    break
                elif UpgradeModule_List[UpgradeIndex] == 2:
                    self.Time_Delay = 0.3 #200ms执行一次
                    Return_Flag = self.Upgrade_BMS_UARTResponse()
                    if Return_Flag != True:
                        Upgrade_Struct_Dict['Step_Count'] = Upgrade_Struct_Dict['Step_Count'] + 1
                        self.UART_UpgradeCheckInformation(UpgradeIndex)
                        if  Upgrade_Struct_Dict['Step_Count'] > 10:
                            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(UpgradeIndex+1) + \
                                                          '号模块接收校验数据失败....\n'
                            Upgrade_Struct_Dict['Step_Count'] = 0
                            UpgradeModule_List[UpgradeIndex] = 99
                    break
                elif UpgradeModule_List[UpgradeIndex] == 3:
                    if Upgrade_Struct_Dict['UpgradeFile_Index']+1 < Upgrade_Struct_Dict['UpgradePack_Num']:
                        self.Time_Delay = 0.3 #300ms执行一次
                    else:
                        self.Time_Delay = 1 #1000ms执行一次
                    Return_Flag = self.Upgrade_BMS_UARTResponse()
                    if Return_Flag != True:
                        Upgrade_Struct_Dict['Step_Count'] = Upgrade_Struct_Dict['Step_Count'] + 1
                        self.UART_UpgradeData(UpgradeIndex)
                        if  Upgrade_Struct_Dict['Step_Count'] > 3:
                            Upgrade_Struct_Dict['Step_Count'] = 0
                            UpgradeModule_List[UpgradeIndex] = 99
                            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(UpgradeIndex+1) + \
                                                          '号模块第'+str(Upgrade_Struct_Dict['UpgradeFile_Index']+1)+'包接收失败....\n'
                        else:
                            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(UpgradeIndex+1) + \
                                                          '号模块第'+str(Upgrade_Struct_Dict['UpgradeFile_Index']+1)+'包发送....\n'
                    break
                elif UpgradeModule_List[UpgradeIndex] == 4:
                    self.Time_Delay = 0.5 #500ms执行一次
                    Return_Flag = self.Upgrade_BMS_UARTResponse()
                    if Return_Flag != True:
                        Upgrade_Struct_Dict['Step_Count'] = Upgrade_Struct_Dict['Step_Count'] + 1
                        self.UART_UpgradeStop(UpgradeIndex)
                        if  Upgrade_Struct_Dict['Step_Count'] > 10:
                            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(UpgradeIndex+1) + \
                                                          '号模块进入APP失败....\n'
                            Upgrade_Struct_Dict['Step_Count'] = 0
                            UpgradeModule_List[UpgradeIndex] = 99
                    break
        Return_Result = False
        for i in range(20):#任何一个模块在升级步骤中，线程继续
            if UpgradeModule_List[i] < 5 and UpgradeModule_List[i] > 0:
                Return_Result = True
        return Return_Result


    def UART_UpgradeStart(self,BMS_Index):
        send_list = [0x01+BMS_Index,0x10,0x17,0x73,0x00,0x01,0x02,0x00,0x01]
        temp_crc = crc16(send_list,0,9)
        send_list.append(temp_crc%256)
        send_list.append(temp_crc//256)
        send_list = bytes(send_list)
        try:
            Serial_Port.write(send_list)  # item.encode('utf-8'))
        except Exception as e:
            pass

    def UART_UpgradeCheckInformation(self,BMS_Index):
        global Upgrade_Struct_Dict

        send_list = [0x01+BMS_Index,0xF1,0x01,0x07]
        send_list.append(Upgrade_Struct_Dict['CRC校验']//256)
        send_list.append(Upgrade_Struct_Dict['CRC校验']%256)
        send_list.append(Upgrade_Struct_Dict['UpgradeFile_Size'] // 65535)
        send_list.append(Upgrade_Struct_Dict['UpgradeFile_Size'] % 65535 // 256)
        send_list.append(Upgrade_Struct_Dict['UpgradeFile_Size'] % 256)
        send_list.append(Upgrade_Struct_Dict['UpgradePack_Num']//256)
        send_list.append(Upgrade_Struct_Dict['UpgradePack_Num']%256)

        temp_crc = crc16(send_list,0,11)
        send_list.append(temp_crc%256)
        send_list.append(temp_crc//256)
        send_list = bytes(send_list)
        try:
            Serial_Port.write(send_list)  # item.encode('utf-8'))
        except Exception as e:
            pass

    def UART_UpgradeData(self,BMS_Index):
        global Upgrade_Struct_Dict

        send_list = [0x01 + BMS_Index, 0xF2, 0x01, 130]

        send_list.append(Upgrade_Struct_Dict['UpgradeFile_Index']//256)
        send_list.append(Upgrade_Struct_Dict['UpgradeFile_Index']%256)
        Pack_Byte_Num = 128
        if Upgrade_Struct_Dict['UpgradeFile_Index'] <= Upgrade_Struct_Dict['UpgradePack_Num']:
            for i in range(Pack_Byte_Num):
                temp = Upgrade_File[Upgrade_Struct_Dict['UpgradeFile_Index']*Pack_Byte_Num + i]
                send_list.append(temp)
        temp_crc = crc16(send_list,0,6+Pack_Byte_Num)
        send_list.append(temp_crc%256)
        send_list.append(temp_crc//256)

        send_list = bytes(send_list)
        try:
            Serial_Port.write(send_list)  # item.encode('utf-8'))
        except Exception as e:
            pass

    def UART_UpgradeStop(self,BMS_Index):
        send_list = [0x01 + BMS_Index, 0x04,0x0F, 0xA0, 0x00,0x01]

        temp_crc = crc16(send_list,0,6)
        send_list.append(temp_crc%256)
        send_list.append(temp_crc//256)

        send_list = bytes(send_list)
        try:
            Serial_Port.write(send_list)  # item.encode('utf-8'))
        except Exception as e:
            pass

    def Upgrade_BMS_UARTResponse(self,):
        global UpgradeModule_List
        global Upgrade_Struct_Dict
        global UpgradeModule_SendFileIndexList

        ReadBuff = []
        try:
            num = Serial_Port.inWaiting()
        except:
            return None
        if num > 3:
            data = Serial_Port.read(num)
            num = len(data)
            # ReadBuff = int.from_bytes(data, byteorder='little', signed=True)
            # for i in range(len(data)):
            #     print(data[i])
                # ReadBuff.append(int(hex(data[i*4:i*4+4])))
            Rec_CRC = data[num-2]*256+data[num-1]
            Cal_CRC = crc16(data,0,num-2)
            if Rec_CRC == Cal_CRC:
                if data[1] == 0x10:  # 开始升级
                    BMS_Index = data[0]-1
                    if BMS_Index >= 0 and BMS_Index < 21 and UpgradeModule_List[BMS_Index] != 99:
                        if data[4] == 1:#成功
                            Upgrade_Struct_Dict['重发次数'] = 0
                            if UpgradeModule_List[BMS_Index] != 2:
                                UpgradeModule_List[BMS_Index] = 2
                                Upgrade_Struct_Dict['Step_Count'] = 0
                                Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + '号模块进入Boot....\n'
                                return True
                        else:#失败
                            return False
                    else:#地址错误
                        return False
                elif data[1] == 0xF1:   #校验
                    BMS_Index = data[0]-1
                    if BMS_Index >= 0 and BMS_Index < 21 and UpgradeModule_List[BMS_Index] != 99:
                        if data[4] == 1:#成功
                            Upgrade_Struct_Dict['重发次数'] = 0
                            if UpgradeModule_List[BMS_Index] != 3:
                                UpgradeModule_List[BMS_Index] = 3
                                Upgrade_Struct_Dict['Step_Count'] = 0
                                Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + '号模块校验信息接收完成....\n'
                                return True
                        else:#失败
                            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + '号模块校验信息接收失败....\n'
                            return False
                    else:#地址错误
                        return False
                elif data[1] == 0xF2:   #升级数据
                    BMS_Index = data[0]-1
                    if BMS_Index >= 0 and BMS_Index < 21 and UpgradeModule_List[BMS_Index] != 99:
                        if data[4] == 1:#成功
                            Upgrade_Struct_Dict['UpgradeFile_Index'] = Upgrade_Struct_Dict['UpgradeFile_Index'] + 1
                            Upgrade_Struct_Dict['重发次数'] = 0
                            Upgrade_Struct_Dict['Step_Count'] = 0
                            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + \
                                                          '号模块第'+str(Upgrade_Struct_Dict['UpgradeFile_Index'])+'包接收完成....\n'
                            if Upgrade_Struct_Dict['UpgradeFile_Index'] == Upgrade_Struct_Dict['UpgradePack_Num']:
                                if UpgradeModule_List[BMS_Index] != 4:
                                    UpgradeModule_List[BMS_Index] = 4
                            return True
                        elif data[4] == 3:#文件CRC校验失败
                            Upgrade_Struct_Dict['重发次数'] = 4
                            Upgrade_Struct_Dict['Step_Count'] = 0
                            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + \
                                                          '号模块文件校验失败....\n'
                            return False
                        else:#失败
                            return False
                    else:#地址错误
                        return False
                elif data[1] == 0x04:#结束
                    BMS_Index = data[0]-1
                    if BMS_Index >= 0 and BMS_Index < 21 and UpgradeModule_List[BMS_Index] != 99:
                        if UpgradeModule_List[BMS_Index] != 5:
                            UpgradeModule_List[BMS_Index] = 5
                            BMS_Version = "升级成功，版本号：" + str(data[3]) +'.'+ str(data[4])
                            Upgrade_Struct_Dict['Step_Count'] = 0
                            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + str(BMS_Index+1) + '号模块升级完成....\n' + BMS_Version + '\n'
                            return True
                    else:#地址错误
                        return False




######################################界面类#########################################
class Ui_Upgrade_Tool(object):
    def setupUi(self, Upgrade_Tool):
        Upgrade_Tool.setObjectName("Upgrade_Tool")
        Upgrade_Tool.resize(748, 637)
        self.centralwidget = QtWidgets.QWidget(Upgrade_Tool)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.widget_TCP = QtWidgets.QWidget(self.centralwidget)
        self.widget_TCP.setEnabled(True)
        self.widget_TCP.setAutoFillBackground(True)
        self.widget_TCP.setObjectName("widget_TCP")
        self.label_TCP = QtWidgets.QLabel(self.widget_TCP)
        self.label_TCP.setGeometry(QtCore.QRect(9, 9, 53, 18))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_TCP.setFont(font)
        self.label_TCP.setObjectName("label_TCP")
        self.label_IPPort = QtWidgets.QLabel(self.widget_TCP)
        self.label_IPPort.setGeometry(QtCore.QRect(10, 70, 54, 16))
        self.label_IPPort.setObjectName("label_IPPort")
        self.lineEdit_IPAddr = QtWidgets.QLineEdit(self.widget_TCP)
        self.lineEdit_IPAddr.setGeometry(QtCore.QRect(81, 40, 133, 20))
        self.lineEdit_IPAddr.setObjectName("lineEdit_IPAddr")
        self.lineEdit_IPPort = QtWidgets.QLineEdit(self.widget_TCP)
        self.lineEdit_IPPort.setGeometry(QtCore.QRect(81, 70, 133, 20))
        self.lineEdit_IPPort.setObjectName("lineEdit_IPPort")
        self.label_IPAddr = QtWidgets.QLabel(self.widget_TCP)
        self.label_IPAddr.setGeometry(QtCore.QRect(9, 40, 66, 16))
        self.label_IPAddr.setObjectName("label_IPAddr")
        self.pushButton_TCPConnect = QtWidgets.QPushButton(self.widget_TCP)
        self.pushButton_TCPConnect.setGeometry(QtCore.QRect(9, 190, 75, 23))
        self.pushButton_TCPConnect.setObjectName("pushButton_TCPConnect")
        self.gridLayout_5.addWidget(self.widget_TCP, 0, 0, 1, 1)
        self.widget_UART = QtWidgets.QWidget(self.centralwidget)
        self.widget_UART.setEnabled(True)
        self.widget_UART.setAutoFillBackground(True)
        self.widget_UART.setObjectName("widget_UART")
        self.label_UART = QtWidgets.QLabel(self.widget_UART)
        self.label_UART.setGeometry(QtCore.QRect(9, 9, 60, 18))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_UART.setFont(font)
        self.label_UART.setObjectName("label_UART")
        self.pushButton_UARTConnect = QtWidgets.QPushButton(self.widget_UART)
        self.pushButton_UARTConnect.setGeometry(QtCore.QRect(9, 190, 75, 23))
        self.pushButton_UARTConnect.setObjectName("pushButton_UARTConnect")
        self.pushButton_CheckPort = QtWidgets.QPushButton(self.widget_UART)
        self.pushButton_CheckPort.setGeometry(QtCore.QRect(210, 160, 80, 23))
        self.pushButton_CheckPort.setObjectName("pushButton_CheckPort")
        self.comboBox_Port = QtWidgets.QComboBox(self.widget_UART)
        self.comboBox_Port.setGeometry(QtCore.QRect(90, 70, 61, 20))
        self.comboBox_Port.setObjectName("comboBox_Port")
        self.comboBox_Port.addItem("")
        self.comboBox_Port.addItem("")
        self.comboBox_Port.addItem("")
        self.comboBox_Port.addItem("")
        self.comboBox_Port.addItem("")
        self.comboBox_Port.addItem("")
        self.comboBox_Port.addItem("")
        self.comboBox_Port.addItem("")
        self.comboBox_Port.addItem("")
        self.comboBox_Port.addItem("")
        self.comboBox_Port.addItem("")
        self.comboBox_Port.addItem("")
        self.comboBox_Port.addItem("")
        self.comboBox_Port.addItem("")
        self.comboBox_Port.addItem("")
        self.textBrowser = QtWidgets.QTextBrowser(self.widget_UART)
        self.textBrowser.setGeometry(QtCore.QRect(158, 40, 141, 111))
        self.textBrowser.setObjectName("textBrowser")
        self.comboBox_StopBit = QtWidgets.QComboBox(self.widget_UART)
        self.comboBox_StopBit.setGeometry(QtCore.QRect(90, 130, 61, 20))
        self.comboBox_StopBit.setObjectName("comboBox_StopBit")
        self.comboBox_StopBit.addItem("")
        self.comboBox_StopBit.addItem("")
        self.label_PortSelect = QtWidgets.QLabel(self.widget_UART)
        self.label_PortSelect.setGeometry(QtCore.QRect(9, 70, 60, 16))
        self.label_PortSelect.setObjectName("label_PortSelect")
        self.comboBox_BoundRate = QtWidgets.QComboBox(self.widget_UART)
        self.comboBox_BoundRate.setGeometry(QtCore.QRect(90, 40, 62, 20))
        self.comboBox_BoundRate.setObjectName("comboBox_BoundRate")
        self.comboBox_BoundRate.addItem("")
        self.comboBox_BoundRate.addItem("")
        self.comboBox_BoundRate.addItem("")
        self.comboBox_CRCBit = QtWidgets.QComboBox(self.widget_UART)
        self.comboBox_CRCBit.setEnabled(True)
        self.comboBox_CRCBit.setGeometry(QtCore.QRect(90, 160, 61, 20))
        self.comboBox_CRCBit.setObjectName("comboBox_CRCBit")
        self.comboBox_CRCBit.addItem("")
        self.comboBox_CRCBit.addItem("")
        self.comboBox_CRCBit.addItem("")
        self.comboBox_CRCBit.addItem("")
        self.comboBox_CRCBit.addItem("")
        self.label_BoundRate = QtWidgets.QLabel(self.widget_UART)
        self.label_BoundRate.setGeometry(QtCore.QRect(9, 40, 48, 16))
        self.label_BoundRate.setObjectName("label_BoundRate")
        self.label_Bit = QtWidgets.QLabel(self.widget_UART)
        self.label_Bit.setGeometry(QtCore.QRect(9, 100, 48, 16))
        self.label_Bit.setObjectName("label_Bit")
        self.label_CRCBit = QtWidgets.QLabel(self.widget_UART)
        self.label_CRCBit.setGeometry(QtCore.QRect(9, 160, 36, 16))
        self.label_CRCBit.setObjectName("label_CRCBit")
        self.label_StopBit = QtWidgets.QLabel(self.widget_UART)
        self.label_StopBit.setGeometry(QtCore.QRect(9, 130, 48, 16))
        self.label_StopBit.setObjectName("label_StopBit")
        self.comboBox_Bit = QtWidgets.QComboBox(self.widget_UART)
        self.comboBox_Bit.setGeometry(QtCore.QRect(90, 100, 61, 20))
        self.comboBox_Bit.setObjectName("comboBox_Bit")
        self.comboBox_Bit.addItem("")
        self.comboBox_Bit.addItem("")
        self.comboBox_Bit.addItem("")
        self.gridLayout_5.addWidget(self.widget_UART, 0, 4, 1, 1)
        self.widget_CAN = QtWidgets.QWidget(self.centralwidget)
        self.widget_CAN.setEnabled(True)
        self.widget_CAN.setAutoFillBackground(True)
        self.widget_CAN.setObjectName("widget_CAN")
        self.label_CAN = QtWidgets.QLabel(self.widget_CAN)
        self.label_CAN.setGeometry(QtCore.QRect(9, 9, 53, 18))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_CAN.setFont(font)
        self.label_CAN.setObjectName("label_CAN")
        self.pushButton_CANConnect = QtWidgets.QPushButton(self.widget_CAN)
        self.pushButton_CANConnect.setGeometry(QtCore.QRect(9, 190, 75, 23))
        self.pushButton_CANConnect.setObjectName("pushButton_CANConnect")
        self.comboBox_CANDevice = QtWidgets.QComboBox(self.widget_CAN)
        self.comboBox_CANDevice.setGeometry(QtCore.QRect(90, 40, 71, 20))
        self.comboBox_CANDevice.setObjectName("comboBox_CANDevice")
        self.comboBox_CANDevice.addItem("")
        self.comboBox_CANDevice.addItem("")
        self.comboBox_CANBoundRate = QtWidgets.QComboBox(self.widget_CAN)
        self.comboBox_CANBoundRate.setGeometry(QtCore.QRect(90, 130, 71, 20))
        self.comboBox_CANBoundRate.setObjectName("comboBox_CANBoundRate")
        self.comboBox_CANBoundRate.addItem("")
        self.comboBox_CANBoundRate.addItem("")
        self.comboBox_CANBoundRate.addItem("")
        self.comboBox_CANBoundRate.addItem("")
        self.comboBox_CANBoundRate.addItem("")
        self.comboBox_CANBoundRate.addItem("")
        self.comboBox_CANBoundRate.addItem("")
        self.comboBox_CANBoundRate.addItem("")
        self.label_CANChannel = QtWidgets.QLabel(self.widget_CAN)
        self.label_CANChannel.setGeometry(QtCore.QRect(9, 100, 36, 16))
        self.label_CANChannel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_CANChannel.setObjectName("label_CANChannel")
        self.comboBox_CANChannel = QtWidgets.QComboBox(self.widget_CAN)
        self.comboBox_CANChannel.setGeometry(QtCore.QRect(90, 100, 71, 20))
        self.comboBox_CANChannel.setObjectName("comboBox_CANChannel")
        self.comboBox_CANChannel.addItem("")
        self.comboBox_CANChannel.addItem("")
        self.label_CANBoundRate = QtWidgets.QLabel(self.widget_CAN)
        self.label_CANBoundRate.setGeometry(QtCore.QRect(9, 130, 36, 16))
        self.label_CANBoundRate.setObjectName("label_CANBoundRate")
        self.comboBox_CANIndex = QtWidgets.QComboBox(self.widget_CAN)
        self.comboBox_CANIndex.setGeometry(QtCore.QRect(90, 70, 71, 20))
        self.comboBox_CANIndex.setObjectName("comboBox_CANIndex")
        self.comboBox_CANIndex.addItem("")
        self.comboBox_CANIndex.addItem("")
        self.comboBox_CANIndex.addItem("")
        self.comboBox_CANIndex.addItem("")
        self.comboBox_CANIndex.addItem("")
        self.comboBox_CANIndex.addItem("")
        self.comboBox_CANIndex.addItem("")
        self.comboBox_CANIndex.addItem("")
        self.label_CANDevice = QtWidgets.QLabel(self.widget_CAN)
        self.label_CANDevice.setGeometry(QtCore.QRect(9, 40, 42, 16))
        self.label_CANDevice.setObjectName("label_CANDevice")
        self.label_CANIndex = QtWidgets.QLabel(self.widget_CAN)
        self.label_CANIndex.setGeometry(QtCore.QRect(9, 70, 60, 16))
        self.label_CANIndex.setObjectName("label_CANIndex")
        self.gridLayout_5.addWidget(self.widget_CAN, 0, 2, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_5.addWidget(self.line_3, 1, 0, 1, 5)
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_5.addWidget(self.line_5, 0, 3, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_FileVersion = QtWidgets.QLabel(self.centralwidget)
        self.label_FileVersion.setObjectName("label_FileVersion")
        self.gridLayout_4.addWidget(self.label_FileVersion, 5, 1, 1, 2)
        self.checkBox_Module5 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module5.setAutoFillBackground(True)
        self.checkBox_Module5.setObjectName("checkBox_Module5")
        self.gridLayout_4.addWidget(self.checkBox_Module5, 9, 5, 1, 1)
        self.checkBox_Module20 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module20.setAutoFillBackground(True)
        self.checkBox_Module20.setObjectName("checkBox_Module20")
        self.gridLayout_4.addWidget(self.checkBox_Module20, 12, 5, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_4.addWidget(self.line_2, 7, 1, 1, 5)
        self.label_FileSize = QtWidgets.QLabel(self.centralwidget)
        self.label_FileSize.setObjectName("label_FileSize")
        self.gridLayout_4.addWidget(self.label_FileSize, 4, 1, 1, 2)
        self.checkBox_Module17 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module17.setAutoFillBackground(True)
        self.checkBox_Module17.setObjectName("checkBox_Module17")
        self.gridLayout_4.addWidget(self.checkBox_Module17, 12, 2, 1, 1)
        self.checkBox_Module16 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module16.setAutoFillBackground(True)
        self.checkBox_Module16.setObjectName("checkBox_Module16")
        self.gridLayout_4.addWidget(self.checkBox_Module16, 12, 1, 1, 1)
        self.label_Load = QtWidgets.QLabel(self.centralwidget)
        self.label_Load.setObjectName("label_Load")
        self.gridLayout_4.addWidget(self.label_Load, 2, 2, 1, 4)
        self.checkBox_Module18 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module18.setAutoFillBackground(True)
        self.checkBox_Module18.setObjectName("checkBox_Module18")
        self.gridLayout_4.addWidget(self.checkBox_Module18, 12, 3, 1, 1)
        self.checkBox_Module9 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module9.setAutoFillBackground(True)
        self.checkBox_Module9.setObjectName("checkBox_Module9")
        self.gridLayout_4.addWidget(self.checkBox_Module9, 10, 4, 1, 1)
        self.checkBox_AllUp = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_AllUp.setObjectName("checkBox_AllUp")
        self.gridLayout_4.addWidget(self.checkBox_AllUp, 8, 5, 1, 1)
        self.pushButton_StartUpgrade = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_StartUpgrade.setObjectName("pushButton_StartUpgrade")
        self.gridLayout_4.addWidget(self.pushButton_StartUpgrade, 14, 1, 1, 1)
        self.checkBox_Module3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module3.setAutoFillBackground(True)
        self.checkBox_Module3.setObjectName("checkBox_Module3")
        self.gridLayout_4.addWidget(self.checkBox_Module3, 9, 3, 1, 1)
        self.checkBox_Module11 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module11.setAutoFillBackground(True)
        self.checkBox_Module11.setObjectName("checkBox_Module11")
        self.gridLayout_4.addWidget(self.checkBox_Module11, 11, 1, 1, 1)
        self.checkBox_SelectAll = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_SelectAll.setObjectName("checkBox_SelectAll")
        self.gridLayout_4.addWidget(self.checkBox_SelectAll, 13, 5, 1, 1)
        self.checkBox_Module10 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module10.setAutoFillBackground(True)
        self.checkBox_Module10.setObjectName("checkBox_Module10")
        self.gridLayout_4.addWidget(self.checkBox_Module10, 10, 5, 1, 1)
        self.checkBox_Module12 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module12.setAutoFillBackground(True)
        self.checkBox_Module12.setObjectName("checkBox_Module12")
        self.gridLayout_4.addWidget(self.checkBox_Module12, 11, 2, 1, 1)
        self.label_FileCRC = QtWidgets.QLabel(self.centralwidget)
        self.label_FileCRC.setObjectName("label_FileCRC")
        self.gridLayout_4.addWidget(self.label_FileCRC, 4, 3, 1, 3)
        self.checkBox_Module7 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module7.setAutoFillBackground(True)
        self.checkBox_Module7.setObjectName("checkBox_Module7")
        self.gridLayout_4.addWidget(self.checkBox_Module7, 10, 2, 1, 1)
        self.checkBox_Module13 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module13.setAutoFillBackground(True)
        self.checkBox_Module13.setObjectName("checkBox_Module13")
        self.gridLayout_4.addWidget(self.checkBox_Module13, 11, 3, 1, 1)
        self.checkBox_Module8 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module8.setAutoFillBackground(True)
        self.checkBox_Module8.setObjectName("checkBox_Module8")
        self.gridLayout_4.addWidget(self.checkBox_Module8, 10, 3, 1, 1)
        self.comboBox_SelcectZC = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_SelcectZC.setObjectName("comboBox_SelcectZC")
        self.comboBox_SelcectZC.addItem("")
        self.comboBox_SelcectZC.addItem("")
        self.gridLayout_4.addWidget(self.comboBox_SelcectZC, 8, 1, 1, 1)
        self.checkBox_Module19 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module19.setAutoFillBackground(True)
        self.checkBox_Module19.setObjectName("checkBox_Module19")
        self.gridLayout_4.addWidget(self.checkBox_Module19, 12, 4, 1, 1)
        self.checkBox_Module4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module4.setAutoFillBackground(True)
        self.checkBox_Module4.setObjectName("checkBox_Module4")
        self.gridLayout_4.addWidget(self.checkBox_Module4, 9, 4, 1, 1)
        self.pushButton_OpenFile = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_OpenFile.setObjectName("pushButton_OpenFile")
        self.gridLayout_4.addWidget(self.pushButton_OpenFile, 2, 1, 1, 1)
        self.checkBox_Module2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module2.setAutoFillBackground(True)
        self.checkBox_Module2.setObjectName("checkBox_Module2")
        self.gridLayout_4.addWidget(self.checkBox_Module2, 9, 2, 1, 1)
        self.checkBox_Module6 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module6.setAutoFillBackground(True)
        self.checkBox_Module6.setObjectName("checkBox_Module6")
        self.gridLayout_4.addWidget(self.checkBox_Module6, 10, 1, 1, 1)
        self.checkBox_Module15 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module15.setAutoFillBackground(True)
        self.checkBox_Module15.setObjectName("checkBox_Module15")
        self.gridLayout_4.addWidget(self.checkBox_Module15, 11, 5, 1, 1)
        self.checkBox_OneUp = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_OneUp.setObjectName("checkBox_OneUp")
        self.checkBox_OneUp.setChecked(True)
        self.gridLayout_4.addWidget(self.checkBox_OneUp, 8, 4, 1, 1)
        self.checkBox_Module14 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module14.setAutoFillBackground(True)
        self.checkBox_Module14.setObjectName("checkBox_Module14")
        self.gridLayout_4.addWidget(self.checkBox_Module14, 11, 4, 1, 1)

        self.checkBox_Module1 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Module1.setAutoFillBackground(True)
        self.checkBox_Module1.setObjectName("checkBox_Module1")
        self.gridLayout_4.addWidget(self.checkBox_Module1, 9, 1, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_4.addWidget(self.progressBar, 14, 2, 1, 4)
        self.pushButton_SaveRecord = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_SaveRecord.setObjectName("pushButton_SaveRecord")
        self.gridLayout_4.addWidget(self.pushButton_SaveRecord, 14, 9, 1, 1)
        self.textBrowser_UpgradeRecord = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_UpgradeRecord.setMinimumSize(QtCore.QSize(318, 291))
        self.textBrowser_UpgradeRecord.setObjectName("textBrowser_UpgradeRecord")
        self.gridLayout_4.addWidget(self.textBrowser_UpgradeRecord, 2, 6, 12, 4)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_4.addWidget(self.line, 1, 1, 1, 9)
        self.label_CommInfo = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_CommInfo.setFont(font)
        self.label_CommInfo.setObjectName("label_CommInfo")
        self.gridLayout_4.addWidget(self.label_CommInfo, 0, 1, 1, 9)
        self.gridLayout_4.setRowMinimumHeight(2, 30)
        self.gridLayout_4.setRowMinimumHeight(8, 30)
        self.gridLayout_4.setRowMinimumHeight(9, 30)
        self.gridLayout_4.setRowMinimumHeight(10, 30)
        self.gridLayout_4.setRowMinimumHeight(11, 30)
        self.gridLayout_4.setRowMinimumHeight(12, 30)
        self.gridLayout_4.setRowMinimumHeight(13, 30)
        self.gridLayout_4.setRowMinimumHeight(14, 30)
        self.gridLayout_5.addLayout(self.gridLayout_4, 2, 0, 1, 5)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_5.addWidget(self.line_4, 0, 1, 1, 1)
        self.gridLayout_5.setColumnMinimumWidth(0, 220)
        self.gridLayout_5.setColumnMinimumWidth(2, 180)
        self.gridLayout_5.setColumnMinimumWidth(4, 300)
        self.gridLayout_5.setRowMinimumHeight(0, 220)
        Upgrade_Tool.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Upgrade_Tool)
        self.statusbar.setObjectName("statusbar")
        Upgrade_Tool.setStatusBar(self.statusbar)
        self.actionCAN_Open = QtWidgets.QAction(Upgrade_Tool)
        self.actionCAN_Open.setObjectName("actionCAN_Open")
        self.actionUART_Open = QtWidgets.QAction(Upgrade_Tool)
        self.actionUART_Open.setObjectName("actionUART_Open")
        self.actionTCP_Open = QtWidgets.QAction(Upgrade_Tool)
        self.actionTCP_Open.setObjectName("actionTCP_Open")

        self.retranslateUi(Upgrade_Tool)
        self.pushButton_OpenFile.clicked.connect(self.Open_Bin)
        self.pushButton_TCPConnect.clicked.connect(self.TCP_Init)
        self.pushButton_CANConnect.clicked.connect(self.CAN_Init)
        self.pushButton_UARTConnect.clicked.connect(self.Poart_Init)
        self.pushButton_CheckPort.clicked.connect(self.Port_Check)
        self.checkBox_OneUp.stateChanged.connect(self.OneUp)
        self.checkBox_AllUp.stateChanged.connect(self.AllUp)
        self.checkBox_SelectAll.stateChanged.connect(self.Check_ALLModule)
        self.pushButton_StartUpgrade.clicked.connect(self.UpgardeMOdule)
        self.comboBox_SelcectZC.currentIndexChanged.connect(self.Module_Change)
        self.pushButton_SaveRecord.clicked.connect(self.Record_Save2TXT)

        TCP_RunTimer.timeout.connect(self.TCP_Upgrade)
        CAN_RunTimer.timeout.connect(self.CAN_Upgrade)
        Port_RunTimer.timeout.connect(self.Port_Upgrade)
        QtCore.QMetaObject.connectSlotsByName(Upgrade_Tool)

##############################################
    def Open_Bin(self):
        global Upgrade_Struct_Dict
        global Upgrade_File

        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Bin files(*.bin)')
        if openfile_name[0]:
            self.label_Load.setText(openfile_name[0])
            Upgrade_FileTemp = open(openfile_name[0],'rb')
            Upgrade_Struct_Dict['UpgradeFile_Size'] = os.path.getsize(openfile_name[0])  # 获得文件大小
            for i in range(Upgrade_Struct_Dict['UpgradeFile_Size']):
                hus = Upgrade_FileTemp.read(1)
                hus = ord(hus)
                Upgrade_File[i] = hus
            Upgrade_Struct_Dict['CRC校验'] = crc16(Upgrade_File,0,Upgrade_Struct_Dict['UpgradeFile_Size'])
            self.label_FileSize.setText("文件大小: " + str(Upgrade_Struct_Dict['UpgradeFile_Size']) + " Bytes")
            self.label_FileCRC.setText("CRC校验: "+str(hex(Upgrade_Struct_Dict['CRC校验'])))
            path = openfile_name[0]
            file_Name = os.path.basename(path)[0:-4]
            self.label_FileVersion.setText('文件版本: '+file_Name)

################TCP初始化函数##############################

    def TCP_Init(self):
        global Communication_Information
        global Communication_Index

        temp  = self.pushButton_TCPConnect.text()
        TCP_Port = self.lineEdit_IPPort.text()
        TCP_IP = self.lineEdit_IPAddr.text()
        if temp == "连接":
            try:
                ReturnNum = self.TCP_Connect()
                if ReturnNum == 0:#打开成功
                    self.pushButton_TCPConnect.setText("关闭")
                    self.widget_CAN.setEnabled(False)
                    self.widget_UART.setEnabled(False)
                    Communication_Information = "TCP/IP连接.IP地址: " + str(TCP_IP) + "IP端口: "+str(TCP_Port)
                    self.label_CommInfo.setText(Communication_Information)
                    Communication_Index = 1
                else:#打开失败
                    reply = QMessageBox.warning(self,
                                                "提示",
                                                "打开失败！",
                                                QMessageBox.Yes)
            except:
                reply = QMessageBox.warning(self,
                                            "提示",
                                            "打开失败！",
                                            QMessageBox.Yes)
        elif temp == "关闭":
            self.TCP_Close()
            self.pushButton_TCPConnect.setText("连接")
            self.widget_CAN.setEnabled(True)
            self.widget_UART.setEnabled(True)

    def TCP_Connect(self):
        global tcp_client_socket

        TCP_Port = self.lineEdit_IPPort.text()
        TCP_IP = self.lineEdit_IPAddr.text()
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_client_socket.connect((BCMU_IP, BCMU_Port))
            Message = [0xAA, 0x55, 0x00, 0x00, 0x00, 0x06, 0x01, 0x04, 0x00, 0x00, 0x00, 0x01]
            meg = struct.pack("%dB" % (len(Message)), *Message)
            tcp_client_socket.send(meg)

            time.sleep(0.1)
            # 4.接收服务器返回的消息
            recv_data = tcp_client_socket.recv(2048)

            if recv_data:
                return 0
            else:
                Close_Connect()
                return -1
        except:
            tcp_client_socket
            tcp_client_socket.close()
            return -1

    def TCP_Close(self):
        global tcp_client_socket
        global Communication_Information
        global Communication_Index

        tcp_client_socket.close()
        Communication_Information = "未打开设备"
        self.label_CommInfo.setText(Communication_Information)
        Communication_Index = 0

##################CAN初始化函数############################
    def CAN_Init(self):
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global CANDeviceChannelNumber
        global Communication_Information
        global Communication_Index
        global CANDeviceBoundRate
        CANDeviceName = self.comboBox_CANDevice.currentText()
        if CANDeviceName == 'USBCAN1':
            CANDeviceNameNumber = 3
        elif CANDeviceName == 'USBCAN2':
            CANDeviceNameNumber = 4
        CANDeviceIndex = self.comboBox_CANIndex.currentText()
        CANDeviceIndexNumber = int(CANDeviceIndex)
        CANDeviceChannel = self.comboBox_CANChannel.currentText()
        CANDeviceChannelNumber = int(CANDeviceChannel)
        BoundRate = self.comboBox_CANBoundRate.currentText()
        if BoundRate == '10Kbps':
            # vic.Timing0 = 0x31
            # vic.Timing1 = 0x1C
            CANDeviceBoundRate = 0x311C
        elif BoundRate == '50Kbps':
            # vic.Timing0 = 0x09
            # vic.Timing1 = 0x1C
            CANDeviceBoundRate = 0x091C
        elif BoundRate == '100Kbps':
            # vic.Timing0 = 0x04
            # vic.Timing1 = 0x1C
            CANDeviceBoundRate = 0x041C
        elif BoundRate == '125Kbps':
            # vic.Timing0 = 0x03
            # vic.Timing1 = 0x1C
            CANDeviceBoundRate = 0x031C
        elif BoundRate == '200Kbps':
            # vic.Timing0 = 0x81
            # vic.Timing1 = 0xFA
            CANDeviceBoundRate = 0x81FA
        elif BoundRate == '250Kbps':
            # vic.Timing0 = 0x01
            # vic.Timing1 = 0x1C
            CANDeviceBoundRate = 0x011C
        elif BoundRate == '500Kbps':
            # vic.Timing0 = 0x00
            # vic.Timing1 = 0x1C
            CANDeviceBoundRate = 0x001C
        elif BoundRate == '1000Kbps':
            # vic.Timing0 = 0x09
            # vic.Timing1 = 0x14
            CANDeviceBoundRate = 0x0914
        if self.pushButton_CANConnect.text() == "连接":
            try:
                ReturN_Flag =  Gloabl_CAN_Init()
                if ReturN_Flag != 1:
                    reply = QMessageBox.warning(self,
                                                "提示"+str(ReturN_Flag),
                                                "CAN启动失败！",
                                                QMessageBox.Yes)
                    return
                self.CAN_Close()
                self.pushButton_CANConnect.setText("关闭")


                self.widget_TCP.setEnabled(False)
                self.widget_UART.setEnabled(False)
                Communication_Information = CANDeviceName + '  波特率：' + BoundRate + '  通道号：' + CANDeviceChannel
                self.label_CommInfo.setText(Communication_Information)
                Communication_Index = 2
            except Exception as e:
                print(e)
                reply = QMessageBox.warning(self,
                                            "提示",
                                            "CAN启动失败2！",
                                            QMessageBox.Yes)
        elif self.pushButton_CANConnect.text() == "关闭":
            self.CAN_Close()

    def CAN_Close(self):
        canLib = windll.LoadLibrary('.\DLL\ControlCAN.dll')
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global Communication_Information
        global Communication_Index

        canLib.VCI_CloseDevice(CANDeviceNameNumber, CANDeviceIndexNumber)
        self.pushButton_CANConnect.setText(QtCore.QCoreApplication.translate("Form", "连接"))
        Communication_Information = "未打开设备"
        self.label_CommInfo.setText(Communication_Information)
        Communication_Index = 0

        self.widget_TCP.setEnabled(True)
        self.widget_UART.setEnabled(True)


###################Port初始化函数###########################
    def Poart_Init(self):
        global Communication_Information
        global Communication_Index
        global Serial_Port

        if self.pushButton_UARTConnect.text() == "连接" :
            Serial_Port.baudrate = int(self.comboBox_BoundRate.currentText())
            Serial_Port.port = str(self.comboBox_Port.currentText())
            Serial_Port.bytesize = int(self.comboBox_Bit.currentText())
            Serial_Port.stopbits = int(self.comboBox_StopBit.currentText())
            self.str = str(self.comboBox_CRCBit.currentText())
            Serial_Port.parity = self.str[0:1]

            try:
                Serial_Port.open()
                time.sleep(0.1)
                if Serial_Port.isOpen():
                    self.textBrowser.append("打开成功!!!")
                    self.pushButton_UARTConnect.setText(QtCore.QCoreApplication.translate("Form", "关闭"))
                    Communication_Information = '设备信息:串口' + str(Serial_Port.port) + '  波特率：' + str(Serial_Port.baudrate)
                    self.label_CommInfo.setText(Communication_Information)
                    Communication_Index = 3

                    self.widget_CAN.setEnabled(False)
                    self.widget_TCP.setEnabled(False)
            except:
                reply = QMessageBox.warning(self,
                                            "提示",
                                            "串口打开失败，请检查串口设置！",
                                            QMessageBox.Yes)

        elif self.pushButton_UARTConnect.text() == "关闭" :
            self.Port_Close()

    def Port_Close(self):
        global Communication_Information
        global Serial_Port

        self.textBrowser.clear()
        Serial_Port.close()
        self.textBrowser.append("串口关闭!!!")
        self.pushButton_UARTConnect.setText(QtCore.QCoreApplication.translate("Form", "连接"))
        Communication_Information = "未打开设备"
        self.label_CommInfo.setText(Communication_Information)
        Communication_Index = 0
        self.widget_CAN.setEnabled(True)
        self.widget_TCP.setEnabled(True)

    def Port_Check(self):
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.textBrowser.clear()
        for Port_Com in port_list:
            self.Com_Dict["%s" % Port_Com[0]] = "%s" % Port_Com[1]
            self.textBrowser.append("串口号:")
            self.textBrowser.append(Port_Com[0])  # 返回串口号，如COM1
            # self.textBrowser.append("设备硬件:")
            # self.textBrowser.append(port[0])  # 返回设备硬件描述 如USB-SERIAL CH340
            # self.textBrowser.append("设备编号:")
            # self.textBrowser.append(str(port[0]))  # 返回设备编号 如29987
            # self.textBrowser.append("支持波特率:")
            # Baud_List =  com.standardBaudRates()
            # for Baud in Baud_List:
            #     self.textBrowser.append(str(Baud))  # 返回设备的支持波特率列表 如[110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 56000, 57600, 115200, 128000, 256000]

        if len(self.Com_Dict) == 0:
            self.textBrowser.append("无串口")


###################升级组件函数###########################
    def Check_ALLModule(self):
        if self.checkBox_SelectAll.isChecked():
            self.checkBox_Module1.setChecked(True)
            self.checkBox_Module2.setChecked(True)
            self.checkBox_Module3.setChecked(True)
            self.checkBox_Module4.setChecked(True)
            self.checkBox_Module5.setChecked(True)
            self.checkBox_Module6.setChecked(True)
            self.checkBox_Module7.setChecked(True)
            self.checkBox_Module8.setChecked(True)
            self.checkBox_Module9.setChecked(True)
            self.checkBox_Module10.setChecked(True)
            self.checkBox_Module11.setChecked(True)
            self.checkBox_Module12.setChecked(True)
            self.checkBox_Module13.setChecked(True)
            self.checkBox_Module14.setChecked(True)
            self.checkBox_Module15.setChecked(True)
            self.checkBox_Module16.setChecked(True)
            self.checkBox_Module17.setChecked(True)
            self.checkBox_Module18.setChecked(True)
            self.checkBox_Module19.setChecked(True)
            self.checkBox_Module20.setChecked(True)
        else:
            self.checkBox_Module1.setChecked(False)
            self.checkBox_Module2.setChecked(False)
            self.checkBox_Module3.setChecked(False)
            self.checkBox_Module4.setChecked(False)
            self.checkBox_Module5.setChecked(False)
            self.checkBox_Module6.setChecked(False)
            self.checkBox_Module7.setChecked(False)
            self.checkBox_Module8.setChecked(False)
            self.checkBox_Module9.setChecked(False)
            self.checkBox_Module10.setChecked(False)
            self.checkBox_Module11.setChecked(False)
            self.checkBox_Module12.setChecked(False)
            self.checkBox_Module13.setChecked(False)
            self.checkBox_Module14.setChecked(False)
            self.checkBox_Module15.setChecked(False)
            self.checkBox_Module16.setChecked(False)
            self.checkBox_Module17.setChecked(False)
            self.checkBox_Module18.setChecked(False)
            self.checkBox_Module19.setChecked(False)
            self.checkBox_Module20.setChecked(False)

    def OneUp(self):
        if self.checkBox_OneUp.isChecked():
            self.checkBox_AllUp.setChecked(False)

    def AllUp(self):
        if self.checkBox_AllUp.isChecked():
            self.checkBox_OneUp.setChecked(False)

    def UpargeModule_Init(self):
        global UpgradeModule_List

        temp = 0
        if self.checkBox_Module1.isChecked():
            UpgradeModule_List[0] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[0] = 0
        if self.checkBox_Module2.isChecked():
            UpgradeModule_List[1] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[1] = 0
        if self.checkBox_Module3.isChecked():
            UpgradeModule_List[2] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[2] = 0
        if self.checkBox_Module4.isChecked():
            UpgradeModule_List[3] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[3] = 0
        if self.checkBox_Module5.isChecked():
            UpgradeModule_List[4] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[4] = 0
        if self.checkBox_Module6.isChecked():
            UpgradeModule_List[5] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[5] = 0
        if self.checkBox_Module7.isChecked():
            UpgradeModule_List[6] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[6] = 0
        if self.checkBox_Module8.isChecked():
            UpgradeModule_List[7] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[7] = 0
        if self.checkBox_Module9.isChecked():
            UpgradeModule_List[8] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[8] = 0
        if self.checkBox_Module10.isChecked():
            UpgradeModule_List[9] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[9] = 0
        if self.checkBox_Module11.isChecked():
            UpgradeModule_List[10] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[10] = 0
        if self.checkBox_Module12.isChecked():
            UpgradeModule_List[11] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[11] = 0
        if self.checkBox_Module13.isChecked():
            UpgradeModule_List[12] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[12] = 0
        if self.checkBox_Module14.isChecked():
            UpgradeModule_List[13] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[13] = 0
        if self.checkBox_Module15.isChecked():
            UpgradeModule_List[14] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[14] = 0
        if self.checkBox_Module16.isChecked():
            UpgradeModule_List[15] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[15] = 0
        if self.checkBox_Module17.isChecked():
            UpgradeModule_List[16] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[16] = 0
        if self.checkBox_Module18.isChecked():
            UpgradeModule_List[17] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[17] = 0
        if self.checkBox_Module19.isChecked():
            UpgradeModule_List[18] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[18] = 0
        if self.checkBox_Module20.isChecked():
            UpgradeModule_List[19] = 1
            temp = temp + 1
        else:
            UpgradeModule_List[19] = 0

        if temp == 0:
            reply = QMessageBox.warning(self,
                                        "提示",
                                        "未选择设备！",
                                        QMessageBox.Yes)
        return temp

    def Record_Save2TXT(self):
        try:
            StrText = self.textBrowser_UpgradeRecord.toPlainText()
            StrText = str(StrText)
            temp_time = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
            DataLoad = '.\日志'+str(temp_time)+'.txt'
            f = open(DataLoad, 'w')
            f.write('{}'.format(StrText))
            f.close()
        except Exception as e:
            print(e)

    def Module_Change(self):
        global Upgrade_Struct_Dict

        if self.comboBox_SelcectZC.currentText() == '主控BCMU':
            Upgrade_Struct_Dict['BMS_BaseID'] = 0x80
        elif self.comboBox_SelcectZC.currentText() == '从控BMU':
            Upgrade_Struct_Dict['BMS_BaseID'] = 0x65


#################升级操作#############################
    def UpgardeMOdule(self):
        global Communication_Index
        global Upgrade_Struct_Dict

        Uprade_Temp = self.pushButton_StartUpgrade.text()
        if Uprade_Temp == '开始升级':
            if Communication_Index == 0 or Upgrade_Struct_Dict['UpgradeFile_Size'] == 0:
                reply = QMessageBox.warning(self,
                                            "提示",
                                            "未打开通讯设备/文件！",
                                            QMessageBox.Yes)
            elif Communication_Index == 1:#TCP
                TCP_RunTimer.start(50)
                self.pushButton_StartUpgrade.setText('停止升级')
                #self.TCP_Upgrade()
            elif Communication_Index == 2 :#CAN
                Return_Falg = self.UpargeModule_Init()#获取需要升级的模块
                Upgrade_Struct_Dict['UpgradePack_Num'] = Upgrade_Struct_Dict['UpgradeFile_Size'] // 1024 + 1
                if Return_Falg == 0:#没有选择的设备
                    return
                Upgrade_Struct_Dict['Upgrade_Step'] = 0
                Upgrade_Struct_Dict['重发计次'] = 0
                self.CAN_ShowResult(1)
                self.progressBar.setValue(0)
                CAN_RunTimer.start(500)
                self.pushButton_StartUpgrade.setText('停止升级')
                # self.CAN_Upgrade()
            elif Communication_Index == 3:#PORT
                Return_Falg = self.UpargeModule_Init()#获取需要升级的模块
                Upgrade_Struct_Dict['UpgradePack_Num'] = Upgrade_Struct_Dict['UpgradeFile_Size'] // 128 + 1
                if Return_Falg == 0:#没有选择的设备
                    return
                Upgrade_Struct_Dict['Upgrade_Step'] = 0
                Upgrade_Struct_Dict['重发计次'] = 0
                self.CAN_ShowResult(1)
                self.progressBar.setValue(0)
                self.pushButton_StartUpgrade.setText('停止升级')
                Port_RunTimer.start(500)
                # self.Port_Upgrade()
        elif Uprade_Temp == '停止升级':
            self.StopUpgrade()

    def StopUpgrade(self):
        global Upgrade_Struct_Dict

        if Communication_Index == 1:
            TCP_RunTimer.stop()
        elif Communication_Index == 2:
            self.CAN_UpgradeStop()
        elif Communication_Index == 3:
            self.Port_UpgradeStop()

        Upgrade_Struct_Dict['Upgrade_Step'] = 0
        self.pushButton_StartUpgrade.setText('开始升级')

####################TCP升级/数据处理##########################
    def TCP_Upgrade(self):
        global Upgrade_Struct_Dict

        if Upgrade_Struct_Dict['Upgrade_Step'] == 0:#初始化
            Upgrade_Struct_Dict['Upgrade_Step'] = 1
            Upgrade_Struct_Dict['Step_Count'] = 1
            Upgrade_Struct_Dict['UpgradeFile_Index'] = 1
            Upgrade_Struct_Dict['升级状态'] = ''
            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + 'TCP/IP 开始升级....\n'
            self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])
        elif Upgrade_Struct_Dict['Upgrade_Step'] == 1:  # 升级标志并开始升级
            if Upgrade_Struct_Dict['Step_Count'] % 2 == 1:  # 100ms发送一次
                try:
                    # BCMU_Addr = self.lineEdit_IPAddr.text()
                    # BCMU_Port = int(self.lineEdit_IPPort.text())
                    # TCP_MODBUS.TCP_Init(BCMU_Addr, BCMU_Port)
                    self.Start_Upgrade()  # 复位
                    returnNum = self.Check_UpgradeFlag()  # 检查是否进入Boot
                    if returnNum == 0:
                        Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + '发送概要信息....\n'
                        self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])
                        Upgrade_Struct_Dict['Upgrade_Step'] = Upgrade_Struct_Dict['Upgrade_Step'] + 1
                        Upgrade_Struct_Dict['Step_Count'] = 1
                    else:
                        i = 0
                except:
                    i = 0
                if Upgrade_Struct_Dict['Step_Count'] > 40:  # 40次尝试，2S
                    Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + '进入BOOT失败....\n'
                    self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])
                    Upgrade_Struct_Dict['Upgrade_Step'] = 6
            Upgrade_Struct_Dict['Step_Count'] = Upgrade_Struct_Dict['Step_Count'] + 1
        elif Upgrade_Struct_Dict['Upgrade_Step'] == 2:  # 升级标志并发送概要信息
            if Upgrade_Struct_Dict['Step_Count'] % 2 == 1:  # 100ms发送一次
                Send_BUffer = [0xAA, 0x55, 0x00, 0x00, 0x00, 0x06, 0x01, 0x01]
                Send_BUffer.append((Upgrade_Struct_Dict['UpgradeFile_Size'] // 1024 + 1) // 256)
                Send_BUffer.append((Upgrade_Struct_Dict['UpgradeFile_Size'] // 1024 + 1) % 256)  # 总包数
                Send_BUffer.append((Upgrade_Struct_Dict['UpgradeFile_Size'] >> 24) % 256)
                Send_BUffer.append((Upgrade_Struct_Dict['UpgradeFile_Size'] >> 16) % 256)
                Send_BUffer.append((Upgrade_Struct_Dict['UpgradeFile_Size'] >> 8) % 256)
                Send_BUffer.append((Upgrade_Struct_Dict['UpgradeFile_Size'] >> 0) % 256)  # 总字节数
                Send_BUffer.append(Upgrade_Struct_Dict['CRC校验'] // 256)
                Send_BUffer.append(Upgrade_Struct_Dict['CRC校验'] % 256)  # CRC校验
                try:
                    self.TCP_SendData(Send_BUffer)
                    time.sleep(0.1)
                    ReceiveData = self.TCP_ReceiveData()
                    if ReceiveData[8] == 1:
                        Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + '发送升级文件....\n'
                        self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])
                        Upgrade_Struct_Dict['Upgrade_Step'] = Upgrade_Struct_Dict['Upgrade_Step'] + 1
                        Upgrade_Struct_Dict['Step_Count'] = 1
                except:
                    i = 0
                if Upgrade_Struct_Dict['Step_Count'] > 6:
                    Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + '发送概要信息通讯失败....\n'
                    self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])
                    Upgrade_Struct_Dict['Upgrade_Step'] = 6
            Upgrade_Struct_Dict['Step_Count'] = Upgrade_Struct_Dict['Step_Count'] + 1
        elif Upgrade_Struct_Dict['Upgrade_Step'] == 3:  # 升级标志并发送升级文件
            if Upgrade_Struct_Dict['UpgradeFile_Index'] < (Upgrade_Struct_Dict['UpgradeFile_Size'] // 1024 + 1):
                self.progressBar_Upgrade.setValue(
                    Upgrade_Struct_Dict['UpgradeFile_Index'] * 1024 / Upgrade_Struct_Dict['UpgradeFile_Size'] * 100)
                Send_BUffer = [0xAA, 0x55, 0x00, 0x00, 0x00, 0x06, 0x01, 0x02]
                temp = Upgrade_Struct_Dict['UpgradeFile_Index']
                Send_BUffer.append(temp // 256)
                Send_BUffer.append(temp % 256)  # 第几包
                temp = 1024
                Send_BUffer.append(temp // 256)
                Send_BUffer.append(temp % 256)  # 多少字节
                temp = Upgrade_Struct_Dict['UpgradeFile_Index'] * 1024 - 1024
                for i in range(1024):
                    Send_BUffer.append(Upgrade_File[temp + i])
                CRC_temp = self.crc16(Send_BUffer,0, 1035)
                Send_BUffer.append(CRC_temp // 256)
                Send_BUffer.append(CRC_temp % 256)  # 校验
                try:
                    self.TCP_SendData(Send_BUffer)
                    time.sleep(0.1)
                    ReceiveData = self.TCP_ReceiveData()
                    if ReceiveData[8] == 0:
                        Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + '升级文件下发第'+str(Upgrade_Struct_Dict['UpgradeFile_Index'])+'....\n'
                        self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])
                        Upgrade_Struct_Dict['UpgradeFile_Index'] = Upgrade_Struct_Dict['UpgradeFile_Index'] + 1
                        Upgrade_Struct_Dict['Step_Count'] = 1
                    else:
                        Upgrade_Struct_Dict['Step_Count'] = Upgrade_Struct_Dict['Step_Count'] + 1
                except:
                    Upgrade_Struct_Dict['Step_Count'] = Upgrade_Struct_Dict['Step_Count'] + 1
                if Upgrade_Struct_Dict['Step_Count'] > 3:
                    Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + '升级文件下发失败....\n'
                    self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])
                    Upgrade_Struct_Dict['Upgrade_Step'] = 6


            elif Upgrade_Struct_Dict['UpgradeFile_Index'] == (Upgrade_Struct_Dict['UpgradeFile_Size'] // 1024 + 1):
                self.progressBar_Upgrade.setValue(100)
                Send_BUffer = [0xAA, 0x55, 0x00, 0x00, 0x00, 0x06, 0x01, 0x02]
                temp = Upgrade_Struct_Dict['UpgradeFile_Index']
                Send_BUffer.append(temp // 256)
                Send_BUffer.append(temp % 256)  # 第几包
                temp2 = Upgrade_Struct_Dict['UpgradeFile_Size'] - Upgrade_Struct_Dict['UpgradeFile_Index'] * 1024 + 1024
                Send_BUffer.append(temp2 // 256)
                Send_BUffer.append(temp2 % 256)  # 多少字节
                temp = Upgrade_Struct_Dict['UpgradeFile_Index'] * 1024 - 1024
                for i in range(temp2):
                    Send_BUffer.append(Upgrade_File[temp + i])
                CRC_temp = self.crc16(Send_BUffer,0, 11 + temp2)
                Send_BUffer.append(CRC_temp // 256)
                Send_BUffer.append(CRC_temp % 256)  # 校验
                try:
                    self.TCP_SendData(Send_BUffer)
                    time.sleep(0.1)
                    ReceiveData = self.TCP_ReceiveData()
                    if ReceiveData[8] == 0:
                        Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + '升级文件下发第'+str(Upgrade_Struct_Dict['UpgradeFile_Index'])+'....\n'
                        self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])
                        Upgrade_Struct_Dict['Upgrade_Step'] = Upgrade_Struct_Dict['Upgrade_Step'] + 1
                        Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + '跳转进入APP....\n'
                        self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])
                        Upgrade_Struct_Dict['Step_Count'] = 1
                    else:
                        Upgrade_Struct_Dict['Step_Count'] = Upgrade_Struct_Dict['Step_Count'] + 1
                except:
                    Upgrade_Struct_Dict['Step_Count'] = Upgrade_Struct_Dict['Step_Count'] + 1
                if Upgrade_Struct_Dict['Step_Count'] > 3:
                    Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + '升级文件下发失败....\n'
                    self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])
                    Upgrade_Struct_Dict['Upgrade_Step'] = 5
        elif Upgrade_Struct_Dict['Upgrade_Step'] == 4:  # 升级标志并发送结束升级
            Send_BUffer = [0xAA, 0x55, 0x00, 0x00, 0x00, 0x06, 0x01, 0x03, 0x00, 0x00, 0x00]
            try:
                self.TCP_SendData(Send_BUffer)
                time.sleep(0.1)
                ReceiveData = self.TCP_ReceiveData()
                Upgrade_Struct_Dict['Upgrade_Step'] = Upgrade_Struct_Dict['Upgrade_Step'] + 1
                Upgrade_Struct_Dict['Step_Count'] = 1
            except:
                Upgrade_Struct_Dict['Step_Count'] = Upgrade_Struct_Dict['Step_Count'] + 1
            Upgrade_Struct_Dict['Step_Count'] = Upgrade_Struct_Dict['Step_Count'] + 1
            if Upgrade_Struct_Dict['Step_Count'] > 6:
                Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + '进入APP通讯失败....\n'
                self.textBrowserUpgradeStates.setText(Upgrade_Struct_Dict['升级状态'])
                Upgrade_Struct_Dict['Upgrade_Step'] = 6
        elif Upgrade_Struct_Dict['Upgrade_Step'] == 5:  # 结束
            if Upgrade_Struct_Dict['Step_Count'] % 2 == 1:  # 100ms发送一次
                try:
                    # BCMU_Addr = self.lineEdit_IPAddr.text()
                    # BCMU_Port = int(self.lineEdit_IPPort.text())
                    # TCP_MODBUS.Connect_Server(BCMU_Addr, BCMU_Port)
                    returnNum = self.Get_APPVersion()  # 检查是否进入APP
                    APPVersion = str(returnNum[9]) + '.' + str(returnNum[10])
                    if APPVersion != '0':
                        self.End_Ugrade(APPVersion)
                    else:
                        i = 0
                except:
                    i = 0
                if Upgrade_Struct_Dict['Step_Count'] > 40:  # 40次尝试，2S
                    Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + '版本号读取失败....\n'
                    self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])
                    self.End_Ugrade('0')
            Upgrade_Struct_Dict['Step_Count'] = Upgrade_Struct_Dict['Step_Count'] + 1
        elif Upgrade_Struct_Dict['Upgrade_Step'] == 6:  # 非正常结束
            try:
                BCMU_Addr = self.lineEdit_IPAddr.text()
                BCMU_Port = int(self.lineEdit_IPPort.text())
                returnNum = self.Connect_Server(BCMU_Addr, BCMU_Port)
                if returnNum == 0:
                    self.End_Ugrade('0')
                else:
                    self.End_Ugrade('0')
                    Upgrade_Struct_Dict['Step_Count'] = Upgrade_Struct_Dict['Step_Count'] + 1
            except:
                i = 0

    def Start_Upgrade():
        global tcp_client_socket
        try:
            Message = [0xAA, 0x55, 0x00, 0x00, 0x00, 0x06, 0x01, 80, 0x01, 0x00, 0x00, 0x00]
            meg = struct.pack("%dB" % (len(Message)), *Message)
            tcp_client_socket.send(meg)
            # # 4.接收服务器返回的消息
            # recv_data = tcp_client_socket.recv(2048)
        except:
            return -1

    def Check_UpgradeFlag():
        global tcp_client_socket
        try:
            Message = [0xAA, 0x55, 0x00, 0x00, 0x00, 0x06, 0x01, 80, 0x17, 0x74, 0x00, 0x01]
            meg = struct.pack("%dB" % (len(Message)), *Message)
            tcp_client_socket.send(meg)
            # 4.接收服务器返回的消息
            recv_data = tcp_client_socket.recv(2048)

            if recv_data[11] == 1:
                return 0
            else:
                return 1
        except:
            return -1

    def Get_APPVersion():
        global tcp_client_socket
        try:
            Message = [0xAA, 0x55, 0x00, 0x00, 0x00, 0x06, 0x01, 0x04, 0x0F, 0xA0, 0x00, 0x01]
            meg = struct.pack("%dB" % (len(Message)), *Message)
            tcp_client_socket.send(meg)
            # 4.接收服务器返回的消息
            recv_data = tcp_client_socket.recv(2048)

            if len(recv_data) > 10:
                return recv_data
            else:
                return '0'
        except:
            return '0'

    def TCP_SendData(Data_Buffer):
        global tcp_client_socket
        try:
            Message = Data_Buffer
            meg = struct.pack("%dB" % (len(Message)), *Message)
            tcp_client_socket.send(meg)
            return 0
        except:
            return -1

    def TCP_ReceiveData():
        global tcp_client_socket

        try:
            recv_data = tcp_client_socket.recv(2048)

            if recv_data:
                return recv_data
            else:
                return -1
        except:
            return -1

    def End_Ugrade(self,APPVersion):
        global Upgrade_Struct_Dict

        if APPVersion == '0':
            Upgrade_Struct_Dict['Start_Flag'] = 0
            Upgrade_Struct_Dict['Upgrade_Step'] = 1
            Upgrade_Struct_Dict['Step_Count'] = 1
            Upgrade_Struct_Dict['UpgradeFile_Index'] = 1
            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态']+'升级失败....\n'
            self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])
        else:
            Upgrade_Struct_Dict['Start_Flag'] = 0
            Upgrade_Struct_Dict['Upgrade_Step'] = 1
            Upgrade_Struct_Dict['Step_Count'] = 1
            Upgrade_Struct_Dict['UpgradeFile_Index'] = 1
            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态']+'升级结束....\n'+'版本号:'+APPVersion+'\n'
            self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])

####################CAN升级/数据升级##########################
    def CAN_Upgrade(self):
        global Upgrade_Struct_Dict
        global UpgradeModule_SendFileIndexList

        if Upgrade_Struct_Dict['Upgrade_Step'] == 0:
            Upgrade_Struct_Dict['Upgrade_Step'] = 1
            Upgrade_Struct_Dict['Step_Count'] = 1
            Upgrade_Struct_Dict['UpgradeFile_Index'] = 0
            Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] = 0
            Upgrade_Struct_Dict['升级状态'] = ''
            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + 'CAN 开始升级....\n'
            for i in range(20):
                UpgradeModule_SendFileIndexList[i] = 0


            if self.checkBox_OneUp.isChecked():
                Upgrade_Struct_Dict['Upgrade_Num'] = 1
            elif self.checkBox_AllUp.isChecked():
                Upgrade_Struct_Dict['Upgrade_Num'] = 2

            self.thread = StoppableThread()
            self.thread.daemon = True
            self.thread.CommIndex_CANUART = 1
            self.thread.start()
        elif Upgrade_Struct_Dict['Upgrade_Step'] ==99:
            self.StopUpgrade()

        temp_value = 0
        temp_Maxvalue = 0
        for i in range(20):
            if UpgradeModule_List[i] == 0:
                temp_value = temp_value + 0
            elif UpgradeModule_List[i] == 1:
                temp_value = temp_value + 0
                temp_Maxvalue = temp_Maxvalue + 100
            elif UpgradeModule_List[i] == 2:
                temp_value = temp_value + 10
                temp_Maxvalue = temp_Maxvalue + 100
            elif UpgradeModule_List[i] == 3:
                temp_value = temp_value + 20+ Upgrade_Struct_Dict['UpgradeFile_Index']/Upgrade_Struct_Dict['UpgradePack_Num'] * 70
                temp_Maxvalue = temp_Maxvalue + 100
            elif UpgradeModule_List[i] == 4:
                temp_value = temp_value + 90
                temp_Maxvalue = temp_Maxvalue + 100
            elif UpgradeModule_List[i] == 5:
                temp_value = temp_value + 100
                temp_Maxvalue = temp_Maxvalue + 100
            elif UpgradeModule_List[i] == 99:
                temp_value = temp_value + 100
                temp_Maxvalue = temp_Maxvalue + 100
        temp_value = temp_value / temp_Maxvalue * 100

        self.CAN_ShowResult(0)
        self.progressBar.setValue(temp_value)
        self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])

    def CAN_UpgradeStop(self):

        Upgrade_Struct_Dict['Upgrade_Step'] = 0
        Upgrade_Struct_Dict['Step_Count'] = 0
        Upgrade_Struct_Dict['UpgradeFile_Index'] = 0
        Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] = 0
        Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + 'CAN 升级结束....\n'
        self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])
        self.thread.terminate()
        CAN_RunTimer.stop()

    def CAN_ShowResult(self,Init_Flag):
        global UpgradeModule_List

        # default (255,255,255) green(0,170,0) red(255,0,0)
        palette_Default = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette_Default.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        palette_Red = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette_Red.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        palette_Green = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette_Green.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        if Init_Flag == 1:
            self.checkBox_Module1.setPalette(palette_Default)
            self.checkBox_Module2.setPalette(palette_Default)
            self.checkBox_Module3.setPalette(palette_Default)
            self.checkBox_Module4.setPalette(palette_Default)
            self.checkBox_Module5.setPalette(palette_Default)
            self.checkBox_Module6.setPalette(palette_Default)
            self.checkBox_Module7.setPalette(palette_Default)
            self.checkBox_Module8.setPalette(palette_Default)
            self.checkBox_Module9.setPalette(palette_Default)
            self.checkBox_Module10.setPalette(palette_Default)
            self.checkBox_Module11.setPalette(palette_Default)
            self.checkBox_Module12.setPalette(palette_Default)
            self.checkBox_Module13.setPalette(palette_Default)
            self.checkBox_Module14.setPalette(palette_Default)
            self.checkBox_Module15.setPalette(palette_Default)
            self.checkBox_Module16.setPalette(palette_Default)
            self.checkBox_Module17.setPalette(palette_Default)
            self.checkBox_Module18.setPalette(palette_Default)
            self.checkBox_Module19.setPalette(palette_Default)
            self.checkBox_Module20.setPalette(palette_Default)
        else:
            if UpgradeModule_List[0] == 5:
                self.checkBox_Module1.setPalette(palette_Green)
            elif UpgradeModule_List[0] == 99:
                self.checkBox_Module1.setPalette(palette_Red)
            if UpgradeModule_List[1] == 5:
                self.checkBox_Module2.setPalette(palette_Green)
            elif UpgradeModule_List[1] == 99:
                self.checkBox_Module2.setPalette(palette_Red)
            if UpgradeModule_List[2] == 5:
                self.checkBox_Module3.setPalette(palette_Green)
            elif UpgradeModule_List[2] == 99:
                self.checkBox_Module3.setPalette(palette_Red)
            if UpgradeModule_List[3] == 5:
                self.checkBox_Module4.setPalette(palette_Green)
            elif UpgradeModule_List[3] == 99:
                self.checkBox_Module4.setPalette(palette_Red)
            if UpgradeModule_List[4] == 5:
                self.checkBox_Module5.setPalette(palette_Green)
            elif UpgradeModule_List[4] == 99:
                self.checkBox_Module5.setPalette(palette_Red)
            if UpgradeModule_List[5] == 5:
                self.checkBox_Module6.setPalette(palette_Green)
            elif UpgradeModule_List[5] == 99:
                self.checkBox_Module6.setPalette(palette_Red)
            if UpgradeModule_List[6] == 5:
                self.checkBox_Module7.setPalette(palette_Green)
            elif UpgradeModule_List[6] == 99:
                self.checkBox_Module7.setPalette(palette_Red)
            if UpgradeModule_List[7] == 5:
                self.checkBox_Module8.setPalette(palette_Green)
            elif UpgradeModule_List[7] == 99:
                self.checkBox_Module8.setPalette(palette_Red)
            if UpgradeModule_List[8] == 5:
                self.checkBox_Module9.setPalette(palette_Green)
            elif UpgradeModule_List[8] == 99:
                self.checkBox_Module9.setPalette(palette_Red)
            if UpgradeModule_List[9] == 5:
                self.checkBox_Module10.setPalette(palette_Green)
            elif UpgradeModule_List[9] == 99:
                self.checkBox_Module10.setPalette(palette_Red)
            if UpgradeModule_List[10] == 5:
                self.checkBox_Module11.setPalette(palette_Green)
            elif UpgradeModule_List[10] == 99:
                self.checkBox_Module11.setPalette(palette_Red)
            if UpgradeModule_List[11] == 5:
                self.checkBox_Module12.setPalette(palette_Green)
            elif UpgradeModule_List[11] == 99:
                self.checkBox_Module12.setPalette(palette_Red)
            if UpgradeModule_List[12] == 5:
                self.checkBox_Module13.setPalette(palette_Green)
            elif UpgradeModule_List[12] == 99:
                self.checkBox_Module13.setPalette(palette_Red)
            if UpgradeModule_List[13] == 5:
                self.checkBox_Module14.setPalette(palette_Green)
            elif UpgradeModule_List[13] == 99:
                self.checkBox_Module14.setPalette(palette_Red)
            if UpgradeModule_List[14] == 5:
                self.checkBox_Module15.setPalette(palette_Green)
            elif UpgradeModule_List[14] == 99:
                self.checkBox_Module15.setPalette(palette_Red)
            if UpgradeModule_List[15] == 5:
                self.checkBox_Module16.setPalette(palette_Green)
            elif UpgradeModule_List[15] == 99:
                self.checkBox_Module16.setPalette(palette_Red)
            if UpgradeModule_List[16] == 5:
                self.checkBox_Module17.setPalette(palette_Green)
            elif UpgradeModule_List[16] == 99:
                self.checkBox_Module17.setPalette(palette_Red)
            if UpgradeModule_List[17] == 5:
                self.checkBox_Module18.setPalette(palette_Green)
            elif UpgradeModule_List[17] == 99:
                self.checkBox_Module18.setPalette(palette_Red)
            if UpgradeModule_List[18] == 5:
                self.checkBox_Module19.setPalette(palette_Green)
            elif UpgradeModule_List[18] == 99:
                self.checkBox_Module19.setPalette(palette_Red)
            if UpgradeModule_List[19] == 5:
                self.checkBox_Module20.setPalette(palette_Green)
            elif UpgradeModule_List[19] == 99:
                self.checkBox_Module20.setPalette(palette_Red)

####################Port升级/数据处理##########################
    def Port_Upgrade(self):
        global Upgrade_Struct_Dict


        if Upgrade_Struct_Dict['Upgrade_Step'] == 0:
            Upgrade_Struct_Dict['Upgrade_Step'] = 1
            Upgrade_Struct_Dict['Step_Count'] = 1
            Upgrade_Struct_Dict['UpgradeFile_Index'] = 0
            Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] = 0
            Upgrade_Struct_Dict['升级状态'] = ''
            Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + 'Uart 开始升级....\n'
            for i in range(20):
                UpgradeModule_SendFileIndexList[i] = 0


            if self.checkBox_OneUp.isChecked():
                Upgrade_Struct_Dict['Upgrade_Num'] = 1
            elif self.checkBox_AllUp.isChecked():
                Upgrade_Struct_Dict['Upgrade_Num'] = 2

            self.thread = StoppableThread()
            self.thread.daemon = True
            self.thread.CommIndex_CANUART = 2
            self.thread.start()
        elif Upgrade_Struct_Dict['Upgrade_Step'] ==99:
            self.StopUpgrade()

        temp_value = 0
        temp_Maxvalue = 0
        for i in range(20):
            if UpgradeModule_List[i] == 0:
                temp_value = temp_value + 0
            elif UpgradeModule_List[i] == 1:
                temp_value = temp_value + 0
                temp_Maxvalue = temp_Maxvalue + 100
            elif UpgradeModule_List[i] == 2:
                temp_value = temp_value + 10
                temp_Maxvalue = temp_Maxvalue + 100
            elif UpgradeModule_List[i] == 3:
                temp_value = temp_value + 20+ Upgrade_Struct_Dict['UpgradeFile_Index']/Upgrade_Struct_Dict['UpgradePack_Num'] * 70
                temp_Maxvalue = temp_Maxvalue + 100
            elif UpgradeModule_List[i] == 4:
                temp_value = temp_value + 90
                temp_Maxvalue = temp_Maxvalue + 100
            elif UpgradeModule_List[i] == 5:
                temp_value = temp_value + 100
                temp_Maxvalue = temp_Maxvalue + 100
            elif UpgradeModule_List[i] == 99:
                temp_value = temp_value + 100
                temp_Maxvalue = temp_Maxvalue + 100
        temp_value = temp_value / temp_Maxvalue * 100

        self.CAN_ShowResult(0)
        self.progressBar.setValue(temp_value)
        self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])

    def Port_UpgradeStop(self):
        Upgrade_Struct_Dict['Upgrade_Step'] = 0
        Upgrade_Struct_Dict['Step_Count'] = 0
        Upgrade_Struct_Dict['UpgradeFile_Index'] = 0
        Upgrade_Struct_Dict['UpgradeFile_PaintIndx'] = 0
        Upgrade_Struct_Dict['升级状态'] = Upgrade_Struct_Dict['升级状态'] + 'Uart 升级结束....\n'
        self.textBrowser_UpgradeRecord.setText(Upgrade_Struct_Dict['升级状态'])
        self.thread.terminate()
        Port_RunTimer.stop()


####################界面解释##########################
    def retranslateUi(self, Upgrade_Tool):
        _translate = QtCore.QCoreApplication.translate
        Upgrade_Tool.setWindowTitle(_translate("Upgrade_Tool", "MainWindow"))
        self.label_TCP.setText(_translate("Upgrade_Tool", "TCP链接"))
        self.label_IPPort.setText(_translate("Upgrade_Tool", "BCMU_端口"))
        self.lineEdit_IPAddr.setText(_translate("Upgrade_Tool", "192.168.1.100"))
        self.lineEdit_IPPort.setText(_translate("Upgrade_Tool", "6001"))
        self.label_IPAddr.setText(_translate("Upgrade_Tool", "BCMU_IP地址"))
        self.pushButton_TCPConnect.setText(_translate("Upgrade_Tool", "连接"))
        self.label_UART.setText(_translate("Upgrade_Tool", "UART链接"))
        self.pushButton_UARTConnect.setText(_translate("Upgrade_Tool", "连接"))
        self.pushButton_CheckPort.setText(_translate("Upgrade_Tool", "检查可用串口"))
        self.comboBox_Port.setItemText(0, _translate("Upgrade_Tool", "COM1"))
        self.comboBox_Port.setItemText(1, _translate("Upgrade_Tool", "COM2"))
        self.comboBox_Port.setItemText(2, _translate("Upgrade_Tool", "COM3"))
        self.comboBox_Port.setItemText(3, _translate("Upgrade_Tool", "COM4"))
        self.comboBox_Port.setItemText(4, _translate("Upgrade_Tool", "COM5"))
        self.comboBox_Port.setItemText(5, _translate("Upgrade_Tool", "COM6"))
        self.comboBox_Port.setItemText(6, _translate("Upgrade_Tool", "COM7"))
        self.comboBox_Port.setItemText(7, _translate("Upgrade_Tool", "COM8"))
        self.comboBox_Port.setItemText(8, _translate("Upgrade_Tool", "COM9"))
        self.comboBox_Port.setItemText(9, _translate("Upgrade_Tool", "COM10"))
        self.comboBox_Port.setItemText(10, _translate("Upgrade_Tool", "COM11"))
        self.comboBox_Port.setItemText(11, _translate("Upgrade_Tool", "COM12"))
        self.comboBox_Port.setItemText(12, _translate("Upgrade_Tool", "COM13"))
        self.comboBox_Port.setItemText(13, _translate("Upgrade_Tool", "COM14"))
        self.comboBox_Port.setItemText(14, _translate("Upgrade_Tool", "COM15"))
        self.comboBox_StopBit.setItemText(0, _translate("Upgrade_Tool", "1"))
        self.comboBox_StopBit.setItemText(1, _translate("Upgrade_Tool", "2"))
        self.label_PortSelect.setText(_translate("Upgrade_Tool", "串口选择："))
        self.comboBox_BoundRate.setItemText(0, _translate("Upgrade_Tool", "9600"))
        self.comboBox_BoundRate.setItemText(1, _translate("Upgrade_Tool", "19200"))
        self.comboBox_BoundRate.setItemText(2, _translate("Upgrade_Tool", "115200"))
        self.comboBox_CRCBit.setItemText(0, _translate("Upgrade_Tool", "NONE"))
        self.comboBox_CRCBit.setItemText(1, _translate("Upgrade_Tool", "EVEN"))
        self.comboBox_CRCBit.setItemText(2, _translate("Upgrade_Tool", "ODD"))
        self.comboBox_CRCBit.setItemText(3, _translate("Upgrade_Tool", "MARK"))
        self.comboBox_CRCBit.setItemText(4, _translate("Upgrade_Tool", "SPACE"))
        self.label_BoundRate.setText(_translate("Upgrade_Tool", "波特率："))
        self.label_Bit.setText(_translate("Upgrade_Tool", "数据位："))
        self.label_CRCBit.setText(_translate("Upgrade_Tool", "检验位"))
        self.label_StopBit.setText(_translate("Upgrade_Tool", "停止位："))
        self.comboBox_Bit.setItemText(0, _translate("Upgrade_Tool", "8"))
        self.comboBox_Bit.setItemText(1, _translate("Upgrade_Tool", "8.5"))
        self.comboBox_Bit.setItemText(2, _translate("Upgrade_Tool", "9"))
        self.label_CAN.setText(_translate("Upgrade_Tool", "CAN链接"))
        self.pushButton_CANConnect.setText(_translate("Upgrade_Tool", "连接"))
        self.comboBox_CANDevice.setItemText(0, _translate("Upgrade_Tool", "USBCAN2"))
        self.comboBox_CANDevice.setItemText(1, _translate("Upgrade_Tool", "USBCAN1"))
        self.comboBox_CANBoundRate.setItemText(0, _translate("Upgrade_Tool", "10Kbps"))
        self.comboBox_CANBoundRate.setItemText(1, _translate("Upgrade_Tool", "50Kbps"))
        self.comboBox_CANBoundRate.setItemText(2, _translate("Upgrade_Tool", "100Kbps"))
        self.comboBox_CANBoundRate.setItemText(3, _translate("Upgrade_Tool", "125Kbps"))
        self.comboBox_CANBoundRate.setItemText(4, _translate("Upgrade_Tool", "200Kbps"))
        self.comboBox_CANBoundRate.setItemText(5, _translate("Upgrade_Tool", "250Kbps"))
        self.comboBox_CANBoundRate.setItemText(6, _translate("Upgrade_Tool", "500Kbps"))
        self.comboBox_CANBoundRate.setItemText(7, _translate("Upgrade_Tool", "1000Kbps"))
        self.label_CANChannel.setText(_translate("Upgrade_Tool", "通道号"))
        self.comboBox_CANChannel.setItemText(0, _translate("Upgrade_Tool", "0"))
        self.comboBox_CANChannel.setItemText(1, _translate("Upgrade_Tool", "1"))
        self.label_CANBoundRate.setText(_translate("Upgrade_Tool", "波特率"))
        self.comboBox_CANIndex.setItemText(0, _translate("Upgrade_Tool", "0"))
        self.comboBox_CANIndex.setItemText(1, _translate("Upgrade_Tool", "1"))
        self.comboBox_CANIndex.setItemText(2, _translate("Upgrade_Tool", "2"))
        self.comboBox_CANIndex.setItemText(3, _translate("Upgrade_Tool", "3"))
        self.comboBox_CANIndex.setItemText(4, _translate("Upgrade_Tool", "4"))
        self.comboBox_CANIndex.setItemText(5, _translate("Upgrade_Tool", "5"))
        self.comboBox_CANIndex.setItemText(6, _translate("Upgrade_Tool", "6"))
        self.comboBox_CANIndex.setItemText(7, _translate("Upgrade_Tool", "7"))
        self.label_CANDevice.setText(_translate("Upgrade_Tool", "CAN设备"))
        self.label_CANIndex.setText(_translate("Upgrade_Tool", "设备索引号"))
        self.label_FileVersion.setText(_translate("Upgrade_Tool", "文件版本："))
        self.checkBox_Module5.setText(_translate("Upgrade_Tool", "5号模块"))
        self.checkBox_Module20.setText(_translate("Upgrade_Tool", "20号模块"))
        self.label_FileSize.setText(_translate("Upgrade_Tool", "文件大小："))
        self.checkBox_Module17.setText(_translate("Upgrade_Tool", "17号模块"))
        self.checkBox_Module16.setText(_translate("Upgrade_Tool", "16号模块"))
        self.label_Load.setText(_translate("Upgrade_Tool", "升级文件路径："))
        self.checkBox_Module18.setText(_translate("Upgrade_Tool", "18号模块"))
        self.checkBox_Module9.setText(_translate("Upgrade_Tool", "9号模块"))
        self.checkBox_AllUp.setText(_translate("Upgrade_Tool", "全部升级"))
        self.pushButton_StartUpgrade.setText(_translate("Upgrade_Tool", "开始升级"))
        self.checkBox_Module3.setText(_translate("Upgrade_Tool", "3号模块"))
        self.checkBox_Module11.setText(_translate("Upgrade_Tool", "11号模块"))
        self.checkBox_SelectAll.setText(_translate("Upgrade_Tool", "全选"))
        self.checkBox_Module10.setText(_translate("Upgrade_Tool", "10号模块"))
        self.checkBox_Module12.setText(_translate("Upgrade_Tool", "12号模块"))
        self.label_FileCRC.setText(_translate("Upgrade_Tool", "文件CRC校验："))
        self.checkBox_Module7.setText(_translate("Upgrade_Tool", "7号模块"))
        self.checkBox_Module13.setText(_translate("Upgrade_Tool", "13号模块"))
        self.checkBox_Module8.setText(_translate("Upgrade_Tool", "8号模块"))
        self.comboBox_SelcectZC.setItemText(0, _translate("Upgrade_Tool", "主控BCMU"))
        self.comboBox_SelcectZC.setItemText(1, _translate("Upgrade_Tool", "从控BMU"))
        self.checkBox_Module19.setText(_translate("Upgrade_Tool", "19号模块"))
        self.checkBox_Module4.setText(_translate("Upgrade_Tool", "4号模块"))
        self.pushButton_OpenFile.setText(_translate("Upgrade_Tool", "打开升级文件"))
        self.checkBox_Module2.setText(_translate("Upgrade_Tool", "2号模块"))
        self.checkBox_Module6.setText(_translate("Upgrade_Tool", "6号模块"))
        self.checkBox_Module15.setText(_translate("Upgrade_Tool", "15号模块"))
        self.checkBox_OneUp.setText(_translate("Upgrade_Tool", "单机升级"))
        self.checkBox_Module14.setText(_translate("Upgrade_Tool", "14号模块"))
        self.checkBox_Module1.setText(_translate("Upgrade_Tool", "1号模块"))
        self.pushButton_SaveRecord.setText(_translate("Upgrade_Tool", "保存日志"))
        self.textBrowser_UpgradeRecord.setHtml(_translate("Upgrade_Tool", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">日志：</p></body></html>"))
        self.label_CommInfo.setText(_translate("Upgrade_Tool", "通讯设备信息：未打开"))
        self.actionCAN_Open.setText(_translate("Upgrade_Tool", "CAN_Open"))
        self.actionUART_Open.setText(_translate("Upgrade_Tool", "UART_Open"))
        self.actionTCP_Open.setText(_translate("Upgrade_Tool", "TCP_Open"))

class Main(QMainWindow, Ui_Upgrade_Tool):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)

if __name__ == "__main__":
    COM_Status = 0
    app = QApplication(sys.argv)
    MainWindows = Main()

    MainWindows.show()

    sys.exit(app.exec_())
