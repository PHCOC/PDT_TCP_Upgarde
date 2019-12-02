# -*- coding:utf-8 -*-
import array

ArrayNum = 300

_1S_Count = 0
_5S_Count = 0
_10S_Count = 0
_30S_Count = 0
Current_Buffer_1S = array.array('i')
Current_Buffer_5S = array.array('i')
Current_Buffer_10S = array.array('i')
Current_Buffer_30S = array.array('i')

SOC_Buffer_1S = array.array('i')
SOC_Buffer_5S = array.array('i')
SOC_Buffer_10S = array.array('i')
SOC_Buffer_30S = array.array('i')

Voltage_Buffer_1S = array.array('i')
Voltage_Buffer_5S = array.array('i')
Voltage_Buffer_10S = array.array('i')
Voltage_Buffer_30S = array.array('i')


def Add_Data_To_Buffer(Current_Data,SOC_Data,Voltage_Data,Time):
    global _1S_Count
    global _5S_Count
    global _10S_Count
    global _30S_Count

    _1S_Count += Time
    _5S_Count += Time
    _10S_Count += Time
    _30S_Count += Time

    if Current_Data > 327680:
        Current_Data = Current_Data - 655360
        # Current_Data = -1000
    SOC_Data = int(SOC_Data / 10)
    Voltage_Data = int(Voltage_Data / 10)

    if _1S_Count >= 1000:
        _1S_Count = 0
        if len(Current_Buffer_1S) < ArrayNum:
            Current_Buffer_1S.append(Current_Data)
            SOC_Buffer_1S.append(SOC_Data)
            Voltage_Buffer_1S.append(Voltage_Data)
        else:
            Current_Buffer_1S[:-1] = Current_Buffer_1S[1:]
            Current_Buffer_1S[-1] = Current_Data
            SOC_Buffer_1S[:-1] = SOC_Buffer_1S[1:]
            SOC_Buffer_1S[-1] = SOC_Data
            Voltage_Buffer_1S[:-1] = Voltage_Buffer_1S[1:]
            Voltage_Buffer_1S[-1] = Voltage_Data

    if _5S_Count >= 5000:
        _5S_Count = 0
        if len(Current_Buffer_5S) < ArrayNum:
            Current_Buffer_5S.append(Current_Data)
            SOC_Buffer_5S.append(SOC_Data)
            Voltage_Buffer_5S.append(Voltage_Data)
        else:
            Current_Buffer_5S[:-1] = Current_Buffer_5S[1:]
            Current_Buffer_5S[-1] = Current_Data
            SOC_Buffer_5S[:-1] = SOC_Buffer_5S[1:]
            SOC_Buffer_5S[-1] = SOC_Data
            Voltage_Buffer_5S[:-1] = Voltage_Buffer_5S[1:]
            Voltage_Buffer_5S[-1] = Voltage_Data


    if _10S_Count >= 10000:
        _10S_Count = 0
        if len(Current_Buffer_10S) < ArrayNum:
            Current_Buffer_10S.append(Current_Data)
            SOC_Buffer_10S.append(SOC_Data)
            Voltage_Buffer_10S.append(Voltage_Data)
        else:
            Current_Buffer_10S[:-1] = Current_Buffer_10S[1:]
            Current_Buffer_10S[-1] = Current_Data
            SOC_Buffer_10S[:-1] = SOC_Buffer_10S[1:]
            SOC_Buffer_10S[-1] = SOC_Data
            Voltage_Buffer_10S[:-1] = Voltage_Buffer_10S[1:]
            Voltage_Buffer_10S[-1] = Voltage_Data

    if _30S_Count >= 30000:
        _30S_Count = 0
        if len(Current_Buffer_30S) < ArrayNum:
            Current_Buffer_30S.append(Current_Data)
            SOC_Buffer_30S.append(SOC_Data)
            Voltage_Buffer_30S.append(Voltage_Data)
        else:
            Current_Buffer_30S[:-1] = Current_Buffer_30S[1:]
            Current_Buffer_30S[-1] = Current_Data
            SOC_Buffer_30S[:-1] = SOC_Buffer_30S[1:]
            SOC_Buffer_30S[-1] = SOC_Data
            Voltage_Buffer_30S[:-1] = Voltage_Buffer_30S[1:]
            Voltage_Buffer_30S[-1] = Voltage_Data



def Read_Data(Index,Timer):
    if Timer == 1:
        if Index == 1:
            return Current_Buffer_1S
        if Index == 2:
            return SOC_Buffer_1S
        if Index == 3:
            return Voltage_Buffer_1S
    if Timer == 5:
        if Index == 1:
            return Current_Buffer_5S
        if Index == 2:
            return SOC_Buffer_5S
        if Index == 3:
            return Voltage_Buffer_5S
    if Timer == 10:
        if Index == 1:
            return Current_Buffer_10S
        if Index == 2:
            return SOC_Buffer_10S
        if Index == 3:
            return Voltage_Buffer_10S
    if Timer == 30:
        if Index == 1:
            return Current_Buffer_30S
        if Index == 2:
            return SOC_Buffer_30S
        if Index == 3:
            return Voltage_Buffer_30S