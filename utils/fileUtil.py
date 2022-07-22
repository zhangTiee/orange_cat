# -*- coding: utf-8 -*-
# @desc    :
# @version :python3.6
# @Time    :2022/7/4 11:17
# @Author  : zjl
import os
import pandas as pd
import datetime
from uuid import uuid4

pd.set_option("display.max_columns", None)


def GetExcelData(path):
    """
    获取数据源,扫描当前目录下后缀名为xlsx的文件
    :return:excel文件内容
    """
    data = pd.read_excel(path).fillna(0)
    data_list = []
    for i in range(0, len(data)):
        data_dic = {
            "date": data.loc[i, "日期"],
            "food": data.loc[i, "餐饮"],
            "transportation": data.loc[i, "交通"],
            "necessities": data.loc[i, "生活用品"],
            "rent": data.loc[i, "房租水电"],
            "clothes": data.loc[i, "衣服"],
            "snack": data.loc[i, "零食"],
            "entertainment": data.loc[i, "娱乐"],
            "communication": data.loc[i, "通讯"],
            "soc_security": data.loc[i, "社保"],
            "beauty_salons": data.loc[i, "美容美发"],
            "electronic_product": data.loc[i, "电子产品"],
            "other": data.loc[i, "其他"],
        }
        data_list.append(data_dic)
    return data_list


def save_data(file):
    """
    处理接口上传文件
    :return:
    """
    """保存文件"""
    # 原始文件名
    old_filename = file.filename
    # 存储文件名
    new_filename = str(uuid4()) + os.path.splitext(old_filename)[-1]
    dest_path = rf"{os.getcwd()}\tmp\file\{datetime.datetime.now().strftime('%Y%m%d')}"
    if not os.path.isdir(dest_path):
        os.makedirs(dest_path)
    save_file = os.path.abspath(os.path.join(dest_path, new_filename))
    if os.path.isfile(save_file):
        # 先删除，再保存
        os.remove(save_file)
    file.save(save_file)
    return old_filename, new_filename, save_file


def remove_file(file):
    """
    删除上传文件
    :return:
    """
    if os.path.isfile(file):
        # 先删除，再保存
        os.remove(file)
