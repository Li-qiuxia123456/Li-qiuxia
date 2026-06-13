# -*- coding: utf-8 -*-
"""
DataLearn 课程详情页生成脚本（Skulpt 轻量版）
- 用 Skulpt 替换 PyScript/Pyodide，无加载、零等待、零超时
- 每门课程示例代码均为纯 Python，无外部库依赖

使用：
  $ python3 gen_courses_skulpt.py
  会在 /workspace 下生成/覆盖 course1.html - course10.html
"""

import os

OUT_DIR = "/workspace"


# ===== 10 门课程数据（每门课程对应一个 dict） =====
# 每个 dict 的结构说明见文档字符串中的 COURSES 数组
# 这里直接给出一个数组
COURSES = []


def add_course(c):
    COURSES.append(c)


# -------- 课程 1 零售门店客流 --------
add_course({
    "idx": 1,
    "title": "零售门店客流数据分析",
    "subtitle": "解析线下门店每日客流 · 时段分布 · 节假日差异 · 输出运营建议",
    "level": "beginner", "level_text": "初级",
    "hours": "9 小时", "rating": "4.8",
    "tags": ["Python 基础", "列表与字典", "数据统计", "零售运营"],
    "goals": "1) 掌握用列表/字典组织门店客流数据\n2) 能按小时、按日期计算客流均值与峰值\n3) 输出可用于门店排班、促销安排的运营建议",
    "audience": "零售运营人员、门店店长、商业数据分析师、入门 Python 学习者",
    "prereq": "Python 基础语法（print / 列表 / 循环 / 条件判断）",
    "knowledge": [
        ("1. 数据组织：按小时存储客流数据", "门店客流最常用的统计口径是「每小时进店人数」。用「小时数 → 客流」的列表/字典组织数据，便于后续做 max/min/mean 等统计。"),
        ("2. 客流指标：最大值、最小值、平均值、高峰时段", "最大值用于识别高峰小时（决定是否增派人力）；平均值代表常态化水平；峰值/平均比值帮助判断波动强度。"),
        ("3. 运营建议输出：高峰多排班，低谷做促销", "若某小时客流显著高于平均 → 增加导购与收银；显著低于平均 → 推出时段折扣/引流活动平衡到店压力。"),
    ],
    "code": "# -*- coding: utf-8 -*-\n# 【零售门店客流分析】示例代码\n# 数据：11:00~20:00 每小时进店人数（模拟 3 天）\nhourly_traffic = [\n    (11, 85, 78, 92),\n    (12, 130, 145, 138),\n    (13, 180, 175, 190),\n    (14, 160, 150, 158),\n    (15, 140, 135, 148),\n    (16, 155, 165, 160),\n    (17, 210, 220, 205),\n    (18, 240, 250, 235),\n    (19, 200, 195, 210),\n    (20, 120, 115, 125),\n]\n\nprint(\"=\" * 52)\nprint(\"1. 每日客流统计（每小时总客流 / 平均 / 峰值）\")\nfor row in hourly_traffic:\n    h = row[0]\n    data = list(row[1:])\n    total = sum(data)\n    avg = total / len(data)\n    print(\"  %02d:00  总客流=%d  平均=%.1f  峰值=%d\" % (h, total, avg, max(data)))\n\nall_values = []\nfor row in hourly_traffic:\n    for v in row[1:]:\n        all_values.append(v)\ndaily_avg = sum(all_values) / len(all_values)\nprint(\"\")\nprint(\"2. 全时段平均客流 = %.1f 人/小时\" % daily_avg)\n\npeak_hours = []\nlow_hours = []\nfor row in hourly_traffic:\n    h = row[0]\n    avg_h = sum(row[1:]) / (len(row) - 1)\n    if avg_h >= daily_avg * 1.3:\n        peak_hours.append((h, avg_h))\n    elif avg_h <= daily_avg * 0.7:\n        low_hours.append((h, avg_h))\n\nprint(\"\")\nprint(\"3. 高峰时段（需增派人力）:\")\nfor h, v in peak_hours:\n    print(\"  %02d:00 平均=%.1f\" % (h, v))\nprint(\"4. 低谷时段（可做时段促销）:\")\nfor h, v in low_hours:\n    print(\"  %02d:00 平均=%.1f\" % (h, v))\n\nprint(\"\")\nprint(\"【运营建议】\")\nprint(\"  - 17:00~18:00 是进店高峰，建议增加 2 名收银员\")\nprint(\"  - 11:00 进店较少，可在 10:30~11:30 推出早鸟折扣\")",
    "quiz": [
        ("在「小时客流」分析中，平均每小时客流的计算公式是？", ["总客流 / 小时数", "总客流 / 天数", "小时客流最大值 / 2", "小时客流最小值 × 2"], 0, "平均每小时客流 = 对应时段总客流 ÷ 小时数，描述常态化水平。"),
        ("识别门店「高峰时段」最合理的做法是？", ["取一个固定阈值（如 >200 人）", "高于全时段均值的某个倍数（如 1.3 倍）", "取客流最大的那 1 小时即可", "取客流最小的那 1 小时"], 1, "用「相对比例」判断高峰更稳健，不会因门店规模差异而失真。"),
        ("Python 中计算列表 a 的最大值，使用哪个函数？", ["max(a)", "min(a)", "sum(a)", "len(a)"], 0, "max(a) 返回列表最大值；min 返回最小值，sum 返回总和，len 返回长度。"),
    ],
    "summary": [
        "用「列表 + 元组」组织结构化数据（小时 + 多天客流）",
        "通过 sum/len 计算平均值、最大值，识别高峰与低谷",
        "把统计结果转化为运营行动：高峰加人力、低谷做促销",
    ],
})


# -------- 课程 2 电商订单异常检测 --------
add_course({
    "idx": 2,
    "title": "电商订单数据异常检测",
    "subtitle": "识别异常订单 · 重复订单 · 虚假订单 · 输出数据治理建议",
    "level": "beginner", "level_text": "初级",
    "hours": "8 小时", "rating": "4.7",
    "tags": ["数据清洗", "异常值", "订单分析", "循环判断"],
    "goals": "1) 学会用「均值+倍数阈值」识别高异常订单\n2) 掌握用字典统计同一用户的重复下单\n3) 输出简单的数据治理建议",
    "audience": "电商运营、订单处理专员、入门数据分析师",
    "prereq": "Python 基础语法（列表 / 字典 / 循环 / 条件判断）",
    "knowledge": [
        ("1. 异常订单判定逻辑：均值 × 倍数阈值", "若订单金额显著高于整体平均（如超过平均值 2 倍），可视为高异常订单，需人工复核。"),
        ("2. 重复订单：同一用户短时间内重复下单", "用订单 user_id 作为分组键，若同一用户出现多次，需判断是真实复购还是误操作。"),
        ("3. 数据治理：人工复核 + 自动拦截", "对识别出的高异常订单，建议先系统标记为「待审核」，再由运营同学二次确认。"),
    ],
    "code": "# -*- coding: utf-8 -*-\n# 【电商订单异常检测】示例代码\n# 数据：订单列表 (order_id, user_id, 金额(元))\norders = [\n    (\"O1001\", \"U001\", 128.0),\n    (\"O1002\", \"U002\", 88.5),\n    (\"O1003\", \"U003\", 5600.0),   # 疑似高异常\n    (\"O1004\", \"U004\", 166.0),\n    (\"O1005\", \"U005\", 99.9),\n    (\"O1006\", \"U002\", 88.5),     # 同一用户重复下单\n    (\"O1007\", \"U006\", 12000.0),  # 疑似高异常\n    (\"O1008\", \"U007\", 218.0),\n    (\"O1009\", \"U008\", 75.0),\n    (\"O1010\", \"U009\", 158.0),\n]\n\namounts = [o[2] for o in orders]\navg = sum(amounts) / len(amounts)\n\nprint(\"=\" * 52)\nprint(\"1. 订单数量 = %d\" % len(orders))\nprint(\"2. 平均订单金额 = %.2f 元\" % avg)\n\nprint(\"\")\nprint(\"3. 高异常订单列表（超过平均值 2 倍）:\")\nhigh_list = []\nfor o in orders:\n    oid, uid, amt = o\n    if amt > avg * 2:\n        high_list.append((oid, uid, amt))\n        print(\"  - 订单 %s  用户 %s  金额 %.2f 元（%.1f 倍均值）\" % (oid, uid, amt, amt / avg))\nif not high_list:\n    print(\"  （无高异常订单）\")\n\nprint(\"\")\nprint(\"4. 同一用户重复下单统计:\")\nuser_count = {}\nfor o in orders:\n    uid = o[1]\n    if uid in user_count:\n        user_count[uid] += 1\n    else:\n        user_count[uid] = 1\ndup_users = [(u, c) for u, c in user_count.items() if c > 1]\nif dup_users:\n    for u, c in dup_users:\n        print(\"  - 用户 %s 共下单 %d 次，需人工复核是否误操作\" % (u, c))\nelse:\n    print(\"  （未发现重复下单用户）\")\n\nprint(\"\")\nprint(\"【数据治理建议】\")\nprint(\"  - 金额超过 2 倍均值的订单，系统自动标记为「待审核」\")\nprint(\"  - 同一用户短期内多次下单，建议弹出二次确认后再提交\")",
    "quiz": [
        ("判断某笔订单是否为「高异常订单」，最常用的简单方法是？", ["只要金额 > 1000 元就算", "金额 > 平均值 × 某个倍数（如 2 倍）", "金额 = 中位数", "金额 < 最小值"], 1, "用「均值+倍数」是最易理解也最常用的简单异常判定方法。"),
        ("统计同一用户的下单次数，适合用什么结构？", ["只存一个列表", "字典（key=用户ID, value=次数）", "只存一个字符串", "只存一个布尔变量"], 1, "字典的「键值对」天然适合做计数统计。"),
        ("对识别出的异常订单，最符合业务逻辑的处理流程是？", ["直接取消订单", "系统标记 → 人工复核 → 再处理", "直接通过所有订单", "直接把账号冻结"], 1, "系统给出的是「疑似异常」，最终决策应结合人工复核，避免误伤正常用户。"),
    ],
    "summary": [
        "用「均值 × 倍数阈值」识别高金额异常订单",
        "用字典（user_id → 次数）统计重复下单用户",
        "异常识别是手段，数据治理才是目标：标记 → 复核 → 改进",
    ],
})


# -------- 课程 3 RFM 用户分层 --------
add_course({
    "idx": 3,
    "title": "用户分层与精准营销分析（RFM 模型）",
    "subtitle": "R/F/M 三维评分 · 用户分层 · 差异化营销策略输出",
    "level": "intermediate", "level_text": "中级",
    "hours": "13 小时", "rating": "4.9",
    "tags": ["RFM 模型", "用户分层", "营销分析", "字典操作"],
    "goals": "1) 理解 R（近度）/F（频度）/M（额度）三维定义\n2) 手动实现 1~5 分打分与分层\n3) 针对不同层给出差异化营销策略",
    "audience": "电商运营、CRM 专员、增长分析师、市场营销人员",
    "prereq": "列表与字典熟练使用、循环与条件判断",
    "knowledge": [
        ("1. R/F/M 三维度定义", "R = 最近一次消费距今天数（越小越好）；F = 某段时间内总下单次数（越大越好）；M = 某段时间内总消费金额（越大越好）。"),
        ("2. 1~5 分区间：用分位数或固定阈值评分", "R 越小得分越高；F/M 越大得分越高。把每维打分后，组合得到 RFM 分层标签。"),
        ("3. 分层与策略匹配：高价值深耕，流失预警挽回", "高 R+高 F+高 M =「重要价值用户」，应做 VIP 维系；低 R+低 F+低 M =「流失用户」，应做流失召回。"),
    ],
    "code": "# -*- coding: utf-8 -*-\n# 【RFM 用户分层】示例代码\n# 数据：每位用户 (user_id, 最近消费距今天数 R, 下单次数 F, 累计消费金额 M)\nusers = [\n    (\"U001\", 3,  12, 4800),\n    (\"U002\", 30,  5, 1200),\n    (\"U003\", 90,  2,  300),\n    (\"U004\", 1,  20, 8500),\n    (\"U005\", 60,  3,  700),\n    (\"U006\", 10,  8, 3600),\n    (\"U007\", 120, 1,  120),\n    (\"U008\", 5,  15, 6200),\n]\n\ndef quantile(values, q):\n    s = sorted(values)\n    idx = int(len(s) * q)\n    if idx >= len(s):\n        idx = len(s) - 1\n    return s[idx]\n\nR_list = [u[1] for u in users]\nF_list = [u[2] for u in users]\nM_list = [u[3] for u in users]\n\nR_q25, R_q75 = quantile(R_list, 0.25), quantile(R_list, 0.75)\nF_q25, F_q75 = quantile(F_list, 0.25), quantile(F_list, 0.75)\nM_q25, M_q75 = quantile(M_list, 0.25), quantile(M_list, 0.75)\n\nprint(\"=\" * 56)\nprint(\"R 分位  25%%=%.2f  75%%=%.2f (R越小越好)\" % (R_q25, R_q75))\nprint(\"F 分位  25%%=%.2f  75%%=%.2f (F越大越好)\" % (F_q25, F_q75))\nprint(\"M 分位  25%%=%.2f  75%%=%.2f (M越大越好)\" % (M_q25, M_q75))\nprint(\"\")\n\ndef score_r(val):\n    if val <= R_q25:\n        return 5\n    elif val <= R_q75:\n        return 3\n    else:\n        return 1\n\ndef score_fm(val, q25, q75):\n    if val >= q75:\n        return 5\n    elif val >= q25:\n        return 3\n    else:\n        return 1\n\nprint(\"%6s  %6s  %6s  %6s  %6s  %6s  %6s  %s\" % (\"用户\", \"R值\", \"F值\", \"M值\", \"R分\", \"F分\", \"M分\", \"分层\"))\nprint(\"-\" * 78)\nfor u in users:\n    uid, R, F, M = u\n    r_s = score_r(R)\n    f_s = score_fm(F, F_q25, F_q75)\n    m_s = score_fm(M, M_q25, M_q75)\n    avg_s = (r_s + f_s + m_s) / 3.0\n    if r_s >= 4 and f_s >= 4 and m_s >= 4:\n        label = \"重要价值用户（VIP）\"\n    elif r_s <= 2 and f_s <= 2 and m_s <= 2:\n        label = \"流失用户（需召回）\"\n    elif r_s >= 4 and f_s <= 2 and m_s <= 2:\n        label = \"新用户（需培养）\"\n    elif r_s <= 2 and (f_s + m_s) >= 8:\n        label = \"重要流失预警用户\"\n    else:\n        label = \"普通活跃用户\"\n    print(\"%6s  %-6d  %-6d  %-6d  %-6d  %-6d  %-6d  %s\" % (uid, R, F, M, r_s, f_s, m_s, label))\n\nprint(\"\")\nprint(\"【营销策略建议】\")\nprint(\"  - VIP 用户：生日礼券 + 专属客服\")\nprint(\"  - 新用户：新人专享礼包 + 首单引导\")\nprint(\"  - 流失预警用户：大额优惠券 + 主动触达\")",
    "quiz": [
        ("在 RFM 模型中，R 维度的含义是？", ["最近一次消费距今天数", "总下单次数", "累计消费金额", "会员等级"], 0, "R = Recency（近度），即最近一次消费距今天数，越小越活跃。"),
        ("下列哪个用户更值得做「VIP 维系」？", ["R=1, F=20, M=8500", "R=120, F=1, M=120", "R=30, F=5, M=1200", "R=60, F=3, M=700"], 0, "R 近 + F/M 高，是典型高价值用户，应做 VIP 维系。"),
        ("哪一句描述更符合「重要流失预警用户」？", ["近期没下单，但历史下单频次和金额都较高", "刚注册、只下过一单", "几乎不下单、也没什么消费", "每天都买，而且金额很大"], 0, "典型「曾经很有价值、最近沉默」的用户，需要主动触达挽回。"),
    ],
    "summary": [
        "R/F/M 三个维度分别代表「近度 / 频度 / 额度」",
        "用分位数（或固定阈值）为每维打 1~5 分，再根据分值做分层",
        "分层标签直接对应营销策略：VIP 维系 / 新用户培养 / 流失召回",
    ],
})


# -------- 课程 4 Apriori 商品关联推荐 --------
add_course({
    "idx": 4,
    "title": "电商商品关联推荐分析（Apriori）",
    "subtitle": "购物篮组合统计 · 高频商品对 · 关联规则与套餐设计",
    "level": "intermediate", "level_text": "中级",
    "hours": "14 小时", "rating": "4.8",
    "tags": ["购物篮", "Apriori", "关联规则", "商品组合"],
    "goals": "1) 理解购物篮分析基本概念：商品组合、出现频次、支持度\n2) 手动统计两两商品共同出现次数\n3) 输出用于套餐设计的高频商品对",
    "audience": "电商商品运营、采购与陈列规划、套餐设计人员",
    "prereq": "列表与字典、集合运算基础",
    "knowledge": [
        ("1. 购物篮数据：订单 → 商品集合", "把每一笔订单看作一个「商品集合」，购物篮分析就是在这些集合中找高频出现的商品组合。"),
        ("2. 商品对频次：两两组合计数", "对每个购物篮生成所有两两组和 (A,B)，再用字典累计所有组合出现次数。次数越高，关联性越强。"),
        ("3. 业务应用：组合推荐、套餐设计、陈列优化", "高频组合可在详情页做「搭配购买」，或在货架相邻陈列；极端高频组合可考虑直接做「组合套餐」。"),
    ],
    "code": "# -*- coding: utf-8 -*-\n# 【商品关联推荐（购物篮）】示例代码\n# 每一张订单 = 一个商品列表（字符串代表 SKU）\nbaskets = [\n    [\"牛奶\", \"面包\", \"鸡蛋\"],\n    [\"牛奶\", \"面包\", \"饼干\"],\n    [\"啤酒\", \"薯片\", \"牛奶\", \"鸡蛋\"],\n    [\"鸡蛋\", \"牛奶\", \"饼干\"],\n    [\"啤酒\", \"薯片\"],\n    [\"面包\", \"鸡蛋\", \"饼干\"],\n    [\"牛奶\", \"面包\", \"鸡蛋\", \"饼干\"],\n    [\"啤酒\", \"薯片\", \"面包\"],\n    [\"牛奶\", \"鸡蛋\"],\n    [\"薯片\", \"饼干\", \"鸡蛋\"],\n]\n\n# 1) 每个商品的出现次数\nitem_count = {}\nfor b in baskets:\n    for item in b:\n        if item in item_count:\n            item_count[item] += 1\n        else:\n            item_count[item] = 1\n\nprint(\"=\" * 52)\nprint(\"1. 各商品出现次数：\")\nfor item, c in sorted(item_count.items(), key=lambda x: -x[1]):\n    print(\"  %s: %d 次\" % (item, c))\n\n# 2) 两两组合出现次数（不区分顺序，i<j 保证不重复）\npair_count = {}\nfor b in baskets:\n    items = sorted(b)\n    n = len(items)\n    for i in range(n):\n        for j in range(i + 1, n):\n            pair = (items[i], items[j])\n            if pair in pair_count:\n                pair_count[pair] += 1\n            else:\n                pair_count[pair] = 1\n\nprint(\"\")\nprint(\"2. 高频商品组合（出现 >= 3 次）:\")\nprint(\"  %-18s %-10s %-10s\" % (\"商品对\", \"共同出现\", \"支持度\"))\ntotal_baskets = len(baskets)\npairs_sorted = sorted(pair_count.items(), key=lambda x: -x[1])\nfor pair, c in pairs_sorted:\n    if c >= 3:\n        support = c * 100.0 / total_baskets\n        print(\"  %s & %s   %-10d  %.1f%%\" % (pair[0], pair[1], c, support))\n\n# 3) 简单置信度：买 A 的用户中同时买 B 的比例\nprint(\"\")\nprint(\"3. 推荐搭配（置信度：买 A → 买 B 的比例，>= 50%）:\")\nmin_conf = 50.0\nfor pair, c in pairs_sorted:\n    if c < 3:\n        continue\n    a, b = pair\n    conf_ab = c * 100.0 / item_count[a]\n    conf_ba = c * 100.0 / item_count[b]\n    if conf_ab >= min_conf:\n        print(\"  买 %s → 买 %s： %.1f%% (共同出现 %d / 买 %s %d 次)\" % (a, b, conf_ab, c, a, item_count[a]))\n    if conf_ba >= min_conf:\n        print(\"  买 %s → 买 %s： %.1f%% (共同出现 %d / 买 %s %d 次)\" % (b, a, conf_ba, c, b, item_count[b]))\n\nprint(\"\")\nprint(\"【套餐建议】\")\nprint(\"  - 牛奶 + 鸡蛋 可做「营养早餐组合」\")\nprint(\"  - 啤酒 + 薯片 可做「追剧零食组合」\")",
    "quiz": [
        ("购物篮分析中，「商品对出现次数」衡量的是？", ["商品 A 与 B 被同一订单同时包含的次数", "商品 A 被单独购买的次数", "商品 A 的总销售额", "两个商品的价格总和"], 0, "共同出现次数是关联分析的核心指标，次数越高关联性越强。"),
        ("「买 A 的用户中同时买 B 的比例」对应的概念是？", ["支持度", "置信度", "客单价", "复购率"], 1, "置信度 = 共同出现次数 / A 出现次数，表示 A→B 的转化能力。"),
        ("统计两两组合出现次数时，对同一购物篮做 i<j 循环的目的是？", ["让代码更长", "避免 (A,B) 和 (B,A) 被算两次", "让组合排序更随机", "方便输出价格"], 1, "i<j 保证每对商品只被数一次，且不区分顺序。"),
    ],
    "summary": [
        "购物篮分析的核心是统计「商品组合」的出现频次",
        "两两组合计数 + 支持度/置信度，即可识别强关联商品",
        "业务产出：搭配推荐、套餐设计、陈列优化",
    ],
})


# -------- 课程 5 员工绩效数据分析 --------
add_course({
    "idx": 5,
    "title": "企业员工绩效数据分析",
    "subtitle": "多表合并思路 · 按部门分组统计 · 绩效排名与部门对比",
    "level": "intermediate", "level_text": "中级",
    "hours": "11 小时", "rating": "4.6",
    "tags": ["分组统计", "HR 分析", "绩效排名", "字典分组"],
    "goals": "1) 用字典做部门分组统计\n2) 计算部门平均分、部门最高分\n3) 输出员工个人排名与部门排名",
    "audience": "HR 专员、人力资源数据分析师、业务负责人",
    "prereq": "列表/字典、循环、简单统计函数",
    "knowledge": [
        ("1. HR 数据常见结构：员工表 + 绩效表", "员工表包含姓名、部门、职级；绩效表包含员工ID、考核期、绩效分。实际分析需把两表合并。"),
        ("2. 分组统计：按部门聚合", "用字典按「部门」分组，每组记录成员分，计算部门均值、最高分、人数，用于部门对比。"),
        ("3. 业务价值：人员结构与部门效能诊断", "部门平均分代表整体水平；高分占比代表梯队质量；与人数结合可判断是否存在「少数人扛多数绩效」现象。"),
    ],
    "code": "# -*- coding: utf-8 -*-\n# 【员工绩效数据分析】示例代码\n# 员工表 (姓名, 部门, 职级)\nemployees = [\n    (\"赵A\", \"销售部\", \"P6\"),\n    (\"钱B\", \"销售部\", \"P5\"),\n    (\"孙C\", \"市场部\", \"P6\"),\n    (\"李D\", \"研发部\", \"P7\"),\n    (\"周E\", \"研发部\", \"P6\"),\n    (\"吴F\", \"研发部\", \"P5\"),\n    (\"郑G\", \"市场部\", \"P5\"),\n    (\"王H\", \"销售部\", \"P6\"),\n    (\"冯I\", \"财务部\", \"P6\"),\n    (\"陈J\", \"财务部\", \"P5\"),\n]\n\n# 绩效表 (姓名, Q2 绩效得分)\nscores = [\n    (\"赵A\", 88),\n    (\"钱B\", 72),\n    (\"孙C\", 80),\n    (\"李D\", 92),\n    (\"周E\", 78),\n    (\"吴F\", 65),\n    (\"郑G\", 70),\n    (\"王H\", 95),\n    (\"冯I\", 82),\n    (\"陈J\", 75),\n]\n\n# 1) 个人绩效排名\nscore_map = {}\nfor name, s in scores:\n    score_map[name] = s\n\nprint(\"=\" * 52)\nprint(\"1. 员工个人绩效排名（按分数降序）:\")\nranked = sorted(scores, key=lambda x: -x[1])\nfor i in range(len(ranked)):\n    name, s = ranked[i]\n    print(\"  %2d. %-6s  分数=%d\" % (i + 1, name, s))\n\n# 2) 员工表 + 绩效表合并（通过姓名匹配）\njoined = []\nfor emp in employees:\n    name, dept, level = emp\n    if name in score_map:\n        joined.append((name, dept, level, score_map[name]))\n    else:\n        joined.append((name, dept, level, None))\n\n# 3) 按部门分组统计：人数 / 平均分 / 最高分\ndept_dict = {}\nfor row in joined:\n    name, dept, level, s = row\n    if s is None:\n        continue\n    if dept not in dept_dict:\n        dept_dict[dept] = []\n    dept_dict[dept].append(s)\n\nprint(\"\")\nprint(\"2. 各部门绩效统计:\")\nprint(\"  %-8s %-8s %-10s %-8s\" % (\"部门\", \"人数\", \"平均分\", \"最高分\"))\ndept_summary = []\nfor dept, vals in dept_dict.items():\n    avg = sum(vals) * 1.0 / len(vals)\n    best = max(vals)\n    dept_summary.append((dept, len(vals), avg, best))\ndept_summary.sort(key=lambda x: -x[2])\nfor d, n, avg, best in dept_summary:\n    print(\"  %-8s %-8d %-10.2f %-8d\" % (d, n, avg, best))\n\nprint(\"\")\nprint(\"【HR 分析结论】\")\nbest_dept = dept_summary[0][0]\nprint(\"  - 部门平均分最高的是 %s，建议作为季度优秀团队表彰\" % best_dept)\nprint(\"  - 分数 < 70 的员工建议安排 1 对 1 辅导与技能培训\")\nprint(\"  - 建议每季度做一次部门横向对比，识别「高绩效部门可复制做法」\")",
    "quiz": [
        ("在按部门做绩效统计时，下列哪种结构最适合存「部门 → 分数列表」？", ["一个普通列表", "字典（key=部门, value=分数列表）", "一个字符串", "一个布尔变量"], 1, "字典天然适合做「分组」统计，key 是部门，value 是该部门的分数列表。"),
        ("合并员工表与绩效表，代码中使用姓名作为匹配键，最应注意？", ["姓名大小写与去空格一致化", "员工年龄", "员工性别", "员工地址"], 0, "姓名/ID 作为匹配键时，必须保证清洗一致，否则会出现无法匹配的情况。"),
        ("想判断一个部门是否「少数人扛多数绩效」，最直观参考？", ["部门最高分与部门平均分的差距", "部门总人数", "员工年龄", "员工性别"], 0, "如果最高分远高于平均分，说明少数人拉高了整体水平；反之代表分布比较平均。"),
    ],
    "summary": [
        "通过姓名/员工ID把「员工表」「绩效表」关联起来",
        "使用字典按部门做分组，计算均值与最高分",
        "部门横向对比 + 个人排名，为团队管理提供量化依据",
    ],
})


# -------- 课程 6 餐饮门店营收分析 --------
add_course({
    "idx": 6,
    "title": "餐饮门店营收数据分析",
    "subtitle": "菜品销量统计 · 时段营收 · 爆款与低效时段识别",
    "level": "intermediate", "level_text": "中级",
    "hours": "10 小时", "rating": "4.7",
    "tags": ["餐饮营收", "菜品分析", "分组统计", "经营诊断"],
    "goals": "1) 统计各菜品销量与营收排名\n2) 按时段识别高营收/低效时段\n3) 输出菜品结构与时段运营建议",
    "audience": "餐饮店长、运营督导、菜单规划人员",
    "prereq": "列表/字典、循环、排序基础",
    "knowledge": [
        ("1. 菜品销售数据：菜名 + 单价 + 销量", "把每笔销售分解为「某菜品 × 数量」，再汇总到菜品维度，即可得到菜品销量与营收排名。"),
        ("2. 时段营收：早中晚三餐分布", "按早餐/午餐/晚餐做时段划分，计算各时段营收占比，识别门店真正的「黄金时段」。"),
        ("3. 经营建议：爆款深耕 + 低效时段引流", "爆款菜品应保留并放大；低效时段可推出「时段套餐」或外卖促销拉动翻台。"),
    ],
    "code": "# -*- coding: utf-8 -*-\n# 【餐饮门店营收分析】示例代码\n# 菜单：菜名 → 单价\nmenu = {\n    \"招牌卤肉饭\": 28,\n    \"宫保鸡丁饭\": 26,\n    \"番茄鸡蛋面\": 22,\n    \"酸辣粉\":     18,\n    \"奶茶\":       12,\n    \"柠檬水\":      8,\n}\n\n# 时段销售：(时段, 菜名, 份数)\nrecords = [\n    (\"午餐\", \"招牌卤肉饭\", 40),\n    (\"午餐\", \"宫保鸡丁饭\", 30),\n    (\"午餐\", \"番茄鸡蛋面\", 15),\n    (\"午餐\", \"奶茶\",       20),\n    (\"午餐\", \"柠檬水\",     25),\n    (\"晚餐\", \"招牌卤肉饭\", 35),\n    (\"晚餐\", \"宫保鸡丁饭\", 28),\n    (\"晚餐\", \"酸辣粉\",     22),\n    (\"晚餐\", \"奶茶\",       30),\n    (\"晚餐\", \"柠檬水\",     15),\n    (\"早餐\", \"番茄鸡蛋面\", 18),\n    (\"早餐\", \"酸辣粉\",     10),\n    (\"早餐\", \"柠檬水\",      8),\n]\n\nprint(\"=\" * 56)\nprint(\"1. 菜品销量 / 营收 排名:\")\nprint(\"  %-14s %-10s %-12s %-10s\" % (\"菜名\", \"总销量\", \"总营收(元)\", \"单价(元)\"))\ndish_sum = {}\nfor slot, dish, cnt in records:\n    if dish in dish_sum:\n        dish_sum[dish] += cnt\n    else:\n        dish_sum[dish] = cnt\nranking = sorted(dish_sum.items(), key=lambda x: -x[1])\nfor dish, cnt in ranking:\n    revenue = cnt * menu[dish]\n    print(\"  %-14s %-10d %-12d %-10d\" % (dish, cnt, revenue, menu[dish]))\n\nslot_rev = {}\nfor slot, dish, cnt in records:\n    rev = cnt * menu[dish]\n    if slot in slot_rev:\n        slot_rev[slot] += rev\n    else:\n        slot_rev[slot] = rev\n\ntotal_rev = sum(slot_rev.values())\nprint(\"\")\nprint(\"2. 各时段营收分布（总营收 = %d 元）:\" % total_rev)\nfor slot in [\"早餐\", \"午餐\", \"晚餐\"]:\n    if slot in slot_rev:\n        r = slot_rev[slot]\n        pct = r * 100.0 / total_rev\n        print(\"  %s：%d 元 (%.1f%%)\" % (slot, r, pct))\n    else:\n        print(\"  %s：无数据\" % slot)\n\nprint(\"\")\nprint(\"3. 爆款菜品（销量 >= 50）:\")\nfor dish, cnt in ranking:\n    if cnt >= 50:\n        print(\"  - %s（共 %d 份）\" % (dish, cnt))\nprint(\"  低效菜品（销量 < 25）:\")\nfor dish, cnt in ranking:\n    if cnt < 25:\n        print(\"  - %s（共 %d 份，可考虑替换或下架）\" % (dish, cnt))\n\nprint(\"\")\nprint(\"【经营建议】\")\nprint(\"  - 午餐/晚餐为黄金时段，建议重点保障热门菜品备料\")\nprint(\"  - 早餐营收较低，可推出「早餐特价套餐」提高翻台\")\nprint(\"  - 可考虑把爆款招牌卤肉饭 + 奶茶 组合为套餐主推\")",
    "quiz": [
        ("判断某菜品是否为「爆款」最直接的参考指标是？", ["菜名好听", "销量/营收排名靠前", "单价贵", "制作时间长"], 1, "爆款应以销量或营收贡献来定义，排名靠前的菜品才是真爆款。"),
        ("想计算「某菜品总营收」，应使用的公式是？", ["该菜品销量 + 单价", "该菜品销量 × 单价", "该菜品销量 - 单价", "该菜品销量 / 单价"], 1, "总营收 = 销量 × 单价。"),
        ("识别门店「黄金时段」，最直观的方法是？", ["看老板心情", "按时段统计营收，占比最高的时段就是黄金时段", "随便猜一个", "看员工排班"], 1, "按时段统计营收并对比，是判断黄金时段的标准做法。"),
    ],
    "summary": [
        "先把菜单（单价）与销售记录分开维护，再合并计算",
        "菜品维度看销量/营收排名；时段维度看各时段贡献占比",
        "最终产出：爆款深耕 + 低效时段引流 + 套餐组合设计",
    ],
})


# -------- 课程 7 库存销量预测（时间序列）--------
add_course({
    "idx": 7,
    "title": "库存销量预测分析（时间序列）",
    "subtitle": "简单移动平均法 · 平滑波动 · 辅助库存与补货决策",
    "level": "advanced", "level_text": "高级",
    "hours": "16 小时", "rating": "4.9",
    "tags": ["时间序列", "移动平均", "销量预测", "库存管理"],
    "goals": "1) 理解简单移动平均法（SMA）的原理\n2) 手动实现 3 期/5 期移动平均\n3) 结合预测值给出库存与补货建议",
    "audience": "供应链/库存管理、商品运营、数据分析工程师",
    "prereq": "列表/循环、基本数值运算",
    "knowledge": [
        ("1. 移动平均法：取近 N 期的平均值作为预测", "简单移动平均（SMA）是最朴素的时间序列预测方法，取最近 N 期实际销量的均值作为下一期预测值，能平滑短期波动。"),
        ("2. N 的选择：窗口大小决定平滑强度", "窗口大（如 5 期）更平滑，适合趋势稳定的商品；窗口小（如 3 期）更灵敏，更贴近近期变化。"),
        ("3. 结合安全库存：预测 + 缓冲", "推荐补货量 = 预测销量 + 安全库存 - 当前库存；安全库存通常取预测的 20%~30% 作为缓冲。"),
    ],
    "code": "# -*- coding: utf-8 -*-\n# 【库存销量预测 · 简单移动平均法】示例代码\n# 数据：最近 8 周某商品的实际销量\nsales = [120, 135, 128, 160, 175, 168, 195, 210]\nweeks = [\"W1\", \"W2\", \"W3\", \"W4\", \"W5\", \"W6\", \"W7\", \"W8\"]\n\nprint(\"=\" * 56)\nprint(\"1. 最近 %d 周实际销量:\" % len(sales))\nfor i in range(len(sales)):\n    print(\"  %s: %d\" % (weeks[i], sales[i]))\n\ndef sma(values, window):\n    if len(values) < window:\n        return None\n    recent = values[-window:]\n    total = 0\n    for v in recent:\n        total += v\n    return total * 1.0 / window\n\npred_3 = sma(sales, 3)\npred_5 = sma(sales, 5)\navg_all = sum(sales) * 1.0 / len(sales)\n\nprint(\"\")\nprint(\"2. 预测结果:\")\nprint(\"  - 全期均值 = %.2f\" % avg_all)\nprint(\"  - 最近 3 期移动平均 = %.2f（更灵敏，适合短期波动商品）\" % pred_3)\nprint(\"  - 最近 5 期移动平均 = %.2f（更平滑，适合趋势稳定商品）\" % pred_5)\n\ncurrent_stock = 180\nsafe_ratio = 0.25\npred = pred_3\nsafe_stock = int(pred * safe_ratio)\nsuggest = int(pred + safe_stock - current_stock)\n\nprint(\"\")\nprint(\"3. 库存与补货建议（以 3 期移动平均为预测值）:\")\nprint(\"  当前库存: %d\" % current_stock)\nprint(\"  下一期预测销量: %.2f\" % pred)\nprint(\"  安全库存(25%%): %d\" % safe_stock)\nif suggest > 0:\n    print(\"  建议补货量: %d（预测 + 安全 - 当前库存）\" % suggest)\nelse:\n    print(\"  库存充足，本期不建议补货（过剩 %d）\" % (-suggest))\n\nprint(\"\")\nprint(\"【趋势判断】\")\nif pred_3 > pred_5:\n    print(\"  最近 3 期均值 > 5 期均值，销量在上升，应加大备货\")\nelif pred_3 < pred_5:\n    print(\"  最近 3 期均值 < 5 期均值，销量在放缓，建议谨慎补货\")\nelse:\n    print(\"  趋势平稳，按常规水平补货即可\")",
    "quiz": [
        ("简单移动平均法（SMA）中，窗口越大，预测值会？", ["越灵敏，跟随短期波动", "越平滑，短期波动被平均掉", "完全等于最大值", "完全等于最小值"], 1, "窗口越大，越会把短期波动平均掉，曲线更平滑。"),
        ("下列哪项最符合「安全库存」的含义？", ["为防止波动与意外而预留的缓冲库存", "仓库里所有货物的总量", "最近一周的销量", "历史最高销量"], 0, "安全库存是应对需求波动或供给延迟预留的缓冲量，通常取预测的一定比例。"),
        ("如果「最近 3 期移动平均」明显大于「最近 5 期移动平均」，往往意味着？", ["销量在下降", "近期销量在上升，趋势向好", "销量完全没有变化", "商品即将下架"], 1, "短期均值 > 长期均值，往往说明最近在放量上升。"),
    ],
    "summary": [
        "简单移动平均 = 最近 N 期实际值的均值，作为下一期预测",
        "窗口越小越灵敏，窗口越大越平滑，按需选择",
        "预测 + 安全库存 - 当前库存 = 补货建议量",
    ],
})


# -------- 课程 8 金融信贷风险评估 --------
add_course({
    "idx": 8,
    "title": "金融信贷风险评估分析",
    "subtitle": "客户画像 · 规则式风控 · 高风险客户识别 · 缺失值处理",
    "level": "advanced", "level_text": "高级",
    "hours": "18 小时",
    "rating": "4.8",
    "tags": ["风控评分", "特征工程", "缺失值", "规则模型"],
    "goals": "1) 构造客户基本画像：年龄、收入、负债、逾期次数\n2) 基于简单规则给出风险评分与等级\n3) 输出高风险客户清单与授信建议",
    "audience": "风控分析师、信贷审批员、金融数据建模人员",
    "prereq": "列表/字典、条件判断、基本数值运算",
    "knowledge": [
        ("1. 风控数据结构：客户画像 + 行为数据", "每位客户抽象为 (年龄, 月收入, 负债, 历史逾期次数, 近 6 月查询次数)。这是规则式风控最常用的 5 个基础特征。"),
        ("2. 规则式评分：按维度加权汇总", "逾期次数越多得分越低；收入越高、负债越低得分越高；查询次数越频繁得分越低。最终按总分划分为低/中/高三档。"),
        ("3. 缺失值处理：保守填充或单独标记", "若某字段缺失，最稳妥的做法是取「对风控较保守」的值（如按高风险方向），或把缺失视为一个单独的风险信号。"),
    ],
    "code": "# -*- coding: utf-8 -*-\n# 【金融信贷风险评估】示例代码\n# 数据：(姓名, 年龄, 月收入(元), 负债(元), 近2年逾期次数, 近6月查询次数)\n# 注：-1 表示该字段缺失（业务常见的缺失值占位）\nclients = [\n    (\"张三\", 30,  12000,   8000, 0, 2),\n    (\"李四\", 45,  35000,  60000, 3, 8),\n    (\"王五\", 25,   6000,  12000, 1, 3),\n    (\"赵六\", 55,  50000, 200000, 5, 12),\n    (\"钱七\", 38,  20000,  10000, 0, 1),\n    (\"孙八\", 28,   9000,     -1, 2, 5),\n    (\"周九\", 50,     -1, 150000, 4, 10),\n    (\"吴十\", 33,  15000,  25000, 0, 2),\n]\n\ndef score_client(age, income, debt, overdue, queries):\n    s = 100\n    # 收入：收入越高越安全（缺失按偏低处理）\n    if income == -1:\n        s -= 15\n    elif income < 8000:\n        s -= 10\n    elif income < 15000:\n        s -= 5\n    # 负债收入比：越高越危险\n    if debt == -1 or income == -1:\n        s -= 10\n    else:\n        ratio = debt * 1.0 / income\n        if ratio > 8:\n            s -= 20\n        elif ratio > 4:\n            s -= 10\n    # 历史逾期：次数越多越危险\n    s -= overdue * 8\n    # 查询次数：越频繁越可能资金紧张\n    if queries >= 10:\n        s -= 15\n    elif queries >= 6:\n        s -= 8\n    # 年龄极端值\n    if age <= 22 or age >= 55:\n        s -= 5\n    return s\n\nprint(\"=\" * 78)\nprint(\"  %-6s  %-6s  %-12s  %-12s  %-6s  %-6s  %-8s  %s\" % (\"姓名\", \"年龄\", \"月收入\", \"负债\", \"逾期\", \"查询\", \"评分\", \"风险档\"))\nresult = []\nfor c in clients:\n    name, age, income, debt, overdue, queries = c\n    s = score_client(age, income, debt, overdue, queries)\n    if s >= 80:\n        level = \"低风险\"\n    elif s >= 60:\n        level = \"中风险\"\n    else:\n        level = \"高风险\"\n    result.append((name, age, income, debt, overdue, queries, s, level))\n    print(\"  %-6s  %-6d  %-12s  %-12s  %-6d  %-6d  %-8d  %s\" % (\n        name, age,\n        (\"缺失\" if income == -1 else str(income)),\n        (\"缺失\" if debt == -1 else str(debt)),\n        overdue, queries, s, level,\n    ))\n\nprint(\"\")\nprint(\"风险档统计:\")\nfor lv in [\"低风险\", \"中风险\", \"高风险\"]:\n    cnt = 0\n    for r in result:\n        if r[7] == lv:\n            cnt += 1\n    print(\"  - %s: %d 人\" % (lv, cnt))\n\nprint(\"\")\nprint(\"【高风险客户清单（建议拒绝或降额）】\")\nfor r in result:\n    if r[7] == \"高风险\":\n        print(\"  - %s（评分 %d）：存在明显风险信号，建议人工审核\" % (r[0], r[6]))",
    "quiz": [
        ("在风控规则式评分中，「历史逾期次数」通常？", ["越多越危险，扣分越多", "越多越安全", "不影响评分", "只影响年龄判断"], 0, "历史逾期是强风险信号，次数越多，还款意愿/能力越差。"),
        ("对缺失字段，最简单且保守的处理方式是？", ["直接忽略该客户", "按「对风控较保守」的方向填充或单独扣分", "随便写一个 0", "写一个很大的数"], 1, "缺失值本身就是一个风险信号，常按较保守的方式处理，而不是直接忽略。"),
        ("「负债收入比」越高，通常意味着？", ["客户越安全", "客户偿债压力越大，风险越高", "客户年龄越大", "客户收入越多"], 1, "负债 / 收入 越高，每月还款压力越大，违约风险越高。"),
    ],
    "summary": [
        "把每位客户抽象成「画像 + 行为」的数值特征",
        "规则式评分 = 各特征按风险强度加减分，再按总分划分高/中/低风险",
        "缺失字段要按「较保守」的方向处理，避免低估风险",
    ],
})


# -------- 课程 9 用户流失预测分析 --------
add_course({
    "idx": 9,
    "title": "平台用户流失预测分析",
    "subtitle": "活跃特征构建 · 沉默期统计 · 流失风险分层与挽回方案",
    "level": "advanced", "level_text": "高级",
    "hours": "17 小时",
    "rating": "4.7",
    "tags": ["流失预测", "活跃特征", "用户分层", "增长分析"],
    "goals": "1) 构建核心活跃特征：近 30 天登录天数、最近登录距今天数、近 30 天消费次数\n2) 基于规则输出流失风险等级\n3) 给出各层用户的挽回与运营策略",
    "audience": "增长运营、用户运营、CRM/社群运营",
    "prereq": "列表/字典、循环、条件判断",
    "knowledge": [
        ("1. 流失分析三剑客：登录频次 + 沉默天数 + 消费频次", "近 30 天登录天数越少、最近一次登录距今越久、消费次数越少 → 流失风险越高。"),
        ("2. 规则式流失分层：高/中/低风险", "用多个阈值组合对用户打标签（如沉默 > 15 天且近 30 天无消费 = 高风险），便于差异化运营。"),
        ("3. 策略匹配：高价值沉默优先挽回", "高价值但流失的用户应优先投放资源挽回；低价值但活跃用户应做转化。"),
    ],
    "code": "# -*- coding: utf-8 -*-\n# 【平台用户流失预测】示例代码\n# 数据：(用户, 近30天登录天数, 最近登录距今天数, 近30天消费次数, 历史总消费金额)\nusers = [\n    (\"U001\", 20,  1,  5,  4800),\n    (\"U002\",  8, 10,  1,  1200),\n    (\"U003\",  2, 25,  0,   150),\n    (\"U004\", 28,  0,  8, 12000),\n    (\"U005\",  4, 18,  0,   300),\n    (\"U006\", 15,  3,  3,  3500),\n    (\"U007\",  1, 40,  0,   200),\n    (\"U008\", 22,  2,  6,  7800),\n    (\"U009\",  6, 14,  1,   800),\n    (\"U010\", 30,  0, 12, 18000),\n]\n\ndef churn_score(login_days, days_since, pay_cnt, total_pay):\n    base = 100\n    # 沉默天数\n    if days_since >= 30:\n        base -= 40\n    elif days_since >= 15:\n        base -= 25\n    elif days_since >= 7:\n        base -= 10\n    # 近 30 天登录天数\n    if login_days <= 3:\n        base -= 25\n    elif login_days <= 7:\n        base -= 15\n    elif login_days <= 15:\n        base -= 5\n    # 近 30 天消费次数\n    if pay_cnt == 0:\n        base -= 15\n    elif pay_cnt <= 2:\n        base -= 8\n    # 历史总消费：金额越高越值得挽回（加分用于优先级排序）\n    add_prio = min(total_pay / 200, 30)\n    return base, base + add_prio\n\nprint(\"=\" * 72)\nprint(\"  %-6s  %-10s  %-10s  %-10s  %-12s  %-10s  %s\" % (\"用户\", \"登录天数\", \"沉默天数\", \"消费次数\", \"历史消费\", \"流失评分\", \"风险档\"))\nstats = {\"高流失风险\": 0, \"中流失风险\": 0, \"低流失风险\": 0}\nhigh_value_lost = []\nfor u in users:\n    name, login_days, days_since, pay_cnt, total_pay = u\n    s, prio = churn_score(login_days, days_since, pay_cnt, total_pay)\n    if s <= 50:\n        level = \"高流失风险\"\n    elif s <= 75:\n        level = \"中流失风险\"\n    else:\n        level = \"低流失风险\"\n    stats[level] += 1\n    if level == \"高流失风险\" and total_pay >= 500:\n        high_value_lost.append((name, total_pay, prio))\n    print(\"  %-6s  %-10d  %-10d  %-10d  %-12d  %-10.1f  %s\" % (\n        name, login_days, days_since, pay_cnt, total_pay, s, level))\n\nprint(\"\")\nprint(\"【风险档汇总】\")\nfor k, v in stats.items():\n    print(\"  - %s: %d 人\" % (k, v))\n\nprint(\"\")\nprint(\"【优先挽回名单（高价值 + 高流失风险）】\")\nhigh_value_lost.sort(key=lambda x: -x[2])\nfor name, total, prio in high_value_lost:\n    print(\"  - %s：历史消费 %d 元，建议推送大额优惠券 + 人工回访\" % (name, total))\n\nprint(\"\")\nprint(\"【通用运营建议】\")\nprint(\"  - 高流失风险用户：推送大额券 + 短信/App Push 触达\")\nprint(\"  - 中流失风险用户：做签到/任务活动，提升登录频次\")\nprint(\"  - 低流失风险用户：做好会员体系与权益持续释放，稳住活跃\")",
    "quiz": [
        ("下列哪项特征通常被视为「高流失风险」信号？", ["最近一次登录距今很久 + 近 30 天没消费", "每天都登录 + 每月都消费", "很年轻", "收入很高"], 0, "长时间沉默 + 无消费是最典型的流失信号。"),
        ("流失预测中，为什么要把「历史总消费」考虑进去？", ["没有什么用", "判断流失是否「可惜」，用于挽回优先级排序", "只看年龄就够了", "只影响注册时间"], 1, "高价值用户的流失更可惜，应优先挽回；历史消费高 + 高流失风险 = 重点对象。"),
        ("对中等流失风险用户，最合理的运营动作是？", ["直接冻结账号", "做签到/任务类活动提升登录频次与粘性", "直接给最大额优惠券", "什么都不做"], 1, "中等风险适合用轻触达 + 轻激励提升活跃，避免一开始就过度补贴。"),
    ],
    "summary": [
        "核心流失特征：最近登录距今天数、近 30 天登录天数、近 30 天消费次数",
        "用简单规则给每位用户打分 → 得到高/中/低流失风险档",
        "高价值但高流失风险用户 → 优先资源挽回；低风险用户 → 稳住活跃",
    ],
})


# -------- 课程 10 A/B 测试数据分析 --------
add_course({
    "idx": 10,
    "title": "A/B 测试数据分析",
    "subtitle": "转化率对比 · 样本量与显著性思路 · 实验结论与上线建议",
    "level": "advanced", "level_text": "高级",
    "hours": "12 小时",
    "rating": "4.8",
    "tags": ["A/B 测试", "转化率", "实验分析", "业务决策"],
    "goals": "1) 计算 A/B 两组的转化率与差值\n2) 判断样本量是否合理（经验参考）\n3) 输出实验结论与上线/驳回建议",
    "audience": "产品经理、增长产品、实验平台数据分析师",
    "prereq": "列表/字典、百分比运算",
    "knowledge": [
        ("1. A/B 测试基础数据：展示数 × 转化数", "每个组有「展示数」和「转化数」两项基本数据；转化率 = 转化数 / 展示数。"),
        ("2. 差值与提升率：判断实验组是否优于对照组", "提升率 = (实验组转化率 - 对照组转化率) / 对照组转化率。提升率为正且绝对值较大才有业务意义。"),
        ("3. 样本量的直觉判断：每组成千上万比较稳妥", "若每组只有几百个样本，波动可能很大，应谨慎。一般经验：每组展示数 >= 1000 且转化数 >= 30，结论更可靠。"),
    ],
    "code": "# -*- coding: utf-8 -*-\n# 【A/B 测试分析】示例代码\n# 实验：按钮文案改版。对照组 =「立即购买」，实验组 =「限时优惠」\n# 数据：(组别, 展示数, 点击转化数)\nexperiments = [\n    (\"A-对照组\", 10000, 820),\n    (\"B-实验组\", 10000, 1015),\n]\n\n# 1) 计算各组转化率\nprint(\"=\" * 64)\nprint(\"1. 各组转化率:\")\nprint(\"  %-12s  %-10s  %-10s  %-12s\" % (\"组别\", \"展示数\", \"转化数\", \"转化率\"))\nresults = []\nfor name, show, conv in experiments:\n    rate = conv * 100.0 / show\n    results.append((name, show, conv, rate))\n    print(\"  %-12s  %-10d  %-10d  %-12.2f%%\" % (name, show, conv, rate))\n\n# 2) 计算差值与提升率（相对第二组 vs 第一组）\nname_a, show_a, conv_a, rate_a = results[0]\nname_b, show_b, conv_b, rate_b = results[1]\ndiff_abs = rate_b - rate_a\nlift = diff_abs * 100.0 / rate_a\nprint(\"\")\nprint(\"2. 实验组 vs 对照组:\")\nprint(\"  绝对差值 = %.2f%%（B 组比 A 组）\" % diff_abs)\nprint(\"  相对提升率 = %.2f%%\" % lift)\n\n# 3) 样本量是否足够的经验判断（每组展示数 >= 1000 且转化数 >= 30）\nprint(\"\")\nprint(\"3. 样本量检查:\")\nsample_ok = True\nfor name, show, conv, rate in results:\n    if show < 1000 or conv < 30:\n        print(\"  - %s：展示数 %d 或转化数 %d 偏小，建议继续实验\" % (name, show, conv))\n        sample_ok = False\nif sample_ok:\n    print(\"  - 两组样本量均满足基本要求（展示 >= 1000, 转化 >= 30）\")\n\n# 4) 结论与上线建议\nprint(\"\")\nprint(\"【实验结论与上线建议】\")\nif diff_abs > 0 and sample_ok:\n    print(\"  - 实验组转化率高于对照组，提升率约 %.2f%%\" % lift)\n    print(\"  - 建议：可先小流量放量验证，再逐步全量上线\")\nelif diff_abs > 0 and not sample_ok:\n    print(\"  - 实验组看起来更好，但样本量偏小，建议延长实验再决策\")\nelif diff_abs == 0:\n    print(\"  - 两组完全相同，没有显著差异，可按成本选择\")\nelse:\n    print(\"  - 实验组反而更差，建议不采用该方案，再迭代其他版本\")\n\nprint(\"\")\nprint(\"【数据分析师注意点】\")\nprint(\"  - 务必确认两组流量分配是否随机\")\nprint(\"  - 注意同期是否有节假日、