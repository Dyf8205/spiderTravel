import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import gzip
import xml.etree.ElementTree as ET
import re
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

SITEMAP_INDEX_URL = "https://www.traveloka.com/en-en/sitemap/index.xml.gz"



NS = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

MAX_WORKERS = 10
MAX_RETRIES = 10  # 单个链接最大重试次数


def get_proxies():
    """获取一个可用的代理 IP"""
    while True:
        try:
            url = 'https://service.ipzan.com/core-extract?num=1&no=20230811703171574402&minute=1&format=json&repeat=1&protocol=1&pool=ordinary&mode=auth&secret=ihdgjuvs0jaadp'
            response = requests.get(url, timeout=10)
            contents = response.json()
            ip = contents['data']["list"][0]['ip']
            port = contents['data']["list"][0]['port']
            proxy_url = f"{ip}:{port}"
            proxies = {
                "http": f"http://{proxy_url}",
                "https": f"http://{proxy_url}",
            }
            test_resp = requests.get('http://www.baidu.com', proxies=proxies, timeout=10)
            if test_resp.status_code == 200:
                print(f"  [代理] 获取成功: {proxy_url}")
                return proxies
        except Exception:
            pass


def decompress_gz(data):
    """解压 gz，返回字符串"""
    return gzip.decompress(data).decode("utf-8")


def parse_sitemap_locs(xml_text):
    """从 sitemap XML 中提取所有 <loc> URL"""
    root = ET.fromstring(xml_text)
    return [loc.text.strip() for loc in root.findall(".//ns:loc", NS)]


def worker(task_queue, all_hotel_urls, lock, counter, total, thread_name):
    """
    工作线程：从队列取任务，每个线程维护自己的代理 IP。
    请求失败时换代理重试，单个链接最多重试 MAX_RETRIES 次。
    """
    proxies = get_proxies()

    while True:
        try:
            url = task_queue.get_nowait()
        except Exception:
            break  # 队列空了，退出

        success = False
        for attempt in range(MAX_RETRIES):
            try:
                resp = requests.get(url, headers=HEADERS, proxies=proxies,
                                    timeout=30, verify=False)
                resp.raise_for_status()
                xml_text = decompress_gz(resp.content)
                urls = parse_sitemap_locs(xml_text)
                with lock:
                    all_hotel_urls.extend(urls)
                    counter[0] += 1
                    print(f"  [{counter[0]}/{total}] {thread_name} 提取 {len(urls)} 个 URL，累计: {len(all_hotel_urls)}")
                success = True
                break
            except Exception as e:
                print(f"  {thread_name} 请求失败(第{attempt+1}次): {e}，更换代理...")
                proxies = get_proxies()

        if not success:
            with lock:
                counter[0] += 1
                print(f"  [{counter[0]}/{total}] {thread_name} 最终失败: {url}")

        task_queue.task_done()


def main():
    # 1. 下载并解压 sitemap index（用临时代理）
    print("[1/3] 下载 sitemap index...")
    proxies = get_proxies()
    resp = requests.get(SITEMAP_INDEX_URL, headers=HEADERS, proxies=proxies,
                        timeout=30, verify=False)
    resp.raise_for_status()
    index_xml = decompress_gz(resp.content)

    # 2. 筛选 hotel-detail 链接
    print("\n[2/3] 筛选 hotel-detail 链接...")
    all_urls = parse_sitemap_locs(index_xml)
    hotel_detail_urls = [u for u in all_urls if "hotel-detail" in u]
    print(f"  共 {len(all_urls)} 个 sitemap，其中 hotel-detail: {len(hotel_detail_urls)} 个")

    # 3. 多线程下载，每个线程维护自己的代理
    print(f"\n[3/3] 多线程({MAX_WORKERS})下载 hotel-detail sitemap...")
    task_queue = Queue()
    for u in hotel_detail_urls:
        task_queue.put(u)

    all_hotel_urls = []
    lock = threading.Lock()
    counter = [0]
    total = len(hotel_detail_urls)

    threads = []
    for i in range(MAX_WORKERS):
        t = threading.Thread(target=worker,
                             args=(task_queue, all_hotel_urls, lock, counter, total, f"线程{i+1}"))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"\n完成！酒店 URL 总数: {len(all_hotel_urls)}")
    return all_hotel_urls


if __name__ == "__main__":
    all_hotel_urls = main()
