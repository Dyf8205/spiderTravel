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
    name = 'trip_hotel_list'
    # allowed_domains = ['lbs.amap.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'RETRY_ENABLED': True,
        'DOWNLOAD_TIMEOUT': 50,
        'RETRY_HTTP_CODES': [418, 419, 429, 500, 502, 503, 504, 509, 403, 509, 407],
        'RETRY_TIMES': 10,
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

    redis_key = 'trip_hotel_list'

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
        self.db_name = "trip2"

        super(GoogleMapsSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        """
        根据redis中读取的分类信息的二进制数据, 构建请求
        :param data: url信息的二进制数据
        :return: 构建的请求对象
        """
        data_dict = pickle.loads(data)
        cityName = data_dict['cityName']
        pageIndex = data_dict['pageIndex']
        logging.info(f"开始采集：{cityName}-第{pageIndex}页")

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://us.trip.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://us.trip.com/",
            # "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            # "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": random.choice(self.useragent_list)
        }
        # url = "https://www.trip.com/restapi/soa2/20400/getResultForTripOnline"
        url = "https://www.trip.com/restapi/soa2/20400/getGsMainResultForTripOnline"
        data = {
            "keyword": cityName,
            "lang": "en",
            "locale": "en-US",
            "currency": "USD",
            "pageIndex": pageIndex,
            "pageSize": 200,
            "tab": "hotel",
            "head": {
                "cver": "3.0",
                "auth": None,
                # "cid": "1762267681196.6ef3LgHqXvNL",
                "syscode": "999",
                "locale": "en-US",
                "extension": [
                    {
                        "name": "locale",
                        "value": "en-US"
                    },
                    {
                        "name": "platform",
                        "value": "Online"
                    },
                    {
                        "name": "currency",
                        "value": "USD"
                    }
                ]
            }
        }



        item = dict()
        item['pageIndex'] = pageIndex
        item['cityName'] = cityName

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
        pageIndex = item_temp['pageIndex']
        cityName = item_temp['cityName']

        if '300*=*=*' in response.url:
            logging.warning('300重定向 {}'.format(response.url))
            error_item = dict()
            # error_item['cityId'] = cityId
            error_item['id'] = f"{cityName}==={pageIndex}"
            error_item['type'] = '300重定向异常'
            error_item['other_args'] = {}
            error_item['other_args']['db'] = self.db_name
            error_item['other_args']['table_name'] = 'error_urls'
            yield error_item
            return

        if '400or500*=*=*' in response.url:
            logging.error('400or500 {}'.format(response.url))
            error_item = dict()
            # error_item['cityId'] = cityId
            error_item['id'] = f"{cityName}==={pageIndex}"
            error_item['type'] = '400 or 500'
            error_item['detail'] = ''

            error_item['other_args'] = {}
            error_item['other_args']['db'] = self.db_name
            error_item['other_args']['table_name'] = 'error_urls'
            yield error_item
            return

        if 'exception*=*=*' in response.url:
            logging.error('exception {}'.format(response.url))
            error_item = dict()
            # error_item['cityId'] = cityId
            error_item['id'] = f"{cityName}==={pageIndex}"
            error_item['type'] = 'exception'
            error_item['detail'] = ''
            error_item['other_args'] = {}
            error_item['other_args']['db'] = self.db_name
            error_item['other_args']['table_name'] = 'error_urls'
            yield error_item
            return

        try:
            res_dict = json.loads(response.text)
            hotelList = res_dict['data'][0]['itemList']
            for hotel_dict in hotelList:
                hotel_dict['other_args'] = dict()
                hotel_dict['other_args']['db'] = self.db_name
                hotel_dict['other_args']['table_name'] = 'seed_hotels2'
                yield hotel_dict

            try:
                item_total = dict()
                item_total['other_args'] = dict()
                item_total['other_args']['db'] = self.db_name
                item_total['other_args']['table_name'] = 'area_count'
                item_total["id"] = cityName
                item_total["count"] = res_dict['data'][0]['resultTab']['total']
                yield item_total
            except:
                pass

            isLastPage = res_dict['isLastPage']
            if not isLastPage:
                pageIndex += 1
                if pageIndex > 3:
                    return
                logging.info(f"开始采集：{cityName}-第{pageIndex}页")
                headers = {
                    "accept": "application/json, text/plain, */*",
                    "accept-language": "zh-CN,zh;q=0.9",
                    "cache-control": "no-cache",
                    "content-type": "application/json",
                    "origin": "https://us.trip.com",
                    "pragma": "no-cache",
                    "priority": "u=1, i",
                    "referer": "https://us.trip.com/",
                    # "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
                    "sec-ch-ua-mobile": "?0",
                    # "sec-ch-ua-platform": "\"Windows\"",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "user-agent": random.choice(self.useragent_list)
                }
                # url = "https://www.trip.com/restapi/soa2/20400/getResultForTripOnline"
                url = "https://www.trip.com/restapi/soa2/20400/getGsMainResultForTripOnline"
                data = {
                    "keyword": cityName,
                    "lang": "en",
                    "locale": "en-US",
                    "currency": "USD",
                    "pageIndex": pageIndex,
                    "pageSize": 200,
                    "tab": "hotel",
                    "head": {
                        "cver": "3.0",
                        "auth": None,
                        # "cid": "1762267681196.6ef3LgHqXvNL",
                        "syscode": "999",
                        "locale": "en-US",
                        "extension": [
                            {
                                "name": "locale",
                                "value": "en-US"
                            },
                            {
                                "name": "platform",
                                "value": "Online"
                            },
                            {
                                "name": "currency",
                                "value": "USD"
                            }
                        ]
                    }
                }

                item = dict()
                item['pageIndex'] = pageIndex
                item['cityName'] = cityName

                yield scrapy.FormRequest(
                    url=url,
                    callback=self.parse_around,
                    headers=headers,
                    body=json.dumps(data, separators=(',', ':')),
                    method='POST',
                    meta={'item': deepcopy(item)},
                    dont_filter=True
                )

        except Exception as e:
            logging.error('解析异常 {}'.format(response.url))
            error_item = dict()
            # error_item['cityId'] = cityId
            error_item['id'] = f"{cityName}==={pageIndex}"
            error_item['type'] = 'analysis error'
            error_item['detail'] = traceback.format_exc()
            error_item['response'] = response.text
            error_item['other_args'] = {}
            error_item['other_args']['db'] = self.db_name
            error_item['other_args']['table_name'] = 'error_urls'
            yield error_item

    def generate_random_string(self, length=12):
        # 定义字符集：数字+小写字母+大写字母
        characters = string.ascii_letters + string.digits
        # 随机选择字符并组合
        return ''.join(random.choice(characters) for _ in range(length))
