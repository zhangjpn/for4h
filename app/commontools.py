#-*- coding:utf-8 -*-

import requests

def get_remote_token(**kwargs):
    """通过username和password获取远程的access_token"""
    query_string = 'http://'  # 查询远程token的url
    res = requests.post(url=query_string, json=kwargs)
    js = res.json
    return json
