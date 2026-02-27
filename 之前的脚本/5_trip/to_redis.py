# -*- coding:utf-8 -*-
import json
import math
import json
from redis import StrictRedis
import pickle
import requests
from urllib import parse
import pymongo
import re

M_HOST = "localhost"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("ABFSDD@ABFS!&rh")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri)
col = client['trip']['seed']

# redis配置
REDIS_KEY = 'trip_keyword'
REDIS_URL = 'redis://:ABFSDD@ABFS!&rh@127.0.0.1:5000/1'
redis = StrictRedis.from_url(REDIS_URL)


cursor = col.find({}, no_cursor_timeout=True, batch_size=5)
for i in cursor:
    url = i['url']
    keyword = re.findall('-Reviews-(.+?)\.html', url)[0].replace("-", " ").replace("_", " ")
    print(keyword)
    item = dict()
    item['keyword'] = keyword
    item['uuid'] = i['uuid']
    data = pickle.dumps(item)
    # 添加到商品爬虫redis_key指定的list
    redis.rpush(REDIS_KEY, data)

client.close()
