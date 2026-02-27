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

REDIS_KEY = 'trip_list'
REDIS_URL = 'redis://:ABFSDD@ABFS!&rh@127.0.0.1:5000/1'
redis = StrictRedis.from_url(REDIS_URL)

M_HOST = "127.0.0.1"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("ABFSDD@ABFS!&rh")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri)
colarea = mongoclient['trip2']['area']
colarea.ensure_index("area", unique=True)

colcountry = mongoclient['trip2']['country']
colcountry.ensure_index("country", unique=True)

col = mongoclient['trip']['ids']
cursor = col.find({})
count = 0
num = 0
for i in cursor:
    dataSource = i['dataSource']
    if dataSource != "TRIP":
        continue

    try:
        newContent = i['newContent']
        item_content = dict()
        item_content['area'] = newContent
        try:
            colarea.insert(item_content, check_keys=False)
        except:
            pass

        item_country = dict()
        country = newContent.split(", ")[-1]
        item_country['country'] = country
        try:
            colcountry.insert(item_country, check_keys=False)
        except:
            pass


    except:
        pass


mongoclient.close()
