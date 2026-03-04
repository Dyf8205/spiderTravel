# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/11 17:02
# explain: 多进程版本 - 爬虫进程，结果放入Redis队列
import re
import requests
import pickle
from get_proxy import get_proxies, get_random_proxy
from loguru import logger
from lxml import etree
import time
import random
import os
from urllib import parse
from redis import StrictRedis
from datetime import datetime
import json
from multiprocessing import Process

logger.add("./logs/kkday.log",mode="w")

# 配置
REDIS_KEY = 'ja_kkday_base_detail'
REDIS_RESULT_KEY = 'ja_kkday_result'  # 结果队列
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/1'
MAX_QUEUE_SIZE = 500  # 结果队列最大长度，超过则等待

PROCESS_NUM = 100  # 进程数量


def get_redis():
    """获取Redis连接"""
    return StrictRedis.from_url(REDIS_URL)


def worker(worker_id):
    """工作进程 - 只负责爬取，结果放入Redis队列"""
    time.sleep(worker_id * 0.3)  # 错开启动
    redis_client = get_redis()

    logger.info(f"Worker {worker_id} started, pid: {os.getpid()}")

    try:
        while True:
            item = redis_client.rpop(REDIS_KEY)
            if item is None:
                logger.info(f"Worker {worker_id}: Redis 队列为空，退出")
                break

            baseData = pickle.loads(item)
            baseUrl = baseData["url"]

            data = {}
            data["url"] = baseUrl
            data["id"] = baseData["id"]
            try:
                for index in range(5):
                    try:
                        session = requests.Session()
                        headers = {
                            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                            'accept-language': 'en-US,en;q=0.9',
                            'cache-control': 'no-cache',
                            'pragma': 'no-cache',
                            'priority': 'u=0, i',
                            'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'document',
                            'sec-fetch-mode': 'navigate',
                            'sec-fetch-site': 'same-origin',
                            'sec-fetch-user': '?1',
                            'upgrade-insecure-requests': '1',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
                        }
                        response = session.get(baseUrl, headers=headers, proxies=get_random_proxy(),timeout=40)
                        break
                    except Exception as e:
                        if index == 4:
                            raise Exception("详情页访问失败" )
                        pass

                logger.info("详情页" + str(response.status_code))
                if response.status_code != 200:
                    raise Exception(f"详情页 {response.status_code}")

                data["website_snapshot"] = response.text
                data["response_url"] = response.url
                if "__INIT_STATE__" not in response.text and "application/ld+json" not in response.text:
                    raise Exception("判断失败 出现新的内容")

                formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data["crawl_time"] = formatted_time
                data["success"] = True

                # 等待队列有空间
                while redis_client.llen(REDIS_RESULT_KEY) > MAX_QUEUE_SIZE:
                    time.sleep(1)

                # 放入结果队列
                redis_client.lpush(REDIS_RESULT_KEY, pickle.dumps(data))
                logger.success(f"Worker {worker_id}: 成功 " + baseUrl)

            except Exception as e:
                logger.error(f"Worker {worker_id}: " + str(e))
                logger.error(baseData["url"] + str(e))
                data = {}
                data["url"] = baseUrl
                data["id"] = baseData["id"]
                data['error'] = str(e)
                data["success"] = False

                # 放入结果队列
                redis_client.lpush(REDIS_RESULT_KEY, pickle.dumps(data))

    finally:
        redis_client.close()
        logger.info(f"Worker {worker_id} finished")


def main():
    processes = []

    for i in range(PROCESS_NUM):
        p = Process(target=worker, args=(i,))
        p.start()
        processes.append(p)
        logger.info(f"Started worker {i}")

    for p in processes:
        p.join()

    logger.info("All workers finished")


if __name__ == '__main__':
    main()
