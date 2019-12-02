# -*- coding:utf-8 -*-\
import sys

Standard_Dict =[
    # '总电压L':
        35500,
    # '总电压H':
        36500,
    # '单体电压L':
        3500,
    # '单体电压H':
        3700,
    # '单体温度L':
        10,
    # '单体温度H':
        40,
    # 'SOCL':
        10,
    # 'SOCH':
        30,
    # '满充容量L':
        9000,
    # '满充容量H':
        11000,
    # '剩余容量L':
        1000,
    # '剩余容量H':
        3000,
    # '电流L':
        -30,
    # '电流H':
        20,
    # '版本号':
        1117
]

def Standard_Dict_Read(Num):
    return Standard_Dict[Num]

def Standard_Dict_Write(Num,Write_Data):
    Standard_Dict[Num] = Write_Data


Password = 'DLG1025'
