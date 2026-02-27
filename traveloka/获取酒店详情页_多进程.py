# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/11 17:02
# explain: 多进程版本 - 爬虫进程，结果放入Redis队列
import re
import requests
import pickle
from awswaf.aws import AwsWaf
from urllib.parse import urlparse
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

# 配置
REDIS_KEY = 'traveloka_detail'
REDIS_RESULT_KEY = 'traveloka_result'  # 结果队列
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/1'
MAX_QUEUE_SIZE = 500  # 结果队列最大长度，超过则等待

PROCESS_NUM = 80  # 进程数量


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
            path = re.findall(r"https://www\.traveloka\.com/(.+?)/hotel", baseUrl)[0]
            data = {}
            data["url"] = baseUrl
            data["uuid"] = baseData["uuid"]

            if path == "id-id":
                tv_country = "ID"
                tv_currency = 'IDR'
                tv_language = 'id_ID'
                x_route_prefix = "id-id"
                currency = 'IDR'
            elif path == "ja-jp":
                tv_country = "JP"
                tv_currency = 'JPY'
                tv_language = 'ja_JP'
                x_route_prefix = "ja-jp"
                currency = 'JPY'
            else:
                logger.error(f'url path 解析出现新的国家 {path}')
                continue

            try:
                for index in range(5):
                    try:
                        session = requests.Session()
                        headers = {
                            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                            'accept-language': 'zh-CN,zh;q=0.9',
                            'cache-control': 'no-cache',
                            'pragma': 'no-cache',
                            'priority': 'u=0, i',
                            'referer': baseUrl,
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
                        response = session.get(baseUrl, headers=headers, proxies=get_random_proxy(),timeout=30)
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
                try:
                    etree.HTML(response.content).xpath("//script[@id='__NEXT_DATA__']/text()")[0]
                except Exception as e:
                    raise Exception("详情页访问失败")

                # 获取亚马逊token
                for index in range(5):
                    try:
                        goku, host = AwsWaf.extract(response.text)
                        token = AwsWaf(goku, host, urlparse(baseUrl).netloc, get_random_proxy())()
                        break
                    except Exception as e:
                        if index == 4:
                            raise Exception("token 获取失败")
                        pass

                logger.info(token)
                headers = {
                    'accept': '*/*',
                    'accept-language': 'zh-CN,zh;q=0.9',
                    'cache-control': 'no-cache',
                    'content-type': 'application/json',
                    'origin': 'https://www.traveloka.com',
                    'pragma': 'no-cache',
                    'priority': 'u=1, i',
                    'referer': baseUrl,
                    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="144", "Chromium";v="144"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'tv-country': tv_country,
                    'tv-currency': tv_currency,
                    'tv-language': tv_language,
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
                    'x-client-interface': 'desktop',
                    'x-domain': 'accomRoom',
                    'x-route-prefix': x_route_prefix,
                }

                def ue():
                    e = random.randint(0, 999999988)
                    t = random.randint(0, 999999988)
                    return f"{e}{t}"

                fbp = f"fb.1.{int(time.time() * 1000 + 20000)}.{ue()}"
                timestamp = str(int(time.time() * 1000 + 30000))
                json_data = {
                    'fields': [],
                    'data': {
                        'contexts': {
                            'hotelDetailURL': baseUrl,
                            'bookingId': None,
                            'sourceIdentifier': 'HOTEL_DETAIL',
                            'shouldDisplayAllRooms': False,
                            'marketingContextCapsule': {
                                'fb_browser_id_fbp': fbp,
                                'timestamp': timestamp,
                                'initial_page_full_url': baseUrl.split("/hotel/")[0] + "/hotel",
                                'initial_timestamp': timestamp,
                                'page_full_url': baseUrl,
                                'client_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
                            },
                        },
                        'prevSearchId': 'undefined',
                        'numInfants': 0,
                        'ccGuaranteeOptions': {
                            'ccInfoPreferences': ['CC_TOKEN', 'CC_FULL_INFO'],
                            'ccGuaranteeRequirementOptions': ['CC_GUARANTEE'],
                        },
                        'rateTypes': ['PAY_NOW', 'PAY_AT_PROPERTY'],
                        'isJustLogin': False,
                        'isReschedule': False,
                        'monitoringSpec': {'referrer': baseUrl},
                        'hotelId': baseUrl.split("?cur=")[0].split("/")[-1].split("-")[-1],
                        'currency': currency,
                        'labelContext': {},
                        'isExtraBedIncluded': False,
                        'hasPromoLabel': False,
                        'supportedRoomHighlightTypes': ['ROOM'],
                        'checkInDate': {'day': '20', 'month': '3', 'year': '2026'},
                        'checkOutDate': {'day': '21', 'month': '3', 'year': '2026'},
                        'numOfNights': 1,
                        'numAdults': 1,
                        'numRooms': 1,
                        'numChildren': 0,
                        'childAges': [],
                        'tid': 'ae75aca7-5e60-4239-ae57-529d8fc4ab7f',
                    },
                    'clientInterface': 'desktop',
                }

                session.cookies.update({"aws-waf-token": token})

                for index in range(5):
                    try:
                        room_response = session.post(
                            'https://www.traveloka.com/api/v2/hotel/search/rooms',
                            headers=headers,
                            json=json_data,
                            proxies=get_random_proxy(),
                            timeout=30
                        )
                        break
                    except Exception as e:
                        if index == 4:
                            raise Exception("room 失败 " + str(e))

                data["roomJson"] = room_response.text

                if room_response.json()["data"]["status"] != "SUCCESS":
                    raise Exception("room 失败")

                headers = {
                    'accept': '*/*',
                    'accept-language': 'zh-CN,zh;q=0.9',
                    'cache-control': 'no-cache',
                    'content-type': 'application/json',
                    'origin': 'https://www.traveloka.com',
                    'pragma': 'no-cache',
                    'priority': 'u=1, i',
                    'referer': baseUrl,
                    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Microsoft Edge";v="144"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'tv-country': tv_country,
                    'tv-currency': tv_currency,
                    'tv-language': tv_language,
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0',
                    'x-client-interface': 'desktop',
                    'x-domain': 'content',
                    'x-route-prefix': x_route_prefix,
                }

                json_data = {
                    'fields': [],
                    'data': {
                        'productId': baseUrl.split("?cur=")[0].split("/")[-1].split("-")[-1],
                        'productType': 'ACCOMMODATION',
                        'productSubtype': None,
                        'filters': None,
                        'subFilters': None,
                        'page': 2,
                        'size': 10,
                        'sort': None,
                    },
                    'clientInterface': 'desktop',
                }

                for j in range(5):
                    try:
                        traverler_response = session.post(
                            'https://www.traveloka.com/api/v2/explore/media-gallery/traveler',
                            headers=headers,
                            json=json_data,
                            proxies=get_random_proxy(),
                            timeout=30
                        )
                        break
                    except Exception as e:
                        if j == 4:
                            raise Exception('Traveler 接口获取不是200 ' +str(e))

                if traverler_response.status_code != 200:
                    raise Exception('Traveler 接口获取不是200')

                traverler_response.json()["data"]["items"]
                data["traverlerJson"] = traverler_response.text

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
                data["uuid"] = baseData["uuid"]
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
