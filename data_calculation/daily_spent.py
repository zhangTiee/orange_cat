# -*- coding: utf-8 -*-
# @desc    :
# @version :python3.6
# @Time    :2022/7/4 10:43
# @Author  : zjl
import datetime

from utils.mySQLUtil import MySQLUtil
from utils.get_file_data import GetExcelData


def daily_data():
    """
    导入每日数据
    :return:
    """
    data = GetExcelData()
    for data_ in data:
        data_list = list(data_.values())
        add_daily_spent(data_list)


def add_daily_spent(data_list):
    """
    新增每日记录
    :param data_list:
    :return:
    """
    for i in range(0, len(data_list)):
        data_list[i] = 0.0 if not data_list[i] else data_list[i]
    add_sql = f"""
    insert into daily_spend(date, food, transportation, necessities, rent, clothes, snack, entertainment, communication, soc_security, other)
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s)"""
    MySQLUtil().SqlCommit(add_sql, tuple(data_list))


def update_daily_spent(data_list):
    """
    更新每日记录
    :param data_list:
    :return:
    """
    for i in range(0, len(data_list)):
        data_list[i] = 0.0 if not data_list[i] else data_list[i]
    upd_sql = f"""
    update daily_spend set food=%s,transportation=%s,necessities=%s,rent=%s,clothes=%s,snack=%s,entertainment=%s,communication=%s,soc_security=%s,other=%s 
    where date = %s"""
    date = data_list[0]
    data_list = data_list[1:]
    data_list.append(date)
    MySQLUtil().SqlCommit(upd_sql, tuple(data_list))


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
    query_sql = f"""select * from daily_spend {filter_sql} order by date desc limit {page},{limit}"""
    query_count_sql = f"""select count(*) from daily_spend {filter_sql}"""
    res_data = MySQLUtil().SqlSe(query_sql)
    count = MySQLUtil().SqlSe(query_count_sql)[0][0]
    res_list = []
    for res_data_ in res_data:
        res_dict = {
            "date": res_data_[0],
            "food": res_data_[1],
            "transportation": res_data_[2],
            "necessities": res_data_[3],
            "rent": res_data_[4],
            "clothes": res_data_[5],
            "snack": res_data_[6],
            "entertainment": res_data_[7],
            "communication": res_data_[8],
            "soc_security": res_data_[9],
            "other": res_data_[10],
            "id": res_data_[11],
            "sum": sum(res_data_[1:-1]),
        }
        res_list.append(res_dict)
    return count, res_list
