# -*- coding:utf-8 -*-

from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from .models import CarFixRecord, StdCarFixRecord
from mongoengine import connect


class CarFixRecordModelView(ModelView):
    """展示原始数据"""
    can_export = True
    column_list = ()
    column_label = {}


class StdCarFixRecordModelView(ModelView):
    """展示标准数据"""
    can_export = True
    column_list = ()
    column_label = {}


def init_admin(app):
    connect(db='spv1', alias='spv1', host='127.0.0.1', port=27017)  # 暂存数据库
    connect(db='for4h', alias='for4h', host='127.0.0.1', port=27017)  # 暂存数据库
    admin = Admin(name='驷惠数据后台管理', url='/4h/admin')
    admin.add_view(CarFixRecordModelView(CarFixRecord, name='原始维修数据'))
    admin.add_view(StdCarFixRecordModelView(StdCarFixRecord, name='标准维修数据'))
    admin.init_app(app)
