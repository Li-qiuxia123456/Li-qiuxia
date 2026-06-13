#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""预处理 build.py：把 `%(name)s` 命名占位符改为 `%s`，并确保 CSS/JS 中的 % 已转义为 %%"""
import re

with open("build.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1) 先找到所有 `%(xxx)s` 形式的命名占位符，按出现顺序改为 `%s`
# 注意：`%(idx)02d` 这样的也存在
# 用正则匹配 `%\([a-zA-Z_][a-zA-Z0-9_]*\)(?:\d*\.?\d*)?[sdfeEgGhHbBxXo]`
pattern = re.compile(r"%\([a-zA-Z_][a-zA-Z0-9_]*\)(?:\d*\.?\d*)?[sdfeEgGhHbBxXo]")

# 仅替换「HTML 模板字符串内部」的命名占位符：
# 简化处理：全文把 `%(name)s` 等改为 `%s`，然后确保 CSS/JS 里的 %（width: 100%; 等）变成 %%
# 但这里有个问题：如果 CSS/JS 里有 `%`，而且已经是 `%s` 的话，替换后就会出错。
# 解决方法：我们先把所有非模板用的 `%` 先转义为 `%%`，然后再把命名占位符替换为 `%s`。
#
# 更简单可靠的方法：直接把 `%(name)s` 的命名部分去掉，变成 `%s` / `%02d` 等。
# 只需要：`%(name)XX` → `%XX`，保留最后的格式符
content2 = pattern.sub(lambda m: "%" + m.group(0).rsplit(")", 1)[1], content)

# 2) 检查是否在 CSS/JS 里还留有单独的 %（比如 width: 100%; 或者 CSS 的 %）
# 我们的 HTML 模板里有大量的 CSS `%`。这些在 Python 字符串格式化时会被当成格式化符号。
# 我们需要：所有不是 `%s` / `%d` / `%02d` / `%f` / `%%` 的独立 % 都应该转义为 %%
# 这里手工识别太复杂，让我们用另一种思路：把 `%s` 先用临时标记替换，然后把剩余的所有 `%` 替换为 `%%`，最后把临时标记替换回 `%s` 等。

# 先收集所有格式化标记
tokens = []
def collect(m):
    tokens.append(m.group(0))
    return "\x00%04d\x00" % (len(tokens) - 1)
content3 = re.sub(r"%(?:\d*\.?\d*)?[sdfeEgGhHbBxXo%]", collect, content2)

# 剩余的 % 全部替换为 %%
content3 = content3.replace("%", "%%")

# 把临时标记恢复为真正的格式化标记
for i, tok in enumerate(tokens):
    content3 = content3.replace("\x00%04d\x00" % i, tok)

with open("build.py", "w", encoding="utf-8") as f:
    f.write(content3)

print("完成：共替换 %d 个命名/位置格式化标记，其余所有 %% 已转义" % len(tokens))
