# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/26 10:10
# explain:
import json

with open("./travelka详情页2.json", "r", encoding="utf-8") as f:
    jsjs = f.read()
baseDict = json.loads(jsjs)



address    = baseDict["props"]["pageProps"]["hotel"]["address"]
feature_id  = str(baseDict["props"]["pageProps"]["pathId"])
displayName = baseDict["props"]["pageProps"]["hotel"]["displayName"]
longitude   = baseDict["props"]["pageProps"]["hotel"]["longitude"]
latitude   = baseDict["props"]["pageProps"]["hotel"]["latitude"]
en_name    = baseDict["props"]["pageProps"]["hotel"]["name"]
name_path  = baseDict["locale"]
all_names  = {f"name_{name_path}": displayName, "name_en": en_name}
all_names   = json.dumps(all_names, ensure_ascii=False)



print(address    )
print(feature_id )
print(displayName)
print(longitude  )
print(latitude   )
print(en_name    )
print(name_path  )
print(all_names  )
print(all_names  )


img_list = []
img_filter_list = []
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

#详情页中用户上传的图片
for image_tab in baseDict["props"]["pageProps"]["reviewDataProps"]["mediaGalleryByTravelerResponse"]["items"]:
    image_item = dict()
    image_item['img_tag'] = ""
    image_item['img_title'] = ""
    image_item['origin_img_url'] = image_tab["media"]['url']
    image_item['tos_img_url'] = ""
    image_item['img_source'] = "user"
    img_list.append(image_item)





with open("./room.json", "r", encoding="utf-8") as f:
    roomJson = f.read()

roomDict = json.loads(roomJson)
for image_tab in roomDict["data"]["recommendedEntries"]:
    img_tag = image_tab["name"]
    for image_dict in image_tab["imageWithCaptions"]:
        image_item = dict()
        image_item['img_tag'] = img_tag
        image_item['img_title'] = image_dict['caption'] if image_dict['caption'] else ""
        image_item['origin_img_url'] = image_dict['url']
        image_item['tos_img_url'] = ""
        image_item['img_source'] = "hotel"
        print(image_item)
        img_list.append(image_item)

with open("./traverler.json", "r", encoding="utf-8") as f:
    traverlerJson = f.read()


traverlerDict = json.loads(traverlerJson)

for image_tab in traverlerDict["data"]["items"]:
    image_item = dict()
    image_item['img_tag'] = ""
    image_item['img_title'] = ""
    image_item['origin_img_url'] = image_tab["media"]['url']
    image_item['tos_img_url'] = ""
    image_item['img_source'] = "user"
    img_list.append(image_item)

print(img_list.__len__())