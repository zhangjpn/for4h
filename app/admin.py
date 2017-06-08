#-*- coding:utf-8 -*-

from flask_admin import Admin, ModelView
from models import CarFixRecord

class CarFixRecordModelView(ModelView):
    can_export = True
    column_list = ()
    column_label = {}


def init_admin():
    admin = Admin(name='驷惠数据后台管理',url='/4h/admin/')
    admin.add_view(CarFixRecordModelView(CarFixRecord))
