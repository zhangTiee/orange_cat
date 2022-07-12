# -*- coding: utf-8 -*-
# @desc    :
# @version :python3.6
# @Time    :2022/7/4 10:43
# @Author  : zjl
import datetime
import os

from pandas import DataFrame

from utils.mySQLUtil import MySQLUtil
from utils.fileUtil import GetExcelData
from utils.fileUtil import save_data, remove_file


def data_dr(file):
    """
    导入每日数据
    :return:
    """
    _, _, path = save_data(file)
    data = GetExcelData(path)
    for data_ in data:
        data_list = list(data_.values())
        add_daily_spent(data_list)
    remove_file(path)


def add_daily_spent(data_list):
    """
    新增每日记录
    :param data_list:
    :return:
    """
    for i in range(0, len(data_list)):
        data_list[i] = str(data_list[i])
        data_list[i] = '0.0' if not data_list[i] else data_list[i]
    data_info = {
        "date": data_list[0],
        "food": data_list[1],
        "transportation": data_list[2],
        "necessities": data_list[3],
        "rent": data_list[4],
        "clothes": data_list[5],
        "snack": data_list[6],
        "entertainment": data_list[7],
        "communication": data_list[8],
        "soc_security": data_list[9],
        "other": data_list[10],
    }
    MySQLUtil().SqlInsert("daily_spend", data_info)


def update_daily_spent(data_list):
    """
    更新每日记录
    :param data_list:
    :return:
    """
    for i in range(0, len(data_list)):
        data_list[i] = '0.0' if not data_list[i] else data_list[i]
    data_info = {
        "date": data_list[0],
        "food": data_list[1],
        "transportation": data_list[2],
        "necessities": data_list[3],
        "rent": data_list[4],
        "clothes": data_list[5],
        "snack": data_list[6],
        "entertainment": data_list[7],
        "communication": data_list[8],
        "soc_security": data_list[9],
        "other": data_list[10],
    }
    MySQLUtil().SqlUpdate("daily_spend", data_info, "date")


def sel_daily_spent(page, limit, start_date, end_date):
    """
    查询记录
    :param page:
    :param limit:
    :param start_date:
    :param end_date:
    :return:
    """
    page = (page - 1) * limit
    filter_sql = ""
    if start_date or end_date:
        if not start_date:
            start_date = 19491001
        if not end_date:
            end_date = 99991231
        filter_sql = f"""where date between {start_date} and {end_date} """
    query_sql = f"""
            select * from daily_spend {filter_sql} order by date desc limit {page},{limit}"""
    query_count_sql = f"""
            select count(*) from daily_spend {filter_sql}"""
    res_data = MySQLUtil().SqlSe(query_sql)
    count = MySQLUtil().SqlSe(query_count_sql)[0]["count(*)"]
    for res_data_ in res_data:
        res_data_["sum"] = sum(list(res_data_.values())[1:-1])
    return count, res_data


def data_dc():
    """
    数据导出
    :return:
    """
    query_sql = f"""
   select date, food, transportation, necessities, rent, clothes, snack, entertainment, communication, soc_security, other from daily_spend order by date desc
    """
    res_data = MySQLUtil().SqlSe(query_sql)
    data_list = []
    for index, row in enumerate(res_data):
        row_list = [index+1]
        row_list.extend(list(row.values()))
        data_list.append(row_list)
    excel_data = DataFrame(columns=["序号", "日期", "餐饮", "交通", "生活用品", "房租水电", "衣服", "零食", "娱乐", "通讯", "社保", "其他"], data=data_list)
    out_path = rf"{os.getcwd()}\tmp\file\{datetime.datetime.now().strftime('%Y%m%d')}\消费记录_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    excel_data.to_excel(out_path, sheet_name="消费记录", index=None)
