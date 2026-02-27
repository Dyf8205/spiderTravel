# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/11 17:02
# explain:
import re

import requests
import pickle
from awswaf.aws import AwsWaf
from urllib.parse import urlparse
from get_proxy import get_proxies,get_random_proxy
from loguru import logger
from lxml import etree
import time
import random
import os
from urllib import parse
import pymongo
from redis import StrictRedis
from datetime import datetime
logger.add(f"./logs/travelka_details{os.getpid()}.log",)
import json

REDIS_KEY = 'traveloka_detail'
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/1'
redis = StrictRedis.from_url(REDIS_URL)

M_HOST = "127.0.0.1"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri)



collist = mongoclient["traveloka"].list_collection_names()

if "details" not in collist:
     col =  mongoclient["traveloka"]["details"]
     col.create_index("uuid", unique=True)
if "error_urls" not in collist:
    col = mongoclient["traveloka"]["error_urls"]
    col.create_index("uuid", unique=True)

success_col = mongoclient["traveloka"]["details"]
error_col = mongoclient["traveloka"]["error_urls"]

while True:
    item = redis.rpop("traveloka_detail") #从redis获取 详情页链接
    if item is None:
        break

    baseData = pickle.loads(item)
    baseUrl = baseData["url"]
    path = re.findall("https://www\.traveloka\.com/(.+?)/hotel",baseUrl)[0]  #获取地区标志
    data = {}
    data["url"] = baseUrl
    data["uuid"]  = baseData["uuid"]
    if path == "id-id":   # 用于处理请求头等具体信息
        tv_country = "ID"
        tv_currency = 'IDR'
        tv_language = 'id_ID'
        x_route_prefix = "id-id"
        currency = 'IDR'
    elif path == "ja-jp":
        tv_country = "JP"
        tv_currency = 'JPY'
        tv_language= 'ja_JP'
        x_route_prefix = "ja-jp"
        currency = 'JPY'
    else:
        raise Exception(f'url path 解析出现新的国家 {path}')

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

                response = session.get(baseUrl, headers=headers, proxies=get_random_proxy())
                break
            except:
                if index ==4:
                    raise Exception("详情页 非200")
                pass


        logger.info("详情页" + str(response.status_code))
        if response.status_code != 200:
            raise Exception("详情页 非200")

        # with open("详情页.html", "w", encoding="utf") as f:
        #     f.write(response.text)
        data["website_snapshot"] = response.text
        data["response_url"] = response.url
        etree.HTML(response.content).xpath("//script[@id='__NEXT_DATA__']/text()")[0]  # 用来判断数据是否正常

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
            # 't-a-v': '262152',
            # 'tv-clientsessionid': 'T1-web.01KJ1GDVF0NFBXW826VFVS81XZ',
            'tv-country': tv_country,
            'tv-currency': tv_currency,
            'tv-language': tv_language,
            # 'tv-mcc-id': '01KJ1GE1SV0FWR67BN3NX1NBN1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            # 'www-app-version': 'release_webacd_20260212-5fdaea5fa1',
            'x-client-interface': 'desktop',
            # 'x-did': 'MDFLSjFHRTFUWDVLN1JFVEVFQU1ZN1BDNE4=',
            'x-domain': 'accomRoom',
            'x-route-prefix': x_route_prefix,
            # 'cookie': 'clientSessionId=T1-web.01KJ1GDVF0NFBXW826VFVS81XZ; tv_lt=1771724795360; tv_cs=1; datadome=FTiIzGb0FZZc_kjQzQ94x28oGGsutMzpqWDM8TIm8GyFA61sItQtyflTWdmBjFh4kxB2Oe4jEG56w29VTepz1F52_xCPJfPo2~uh1a0IyZTKbGTn1770Bw4vw7rpft_a; aws-waf-token=7ff5e537-2fb4-4964-993d-c986a556bfd3:AgoApLIK4EoXAAAA:1ZcypKQ9hn5Bi6TsfvBamK73U968N8PZvzACkjX6Ql+QVABnLzai5u68EQ0FWABTNdMf+aAgv55gR3kuHGJp98bvCIvZ1No73CKV0CsPIULgyHTgbfWue6HRj7S1xwmz7J03Q3R4s232sDdoEaSp71ORsxTyFYjPqrQFouv8OuN7HCiQSoazvR/hafqB/6M9DTc=; tv-repeat-visit=true; tv_mcc_id=01KJ1GE1SV0FWR67BN3NX1NBN1; _dd_s=rum=0&expire=1771725701882&logs=1&id=91df5a9e-912f-45b0-a2f5-d8b3573fb170&created=1771724801882; countryCode=CN; tv_user={"authorizationLevel":100,"id":null}; tvl=qgdHX7GvehrD9XH5a3S4PUiOJGezXQ9yizVaSxTklwrLYY64AE4apiD1qmHRGaV8gGAQoV6xR5wi1hxtboYegx0JoHbuxL9J5IDMykh7yrn/kmgjvZe3CXlrOt5A94G1h8SGYm0D03zEW7S7g02l9zkAPbkMGQ6AJj+0Bs51j2ci2542wrWiZiqC1He68olpLIhAYrrfgxgwH0A9OA47otShoMf2ODrNss0LV9I2JQ8/q20nK1P8fo7+Vm0FVb5qaSGwHQzQQDA7bnV/TO/HO34BvcVRTQ9w2GyG0ZXjzTbM0WMA1zSky7I1/5su3gOq3hD2k6rZCP5V+wjmo86w0uz9qkSgM2rpVdsDzaEw+zMPrnXJ1JZhX10HvYL38k0lxbVWc9mUJC6U6r8wkx04c+4CDTx/jJt5ZXoEQTwGFtmvFcCuLSwzN6i0oSIN7Me1qAF7deTrMY+NA0g3ss4OLA==; tvs=qgdHX7GvehrD9XH5a3S4PXWKx93/3Xi103f/kPpnhg3OSo3cGZrh1hhvLQxZwJnicHn5NHIgVN8BbvrNvAgFRvcs37PX6fQ3qANKZ9dxg/QnCKTXxoKBXBgRJAoECuhbd+gyQzq70AhHhvg65it3EHJ8QJVLDxjwhIbxYg4fKH9bPZBZuDO5H0NNMHQUyz3UHuDnJqjeQFkKDArygq4lbMQNdiOIdbdo3NOzN10CC0HQLgLfVAHzIKBP7HlPTDPnY4bl360Z5o4iFx0PKn+v+ycuR09QG+/6KEYnOYGqNYBcwfhjpkLnjYzB9UovvgjC2cKqT4UBkDl8LUsuy3Il27PSN1MqvullUU9JKDdNhvrWP6OvimOVeMSLYUjIR9mP; tvo=L2FwaS92Mi9ob3RlbC9jYWxlbmRhci9ob3RlbA==',
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
                        'initial_page_full_url': baseUrl.split("/hotel/")[0]+"/hotel",
                        'initial_timestamp': timestamp,
                        'page_full_url': baseUrl,
                        'client_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
                    },
                },
                'prevSearchId': 'undefined',
                'numInfants': 0,
                'ccGuaranteeOptions': {
                    'ccInfoPreferences': [
                        'CC_TOKEN',
                        'CC_FULL_INFO',
                    ],
                    'ccGuaranteeRequirementOptions': [
                        'CC_GUARANTEE',
                    ],
                },
                'rateTypes': [
                    'PAY_NOW',
                    'PAY_AT_PROPERTY',
                ],
                'isJustLogin': False,
                'isReschedule': False,
                'monitoringSpec': {
                    'referrer': baseUrl,
                },
                'hotelId': baseUrl.split("?cur=")[0].split("/")[-1].split("-")[-1],
                'currency': currency,
                'labelContext': {},
                'isExtraBedIncluded': False,
                'hasPromoLabel': False,
                'supportedRoomHighlightTypes': [
                    'ROOM',
                ],
                'checkInDate': {
                    'day': '20',
                    'month': '3',
                    'year': '2026',
                },
                'checkOutDate': {
                    'day': '21',
                    'month': '3',
                    'year': '2026',
                },
                'numOfNights': 1,
                'numAdults': 1,
                'numRooms': 1,
                'numChildren': 0,
                'childAges': [],
                'tid': 'ae75aca7-5e60-4239-ae57-529d8fc4ab7f',
            },
            'clientInterface': 'desktop',
        }

        session.cookies.update({
            "aws-waf-token": token})

        for index in range(5):
            try:
                room_response = session.post('https://www.traveloka.com/api/v2/hotel/search/rooms', headers=headers, json=json_data,
                                             proxies=get_random_proxy(),timeout=30)
                break
            except:
                if index ==4:
                    raise Exception("room 失败")

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
            # 't-a-v': '262268',
            # 'tv-clientsessionid': 'T1-web.01KH7ZDTK6EMV8QTRMVFATE7SA',
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
                    proxies=get_random_proxy(),timeout=30
                )
                break
            except:
                if index ==4:
                    raise Exception('Traveler 接口获取不是200')

        if traverler_response.status_code != 200:
            raise Exception('Traveler 接口获取不是200')

        traverler_response.json()["data"]["items"]

        data["traverlerJson"] = traverler_response.text #用户上传的信息

        # 格式化时间为所需的格式
        formatted_time =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["crawl_time"] = formatted_time

        success_col.update_one({"uuid": data["uuid"]}, {"$set": data}, upsert=True)
        logger.success("成功 "+baseUrl)

    except Exception as e:
        logger.error(str(e))
        logger.error(baseData["url"] + str(e))
        data = {}
        data["url"] = baseUrl
        data["uuid"] = baseData["uuid"]
        data['error'] = str(e)
        error_col.update_one({"uuid": data["uuid"]}, {"$set": data}, upsert=True)



mongoclient.close()