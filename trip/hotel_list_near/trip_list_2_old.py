# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/27 17:44
# explain:
# -*- coding: utf-8 -*-
import base64
import hashlib
import pickle
import string

from scrapy.exceptions import CloseSpider
import pymongo
import requests
from scrapy_redis.spiders import RedisSpider
import scrapy
import re
import json
from copy import deepcopy
import logging
import traceback
from urllib import parse
import os
import uuid
import random
import time


class GoogleMapsSpider(RedisSpider):
    name = 'trip_list2'
    # allowed_domains = ['lbs.amap.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'RETRY_ENABLED': True,
        'DOWNLOAD_TIMEOUT': 50,
        'RETRY_HTTP_CODES': [418, 419, 429, 500, 502, 503, 504, 509, 403, 509, 407],
        'RETRY_TIMES': 5,
        "DOWNLOADER_MIDDLEWARES": {
            # 'HuaweiProject.middlewares.RandomUserAgentMiddleware': 543,
            # 'HuaweiProject.middlewares.CurlCffiMiddleware': 546,
            'HuaweiProject.middlewares.ProxiesZHANDAYEMiddleware': 545,
            'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 547,  # 权重值需要小于ProcessAllExceptionMiddleware
            'HuaweiProject.middlewares.ProcessAllExceptionMiddleware': 548,  # 权重值需要小于550
        },
        'ITEM_PIPELINES': {
            'HuaweiProject.pipelines.ExpediaMongodbPipeline': 300,
        },
    }

    redis_key = 'trip_list_near'

    def __init__(self, *args, **kwargs):
        self.useragent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        ]
        self.db_name = "trip"

        super(GoogleMapsSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        """
        根据redis中读取的分类信息的二进制数据, 构建请求
        :param data: url信息的二进制数据
        :return: 构建的请求对象
        """

        headers = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "cookieorigin": "https://hk.trip.com",
            "origin": "https://hk.trip.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://hk.trip.com",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": random.choice(self.useragent_list),
        }
        url = "https://hk.trip.com/restapi/soa2/34951/fetchRecommendList"
        data_dict = pickle.loads(data)
        hotelId = data_dict['hotelId']
        cityId = data_dict['cityId']
        countryId = data_dict['countryId']
        name = data_dict['name']
        latitude = data_dict['latitude']
        longitude = data_dict['longitude']
        logging.info(f"开始采集：{hotelId}")
        cid = f"{int(time.time() * 1000)}.{self.generate_random_string(12)}"
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

        # url = "https://httpbin.org/get?show_env=1"
        # url = "https://tls.peet.ws/api/all"

        item = dict()
        item['hotelId'] = hotelId
        item['cityId'] = cityId

        yield scrapy.FormRequest(
            url=url,
            callback=self.parse_around,
            headers=headers,
            body=json.dumps(data, separators=(',', ':')),
            method='POST',
            meta={'item': deepcopy(item)},
            dont_filter=True
        )

    def parse_around(self, response):
        item_temp = response.meta["item"]
        hotelId = item_temp['hotelId']
        cityId = item_temp['cityId']
        # logging.info(response.text)
        # return

        if '300*=*=*' in response.url:
            logging.warning('300重定向 {}'.format(response.url))
            error_item = dict()
            error_item['cityId'] = cityId
            error_item['id'] = hotelId
            error_item['type'] = '300重定向异常'
            error_item['other_args'] = {}
            error_item['other_args']['db'] = self.db_name
            error_item['other_args']['table_name'] = 'error_urls_near'
            yield error_item
            return

        if '400or500*=*=*' in response.url:
            logging.error('400or500 {}'.format(response.url))
            error_item = dict()
            error_item['cityId'] = cityId
            error_item['id'] = hotelId
            error_item['type'] = '400 or 500'
            error_item['detail'] = ''

            error_item['other_args'] = {}
            error_item['other_args']['db'] = self.db_name
            error_item['other_args']['table_name'] = 'error_urls_near'
            yield error_item
            return

        if 'exception*=*=*' in response.url:
            logging.error('exception {}'.format(response.url))
            error_item = dict()
            error_item['cityId'] = cityId
            error_item['id'] = hotelId
            error_item['type'] = 'exception'
            error_item['detail'] = ''
            error_item['other_args'] = {}
            error_item['other_args']['db'] = self.db_name
            error_item['other_args']['table_name'] = 'error_urls_near'
            yield error_item
            return

        try:
            hotelList = json.loads(response.text)['data']['recommendHotel']['hotelList']
            for hotel_dict in hotelList:
                try:
                    hotel_dict['id'] = hotel_dict['hotelInfo']['summary']['hotelId']
                except:
                    logging.error("hotel_dict['id'] = hotel_dict['hotelInfo']['summary']['hotelId']")
                    continue
                hotel_dict['other_args'] = dict()
                hotel_dict['other_args']['db'] = self.db_name
                hotel_dict['other_args']['table_name'] = 'hotel_list_near'
                yield hotel_dict

        except Exception as e:
            logging.error('解析异常 {}'.format(response.url))
            error_item = dict()
            error_item['cityId'] = cityId
            error_item['id'] = hotelId
            error_item['type'] = 'analysis error'
            error_item['detail'] = traceback.format_exc()
            error_item['response'] = response.text
            error_item['other_args'] = {}
            error_item['other_args']['db'] = self.db_name
            error_item['other_args']['table_name'] = 'error_urls_near'
            yield error_item

    def generate_random_string(self, length=12):
        # 定义字符集：数字+小写字母+大写字母
        characters = string.ascii_letters + string.digits
        # 随机选择字符并组合
        return ''.join(random.choice(characters) for _ in range(length))
