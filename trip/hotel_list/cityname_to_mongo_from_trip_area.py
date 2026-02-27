# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/24 16:22
# explain:



import requests
import re
import time
import json
import math
import json
import pickle
import requests
import pymongo
from urllib import parse
import hashlib
import os


# redis配置
from redis import StrictRedis

REDIS_KEY = 'trip_hotel_list'
REDIS_URL = 'redis://:grad@0212!GnGn@111.txt.170.7.65:5001/1'
redis = StrictRedis.from_url(REDIS_URL)

M_HOST = "127.0.0.1"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri,maxPoolSize=3)
col = mongoclient['trip']['area']

col2 = mongoclient['trip']['area_and_gadm']
col2.create_index("uuid", unique=True)



def hash_sha1(url):
    # 创建md5对象
    h = hashlib.sha1()
    h.update(url.encode(encoding='utf-8'))
    res = h.hexdigest()
    return res

cursor = col.find( {}, no_cursor_timeout=True, batch_size=5)
count = 0
num = 0
for i in cursor:
    num += 1
    if i['area'] == None:
        continue
    item = dict()
    item['area'] = i['area']
    item['uuid'] = hash_sha1(i['area'])
    col2.update_one({"uuid": item["uuid"]}, {"$set": item}, upsert=True)



mongoclient.close()
redis.close()