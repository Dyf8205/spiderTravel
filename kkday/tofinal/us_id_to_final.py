# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/3/6 16:43
# explain:
# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/25 11:08
# explain:
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
from redis import StrictRedis

logging.add("./logs/us_id_to_final.log",mode="w")

M_HOST = "127.0.0.1"  # 地址
M_PORT = 5002  # 端口
M_USER = "admin"  # 用户名
M_PASSWORD = parse.quote_plus("grad@0212!GnGn")
uri = 'mongodb://{}:{}@{}:{}'.format(M_USER, M_PASSWORD, M_HOST, str(M_PORT))
mongoclient = pymongo.MongoClient(uri,maxPoolSize=6)

source = "Kkday"
industry ="ACC"

col = mongoclient['kkday']["us_detail"]   #详情链接
cursor = col.find({}, no_cursor_timeout=True, batch_size=5)

imgcol = mongoclient["kkday"]["image_detail"]     #图片json链接



final_col_id = mongoclient['kkday'][f'en_id_final']  #印尼链接
final_col_id.create_index("feature_id", unique=True)


final_col_th = mongoclient['kkday'][f'en_us_final']   #泰国链接
final_col_th.create_index("feature_id", unique=True)


travellerType_dict={
    "01":"Couple",
    "02":"Family",
    "03":"Friend",
    "04":"Solo traveler",
    "05":"Business traveler",
}


count = 0
num = 0
for i in cursor:
    count += 1
    url = i['url']
    img_list =[]
     # 唯一标识符

    if "__INIT_STATE__" in i["website_snapshot"]:
        baseDict = json.loads(re.findall("window\.__INIT_STATE__\s*=\s*([\s\S]+?);\s+</script>", i["website_snapshot"])[0])
        hotelServiceData = baseDict["state"]["product"]["hotelServiceData"]
        feature_id = str(hotelServiceData["prodOid"])

        hotelBaseInfo = hotelServiceData["hotelBaseInfo"]

        latitude = str(hotelBaseInfo["latitude"])
        longitude = str(hotelBaseInfo["longitude"])

        name = hotelBaseInfo["hotelName"]
        # en_name = baseDict["hotelDetailResponse"]["hotelBaseInfo"]["nameInfo"]["nameEn"]
        # name_path = re.findall("https://(.+?)\.kkday\.com", url)[0]  # 获取当地的标志
        all_names = { "name_en": hotelBaseInfo["hotelName"]}
        all_names = json.dumps(all_names, ensure_ascii=False)
        address = hotelBaseInfo["address"]

        for image_dict in hotelServiceData["hotelPictures"]["list"]:
            image_item = dict()
            image_item['img_tag'] = ""
            image_item['img_title'] = ""
            image_item['origin_img_url'] = image_dict['url']
            image_item['tos_img_url'] = ""
            image_item['img_source'] = "hotel"
            img_list.append(image_item)



        
    #
    imgjson = json.loads(imgcol.find_one({"id":feature_id})["website_snapshot"])
    for jsonstr in imgjson:
        image_list = json.loads(jsonstr)["data"]["images"]
        for image in image_list:
            image_item = dict()
            image_item['img_tag'] = travellerType_dict[image["author"]["travellerType"]]
            image_item['img_title'] = image["author"]["title"]
            image_item['origin_img_url'] = image_dict['url']
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


    if name_path =="th":
        final_col_th.update_one({"feature_id": item["feature_id"]}, {"$set": item}, upsert=True)
    elif name_path == "jp":
        final_col_jp.update_one({"feature_id": item["feature_id"]}, {"$set": item}, upsert=True)
    elif name_path == "id":
        final_col_id.update_one({"feature_id": item["feature_id"]}, {"$set": item}, upsert=True)
    elif name_path == "my":
        final_col_my.update_one({"feature_id": item["feature_id"]}, {"$set": item}, upsert=True)
    else:
        logging.error(name_path)
    num +=1
    logging.info(f"{name_path}-{count}-{num} 保存成功 {feature_id}")

logging.error(f"{count}-{num} 完成")

mongoclient.close()
