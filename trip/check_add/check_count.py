# -*- coding:utf-8 -*-
from urllib import parse
import pymongo

M_HOST = "localhost"
M_PORT = 5002
M_USER = "admin"
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri)

db = client['trip']

final_collections = ['id_id_final', 'th_th_final', 'ms_my_final', 'ja_jp_final']

total_final = 0
for col_name in final_collections:
    count = db[col_name].count_documents({})
    total_final += count
    print(f"{col_name}: {count}")

details_count = db['details'].count_documents({})
print(f"details: {details_count}")
print(f"\nfinal 之和: {total_final}")
print(f"差值 (details - final之和): {details_count - total_final}")

client.close()
