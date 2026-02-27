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
import hashlib
import gzip
import base64
import logging
from copy import deepcopy

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s [line:%(lineno)d]: %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S %p')

M_HOST = "127.0.0.1"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("0820RH@ccs!&rh")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri)

table_name = "en_us"
final_col = mongoclient['agoda2'][f'{table_name}_final']
final_col.ensure_index("feature_id", unique=True)

col = mongoclient['agoda2'][table_name]
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)
count = 0
num = 0
for i in cursor:
    count += 1
    url = i['url']
    result = i['result']

    info_dict = i['info']
    id = info_dict['id']
    name_dict = info_dict['name']
    address_dict = info_dict['address']
    latitude = info_dict['latitude']
    longitude = info_dict['longitude']
    images = info_dict['images']

    source = "Agoda"

    feature_id = str(id)
    name = name_dict['localName']

    # todo address为字符串，agoda返回的是字典，所以json.dumps了一下
    address = json.dumps(address_dict, ensure_ascii=False)

    # todo all_names每个国家不一样，参考excel,name_xx（xx为实际国家的语言标签）
    all_names = {"name_en": name_dict['englishName']}
    all_names = json.dumps(all_names, ensure_ascii=False)

    lat_wgs84 = str(latitude)
    lon_wgs84 = str(longitude)
    website = url

    industry = "ACC"

    img_list = []
    for image_dict in images:
        image_item = dict()
        image_item['img_tag'] = image_dict['category']
        image_item['img_title'] = image_dict['caption']
        image_item['origin_img_url'] = image_dict['url']
        image_item['tos_img_url'] = ""
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
        "lat_wgs84": lat_wgs84,
        "lon_wgs84": lon_wgs84,
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
        "website": website,
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
        final_col.insert(item, check_keys=False)
        num += 1
        logging.info(f"{count}-{num} 保存成功 {feature_id}")
    except Exception as e:
        pass


mongoclient.close()
