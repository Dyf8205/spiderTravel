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
colhotel = mongoclient['trip2']['seed_hotels']
col = mongoclient['trip']['ids']
num = 0
count = 0
with open("trip_jap_id.txt", "r", encoding="utf-8") as f:
    while True:
        res = f.readline().strip()
        if not res:
            break

        num += 1
        res_find = colhotel.find_one({"id": int(res)})
        if res_find:
            count += 1
            print(f"{num}-{count}")
        else:
            res_find2 = col.find_one({"id": res})
            if res_find2:
                count += 1
                print(f"{num}-{count}")


mongoclient.close()
