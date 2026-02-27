# -*- coding:utf-8 -*-
from lxml import etree

with open("detail.html","r",encoding="utf-8") as f:
    h =f.read()
etree = etree.HTML(h)
import json
print(etree.xpath("//script[@id='webcore_internal']/text()")[0])