# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/24 11:34
# explain: 对比 trip_before2 和 trip 库，找出 trip 中新增的 url

import pymongo
from urllib import parse
from redis import StrictRedis

# redis配置
REDIS_URL = 'redis://:grad@0212!GnGn@127.0.0.1:5001/2'
redis = StrictRedis.from_url(REDIS_URL, decode_responses=True)

M_HOST = "127.0.0.1"
M_PORT = 5002
M_USER = "admin"
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri, maxPoolSize=1)

REDIS_KEY = "check_add:old_urls"
BATCH_SIZE = 5000
QUERY_FILTER = {"districtName": {"$regex": "(Indonesia|Japan|Thailand|Malaysia)$"}}

# 清理旧数据
redis.delete(REDIS_KEY)

# Step 1: 把 trip_before2 两个集合的 url 写入 Redis Set
count = 0
pipe = redis.pipeline()

for col_name in ['seed_hotels', 'seed_hotels2']:
    col = mongoclient['trip_before2'][col_name]
    cursor = col.find(QUERY_FILTER, {"url": 1}, no_cursor_timeout=True, batch_size=5)
    for doc in cursor:
        url = doc.get("url")
        if url:
            pipe.sadd(REDIS_KEY, url)
            count += 1
            if count % BATCH_SIZE == 0:
                pipe.execute()
                pipe = redis.pipeline()
                print(f"[加载旧数据] 已写入 {count} 条")
    cursor.close()

pipe.execute()
print(f"[加载旧数据] 完成，trip_before2 共 {count} 条 url")

# Step 2: 遍历 trip.seed_hotels2，找出新增的 url
col = mongoclient['trip']['seed_hotels2']
cursor = col.find(QUERY_FILTER, {"url": 1}, no_cursor_timeout=True, batch_size=5)

new_urls = []
scanned = 0
for doc in cursor:
    scanned += 1
    url = doc.get("url")
    if url and not redis.sismember(REDIS_KEY, url):
        new_urls.append(url)
    if scanned % BATCH_SIZE == 0:
        print(f"[扫描新数据] 已扫描 {scanned} 条，新增 {len(new_urls)} 条")

cursor.close()
print(f"[扫描新数据] 完成，trip.seed_hotels2 共 {scanned} 条，新增 {len(new_urls)} 条")

# Step 3: 输出结果
if new_urls:
    output_file = "new_urls.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for url in new_urls:
            f.write(url + "\n")
    print(f"新增 url 已写入 {output_file}")
else:
    print("没有新增 url")

# 清理
redis.delete(REDIS_KEY)
mongoclient.close()
redis.close()