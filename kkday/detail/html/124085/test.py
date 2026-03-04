# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/3/4 11:58
# explain:
import json
from lxml import etree
import re
with open("124085 非正常酒店.html", "r", encoding="utf") as f:
    html = f.read()

html = etree.HTML(html)
jsonstr = html.xpath('//script[@type="application/ld+json"]/text()')[0]
print(jsonstr)
dict1 = json.loads(jsonstr)  # @graph[2].itemListElement
# dict1["state"]["product"]["prodInfo"]["destinations"]["breadcrumbs"]
print(dict1["@graph"][2]["itemListElement"][0]["name"])