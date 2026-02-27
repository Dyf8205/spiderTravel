#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从Trip.com酒店详情HTML中提取酒店信息
提取内容：酒店名称、地址、经纬度坐标
"""

import re
import json
from bs4 import BeautifulSoup


def extract_hotel_info(html_file):
    """从HTML文件中提取酒店信息"""

    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    hotel_info = {
        'hotel_name': None,
        'address': None,
        'latitude': None,
        'longitude': None
    }

    # 提取酒店名称
    # 方法1: 从h1标签中提取
    h1_tag = soup.find('h1', class_=re.compile('headInit.*title.*name'))
    if h1_tag:
        hotel_info['hotel_name'] = h1_tag.get_text(strip=True)

    # 提取地址
    # 方法1: 从地址span标签中提取
    address_span = soup.find('span', class_=re.compile('headInit.*address.*text'))
    if address_span:
        hotel_info['address'] = address_span.get('aria-label', '').strip()

    # 提取经纬度坐标
    # 方法1: 从script标签中的JSON数据提取
    script_tags = soup.find_all('script', type='application/json')
    for script in script_tags:
        try:
            json_data = json.loads(script.string)
            # 递归搜索JSON中的lat/lng或latitude/longitude
            coords = find_coordinates_in_json(json_data)
            if coords:
                hotel_info['latitude'] = coords.get('lat') or coords.get('latitude')
                hotel_info['longitude'] = coords.get('lng') or coords.get('longitude')
                if hotel_info['latitude'] and hotel_info['longitude']:
                    break
        except:
            continue

    # 方法2: 从HTML文本中用正则表达式搜索坐标
    if not hotel_info['latitude'] or not hotel_info['longitude']:
        # 搜索常见的坐标格式
        lat_pattern = r'"(?:lat|latitude)":\s*([0-9.]+)'
        lng_pattern = r'"(?:lng|lon|longitude)":\s*([0-9.]+)'

        lat_match = re.search(lat_pattern, html_content)
        lng_match = re.search(lng_pattern, html_content)

        if lat_match:
            hotel_info['latitude'] = float(lat_match.group(1))
        if lng_match:
            hotel_info['longitude'] = float(lng_match.group(1))

    # 方法2.5: 搜索通用的坐标数值对 (纬度范围-90到90, 经度范围-180到180)
    if not hotel_info['latitude'] or not hotel_info['longitude']:
        # 搜索所有可能的坐标数值
        all_coords = re.findall(r'\b(\d{1,3}\.\d{4,})\b', html_content)

        # 尝试找到合理的纬度和经度对
        for i, coord in enumerate(all_coords):
            coord_val = float(coord)
            # 检查是否为有效纬度 (-90 到 90)
            if -90 <= coord_val <= 90 and not hotel_info['latitude']:
                # 检查下一个值是否为有效经度
                if i + 1 < len(all_coords):
                    next_coord = float(all_coords[i + 1])
                    if -180 <= next_coord <= 180:
                        hotel_info['latitude'] = coord_val
                        hotel_info['longitude'] = next_coord
                        break

    # 方法3: 搜索地图相关的URL参数
    if not hotel_info['latitude'] or not hotel_info['longitude']:
        map_pattern = r'[?&](?:lat|latitude)=([0-9.]+).*?[?&](?:lng|lon|longitude)=([0-9.]+)'
        map_match = re.search(map_pattern, html_content)
        if map_match:
            hotel_info['latitude'] = float(map_match.group(1))
            hotel_info['longitude'] = float(map_match.group(2))

    return hotel_info


def find_coordinates_in_json(data, depth=0, max_depth=10):
    """递归搜索JSON数据中的坐标信息"""
    if depth > max_depth:
        return None

    if isinstance(data, dict):
        # 检查当前字典是否包含坐标
        has_lat = any(k in data for k in ['lat', 'latitude'])
        has_lng = any(k in data for k in ['lng', 'lon', 'longitude'])

        if has_lat and has_lng:
            result = {}
            for key in ['lat', 'latitude']:
                if key in data and isinstance(data[key], (int, float)):
                    result['lat'] = data[key]
                    break
            for key in ['lng', 'lon', 'longitude']:
                if key in data and isinstance(data[key], (int, float)):
                    result['lng'] = data[key]
                    break
            if 'lat' in result and 'lng' in result:
                return result

        # 递归搜索子字典
        for value in data.values():
            coords = find_coordinates_in_json(value, depth + 1, max_depth)
            if coords:
                return coords

    elif isinstance(data, list):
        # 递归搜索列表元素
        for item in data:
            coords = find_coordinates_in_json(item, depth + 1, max_depth)
            if coords:
                return coords

    return None


def main():
    html_file = 'detail.html'

    print(f"正在从 {html_file} 提取酒店信息...\n")

    hotel_info = extract_hotel_info(html_file)

    print("=" * 60)
    print("提取结果:")
    print("=" * 60)
    print(f"酒店名称: {hotel_info['hotel_name']}")
    print(f"地址: {hotel_info['address']}")
    print(f"纬度: {hotel_info['latitude']}")
    print(f"经度: {hotel_info['longitude']}")
    print("=" * 60)

    # 保存为JSON文件
    output_file = 'hotel_info.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(hotel_info, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存到: {output_file}")


if __name__ == '__main__':
    main()
