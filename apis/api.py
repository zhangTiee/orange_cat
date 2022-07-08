# -*- coding: utf-8 -*-
# @desc    :
# @version :python3.6
# @Time    :2022/7/4 11:57
# @Author  : zjl

import flask

from data_calculation.daily_spent import (
    add_daily_spent,
    update_daily_spent,
    sel_daily_spent,
)
from data_calculation.mounth_spent import (
    sel_mounth_data,
)

app = flask.Flask(__name__)


# 日度新增
@app.route('/daily_spent/add', methods=['POST'])
def add_data():
    date = flask.request.values.get('date')
    food = flask.request.values.get('food')
    transportation = flask.request.values.get('transportation')
    necessities = flask.request.values.get('necessities')
    rent = flask.request.values.get('rent')
    clothes = flask.request.values.get('clothes')
    snack = flask.request.values.get('snack')
    entertainment = flask.request.values.get('entertainment')
    communication = flask.request.values.get('communication')
    soc_security = flask.request.values.get("soc_security")
    other = flask.request.values.get('other')
    add_daily_spent([date, food, transportation, necessities, rent, clothes, snack, entertainment, communication, soc_security,  other])
    return {"code": 0, "msg": "新增完成"}


# 日度修改
@app.route('/daily_spent/update', methods=['POST'])
def update_data():
    date = flask.request.values.get('date')
    food = flask.request.values.get('food')
    transportation = flask.request.values.get('transportation')
    necessities = flask.request.values.get('necessities')
    rent = flask.request.values.get('rent')
    clothes = flask.request.values.get('clothes')
    snack = flask.request.values.get('snack')
    entertainment = flask.request.values.get('entertainment')
    communication = flask.request.values.get('communication')
    soc_security = flask.request.values.get("soc_security")
    other = flask.request.values.get('other')
    update_daily_spent([date, food, transportation, necessities, rent, clothes, snack, entertainment, communication, soc_security, other])
    return {"code": 0, "msg": "更新完成"}


# 日查询
@app.route('/daily_spent/select', methods=['GET', 'POST'])
def select_data():
    page = flask.request.values.get('page')
    limit = flask.request.values.get('limit')
    start_date = flask.request.values.get('start_date', "")
    end_date = flask.request.values.get('end_date', "")
    count, res_data = sel_daily_spent(int(page), int(limit), start_date, end_date)
    return {"code": 0, "msg": "查询成功", "data": res_data, "count": count}


# 月度查询
@app.route('/month_spent/select', methods=['POST'])
def sel_month_data():
    month = flask.request.values.get('month')
    res_data = sel_mounth_data(month)
    return {"code": 0, "msg": "查询成功", "data": res_data}


app.run()
