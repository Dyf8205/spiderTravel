# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/3/5 17:07
# explain:
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

# logger.add(f"./logs/{Path(__file__).stem}.log", mode="w")

M_HOST = "127.0.0.1"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
client = pymongo.MongoClient(uri, maxPoolSize=10)


us_num = 0

id_num = 0

ja_num = 0

col = client['kkday']['base_details']
cursor = col.find({"url":"https://www.kkday.com/en-us/product/189461"}, {"_id": 0}, no_cursor_timeout=True, batch_size=5)

index = 0
for i in cursor:
    logger.info("查询成功")
    data = deepcopy(i)
    index += 1
    if index % 5000 == 0:
        logger.success(f"共检查 {index}")
        logger.success(f"美国有 {us_num}")
        logger.success(f"日本有 {ja_num}")
        logger.success(f"印尼有 {id_num}")

    html = etree.HTML(i["website_snapshot"])
    cut_bread_list = html.xpath('//div[@class="cut-bread"]//a/text()')
    if len(cut_bread_list) != 0:  # 面包屑标签存在
        cut_bread_list = [s.strip() for s in cut_bread_list]
        if "Accommodation" in cut_bread_list:  # 那就可以拿到国家信息  带着两个 说明是酒店
            country = cut_bread_list[0]
            if "United States" == country:

                us_num += 1
            elif "Japan" == country:
                del data["website_snapshot"]
                del data["response_url"]
                item = dict()
                item["url"] = data["url"].replace("en-us", "ja")
                item["id"] = data["id"]

                ja_num += 1
            elif "Indonesia" == country:

                id_num += 1
            continue
        else:  # 面包屑没有Accommodation
            continue
    else:  # 第一种json面包屑
        if "__INIT_STATE__" in i["website_snapshot"]:  # 第一中json
            json_dict = json.loads(re.findall("window\.__INIT_STATE__\s*=\s*([\s\S]+?);\s+</script>", i["website_snapshot"])[0])
            try:
                if "Accommodation" in json.dumps(
                        json_dict["state"]["product"]["prodInfo"]["destinations"]["breadcrumbs"]):
                    try:
                        country = json_dict["state"]["product"]["prodInfo"]["destinations"]["breadcrumbs"][0]["name"]
                    except Exception as e:
                        logger.error(i["url"] + ' 第一种json拿不到面包屑')
                        continue  # 这里如果没有的话 基本不是  商品详情页   如 https://www.kkday.com/en-us/product/105149
                    if "United States" == country:

                        us_num += 1
                    elif "Japan" == country:
                        del data["website_snapshot"]
                        del data["response_url"]
                        item = dict()
                        item["url"] = data["url"].replace("en-us", "ja")
                        item["id"] = data["id"]

                        ja_num += 1
                    elif "Indonesia" == country:

                        id_num += 1
                    continue
                else:
                    continue
            except Exception as e:
                logger.error(i["url"] + ' 第一种json解析出现问题')
                continue

        elif 'type="application/ld+json"' in i["website_snapshot"]: #第二种json面包屑
            try:
                jsonstr = html.xpath('//script[@type="application/ld+json"]/text()')[0]
            except:
                logger.error(i["url"] + '  第二种json获取失败')
                continue
            dict1 = json.loads(jsonstr)
            try:
                if "Accommodation" in json.dumps(dict1["@graph"][2]["itemListElement"]):
                    country = dict1["@graph"][2]["itemListElement"][0]["name"]
                    if "United States" == country:

                        us_num += 1
                    elif "Japan" == country:
                        del data["website_snapshot"]
                        del data["response_url"]
                        item = dict()
                        item["url"] = data["url"].replace("en-us", "ja")
                        item["id"] = data["id"]

                        ja_num += 1
                    elif "Indonesia" == country:

                        id_num += 1
                    continue
                else:
                    continue
            except:
                logger.error(i["url"]+"   第二种获取面包屑失败")
                continue
        else:
            logger.error(i["url"] + ' 其他问题')
            continue


logger.success(f"美国有 {us_num}")
logger.success(f"日本有 {ja_num}")
logger.success(f"印尼有 {id_num}")
cursor.close()
client.close()