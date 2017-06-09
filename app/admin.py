# -*- coding:utf-8 -*-

from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from .models import CarFixRecord, StdCarFixRecord
from mongoengine import connect
from .fields import STDCARFIXRECORDFIELD

class CarFixRecordModelView(ModelView):
    """展示原始数据"""
    can_export = True
    column_list = ()
    can_edit = False
    can_create = False  # 调试
    can_delete = False
    column_labels = {
        'carinfo': '车辆信息',
        'repairhourslist': '维修项目',
        'carpartslist': '配件信息',
        'othercostlist': '其它费用信息',
    }


class StdCarFixRecordModelView(ModelView):
    """展示标准数据"""
    can_export = True
    can_edit = False
    can_create = False
    can_delete = False
    column_labels = STDCARFIXRECORDFIELD


def init_admin(app):
    connect(db='spv1', alias='spv1', host='127.0.0.1', port=27017)  # 暂存数据库
    connect(db='for4h', alias='for4h', host='127.0.0.1', port=27017)  # 暂存数据库
    admin = Admin(name='驷惠数据后台管理', url='/4h/admin')
    admin.add_view(CarFixRecordModelView(CarFixRecord, name='原始维修数据'))
    admin.add_view(StdCarFixRecordModelView(StdCarFixRecord, name='标准维修数据'))
    admin.init_app(app)
