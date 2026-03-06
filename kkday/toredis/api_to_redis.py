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

logger.add(f"./logs/{Path(__file__).stem}.log", mode="w")

# MongoDB配置
M_HOST = "localhost"
M_PORT = 5002
M_USER = "admin"
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = f'mongodb://{M_USER}:{M_PASSWORD}@{M_HOST}:{M_PORT}'
client = pymongo.MongoClient(uri, maxPoolSize=10)

# Redis配置
REDIS_KEY = 'kkday_detail_api'
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/1'
redis = StrictRedis.from_url(REDIS_URL)


def process_collection(collection_name, index):
    """从MongoDB集合读取数据并推送到Redis"""
    col = client['kkday'][collection_name]
    cursor = col.find({}, {"url": 1, "id": 1}, no_cursor_timeout=True, batch_size=5)

    for doc in cursor:
        item = {"url": doc["url"], "id": doc["id"]}
        index += 1
        if index % 5000 ==0:
            logger.info(f"{index}  {item['url']}")
        redis.rpush(REDIS_KEY, pickle.dumps(item))

    return index


if __name__ == "__main__":
    index = 0
    collections = ['ja_sitemap', 'us_detail', 'id_detail']

    for collection in collections:
        index = process_collection(collection, index)

    client.close()

