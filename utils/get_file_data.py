# -*- coding: utf-8 -*-
# @desc    :
# @version :python3.6
# @Time    :2022/7/4 11:17
# @Author  : zjl
import os
import pandas as pd
pd.set_option('display.max_columns', None)


def GetExcelData():
    """
    获取数据源,扫描当前目录下后缀名为xlsx的文件
    :return:excel文件内容
    """
    path = rf"""{os.getcwd()}\source\daily_spend.xlsx"""
    data = pd.read_excel(path).fillna(0)
    data_list = []
    for i in range(0, len(data)):
        data_dic = {
            "date": data.loc[i, "date"],
            "food": data.loc[i, "food"],
            "transportation": data.loc[i, "transportation"],
            "necessities": data.loc[i, "necessities"],
            "rent": data.loc[i, "rent"],
            "clothes": data.loc[i, "clothes"],
            "snack": data.loc[i, "snack"],
            "entertainment": data.loc[i, "entertainment"],
            "communication": data.loc[i, "communication"],
            "soc_security": data.loc[i, "soc_security"],
            "other": data.loc[i, "other"],

        }
        data_list.append(data_dic)
    return data_list


