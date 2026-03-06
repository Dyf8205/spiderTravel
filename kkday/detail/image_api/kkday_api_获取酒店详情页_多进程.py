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

logger.add("./logs/kkday.log", mode="w")

# 配置
REDIS_KEY = 'kkday_detail_api'
REDIS_RESULT_KEY = 'kkday_result_api'  # 结果队列
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/1'
MAX_QUEUE_SIZE = 500  # 结果队列最大长度，超过则等待

PROCESS_NUM = 10  # 进程数量


def get_redis():
    """获取Redis连接"""
    return StrictRedis.from_url(REDIS_URL)


def download(params, result_len,baseurl):
    for index in range(5):
        try:
            session = requests.Session()
            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                # 'referer': 'https://www.kkday.com/en-us/hotel/product/188904?location_id=D-3325&location_title=Universal%20Studio%20Japan&location_type=Area&check_in=2026-03-05&check_out=2026-03-06&rooms=1&adults=2',
                'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                # 'cookie': 'csrf_cookie_name=4478158490b1bcaff3f253ceed44ee95; KKWEB=a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%221633daaacae352f3a8a26a98c75698ab%22%3Bs%3A7%3A%22channel%22%3Bs%3A5%3A%22GUEST%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1772721313%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7Dd504e41cb1090c3956222296922ef6f5; country_lang=en-us; currency=USD; KKUD=1633daaacae352f3a8a26a98c75698ab; datadome=S~Fh79~6_cIHboRlMjOkW4bK6co9_CdkDWxVauGXMFVwXHXJ3wa16yZb4HwU5D0MebMh2ptd1FZ9NsGK7zkRznhBd79LWu9FPGkff0EpFRHUF_8q3AmNQxpzstfqrs7d',
            }
            if "/ja/" in baseurl:
                headers["market"] = "ja"
            response = session.get('https://www.kkday.com/api/_nuxt/cpath/fetch-product-comment-images',
                                   params=params, headers=headers, proxies=get_random_proxy(),
                                   timeout=40)
            session.close()
            break
        except Exception as e:
            if index == 4:
                raise Exception("详情页访问失败")
            pass

    logger.info("详情页" + str(response.status_code))
    if response.status_code != 200:
        if response.status_code == 500 and result_len != 0:
            return None
        raise Exception(f"详情页 {response.status_code}")

    try:
        response.json()["data"]["meta"]["pagination"]["totalPages"]
    except:
        raise Exception("解析失败")

    return response


def worker(worker_id):
    """工作进程 - 只负责爬取，结果放入Redis队列"""
    time.sleep(worker_id * 0.3)  # 错开启动
    redis_client = get_redis()

    logger.info(f"Worker {worker_id} started, pid: {os.getpid()}")
    while True:
        try:

            item = redis_client.rpop(REDIS_KEY)
            if item is None:
                logger.info(f"Worker {worker_id}: Redis 队列为空，退出")
                break

            baseData = pickle.loads(item)

            data = {}
            data["id"] = baseData["id"]
            params = {
                'prodId': str(re.findall("(\d+)", data["id"])[0]),
                'page': '1',
            }
            response_list = []

            response = download(params, response_list.__len__(),baseData["url"])
            response_list.append(response.text)
            totalPages = response.json()["data"]["meta"]["pagination"]["totalPages"]

            for page in range(2, totalPages + 1):  # 需要翻页的 用户照片
                params["page"] = str(page)
                response = download(params, response_list.__len__(),baseData["url"])
                if response == None:
                    break
                response_list.append(response.text)

            data["website_snapshot"] = json.dumps(response_list)
            if response !=None:
                data["response_url"] = response.url
            formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data["crawl_time"] = formatted_time
            data["success"] = True

            # 等待队列有空间
            while redis_client.llen(REDIS_RESULT_KEY) > MAX_QUEUE_SIZE:
                time.sleep(1)
            # 放入结果队列
            redis_client.lpush(REDIS_RESULT_KEY, pickle.dumps(data))
            logger.success(f"Worker {worker_id}: 成功 " + data["id"])

        except Exception as e:
            logger.error(f"Worker {worker_id}: " + str(e))
            logger.error(baseData["url"] + str(e))
            data = {}
            data["id"] = baseData["id"]
            data["url"] = baseData["url"]
            data['error'] = str(e)
            data["success"] = False
            # 放入结果队列
            redis_client.lpush(REDIS_RESULT_KEY, pickle.dumps(data))

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
