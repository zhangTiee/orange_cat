# -*- coding: utf-8 -*-
# @desc    :
# @version :python3.6
# @Time    :2022/7/4 11:57
# @Author  : zjl

from flask import Flask, request

from data_calculation.daily_spent import (
    data_dr,
    add_daily_spent,
    update_daily_spent,
    sel_daily_spent,
    data_dc,
)
from data_calculation.mounth_spent import (
    sel_mounth_data,
)

app = Flask(__name__)


# 日度新增
@app.route("/daily_spent/add", methods=["POST"])
def add_data():
    data = {"date": request.values.get("date"),
            "food": request.values.get("food"),
            "transportation": request.values.get("transportation"),
            "necessities": request.values.get("necessities"),
            "rent": request.values.get("rent"),
            "clothes": request.values.get("clothes"),
            "snack": request.values.get("snack", "0.0"),
            "entertainment": request.values.get("entertainment"),
            "communication": request.values.get("communication"),
            "soc_security": request.values.get("soc_security"),
            "electronic_product": request.values.get("electronic_product"),
            "beauty_salons": request.values.get("beauty_salons"),
            "other": request.values.get("other"),
            }
    add_daily_spent(data)
    return {"code": 0, "msg": "新增完成"}


# 日度修改
@app.route("/daily_spent/update", methods=["POST"])
def update_data():
    data = {"date": request.values.get("date"),
            "food": request.values.get("food"),
            "transportation": request.values.get("transportation"),
            "necessities": request.values.get("necessities"),
            "rent": request.values.get("rent"),
            "clothes": request.values.get("clothes"),
            "snack": request.values.get("snack"),
            "entertainment": request.values.get("entertainment"),
            "communication": request.values.get("communication"),
            "soc_security": request.values.get("soc_security"),
            "beauty_salons": request.values.get("beauty_salons"),
            "electronic_product": request.values.get("electronic_product"),
            "other": request.values.get("other"),
            }
    update_daily_spent(data)
    return {"code": 0, "msg": "更新完成"}


# 日查询
@app.route("/daily_spent/select", methods=["GET", "POST"])
def select_data():
    page = request.values.get("page")
    limit = request.values.get("limit")
    start_date = request.values.get("start_date", "")
    end_date = request.values.get("end_date", "")
    date = request.values.get("date")
    count, res_data = sel_daily_spent(int(page), int(limit), start_date, end_date, date)
    return {"code": 0, "msg": "查询成功", "data": res_data, "count": count}


# 月度查询
@app.route("/month_spent/select", methods=["POST"])
def sel_month_data():
    month = request.values.get("month")
    res_data = sel_mounth_data(month)
    return {"code": 0, "msg": "查询成功", "data": res_data}


# 数据导入
@app.route("/daily_spent/data_import", methods=["POST"])
def data_ipt():
    data_dr(request.files.get("file"))
    return {"code": 0, "msg": "导入成功"}


# 数据导出
@app.route("/daily_spent/data_export", methods=["GET"])
def data_ept():
    data_dc()
    return {"code": 0, "msg": "导出成功"}


app.run()
