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

M_HOST = "111.txt.170.7.65"
M_PORT = 5002
M_USER = "admin"
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
MONGO_URI = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))

def hash_sha1(url):
    # 创建md5对象
    h = hashlib.sha1()
    h.update(url.encode(encoding='utf-8'))
    res = h.hexdigest()
    return res


mongo_client = pymongo.MongoClient(MONGO_URI, maxPoolSize=3)

col = mongo_client["trip"]["area_and_gadm"]
col.create_index("uuid", unique=True)



# 获取当前文件夹下所有 gadm41 开头的 json 文件
files = glob.glob("gadm41*.json")

for jsonfile in files:
    with open(jsonfile, "r", encoding="utf-8") as f:
        res = f.read()

    res_dict = json.loads(res)
    features = res_dict['features']
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
        item['area'] = cityName
        item['uuid'] = hash_sha1(cityName)
        col.update_one({"uuid": item["uuid"]}, {"$set": item}, upsert=True)

mongo_client.close()