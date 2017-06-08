#-*- coding:utf-8 -*-

from mongoengine import connect, Document, EmbededDocument
from mongoengine.fields import *

class RepairPart(EmbededDocument):
    meta = {
        'db_alias': 'for4h',
        'collection': 'repairparts',
        'strict': False,
    }

class RepairHour(EmbededDocument):
    meta = {
        'db_alias': 'for4h',
        'collection': 'repairhours',
        'strict': False,
    }
class Other(EmbededDocument):
    meta = {
        'db_alias': 'for4h',
        'collection': 'others',
        'strict': False,
    }

class CarFixRecord(Document):
    meta = {
        'db_alias': 'for4h',
        'collection': 'carfixrecords',
        'strict': False,
    }
    carinfo = DictField()
    carpartslist = EmbededDocumentListField(EmbededDocumentField(RepairPart))
    caritemslist = EmbededDocumentListField(EmbededDocumentField(RepairPart))

