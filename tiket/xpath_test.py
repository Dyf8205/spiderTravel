# -*- coding:utf-8 -*-
from lxml import etree

with open("1-beach-house-awardwinning-luxury-smart-home-811001762145601690.html","r",encoding="utf-8") as f:
    h =f.read()
etree = etree.HTML(h)
import json
print(etree.xpath('//script[@id="__NEXT_DATA__"]/text()')[0])

# baseDict = json.loads(etree.xpath('//script[@id="__NEXT_DATA__"]/text()')[0])
#
# # props.pageProps.hotelDetailDataResponse.location.coordinates
#
# print(baseDict["props"]["pageProps"]["hotelDetailDataResponse"]["location"]["coordinates"])
#
#
# baseDict["props"]["pageProps"]["hotelDetailDataResponse"]["location"]["coordinates"]