# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/13 10:56
# explain:
# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/12 14:17
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
from get_proxy import get_proxies
import pymongo
from urllib import parse
import hashlib

"""

"""


class Traveloka():
    def __init__(self,site):
        M_HOST = "127.0.0.1"  # 地址
        M_PORT = 5002  # 端口
        M_USER = "admin"  # 用户名
        M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
        uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
        self.mongoclient = pymongo.MongoClient(uri)
        self.coldict ={} # 用来保存不同国家的 链接
        self.site = site # 站点 用来选择数据库 不同站点放在不同的数据库里面

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
            if "hotel-detail"  in url:
                url_list2.append(url.strip())
        return url_list2


    def deatail_sitemap_locs(self,xml_text):
        l = re.findall("<loc>(.+?)</loc>", xml_text)
        for http in l:
            data = {}
            data["id"] = http.split("-")[-1]
            data["county"] = http.split("/")[5]
            data["path"] = http.split("/")[3]
            data['url'] = http
            data['uuid'] = self.hash_sha1(http)

            col = self.coldict.get(data['county'],None)
            if col == None:
                col = self.mongoclient[self.site][data["county"]]
                col.create_index("uuid", unique=True)
                self.coldict[data["county"]] = col
            col.update_one({"uuid": data["uuid"]}, {"$set": data}, upsert=True)
            logger.info(data)




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
                resp = session.get(url, headers=HEADERS, proxies=get_proxies(), timeout=30, verify=False)
                if resp.status_code == 200:
                    return resp
            except:
                logger.exception("")


    def run(self,url):
        resp = self.getWithcurl(url)  # 获取所有的分类信息
        index_xml = self.decompress_gz(resp.content)
        all_url = self.parse_sitemap_locs(index_xml)
        logger.info(all_url)

        for url in all_url:
            logger.info(url)
            resp = self.getWithcurl(url)  # 获取具体hotel链接
            index_xml = self.decompress_gz(resp.content)
            self.deatail_sitemap_locs(index_xml)
            logger.success(url)


if __name__ == '__main__':
    Traveloka("traveloka").run("https://www.traveloka.com/en-en/sitemap/index.xml.gz")









