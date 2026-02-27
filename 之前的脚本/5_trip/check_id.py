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
cursor = col.find({})
count = 0
num = 0
for i in cursor:
    num += 1
    displayType = i['displayType']
    if displayType != "酒店":
        continue
    code = i['code']
    if code.isdigit():
        count += 1
        print(f"{num}-{count}")




mongoclient.close()