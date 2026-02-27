# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/24 11:34
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
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/1'
redis = StrictRedis.from_url(REDIS_URL)

M_HOST = "127.0.0.1"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri,maxPoolSize=1)
col = mongoclient['trip']['area_and_gadm']
cursor = col.find( {"area": {"$regex": "(Indonesia|Japan|Thailand|Malaysia)$"}}, no_cursor_timeout=True, batch_size=5)
count = 0
num = 0
for i in cursor:
    num += 1
    item = dict()
    item['pageIndex'] = 1
    item['cityName'] = i['area']
    if i['area'] == None:
        continue
    print(item)
    data = pickle.dumps(item)
    redis.rpush(REDIS_KEY, data)

mongoclient.close()
redis.close()