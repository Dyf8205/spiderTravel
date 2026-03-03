# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/3/3 15:59
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

import pymongo
from urllib import parse
import hashlib
import json


def get_random_proxy():
    """
    随机从文件中读取proxy
    """
    while True:
        try:
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

class Kkday():
    def __init__(self,site):

        M_HOST = "127.0.0.1"  # 地址
        M_PORT = 5002  # 端口
        M_USER = "admin"  # 用户名
        M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
        uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
        self.mongoclient = pymongo.MongoClient(uri)
        self.coldict ={} # 用来保存不同国家的 链接
        self.site = site # 站点 用来选择数据库 不同站点放在不同的数据库里面
        self.col = self.mongoclient[self.site]["sitemap"]
        self.col.create_index("id", unique=True)
    def hash_sha1(self,url):
        # 创建md5对象
        h = hashlib.sha1()
        h.update(url.encode(encoding='utf-8'))
        res = h.hexdigest()
        return res

    def decompress_gz(self,data):
        """解压 gz，返回字符串"""
        return gzip.decompress(data).decode("utf-8")


    def parse_sitemap_locs(self,xml_text):
        """从 sitemap XML 中提取所有 <loc> URL"""
        url_list = re.findall("<loc>(.+?)</loc>", xml_text)
        url_list2 =[]
        for url in url_list:
            if "sitemap/products"  in url:
                url_list2.append(url.strip())
        return url_list2


    def deatail_sitemap_locs(self,xml_text):
        l = re.findall("<loc>(.+?)</loc>", xml_text)
        for http in l:
            data = {}
            data["id"] = http.split("/")[-1]
            data['url'] = http
            self.col.update_one({"id": data["id"]}, {"$set": data}, upsert=True)
            logger.info(data)
            # break




    def getWithcurl(self,url):
        HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="136", "Google Chrome";v="136"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        }

        while  True:
            try:
                resp = session.get(url, headers=HEADERS, proxies=get_random_proxy(), timeout=30, verify=False)
                if resp.status_code == 200:
                    return resp
            except Exception as e:
                logger.exception(str(e))


    def run(self,url):
        resp = self.getWithcurl(url)  # 获取所有的分类信息
        all_url = self.parse_sitemap_locs(resp.content.decode('utf-8'))
        logger.info(all_url)

        for url in all_url:
            logger.info(url)
            resp = self.getWithcurl(url)  # 获取具体hotel链接
            self.deatail_sitemap_locs(resp.content.decode("utf-8"))
            logger.success(url)



if __name__ == '__main__':
    Kkday("kkday").run("https://www.kkday.com/en-us/sitemap/products")









