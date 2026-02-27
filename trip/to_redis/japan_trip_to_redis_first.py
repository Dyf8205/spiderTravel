# -*- coding:utf-8 -*-
import json
import math
import json
from redis import StrictRedis
import pickle
import requests
from urllib import parse
import pymongo
import hashlib
import re
M_HOST = "localhost"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri)

# redis配置
REDIS_KEY = 'trip_detail'
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/1'
redis = StrictRedis.from_url(REDIS_URL)

filter_list =[]

def hash_sha1(url):
    # 创建md5对象
    h = hashlib.sha1()
    h.update(url.encode(encoding='utf-8'))
    res = h.hexdigest()
    return res

index =0
col = client['trip_before2']['seed_hotels']  # 查找找日本
cursor = col.find({"districtName": {"$regex": "Japan"}}, no_cursor_timeout=True, batch_size=5)
for i in cursor:
    item = dict()
    item['url'] = "https://jp.trip.com" + i['url'] + "?curr=JPY&locale=ja_jp"
    item['id'] = re.findall("hotel-detail-(.+?)/",i['url'])[0]
    print(item)
    index+=1
    data = pickle.dumps(item)
    # 添加到商品爬虫redis_key指定的list
    if data not in filter_list:
    # 添加到商品爬虫redis_key指定的list
        filter_list.append(data)
        redis.rpush(REDIS_KEY, data)



col = client['trip_before2']['seed_hotels2']  # 查找找日本
cursor = col.find({"districtName": {"$regex": "Japan"}}, no_cursor_timeout=True, batch_size=5)
for i in cursor:
    item = dict()
    item['url'] = "https://jp.trip.com" + i['url'] + "?curr=JPY&locale=ja_jp"
    item['id'] = re.findall("hotel-detail-(.+?)/",i['url'])[0]
    print(item)
    index+=1
    data = pickle.dumps(item)
    # 添加到商品爬虫redis_key指定的list
    if data not in filter_list:
    # 添加到商品爬虫redis_key指定的list
        filter_list.append(data)
        redis.rpush(REDIS_KEY, data)

print(f"trip一共有japan {index} 家hotels")
client.close()
