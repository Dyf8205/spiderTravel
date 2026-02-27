# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/26 9:58
# explain:
import json
import re
with open("test.html") as f:
    website_snapshot = f.read()

pattern = r'self\.__next_f\.push\(\[1,\s*"Jc:\[.*?null,(\{.+?\})\]\\n"\]\)'
match = re.search(pattern, i["website_snapshot"], re.DOTALL)

if match:
    json_str = match.group(1)
    # 处理转义
    json_str = json_str.replace('\\"', '"')
    json_str = json_str.replace('\\\\', '\\')
    baseDict = json.loads(json_str)
