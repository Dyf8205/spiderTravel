# -*- coding:utf-8 -*-
import json
import math
import json
import re

from redis import StrictRedis
import pickle
import requests
from urllib import parse
import pymongo
import hashlib
from loguru import logger

logger.add("./logs/trip-to-redis.log")
M_HOST = "localhost"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri)

# redis配置
REDIS_KEY = 'trip_image_json'
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/1'
redis = StrictRedis.from_url(REDIS_URL)


def hash_sha1(url):
    # 创建md5对象
    h = hashlib.sha1()
    h.update(url.encode(encoding='utf-8'))
    res = h.hexdigest()
    return res


index = 0
col = client['trip_image_json']['error_urls']
col_detail = client['trip']['details']
# 错误类型是400or500的 都是没有相关详情页面的数据

cursor = col.find({},{'url': 1, 'id': 1, '_id': 0}, no_cursor_timeout=True, batch_size=5)

for j in cursor:

    i = col.find_one({"id":j["id"]},{'url': 1, 'id': 1, '_id': 0})
    print(i)
    item = dict()
    if "https://jp.trip.com" in i["url"]:
        url = 'https://jp.trip.com/restapi/soa2/28820/ctgethotelalbum'
        item["data"] = {
            'hotelId': 6070530,
            'versionControl': [
                {
                    'key': 'EnableVideo',
                    'value': 'T',
                },
            ],
            'head': {
                'platform': 'PC',
                'cver': '0',
                'bu': 'IBU',
                'group': 'trip',
                'aid': '',
                'sid': '',
                'ouid': '',
                'locale': 'ja-JP',
                'region': 'JP',
                'timezone': '8',
                'currency': 'JPY',
                'pageId': '10320668147',
                'guid': '',
                'isSSR': False,
                'extension': [
                    {
                        'name': 'cityId',
                        'value': '',
                    },
                    {
                        'name': 'checkIn',
                        'value': '',
                    },
                    {
                        'name': 'checkOut',
                        'value': '',
                    },
                ],
            },
        }
    elif "https://id.trip.com" in i["url"]:
        url = 'https://id.trip.com/restapi/soa2/28820/ctgethotelalbum'
        item["data"] = {
            'hotelId': 109405328,
            'versionControl': [
                {
                    'key': 'EnableVideo',
                    'value': 'F',
                },
            ],
            'head': {
                'platform': 'PC',
                'cver': '0',
                'bu': 'IBU',
                'group': 'trip',
                'aid': '',
                'sid': '',
                'ouid': '',
                'locale': 'id-ID',
                'region': 'ID',
                'timezone': '8',
                'currency': 'IDR',
                'pageId': '10320668147',
                'guid': '',
                'isSSR': False,
                'extension': [
                    {
                        'name': 'cityId',
                        'value': '',
                    },
                    {
                        'name': 'checkIn',
                        'value': '',
                    },
                    {
                        'name': 'checkOut',
                        'value': '',
                    },
                ],
            },
        }
    elif "https://my.trip.com" in i["url"]:
        url = 'https://my.trip.com/restapi/soa2/28820/ctgethotelalbum'
        item["data"] = {
            'hotelId': 128833168,
            'versionControl': [
                {
                    'key': 'EnableVideo',
                    'value': 'F',
                },
            ],
            'head': {
                'platform': 'PC',
                'cver': '0',

                'bu': 'IBU',
                'group': 'trip',
                'aid': '',
                'sid': '',
                'ouid': '',
                'locale': 'ms-MY',
                'region': 'MY',
                'timezone': '8',
                'currency': 'MYR',
                'pageId': '10320668147',

                'guid': '',
                'isSSR': False,
                'extension': [
                    {
                        'name': 'cityId',
                        'value': '',
                    },
                    {
                        'name': 'checkIn',
                        'value': '',
                    },
                    {
                        'name': 'checkOut',
                        'value': '',
                    },
                ],
            },
        }
    elif "https://th.trip.com" in i["url"]:
        url = 'https://th.trip.com/restapi/soa2/28820/ctgethotelalbum'
        item["data"] = {
            'hotelId': 12486039,
            'versionControl': [
                {
                    'key': 'EnableVideo',
                    'value': 'F',
                },
            ],
            'head': {

                'ctok': '',
                'cver': '0',
                'lang': '01',
                'sid': '',
                'syscode': '09',
                'auth': '',
                'xsid': '',
                'extension': [
                    {
                        'name': 'cityId',
                        'value': '',
                    },
                    {
                        'name': 'checkIn',
                        'value': '',
                    },
                    {
                        'name': 'checkOut',
                        'value': '',
                    },
                ],
                'Locale': 'th-TH',
                'Language': 'th',
                'Currency': 'THB',

                'platform': 'PC',
                'bu': 'IBU',
                'group': 'trip',
                'aid': '',
                'ouid': '',
                'locale': 'th-TH',
                'region': 'TH',
                'timezone': '8',
                'currency': 'THB',
                'pageId': '10320668147',
                'guid': '',
                'isSSR': False,
            },
        }
    else:
        logger.error(json.dumps(i, indent=4, sort_keys=True) + " 出现新的域名 ")
    item['url'] = url
    item['id'] =i["id"]

    item["data"]["hotelId"] = int(i["id"])
    print(i["url"]+ "  " +str(item["data"]["hotelId"]))
    index += 1
    data = pickle.dumps(item)
    # 添加到商品爬虫redis_key指定的list
    redis.rpush(REDIS_KEY, data)

print(f"trip{index} 条接口数据")
client.close()
