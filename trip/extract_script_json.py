import re
import json


def extract_json_from_script(file_path):
    """从Next.js script内容中提取JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 self.__next_f.push([1,"..."]) 中的内容
    # 提取 Jc:["$","@f",null,{...}] 中的JSON对象
    pattern = r'self\.__next_f\.push\(\[1,"Jc:\[\\"\\$\\",\\"@f\\",null,(.+?)\]\\n"\]\)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        json_str = match.group(1)
        # 处理转义：\" -> "
        json_str = json_str.replace('\\"', '"')
        # 处理转义：\\ -> \
        json_str = json_str.replace('\\\\', '\\')
        print(json_str)
        return json.loads(json_str)

    # 备选方案：直接找大括号包裹的JSON
    pattern2 = r'null,(\{.+\})\]\\n"\]\)'
    match2 = re.search(pattern2, content, re.DOTALL)
    if match2:
        json_str = match2.group(1)
        json_str = json_str.replace('\\"', '"')
        json_str = json_str.replace('\\\\', '\\')
        print(json_str)
        return json.loads(json_str)

    return None


if __name__ == '__main__':
    data = extract_json_from_script('111.txt')
    # if data:
    #     print(f"成功提取JSON，包含 {len(data)} 个键")
    #     print("键列表:", list(data.keys())[:10])
    # else:
    #     print("提取失败")
