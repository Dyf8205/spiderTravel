# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/3/4
# explain: 从 MongoDB base_details 集合去重后，将新数据推送到 Redis

import pymongo
from urllib import parse
from redis import StrictRedis
import pickle
from loguru import logger

logger.add("./logs/base_deatail_kkday_to_redis_again.log", mode="w")

# MongoDB 配置
M_HOST = "localhost"
M_PORT = 5002
M_USER = "admin"
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri, maxPoolSize=10)

# Redis 配置
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/1'
redis = StrictRedis.from_url(REDIS_URL)

REDIS_KEY = 'kkday_base_detail'
REDIS_SET_KEY = "base_detail:existing_ids"
BATCH_SIZE = 5000

# Step 1: 清理旧的去重集合
redis.delete(REDIS_SET_KEY)
logger.info("已清理旧的去重集合")

# Step 2: 从 base_details 集合加载已存在的 id 到 Redis Set
count = 0
pipe = redis.pipeline()

base_details_col = mongoclient['kkday']['base_details']
cursor = base_details_col.find({}, {"id": 1, "url": 1}, no_cursor_timeout=True, batch_size=5)

for doc in cursor:
    doc_id = doc.get("id")
    if doc_id:
        pipe.sadd(REDIS_SET_KEY, doc_id)
        count += 1
        if count % BATCH_SIZE == 0:
            pipe.execute()
            pipe = redis.pipeline()
            logger.info(f"[加载已存在数据] 已写入 {count} 条")

pipe.execute()
cursor.close()
logger.info(f"[加载已存在数据] 完成，base_details 共 {count} 条 id")

# Step 3: 遍历 sitemap 集合，找出新增的数据并推送到 Redis 队列
sitemap_col = mongoclient['kkday']['sitemap']
cursor = sitemap_col.find({}, {"id": 1, "url": 1}, no_cursor_timeout=True, batch_size=5)

index = 0
new_count = 0

for doc in cursor:
    doc_id = doc.get("id")
    doc_url = doc.get("url")

    if doc_id and not redis.sismember(REDIS_SET_KEY, doc_id):
        # 不存在于 base_details，推送到 Redis 队列
        item = {
            "url": doc_url,
            "id": doc_id
        }
        data = pickle.dumps(item)
        redis.rpush(REDIS_KEY, data)
        new_count += 1
        logger.info(f"{new_count}  新增: {item['url']}")

    index += 1
    if index % BATCH_SIZE == 0:
        logger.info(f"[扫描进度] 已扫描 {index} 条，新增 {new_count} 条")

cursor.close()

# Step 4: 清理去重集合
redis.delete(REDIS_SET_KEY)

logger.info(f"[完成] 共扫描 {index} 条，新增 {new_count} 条数据到 Redis 队列")
