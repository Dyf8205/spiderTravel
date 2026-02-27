# -*- coding:utf-8 -*-
import json
import math
import json
from redis import StrictRedis
import pickle
import requests
from urllib import parse
import pymongo
import gzip
import base64
import os
M_HOST = "127.0.0.1"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri)
## 日本
col = client['trip']['ja_jp_final']
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)
filename = "./Trip/Trip_Japan_count_20260225.json"
f = open(filename, "w", encoding="utf-8")
count = 0
for i in cursor:
    del i['_id']
    count += 1
    f.write(json.dumps(i, ensure_ascii=False) + "\n")

f.close()

new_filename = filename.replace("count", str(count))
os.rename(filename, new_filename)
print(f"导出完成，共 {count} 条，文件已重命名为: {new_filename}")

## 印尼
col = client['trip']['id_id_final']
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)
filename = "./Trip/Trip_Indonesia_count_20260225.json"
f = open(filename, "w", encoding="utf-8")
count = 0
for i in cursor:
    del i['_id']
    count += 1
    f.write(json.dumps(i, ensure_ascii=False) + "\n")

f.close()

new_filename = filename.replace("count", str(count))
os.rename(filename, new_filename)
print(f"导出完成，共 {count} 条，文件已重命名为: {new_filename}")


## 马来西亚
col = client['trip']['ms_my_final']
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)
filename = "./Trip/Trip_Malaysia_count_20260225.json"
f = open(filename, "w", encoding="utf-8")
count = 0
for i in cursor:
    del i['_id']
    count += 1
    f.write(json.dumps(i, ensure_ascii=False) + "\n")

f.close()

new_filename = filename.replace("count", str(count))
os.rename(filename, new_filename)
print(f"导出完成，共 {count} 条，文件已重命名为: {new_filename}")


## 泰国
col = client['trip']['th_th_final']
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)
filename = "./Trip/Trip_Thailand_count_20260225.json"
f = open(filename, "w", encoding="utf-8")
count = 0
for i in cursor:
    del i['_id']
    count += 1
    f.write(json.dumps(i, ensure_ascii=False) + "\n")

f.close()

new_filename = filename.replace("count", str(count))
os.rename(filename, new_filename)
print(f"导出完成，共 {count} 条，文件已重命名为: {new_filename}")




client.close()