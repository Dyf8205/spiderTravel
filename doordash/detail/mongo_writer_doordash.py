# -*- coding:UTF-8 -*-
# author:dyf
# explain: MongoDB写入进程，从Redis队列读取数据写入MongoDB
import pickle
import pymongo
from redis import StrictRedis
from urllib import parse
from loguru import logger
import os
from multiprocessing import Process

# 配置
REDIS_RESULT_KEY = 'doordash_result'
REDIS_URL = 'redis://:grad@1218!!xGxG@127.0.0.1:5001/1'

M_HOST = "127.0.0.1"
M_PORT = 5002
M_USER = "admin"
M_PASSWORD = parse.quote_plus("grad@1218!xGxG")
MONGO_URI = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))

WRITER_NUM = 1  # 写入进程数量

logger.add("./logs/doordash_writer.log",mode="w")

def writer(writer_id):
    """写入进程"""
    logger.add(f"./logs/mongo_writer_{writer_id}_{os.getpid()}.log")

    redis_client = StrictRedis.from_url(REDIS_URL)
    mongo_client = pymongo.MongoClient(MONGO_URI, maxPoolSize=3)

    # 初始化集合
    collist = mongo_client["doordash"].list_collection_names()
    if "details" not in collist:
        col = mongo_client["doordash"]["details"]
        col.create_index("id", unique=True)
    if "error_urls" not in collist:
        col = mongo_client["doordash"]["base_error_urls"]
        col.create_index("id", unique=True)

    success_col = mongo_client["doordash"]["details"]
    error_col = mongo_client["doordash"]["base_error_urls"]

    logger.info(f"Writer {writer_id} started, pid: {os.getpid()}")

    empty_count = 0
    try:
        while True:
            item = redis_client.brpop(REDIS_RESULT_KEY, timeout=10)  # 阻塞等待10秒

            if item is None:
                empty_count += 1
                logger.info(f"Writer {writer_id}: 队列为空，等待中... ({empty_count})")
                if empty_count >= 60:  # 连续5分钟没数据就退出
                    logger.info(f"Writer {writer_id}: 长时间无数据，退出")
                    break
                continue

            empty_count = 0
            data = pickle.loads(item[1])

            try:
                if False == data["success"]:
                    error_col.update_one({"id": data["id"]}, {"$set": data}, upsert=True)
                    logger.info(f"Writer {writer_id}: 写入错误记录 {data['id']}")
                else:
                    success_col.update_one({"id": data["id"]}, {"$set": data}, upsert=True)
                    logger.success(f"Writer {writer_id}: 写入成功 {data['url']}")
            except Exception as e:
                logger.error(f"Writer {writer_id}: 写入失败 {e}")
                # 写入失败放回队列
                redis_client.lpush(REDIS_RESULT_KEY, pickle.dumps(data))

    finally:
        redis_client.close()
        mongo_client.close()
        logger.info(f"Writer {writer_id} finished")


def main():
    processes = []

    for i in range(WRITER_NUM):
        p = Process(target=writer, args=(i,))
        p.start()
        processes.append(p)
        logger.info(f"Started writer {i}")

    for p in processes:
        p.join()

    logger.info("All writers finished")


if __name__ == '__main__':
    main()
