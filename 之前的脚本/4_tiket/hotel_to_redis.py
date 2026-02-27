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
M_PASSWORD = parse.quote_plus("018320RHj@ABFS!&rh")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri)
col = client['tiket']['seed_hotel']

# redis配置
REDIS_KEY = 'tiket_detail'
REDIS_URL = 'redis://:018320RHj@ABFS!&rh@127.0.0.1:5000/1'
redis = StrictRedis.from_url(REDIS_URL)


cursor = col.find({}, no_cursor_timeout=True, batch_size=5)
for i in cursor:
    item = dict()
    item['url'] = i['url']
    item['id'] = i['uuid']
    print(item)
    data = pickle.dumps(item)
    # 添加到商品爬虫redis_key指定的list
    redis.rpush(REDIS_KEY, data)

client.close()
