# -*- coding:UTF-8 -*-
import json
import pickle

with open("test.json","r",encoding="utf-8") as f:
    jsonstr = f.read()


baseDict = json.loads(jsonstr)

images = baseDict["props"]["pageProps"]["hotelDetailDataResponse"]["images"]
# img_list = []
for image_dict in images:
    image_item = dict()
    image_item['img_tag'] = image_dict['category']
    image_item['img_title'] = image_dict['caption']
    image_item['origin_img_url'] = image_dict['url']
    image_item['tos_img_url'] = ""
    image_item['img_source'] = "hotel"
    print(image_item)

try:
    for image_dict in baseDict["props"]["pageProps"]["dehydratedState"]["queries"][1]["state"]["data"]["data"]["content"]:
        image_item = dict()
        image_item['img_tag'] = ""
        image_item['img_title'] = ""
        image_item['origin_img_url'] = image_dict['imageUrl']
        image_item['tos_img_url'] = ""
        image_item['img_source'] = "user"
        print(image_item)
except:
    print("无用户上传")