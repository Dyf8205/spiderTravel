# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/24 10:11
# explain:
# -*- coding:utf-8 -*-
import json
import math
import json
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
REDIS_KEY = 'kkday_base_detail'
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/1'
redis = StrictRedis.from_url(REDIS_URL)


def hash_sha1(url):
    # 创建md5对象
    h = hashlib.sha1()
    h.update(url.encode(encoding='utf-8'))
    res = h.hexdigest()
    return res

index=0
col = client['kkday']['base_error_urls']  #查找错误的
cursor = col.find({"error":{"$ne": "详情页 404"}}, no_cursor_timeout=True, batch_size=5)
for i in cursor:

    item = dict()
    item['url'] = i['url']
    item['id'] =  i["id"]
    print(item)
    index+=1
    data = pickle.dumps(item)
    # 添加到商品爬虫redis_key指定的list
    redis.rpush(REDIS_KEY, data)
print(f"{index}条数据需要重新采集")
client.close()
