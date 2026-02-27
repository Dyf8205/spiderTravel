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



index =0
col = client['trip']['details']  # 查找印尼
cursor = col.find({},{"url":1,"_id":1}, no_cursor_timeout=True, batch_size=5)
for i in cursor:

    id = re.findall("hotel-detail-(.+?)/",i['url'])[0]
    print(index, id)
    index+=1
    try:
        col.update_one({"_id": i['_id']}, {"$set": {"id": id}})
    except pymongo.errors.DuplicateKeyError:
        print(f"删除重复数据 id: {id}, _id: {i['_id']}")
        col.delete_one({"_id": i['_id']})

cursor.close()
print(f"完成，共处理 {index} 条记录")
