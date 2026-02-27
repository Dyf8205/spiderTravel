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

# 用于比较的 redis key
TRIP_IDS_KEY = 'trip_detail_ids_check'
IMAGE_IDS_KEY = 'trip_image_json_ids_check'

# 先清空之前的记录
redis.delete(TRIP_IDS_KEY)
redis.delete(IMAGE_IDS_KEY)
print(f"清空后 TRIP_IDS_KEY 数量: {redis.scard(TRIP_IDS_KEY)}")
print(f"清空后 IMAGE_IDS_KEY 数量: {redis.scard(IMAGE_IDS_KEY)}")

# 先用 count_documents 验证数量
col = client['trip']['details']
col2 = client['trip_image_json']['details']
print(f"\n=== MongoDB count_documents 验证 ===")
print(f"trip.details count_documents: {col.count_documents({})}")
print(f"trip_image_json.details count_documents: {col2.count_documents({})}")
print()

# 加载 trip.details 的所有 id
col = client['trip']['details']
cursor = col.find({}, {"id": 1, "_id": 0}, no_cursor_timeout=True, batch_size=1000)
trip_count = 0
for i in cursor:
    redis.sadd(TRIP_IDS_KEY, i['id'])
    trip_count += 1
print(f"trip.details 遍历文档数: {trip_count}")
print(f"trip.details 去重后数量: {redis.scard(TRIP_IDS_KEY)}")

# 加载 trip_image_json.details 的所有 id
col2 = client['trip_image_json']['details']
cursor2 = col2.find({}, {"id": 1, "_id": 0}, no_cursor_timeout=True, batch_size=1000)
image_count = 0
for i in cursor2:
    redis.sadd(IMAGE_IDS_KEY, i['id'])
    image_count += 1
print(f"trip_image_json.details 遍历文档数: {image_count}")
print(f"trip_image_json.details 去重后数量: {redis.scard(IMAGE_IDS_KEY)}")

# 找出差异
# trip 中有但 trip_image_json 中没有的
only_in_trip = redis.sdiff(TRIP_IDS_KEY, IMAGE_IDS_KEY)
print(f"\n=== trip 中有但 trip_image_json 中没有的 ({len(only_in_trip)} 条) ===")
for id_bytes in only_in_trip:
    id_val = id_bytes.decode() if isinstance(id_bytes, bytes) else id_bytes
    print(id_val)

# trip_image_json 中有但 trip 中没有的
only_in_image = redis.sdiff(IMAGE_IDS_KEY, TRIP_IDS_KEY)
print(f"\n=== trip_image_json 中有但 trip 中没有的 ({len(only_in_image)} 条) ===")
for id_bytes in only_in_image:
    id_val = id_bytes.decode() if isinstance(id_bytes, bytes) else id_bytes
    print(id_val)

# 清理
redis.delete(TRIP_IDS_KEY)
redis.delete(IMAGE_IDS_KEY)


client.close()



