# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/3/4 14:46
# explain: 处理从 基础详情后判断是  日本酒店的url  放入redis  准备 重新采集
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
from pathlib import Path
from loguru import logger
logger.add(f"./logs/{Path(__file__).stem}",mode="w")

M_HOST = "localhost"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri,maxPoolSize=10)

# redis配置
REDIS_KEY = 'ja_kkday_base_detail'
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
col = client['kkday']['ja_sitemap']
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)



for i in cursor:


    item = dict()
    item["url"] = i["url"]
    item['id'] = i["id"]
    index+=1
    logger.info(f"{index}  {item['url']}")
    data = pickle.dumps(item)
    redis.rpush(REDIS_KEY, data)

