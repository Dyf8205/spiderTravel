# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/3/3 16:45
# explain:

import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import gzip
from curl_cffi import requests
from loguru import logger

logger.add("./logs/error.log", level="ERROR")
# 成功日志 - 只记录 SUCCESS 级别
logger.add("./logs/success.log", filter=lambda record: record["level"].name == "SUCCESS")
import re
session =requests.Session(impersonate="chrome136")


import json

from loguru import logger

def get_random_proxy():
    # """
    # 随机从文件中读取proxy
    # """
    while True:
        try:
            import requests
            # 127.0.0.1:5007
            proxy_all_list = json.loads(requests.get("http://119.3.172.62:5007/get_all").text)
            if len(proxy_all_list) < 50:
                logger.error('代理ip池数量小于50, 10s后重新获取')
                time.sleep(10)
                continue

            response = requests.get("http://119.3.172.62:5007/get")
            proxies = json.loads(response.text)['proxy']
            if proxies:
                break
            else:
                logger.error('代理ip池为空, 10s后重新获取')
                time.sleep(10)
        except:
            logger.error('代理ip池为空, 10s后重新获取')
            time.sleep(10)

    proxy = proxies

    proxy if proxy.startswith('http') else 'http://' + proxy

    proxies = {
        "http": proxy,
        "https": proxy,
    }
    return proxies

    # while True:
    #     try:
    #         url = 'https://service.ipzan.com/core-extract?num=1&no=20230811703171574402&minute=1&format=json&protocol=1&pool=quality&mode=auth&secret=ihdgjuvs0jaadp'
    #         response = requests.get(url, timeout=10)
    #         contents = response.json()
    #         ip = contents['data']["list"][0]['ip']
    #         port = contents['data']["list"][0]['port']
    #         account = contents['data']["list"][0]['account']
    #         password = contents['data']["list"][0]['password']
    #         proxy_url = f"{ip}:{port}"
    #         proxies = {
    #             "http": f"http://{account}:{password}@{proxy_url}",
    #             "https": f"http://{account}:{password}@{proxy_url}",
    #         }
    #         print(f"  [代理] 获取成功: {proxies}")
    #         test_resp = requests.get('http://www.baidu.com', proxies=proxies, timeout=10)
    #         if test_resp.status_code == 200:
    #             print(f"  [代理] 测试获取成功: {proxies}")
    #             return proxies
    #     except Exception:
    #         pass


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
}

def fetch_with_retry(url, max_retries=3):
    """带重试机制的请求函数"""
    for attempt in range(max_retries):
        try:
            proxies = get_random_proxy()
            logger.info(f"尝试第 {attempt + 1} 次请求，代理: {proxies}")

            response = session.get(
                url,
                timeout=(15, 90),  # (连接超时15s, 读取超时90s)
                headers=headers,
                proxies=proxies,
                allow_redirects=True
            )

            if response.status_code == 200:
                logger.success(f"请求成功: {url}")
                return response
            else:
                logger.warning(f"状态码异常: {response.status_code}")

        except requests.exceptions.Timeout as e:
            logger.error(f"第 {attempt + 1} 次请求超时: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)  # 等待2秒后重试
                continue
            else:
                raise
        except Exception as e:
            logger.error(f"第 {attempt + 1} 次请求失败: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                raise

    raise Exception(f"请求失败，已重试 {max_retries} 次")

# 使用重试函数
response = fetch_with_retry('https://www.kkday.com/ja/product/124085')
print(response.text)