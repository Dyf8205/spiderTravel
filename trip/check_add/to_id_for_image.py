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
col = client['trip']['details']
cursor = col.find({},{"url":1,"_id":1,"id":1}, no_cursor_timeout=True, batch_size=5)


col_img = client['trip_image_json']['details']


for i in cursor:

    uuid = hash_sha1(i["url"].split("?")[0].split("trip.com")[-1])
    idvalue = i["id"]

    # 用uuid查找trip_image_json中的数据
    docs = list(col_img.find({"id": uuid}))
    if len(docs) > 0:
        # 更新第一条
        col_img.update_one({"_id": docs[0]['_id']}, {"$set": {"id": idvalue}})
        # 删除多余的重复数据
        if len(docs) > 1:
            for d in docs[1:]:
                col_img.delete_one({"_id": d['_id']})
                print(f"删除重复数据 uuid: {uuid}, _id: {d['_id']}")
    index += 1
    print(index, idvalue, uuid)

cursor.close()
print(f"完成，共处理 {index} 条记录")
