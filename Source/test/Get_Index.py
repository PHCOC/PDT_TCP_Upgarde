# -*- coding:utf-8 -*-
#version 1.01

import csv
import re
import codecs
import xlwt
import os
import sys


# num_list = ['CM', 'cm', 'g', '克', 'kg', '千克', 'ml', 'mL', '毫升', 'L', '斤', '块',
#            '块装', '抽', '抽装', '盒', '盒装', '册', '册装', '件装', '件套', '包',
#            '包装', '双', '双装', '袋', '袋装', '条', '条装', '支', '支装', '杯',
#            '杯装',  '瓶', '瓶装', '支', '支装', '罐', '罐装', '片', '片装', '粒',
#            '岁', 'm', '个月', '月','粒/瓶']
num_list = ['CM', 'g', '克', 'kg', '千克', 'ml/瓶|ml|cm|mL|m', '毫升', 'L', '斤', '块装|块',
            '抽装|抽', '盒装|盒', '册装|册', '件装', '件套', '包装|包', '个月|月','岁',
            '双装|双', '袋装|袋', '条装|条', '支装|支', '杯装|杯',  '瓶装|粒/瓶|瓶|粒', '罐装|罐', '片装|片'
            ]
num_temp = 'CM|g|克|kg|千克|ml|cm|mL|m|毫升|L|斤|块装|块|抽装|抽|盒装|盒|册装|册|件装|件套|包装|包|个月|月|岁|双装|双|' \
           '袋装|袋|条装|条|支装|支|杯装|杯|瓶装|粒/瓶|瓶|粒|罐装|罐|片装|片|ml/瓶'

num_num = len(num_list)
Data_Buffer = ['' for i in range(10)]

csv_data = csv.reader(open('item_inf.csv'))
book = xlwt.Workbook(encoding='utf-8')
sheet = book.add_sheet('1')

# def Regular_Match(Input_Str):
#     Cycle_Cnt = 0
#     for i in range(num_num):
#         Regular = ''
#         Regular = r'([0-9]*)(-*)(~*)(\.*)([0-9]+)('+num_list[i] + r')+(\+|\*)*([0-9]*)('+num_temp+r')*'
#         pattern = re.compile(Regular,re.S)
#         items = re.findall(pattern, Input_Str)
#         for item in items:
#             temp = (len(item))
#             TempIndex = ''
#             for j in range(temp):
#                 Data_Buffer[Cycle_Cnt] =  Data_Buffer[Cycle_Cnt] + item[j]
#             Cycle_Cnt = Cycle_Cnt + 1
#     return Data_Buffer
#
#
#
# print(Regular_Match('欣兰黑里透白冻膜 225g / 净透洗颜乳 80g'))

Cycle_Cnt = 0

def Type_Match(Input_Str,Second_Name):
    TempK = 0
    Input_Str = Input_Str.replace('系列','Xilie')
    # csv_item[0] = csv_item[0].replace('\'','l')
    # csv_item[0] = csv_item[0].replace('&','a')
    # csv_item[0] = csv_item[0].replace('\.','a')
    # Index = r'([^\x00-\xff]+)系列'
    # pattern = re.compile(Index,re.S)
    # items = re.findall(pattern, csv_item[0])
    # if len(items)>0:
    #
    Index = r'服饰'
    pattern = re.compile(Index,re.S)
    items = re.findall(pattern, Second_Name)

    if len(items) < 1:
        return False

    Index = r'([^\x00-\xff]+)'
    pattern = re.compile(Index,re.S)
    items = re.findall(pattern, Input_Str)
    for item in items:
        temp = (len(item))
        TempIndex = ''
        for j in range(temp):
            Input_Str = Input_Str.replace(item[j],' ')

    Index = r'(*+[0-9]*)'
    pattern = re.compile(Index,re.S)
    items = re.findall(pattern, Input_Str)
    for item in items:
        temp = (len(item))
        TempIndex = ''
        for j in range(temp):
            Input_Str = Input_Str.replace(item[j],' ')

    Index = r'\s+(\S+)\s?'
    pattern = re.compile(Index,re.S)
    items = re.findall(pattern, Input_Str)
    for item in items:
        TempIndex = ''
        if item.isalpha():
            dfg = 0
        else:
            if len(item) > 3:
                return item



# Cycle_Cnt = 0
# for csv_item in csv_data:
#     TempK = 0
#     sheet.write(Cycle_Cnt,0,csv_item[0])
#     for i in range(num_num):
#         Index = ''
#         Index = r'([0-9]*)(-*)(~*)(\.*)([0-9]+)('+num_list[i] + r')+(\+|\*)*([0-9]*)('+num_temp+r')*'
#         pattern = re.compile(Index,re.S)
#         items = re.findall(pattern, csv_item[0])
#         for item in items:
#             temp = (len(item))
#             TempIndex = ''
#             for j in range(temp):
#                 TempIndex = TempIndex + item[j]
#             sheet.write(Cycle_Cnt,TempK+1,TempIndex)
#             TempK = TempK +1
#     Cycle_Cnt = Cycle_Cnt + 1
# book.save(".\Index.xls")
#
# exit()