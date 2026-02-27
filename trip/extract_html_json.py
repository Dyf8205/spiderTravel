import re
import json


def extract_json_from_html(content):
    """从HTML文件中提取Next.js script中的JSON数据"""


    # 方法1: 正则匹配包含 Jc: 的 self.__next_f.push 内容
    pattern = r'self\.__next_f\.push\(\[1,\s*"Jc:\[.*?null,(\{.+?\})\]\\n"\]\)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        json_str = match.group(1)
        # 处理转义
        json_str = json_str.replace('\\"', '"')
        json_str = json_str.replace('\\\\', '\\')
        print(json_str)
        return json.loads(json_str)
    else:
        raise Exception('')


if __name__ == '__main__':
    data = extract_json_from_html('detail.html')
    if data:
        print(f"成功提取JSON，包含 {len(data)} 个键")
        print("键列表:", list(data.keys())[:10])
    else:
        print("提取失败")
