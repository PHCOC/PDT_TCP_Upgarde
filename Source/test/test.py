# -*- coding: UTF-8 -*-
#__author__="chenhong"

import time
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
# from scipy.interpolate import spline
#这个程序的实质就是在前九秒保持零输出，在后面的操作中在传递函数为某某的系统中输出1

class PID:
    def __init__(self, P=0.2, I=0.0, D=0.0):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time
        self.clear()
    def clear(self):
        self.SetPoint = 0.0
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.int_error = 0.0
        self.windup_guard = 20.0
        self.output = 0.0
    def update(self, feedback_value):
        error = self.SetPoint - feedback_value
        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error
        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error#比例
            self.ITerm = error + self.last_error + self.int_error#积分
            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard
            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error
            self.output = self.Kp*(error - self.last_error) + self.Ki*(error) + self.Kd*(error - 2*self.last_error + self.int_error)
            self.last_time = self.current_time
            self.last_error = error
            self.int_error = self.last_error
            # self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)
    def setKp(self, proportional_gain):
        self.Kp = proportional_gain
    def setKi(self, integral_gain):
        self.Ki = integral_gain
    def setKd(self, derivative_gain):
        self.Kd = derivative_gain
    def setWindup(self, windup):
        self.windup_guard = windup
    def setSampleTime(self, sample_time):
        self.sample_time = sample_time

def test_pid(P = 0.2,  I = 0.0, D= 0.0, L=100):
    """Self-test PID class

    .. note::
        ...
        for i in range(1, END):
            pid.update(feedback)
            output = pid.output
            if pid.SetPoint > 0:
                feedback += (output - (1/i))
            if i>9:
                pid.SetPoint = 1
            time.sleep(0.02)
        ---
    """
    pid = PID(P, I, D)

    pid.SetPoint=0.0
    pid.setSampleTime(0.01)

    END = L
    feedback = 0

    feedback_list = []
    time_list = []
    setpoint_list = []

    for i in range(1, END):
        pid.update(feedback)
        output = pid.output
        if pid.SetPoint > 0:
            feedback +=output# (output - (1/i))控制系统的函数
        if i>9:
            pid.SetPoint = 10
        time.sleep(0.01)

        feedback_list.append(feedback)
        setpoint_list.append(pid.SetPoint)
        time_list.append(i)

    # time_sm = np.array(time_list)
    # time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)
    # feedback_smooth = spline(time_list, feedback_list, time_smooth)
    plt.figure(0)
    # plt.plot(time_smooth, feedback_smooth)
    plt.plot(time_list, feedback_list)

    plt.plot(time_list, setpoint_list)
    plt.xlim((0, L))
    plt.ylim((min(feedback_list)-0.5, max(feedback_list)+0.5))
    plt.xlabel('time (s)')
    plt.ylabel('PID (PV)')
    plt.title('TEST PID')

    plt.ylim((0, 15))

    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    test_pid(0.1, 0.4, 0.1, L=40)
#    test_pid(0.8, L=50)




# from ctypes import *
#
# import threading
# import time
# import os # 原本需要用来启动的无线循环的函数
# def print_thread():
#     pid = os.getpid()
#     counts = 0
#
#     canLib = windll.LoadLibrary('./ControlCAN.dll')
#     vco = _VCI_CAN_OBJ()
#     vco.ID = 0x18000102
#     vco.SendType = 0
#     vco.RemoteFlag = 0
#     vco.ExternFlag = 1
#     vco.DataLen = 8
#     vco.Data = (1, 2, 3, 4, 5, 6, 7, 8)
#     print('发送: %d' % (canLib.VCI_Transmit(4, 0, 0, pointer(vco), 1)))
#
#
# class _VCI_INIT_CONFIG(Structure):
#     _fields_ = [('AccCode', c_ulong),
#                 ('AccMask', c_ulong),
#                 ('Reserved', c_ulong),
#                 ('Filter', c_ubyte),
#                 ('Timing0', c_ubyte),
#                 ('Timing1', c_ubyte),
#                 ('Mode', c_ubyte)]
#
#
# class _VCI_CAN_OBJ(Structure):
#     _fields_ = [('ID', c_uint),
#                 ('TimeStamp', c_uint),
#                 ('TimeFlag', c_byte),
#                 ('SendType', c_byte),
#                 ('RemoteFlag', c_byte),
#                 ('ExternFlag', c_byte),
#                 ('DataLen', c_byte),
#                 ('Data', c_byte*8),
#                 ('Reserved', c_byte*3)]
#
# def Gloabl_CAN_Init():
#     vic = _VCI_INIT_CONFIG()
#     vic.AccCode = 0x00000000
#     vic.AccMask = 0xffffffff
#     vic.Filter = 0
#     vic.Timing0 = 0x01
#     vic.Timing1 = 0x1c
#     vic.Mode = 0
#
#     canLib = windll.LoadLibrary('.\ControlCAN.dll')
#     print('打开设备: %d' % (canLib.VCI_OpenDevice(4, 0, 0)))
#     print('初始化: %d' % (canLib.VCI_InitCAN(4, 0, 0, pointer(vic))))
#     print('启动: %d' % (canLib.VCI_StartCAN(4, 0, 0)))
#
#
# import threading
# import time
# import os # 原本需要用来启动的无线循环的函数
# # def print_thread():
# #     pid = os.getpid()
# #     counts = 0
# #     while True:
# #         print(f'threading pid: {pid} ran: {counts:04d} s')
# #         counts += 1
# #         time.sleep(1)
# # 把函数放到改写到类的run方法中，便可以通过调用类方法，实现线程的终止
#
# class ehh():
#     def call_thread(self):
#         Gloabl_CAN_Init()
#
#         thread = StoppableThread(self)
#         thread.daemon = True
#         thread.start()
#         pid = os.getpid()
#         counts = 0
#         for i in range(5):
#             print(f'0 call threading pid: {pid} ran: {counts:04d} s')
#             counts += 2
#             time.sleep(2)
#         # 主动把线程退出
#         thread.terminate()
# class StoppableThread(threading.Thread,ehh):
#     def __init__(self, daemon=None):
#         super(StoppableThread, self).__init__(daemon=daemon)
#         self.__is_running = True
#         self.daemon = daemon
#     def terminate(self):
#         self.__is_running = False
#     def run(self):
#         pid = os.getpid()
#         counts = 0
#         while self.__is_running:
#             print(f'threading running: {pid} ran: {counts:04d} s')
#             canLib = windll.LoadLibrary('./ControlCAN.dll')
#             vco = _VCI_CAN_OBJ()
#             vco.ID = 0x18000102
#             vco.SendType = 0
#             vco.RemoteFlag = 0
#             vco.ExternFlag = 1
#             vco.DataLen = 8
#             vco.Data = (1, 2, 3, 4, 5, 6, 7, 8)
#             print( (canLib.VCI_Transmit(4, 0, 0, pointer(vco), 1)))
#             counts += 1
#             time.sleep(1)
#
# if __name__ == '__main__':
#     ehh2 = ehh()
#     ehh2.call_thread()
#     print(f'==========call_thread finish===========')
#     counts = 0
#     for i in range(5):
#         counts += 1
#         time.sleep(1)
#         print(f'main thread:{counts:04d} s')

# import random
#
# # recomm = [50.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0,500.0]
# recom2 = [50.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0,500.0]
# recomm = [600.0, 600.0, 650.0, 700.0, 750.0, 800.0, 850.0, 900.0, 950.0,960.0]
# # recomm = [960, 950, 900, 850, 800, 750, 700, 650, 600,550]
# # for i in range(9):
# #     recomm[i] = random.randint(0,1000)
#
# AVG = recomm[0]
# for i in range(10):
#     recomm[i] = recomm[i]
#     AVG = (AVG+recomm[i])
# AVG = AVG / 10
# print(AVG)
#
# temp = 0
# for i in range(10):
#     recom2[i] = recomm[i] - AVG
#     temp = temp + abs(recom2[i])
# for i in range(10):
#     recom2[i] = recom2[i] * abs(recom2[i] / temp)
# MSOC = AVG
# for i in range(10):
#     MSOC = MSOC + recom2[i]
# print(MSOC)
#
# temp = recomm[0]
# MSOC = recomm[0]
# for i in range(10):
#     MSOC = AVG/MSOC+(1-AVG/1000)*recomm[i]
#     # temp = (MSOC+recomm[i])/2
#     # if recomm[i] > 500:
#     #     MSOC =  recomm[i] / 1000 * recomm[i] + (1 - recomm[i] / 1000) * MSOC
#     # else:
#     #     MSOC =  recomm[i] / 2 / 1000 * recomm[i] + (1 - recomm[i] / 2 / 1000) * MSOC
#
# print(recomm)
# print(MSOC)

# recomm2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# cat_dict2 = {1: 'A', 2: 'B', 3: 'B', 4: 'C', 5: 'C', 6: 'A', 7: 'B', 8: 'A', 9: 'A', 10: 'A', 11: 'D', 12: "B"}
#
# recomm = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# cat_dict = {1: 'A', 2: 'B', 3: 'B', 4: 'C', 5: 'C', 6: 'A', 7: 'B', 8: 'A', 9: 'A', 10: 'A', 11: 'D', 12: "B"}
#
# try:
#     windows_len = input("输入窗口长度：")
#     windows_len = int(windows_len)-1
#     if windows_len > len(cat_dict):
#         print("窗口超长度")
# except:
#     print("输入非数字")
#     exit()
#
# cat_dict_len = len(cat_dict)
# new_dict = {}
# new_recomm = [0 for i in range(cat_dict_len)]
# list_newdict = [0 for i in range(windows_len)]
# search_list = 1
# new_dict.update({recomm[0]: cat_dict[recomm[0]]})
# new_recomm[0] = recomm[0]
# cat_dict.pop(recomm[0])
# recomm.remove(recomm[0])
#
# for i in range(len(cat_dict)):
#     if search_list <= windows_len:
#         for j in range(search_list):
#             list_newdict[j] = new_dict[new_recomm[j]]
#         for j in range(len(cat_dict)):
#             if cat_dict[recomm[j]] in list_newdict:
#                 if j == (len(cat_dict)-1):
#                     new_dict.update({recomm[0]: cat_dict[recomm[0]]})
#                     new_recomm[search_list] = recomm[0]
#                     cat_dict.pop(recomm[0])
#                     recomm.remove(recomm[0])
#                     break
#             else:
#                 new_dict.update({recomm[j]: cat_dict[recomm[j]]})
#                 new_recomm[search_list] = recomm[j]
#                 cat_dict.pop(recomm[j])
#                 recomm.remove(recomm[j])
#                 break
#     else:
#         for j in range(windows_len):
#             list_newdict[j] = new_dict[new_recomm[i+1-windows_len+j]]
#         for j in range(len(cat_dict)):
#             if cat_dict[recomm[j]] in list_newdict:
#                 if j == (len(cat_dict)-1):
#                     new_dict.update({recomm[0]: cat_dict[recomm[0]]})
#                     new_recomm[search_list] = recomm[0]
#                     cat_dict.pop(recomm[0])
#                     recomm.remove(recomm[0])
#                     break
#             else:
#                 new_dict.update({recomm[j]: cat_dict[recomm[j]]})
#                 new_recomm[search_list] = recomm[j]
#                 cat_dict.pop(recomm[j])
#                 recomm.remove(recomm[j])
#                 break
#
#     search_list += 1
#
# print  new_recomm
# print  new_dict


# # -*- coding: utf-8 -*-
#
# import numpy as np
# from matplotlib import pyplot as plt
# from matplotlib import animation
#
# # path = "Nccut_TraceFile.log"
# # file = open(path, 'r')
#
# AMat = []
# BMat = []
# XMat = []
# YMat = []
# ZMat = []
#
# # for line in file.readlines():
# #     lineArr = line.strip().split()
# #     AMat.append(int(lineArr[0]))
# #     BMat.append(int(lineArr[1]))
# #     XMat.append(int(lineArr[2]))
# #     YMat.append(int(lineArr[3]))
# #     ZMat.append(int(lineArr[4]))
#
# fig = plt.figure()
# axA = fig.add_subplot(5, 1, 1, xlim=(0, 0.2), ylim=(0, 40))
# axB = fig.add_subplot(5, 1, 2, xlim=(0, 0.2), ylim=(0, 40))
# axX = fig.add_subplot(5, 1, 3, xlim=(0, 0.2), ylim=(0, 200))
# axY = fig.add_subplot(5, 1, 4, xlim=(0, 0.2), ylim=(0, 200))
# axZ = fig.add_subplot(5, 1, 5, xlim=(0, 0.2), ylim=(0, 200))
#
# lineA, = axA.plot([], [], lw=1)
# lineB, = axB.plot([], [], lw=1)
# lineX, = axX.plot([], [], lw=1)
# lineY, = axY.plot([], [], lw=1)
# lineZ, = axZ.plot([], [], lw=1)
#
#
# def init():
#     lineA.set_data([], [])
#     lineB.set_data([], [])
#     lineX.set_data([], [])
#     lineY.set_data([], [])
#     lineZ.set_data([], [])
#     return lineA, lineB, lineX, lineY, lineZ
#
#
# def animate(i):
#     t = np.linspace(0, 0.2, 10)
#     yA = AMat[i:10 + i]
#     lineA.set_data(t, yA)
#
#     yB = BMat[i:10 + i]
#     lineB.set_data(t, yB)
#
#     yX = XMat[i:10 + i]
#     lineX.set_data(t, yX)
#
#     yY = YMat[i:10 + i]
#     lineY.set_data(t, yY)
#
#     yZ = ZMat[i:10 + i]
#     lineZ.set_data(t, yZ)
#
#     return lineA, lineB, lineX, lineY, lineZ
#
#
# anim1 = animation.FuncAnimation(fig, animate, init_func=init, frames=len(XMat) - 10, interval=2)
