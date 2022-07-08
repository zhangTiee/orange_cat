# -*- coding: utf-8 -*-
# @desc    :
# @version :python3.6
# @Time    :2022/7/4 10:50
# @Author  : zjl
import datetime

from utils.mySQLUtil import MySQLUtil


def add_mounth_data(month):
    """
    添加月度总结
    :return:
    """
    month_list = [month]
    query_sql = f"""
    select sum(food),sum(transportation),sum(necessities),sum(rent),sum(clothes),sum(snack),sum(entertainment),sum(communication),sum(soc_security),sum(other) from daily_spend
    where date like '{month}%'"""
    month_list.extend(MySQLUtil().SqlSe(query_sql)[0])
    query_count_sql = f"""select count(*) from month_spend where month like '{month}%'"""
    count = MySQLUtil().SqlSe(query_count_sql)[0][0]
    if not count:
        ins_sql = f"""
        insert into month_spend(month, food, transportation, necessities, rent, clothes, snack, entertainment, communication, soc_security, other)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        MySQLUtil().SqlCommit(ins_sql, tuple(month_list))
    else:
        upd_sql = f"""
        update month_spend set food=%s,transportation=%s,necessities=%s,rent=%s,clothes=%s,snack=%s,entertainment=%s,communication=%s,soc_security=%s,other=%s
        where month = {month}
        """
        MySQLUtil().SqlCommit(upd_sql, tuple(month_list[1:]))


def sel_mounth_data(month):
    """
    查询月度数据
    :param month:
    :return:
    """
    query_sql = f"""
    select * from month_spend where month = %s
    """
    add_mounth_data(month)
    res_data = MySQLUtil().SqlSe(query_sql, month)
    if res_data[0][1]:
        data_dic = {
            "date": res_data[0][0],
            "food": res_data[0][1],
            "transportation": res_data[0][2],
            "necessities": res_data[0][3],
            "rent": res_data[0][4],
            "clothes": res_data[0][5],
            "snack": res_data[0][6],
            "entertainment": res_data[0][7],
            "communication": res_data[0][8],
            "soc_security": res_data[0][9],
            "other": res_data[0][10],
        }
        data_dic["sum"] = sum(list(data_dic.values())[1:])
        data_ratio = {
            "food": round(res_data[0][1]/data_dic["sum"], 3),
            "transportation": round(res_data[0][2]/data_dic["sum"], 3),
            "necessities": round(res_data[0][3]/data_dic["sum"], 3),
            "rent": round(res_data[0][4]/data_dic["sum"], 3),
            "clothes": round(res_data[0][5]/data_dic["sum"], 3),
            "snack": round(res_data[0][6]/data_dic["sum"], 3),
            "entertainment": round(res_data[0][7]/data_dic["sum"], 3),
            "communication": round(res_data[0][8]/data_dic["sum"], 3),
            "soc_security": round(res_data[0][9] / data_dic["sum"], 3),
            "other": round(res_data[0][10]/data_dic["sum"], 3),
        }
    else:
        data_dic = {}
        data_ratio = {}
    data = {"month_data": data_dic, "data_ratio": data_ratio}
    return data


