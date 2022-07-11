# -*- coding: utf-8 -*-
# @desc    :
# @version :python3.6
# @Time    :2022/7/4 10:43
# @Author  : zjl
import datetime

from utils.mySQLUtil import MySQLUtil
from utils.get_file_data import GetExcelData


def data_dr():
    """
    导入每日数据
    :return:
    """
    data = GetExcelData()
    for data_ in data:
        data_list = list(data_.values())
        # add_daily_spent(data_list)


def add_daily_spent(data_list):
    """
    新增每日记录
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
