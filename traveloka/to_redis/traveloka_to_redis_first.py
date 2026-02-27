# -*- coding:utf-8 -*-
import json
import math
import json
from redis import StrictRedis
import pickle
import requests
from urllib import parse
import pymongo
import hashlib
def hash_sha1(url):
    # 创建md5对象
    h = hashlib.sha1()
    h.update(url.encode(encoding='utf-8'))
    res = h.hexdigest()
    return res



M_HOST = "localhost"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri)


# redis配置
REDIS_KEY = 'traveloka_detail'
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/1'
redis = StrictRedis.from_url(REDIS_URL)


col = client['traveloka']['indonesia']  #查找 印度尼西亚 的
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)
for i in cursor:
    item = dict()
    item['url'] = i['url'].replace('en-en', 'id-id')+"?cur=IDR"
    item['uuid'] = i["uuid"]
    print(item)
    data = pickle.dumps(item)
    # 添加到商品爬虫redis_key指定的list
    redis.rpush(REDIS_KEY, data)


col = client['traveloka']['japan']  #查找 马来西亚的
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)
for i in cursor:
    item = dict()
    item['url'] = i['url'].replace('en-en', 'ja-jp') +"?cur=JPY"
    item['uuid'] = i['uuid']
    print(item)
    data = pickle.dumps(item)
    # 添加到商品爬虫redis_key指定的list
    redis.rpush(REDIS_KEY, data)


client.close()
