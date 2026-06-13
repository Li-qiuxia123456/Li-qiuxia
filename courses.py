# -*- coding: utf-8 -*-
"""课程数据。所有 code 字段中不要使用 \n 转义，使用真实换行。"""

COURSES = []

def add(c):
    COURSES.append(c)

# ===== 课程 1：门店客流 =====
add({
    "idx": 1,
    "title": "零售门店客流数据分析",
    "subtitle": "解析线下门店每日客流、时段分布与节假日差异，输出排班与促销建议。",
    "level": "beginner", "level_text": "初级",
    "hours": "9 小时", "rating": "4.8",
    "tags": ["Python 基础", "列表与字典", "数据统计", "零售运营"],
    "goals": "1 掌握列表+字典组织门店客流数据 / 2 按小时和日期计算均值与峰值 / 3 识别高低峰时段 / 4 输出可落地的排班与促销建议",
    "audience": "零售店长、运营经理、数据分析初学者。",
    "prereq": "Python 基础语法（列表、字典、for 循环）。",
    "knowledge": [
        ("1 数据组织：列表 + 字典",
         '<p>每条数据就是一个字典：<code>日、小时、客流</code>，多条组成列表。</p>'),
        ("2 数据统计：求和、求平均、求峰值",
         '<p>用 <code>for</code> 循环遍历累加得到总和；除以样本数得到均值；跟踪最大值。</p>'),
        ("3 业务洞察：高低峰识别",
         '<p>把每小时数据分别收集，计算均值后排序，即可识别高峰与低谷时段。</p>'),
    ],
    "code": '''# 零售门店客流数据分析
traffic = [
    {"day": "周一", "hour": 8,  "count": 32},
    {"day": "周一", "hour": 11, "count": 85},
    {"day": "周一", "hour": 12, "count": 110},
    {"day": "周一", "hour": 18, "count": 156},
    {"day": "周一", "hour": 19, "count": 142},
    {"day": "周一", "hour": 20, "count": 98},
    {"day": "周二", "hour": 8,  "count": 28},
    {"day": "周二", "hour": 11, "count": 80},
    {"day": "周二", "hour": 12, "count": 105},
    {"day": "周二", "hour": 18, "count": 148},
    {"day": "周二", "hour": 19, "count": 138},
    {"day": "周二", "hour": 20, "count": 92},
    {"day": "周三", "hour": 8,  "count": 30},
    {"day": "周三", "hour": 11, "count": 82},
    {"day": "周三", "hour": 12, "count": 108},
    {"day": "周三", "hour": 18, "count": 150},
    {"day": "周三", "hour": 19, "count": 145},
    {"day": "周三", "hour": 20, "count": 100},
    {"day": "周四", "hour": 8,  "count": 35},
    {"day": "周四", "hour": 11, "count": 92},
    {"day": "周四", "hour": 12, "count": 115},
    {"day": "周四", "hour": 18, "count": 162},
    {"day": "周四", "hour": 19, "count": 158},
    {"day": "周四", "hour": 20, "count": 105},
    {"day": "周五", "hour": 8,  "count": 40},
    {"day": "周五", "hour": 11, "count": 98},
    {"day": "周五", "hour": 12, "count": 130},
    {"day": "周五", "hour": 18, "count": 180},
    {"day": "周五", "hour": 19, "count": 175},
    {"day": "周五", "hour": 20, "count": 135},
]

print("==== 整体统计 ====")
total = 0
for t in traffic:
    total = total + t["count"]
avg = total / len(traffic)
print("样本时段数：", len(traffic))
print("总客流：", total, "人")
print("平均每时段客流：", round(avg, 1), "人")

by_hour = {}
for t in traffic:
    h = t["hour"]
    if h not in by_hour:
        by_hour[h] = []
    by_hour[h].append(t["count"])

print()
print("==== 各小时平均客流（从高到低）====")
hour_list = list(by_hour.keys())
for i in range(len(hour_list)):
    for j in range(i+1, len(hour_list)):
        ai = sum(by_hour[hour_list[i]]) / len(by_hour[hour_list[i]])
        aj = sum(by_hour[hour_list[j]]) / len(by_hour[hour_list[j]])
        if aj > ai:
            hour_list[i], hour_list[j] = hour_list[j], hour_list[i]

for h in hour_list:
    counts = by_hour[h]
    avg_h = sum(counts) / len(counts)
    print(str(h) + ":00  平均", round(avg_h, 1), "人")

print()
print("==== 业务建议 ====")
print("最高峰时段：", str(hour_list[0]) + ":00，建议增派店员、加快结账速度")
print("最低谷时段：", str(hour_list[-1]) + ":00，建议推出限时促销")
print("周末（周五晚）客流明显高于工作日，建议：")
print("  1) 周五 18-20 点增派临时兼职")
print("  2) 低谷时段推出限时折扣（如 8 点早餐套餐）")
print("  3) 监控 19 点客流与库存，避免缺货")
''',
    "quiz": [
        ("客流分析中「峰值 / 均值」比值偏高最能直接说明什么？",
         ["门店位置不好", "客流波动较大，需要动态排班", "收银员工作不认真", "店铺租金太高"], 1,
         "比值高意味着高峰时段远高于平时，波动剧烈，固定排班无法应对。"),
        ("按小时分组统计的核心数据结构是？",
         ["一个简单的列表", "字典：key=小时，value=客流列表", "一个字符串", "一组布尔值"], 1,
         "字典 key=小时、value=该小时的所有客流样本列表，便于计算均值。"),
    ],
    "summary": [
        "列表 + 字典是组织结构化数据的最基础形态。",
        "按小时分组求均值、排序后可以识别高低峰时段。",
        "数据 -> 洞察 -> 业务建议，形成完整闭环。",
        "实际落地需要结合排班、库存与促销三个方面协同。",
    ]
})
