# -*- coding:utf-8 -*-
import json
import math
import json
import re

from redis import StrictRedis
import pickle
import requests
from urllib import parse
import pymongo
import hashlib

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

def hash_sha1(url):
    # 创建md5对象
    h = hashlib.sha1()
    h.update(url.encode(encoding='utf-8'))
    res = h.hexdigest()
    return res

index =0
col = client['trip']['.']
cursor = col.find({},{"url":1,"_id":1,"id":1}, no_cursor_timeout=True, batch_size=5)


col_img = client['trip_image_json']['.']

missing = []

for i in cursor:
    idvalue = i.get("id")
    if not idvalue:
        index += 1
        print(f"跳过无id记录: {index}, _id: {i['_id']}")
        continue

    exists = col_img.find_one({"id": idvalue}, {"_id": 1})
    index += 1
    if not exists:
        missing.append(idvalue)
        print(f"[缺失] {index}, id: {idvalue}")
    else:
        print(f"[存在] {index}, id: {idvalue}")

cursor.close()
print(f"\n完成，共检查 {index} 条记录")
print(f"trip_image_json.details 中缺失的id数量: {len(missing)}")
if missing:
    print("缺失的id列表:")
    for m in missing:
        print(f"  {m}")
