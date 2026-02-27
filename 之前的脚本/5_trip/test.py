import random
import string

def generate_random_string(length=12):
    # 定义字符集：数字+小写字母+大写字母
    characters = string.ascii_letters + string.digits
    # 随机选择字符并组合
    return ''.join(random.choice(characters) for _ in range(length))

# 生成12位随机字符串
random_str = generate_random_string(12)
print(random_str)  # 例如：aB3dFg7H9jK1

import time

# 获取当前13位时间戳（毫秒级）
timestamp_13 = int(time.time() * 1000)
print(f"13位时间戳: {timestamp_13}")
# 例如：1700000000123

import random

# 生成9位随机数字字符串
nine_digit_str = ''.join(random.choices('0123456789', k=9))
print(f"9位随机数字字符串: {nine_digit_str}")
# 例如：'987654321'