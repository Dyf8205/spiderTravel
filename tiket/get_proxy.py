# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/12 9:59
# explain:
import requests
# def get_proxies():
#     """获取一个可用的代理 IP"""
#     while True:
#         try:
#             url = 'https://service.ipzan.com/core-extract?num=1&no=20230811703171574402&minute=1&format=json&repeat=1&protocol=1&pool=ordinary&mode=auth&secret=ihdgjuvs0jaadp'
#             response = requests.get(url, timeout=10)
#             contents = response.json()
#             ip = contents['data']["list"][0]['ip']
#             port = contents['data']["list"][0]['port']
#             proxy_url = f"{ip}:{port}"
#             proxies = {
#                 "http": f"http://{proxy_url}",
#                 "https": f"http://{proxy_url}",
#             }
#             test_resp = requests.get('http://www.baidu.com', proxies=proxies, timeout=10)
#             if test_resp.status_code == 200:
#                 print(f"  [代理] 获取成功: {proxy_url}")
#                 return proxies
#         except Exception:
#             pass


def get_proxies():
    """获取一个可用的代理 IP"""
    while True:
        try:
            url = 'https://service.ipzan.com/core-extract?num=1&no=20230811703171574402&minute=1&format=json&protocol=1&pool=quality&mode=auth&secret=ihdgjuvs0jaadp'
            response = requests.get(url, timeout=10)
            contents = response.json()
            ip = contents['data']["list"][0]['ip']
            port = contents['data']["list"][0]['port']
            account = contents['data']["list"][0]['account']
            password = contents['data']["list"][0]['password']
            proxy_url = f"{ip}:{port}"
            proxies = {
                "http": f"http://{account}:{password}@{proxy_url}",
                "https": f"http://{account}:{password}@{proxy_url}",
            }
            test_resp = requests.get('http://www.baidu.com', proxies=proxies, timeout=10)
            if test_resp.status_code == 200:
                print(f"  [代理] 获取成功: {proxies}")
                return proxies
        except Exception:
            pass

if __name__ == '__main__':

    proxies = get_proxies()