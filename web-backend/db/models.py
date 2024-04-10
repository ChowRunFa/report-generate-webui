# -*- coding: utf-8 -*-
# @Time    : 2022/6/26 16:22
# @Author  : ChowRunFa
# @File    : models.py
# @Software: PyCharm
from flask_sqlalchemy import SQLAlchemy
import simplejson as json#pip install simplejson 或者 pip install python-simplejson
# from dbServer import Connection

db = SQLAlchemy()

class llm_set(db.Model):
    __tablename__ = 'llm_set'
    llm_name = db.Column(db.String(255), primary_key=True)
    api_key = db.Column(db.String(255), primary_key=True)
    api_base = db.Column(db.String(255), primary_key=True)
    using = db.Column(db.Integer, default=0)


    __table_args__ = (
        {'comment': 'llm_name: 大模型名称, api_key: 大模型的apikey, api_base: 大模型的api base, using: 是否使用该条记录'}
    )