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
from lxml import etree
import hashlib
import gzip
import base64
from loguru import logger as logging
from copy import deepcopy
from redis import StrictRedis

logging.add("./logs/trip_get_near_data_to_redis.log",level="ERROR")

M_HOST = "127.0.0.1"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri,maxPoolSize=3)


REDIS_KEY = 'trip_list_near'
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/1'
redis = StrictRedis.from_url(REDIS_URL)


col = mongoclient['trip']["details"]
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)
count = 0
num = 0
for i in cursor:
    count += 1
    url = i['url']
     # 唯一标识符
    pattern = r'self\.__next_f\.push\(\[1,\s*"Jc:\[.*?null,(\{.+?\})\]\\n"\]\)'
    match = re.search(pattern, i["website_snapshot"], re.DOTALL)

    if match:
        json_str = match.group(1)
        # 处理转义
        json_str = json_str.replace('\\"', '"')
        json_str = json_str.replace('\\\\', '\\')
        baseDict = json.loads(json_str)
    else:
        logging.error(url)


    item = {}

    item["latitude"] = baseDict["hotelDetailResponse"]["hotelPositionInfo"]["lat"]
    item["longitude"] = baseDict["hotelDetailResponse"]["hotelPositionInfo"]["lng"]
    item["hotelId"] = baseDict["urlParams"]["hotelId"]
    item["name"] =  baseDict["hotelDetailResponse"]["hotelBaseInfo"]["nameInfo"]["name"]
    item["cityId"] =   baseDict["hotelDetailResponse"]["hotelBaseInfo"]["cityId"]
    item["countryId"] = baseDict["hotelDetailResponse"]["hotelBaseInfo"]["countryId"]

    data = pickle.dumps(item)
    redis.rpush(REDIS_KEY, data)



mongoclient.close()
