# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/25 11:08
# explain:
import requests
import re
import time
import json
import math
import json
import pickle
import requests
import pymongo
from urllib import parse
from lxml import etree
import hashlib
import gzip
import base64
from loguru import logger as logging
from copy import deepcopy
from redis import StrictRedis

logging.add("./logs/make_final_traveloka.log", mode="w")

M_HOST = "127.0.0.1"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri, maxPoolSize=6)

source = "Traveloka"
industry = "ACC"

col = mongoclient['traveloka']["details"]  # 详情链接
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)

final_col_id = mongoclient['traveloka'][f'id_id_final']  # 印尼链接
final_col_id.create_index("feature_id", unique=True)

final_col_jp = mongoclient['traveloka'][f'ja_jp_final']  # 日本链接
final_col_jp.create_index("feature_id", unique=True)

count = 0
num = 0
for i in cursor:
    count += 1
    url = i['url']
    # 唯一标识符
    try:
        h = etree.HTML(i["website_snapshot"])
        baseDict = json.loads(h.xpath('//script[@id="__NEXT_DATA__"]/text()')[0])
    except Exception as e:
        logging.error(url + " json查询失败")
        continue

    address = baseDict["props"]["pageProps"]["hotel"]["address"]
    feature_id = str(baseDict["props"]["pageProps"]["pathId"])
    name = baseDict["props"]["pageProps"]["hotel"]["displayName"]
    longitude = baseDict["props"]["pageProps"]["hotel"]["longitude"]
    latitude = baseDict["props"]["pageProps"]["hotel"]["latitude"]
    en_name = baseDict["props"]["pageProps"]["hotel"]["name"]
    name_path = baseDict["locale"].split("-")[-1]
    all_names = {f"name_{name_path}": name, "name_en": en_name}
    all_names = json.dumps(all_names, ensure_ascii=False)
    # 详情页的图片
    img_list = []
    for image_tab in baseDict["props"]["pageProps"]["hotel"]["imageCategory"]:
        img_tag = image_tab["type"]
        for image_dict in image_tab["assets"]:
            image_item = dict()
            image_item['img_tag'] = img_tag
            image_item['img_title'] = image_dict['caption'] if image_dict['caption'] else ""
            image_item['origin_img_url'] = image_dict['url']
            image_item['tos_img_url'] = ""
            image_item['img_source'] = "hotel"
            img_list.append(image_item)
    try:
        # 详情页中用户上传的图片
        for image_tab in baseDict["props"]["pageProps"]["reviewDataProps"]["mediaGalleryByTravelerResponse"]["items"]:
            image_item = dict()
            image_item['img_tag'] = ""
            image_item['img_title'] = ""
            image_item['origin_img_url'] = image_tab["media"]['url']
            image_item['tos_img_url'] = ""
            image_item['img_source'] = "user"
            img_list.append(image_item)
    except:
        logging.error(url)
        pass

    # room中的图片

    roomDict = json.loads(i["roomJson"])
    for image_tab in roomDict["data"]["recommendedEntries"]:
        img_tag = image_tab["name"]
        for image_dict in image_tab["imageWithCaptions"]:
            image_item = dict()
            image_item['img_tag'] = img_tag
            image_item['img_title'] = image_dict['caption'] if image_dict['caption'] else ""
            image_item['origin_img_url'] = image_dict['url']
            image_item['tos_img_url'] = ""
            image_item['img_source'] = "hotel"
            img_list.append(image_item)

    # 用户上传的图片
    traverlerDict = json.loads(i["traverlerJson"])

    for image_tab in traverlerDict["data"]["items"]:
        image_item = dict()
        image_item['img_tag'] = ""
        image_item['img_title'] = ""
        image_item['origin_img_url'] = image_tab["media"]['url']
        image_item['tos_img_url'] = ""
        image_item['img_source'] = "user"
        img_list.append(image_item)

    img_list = json.dumps(img_list, ensure_ascii=False)

    item = {
        "source": source,
        "feature_id": feature_id,
        "name": name,
        "country_or_region": "",
        "geoname_id": "",
        "l0_gnid": "",
        "l1_gnid": "",
        "l2_gnid": "",
        "l3_gnid": "",
        "l4_gnid": "",
        "province": "",
        "city": "",
        "district": "",
        "town": "",
        "address": address,
        "biz_area": "",
        "all_names": all_names,
        "all_address": "",
        "lat_wgs84": str(latitude),
        "lon_wgs84": str(longitude),
        "geohash_wgs84": "",
        "geohash6": "",
        "alias": "",
        "tags": "",
        "tt_type": "",
        "tt_type_v4": "",
        "brand": "",
        "branch": "",
        "source_status": "",
        "zip_code": "",
        "website": url,
        "website_snapshot": "",
        "prt_feature_id": "",
        "g1_cid": "",
        "tel": "",
        "hours": "",
        "email": "",
        "price": "",
        "price_grade": "",
        "img_count": "",
        "img_list": img_list,
        "description": "",
        "rich_attr1": "",
        "rich_attr2": "",
        "rich_attr3": "",
        "rich_attr4": "",
        "rich_attr5": "",
        "industry": industry,
        "industry_attrs": "",
        "review_count": "",
        "poi_rating": "",
        "rating_info": "",
        "content_feature_src": "",
        "content_feature": "",
        "is_product": "",
        "product_filter": "",
        "product_detail": "",
        "product_extra": "",
        "related_account": "",
        "account_extra": "",
        "reality_confidence": "",
        "quality_confidence": "",
        "feature_ids_clues": "",
        "lid": "",
        "prod_id": "",
        "rank": "",
        "date": "",
        "desc": ""
    }

    if name_path == "jp":
        final_col_jp.update_one({"feature_id": item["feature_id"]}, {"$set": item}, upsert=True)
    elif name_path == "id":
        final_col_id.update_one({"feature_id": item["feature_id"]}, {"$set": item}, upsert=True)
    else:
        logging.error(name_path)
    num += 1
    logging.info(f"{name_path}-{count}-{num} 保存成功 {feature_id}")

logging.success(f"{count}-{num} 完成")

mongoclient.close()
