# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/3/5 18:11
# explain:


from redis import StrictRedis
import pickle
import requests
from urllib import parse
import pymongo
import hashlib
from pathlib import Path
from loguru import logger
logger.add(f"./logs/{Path(__file__).stem}.log",mode="w")

M_HOST = "localhost"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@1218!xGxG")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri,maxPoolSize=10)

# redis配置
REDIS_KEY = 'doordash_detail'
REDIS_URL = 'redis://:grad@1218!!xGxG@127.0.0.1:5001/1'
redis = StrictRedis.from_url(REDIS_URL)

filter_list = []

def hash_sha1(url):
    # 创建md5对象
    h = hashlib.sha1()
    h.update(url.encode(encoding='utf-8'))
    res = h.hexdigest()
    return res

# 第一步：从 doordash.details 获取已有的 id，存入 Redis 集合
logger.info("开始从 doordash.details 获取已有 id...")
details_col = client['doordash']['details']
details_cursor = details_col.find({}, {"id": 1}, no_cursor_timeout=True, batch_size=1000)

REDIS_FILTER_KEY = 'doordash_detail_ids_filter'
# 清空旧的过滤集合
redis.delete(REDIS_FILTER_KEY)

detail_count = 0
for detail in details_cursor:
    if 'id' in detail:
        redis.sadd(REDIS_FILTER_KEY, detail['id'])
        detail_count += 1
        if detail_count % 10000 == 0:
            logger.info(f"已加载 {detail_count} 个 detail id 到过滤集合")

details_cursor.close()
logger.info(f"完成加载，共 {detail_count} 个 detail id")

# 第二步：从 doordash.sitemap 获取数据，通过 id 去重后打入 REDIS_KEY
logger.info("开始从 doordash.sitemap 获取数据并过滤...")
index = 0
pushed_count = 0
col = client['doordash']['sitemap']
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)

for i in cursor:
    item = dict()
    item["url"] = i["url"]
    item['id'] = i["id"]
    index += 1

    # 通过 Redis 集合判断 id 是否已存在
    if not redis.sismember(REDIS_FILTER_KEY, item['id']):
        data = pickle.dumps(item)
        redis.rpush(REDIS_KEY, data)
        pushed_count += 1

        if pushed_count % 1000 == 0:
            logger.info(f"已推送 {pushed_count} 条新数据到 Redis")

    if index % 5000 == 0:
        logger.info(f"已处理 {index} 条 sitemap 数据，推送 {pushed_count} 条")

cursor.close()
logger.info(f"完成！共处理 {index} 条 sitemap 数据，推送 {pushed_count} 条新数据到 {REDIS_KEY}")

