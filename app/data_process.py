# -*- coding:utf-8 -*-

from .models import StdCarFixRecord
import logging
from logging.handlers import RotatingFileHandler
import os.path as path
from .commontools import *
import json
# 记录日志
log_base = path.join(path.dirname(path.dirname(__file__)), 'upload_base.log')
log_warn = path.join(path.dirname(path.dirname(__file__)), 'upload_warn.log')
logger = logging.getLogger('upload')
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fhandler = logging.FileHandler(log_warn, mode='a')
fhandler.setFormatter(formatter)
fhandler.setLevel(logging.WARNING)
rhandler = RotatingFileHandler(log_base, mode='a', maxBytes=1*1024*1024, backupCount=3)
rhandler.setLevel(logging.INFO)
rhandler.setFormatter(formatter)
logger.addHandler(fhandler)  # 重要日志
logger.addHandler(rhandler)  # 一般日志轮替


def standardize_data(data):
    carinfo = json.loads(data.get('carinfo'))
    repairhourslist = json.loads(data.get('repairhourslist'))
    carpartslist = json.loads(data.get('carpartslist'))
    othercostlist = json.loads(data.get('othercostlist'))
    company_id = get_company_id(carinfo.get('company'))
    store_id = get_store_id(carinfo.get('company'))

    connect(db='for4h', alias='for4h', host='127.0.0.1', port=27017)  # 测试数据库
    connect(db='spv1', alias='spv1', host='127.0.0.1', port=27017)  # 正式上传的时候数据放到spv1数据库中

    # 获取repairItems列表
    repairitems = []
    for hour in repairhourslist:
        item = {
            'name': hour.get('repairname'),  # 维修项目名称
            'hours': float(hour.get('repairhours', 0)),  # 维修工时
            'price': float(hour.get('laborhourprice', 0)),  # 维修工时单价
            'cost': float(hour.get('repaircost', 0))  # 金额
        }
        repairitems.append(item)
    repairparts = []
    for part in carpartslist:
        item = {
            'name': part.get('partsname', ''),  # 配件名称
            'partNo': part.get('partsno', ''),  # 配件编码
            'brand': part.get('partsmanufacture', ''),  # 品牌
            'quantity': int(part.get('partsquantity', 0)),  # 配件数量
            'attribute': part.get('partsattribute', ''),  # 配件属性
            '_self': True if part.get('caruserparts', '0') == '1' else False,  # 是否为自备配件(原始数据1-是 0-否)  #python关键字self无法用作变量
            'price': float(part.get('partscost', 0)),  # 单价
            'cost': float(part.get('partsallcost', 0)),  # 金额
        }
        repairparts.append(item)

    others = []
    for item in othercostlist:
        cost = {
            'name': item.get('othername'),  # 其他费用项目名称
            'cost': float(item.get('othercost')),  # 金额
        }
        others.append(cost)

    qainfo = {
        'qaMileage': 0,  # 质量保证里程
        'qaDate': datetime.datetime(1990, 1, 1),  # 质量保证时间
    }
    sum_doc = {
        'cost': float(data.get('total', 0)),  # 总费用
        'realcost': float(data.get('total', 0)),  # 实收总费用
    }
    now = datetime.datetime.now()
    std_data = {
        'plateNo': carinfo.get('carno', ''),  # 车牌号码
        'engineNo': carinfo.get('enginenumber', ''),  # 发动机号码
        'statementNo': carinfo.get('statementno', ''),  # 结算清单编号
        'settlementDate': str_to_date(carinfo.get('settledate')),  # 结算日期
        'deliveryDate': str_to_date(data.get('repairdate')),  # 送修日期
        'deliveryMileage': int(data.get('repairmile', 0)),  # 送修里程
        'description': ':'.join([data.get('faultreason', ''), data.get('faultdescript', '')]),  # 故障信息
        'repairItems': repairitems,  # 维修项目列表
        'repairParts': repairparts,  # 维修配件列表
        'others': others,  # 其他费用列表
        'sum': sum_doc,  # 总费用
        'QAInfo': qainfo,  # 质保信息
        'VINCode': carinfo.get('carvin'),  # VIN码
        'vehicleOwner': '',  # 车辆所有者 没此字段
        'vehicleBrand': '',  # 车辆品牌 没此字段
        'vehicleType': int(carinfo.get('cartype', 0)),  # 车辆类型 原类型：Number
        'repairType': int(carinfo.get('repairtype', 0)),  # 维修类型  原类型：Number
        'repairName': '',  # 送修人名称 没此字段
        'repairMobile': '',  # 送修人联系方式  没此字段
        'source': 5,  # 维修表单来源：1:新增，2：上传，3：接口 # 新增5：4h来源
        'status': 0,  # 维修表单是否同步，0:未同步，1：同步
        'integratedRate': 3,  # 表单完整率 0:不合格，1:高，2:中，3:低，
        'companyId': company_id,  # 维修企业
        'xlsxPath': '',  # XLSX文件下载
        'originalXLSXName': '',  # 原xlsx名称
        'xlsxStatus': 3,  # 数据标准化,0: 标准中，1:已标准, 2:标准失败
        'factoryDate': None,  # 出厂日期 没此字段
        'factoryMileage': 0,  # 出厂里程 没此字段
        'updated': now,  # 更新日期
        'created': now,  # 创建日期
        'is_status_fix': 0,  # 非标准数据,0: 未确认，1:已确认， 2:已核对确认
        'store': store_id,  # 关联对应门店
    }

    return std_data


def validate_data(std_data):
    # 验证必要的字段是否存在
    required_fields = ['VINCode', 'plateNo', ]  # 'vehicleBrand', 'deliveryDate', 'factoryDate'
    for key in required_fields:
        if not std_data.get(key):
            logger.warning('缺少必需字段：%s' % key)
            return False
    # 验证vin是否有效
    if not is_valid_vin(std_data.get('VINCode')):  # 判断vin码有效性
        logger.warning('无效的车架号（VIN）: %s' % std_data.get('VINCode'))
        return False
    return True


def process_and_upload(data):
    """从原始维修单中判断注册维修企业、获取标准化的字段和有效性判断，
    清洗之后获得标准化的数据，上传到暂存的标准数据库
    :param data:维修单数据"""
    std_data = standardize_data(data)
    is_valid = validate_data(std_data)
    if not is_valid:
        return False
    # 如果数据有效并且该维修企业已在后台注册，那么上传数据
    if std_data.get('companyId'):
        try:
            StdCarFixRecord(**std_data).save()
            logger.info('数据上传成功，上传位置：for4h.maintenaces 结算清单编号(statementNo):%s' % std_data.get('statementNo'))
        except Exception as e:
            logger.exception('标准数据上传失败，触发异常：%s' % e)
    # 数据保存到临时标准数据表
    try:
        coll = MongoClient()['for4h'].maintenaces4h  # 临时标准数据表
        coll.insert_one(std_data)
        logger.info('数据保存成功，数据保存位置：for4h.maintenaces4h 结算清单编号(statementNo):%s' % std_data.get('statementNo'))
    except Exception as e:
        logger.exception('标准数据保存失败，触发异常：%s' % e)
