import re
import json

# 读取script文件
with open('./script/3.txt', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"文件大小: {len(content)} 字符\n")

# 使用提供的正则提取JSON

match = re.search(r'self\.__next_f\.push\(\[1,\s*"34:\[.*?null,(\{.+?\})\]\\n"\]\)', content, re.DOTALL)

if match:
    json_str = match.group(1)
    json_str = json_str.replace('\\"', '"')
    json_str = json_str.replace('\\\\', '\\')

    print(f"[OK] 找到匹配的JSON数据")
    print(f"JSON长度: {len(json_str)} 字符\n")
    # 解析JSON
    baseDict = json.loads(json_str)
    # 保存到文件
    with open('./script/3.json', 'w', encoding='utf-8') as f:
        json.dump(baseDict, f, indent=2, ensure_ascii=False)

    print(f"[OK] JSON已保存到: ./script/3.json")
else:
    print("[ERROR] 未找到匹配的内容")
