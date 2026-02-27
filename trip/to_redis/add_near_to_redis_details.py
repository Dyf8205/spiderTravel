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

logger.add("./logs/add_near_to_redis_details.log",mode="w")

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
col = client['trip']['hotel_list_near']
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)

filter_col =  client['trip']['details']


for i in cursor:
    countryId = int(i['hotelInfo']['positionInfo']['countryId'])
    hotelId = str(i['hotelInfo']['summary']['hotelId'])

    item = dict()

    item['id'] = hotelId
    isIn = filter_col.find_one({'id': item['id']}, {'_id':1})
    if isIn ==None:

        if 108 == countryId:  #108 印尼
            item['url'] = "https://id.trip.com/hotels/detail/?hotelId=" + hotelId + "&curr=IDR&locale=id_id"
        elif 78 == countryId: # 78  日本
            item['url'] = "https://jp.trip.com/hotels/detail/?hotelId=" + hotelId +"&curr=JPY&locale=ja_jp"
        elif  2 == countryId: # 2  马来西亚
            item['url'] = "https://my.trip.com/hotels/detail/?hotelId=" + hotelId +"&locale=ms_my&curr=MYR"
        elif  4 == countryId: # 4 泰国
            item['url'] = "https://th.trip.com/hotels/detail/?hotelId=" + hotelId +"&curr=THB&locale=th_th"
        else:
            logger.error(f"{hotelId}  {countryId}"  )
            continue
        index+=1
        logger.info(f"{index}  {item['url']}")
        data = pickle.dumps(item)
        redis.rpush(REDIS_KEY, data)
    else:
        continue

