# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/12 9:59
# explain:
import requests
from loguru import logger as logging
import  time
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
                logging.error('代理ip池数量小于50, 10s后重新获取')
                time.sleep(10)
                continue

            response = requests.get("http://119.3.172.62:5007/get")
            proxies = json.loads(response.text)['proxy']
            if proxies:
                break
            else:
                logging.error('代理ip池为空, 10s后重新获取')
                time.sleep(10)
        except:
            logging.error('代理ip池为空, 10s后重新获取')
            time.sleep(10)

    proxy = proxies

    proxy if proxy.startswith('http') else 'http://' + proxy


    proxies = {
        "http": proxy,
        "https": proxy,
    }
    return proxies


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
            print(f"  [代理] 获取成功: {proxies}")
            test_resp = requests.get('http://www.baidu.com', proxies=proxies, timeout=10)
            if test_resp.status_code == 200:
                print(f"  [代理] 测试获取成功: {proxies}")
                return proxies
        except Exception:
            pass

if __name__ == '__main__':

    proxies = get_proxies()