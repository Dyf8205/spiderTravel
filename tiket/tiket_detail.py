# -*- coding: utf-8 -*-
import base64
import hashlib
import pickle
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


class GoogleMapsSpider(RedisSpider):
    name = 'tiket_detail'
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
            'HuaweiProject.middlewares.CurlCffiMiddleware': 546,
            # 'HuaweiProject.middlewares.RandomUserAgentMiddleware': 543,

            'HuaweiProject.middlewares.ProxiesZHANDAYEMiddleware': 545,
            'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 547,  # 权重值需要小于ProcessAllExceptionMiddleware
            'HuaweiProject.middlewares.ProcessAllExceptionMiddleware': 548,  # 权重值需要小于550
        },
        'ITEM_PIPELINES': {
            'HuaweiProject.pipelines.ExpediaMongodbPipeline': 300,
        },
    }

    redis_key = 'tiket_detail'

    def __init__(self, *args, **kwargs):
        self.db_name = "tiket"
        super(GoogleMapsSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        """
        根据redis中读取的分类信息的二进制数据, 构建请求
        :param data: url信息的二进制数据
        :return: 构建的请求对象
        """
        data_dict = pickle.loads(data)
        url = data_dict['url']
        id = data_dict['id']
        logging.info(f"开始采集：{url}")

        # url = "https://httpbin.org/get?show_env=1"
        # url = "https://tls.peet.ws/api/all"
        item = dict()
        item['url'] = url
        item['id'] = id

        return scrapy.Request(
            url=url,
            callback=self.parse_around,
            meta={'item': deepcopy(item)},
            dont_filter=True
        )

    def parse_around(self, response):
        # logging.info(response.text)
        # return

        item_temp = response.meta["item"]
        url = item_temp['url']
        id = item_temp['id']

        if '300*=*=*' in response.url:
            logging.warning('300重定向 {}'.format(response.url))
            error_item = dict()
            error_item['url'] = response.url
            error_item['id'] = id
            error_item['type'] = '300重定向异常'
            error_item['other_args'] = {}
            error_item['other_args']['db'] = self.db_name
            error_item['other_args']['table_name'] = 'error_urls'
            yield error_item
            return

        if '400or500*=*=*' in response.url:
            logging.error('400or500 {}'.format(response.url))
            error_item = dict()
            error_item['url'] = url
            error_item['id'] = id
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
            error_item['url'] = url
            error_item['id'] = id
            error_item['type'] = 'exception'
            error_item['detail'] = ''
            error_item['other_args'] = {}
            error_item['other_args']['db'] = self.db_name
            error_item['other_args']['table_name'] = 'error_urls'
            yield error_item
            return

        try:
            res = response.xpath("//script[@id='__NEXT_DATA__']/text()").get()
            item = dict()
            item['url'] = url
            item['response_url'] = response.url
            item['id'] = id
            item['result'] = json.loads(res)
            item['other_args'] = {}
            item['other_args']['db'] = self.db_name
            item['other_args']['table_name'] = 'details'
            yield item

        except Exception as e:
            logging.error('解析异常 {}'.format(response.url))
            error_item = dict()
            error_item['url'] = url
            error_item['id'] = id
            error_item['type'] = 'analysis error'
            error_item['detail'] = traceback.format_exc()
            error_item['response'] = response.text
            error_item['other_args'] = {}
            error_item['other_args']['db'] = self.db_name
            error_item['other_args']['table_name'] = 'error_urls'
            yield error_item
