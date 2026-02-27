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
col = mongoclient['trip']['ids']
listcol = mongoclient['trip']['list']
cursor = listcol.find({})
count = 0
num = 0
for i in cursor:
    count += 1
    id = i['id']
    res_find = col.find_one({"id": id})
    if res_find:
        continue

    num += 1
    print(f"{count}-{num}")





mongoclient.close()