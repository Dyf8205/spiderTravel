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
from lxml import etree
import hashlib
import gzip
import base64
from loguru import logger as logging
from copy import deepcopy
from redis import StrictRedis

logging.add("./logs/trip_get_near_data_to_redis.log", level="ERROR")

M_HOST = "127.0.0.1"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri, maxPoolSize=3)

REDIS_KEY = 'trip_list_near'
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/1'
redis = StrictRedis.from_url(REDIS_URL)

col = mongoclient['trip']["details"]
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)
count = 0
num = 0
for i in cursor:
    count += 1
    url = i['url']
    # 唯一标识符
    pattern = r'self\.__next_f\.push\(\[1,\s*"Jc:\[.*?null,(\{.+?\})\]\\n"\]\)'
    match = re.search(pattern, i["website_snapshot"], re.DOTALL)

    if match:
        try:
            json_str = match.group(1)
            # 处理转义
            json_str = json_str.replace('\\"', '"')
            json_str = json_str.replace('\\\\', '\\')
            baseDict = json.loads(json_str)
            item = {}
            item["latitude"] = baseDict["hotelDetailResponse"]["hotelPositionInfo"]["lat"]
            item["longitude"] = baseDict["hotelDetailResponse"]["hotelPositionInfo"]["lng"]
            item["hotelId"] = baseDict["urlParams"]["hotelId"]
            item["name"] = baseDict["hotelDetailResponse"]["hotelBaseInfo"]["nameInfo"]["name"]
            item["cityId"] = baseDict["hotelDetailResponse"]["hotelBaseInfo"]["cityId"]
            item["countryId"] = baseDict["hotelDetailResponse"]["hotelBaseInfo"]["countryId"]
            data_dict = baseDict
            hotelId = data_dict['hotelId']
            cityId = data_dict['cityId']
            countryId = data_dict['countryId']
            name = data_dict['name']
            latitude = data_dict['latitude']
            longitude = data_dict['longitude']
            logging.info(f"开始采集：{hotelId}")

            import string
            import random


            def generate_random_string(self, length=12):
                # 定义字符集：数字+小写字母+大写字母
                characters = string.ascii_letters + string.digits
                # 随机选择字符并组合
                return ''.join(random.choice(characters) for _ in range(length))


            cid = f"{int(time.time() * 1000)}.{generate_random_string(12)}"
            pageid = f"10{''.join(random.choices('0123456789', k=9))}"

            data = {
                "date": {
                    "dateType": 1,
                    "dateInfo": {
                        "checkInDate": "20260323",
                        "checkOutDate": "20260324"
                    }
                },
                "destination": {
                    "type": 1,
                    "geo": {
                        "cityId": cityId,
                        "countryId": countryId
                    },
                    "keyword": {
                        "word": name
                    }
                },
                "extraFilter": {
                    "childInfoItems": [],
                    "ctripMainLandBDCoordinate": True,
                    "sessionId": "",
                    "extendableParams": {
                        "tripWalkDriveSwitch": "T",
                        "isUgcSentenceB": "",
                        "multiLangHotelNameVersion": "E"
                    }
                },
                "filters": [
                    {
                        "type": "17",
                        "title": "直線距離（由近到遠）",
                        "value": "5",
                        "filterId": "17|5"
                    },
                    {
                        "type": "31",
                        "title": "",
                        "value": str(hotelId),
                        "filterId": "31|" + str(hotelId)
                    },
                    {
                        "type": "80",
                        "title": "每房每晚價格（未連稅及附加費）",
                        "value": "0",
                        "filterId": "80|0|1"
                    },
                    {
                        "filterId": "29|1",
                        "type": "29",
                        "value": "1|2"
                    }
                ],
                "roomQuantity": 1,
                "marketInfo": {
                    "received": False,
                    "isRechargeSuccessful": False,
                    "guideBannerInfo": {
                        "title": "歡迎！預訂住宿即享{0}10%{/0}優惠！",
                        "subItems": [
                            "獲取優惠代碼，節省高達 10%",
                            "下載 App，獲取另一個優惠代碼，節省5%（最多 HK$50）"
                        ],
                        "bannerSubItems": [
                            {
                                "text": "獲取優惠代碼，節省高達 10%",
                                "iconType": "yes"
                            },
                            {
                                "text": "下載 App，獲取另一個優惠代碼，節省5%（最多 HK$50）",
                                "iconType": "yes"
                            },
                            {
                                "text": "使用您的優惠代碼",
                                "iconType": "plus"
                            }
                        ]
                    },
                    "unclaimedActivityInfos": [
                        {
                            "strategyId": 0,
                            "activityId": 349,
                            "property": 5,
                            "couponShowType": ""
                        }
                    ],
                    "authInfo": {
                        "isLogin": False,
                        "isMember": False
                    },
                    "extraInfo": {
                        "SpecialActivityId": "T"
                    }
                },
                "paging": {
                    "pageIndex": 1,
                    "pageSize": 20,
                    "pageCode": str(pageid)
                },
                "hotelIdFilter": {
                    "hotelAldyShown": [
                        str(hotelId)
                    ]
                },
                "recommend": {
                    "searchType": "",
                    "nearbyHotHotel": {
                        "hotelId": str(hotelId),
                        "hotelCityId": cityId,
                        "hotelStar": 3,
                        "hotelName": name,
                        "nearbySubType": "TripHotelList",
                        "coordinate": [
                            {
                                "latitude": latitude,
                                "longitude": longitude,
                                "coordinateType": 1
                            },
                            {
                                "latitude": latitude,
                                "longitude": longitude,
                                "coordinateType": 2
                            }
                        ]
                    }
                },
                "head": {
                    "platform": "PC",
                    "cver": "0",
                    "cid": cid,
                    "bu": "IBU",
                    "group": "trip",
                    "aid": "",
                    "sid": "",
                    "ouid": "",
                    "locale": "zh-HK",
                    "timezone": "8",
                    "currency": "HKD",
                    "pageId": pageid,
                    "vid": cid,
                    "guid": "",
                    "isSSR": False,
                    "extension": [
                        {
                            "name": "cityId",
                            "value": ""
                        },
                        {
                            "name": "checkIn",
                            "value": "2026-03-23"
                        },
                        {
                            "name": "checkOut",
                            "value": "2026-03-24"
                        },
                        {
                            "name": "region",
                            "value": "HK"
                        }
                    ]
                }
            }
            print(json.dumps(data, ensure_ascii=False))
            break
            # data = pickle.dumps(item)
            # redis.rpush(REDIS_KEY, data)
        except Exception as e:
            print(e)
            logging.exception("")
            logging.error(url)
            break
    else:
        logging.error(url)
        break

mongoclient.close()
