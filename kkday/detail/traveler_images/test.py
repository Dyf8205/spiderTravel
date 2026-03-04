# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/3/5 16:47
# explain:

import re
import requests
import pickle

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
from loguru import logger
logger.add("./logs/image_api.log",mode="w")
def get_random_proxy():
    """
    随机从文件中读取proxy
    """
    while True:
        try:
            # 127.0.0.1:5007
            proxy_all_list = json.loads(requests.get("http://119.3.172.62:5007/get_all").text)
            if len(proxy_all_list) < 50:
                time.sleep(10)
                continue

            response = requests.get("http://119.3.172.62:5007/get")
            proxies = json.loads(response.text)['proxy']
            if proxies:
                break
            else:
                time.sleep(10)
        except:
            time.sleep(10)

    proxy = proxies

    proxy if proxy.startswith('http') else 'http://' + proxy


    proxies = {
        "http": proxy,
        "https": proxy,
    }
    return proxies


headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'market': 'en-us',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.kkday.com/en-us/product/2852-okinawa-bus-tour-churaumi-aquarium-kouri-island-manzamo-nago-pineapple-park-japan',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Microsoft Edge";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0',
    # 'x-csrf-token': '9b78c18c-35f2-4787-8589-9f8ff21c99e0',
    # 'cookie': 'i18n_redirected=en-us; csrf_token=9b78c18c-35f2-4787-8589-9f8ff21c99e0; KKWEB=a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%224f30522584bbb1a8b21c3818276cdfac%22%3Bs%3A7%3A%22channel%22%3Bs%3A5%3A%22GUEST%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1772700314%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D1d49921b712879792d51d62a8a5cbfe5; country_lang=en-us; lang_ui=en; currency=USD; KKUD=4f30522584bbb1a8b21c3818276cdfac; _ga_E1FBF68JQF=GS2.1.s1772700320$o1$g0$t1772700320$j60$l0$h1422739336; _ga=GA1.1.548405366.1772700320; datadome=seMisxmEKIuFjTQYr7lGhM1Me_JjtbXUQ10QIQapYrOZQItsjoW_eE_d0Uh95YeUO8FUYGV9wy7xs1AsmUhpTbI6fmLvTuo8sVvqBOniqUGfA4aqvm~PjMWy_0mq1h8p; _gcl_au=1.1.1284441114.1772700321',
}

params = {
    'prodId': '2852',
    'page': '1',
}
session = requests.Session()
response = session.get(
    'https://www.kkday.com/api/_nuxt/cpath/fetch-product-comment-images',
    params=params,
    proxies=get_random_proxy(),
    headers=headers,
)
print(response.text)