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

M_HOST = "127.0.0.1"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("ABFSDD@ABFS!&rh")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri)
col = mongoclient['trip2']['seed_citys']
col.ensure_index("cityName", unique=True)

with open("city_urls.json", "r", encoding="utf-8") as f:
    while True:
        res = f.readline().strip()
        if not res:
            break
        res_dict = json.loads(res)
        try:
            col.insert(res_dict, check_keys=False)
        except Exception as e:
            print(e)
            pass



mongoclient.close()