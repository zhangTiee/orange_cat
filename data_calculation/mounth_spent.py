# -*- coding: utf-8 -*-
# @desc    :
# @version :python3.6
# @Time    :2022/7/4 10:50
# @Author  : zjl

from utils.mySQLUtil import MySQLUtil


def add_mounth_data(month):
    """
    添加月度总结
    :return:
    """
    query_sql = f"""
            select sum(food),sum(transportation),sum(necessities),sum(rent),sum(clothes),sum(snack),sum(entertainment),sum(communication),sum(soc_security),sum(beauty_salons),sum(other) from daily_spend
            where date like '{month}%'"""
    month_data = MySQLUtil().SqlSe(query_sql)[0]
    query_count_sql = f"""
            select count(*) from month_spend where month like '{month}%'"""
    count = MySQLUtil().SqlSe(query_count_sql)[0]["count(*)"]
    data_info = {
        "month": month,
        "food": month_data["sum(food)"],
        "transportation": month_data["sum(transportation)"],
        "necessities": month_data["sum(necessities)"],
        "rent": month_data["sum(rent)"],
        "clothes": month_data["sum(clothes)"],
        "snack": month_data["sum(snack)"],
        "entertainment": month_data["sum(entertainment)"],
        "communication": month_data["sum(communication)"],
        "soc_security": month_data["sum(soc_security)"],
        "beauty_salons": month_data["sum(beauty_salons)"],
        "other": month_data["sum(other)"],
    }
    if not count:
        MySQLUtil().SqlInsert("month_spend", data_info)
    else:
        MySQLUtil().SqlUpdate("month_spend", data_info, "month")


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
    if res_data:
        data_dic = res_data[0]
        data_dic["sum"] = sum(list(data_dic.values())[1:])
        data_ratio = {
            "food": round(res_data[0]["food"] / data_dic["sum"], 3),
            "transportation": round(res_data[0]["transportation"] / data_dic["sum"], 3),
            "necessities": round(res_data[0]["necessities"] / data_dic["sum"], 3),
            "rent": round(res_data[0]["rent"] / data_dic["sum"], 3),
            "clothes": round(res_data[0]["clothes"] / data_dic["sum"], 3),
            "snack": round(res_data[0]["snack"] / data_dic["sum"], 3),
            "entertainment": round(res_data[0]["entertainment"] / data_dic["sum"], 3),
            "communication": round(res_data[0]["communication"] / data_dic["sum"], 3),
            "soc_security": round(res_data[0]["soc_security"] / data_dic["sum"], 3),
            "beauty_salons": round(res_data[0]["beauty_salons"] / data_dic["sum"], 3),
            "other": round(res_data[0]["other"] / data_dic["sum"], 3),
        }
    else:
        data_dic = {}
        data_ratio = {}
    data = {"data_statistics": data_dic, "data_ratio": data_ratio}
    return data
