# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/3/5 16:59
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

logger.add(f"./logs/{Path(__file__).stem}.log", mode="w")


with open("./第二种json.html","r",encoding="utf-8") as f:
    website_snapshot = f.read()

html = etree.HTML(website_snapshot)
cut_bread_list = html.xpath('//div[@class="cut-bread"]//a/text()')
if len(cut_bread_list) != 0:  # 面包屑标签存在
    cut_bread_list = [s.strip() for s in cut_bread_list]
    if "Accommodation" in cut_bread_list:  # 那就可以拿到国家信息  带着两个 说明是酒店
        country = cut_bread_list[0]
        if "United States" == country:
            print("成功")
        elif "Japan" == country:
            print("成功")
        elif "Indonesia" == country:
            print("成功")

    else:  # 面包屑没有Accommodation
        pass
else:  # 第一种json面包屑
    if "__INIT_STATE__" in website_snapshot:  # 第一中json
        json_dict = json.loads(re.findall("window\.__INIT_STATE__\s*=\s*([\s\S]+?);\s+</script>", website_snapshot)[0])
        try:
            if "Accommodation" in json.dumps(
                    json_dict["state"]["product"]["prodInfo"]["destinations"]["breadcrumbs"]):
                try:
                    country = json_dict["state"]["product"]["prodInfo"]["destinations"]["breadcrumbs"][0]["name"]
                except Exception as e:
                    print("成功")
                if "United States" == country:
                    print("成功")
                elif "Japan" == country:
                    print("成功")
                elif "Indonesia" == country:
                    print("成功")
            else:
                print("成功")
        except Exception as e:
            logger.error(' 第一种json解析出现问题')


    elif 'type="application/ld+json"' in website_snapshot: #第二种json面包屑
        try:
            jsonstr = html.xpath('//script[@type="application/ld+json"]/text()')[0]
        except:
            logger.error( '  第二种json获取失败')

        dict1 = json.loads(jsonstr)
        try:
            if "Accommodation" in json.dumps(dict1["@graph"][2]["itemListElement"]):
                country = dict1["@graph"][2]["itemListElement"][0]["name"]
                if "United States" == country:
                    print("成功")
                elif "Japan" == country:
                    print("成功")
                elif "Indonesia" == country:
                    print("成功")

            else:
                print("成功")
        except:
            logger.error("   第二种获取面包屑失败")

    else:
        logger.error(' 其他问题')


