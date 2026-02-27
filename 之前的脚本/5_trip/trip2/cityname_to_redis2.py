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
import hashlib
import os


# redis配置
from redis import StrictRedis

REDIS_KEY = 'trip_hotel_list'
REDIS_URL = 'redis://:ABFSDD@ABFS!&rh@127.0.0.1:5000/1'
redis = StrictRedis.from_url(REDIS_URL)

# with open("C:\\Users\\Administrator\\Desktop\\gadm41_JPN_2.json", "r", encoding="utf-8") as f:
with open("gadm41_JPN_2.json", "r", encoding="utf-8") as f:
    res = f.read()

res_dict = json.loads(res)
features = res_dict['features']
print(len(features))
for feature in features:
    NAME_1 = feature['properties']['NAME_1']
    NAME_2 = feature['properties']['NAME_2']
    cityName = f"{NAME_2}, {NAME_1}, Japan"

    item = dict()
    item['pageIndex'] = 1
    item['cityName'] = cityName
    # item['cityName'] = "Tokyo"
    print(item)
    data = pickle.dumps(item)
    # 添加到商品爬虫redis_key指定的list
    redis.rpush(REDIS_KEY, data)