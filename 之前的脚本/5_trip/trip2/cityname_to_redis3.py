# -*- coding:utf-8 -*-
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
REDIS_URL = 'redis://:ABFSDD@ABFS!&rh@127.0.0.1:5000/1'
redis = StrictRedis.from_url(REDIS_URL)

M_HOST = "127.0.0.1"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("ABFSDD@ABFS!&rh")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri)
col = mongoclient['trip2']['area']
cursor = col.find({})
count = 0
num = 0
for i in cursor:
    num += 1
    item = dict()
    item['pageIndex'] = 1
    item['cityName'] = i['area']
    # item['cityName'] = "Tokyo"
    print(item)
    data = pickle.dumps(item)
    # 添加到商品爬虫redis_key指定的list
    redis.rpush(REDIS_KEY, data)
    # break

mongoclient.close()