# -*- coding:utf-8 -*-
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

logging.add("./logs/tiket_final.log",mode="w")

M_HOST = "127.0.0.1"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri,maxPoolSize=3)

source = "Tiket"
industry ="ACC"



final_col_id = mongoclient['tiket'][f'id_id_final']
final_col_id.create_index("feature_id", unique=True)


final_col_my = mongoclient['tiket'][f'en_my_final']
final_col_my.create_index("feature_id", unique=True)


col = mongoclient['tiket']["details"]
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)
count = 0
num = 0
for i in cursor:
    count += 1
    url = i['url']
     # 唯一标识符

    h = etree.HTML(i["website_snapshot"])
    baseDict = json.loads(h.xpath('//script[@id="__NEXT_DATA__"]/text()')[0])
    name = baseDict ["props"]["pageProps"]["hotelDetailDataResponse"]["name"]
    feature_id =baseDict["props"]["pageProps"]["hotelDetailDataResponse"]["hotelId"]

    if "id-id" in url:
        all_names = {"name_id":name}
    elif "en-my" in url:
        all_names = {"name_en":name}

    all_names = json.dumps(all_names, ensure_ascii=False)
        # props.pageProps.hotelDetailDataResponse.address
    address = baseDict ["props"]["pageProps"]["hotelDetailDataResponse"]["address"]

    images =  baseDict ["props"]["pageProps"]["hotelDetailDataResponse"]["images"]
    img_list =[]
    for image_dict in images:
        image_item = dict()
        image_item['img_tag'] = image_dict['category']
        image_item['img_title'] = image_dict['caption']
        image_item['origin_img_url'] = image_dict['url']
        image_item['tos_img_url'] = ""
        image_item['img_source'] = "hotel"
        img_list.append(image_item)


    try:
        for image_dict in baseDict["props"]["pageProps"]["dehydratedState"]["queries"][1]["state"]["data"]["data"]["content"]:
            image_item = dict()
            image_item['img_tag'] = ""
            image_item['img_title'] = ""
            image_item['origin_img_url'] = image_dict['imageUrl']
            image_item['tos_img_url'] = ""
            image_item['img_source'] = "user"
            img_list.append(image_item)
            logging.info(f"{url} 有用户上传")
    except:
        logging.info(f"{url} 没有用户上传")

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
        "lat_wgs84": str(baseDict["props"]["pageProps"]["hotelDetailDataResponse"]["location"]["coordinates"]["latitude"]),
        "lon_wgs84":  str(baseDict["props"]["pageProps"]["hotelDetailDataResponse"]["location"]["coordinates"]["longitude"]),
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
    check_item = deepcopy(item)
    try:
        if "id-id" in url:
            final_col_id.update_one({"feature_id": item["feature_id"]}, {"$set": item}, upsert=True)
            num += 1
            logging.info(f"{count}-{num} 保存成功 {feature_id}")
        elif "en-my" in url:
            final_col_my.update_one({"feature_id": item["feature_id"]}, {"$set": item}, upsert=True)
            num += 1
            logging.info(f"{count}-{num} 保存成功 {feature_id}")
        else:
            logging.error(url)

    except Exception as e:
        logging.error(i['url'] +"\n"+str(e))



mongoclient.close()
