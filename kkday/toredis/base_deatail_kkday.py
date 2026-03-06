# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/25 17:08
# explain:
# -*- coding:utf-8 -*-
import json
import logging
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

logger.add("./logs/base_deatail_kkday_to_redis.log",mode="w")

M_HOST = "localhost"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri,maxPoolSize=10)

# redis配置
REDIS_KEY = 'kkday_base_detail'
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
col = client['kkday']['sitemap']
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)


for i in cursor:


    item = dict()
    item["url"] = i["url"]
    item['id'] = i["id"]
    index+=1
    logger.info(f"{index}  {item['url']}")
    data = pickle.dumps(item)
    redis.rpush(REDIS_KEY, data)

