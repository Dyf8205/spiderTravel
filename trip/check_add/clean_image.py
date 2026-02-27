# -*- coding:utf-8 -*-
from urllib import parse
import pymongo

M_HOST = "localhost"
M_PORT = 5002
M_USER = "admin"
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri)

col = client['trip']['details']
col_img = client['trip_image_json']['details']

# 先把 trip.details 的所有 id 加载到集合中
print("加载 trip.details 的所有 id...")
id_set = set()
for doc in col.find({}, {"id": 1, "_id": 0}):
    if doc.get("id"):
        id_set.add(doc["id"])
print(f"trip.details 共 {len(id_set)} 个id")

# 遍历 trip_image_json.details，不在集合中的删除
index = 0
deleted = 0
cursor = col_img.find({}, {"id": 1, "_id": 1}, no_cursor_timeout=True, batch_size=5)

for doc in cursor:
    index += 1
    idvalue = doc.get("id")
    if idvalue not in id_set:
        col_img.delete_one({"_id": doc["_id"]})
        deleted += 1
        print(f"[删除] {index}, id: {idvalue}, _id: {doc['_id']}")
    else:
        print(f"[保留] {index}, id: {idvalue}")

cursor.close()
print(f"\n完成，共检查 {index} 条，删除 {deleted} 条")
