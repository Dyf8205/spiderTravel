# -*- coding:utf-8 -*-
import json
import math
from redis import StrictRedis
import pickle
import requests
from urllib import parse
import pymongo


M_HOST = "111.txt.170.7.65"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri)


def check_collections_count(database_name):
    """
    检查指定数据库中detail和error_urls集合的数量

    Args:
        database_name: 数据库名称
    """
    try:
        db = client[database_name]

        detail_count = db['details'].count_documents({})
        error_urls_count = db['error_urls'].count_documents({})

        print(f"数据库: {database_name}")
        print(f"details集合数量: {detail_count}")
        print(f"error_urls集合数量: {error_urls_count}")
        print(f"差值: {abs(detail_count - error_urls_count)}")
        print("-" * 50)

        return {
            'database': database_name,
            'detail_count': detail_count,
            'error_urls_count': error_urls_count,
            'difference': abs(detail_count - error_urls_count)
        }
    except Exception as e:
        print(f"检查数据库 {database_name} 时出错: {str(e)}")
        return None



if __name__ == "__main__":
    # 直接检查所有数据库
    check_collections_count("tiket")
