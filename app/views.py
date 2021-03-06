#-*- coding:utf-8 -*-
import datetime

from flask import jsonify, request
import logging
import os.path as path
from pymongo import MongoClient
import uuid
from .data_process import process_and_upload
from threading import Thread

# 日志记录
log_path = path.join(path.dirname(path.dirname(__file__)), '4h.log')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('for4h')
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fhandler = logging.FileHandler(log_path, mode='a')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)


def init_views(app):
    @app.route(r'/4h/')
    def index():
        return jsonify({'hello': 'world'}), 200

    @app.route(r'/4h/restservices/lciprest/lcipgetaccesstoken/query/', methods=['POST'])
    def create_token():
        """根据企业代码和密码生成access_token返回"""
        # username = request.json.get('username')
        # password = request.json.get('password')
        logger.info('User : %s requests for token.')
        # 生成token返回
        token = ''.join(uuid.uuid1().split('-'))
        res_data = {
                   "code": "1",
                   "status": "获取成功",
                   "accsss_token": token,
                    }
        return jsonify(res_data), 200

    @app.route(r'/4h/restservices/lciprest/lcipcarfixrecordadd/query', methods=['POST'])
    def create_carfixrecord():
        """新增维修记录"""
        try:
            data = request.json.copy()
            logger.info(data)
        except:
            print('Failed to parse json data')
            return jsonify({'error': 'failed'})
        if not data:
            data['created'] = datetime.datetime.now()
            data['update'] = datetime.datetime.now()
        # 将原始数据存放到数据库中
        try:
            cli = MongoClient()
            coll_fixrecord = cli.for4h.carfixrecord
            coll_fixrecord.insert_one(data)
            data.pop('_id')
        except Exception as e:
            logger.warning('原始数据保存失败，触发异常：%s' % e)
        # 数据处理和上传
        Thread(target=process_and_upload, args=(data,)).start()
        res = {
                "code": "1",
                "status": "新增成功",
                "recordid": data['_id'].__str__() + '0' * 8,
                "carno": request.json.get('carno'),
                "carvin": request.json.get('carvin'),
                "enginenumber": request.json.get('enginenumber')
                }
        return jsonify(res), 200

    @app.route(r'/4h/restservices/lciprest/lcipcarpartsrecordadd/query', methods=['POST'])
    def create_repairpart():
        """增加维修配件"""
        data = request.json.copy()
        logger.info(data)
        # 将数据存放到数据库中
        cli = MongoClient()
        coll_fixrecord = cli.for4h.repairparts
        coll_fixrecord.insert_one(data)
        part_id = data.get('_id').__str__() + '0' * 8  # 生成唯一识别码
        res_data = {
            "code": "1",
            "status": "新增成功",
            "partsid": part_id,  # 汽车配件记录唯一标识
        }
        return jsonify(res_data), 200

    @app.route(r'/4h/restservices/lciprest/lcipcarfixrecordadd/query', methods=['POST'])
    def create_repairitem():
        """增加维修项目"""
        data = request.json.copy()
        logger.info(data)
        # 将数据存放到数据库中
        cli = MongoClient()
        coll_fixrecord = cli.for4h.repairitems
        coll_fixrecord.insert_one(data)
        part_id = data.get('_id').__str__() + '0' * 8  # 生成唯一识别码
        res_data = {
            "code": "1",
            "status": "新增成功",
            "partsid": part_id,  # 汽车配件记录唯一标识
        }
        return jsonify(res_data), 200

    @app.route(r'/4h/restservices/lciprest/lcipcarfixrecordadd/query', methods=['POST'])
    def create_other():
        """增加其它费用"""
        data = request.json.copy()
        logger.info(data)
        # 将数据存放到数据库中
        cli = MongoClient()
        coll_fixrecord = cli.for4h.others
        coll_fixrecord.insert_one(data)
        other_id = data.get('_id').__str__()  # 生成唯一识别码
        res_data = {
            'code': '1',
            'status': '',
            '': other_id,  # 部件唯一识别码
        }
        return jsonify(res_data), 200
    return app
