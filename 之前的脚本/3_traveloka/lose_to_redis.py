# -*- coding:utf-8 -*-
import json
import math
import json
from redis import StrictRedis
import pickle
import requests
from urllib import parse
import pymongo


M_HOST = "localhost"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("0820RH@ABFSDD!&rh")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri)
col = client['traveloka']['seed']
detailcol = client['traveloka']['details']

# redis配置
REDIS_KEY = 'traveloka_detail'
REDIS_URL = 'redis://:0820RH@ABFSDD!&rh@127.0.0.1:5000/1'
redis = StrictRedis.from_url(REDIS_URL)


count = 0
num = 0
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)
for i in cursor:
    count += 1
    item = dict()
    item['url'] = i['url']
    item['id'] = i['uuid']
    res_find = detailcol.find_one({"id": item['id']})
    if res_find:
        continue

    num += 1
    print(f"{count}-{num}")
    data = pickle.dumps(item)
    # 添加到商品爬虫redis_key指定的list
    redis.rpush(REDIS_KEY, data)

client.close()
