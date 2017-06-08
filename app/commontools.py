# -*-coding:utf-8 -*-

from pymongo import MongoClient
import re
from mongoengine import connect
import time
import datetime


def str_to_date(string):
    if isinstance(string, datetime.datetime):
        return string
    if not isinstance(string, str):
        return None
    string = string.strip()
    try:
        ts = time.strptime(string, '%Y/%m/%d %H:%M:%S')
        dt = datetime.datetime(*ts[0:6])
    except:
        try:
            ts = time.strptime(string, '%Y-%m-%d %H:%M:%S')
            dt = datetime.datetime(*ts[0:6])
        except:
            try:  # 若数据不完整，尝试获取日期
                patt = re.compile(r'([0-9]{4})[\-\/]([0-9]{1,2})[\-\/]([0-9]{1,2})')
                d = patt.findall(string)[0]
                dt = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))
            except:
                dt = None
    return dt


def get_company_id(company_name):
    """通过营业执照获取公司在数据库中的ObjectId对象，对象在spv1.compaies表中
    :param company_name:维修企业名称
    :return ObjectId对象
    """
    company_name.strip()
    try:
        cli = MongoClient(host='127.0.0.1', port=27017, tz_aware=True)
        coll = cli.spv1.companies
        company = coll.find_one({'name': company_name.strip()})
        return company['_id']
    except:
        return None


def get_store_id(company_name):
    """通过维修企业名称获取终端门店的ObjectId对象，该对象在spv1.stores数据表中，"""
    try:
        cli = MongoClient(host='127.0.0.1', port=27017, tz_aware=True)
        store_coll = cli.spv1.stores
        store = store_coll.find_one({'storeName': company_name.strip()})
        return store['_id']
    except:
        return None


def is_valid_vin(vin):
    """判断vin是否有效"""
    if not isinstance(vin, str):
        return False
    kv = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8,
        'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'p': 7, 'r': 9,
        's': 2, 't': 3, 'u': 4, 'v': 5, 'w': 6, 'x': 7, 'y': 8, 'z': 9
    }  # 'q': 8, 无q
    wv = {
        '1': 8, '2': 7, '3': 6, '4': 5, '5': 4, '6': 3, '7': 2, '8': 10,
        '10': 9, '11': 8, '12': 7, '13': 6, '14': 5, '15': 4, '16': 3, '17': 2
    }

    if len(vin) != 17:
        return False
    lowervin = vin.lower()
    verifyCode = lowervin[8]
    if verifyCode < '0' or verifyCode > '9':
        if verifyCode != 'x':
            return False
    total = 0
    for i in range(17):
        if i == 8:
            continue
        code = lowervin[i]
        if code in kv:
            total += kv[code] * wv[str(i + 1)]
        else:
            return False
    res = str(total % 11)
    if verifyCode == 'x':
        return res == 10
    else:
        return res == verifyCode


def is_valid_lic_15(lic):
    """判断15位营业执照有效性,14位数字+1位数据校验码"""
    lic_lower = lic.lower()
    if not re.compile(r'^[0-9]{15}$').findall(lic_lower):
        return False
    x = 10
    total = 0
    for i in range(15):
        total = (x + int(lic_lower[i])) % 10
        if i == 14:
            break
        x = (total * 2) % 11
    return total == 1


def is_valid_lic_18(lic):
    """判断18位营业执照有效性"""
    kv = {'a': 10, 'h': 17, 'r': 25, 'l': 20, '8': 8, '3': 3, 'j': 18, 'q': 24, 'e': 14, 'n': 22,
          'k': 19, '6': 6, '0': 0, '5': 5, '4': 4, '1': 1, '9': 9, 'd': 13, 'u': 27, '7': 7, '2': 2,
          'f': 15, 't': 26, 'w': 28, 'g': 16, 'y': 30, 'p': 23, 'b': 11, 'm': 21, 'c': 12, 'x': 29}
    lic_lower = lic.lower()
    if not re.compile(r'^([159y])([1239])([0-9]{6})([[0-9abcdefghjklmnpqrtuwxy]{10})$').findall(lic_lower):
        return False
    total = 0
    for i in range(17):
        total += kv[lic_lower[i]] * (3 ** i % 31)
    c18 = 31 - (total % 31)
    if c18 == 31:
        c18 = 0
    return c18 == kv[lic_lower[-1]]
