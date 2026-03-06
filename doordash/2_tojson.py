import re
import json

# 读取script文件
with open('./script/4.txt', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"文件大小: {len(content)} 字符\n")

# 使用提供的正则提取JSON
try:
    match = re.search(r'self\.__next_f\.push\(\[1,\s*"2e:\[.*?null,(\{.+?\})\]\\n"\]\)', content, re.DOTALL)

    if match:
        json_str = match.group(1)
        json_str = json_str.replace('\\"', '"')
        json_str = json_str.replace('\\\\', '\\')
        # 解析JSON
        baseDict = json.loads(json_str)
        print(baseDict)
        name = baseDict["platformProps"]["additionalPlatformProps"]
        print(name)
        # raise Exception("获取name失败")
    else:
        # print(e)
        pass
except Exception as e:
    print(e)
