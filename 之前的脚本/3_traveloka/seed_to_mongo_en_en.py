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
M_PASSWORD = parse.quote_plus("0820RH@ABFSDD!&rh")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri)
col = mongoclient['traveloka']['seed_en_sg']
col.ensure_index("uuid", unique=True)

def hash_sha1(url):
    # 创建md5对象
    h = hashlib.sha1()
    h.update(url.encode(encoding='utf-8'))
    res = h.hexdigest()
    return res

path = "/mnt/jiao/website/traveloka/sitemap/en-sg/"
filenames = os.listdir(path)
filenames.sort()
for filename in filenames:
    with open(path + filename, "r", encoding="utf-8") as f:
        res_str = f.read()

    res = re.findall("<loc>(.+?)</loc>", res_str)
    print(f"{filename}-{len(res)}")
    for j in res:
        item = dict()
        item['url'] = j
        item['uuid'] = hash_sha1(j)
        try:
            col.insert(item, check_keys=False)
        except:
            pass

mongoclient.close()
