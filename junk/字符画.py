"""
配合【图片转字符画工具】使用
https://image2text.yunser.com/
"""

import re

# 输出所有盲文字符
for i in range(0x2801, 0x2900):
    print(chr(i), end="")

with open("404.html", "r", encoding="utf-8") as f:
    content = f.read()

    # 使用正则表达式删除空行
    content = re.sub(r"⠀", " ", content)

    # 将处理后的内容写回文件
    with open("4042.html", "w", encoding="utf-8") as f:
        f.write(content)
