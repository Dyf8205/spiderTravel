# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/3/4 10:34
# explain:  对于不同页面区分hotel  United States    Japan   Indonesia




import json
import re
from lxml import etree
from urllib import parse
import pymongo
import hashlib
from loguru import logger
from copy import deepcopy
from pathlib import Path

logger.add(f"./logs/{Path(__file__).stem}",mode="w")

M_HOST = "localhost"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri,maxPoolSize=10)


us_col = client['kkday']['us_detail']
us_col.create_index("id", unique=True)
us_num = 0
id_col = client['kkday']['id_detail']
id_col.create_index("id", unique=True)
id_num = 0
ja_col = client['kkday']['ja_sitemap']
ja_col.create_index("id", unique=True)
ja_num = 0
def hash_sha1(url):
    # 创建md5对象
    h = hashlib.sha1()
    h.update(url.encode(encoding='utf-8'))
    res = h.hexdigest()
    return res


col = client['kkday']['base_details']
cursor = col.find({},{"_id":0}, no_cursor_timeout=True, batch_size=5)



for i in cursor:
    #通过这种判断是不是hotel  不是的 直接跳过
    data = deepcopy(i)

    if "hotel" not in i["response_url"] and   "__INIT_STATE__" not in i["website_snapshot"]  and "accommodation/list" not in i["website_snapshot"]:
        continue


    if "__INIT_STATE__"  in i["website_snapshot"]:
        json_dict = json.loads(re.findall("window\.__INIT_STATE__\s*=\s*([\s\S]+?);\s+</script>", i["website_snapshot"])[0])

        if "Accommodation"  not in json.dumps( json_dict["state"]["product"]["prodInfo"]["destinations"]["breadcrumbs"]):
            logger.error(i["url"] + "  __INIT_STATE__ 存在 但是也不是住宿类型")
            continue
        country = json_dict["state"]["product"]["prodInfo"]["destinations"]["breadcrumbs"][0]["name"]
        if "United States" ==   country:
            us_col.update_one({"id": data["id"]}, {"$set": data}, upsert=True)
            us_num +=1
        elif "Japan"  ==   country:
            del data["website_snapshot"]
            del data["response_url"]
            item = dict()
            item["url"] = data["url"].replace("en-us","ja")
            item["id"] = data["id"]
            ja_col.update_one({"id": item["id"]}, {"$set": item}, upsert=True)
            ja_num +=1
        elif "Indonesia"  ==   country:
            del data["website_snapshot"]
            del data["response_url"]
            data["url"] = data["url"].replace("en-us","en-id")
            id_col.update_one({"id": data["id"]}, {"$set": data}, upsert=True)
            id_num +=1
    elif "accommodation/list"  in i["website_snapshot"]:

        html = etree.HTML(i["website_snapshot"])
        jsonstr = html.xpath('//script[@type="application/ld+json"]/text()')[0]
        dict1 = json.loads(jsonstr)
        if "Accommodation" not in json.dumps(dict1["@graph"][2]["itemListElement"]):
            logger.error(i["url"] + "  accommodation/list 存在 但是也不是住宿类型")

        country = dict1["@graph"][2]["itemListElement"][0]["name"]
        if "United States" == country:
            us_col.update_one({"id": data["id"]}, {"$set": data}, upsert=True)
            us_num += 1
        elif "Japan" == country:
            del data["website_snapshot"]
            del data["response_url"]
            item = dict()
            item["url"] = data["url"].replace("en-us","ja")
            item["id"] = data["id"]
            ja_col.update_one({"id": item["id"]}, {"$set": item}, upsert=True)
            ja_num += 1
        elif "Indonesia" == country:
            id_col.update_one({"id": data["id"]}, {"$set": data}, upsert=True)
            id_num += 1

    else:
        logger.error(i["url"] + "  不是住宿类型")

logger.success(f"美国有 {us_num}")
logger.success(f"日本有 {ja_num}")
logger.success(f"印尼有 {id_num}")

client.close()