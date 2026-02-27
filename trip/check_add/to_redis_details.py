# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/25 17:08
# explain:
# -*- coding:utf-8 -*-
import json
import math
import json
import re

from redis import StrictRedis
import pickle
import requests
from urllib import parse
import pymongo
import hashlib
from loguru import logger

M_HOST = "localhost"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri,maxPoolSize=10)

# redis配置
REDIS_KEY = 'trip_detail'
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/1'
redis = StrictRedis.from_url(REDIS_URL)

filter_list = []

def hash_sha1(url):
    # 创建md5对象
    h = hashlib.sha1()
    h.update(url.encode(encoding='utf-8'))
    res = h.hexdigest()
    return res

index =0
col = client['trip']['seed_hotels2']
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)

filter_col =  client['trip']['details']


for i in cursor:

    item = dict()
    item['id'] = re.findall("hotel-detail-(.+?)/", i['url'])[0]
    isIn = filter_col.find_one({'id': item['id']}, {'_id':1})
    if isIn ==None:

        if "Indonesia" in i["districtName"]:
            item['url'] = "https://id.trip.com" + i['url'] + "?curr=IDR&locale=id_id"
        elif "Japan" in i["districtName"]:
            item['url'] = "https://jp.trip.com" + i['url'] + "?curr=JPY&locale=ja_jp"
        elif "Malaysia" in i["districtName"]:
            item['url'] = "https://my.trip.com" + i['url'] + "?locale=ms_my&curr=MYR"
        elif "Thailand" in i["districtName"]:
            item['url'] = "https://th.trip.com" + i['url'] + "?curr=THB&locale=th_th"
        else:
            logger.error(i["url"])
            break
        index+=1
        data = pickle.dumps(item)
        filter_list.append(data)
        redis.rpush(REDIS_KEY, data)
    else:
        continue

