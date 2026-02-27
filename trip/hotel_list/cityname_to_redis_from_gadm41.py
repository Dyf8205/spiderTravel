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
import glob
import os

# redis配置
from redis import StrictRedis

REDIS_KEY = 'trip_hotel_list'
REDIS_URL = 'redis://:ABFSDD@ABFS!&rh@127.0.0.1:5000/1'
redis = StrictRedis.from_url(REDIS_URL)



# 获取当前文件夹下所有 gadm41 开头的 json 文件
files = glob.glob("gadm41*.json")

for jsonfile in files:


    with open(jsonfile, "r", encoding="utf-8") as f:
        res = f.read()

    res_dict = json.loads(res)
    features = res_dict['features']
    print(jsonfile)
    print(len(features))
    for feature in features:
        country = feature['properties']["COUNTRY"]
        NAME_1 = feature['properties']['NAME_1']
        NAME_2 = feature['properties']['NAME_2']
        NAME_3 = feature['properties'].get('NAME_3',None)
        if NAME_3 != None:
            cityName = f"{NAME_3}, {NAME_2}, {NAME_1}, {country}"
        else:
            cityName = f"{NAME_2}, {NAME_1}, {country}"

        item = dict()
        item['pageIndex'] = 1
        item['cityName'] = cityName
        # item['cityName'] = "Tokyo"
        # print(item)
        # data = pickle.dumps(item)
        # # 添加到商品爬虫redis_key指定的list
        # redis.rpush(REDIS_KEY, data)