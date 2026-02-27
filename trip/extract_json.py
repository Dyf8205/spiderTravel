import re
import json
from html.parser import HTMLParser


def extract_json_by_regex(html_path):
    """使用正则表达式提取script中的JSON"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 匹配 <script id="webcore_internal" type="application/json">...</script>
    pattern = r'<script\s+id="webcore_internal"\s+type="application/json"[^>]*>\s*([\s\S]*?)\s*</script>'
    match = re.search(pattern, html_content)

    if match:
        json_str = match.group(1)
        return json.loads(json_str)
    return None


class ScriptExtractor(HTMLParser):
    """使用HTMLParser提取指定script标签内容"""
    def __init__(self, target_id):
        super().__init__()
        self.target_id = target_id
        self.in_target = False
        self.content = None

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            attrs_dict = dict(attrs)
            if attrs_dict.get('id') == self.target_id:
                self.in_target = True

    def handle_endtag(self, tag):
        if tag == 'script' and self.in_target:
            self.in_target = False

    def handle_data(self, data):
        if self.in_target:
            self.content = data.strip()


def extract_json_by_html_parser(html_path):
    """使用标准库HTMLParser提取script中的JSON"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    parser = ScriptExtractor('webcore_internal')
    parser.feed(html_content)

    if parser.content:
        return json.loads(parser.content)
    return None


if __name__ == '__main__':
    html_path = 'detail.html'

    # 方法1: 正则表达式
    print("=== 使用正则表达式 ===")
    data = extract_json_by_regex(html_path)
    if data:
        print(f"成功提取JSON，包含 {len(data)} 个键")
        print("前5个键:", list(data.keys())[:5])

    print()

    # 方法2: HTMLParser
    print("=== 使用HTMLParser ===")
    data = extract_json_by_html_parser(html_path)
    if data:
        print(f"成功提取JSON，包含 {len(data)} 个键")
        print("前5个键:", list(data.keys())[:5])
