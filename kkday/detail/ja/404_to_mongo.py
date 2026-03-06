# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/3/6 10:29
# explain:
# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/3/4 14:46
# explain: 处理从 基础详情后判断是  日本酒店的url  放入redis  准备 重新采集
import pickle
from urllib import parse
from pathlib import Path

import pymongo
from redis import StrictRedis
from loguru import logger
from copy import deepcopy
logger.add(f"./logs/{Path(__file__).stem}.log", mode="w")

# MongoDB配置
M_HOST = "localhost"
M_PORT = 5002
M_USER = "admin"
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = f'mongodb://{M_USER}:{M_PASSWORD}@{M_HOST}:{M_PORT}'
client = pymongo.MongoClient(uri, maxPoolSize=10)


col_404 = client['kkday']["ja_404"]
col_404.create_index("id", unique=True)
def process_collection(collection_name, index):
    """从MongoDB集合读取数据并推送到Redis"""
    col = client['kkday'][collection_name]
    cursor = col.find({"error":"详情页 404"}, { "_id": 0}, no_cursor_timeout=True, batch_size=5)

    for doc in cursor:
        item = deepcopy(doc)
        index += 1
        if index % 5000 ==0:
            logger.info(f"{index}  {item['url']}")
        col_404.update_one({"id": item["id"]}, {"$set": item}, upsert=True)



if __name__ == "__main__":
    index = 0
    collections = ['ja_base_error_urls']

    for collection in collections:
        index = process_collection(collection, index)

    client.close()

