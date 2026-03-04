import re
import json

# 读取script文件
with open('./script/2.txt', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"文件大小: {len(content)} 字符\n")

# 使用提供的正则提取JSON
try:
    match = re.search(r'self\.__next_f\.push\(\[1,\s*"34:\[.*?null,(\{.+?\})\]\\n"\]\)', content, re.DOTALL)

    if match:
        json_str = match.group(1)
        json_str = json_str.replace('\\"', '"')
        json_str = json_str.replace('\\\\', '\\')
        # 解析JSON
        baseDict = json.loads(json_str)
        name = baseDict["platformProps"]["additionalPlatformProps"]["apolloCacheData"][1]["data"]["storepageFeed"]["storeHeader"]["business"]["name"]
        raise Exception("获取name失败")
    else:
        raise Exception("获取解析失败")
except Exception as e:
    raise Exception("获取json失败")
