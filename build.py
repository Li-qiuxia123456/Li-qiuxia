# -*- coding: utf-8 -*-
"""构建脚本：生成 index.html + course1.html ~ course10.html（Skulpt 轻量版）"""
import os, io, sys

OUT = "/workspace"

# ======================= 课程数据 =======================
# 为避免 Write 工具中文截断，此处直接用纯 ASCII 英文字段结构，
# 再在文件中用多行字符串拼接中文内容。

# 一门课程一个 dict，下面是「元数据结构」，具体内容在稍后的构建脚本中通过 f-string 填充
COURSES_META = []


def add(idx, title, subtitle, level, level_text, hours, rating, tags,
        goals, audience, prereq, knowledge, code, quiz, summary):
    COURSES_META.append(dict(
        idx=idx, title=title, subtitle=subtitle, level=level,
        level_text=level_text, hours=hours, rating=rating, tags=tags,
        goals=goals, audience=audience, prereq=prereq,
        knowledge=knowledge, code=code, quiz=quiz, summary=summary,
    ))


# 为了避免文本工具字符截断问题，我把每门课程的大段文字（code / 解释）
# 单独存到字符串变量，再在 add 调用里引用。

# -------- 课程 1 零售门店客流 --------
C1_TAGS = ["Python基础", "列表与字典", "数据统计", "零售运营"]
C1_KNOW = [
    ("1. 数据组织：按小时存储客流数据",
     "门店客流最常用的统计口径是「每小时进店人数」。用「小时数 -> 客流」的列表/字典组织数据，便于后续做 max/min/mean 等统计。"),
    ("2. 客流指标：最大值、最小值、平均值、高峰时段",
     "最大值用来识别高峰小时（决定是否增派人力）；平均值代表常态化水平；峰值/平均比值帮助判断波动强度。"),
    ("3. 运营建议输出：高峰多排班，低谷做促销",
     "若某小时客流显著高于平均 -> 增加导购与收银；显著低于平均 -> 推出时段折扣/引流活动平衡到店压力。"),
]
C1_CODE = """hourly = [(11,85,78,92),(12,130,145,138),(13,180,175,190),
          (14,160,150,158),(15,140,135,148),(16,155,165,160),
          (17,210,220,205),(18,240,250,235),(19,200,195,210),
          (20,120,115,125)]
print("1. 每日客流小时统计（小时, 总客流, 平均, 峰值）")
for row in hourly:
    h = row[0]
    data = list(row[1:])
    total = sum(data)
    avg = total / len(data)
    print("  %02d 总=%d 平均=%.1f 峰值=%d" %% (h, total, avg, max(data)))

all_values = []
for row in hourly:
    for v in row[1:]:
        all_values.append(v)
daily_avg = sum(all_values) / len(all_values)
print("")
print("2. 全时段平均客流 = %.1f 人/小时" %% daily_avg)

peak_hours = []
low_hours = []
for row in hourly:
    h = row[0]
    avg_h = sum(row[1:]) / (len(row) - 1)
    if avg_h >= daily_avg * 1.3:
        peak_hours.append((h, avg_h))
    elif avg_h <= daily_avg * 0.7:
        low_hours.append((h, avg_h))

print("")
print("3. 高峰时段（需增派人力）:" + str(peak_hours))
print("4. 低谷时段（可做时段促销）:" + str(low_hours))
print("")
print("【运营建议】")
print("  - 17:00~18:00 是进店高峰，建议增加 2 名收银员")
print("  - 11:00 进店较少，可在 10:30~11:30 推出早鸟折扣")
"""

C1_QUIZ = [
    ("在「小时客流」分析中，平均每小时客流的计算公式是？",
     ["总客流 / 小时数", "总客流 / 天数", "小时客流最大值 / 2", "小时客流最小值 x 2"], 0,
     "平均每小时客流 = 对应时段总客流 ÷ 小时数，描述常态化水平。"),
    ("识别门店「高峰时段」最合理的做法是？",
     ["取一个固定阈值（如 > 200 人）", "高于全时段均值的某个倍数（如 1.3 倍）",
      "取客流最大的那 1 小时即可", "取客流最小的那 1 小时"], 1,
     "用「相对比例」判断高峰更稳健，不会因门店规模差异而失真。"),
    ("Python 中计算列表 a 的最大值，使用哪个函数？",
     ["max(a)", "min(a)", "sum(a)", "len(a)"], 0,
     "max(a) 返回列表最大值；min 返回最小值，sum 返回总和，len 返回长度。"),
]
C1_SUMMARY = [
    "用「列表 + 元组」组织结构化数据（小时 + 多天客流）",
    "通过 sum/len 计算平均值、最大值，识别高峰与低谷",
    "把统计结果转化为运营行动：高峰加人力、低谷做促销",
]


# -------- 课程 2 电商订单异常检测 --------
C2_TAGS = ["数据清洗", "异常值", "订单分析", "循环判断"]
C2_KNOW = [
    ("1. 异常订单判定逻辑：均值 x 倍数阈值",
     "若订单金额显著高于整体平均（如超过平均值 2 倍），可视为高异常订单，需人工复核。"),
    ("2. 重复订单：同一用户短时间内重复下单",
     "用订单 user_id 作为分组键，若同一用户出现多次，需判断是真实复购还是误操作。"),
    ("3. 数据治理：人工复核 + 自动拦截",
     "对识别出的高异常订单，建议先系统标记为「待审核」，再由运营同学二次确认。"),
]
C2_CODE = """orders = [
    ("O1001","U001",128.0), ("O1002","U002",88.5),
    ("O1003","U003",5600.0),("O1004","U004",166.0),
    ("O1005","U005",99.9), ("O1006","U002",88.5),
    ("O1007","U006",12000.0),("O1008","U007",218.0),
    ("O1009","U008",75.0),  ("O1010","U009",158.0),
]
amounts = [o[2] for o in orders]
avg = sum(amounts) / len(amounts)
print("1. 订单数量 = %d, 平均金额 = %.2f 元" %% (len(orders), avg))
print("")
print("2. 高异常订单列表（超过平均值 2 倍）:")
for o in orders:
    oid, uid, amt = o
    if amt > avg * 2:
        print("  - %s (用户 %s, 金额 %.2f, %.1f 倍均值)" %% (oid, uid, amt, amt/avg))

print("")
print("3. 同一用户重复下单统计:")
user_count = {}
for o in orders:
    uid = o[1]
    if uid in user_count:
        user_count[uid] += 1
    else:
        user_count[uid] = 1
for u, c in user_count.items():
    if c > 1:
        print("  - 用户 %s 共下单 %d 次，需人工复核" %% (u, c))

print("")
print("【数据治理建议】")
print("  - 金额超过 2 倍均值的订单，系统自动标记为「待审核」")
print("  - 同一用户短期内多次下单，建议弹出二次确认后再提交")
"""

C2_QUIZ = [
    ("判断某笔订单是否为「高异常订单」，最常用的简单方法是？",
     ["只要金额 > 1000 元就算", "金额 > 平均值 x 某个倍数（如 2 倍）",
      "金额 = 中位数", "金额 < 最小值"], 1,
     "用「均值 + 倍数」是最易理解也最常用的简单异常判定方法。"),
    ("统计同一用户的下单次数，适合用什么结构？",
     ["只存一个列表", "字典（key=用户ID, value=次数）", "只存一个字符串", "只存一个布尔变量"], 1,
     "字典的「键值对」天然适合做计数统计。"),
    ("对识别出的异常订单，最符合业务逻辑的处理流程是？",
     ["直接取消订单", "系统标记 -> 人工复核 -> 再处理",
      "直接通过所有订单", "直接把账号冻结"], 1,
     "系统给出的是「疑似异常」，最终决策应结合人工复核，避免误伤正常用户。"),
]
C2_SUMMARY = [
    "用「均值 x 倍数阈值」识别高金额异常订单",
    "用字典（user_id -> 次数）统计重复下单用户",
    "异常识别是手段，数据治理才是目标：标记 -> 复核 -> 改进",
]


# -------- 课程 3 RFM 用户分层 --------
C3_TAGS = ["RFM模型", "用户分层", "营销分析", "字典操作"]
C3_KNOW = [
    ("1. R/F/M 三个维度定义",
     "R = 最近一次消费距今天数（越小越好）；F = 某段时间内总下单次数（越大越好）；M = 某段时间内总消费金额（越大越好）。"),
    ("2. 1~5 分区间：用分位数或固定阈值评分",
     "R 越小得分越高；F/M 越大得分越高。把每维打分后，组合得到 RFM 分层标签。"),
    ("3. 分层与策略匹配：高价值深耕，流失预警挽回",
     "高 R + 高 F + 高 M =「重要价值用户」，应做 VIP 维系；低 R + 低 F + 低 M =「流失用户」，应做流失召回。"),
]
C3_CODE = """users = [
    ("U001",3,12,4800),("U002",30,5,1200),("U003",90,2,300),
    ("U004",1,20,8500),("U005",60,3,700),("U006",10,8,3600),
    ("U007",120,1,120),("U008",5,15,6200),
]
R_list = [u[1] for u in users]
F_list = [u[2] for u in users]
M_list = [u[3] for u in users]

def q25(vals): return sorted(vals)[int(len(vals)*0.25)]
def q75(vals): return sorted(vals)[int(len(vals)*0.75)]
R25, R75 = q25(R_list), q75(R_list)
F25, F75 = q25(F_list), q75(F_list)
M25, M75 = q25(M_list), q75(M_list)

print("1. 分位数（用于评分阈值）:")
print("  R: q25=%.2f, q75=%.2f (R越小越好)" %% (R25, R75))
print("  F: q25=%.2f, q75=%.2f (F越大越好)" %% (F25, F75))
print("  M: q25=%.2f, q75=%.2f (M越大越好)" %% (M25, M75))
print("")

print("2. 每位用户的 R/F/M 分值与分层标签:")
for u in users:
    uid, R, F, M = u
    r_s = 5 if R <= R25 else (3 if R <= R75 else 1)
    f_s = 5 if F >= F75 else (3 if F >= F25 else 1)
    m_s = 5 if M >= M75 else (3 if M >= M25 else 1)
    if r_s >= 4 and f_s >= 4 and m_s >= 4:
        label = "重要价值用户（VIP）"
    elif r_s <= 2 and f_s <= 2 and m_s <= 2:
        label = "流失用户（需召回）"
    elif r_s <= 2 and (f_s + m_s) >= 8:
        label = "重要流失预警用户"
    elif r_s >= 4 and f_s <= 2 and m_s <= 2:
        label = "新用户（需培养）"
    else:
        label = "普通活跃用户"
    print("  %s  R=%d->%d分  F=%d->%d分  M=%d->%d分  ->%s" %% (uid, R, r_s, F, f_s, M, m_s, label))

print("")
print("【营销策略建议】")
print("  - VIP 用户：生日礼券 + 专属客服")
print("  - 新用户：新人专享礼包 + 首单引导")
print("  - 流失预警用户：大额优惠券 + 主动触达")
"""

C3_QUIZ = [
    ("在 RFM 模型中，R 维度的含义是？",
     ["最近一次消费距今天数", "总下单次数", "累计消费金额", "会员等级"], 0,
     "R = Recency（近度），即最近一次消费距今天数，越小越活跃。"),
    ("下列哪个用户更值得做「VIP 维系」？",
     ["R=1, F=20, M=8500", "R=120, F=1, M=120",
      "R=30, F=5, M=1200", "R=60, F=3, M=700"], 0,
     "R 近 + F/M 高，是典型高价值用户，应做 VIP 维系。"),
    ("哪一句描述更符合「重要流失预警用户」？",
     ["近期没下单，但历史下单频次和金额都较高", "刚注册、只下过一单",
      "几乎不下单、也没什么消费", "每天都买，而且金额很大"], 0,
     "典型「曾经很有价值、最近沉默」的用户，需要主动触达挽回。"),
]
C3_SUMMARY = [
    "R/F/M 三个维度分别代表「近度 / 频度 / 额度」",
    "用分位数（或固定阈值）为每维打 1~5 分，再根据分值做分层",
    "分层标签直接对应营销策略：VIP 维系 / 新用户培养 / 流失召回",
]


# -------- 课程 4 Apriori / 关联推荐 --------
C4_TAGS = ["购物篮", "Apriori", "关联规则", "商品组合"]
C4_KNOW = [
    ("1. 购物篮数据：订单 -> 商品集合",
     "把每一笔订单看作一个「商品集合」，购物篮分析就是在这些集合中找高频出现的商品组合。"),
    ("2. 商品对频次：两两组合计数",
     "对每个购物篮生成所有两两组和 (A,B)，再用字典累计所有组合出现次数。次数越高，关联性越强。"),
    ("3. 业务应用：组合推荐、套餐设计、陈列优化",
     "高频组合可在详情页做「搭配购买」，或在货架相邻陈列；极端高频组合可考虑直接做「组合套餐」。"),
]
C4_CODE = """baskets = [
    ["牛奶","面包","鸡蛋"],["牛奶","面包","饼干"],
    ["啤酒","薯片","牛奶","鸡蛋"],["鸡蛋","牛奶","饼干"],
    ["啤酒","薯片"],["面包","鸡蛋","饼干"],
    ["牛奶","面包","鸡蛋","饼干"],["啤酒","薯片","面包"],
    ["牛奶","鸡蛋"],["薯片","饼干","鸡蛋"],
]
item_count = {}
for b in baskets:
    for item in b:
        if item in item_count: item_count[item] += 1
        else: item_count[item] = 1

print("1. 各商品出现次数: " + str(sorted(item_count.items())))
print("")

pair_count = {}
for b in baskets:
    items = sorted(b)
    n = len(items)
    for i in range(n):
        for j in range(i+1, n):
            pair = (items[i], items[j])
            if pair in pair_count: pair_count[pair] += 1
            else: pair_count[pair] = 1

print("2. 高频商品组合（共同出现 >= 3 次）:")
total_baskets = len(baskets)
top_pairs = sorted(pair_count.items(), key=lambda x: -x[1])
for pair, c in top_pairs:
    if c >= 3:
        print("  %s & %s: %d 次, 支持度 %.1f%%" %% (pair[0], pair[1], c, c*100.0/total_baskets))

print("")
print("3. 置信度：买 A -> 买 B 的比例（>= 50%% 显示）:")
for pair, c in top_pairs:
    if c < 3: continue
    a, b = pair
    conf_ab = c * 100.0 / item_count[a]
    conf_ba = c * 100.0 / item_count[b]
    if conf_ab >= 50:
        print("  买 %s -> 买 %s: %.1f%%" %% (a, b, conf_ab))
    if conf_ba >= 50 and a != b:
        print("  买 %s -> 买 %s: %.1f%%" %% (b, a, conf_ba))

print("")
print("【套餐建议】")
print("  - 牛奶 + 鸡蛋 可做「营养早餐组合」")
print("  - 啤酒 + 薯片 可做「追剧零食组合」")
"""

C4_QUIZ = [
    ("购物篮分析中，「商品对共同出现次数」衡量的是？",
     ["商品 A 与 B 被同一订单同时包含的次数", "商品 A 被单独购买的次数",
      "商品 A 的总销售额", "两个商品的价格总和"], 0,
     "共同出现次数是关联分析的核心指标，次数越高关联性越强。"),
    ("「买 A 的用户中同时买 B 的比例」对应概念是？",
     ["支持度", "置信度", "客单价", "复购率"], 1,
     "置信度 = 共同出现次数 / A 出现次数，表示 A->B 的转化能力。"),
    ("统计两两组合出现次数时，对同一购物篮做 i<j 循环的目的是？",
     ["让代码更长", "避免 (A,B) 和 (B,A) 被算两次",
      "让组合排序更随机", "方便输出价格"], 1,
     "i<j 保证每对商品只被数一次，且不区分顺序。"),
]
C4_SUMMARY = [
    "购物篮分析的核心是统计「商品组合」的出现频次",
    "两两组合计数 + 支持度/置信度，即可识别强关联商品",
    "业务产出：搭配推荐、套餐设计、陈列优化",
]


# -------- 课程 5 员工绩效分析 --------
C5_TAGS = ["分组统计", "HR分析", "绩效排名", "字典分组"]
C5_KNOW = [
    ("1. HR 数据常见结构：员工表 + 绩效表",
     "员工表包含姓名、部门、职级；绩效表包含员工ID、考核期、绩效分。实际分析需把两表合并。"),
    ("2. 分组统计：按部门聚合",
     "用字典按「部门」分组，每组记录成员分，计算部门均值、最高分、人数，用于部门对比。"),
    ("3. 业务价值：人员结构与部门效能诊断",
     "部门平均分代表整体水平；高分占比代表梯队质量；与人数结合可判断是否存在「少数人扛多数绩效」现象。"),
]
C5_CODE = """employees = [("赵A","销售部"),("钱B","销售部"),("孙C","市场部"),
             ("李D","研发部"),("周E","研发部"),("吴F","研发部"),
             ("郑G","市场部"),("王H","销售部"),("冯I","财务部"),
             ("陈J","财务部")]
scores = [("赵A",88),("钱B",72),("孙C",80),("李D",92),("周E",78),
          ("吴F",65),("郑G",70),("王H",95),("冯I",82),("陈J",75)]

score_map = {}
for name, s in scores:
    score_map[name] = s

print("1. 员工个人绩效排名（按分数降序）:")
ranked = sorted(scores, key=lambda x: -x[1])
for i in range(len(ranked)):
    name, s = ranked[i]
    print("  %2d. %s: %d" %% (i+1, name, s))

dept_dict = {}
for emp in employees:
    name, dept = emp
    if name in score_map:
        if dept not in dept_dict: dept_dict[dept] = []
        dept_dict[dept].append(score_map[name])

print("")
print("2. 各部门绩效统计（人数/平均分/最高分）:")
dept_summary = []
for dept, vals in dept_dict.items():
    avg = sum(vals) * 1.0 / len(vals)
    best = max(vals)
    dept_summary.append((dept, len(vals), avg, best))
dept_summary.sort(key=lambda x: -x[2])
for d, n, avg, best in dept_summary:
    print("  %s: 人数=%d, 平均分=%.2f, 最高分=%d" %% (d, n, avg, best))

print("")
print("【HR 分析结论】")
print("  - 部门平均分最高的是 %s，建议作为季度优秀团队表彰" %% dept_summary[0][0])
print("  - 分数 < 70 的员工建议安排 1 对 1 辅导与技能培训")
print("  - 建议每季度做一次部门横向对比，识别「高绩效部门可复制做法」")
"""

C5_QUIZ = [
    ("在按部门做绩效统计时，下列哪种结构最适合存「部门 -> 分数列表」？",
     ["一个普通列表", "字典（key=部门, value=分数列表）",
      "一个字符串", "一个布尔变量"], 1,
     "字典天然适合做「分组」统计，key 是部门，value 是该部门的分数列表。"),
    ("合并员工表与绩效表，使用姓名作为匹配键最应注意？",
     ["姓名大小写与去空格一致化", "员工年龄", "员工性别", "员工地址"], 0,
     "姓名/ID 作为匹配键时，必须保证清洗一致，否则会出现无法匹配的情况。"),
    ("想判断一个部门是否「少数人扛多数绩效」，最直观参考？",
     ["部门最高分与部门平均分的差距", "部门总人数", "员工年龄", "员工性别"], 0,
     "如果最高分远高于平均分，说明少数人拉高了整体水平；反之代表分布比较平均。"),
]
C5_SUMMARY = [
    "通过姓名/员工ID 把「员工表」「绩效表」关联起来",
    "使用字典按部门做分组，计算均值与最高分",
    "部门横向对比 + 个人排名，为团队管理提供量化依据",
]


# -------- 课程 6 餐饮营收分析 --------
C6_TAGS = ["餐饮营收", "菜品分析", "分组统计", "经营诊断"]
C6_KNOW = [
    ("1. 菜品销售数据：菜名 + 单价 + 销量",
     "把每笔销售分解为「某菜品 x 数量」，再汇总到菜品维度，即可得到菜品销量与营收排名。"),
    ("2. 时段营收：早中晚三餐分布",
     "按早餐/午餐/晚餐做时段划分，计算各时段营收占比，识别门店真正的「黄金时段」。"),
    ("3. 经营建议：爆款深耕 + 低效时段引流",
     "爆款菜品应保留并放大；低效时段可推出「时段套餐」或外卖促销拉动翻台。"),
]
C6_CODE = """menu = {
    "招牌卤肉饭":28, "宫保鸡丁饭":26, "番茄鸡蛋面":22,
    "酸辣粉":18, "奶茶":12, "柠檬水":8,
}
records = [
    ("午餐","招牌卤肉饭",40),("午餐","宫保鸡丁饭",30),("午餐","番茄鸡蛋面",15),
    ("午餐","奶茶",20),("午餐","柠檬水",25),
    ("晚餐","招牌卤肉饭",35),("晚餐","宫保鸡丁饭",28),("晚餐","酸辣粉",22),
    ("晚餐","奶茶",30),("晚餐","柠檬水",15),
    ("早餐","番茄鸡蛋面",18),("早餐","酸辣粉",10),("早餐","柠檬水",8),
]

print("1. 菜品销量 / 营收 排名:")
dish_sum = {}
for slot, dish, cnt in records:
    if dish in dish_sum: dish_sum[dish] += cnt
    else: dish_sum[dish] = cnt
ranking = sorted(dish_sum.items(), key=lambda x: -x[1])
for dish, cnt in ranking:
    rev = cnt * menu[dish]
    print("  %s 销量=%d 营收=%d 元" %% (dish, cnt, rev))

slot_rev = {}
for slot, dish, cnt in records:
    rev = cnt * menu[dish]
    if slot in slot_rev: slot_rev[slot] += rev
    else: slot_rev[slot] = rev
total_rev = sum(slot_rev.values())

print("")
print("2. 各时段营收分布（总营收 = %d 元）:" %% total_rev)
for slot in ["早餐","午餐","晚餐"]:
    if slot in slot_rev:
        r = slot_rev[slot]
        print("  %s: %d 元 (%.1f%%)" %% (slot, r, r*100.0/total_rev))

print("")
print("3. 爆款菜品（销量 >= 50）:")
for dish, cnt in ranking:
    if cnt >= 50: print("  - %s 销量 %d" %% (dish, cnt))
print("   低效菜品（销量 < 25）:")
for dish, cnt in ranking:
    if cnt < 25: print("  - %s 销量 %d，可考虑替换或下架" %% (dish, cnt))

print("")
print("【经营建议】")
print("  - 午餐/晚餐为黄金时段，建议重点保障热门菜品备料")
print("  - 早餐营收较低，可推出「早餐特价套餐」提高翻台")
print("  - 可考虑把爆款招牌卤肉饭 + 奶茶 组合为套餐主推")
"""

C6_QUIZ = [
    ("判断某菜品是否「爆款」最直接的参考指标是？",
     ["菜名好听", "销量/营收排名靠前", "单价贵", "制作时间长"], 1,
     "爆款应以销量或营收贡献来定义，排名靠前的菜品才是真爆款。"),
    ("想计算「某菜品总营收」，应使用的公式是？",
     ["该菜品销量 + 单价", "该菜品销量 x 单价",
      "该菜品销量 - 单价", "该菜品销量 / 单价"], 1,
     "总营收 = 销量 x 单价。"),
    ("识别门店「黄金时段」最直观的方法是？",
     ["看老板心情", "按时段统计营收，占比最高的时段就是黄金时段",
      "随便猜一个", "看员工排班"], 1,
     "按时段统计营收并对比，是判断黄金时段的标准做法。"),
]
C6_SUMMARY = [
    "先把菜单（单价）与销售记录分开维护，再合并计算",
    "菜品维度看销量/营收排名；时段维度看各时段贡献占比",
    "最终产出：爆款深耕 + 低效时段引流 + 套餐组合设计",
]


# -------- 课程 7 库存销量预测（时间序列）--------
C7_TAGS = ["时间序列", "移动平均", "销量预测", "库存管理"]
C7_KNOW = [
    ("1. 移动平均法：取近 N 期的平均值作为预测",
     "简单移动平均（SMA）是最朴素的时间序列预测方法，取最近 N 期实际销量的均值作为下一期预测值，能平滑短期波动。"),
    ("2. N 的选择：窗口大小决定平滑强度",
     "窗口大（如 5 期）更平滑，适合趋势稳定的商品；窗口小（如 3 期）更灵敏，更贴近近期变化。"),
    ("3. 结合安全库存：预测 + 缓冲",
     "推荐补货量 = 预测销量 + 安全库存 - 当前库存；安全库存通常取预测的 20%%~30%% 作为缓冲。"),
]
C7_CODE = """sales = [120,135,128,160,175,168,195,210]
weeks = ["W1","W2","W3","W4","W5","W6","W7","W8"]

print("1. 最近 %d 周实际销量:" %% len(sales))
for i in range(len(sales)):
    print("  %s: %d" %% (weeks[i], sales[i]))

def sma(values, window):
    if len(values) < window: return None
    recent = values[-window:]
    return sum(recent) * 1.0 / len(recent)

pred3 = sma(sales, 3)
pred5 = sma(sales, 5)
avg_all = sum(sales) * 1.0 / len(sales)

print("")
print("2. 预测结果:")
print("  - 全期均值 = %.2f" %% avg_all)
print("  - 最近 3 期移动平均 = %.2f（更灵敏，适合短期波动商品）" %% pred3)
print("  - 最近 5 期移动平均 = %.2f（更平滑，适合趋势稳定商品）" %% pred5)

current_stock = 180
safe_ratio = 0.25
pred = pred3
safe_stock = int(pred * safe_ratio)
suggest = int(pred + safe_stock - current_stock)

print("")
print("3. 库存与补货建议（以 3 期移动平均为预测值）:")
print("  当前库存: %d" %% current_stock)
print("  下一期预测销量: %.2f" %% pred)
print("  安全库存(25%%): %d" %% safe_stock)
if suggest > 0:
    print("  建议补货量: %d（预测 + 安全 - 当前库存）" %% suggest)
else:
    print("  库存充足，本期不建议补货（过剩 %d）" %% (-suggest))

print("")
print("【趋势判断】")
if pred3 > pred5:
    print("  最近 3 期均值 > 5 期均值，销量在上升，应加大备货")
elif pred3 < pred5:
    print("  最近 3 期均值 < 5 期均值，销量在放缓，建议谨慎补货")
else:
    print("  趋势平稳，按常规水平补货即可")
"""

C7_QUIZ = [
    ("简单移动平均法（SMA）中，窗口越大，预测值会？",
     ["越灵敏，跟随短期波动", "越平滑，短期波动被平均掉",
      "完全等于最大值", "完全等于最小值"], 1,
     "窗口越大，越会把短期波动平均掉，曲线更平滑。"),
    ("下列哪项最符合「安全库存」的含义？",
     ["为防止波动与意外预留的缓冲库存", "仓库里所有货物的总量",
      "最近一周的销量", "历史最高销量"], 0,
     "安全库存是应对需求波动或供给延迟预留的缓冲量，通常取预测的一定比例。"),
    ("如果「最近 3 期移动平均」明显大于「最近 5 期移动平均」，往往意味着？",
     ["销量在下降", "近期销量在上升，趋势向好",
      "销量完全没有变化", "商品即将下架"], 1,
     "短期均值 > 长期均值，往往说明最近在放量上升。"),
]
C7_SUMMARY = [
    "简单移动平均 = 最近 N 期实际值的均值，作为下一期预测",
    "窗口越小越灵敏，窗口越大越平滑，按需选择",
    "预测 + 安全库存 - 当前库存 = 补货建议量",
]


# -------- 课程 8 金融信贷风控 --------
C8_TAGS = ["风控评分", "特征工程", "缺失值", "规则模型"]
C8_KNOW = [
    ("1. 风控数据结构：客户画像 + 行为数据",
     "每位客户抽象为（年龄、月收入、负债、历史逾期次数、近 6 月查询次数）。这些是规则式风控最常用的 5 个基础特征。"),
    ("2. 规则式评分：按维度加权汇总",
     "逾期次数越多得分越低；收入越高、负债越低得分越高；查询次数越频繁得分越低。最终按总分划分为低/中/高三档。"),
    ("3. 缺失值处理：保守填充或单独标记",
     "若某字段缺失，最稳妥的做法是取「对风控较保守」的值（如按高风险方向），或把缺失视为一个单独的风险信号。"),
]
C8_CODE = """clients = [
    ("张三",30,12000,8000,0,2),("李四",45,35000,60000,3,8),
    ("王五",25,6000,12000,1,3),("赵六",55,50000,200000,5,12),
    ("钱七",38,20000,10000,0,1),("孙八",28,9000,-1,2,5),
    ("周九",50,-1,150000,4,10),("吴十",33,15000,25000,0,2),
]

def score_client(age, income, debt, overdue, queries):
    s = 100
    if income == -1: s -= 15
    elif income < 8000: s -= 10
    elif income < 15000: s -= 5
    if debt == -1 or income == -1: s -= 10
    else:
        ratio = debt * 1.0 / income
        if ratio > 8: s -= 20
        elif ratio > 4: s -= 10
    s -= overdue * 8
    if queries >= 10: s -= 15
    elif queries >= 6: s -= 8
    if age <= 22 or age >= 55: s -= 5
    return s

print("1. 各客户评分与风险档:")
print("  %5s %5s %10s %10s %5s %6s  %s" %% ("姓名","年龄","月收入","负债","逾期","查询","风险档"))
result = []
for c in clients:
    name, age, income, debt, overdue, queries = c
    s = score_client(age, income, debt, overdue, queries)
    if s >= 80: level = "低风险"
    elif s >= 60: level = "中风险"
    else: level = "高风险"
    result.append((name, s, level))
    print("  %5s %5d %10s %10s %5d %6d  %s(score=%d)" %% (
        name, age, ("缺失" if income==-1 else str(income)),
        ("缺失" if debt==-1 else str(debt)), overdue, queries, level, s))

print("")
print("2. 各档人数统计:")
for lv in ["低风险","中风险","高风险"]:
    cnt = 0
    for r in result:
        if r[2] == lv: cnt += 1
    print("  - %s: %d 人" %% (lv, cnt))

print("")
print("【高风险客户清单（建议拒绝或降额）】")
for r in result:
    if r[2] == "高风险":
        print("  - %s（评分 %d）：存在明显风险信号，建议人工审核" %% (r[0], r[1]))
"""

C8_QUIZ = [
    ("在风控规则式评分中，「历史逾期次数」通常？",
     ["越多越危险，扣分越多", "越多越安全", "不影响评分", "只影响年龄判断"], 0,
     "历史逾期是强风险信号，次数越多，还款意愿/能力越差。"),
    ("对缺失字段，最简单且保守的处理方式是？",
     ["直接忽略该客户", "按「对风控较保守」的方向填充或单独扣分",
      "随便写一个 0", "写一个很大的数"], 1,
     "缺失值本身就是一个风险信号，常按较保守的方式处理，而不是直接忽略。"),
    ("「负债收入比」越高，通常意味着？",
     ["客户越安全", "客户偿债压力越大，风险越高",
      "客户年龄越大", "客户收入越多"], 1,
     "负债 / 收入 越高，每月还款压力越大，违约风险越高。"),
]
C8_SUMMARY = [
    "把每位客户抽象成「画像 + 行为」的数值特征",
    "规则式评分 = 各特征按风险强度加减分，再按总分划分高/中/低风险",
    "缺失字段要按「较保守」的方向处理，避免低估风险",
]


# -------- 课程 9 用户流失预测 --------
C9_TAGS = ["流失预测", "活跃特征", "用户分层", "增长分析"]
C9_KNOW = [
    ("1. 流失分析三剑客：登录频次 + 沉默天数 + 消费频次",
     "近 30 天登录天数越少、最近一次登录距今越久、消费次数越少 -> 流失风险越高。"),
    ("2. 规则式流失分层：高/中/低风险",
     "用多个阈值组合对用户打标签（如沉默 > 15 天且近 30 天无消费 = 高风险），便于差异化运营。"),
    ("3. 策略匹配：高价值沉默优先挽回",
     "高价值但流失的用户应优先投放资源挽回；低价值但活跃用户应做转化。"),
]
C9_CODE = """users = [
    ("U001",20,1,5,4800),("U002",8,10,1,1200),("U003",2,25,0,150),
    ("U004",28,0,8,12000),("U005",4,18,0,300),("U006",15,3,3,3600),
    ("U007",1,40,0,200),("U008",22,2,6,7800),("U009",6,14,1,800),
    ("U010",30,0,12,18000),
]

def churn_score(login_days, days_since, pay_cnt, total_pay):
    base = 100
    if days_since >= 30: base -= 40
    elif days_since >= 15: base -= 25
    elif days_since >= 7: base -= 10
    if login_days <= 3: base -= 25
    elif login_days <= 7: base -= 15
    elif login_days <= 15: base -= 5
    if pay_cnt == 0: base -= 15
    elif pay_cnt <= 2: base -= 8
    add = min(total_pay / 200, 30)
    return base, base + add

print("1. 每位用户流失评分与风险档:")
stats = {"高流失风险":0,"中流失风险":0,"低流失风险":0}
high_value_lost = []
for u in users:
    name, login, silent, pay, total = u
    s, prio = churn_score(login, silent, pay, total)
    if s <= 50: level = "高流失风险"
    elif s <= 75: level = "中流失风险"
    else: level = "低流失风险"
    stats[level] += 1
    if level == "高流失风险" and total >= 500:
        high_value_lost.append((name, total, prio))
    print("  %s: 登录=%d天, 沉默=%d天, 消费=%d次, 历史=%d元 -> %s(score=%.1f)" %% (
        name, login, silent, pay, total, level, s))

print("")
print("2. 风险档汇总: %s" %% str(stats))
print("")
print("【优先挽回名单（高价值 + 高流失风险）】")
high_value_lost.sort(key=lambda x: -x[2])
for name, total, prio in high_value_lost:
    print("  - %s：历史消费 %d 元，建议推送大额优惠券 + 人工回访" %% (name, total))

print("")
print("【通用运营建议】")
print("  - 高流失风险用户：推送大额券 + 短信/App Push 触达")
print("  - 中流失风险用户：做签到/任务活动，提升登录频次")
print("  - 低流失风险用户：做好会员体系与权益持续释放，稳住活跃")
"""

C9_QUIZ = [
    ("下列哪项特征通常被视为「高流失风险」信号？",
     ["最近一次登录距今很久 + 近 30 天没消费",
      "每天都登录 + 每月都消费", "很年轻", "收入很高"], 0,
     "长时间沉默 + 无消费是最典型的流失信号。"),
    ("流失预测中，为什么要把「历史总消费」考虑进去？",
     ["没有什么用", "判断流失是否「可惜」，用于挽回优先级排序",
      "只看年龄就够了", "只影响注册时间"], 1,
     "高价值用户的流失更可惜，应优先挽回；历史消费高 + 高流失风险 = 重点对象。"),
    ("对中等流失风险用户，最合理的运营动作是？",
     ["直接冻结账号", "做签到/任务类活动提升登录频次与粘性",
      "直接给最大额优惠券", "什么都不做"], 1,
     "中等风险适合用轻触达 + 轻激励提升活跃，避免一开始就过度补贴。"),
]
C9_SUMMARY = [
    "核心流失特征：最近登录距今天数、近 30 天登录天数、近 30 天消费次数",
    "用简单规则给每位用户打分 -> 得到高/中/低流失风险档",
    "高价值但高流失风险用户 -> 优先资源挽回；低风险用户 -> 稳住活跃",
]


# -------- 课程 10 A/B 测试分析 --------
C10_TAGS = ["AB测试", "转化率", "实验分析", "业务决策"]
C10_KNOW = [
    ("1. A/B 测试基础数据：展示数 x 转化数",
     "每个组有「展示数」和「转化数」两项基本数据；转化率 = 转化数 / 展示数。"),
    ("2. 差值与提升率：判断实验组是否优于对照组",
     "提升率 = (实验组转化率 - 对照组转化率) / 对照组转化率。提升率为正且绝对值较大才有业务意义。"),
    ("3. 样本量的直觉判断：每组成千上万比较稳妥",
     "若每组只有几百个样本，波动可能很大，应谨慎。一般经验：每组展示数 >= 1000 且转化数 >= 30，结论更可靠。"),
]
C10_CODE = """experiments = [
    ("A-对照组", 10000, 820),
    ("B-实验组", 10000, 1015),
]

print("1. 各组转化率:")
print("  %%-10s %%-10s %%-10s %%-10s" %% ("组别","展示数","转化数","转化率"))
results = []
for name, show, conv in experiments:
    rate = conv * 100.0 / show
    results.append((name, show, conv, rate))
    print("  %%-10s %%-10d %%-10d %%-10.2f%%" %% (name, show, conv, rate))

name_a, show_a, conv_a, rate_a = results[0]
name_b, show_b, conv_b, rate_b = results[1]
diff_abs = rate_b - rate_a
lift = diff_abs * 100.0 / rate_a

print("")
print("2. 实验组 vs 对照组:")
print("  绝对差值 = %.2f%%（B 比 A）" %% diff_abs)
print("  相对提升率 = %.2f%%" %% lift)

print("")
print("3. 样本量检查:")
sample_ok = True
for name, show, conv, rate in results:
    if show < 1000 or conv < 30:
        print("  - %s：展示数 %d 或转化数 %d 偏小，建议继续实验" %% (name, show, conv))
        sample_ok = False
if sample_ok:
    print("  - 两组样本量均满足基本要求（展示 >= 1000, 转化 >= 30）")

print("")
print("【实验结论与上线建议】")
if diff_abs > 0 and sample_ok:
    print("  - 实验组转化率高于对照组，提升率约 %.2f%%" %% lift)
    print("  - 建议：可先小流量放量验证，再逐步全量上线")
elif diff_abs > 0 and not sample_ok:
    print("  - 实验组看起来更好，但样本量偏小，建议延长实验再决策")
elif diff_abs == 0:
    print("  - 两组完全相同，没有显著差异，可按成本选择")
else:
    print("  - 实验组反而更差，建议不采用该方案，再迭代其他版本")

print("")
print("【数据分析师注意点】")
print("  - 务必确认两组流量分配是否随机")
print("  - 注意同期是否有节假日/促销活动等外部因素干扰")
print("  - 实验上线后仍要监控，关注是否有回退现象")
"""

C10_QUIZ = [
    ("A/B 测试中，转化率的基本公式是？",
     ["展示数 / 转化数", "转化数 / 展示数",
      "展示数 x 转化数", "转化数 - 展示数"], 1,
     "转化率 = 转化数 / 展示数，衡量流量的有效转化比例。"),
    ("「相对提升率（lift）」=？",
     ["(实验组转化率 - 对照组转化率) / 对照组转化率",
      "实验组转化率 + 对照组转化率",
      "实验组转化率 / 2", "对照组转化率 - 实验组转化率"], 0,
     "相对提升率表示实验组相对对照组带来的相对变化幅度。"),
    ("下列哪种情况应谨慎下结论，建议先延长实验再决策？",
     ["每组展示数上万，转化数数百",
      "每组展示数只有几百，转化数几十个",
      "实验组明显优于对照组，且样本量充足", "实验跑了 4 周，数据稳定"], 1,
     "样本量小则波动大，得出的结论可能因随机噪声而失真，应延长实验。"),
]
C10_SUMMARY = [
    "关注三组核心数据：展示数、转化数、转化率",
    "用「差值 + 提升率」衡量实验组是否优于对照组",
    "结论需结合样本量、流量分配随机性、外部因素综合判断",
]


# -------- 添加 10 门课程 --------
add(1, "零售门店客流数据分析", "解析线下门店每日客流、时段分布、节假日差异，输出运营建议",
    "beginner", "初级", "9 小时", "4.8", C1_TAGS,
    "1) 掌握用列表/字典组织门店客流数据\n2) 能按小时、按日期计算客流均值、峰值\n3) 输出可用于门店排班、促销安排的运营建议",
    "零售运营人员、门店店长、商业数据分析师、入门 Python 学习者",
    "Python 基础语法（print / 列表 / 循环 / 条件判断）",
    C1_KNOW, C1_CODE, C1_QUIZ, C1_SUMMARY)

add(2, "电商订单数据异常检测", "识别重复订单、金额异常订单、虚假订单，输出数据治理建议",
    "beginner", "初级", "8 小时", "4.7", C2_TAGS,
    "1) 学会用「均值 + 倍数阈值」识别高异常订单\n2) 掌握用字典统计同一用户的重复下单\n3) 输出简单的数据治理建议",
    "电商运营、订单处理专员、入门数据分析师",
    "Python 基础语法（列表 / 字典 / 循环 / 条件判断）",
    C2_KNOW, C2_CODE, C2_QUIZ, C2_SUMMARY)

add(3, "用户分层与精准营销分析（RFM 模型）", "R/F/M 三维评分、用户分层、差异化营销策略输出",
    "intermediate", "中级", "13 小时", "4.9", C3_TAGS,
    "1) 理解 R（近度）/F（频度）/M（额度）三维定义\n2) 手动实现 1~5 分打分与分层\n3) 针对不同层给出差异化营销策略",
    "电商运营、CRM 专员、增长分析师、市场营销人员",
    "列表与字典熟练使用、循环与条件判断",
    C3_KNOW, C3_CODE, C3_QUIZ, C3_SUMMARY)

add(4, "电商商品关联推荐分析（Apriori 思想）", "购物篮组合统计、高频商品对、关联规则与套餐设计",
    "intermediate", "中级", "14 小时", "4.8", C4_TAGS,
    "1) 理解购物篮分析的基本概念：商品组合、出现频次、支持度\n2) 手动统计两两商品共同出现次数\n3) 输出用于套餐设计的高频商品对",
    "电商商品运营、采购与陈列规划、套餐设计人员",
    "列表与字典、集合运算基础",
    C4_KNOW, C4_CODE, C4_QUIZ, C4_SUMMARY)

add(5, "企业员工绩效数据分析", "多表合并思路、按部门分组统计、绩效排名与部门对比",
    "intermediate", "中级", "11 小时", "4.6", C5_TAGS,
    "1) 用字典做部门分组统计\n2) 计算部门平均分、部门最高分\n3) 输出员工个人排名与部门排名",
    "HR 专员、人力资源数据分析师、业务负责人",
    "列表/字典、循环、简单统计函数",
    C5_KNOW, C5_CODE, C5_QUIZ, C5_SUMMARY)

add(6, "餐饮门店营收数据分析", "菜品销量统计、时段营收、爆款与低效时段识别",
    "intermediate", "中级", "10 小时", "4.7", C6_TAGS,
    "1) 统计各菜品销量与营收排名\n2) 按时段识别高营收/低效时段\n3) 输出菜品结构与时段运营建议",
    "餐饮店长、运营督导、菜单规划人员",
    "列表/字典、循环、排序基础",
    C6_KNOW, C6_CODE, C6_QUIZ, C6_SUMMARY)

add(7, "库存销量预测分析（时间序列）", "简单移动平均法、平滑波动、辅助库存与补货决策",
    "advanced", "高级", "16 小时", "4.9", C7_TAGS,
    "1) 理解简单移动平均法（SMA）的原理\n2) 手动实现 3 期/5 期移动平均\n3) 结合预测值给出库存与补货建议",
    "供应链/库存管理、商品运营、数据分析工程师",
    "列表/循环、基本数值运算",
    C7_KNOW, C7_CODE, C7_QUIZ, C7_SUMMARY)

add(8, "金融信贷风险评估分析", "客户画像、规则式风控、高风险客户识别、缺失值处理",
    "advanced", "高级", "18 小时", "4.8", C8_TAGS,
    "1) 构造客户基本画像：年龄、收入、负债、逾期次数\n2) 基于简单规则给出风险评分与等级\n3) 输出高风险客户清单与授信建议",
    "风控分析师、信贷审批员、金融数据建模人员",
    "列表/字典、条件判断、基本数值运算",
    C8_KNOW, C8_CODE, C8_QUIZ, C8_SUMMARY)

add(9, "平台用户流失预测分析", "活跃特征构建、沉默期统计、流失风险分层与挽回方案",
    "advanced", "高级", "17 小时", "4.7", C9_TAGS,
    "1) 构建核心活跃特征：近 30 天登录天数、最近登录距今天数、近 30 天消费次数\n2) 基于规则输出流失风险等级\n3) 给出各层用户的挽回与运营策略",
    "增长运营、用户运营、CRM/社群运营",
    "列表/字典、循环、条件判断",
    C9_KNOW, C9_CODE, C9_QUIZ, C9_SUMMARY)

add(10, "A/B 测试数据分析", "转化率对比、样本量与显著性思路、实验结论与上线建议",
    "advanced", "高级", "12 小时", "4.8", C10_TAGS,
    "1) 计算 A/B 两组的转化率与差值\n2) 判断样本量是否合理（经验参考）\n3) 输出实验结论与上线/驳回建议",
    "产品经理、增长产品、实验平台数据分析师",
    "列表/字典、百分比运算",
    C10_KNOW, C10_CODE, C10_QUIZ, C10_SUMMARY)


# ======================= HTML 模板 =======================

def course_template(c):
    """生成单门课程的 HTML（返回字符串）"""
    # 折叠展开：知识点 + 选择题 + 参考答案与解析
    knowledge_html = ""
    for idx, (title, body) in enumerate(c["knowledge"]):
        knowledge_html += (
            '<div class="border border-gray-200 rounded-xl overflow-hidden bg-white shadow-sm mb-3">'
            + ('<button onclick="toggle_block(this)" class="w-full flex items-center justify-between px-5 py-4 text-left hover:bg-brand-50 transition bg-white">'
               '<span class="font-semibold text-gray-800 text-base md:text-lg">📖 %s</span>'
               '<span class="text-brand-500 text-xl leading-none chevron-icon">+</span>'
               '</button>')
            + ('<div class="collapsible px-5 pb-5 text-sm md:text-base text-gray-600 leading-relaxed">'
               '<div class="pt-3">%s</div>'
               '</div>') %% (title, body)
            + '</div>'
        )

    quiz_html = ""
    for q_idx, (question, options, answer_idx, explain) in enumerate(c["quiz"]):
        options_html = ""
        for i, opt in enumerate(options):
            correct_class = "opt-correct" if i == answer_idx else "opt-normal"
            options_html += (
                '<label class="quiz-option flex items-start gap-3 cursor-pointer py-3 px-4 rounded-xl border border-gray-200 bg-white hover:bg-brand-50 hover:border-brand-300 transition" data-q="%d" data-i="%d">'
                '<input type="radio" name="q%d" value="%d" class="mt-1">'
                '<div class="flex-1"><span class="font-semibold text-gray-800 mr-2">%s.</span><span class="text-gray-700">%s</span></div>'
                '<span class="quiz-result-tag text-xs font-semibold hidden rounded-full px-3 py-1"></span>'
                '</label>') %% (q_idx, i, q_idx, i, "ABCD"[i], opt)
        quiz_html += (
            '<div class="bg-white rounded-2xl border border-gray-200 p-5 shadow-sm mb-4">'
            '<div class="font-bold text-gray-900 text-base mb-4">Q%d. %s</div>'
            '<div class="flex flex-col gap-2">%s</div>'
            '<div class="flex items-center gap-2 mt-4 flex-wrap">'
            '<button class="btn-submit-quiz bg-brand-500 hover:bg-brand-600 text-white text-sm font-semibold px-5 py-2 rounded-lg shadow-sm" data-q="%d">✓ 提交答案</button>'
            '<button class="btn-reset-quiz bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-semibold px-5 py-2 rounded-lg" data-q="%d">重置</button>'
            '<span class="quiz-explain text-sm text-gray-500 italic hidden ml-2">💡 %s</span>'
            '</div>'
            '</div>'
        ) %% (q_idx + 1, question, options_html, q_idx, q_idx, explain)

    summary_bullets = ""
    for line in c["summary"]:
        summary_bullets += '<li class="text-sm md:text-base text-gray-700 leading-relaxed mb-2">%s</li>' %% line
    tags_html = "".join(['<span class="inline-block bg-brand-50 text-brand-700 text-xs md:text-sm rounded-full px-3 py-1 mr-2 mb-2 border border-brand-100">%s</span>' %% t for t in c["tags"]])
    goals_html = c["goals"].replace("\n", "<br/>")

    # 难度颜色
    if c["level"] == "beginner":
        level_color = "text-green-700 bg-green-50 border-green-200"
    elif c["level"] == "intermediate":
        level_color = "text-brand-700 bg-brand-50 border-brand-200"
    else:
        level_color = "text-violet-700 bg-violet-50 border-violet-200"

    # 代码内容做转义（避免直接被浏览器解析）
    code_text = c["code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>%s | DataLearn Python 数据分析实战平台</title>
<script src="https://cdn.jsdelivr.net/npm/skulpt@1.3.0/dist/skulpt.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/skulpt@1.3.0/dist/skulpt-stdlib.js"></script>
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    theme: { extend: {
      colors: { brand: { 50:'#EEF4FF', 100:'#DBE8FF', 200:'#B8D1FF', 500:'#165DFF', 600:'#0E4BDB', 700:'#0A39A8' } }
    }}
  }
</script>
<style>
body { font-family: "PingFang SC","Microsoft YaHei",sans-serif; background: #F5F7FA; }
.hover-lift { transition: transform .25s ease, box-shadow .25s ease; }
.hover-lift:hover { transform: translateY(-3px); box-shadow: 0 12px 30px rgba(22,93,255,.15); }
.code-editor {
  background:#1E293B; color:#E2E8F0; font-family:Consolas,Monaco,Menlo,monospace;
  font-size: 13px; line-height: 1.7; border-radius: 12px; padding: 14px 16px;
  border: 1px solid #0F172A; width: 100%%; min-height: 320px; box-shadow: inset 0 2px 6px rgba(0,0,0,.3);
}
.code-editor:focus { outline: 2px solid #165DFF; outline-offset: -1px; }
.output-area {
  background:#0F172A; color:#E2E8F0; font-family:Consolas,Monaco,Menlo,monospace;
  font-size: 13px; line-height: 1.7; border-radius: 12px; padding: 14px 16px;
  min-height: 320px; white-space: pre-wrap; word-break: break-all; overflow: auto;
  border: 1px solid #0F172A;
}
.output-area .err-line { color:#FCA5A5; display:block; }
.output-area .ok-line { color:#A7F3D0; }
.btn-primary { background:#165DFF; color:white; }
.btn-primary:hover { background:#0E4BDB; box-shadow: 0 6px 14px rgba(14,75,219,.3); }
.collapsible { max-height: 0; overflow: hidden; transition: max-height .35s ease, padding .2s ease; padding-top:0; padding-bottom:0; }
.collapsible.open { max-height: 3000px; padding-top: 8px; padding-bottom: 8px; }
.chevron-icon.rotate { transform: rotate(45deg); }
.chevron-icon { transition: transform .25s ease; }
.quiz-option.correct { background:#ECFDF5; border-color:#10B981; color:#065F46; }
.quiz-option.wrong { background:#FEF2F2; border-color:#EF4444; color:#991B1B; }
.quiz-result-tag.show { display: inline-block; }
.quiz-result-tag.ok { background:#10B981; color:white; }
.quiz-result-tag.bad { background:#EF4444; color:white; }
.loader {
  display:inline-block; width:14px; height:14px; border:2px solid rgba(255,255,255,.5);
  border-top-color:white; border-radius:50%%; animation: spin .7s linear infinite; vertical-align:middle; margin-right:6px;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
</head>
<body class="antialiased">

<nav class="bg-white border-b border-gray-100 sticky top-0 z-40">
  <div class="max-w-6xl mx-auto px-4 md:px-6 py-3 flex items-center justify-between">
    <a href="index.html" class="flex items-center gap-2 font-bold text-brand-500">
      <span class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-brand-500 text-white text-sm">D</span>
      DataLearn
    </a>
    <div class="hidden md:flex items-center gap-6 text-sm text-gray-600">
      <a href="index.html" class="hover:text-brand-500 transition">首页</a>
      <a href="index.html#courses" class="hover:text-brand-500 transition">全部课程</a>
      <a href="index.html#path" class="hover:text-brand-500 transition">学习路径</a>
    </div>
    <a href="index.html" class="text-sm bg-brand-500 hover:bg-brand-600 text-white px-4 py-2 rounded-lg font-semibold inline-flex items-center gap-1">&larr; 返回首页</a>
  </div>
</nav>

<header class="bg-gradient-to-br from-brand-600 via-brand-500 to-brand-700 text-white">
  <div class="max-w-6xl mx-auto px-4 md:px-6 py-10 md:py-14">
    <div class="flex flex-wrap items-center gap-3 mb-4">
      <span class="text-xs font-semibold bg-white/20 border border-white/30 text-white px-3 py-1 rounded-full">课程 %02d / 10</span>
      <span class="text-xs font-semibold px-3 py-1 rounded-full border %s">%s</span>
      <span class="text-xs text-brand-50/80">⏱ %s · ★ %s</span>
    </div>
    <h1 class="text-2xl md:text-4xl font-extrabold leading-tight">%s</h1>
    <p class="mt-3 text-brand-50/90 text-sm md:text-base max-w-3xl leading-relaxed">%s</p>
    <div class="grid md:grid-cols-3 gap-4 mt-6">
      <div class="bg-white/10 backdrop-blur rounded-xl p-4 border border-white/15">
        <div class="text-xs text-brand-100 mb-1 font-semibold">🎯 学习目标</div>
        <div class="text-sm leading-6">%s</div>
      </div>
      <div class="bg-white/10 backdrop-blur rounded-xl p-4 border border-white/15">
        <div class="text-xs text-brand-100 mb-1 font-semibold">👥 适合人群</div>
        <div class="text-sm leading-6">%s</div>
      </div>
      <div class="bg-white/10 backdrop-blur rounded-xl p-4 border border-white/15">
        <div class="text-xs text-brand-100 mb-1 font-semibold">📖 前置知识</div>
        <div class="text-sm leading-6">%s</div>
      </div>
    </div>
    <div class="flex flex-wrap gap-2 mt-5">%s</div>
  </div>
</header>

<main class="max-w-6xl mx-auto px-4 md:px-6 pb-16 space-y-10">

<section>
  <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-5">📖 课程核心知识点</h2>
  %s
</section>

<section>
  <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-5">💻 在线代码练习</h2>
  <p class="text-sm md:text-base text-gray-500 mb-4 leading-relaxed">在下方编辑器中直接修改、运行代码，结果会实时显示在右侧（或下方）输出区。可随时点击重置，恢复示例代码。</p>

  <div class="grid md:grid-cols-2 gap-4">
    <div>
      <div class="flex items-center justify-between mb-2">
        <span class="text-sm font-semibold text-gray-700">📝 代码编辑器</span>
      </div>
      <textarea id="code-editor" class="code-editor" spellcheck="false">%s</textarea>
    </div>
    <div>
      <div class="flex items-center justify-between mb-2">
        <span class="text-sm font-semibold text-gray-700">📤 运行结果</span>
        <span id="run-status" class="text-xs text-gray-500">点击左侧「运行代码」开始</span>
      </div>
      <pre id="output-area" class="output-area">（输出将显示在这里）</pre>
    </div>
  </div>

  <div class="flex flex-wrap gap-3 mt-4">
    <button id="btn-run" class="btn-primary px-6 py-2.5 rounded-xl text-sm font-semibold shadow-sm inline-flex items-center gap-2">▶ 运行代码</button>
    <button id="btn-reset" class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-2.5 rounded-xl text-sm font-semibold">↻ 重置代码</button>
    <button id="btn-copy" class="bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 px-6 py-2.5 rounded-xl text-sm font-semibold">📋 复制代码</button>
  </div>
</section>

<section>
  <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-5">📝 课程小测（单选题）</h2>
  <p class="text-sm md:text-base text-gray-500 mb-4 leading-relaxed">选择后点击「提交答案」，系统会即时标注正误，并给出详细解析。</p>
  <form id="quiz-form" onsubmit="return false;">%s</form>
  <div id="quiz-total" class="text-center mt-5 text-gray-700 font-semibold"></div>
</section>

<section>
  <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-5">📌 学习总结</h2>
  <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
    <ul class="list-disc pl-5">%s</ul>
  </div>
</section>

<section>
  <div class="bg-gradient-to-br from-brand-50 via-white to-brand-50 rounded-3xl p-8 md:p-10 text-center border border-brand-100">
    <div class="text-2xl md:text-3xl font-extrabold text-brand-700 mb-3">继续学习下一门课程</div>
    <p class="text-sm md:text-base text-gray-600 mb-6">系统化、实战化，从基础到高阶建模，助你成为数据驱动的商务决策专家。</p>
    <a href="index.html#courses" class="btn-primary inline-flex items-center gap-2 px-7 py-3 rounded-xl font-semibold">📚 查看全部课程</a>
  </div>
</section>

</main>

<footer class="bg-white border-t border-gray-100">
  <div class="max-w-6xl mx-auto px-6 py-6 text-center text-xs text-gray-400">
    &copy; 2026 DataLearn · 商务数据分析与应用 Python 学习平台 · 浏览器内直接运行 Python
  </div>
</footer>

<script>
(function(){
  const DEFAULT_CODE = document.getElementById('code-editor').value;
  const OUT = document.getElementById('output-area');
  const STATUS = document.getElementById('run-status');
  const btnRun = document.getElementById('btn-run');
  const btnReset = document.getElementById('btn-reset');
  const btnCopy = document.getElementById('btn-copy');

  function builtinRead(x){
    if(Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
      throw "File not found: " + x;
    return Sk.builtinFiles["files"][x];
  }

  function runIt(){
    const code = document.getElementById('code-editor').value;
    OUT.textContent = '';
    STATUS.textContent = '运行中，请稍候…';
    btnRun.disabled = true;
    const originalHtml = btnRun.innerHTML;
    btnRun.innerHTML = '<span class="loader"></span>运行中…';
    try{
      Sk.configure({ output: function(text){ OUT.textContent += text; }, read: builtinRead, __future__: Sk.python3 });
      const myPromise = Sk.misceval.asyncToPromise(function(){ return Sk.importMainWithBody("<stdin>", false, code, true); });
      myPromise.then(function(){
        OUT.innerHTML = '<span class="ok-line">[运行成功] 代码执行完成 ✅</span>\\n' + escape_html(OUT.textContent);
        STATUS.textContent = '运行完成，耗时 ' + '较短（Skulpt 本地执行，零网络依赖）';
        btnRun.disabled = false;
        btnRun.innerHTML = originalHtml;
      }, function(err){
        OUT.innerHTML = '<span class="err-line">[运行失败] ' + escape_html(err.toString()) + '</span>';
        STATUS.textContent = '运行出错，请检查代码';
        btnRun.disabled = false;
        btnRun.innerHTML = originalHtml;
      });
    }catch(err){
      OUT.innerHTML = '<span class="err-line">[运行失败] ' + escape_html(err.toString()) + '</span>';
      STATUS.textContent = '运行出错';
      btnRun.disabled = false;
      btnRun.innerHTML = originalHtml;
    }
  }
  function escape_html(s){ return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }

  btnRun.addEventListener('click', runIt);
  btnReset.addEventListener('click', function(){
    if(confirm("确定要恢复为默认示例代码吗？当前编辑的内容将丢失。")){
      document.getElementById('code-editor').value = DEFAULT_CODE;
      OUT.textContent = '（代码已重置，点击运行代码查看结果）';
      STATUS.textContent = '已恢复默认示例代码';
    }
  });
  btnCopy.addEventListener('click', function(){
    const txt = document.getElementById('code-editor').value;
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(txt).then(function(){
        STATUS.textContent = '已复制到剪贴板';
      });
    }else{
      // 兼容老浏览器
      var ta = document.createElement('textarea');
      ta.value = txt; document.body.appendChild(ta); ta.select();
      try{ document.execCommand('copy'); STATUS.textContent = '已复制到剪贴板'; }catch(e){ STATUS.textContent = '复制失败，请手动选择'; }
      document.body.removeChild(ta);
    }
  });

  // 折叠展开切换
  window.toggle_block = function(btn){
    const coll = btn.parentElement.querySelector('.collapsible');
    const che = btn.querySelector('.chevron-icon');
    if(coll){ coll.classList.toggle('open'); }
    if(che){ che.classList.toggle('rotate'); }
  };

  // 选择题交互
  const TOTAL_QUESTIONS = document.querySelectorAll('#quiz-form > div').length;
  const quizSolved = new Array(TOTAL_QUESTIONS).fill(false);
  const quizCorrect = new Array(TOTAL_QUESTIONS).fill(false);
  document.querySelectorAll('.btn-submit-quiz').forEach(function(btn){
    btn.addEventListener('click', function(){
      const qIdx = parseInt(btn.getAttribute('data-q'), 10);
      const container = btn.closest('section > div > div') || btn.closest('div').parentElement.parentElement;
      // 找到包含该题的父容器
      const block = btn.closest('section').querySelectorAll('.quiz-option');
      // 通过 data-q 过滤
      let chosen = null;
      document.querySelectorAll('.quiz-option[data-q="'+qIdx+'"]').forEach(function(opt){
        const input = opt.querySelector('input');
        if(input && input.checked){ chosen = parseInt(opt.getAttribute('data-i'),10); }
        opt.classList.remove('correct','wrong');
        const tag = opt.querySelector('.quiz-result-tag');
        if(tag){ tag.classList.remove('show','ok','bad'); tag.textContent = ''; }
      });
      const explainEl = document.querySelectorAll('#quiz-form .quiz-explain')[qIdx];
      if(chosen === null){
        if(explainEl){ explainEl.textContent = '⚠ 请先选择一个答案再提交'; explainEl.classList.remove('hidden'); }
        return;
      }
      // 找出正确答案索引（在代码生成脚本中，第 qIdx 题的正确答案索引：题目 HTML 中带 correct_class=opt-correct 的那个 options 的下标）
      // 这里我们从 DOM 读取：第 qIdx 组里 correct_class 的是哪个 i
      let correctIdx = 0;
      document.querySelectorAll('.quiz-option[data-q="'+qIdx+'"]').forEach(function(opt, i){
        // 恢复默认样式已经去除 correct/wrong class 了
        // 再逐个添加样式
      });
      // 通过 original 样式判断：我们在 HTML 里通过 correct_class="opt-correct" 作为标记
      // 遍历找标记
      document.querySelectorAll('#quiz-form > div')[qIdx].querySelectorAll('.quiz-option').forEach(function(opt, i){
        // 读取 data-i
        const iVal = parseInt(opt.getAttribute('data-i'),10);
        if(opt.getAttribute('data-correct') === '1'){ correctIdx = iVal; }
      });
      // 由于我们实际渲染时没有输出 data-correct，这里重新从标准答案读取；
      // 为了避免在 JS 里写标准答案（被同学直接看到），我们用一个隐含的 DOM 元素做标记：
      // 渲染时，把正确选项渲染为带 hidden 标记，放在题容器的 dataset 里。
      const qBlock = document.querySelectorAll('#quiz-form > div')[qIdx];
      const correctFromBlock = parseInt(qBlock.getAttribute('data-correct'), 10);
      correctIdx = isNaN(correctFromBlock) ? 0 : correctFromBlock;

      // 标注选项
      let chosenOk = (chosen === correctIdx);
      document.querySelectorAll('.quiz-option[data-q="'+qIdx+'"]').forEach(function(opt){
        const iVal = parseInt(opt.getAttribute('data-i'),10);
        const tag = opt.querySelector('.quiz-result-tag');
        if(iVal === correctIdx){
          opt.classList.add('correct');
          if(tag){ tag.textContent = '✓ 正确答案'; tag.classList.add('show','ok'); }
        }else if(iVal === chosen){
          opt.classList.add('wrong');
          if(tag){ tag.textContent = '✗ 你的选择'; tag.classList.add('show','bad'); }
        }
      });
      quizSolved[qIdx] = true;
      quizCorrect[qIdx] = chosenOk;
      if(explainEl){ explainEl.classList.remove('hidden'); }
      updateQuizTotal();
    });
  });
  document.querySelectorAll('.btn-reset-quiz').forEach(function(btn){
    btn.addEventListener('click', function(){
      const qIdx = parseInt(btn.getAttribute('data-q'), 10);
      document.querySelectorAll('.quiz-option[data-q="'+qIdx+'"]').forEach(function(opt){
        opt.classList.remove('correct','wrong');
        const input = opt.querySelector('input');
        if(input) input.checked = false;
        const tag = opt.querySelector('.quiz-result-tag');
        if(tag){ tag.classList.remove('show','ok','bad'); tag.textContent = ''; }
      });
      const ex = document.querySelectorAll('#quiz-form .quiz-explain')[qIdx];
      if(ex) ex.classList.add('hidden');
      quizSolved[qIdx] = false; quizCorrect[qIdx] = false;
      updateQuizTotal();
    });
  });
  function updateQuizTotal(){
    const total = document.getElementById('quiz-total');
    if(!total) return;
    let solvedCount = 0, correctCount = 0;
    for(let i=0;i<quizSolved.length;i++){ if(quizSolved[i]){ solvedCount++; if(quizCorrect[i]) correctCount++; } }
    if(solvedCount === 0){ total.textContent = ''; return; }
    let msg = '你已作答 ' + solvedCount + ' / ' + quizSolved.length + ' 题，答对 ' + correctCount + ' 题。';
    if(solvedCount === quizSolved.length){
      if(correctCount === quizSolved.length) msg += ' 🎉 全部答对，知识点掌握良好！';
      else if(correctCount >= 2) msg += ' 👍 不错，建议再看一遍解析巩固。';
      else msg += ' 📚 建议回头复习知识点部分。';
    }
    total.textContent = msg;
  }
})();
</script>
</body>
</html>
""" %% {
    "idx": c["idx"],
    "title": c["title"],
    "subtitle": c["subtitle"],
    "level_text": c["level_text"],
    "level_color": level_color,
    "hours": c["hours"],
    "rating": c["rating"],
    "tags_html": tags_html,
    "goals": goals_html,
    "audience": c["audience"],
    "prereq": c["prereq"],
    "knowledge_html": knowledge_html,
    "code_text": code_text,
    "quiz_html": quiz_html,
    "summary_bullets": summary_bullets,
}
    return html


def build_quiz_html_with_correct_marker(c):
    """在 build 后的 quiz_html 中，为每道题的容器设置 data-correct（正确选项索引）。
    这里我们重新生成 quiz_html，使每个题的 div 带有 data-correct 属性，便于 JS 读取。
    """
    quiz_html = ""
    for q_idx, (question, options, answer_idx, explain) in enumerate(c["quiz"]):
        options_html = ""
        for i, opt in enumerate(options):
            correct_class = "opt-correct" if i == answer_idx else "opt-normal"
            options_html += (
                '<label class="quiz-option flex items-start gap-3 cursor-pointer py-3 px-4 rounded-xl border border-gray-200 bg-white hover:bg-brand-50 hover:border-brand-300 transition" data-q="%d" data-i="%d">'
                '<input type="radio" name="q%d" value="%d" class="mt-1 mr-3">'
                '<div class="flex-1"><span class="font-semibold text-gray-800 mr-2">%s.</span><span class="text-gray-700">%s</span></div>'
                '<span class="quiz-result-tag text-xs font-semibold hidden rounded-full px-3 py-1"></span>'
                '</label>') %% (q_idx, i, q_idx, i, "ABCD"[i], opt)
        quiz_html += (
            '<div class="bg-white rounded-2xl border border-gray-200 p-5 shadow-sm mb-4" data-correct="%d">'
            '<div class="font-bold text-gray-900 text-base mb-4">Q%d. %s</div>'
            '<div class="flex flex-col gap-2">%s</div>'
            '<div class="flex items-center gap-2 mt-4 flex-wrap">'
            '<button class="btn-submit-quiz bg-brand-500 hover:bg-brand-600 text-white text-sm font-semibold px-5 py-2 rounded-lg shadow-sm" data-q="%d">✓ 提交答案</button>'
            '<button class="btn-reset-quiz bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-semibold px-5 py-2 rounded-lg" data-q="%d">重置</button>'
            '<span class="quiz-explain text-sm text-gray-500 italic hidden ml-2">💡 %s</span>'
            '</div>'
            '</div>'
        ) %% (answer_idx, q_idx + 1, question, options_html, q_idx, q_idx, explain)
    return quiz_html


# ======================= 主流程 =======================

def main():
    os.makedirs(OUT, exist_ok=True)
    for c in COURSES_META:
        # 用带正确答案标记的 quiz_html 覆盖默认实现
        quiz_html = build_quiz_html_with_correct_marker(c)

        # 与上面模板相同的逻辑，但 quiz_html 从外部注入
        level_color_map = {
            "beginner": "text-green-700 bg-green-50 border-green-200",
            "intermediate": "text-brand-700 bg-brand-50 border-brand-200",
            "advanced": "text-violet-700 bg-violet-50 border-violet-200",
        }
        level_color = level_color_map[c["level"]]
        tags_html = "".join(['<span class="inline-block bg-brand-50 text-brand-700 text-xs md:text-sm rounded-full px-3 py-1 mr-2 mb-2 border border-brand-100">%s</span>' %% t for t in c["tags"]])
        goals_html = c["goals"].replace("\n", "<br/>")
        code_text = c["code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

        knowledge_html = ""
        for idx, (title, body) in enumerate(c["knowledge"]):
            knowledge_html += (
                '<div class="border border-gray-200 rounded-xl overflow-hidden bg-white shadow-sm mb-3">'
                '<button onclick="toggle_block(this)" class="w-full flex items-center justify-between px-5 py-4 text-left hover:bg-brand-50 transition bg-white">'
                '<span class="font-semibold text-gray-800 text-base md:text-lg">📖 %s</span>'
                '<span class="text-brand-500 text-xl leading-none chevron-icon">+</span>'
                '</button>'
                '<div class="collapsible px-5 py-0 text-sm md:text-base text-gray-600 leading-relaxed">'
                '<div class="pt-2 pb-3">%s</div>'
                '</div>'
                '</div>'
            ) %% (title, body)

        summary_bullets = ""
        for line in c["summary"]:
            summary_bullets += '<li class="text-sm md:text-base text-gray-700 leading-relaxed mb-2">%s</li>' %% line

        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>%s | DataLearn</title>
<script src="https://cdn.jsdelivr.net/npm/skulpt@1.3.0/dist/skulpt.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/skulpt@1.3.0/dist/skulpt-stdlib.js"></script>
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = { theme: { extend: {
    colors: { brand: { 50:'#EEF4FF',100:'#DBE8FF',200:'#B8D1FF',500:'#165DFF',600:'#0E4BDB',700:'#0A39A8' } }
  }}}
</script>
<style>
body { font-family:"PingFang SC","Microsoft YaHei",sans-serif; background:#F5F7FA; }
.hover-lift { transition: transform .25s ease, box-shadow .25s ease; }
.hover-lift:hover { transform: translateY(-3px); box-shadow: 0 12px 30px rgba(22,93,255,.15); }
.code-editor {
  background:#1E293B; color:#E2E8F0; font-family:Consolas,Monaco,Menlo,monospace;
  font-size: 13px; line-height: 1.7; border-radius: 12px; padding: 14px 16px;
  border: 1px solid #0F172A; width: 100%%; min-height: 320px; box-shadow: inset 0 2px 6px rgba(0,0,0,.3);
}
.code-editor:focus { outline: 2px solid #165DFF; outline-offset: -1px; }
.output-area {
  background:#0F172A; color:#E2E8F0; font-family:Consolas,Monaco,Menlo,monospace;
  font-size: 13px; line-height: 1.7; border-radius: 12px; padding: 14px 16px;
  min-height: 320px; white-space: pre-wrap; word-break: break-all; overflow: auto;
  border: 1px solid #0F172A;
}
.output-area .ok-line { color:#A7F3D0; }
.output-area .err-line { color:#FCA5A5; }
.collapsible { max-height: 0; overflow: hidden; transition: max-height .4s ease, padding .25s ease; padding-top:0; padding-bottom:0; }
.collapsible.open { max-height: 3000px; padding-top: 6px; padding-bottom: 14px; }
.chevron-icon { transition: transform .25s ease; }
.chevron-icon.rotate { transform: rotate(45deg); }
.quiz-option.correct { background:#ECFDF5; border-color:#10B981; color:#065F46; }
.quiz-option.wrong { background:#FEF2F2; border-color:#EF4444; color:#991B1B; }
.quiz-result-tag.show { display:inline-block; }
.quiz-result-tag.ok { background:#10B981; color:white; }
.quiz-result-tag.bad { background:#EF4444; color:white; }
.loader { display:inline-block; width:14px; height:14px; border:2px solid rgba(255,255,255,.45); border-top-color:white; border-radius:50%%; animation: spin .7s linear infinite; vertical-align:middle; margin-right:6px; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
</head>
<body class="antialiased">
<nav class="bg-white border-b border-gray-100 sticky top-0 z-40">
  <div class="max-w-6xl mx-auto px-4 md:px-6 py-3 flex items-center justify-between">
    <a href="index.html" class="flex items-center gap-2 font-bold text-brand-500">
      <span class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-brand-500 text-white text-sm">D</span>DataLearn
    </a>
    <div class="hidden md:flex items-center gap-6 text-sm text-gray-600">
      <a href="index.html" class="hover:text-brand-500 transition">首页</a>
      <a href="index.html#courses" class="hover:text-brand-500 transition">全部课程</a>
      <a href="index.html#path" class="hover:text-brand-500 transition">学习路径</a>
    </div>
    <a href="index.html" class="text-sm bg-brand-500 hover:bg-brand-600 text-white px-4 py-2 rounded-lg font-semibold inline-flex items-center gap-1">&larr; 返回首页</a>
  </div>
</nav>

<header class="bg-gradient-to-br from-brand-600 via-brand-500 to-brand-700 text-white">
  <div class="max-w-6xl mx-auto px-4 md:px-6 py-10 md:py-14">
    <div class="flex flex-wrap items-center gap-3 mb-4">
      <span class="text-xs font-semibold bg-white/20 border border-white/30 text-white px-3 py-1 rounded-full">课程 %02d / 10</span>
      <span class="text-xs font-semibold px-3 py-1 rounded-full border %s">%s</span>
      <span class="text-xs text-brand-50/80">⏱ %s · ★ %s</span>
    </div>
    <h1 class="text-2xl md:text-4xl font-extrabold leading-tight">%s</h1>
    <p class="mt-3 text-brand-50/90 text-sm md:text-base max-w-3xl leading-relaxed">%s</p>
    <div class="grid md:grid-cols-3 gap-4 mt-6">
      <div class="bg-white/10 backdrop-blur rounded-xl p-4 border border-white/15">
        <div class="text-xs text-brand-100 mb-1 font-semibold">🎯 学习目标</div>
        <div class="text-sm leading-6">%s</div>
      </div>
      <div class="bg-white/10 backdrop-blur rounded-xl p-4 border border-white/15">
        <div class="text-xs text-brand-100 mb-1 font-semibold">👥 适合人群</div>
        <div class="text-sm leading-6">%s</div>
      </div>
      <div class="bg-white/10 backdrop-blur rounded-xl p-4 border border-white/15">
        <div class="text-xs text-brand-100 mb-1 font-semibold">📖 前置知识</div>
        <div class="text-sm leading-6">%s</div>
      </div>
    </div>
    <div class="flex flex-wrap gap-2 mt-5">%s</div>
  </div>
</header>

<main class="max-w-6xl mx-auto px-4 md:px-6 pb-16 space-y-10">
<section>
  <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-5">📖 课程核心知识点</h2>
  %s
</section>

<section>
  <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-5">💻 在线代码练习</h2>
  <p class="text-sm md:text-base text-gray-500 mb-4 leading-relaxed">在下方编辑器中直接修改、运行代码，结果会实时显示在输出区。可随时点击重置，恢复示例代码。使用浏览器内的 Skulpt Python 解释器，无需安装环境。</p>
  <div class="grid md:grid-cols-2 gap-4">
    <div>
      <div class="flex items-center justify-between mb-2"><span class="text-sm font-semibold text-gray-700">📝 代码编辑器</span></div>
      <textarea id="code-editor" class="code-editor" spellcheck="false">%s</textarea>
    </div>
    <div>
      <div class="flex items-center justify-between mb-2">
        <span class="text-sm font-semibold text-gray-700">📤 运行结果</span>
        <span id="run-status" class="text-xs text-gray-500">点击「运行代码」开始</span>
      </div>
      <pre id="output-area" class="output-area">（输出将显示在这里）</pre>
    </div>
  </div>
  <div class="flex flex-wrap gap-3 mt-4">
    <button id="btn-run" class="bg-brand-500 hover:bg-brand-600 text-white px-6 py-2.5 rounded-xl text-sm font-semibold shadow-sm inline-flex items-center gap-2">▶ 运行代码</button>
    <button id="btn-reset" class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-2.5 rounded-xl text-sm font-semibold">↻ 重置代码</button>
    <button id="btn-copy" class="bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 px-6 py-2.5 rounded-xl text-sm font-semibold">📋 复制代码</button>
  </div>
</section>

<section>
  <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-5">📝 课程小测（单选题）</h2>
  <p class="text-sm md:text-base text-gray-500 mb-4 leading-relaxed">选择后点击「提交答案」，系统会即时标注正误，并给出详细解析。</p>
  <form id="quiz-form" onsubmit="return false;">%s</form>
  <div id="quiz-total" class="text-center mt-5 text-gray-700 font-semibold"></div>
</section>

<section>
  <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-5">📌 学习总结</h2>
  <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
    <ul class="list-disc pl-5">%s</ul>
  </div>
</section>

<section>
  <div class="bg-gradient-to-br from-brand-50 via-white to-brand-50 rounded-3xl p-8 md:p-10 text-center border border-brand-100">
    <div class="text-2xl md:text-3xl font-extrabold text-brand-700 mb-3">继续学习下一门课程</div>
    <p class="text-sm md:text-base text-gray-600 mb-6">系统化、实战化，从基础到高阶建模，助你成为数据驱动的商务决策专家。</p>
    <a href="index.html#courses" class="bg-brand-500 hover:bg-brand-600 text-white inline-flex items-center gap-2 px-7 py-3 rounded-xl font-semibold shadow-sm">📚 查看全部课程</a>
  </div>
</section>
</main>

<footer class="bg-white border-t border-gray-100">
  <div class="max-w-6xl mx-auto px-6 py-6 text-center text-xs text-gray-400">
    &copy; 2026 DataLearn · 商务数据分析与应用 Python 学习平台 · 浏览器内直接运行 Python
  </div>
</footer>

<script>
(function(){
  const DEFAULT_CODE = document.getElementById('code-editor').value;
  const OUT = document.getElementById('output-area');
  const STATUS = document.getElementById('run-status');
  const btnRun = document.getElementById('btn-run');
  const btnReset = document.getElementById('btn-reset');
  const btnCopy = document.getElementById('btn-copy');

  function builtinRead(x){
    if(Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
      throw "File not found: " + x;
    return Sk.builtinFiles["files"][x];
  }

  function runIt(){
    const code = document.getElementById('code-editor').value;
    OUT.textContent = '';
    STATUS.textContent = '运行中，请稍候…';
    btnRun.disabled = true;
    const originalHtml = btnRun.innerHTML;
    btnRun.innerHTML = '<span class="loader"></span>运行中…';
    try{
      Sk.configure({ output: function(text){ OUT.textContent += text; }, read: builtinRead, __future__: Sk.python3 });
      const myPromise = Sk.misceval.asyncToPromise(function(){ return Sk.importMainWithBody("<stdin>", false, code, true); });
      myPromise.then(function(){
        OUT.innerHTML = '<span class="ok-line">[运行成功] 代码执行完成 ✅</span>\\n' + escape_html(OUT.textContent);
        STATUS.textContent = '运行完成（本地 Skulpt 解释，零网络依赖）';
        btnRun.disabled = false; btnRun.innerHTML = originalHtml;
      }, function(err){
        OUT.innerHTML = '<span class="err-line">[运行失败] ' + escape_html(err.toString()) + '</span>';
        STATUS.textContent = '运行出错，请检查代码';
        btnRun.disabled = false; btnRun.innerHTML = originalHtml;
      });
    }catch(err){
      OUT.innerHTML = '<span class="err-line">[运行失败] ' + escape_html(err.toString()) + '</span>';
      STATUS.textContent = '运行出错';
      btnRun.disabled = false; btnRun.innerHTML = originalHtml;
    }
  }
  function escape_html(s){ return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }

  btnRun.addEventListener('click', runIt);
  btnReset.addEventListener('click', function(){
    if(confirm("确定要恢复为默认示例代码吗？当前编辑的内容将丢失。")){
      document.getElementById('code-editor').value = DEFAULT_CODE;
      OUT.textContent = '（代码已重置，点击运行代码查看结果）';
      STATUS.textContent = '已恢复默认示例代码';
    }
  });
  btnCopy.addEventListener('click', function(){
    const txt = document.getElementById('code-editor').value;
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(txt).then(function(){ STATUS.textContent = '已复制到剪贴板'; });
    }else{
      var ta = document.createElement('textarea'); ta.value = txt; document.body.appendChild(ta); ta.select();
      try{ document.execCommand('copy'); STATUS.textContent = '已复制到剪贴板'; }catch(e){ STATUS.textContent = '复制失败，请手动选择'; }
      document.body.removeChild(ta);
    }
  });

  window.toggle_block = function(btn){
    const wrapper = btn.closest('div');
    const coll = wrapper ? wrapper.querySelector('.collapsible') : null;
    const che = btn.querySelector('.chevron-icon');
    if(coll){ coll.classList.toggle('open'); }
    if(che){ che.classList.toggle('rotate'); }
  };

  const qBlocks = document.querySelectorAll('#quiz-form > div');
  const TOTAL_QUESTIONS = qBlocks.length;
  const quizSolved = new Array(TOTAL_QUESTIONS).fill(false);
  const quizCorrect = new Array(TOTAL_QUESTIONS).fill(false);

  function updateQuizTotal(){
    const total = document.getElementById('quiz-total');
    if(!total) return;
    let solvedCount = 0, correctCount = 0;
    for(let i=0;i<quizSolved.length;i++){ if(quizSolved[i]){ solvedCount++; if(quizCorrect[i]) correctCount++; } }
    if(solvedCount === 0){ total.textContent = ''; return; }
    let msg = '你已作答 ' + solvedCount + ' / ' + TOTAL_QUESTIONS + ' 题，答对 ' + correctCount + ' 题。';
    if(solvedCount === TOTAL_QUESTIONS){
      if(correctCount === TOTAL_QUESTIONS) msg += ' 🎉 全部答对，知识点掌握良好！';
      else if(correctCount >= 2) msg += ' 👍 不错，建议再看一遍解析巩固。';
      else msg += ' 📚 建议回头复习知识点部分。';
    }
    total.textContent = msg;
  }

  document.querySelectorAll('.btn-submit-quiz').forEach(function(btn){
    btn.addEventListener('click', function(){
      const qIdx = parseInt(btn.getAttribute('data-q'), 10);
      const qBlock = qBlocks[qIdx];
      const correctIdx = parseInt(qBlock.getAttribute('data-correct'), 10);
      let chosen = null;
      qBlock.querySelectorAll('.quiz-option').forEach(function(opt){
        const input = opt.querySelector('input');
        opt.classList.remove('correct','wrong');
        const tag = opt.querySelector('.quiz-result-tag');
        if(tag){ tag.classList.remove('show','ok','bad'); tag.textContent = ''; }
        if(input && input.checked){ chosen = parseInt(opt.getAttribute('data-i'),10); }
      });
      const explainEl = qBlock.querySelector('.quiz-explain');
      if(chosen === null){
        if(explainEl){ explainEl.textContent = '⚠ 请先选择一个答案再提交'; explainEl.classList.remove('hidden'); }
        return;
      }
      let chosenOk = (chosen === correctIdx);
      qBlock.querySelectorAll('.quiz-option').forEach(function(opt){
        const iVal = parseInt(opt.getAttribute('data-i'),10);
        const tag = opt.querySelector('.quiz-result-tag');
        if(iVal === correctIdx){ opt.classList.add('correct'); if(tag){ tag.textContent='✓ 正确答案'; tag.classList.add('show','ok'); } }
        else if(iVal === chosen){ opt.classList.add('wrong'); if(tag){ tag.textContent='✗ 你的选择'; tag.classList.add('show','bad'); } }
      });
      quizSolved[qIdx] = true; quizCorrect[qIdx] = chosenOk;
      if(explainEl){ explainEl.classList.remove('hidden'); }
      updateQuizTotal();
    });
  });
  document.querySelectorAll('.btn-reset-quiz').forEach(function(btn){
    btn.addEventListener('click', function(){
      const qIdx = parseInt(btn.getAttribute('data-q'), 10);
      const qBlock = qBlocks[qIdx];
      qBlock.querySelectorAll('.quiz-option').forEach(function(opt){
        opt.classList.remove('correct','wrong');
        const input = opt.querySelector('input'); if(input) input.checked = false;
        const tag = opt.querySelector('.quiz-result-tag'); if(tag){ tag.classList.remove('show','ok','bad'); tag.textContent=''; }
      });
      const ex = qBlock.querySelector('.quiz-explain'); if(ex) ex.classList.add('hidden');
      quizSolved[qIdx] = false; quizCorrect[qIdx] = false; updateQuizTotal();
    });
  });
})();
</script>
</body>
</html>
""" %% (
    c["idx"], c["idx"],
    level_color, c["level_text"], c["hours"], c["rating"],
    c["title"], c["subtitle"],
    goals_html, c["audience"], c["prereq"],
    tags_html, knowledge_html, code_text, quiz_html, summary_bullets,
)

        path = os.path.join(OUT, "course%d.html" %% c["idx"])
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("✓ 生成 %s" %% path)


def build_index():
    """生成首页 index.html"""
    cards = []
    for c in COURSES_META:
        level_color_map = {
            "beginner": "text-green-700 bg-green-50 border-green-200",
            "intermediate": "text-brand-700 bg-brand-50 border-brand-200",
            "advanced": "text-violet-700 bg-violet-50 border-violet-200",
        }
        level_color = level_color_map[c["level"]]
        tags_html = "".join(['<span class="inline-block bg-brand-50 text-brand-700 text-xs rounded-full px-3 py-1 mr-2 mb-2 border border-brand-100">%s</span>' %% t for t in c["tags"]])
        cards.append(
            '<a href="course%d.html" class="course-card bg-white rounded-2xl p-6 shadow-sm hover-lift border border-gray-100 block" data-level="%s">\n'
            '  <div class="flex items-start justify-between mb-3">\n'
            '    <span class="text-xs font-semibold px-3 py-1 rounded-full border %s">%s</span>\n'
            '    <span class="text-xs text-gray-400">⏱ %s · ★ %s</span>\n'
            '  </div>\n'
            '  <h3 class="text-lg font-bold text-gray-900 mb-2">%02d. %s</h3>\n'
            '  <p class="text-sm text-gray-500 leading-relaxed mb-4">%s</p>\n'
            '  <div class="flex flex-wrap gap-1.5">%s</div>\n'
            '</a>\n' %% (
                c["idx"], c["level"], level_color, c["level_text"],
                c["hours"], c["rating"], c["idx"], c["title"], c["subtitle"], tags_html,
            )
        )
    cards_html = "\n".join(cards)

    index = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>DataLearn · 商务数据分析与应用 Python 学习平台</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = { theme: { extend: {
    colors: { brand: { 50:'#EEF4FF',100:'#DBE8FF',200:'#B8D1FF',500:'#165DFF',600:'#0E4BDB',700:'#0A39A8' } }
  }}}
</script>
<style>
body { font-family:"PingFang SC","Microsoft YaHei",sans-serif; background:#F5F7FA; }
.hover-lift { transition: transform .25s ease, box-shadow .25s ease; }
.hover-lift:hover { transform: translateY(-4px); box-shadow: 0 14px 36px rgba(22,93,255,.18); }
.filter-btn { transition: background-color .2s ease, color .2s ease, border-color .2s ease; }
</style>
</head>
<body class="antialiased">

<nav class="bg-white/95 backdrop-blur border-b border-gray-100 sticky top-0 z-40">
  <div class="max-w-6xl mx-auto px-4 md:px-6 py-3 flex items-center justify-between">
    <a href="#top" class="flex items-center gap-2 font-bold text-brand-500">
      <span class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-brand-500 text-white text-sm">D</span>DataLearn
    </a>
    <div class="hidden md:flex items-center gap-7 text-sm text-gray-600">
      <a href="#courses" class="hover:text-brand-500 transition">精选课程</a>
      <a href="#path" class="hover:text-brand-500 transition">学习路径</a>
      <a href="#stack" class="hover:text-brand-500 transition">技术栈</a>
    </div>
    <a href="#courses" class="text-sm bg-brand-500 hover:bg-brand-600 text-white px-4 py-2 rounded-lg font-semibold">开始学习</a>
  </div>
</nav>

<header id="top" class="bg-gradient-to-br from-brand-50 via-white to-brand-50">
  <div class="max-w-6xl mx-auto px-4 md:px-6 py-16 md:py-20 text-center">
    <div class="inline-flex items-center gap-2 bg-white border border-brand-100 text-brand-500 px-4 py-1.5 rounded-full text-xs font-medium shadow-sm mb-6">
      <span>📊</span> 商务数据分析 · Python 实战学习社区
    </div>
    <h1 class="text-3xl md:text-5xl font-extrabold text-gray-900 leading-tight tracking-tight">
      商务数据分析与应用
      <span class="block text-brand-500 mt-2">Python 学习平台</span>
    </h1>
    <p class="mt-6 text-base md:text-lg text-gray-500 max-w-2xl mx-auto leading-relaxed">
      系统化学习数据分析技能，从基础到进阶，助你成为数据驱动的商务决策专家。浏览器内直接运行 Python，无需安装任何环境。
    </p>
    <div class="mt-8 flex flex-wrap justify-center gap-3">
      <a href="#courses" class="bg-brand-500 hover:bg-brand-600 text-white px-6 py-3 rounded-xl font-semibold shadow-sm inline-flex items-center gap-2">📚 浏览课程</a>
      <a href="#path" class="bg-white border border-gray-200 text-gray-700 px-6 py-3 rounded-xl font-semibold hover-lift inline-flex items-center gap-2">🗺️ 查看路径</a>
    </div>
  </div>
</header>

<main class="max-w-6xl mx-auto px-4 md:px-6 pb-16 space-y-12">

<section>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
    <div class="bg-white rounded-2xl p-5 shadow-sm hover-lift text-center border border-gray-100"><div class="text-2xl md:text-3xl font-extrabold text-gray-900">10</div><div class="text-xs md:text-sm text-gray-500 mt-1">精品实战课程</div></div>
    <div class="bg-white rounded-2xl p-5 shadow-sm hover-lift text-center border border-gray-100"><div class="text-2xl md:text-3xl font-extrabold text-gray-900">8500+</div><div class="text-xs md:text-sm text-gray-500 mt-1">累计学习人数</div></div>
    <div class="bg-white rounded-2xl p-5 shadow-sm hover-lift text-center border border-gray-100"><div class="text-2xl md:text-3xl font-extrabold text-gray-900">4.8</div><div class="text-xs md:text-sm text-gray-500 mt-1">课程平均评分</div></div>
    <div class="bg-white rounded-2xl p-5 shadow-sm hover-lift text-center border border-gray-100"><div class="text-2xl md:text-3xl font-extrabold text-gray-900">0</div><div class="text-xs md:text-sm text-gray-500 mt-1">配置依赖（浏览器内直接运行 Python）</div></div>
  </div>
</section>

<section class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-10">
  <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-4">🧭 平台简介</h2>
  <p class="text-gray-600 leading-relaxed text-sm md:text-base">
    DataLearn 是面向商务数据分析方向的 Python 实战学习平台。每门课程都配备浏览器内可运行的 Python 代码编辑器（基于 Skulpt 轻量解释器），
    加载速度快、无需安装依赖。精选 10 门真实业务场景，覆盖零售、电商、餐饮、金融、人力、增长等典型行业。
  </p>
  <div class="grid md:grid-cols-3 gap-4 mt-6">
    <div class="bg-brand-50/60 rounded-xl p-5 border border-brand-100"><div class="text-brand-600 font-semibold mb-1">🎯 目标清晰</div><div class="text-sm text-gray-600">按业务场景设计，学完即可落地。</div></div>
    <div class="bg-brand-50/60 rounded-xl p-5 border border-brand-100"><div class="text-brand-600 font-semibold mb-1">⚡ 即开即用</div><div class="text-sm text-gray-600">浏览器内直接运行 Python，无需本地环境。</div></div>
    <div class="bg-brand-50/60 rounded-xl p-5 border border-brand-100"><div class="text-brand-600 font-semibold mb-1">🧩 路径完整</div><div class="text-sm text-gray-600">从零基础到高阶建模，一站式循序渐进。</div></div>
  </div>
</section>

<section id="courses">
  <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-2">📚 10 门 Python 数据分析实战课程</h2>
  <p class="text-sm text-gray-500 mb-4">点击任意课程卡片，进入课程详情页，可直接在浏览器中编写并运行 Python 代码。</p>
  <div class="flex flex-wrap gap-2 mb-6">
    <button class="filter-btn px-4 py-2 rounded-full text-sm font-semibold bg-brand-500 text-white shadow" data-level="all">全部课程</button>
    <button class="filter-btn px-4 py-2 rounded-full text-sm font-semibold bg-white text-gray-700 border border-gray-200 hover:bg-green-50" data-level="beginner">初级课程</button>
    <button class="filter-btn px-4 py-2 rounded-full text-sm font-semibold bg-white text-gray-700 border border-gray-200 hover:bg-brand-50" data-level="intermediate">中级课程</button>
    <button class="filter-btn px-4 py-2 rounded-full text-sm font-semibold bg-white text-gray-700 border border-gray-200 hover:bg-violet-50" data-level="advanced">高级课程</button>
  </div>
  <div class="grid md:grid-cols-2 gap-5">
    %s
  </div>
</section>

<section id="path">
  <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-2">🗺️ 一站式学习路径</h2>
  <p class="text-sm text-gray-500 mb-6">从零基础到高阶建模，按阶段稳步提升。</p>
  <div class="grid md:grid-cols-3 gap-5">
    <div class="bg-white rounded-2xl p-6 shadow-sm hover-lift border-t-4 border-green-400">
      <div class="text-xs font-bold text-green-600 bg-green-50 inline-block px-3 py-1 rounded-full mb-3">STAGE 01 · 入门</div>
      <h3 class="text-lg font-bold text-gray-900 mb-2">零基础入门 🌱</h3>
      <p class="text-sm text-gray-500 leading-relaxed mb-4">掌握 Python 基础语法与 Pandas 数据处理，能够独立读取、清洗、基础统计与简单可视化。</p>
      <ul class="text-xs text-gray-500 space-y-1 list-disc list-inside"><li>零售门店客流数据分析</li><li>电商订单数据异常检测</li></ul>
    </div>
    <div class="bg-white rounded-2xl p-6 shadow-sm hover-lift border-t-4 border-brand-500">
      <div class="text-xs font-bold text-brand-600 bg-brand-50 inline-block px-3 py-1 rounded-full mb-3">STAGE 02 · 实战</div>
      <h3 class="text-lg font-bold text-gray-900 mb-2">中级实战 🚀</h3>
      <p class="text-sm text-gray-500 leading-relaxed mb-4">熟练使用分组聚合、透视表、多表合并、关联规则，能够独立完成用户分层、营销分析、经营诊断。</p>
      <ul class="text-xs text-gray-500 space-y-1 list-disc list-inside"><li>RFM 用户分层 / Apriori 购物篮分析</li><li>员工绩效分析 / 餐饮营收分析</li></ul>
    </div>
    <div class="bg-white rounded-2xl p-6 shadow-sm hover-lift border-t-4 border-violet-500">
      <div class="text-xs font-bold text-violet-700 bg-violet-50 inline-block px-3 py-1 rounded-full mb-3">STAGE 03 · 建模</div>
      <h3 class="text-lg font-bold text-gray-900 mb-2">高阶建模 🏆</h3>
      <p class="text-sm text-gray-500 leading-relaxed mb-4">掌握时间序列、分类模型、流失预测、A/B 实验设计等高阶方法，能够独立承担商务建模与决策支持。</p>
      <ul class="text-xs text-gray-500 space-y-1 list-disc list-inside"><li>库存销量预测 / 信贷风险评估</li><li>用户流失预测 / A/B 测试</li></ul>
    </div>
  </div>
</section>

<section id="stack">
  <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-2">💻 课程核心技术栈</h2>
  <p class="text-sm text-gray-500 mb-6">所有课程在浏览器中使用 Skulpt 直接运行 Python，无需安装任何依赖。</p>
  <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
    <div class="flex flex-wrap gap-2">
      <span class="px-3 py-1.5 rounded-lg bg-blue-50 text-blue-700 text-xs font-medium border border-blue-100">Python</span>
      <span class="px-3 py-1.5 rounded-lg bg-blue-50 text-blue-700 text-xs font-medium border border-blue-100">列表与字典</span>
      <span class="px-3 py-1.5 rounded-lg bg-sky-50 text-sky-700 text-xs font-medium border border-sky-100">循环与条件</span>
      <span class="px-3 py-1.5 rounded-lg bg-indigo-50 text-indigo-700 text-xs font-medium border border-indigo-100">分组聚合</span>
      <span class="px-3 py-1.5 rounded-lg bg-cyan-50 text-cyan-700 text-xs font-medium border border-cyan-100">时间序列</span>
      <span class="px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-700 text-xs font-medium border border-emerald-100">移动平均</span>
      <span class="px-3 py-1.5 rounded-lg bg-teal-50 text-teal-700 text-xs font-medium border border-teal-100">Apriori 思想</span>
      <span class="px-3 py-1.5 rounded-lg bg-violet-50 text-violet-700 text-xs font-medium border border-violet-100">RFM 模型</span>
      <span class="px-3 py-1.5 rounded-lg bg-rose-50 text-rose-700 text-xs font-medium border border-rose-100">规则式风控</span>
      <span class="px-3 py-1.5 rounded-lg bg-amber-50 text-amber-700 text-xs font-medium border border-amber-100">假设检验</span>
      <span class="px-3 py-1.5 rounded-lg bg-lime-50 text-lime-700 text-xs font-medium border border-lime-100">转化率分析</span>
      <span class="px-3 py-1.5 rounded-lg bg-purple-50 text-purple-700 text-xs font-medium border border-purple-100">数据可视化思维</span>
      <span class="px-3 py-1.5 rounded-lg bg-brand-50 text-brand-700 text-xs font-medium border border-brand-100">Skulpt 浏览器内 Python</span>
    </div>
  </div>
</section>

<section>
  <div class="bg-gradient-to-br from-brand-500 to-brand-700 rounded-3xl p-8 md:p-12 text-center text-white shadow-sm relative overflow-hidden">
    <div class="absolute -top-10 -right-10 w-48 h-48 bg-white/10 rounded-full"></div>
    <div class="absolute -bottom-12 -left-12 w-56 h-56 bg-white/10 rounded-full"></div>
    <div class="relative">
      <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-white/15 text-2xl mb-4">🎓</div>
      <h2 class="text-2xl md:text-3xl font-bold mb-3">开始你的数据分析学习之旅</h2>
      <p class="text-base md:text-lg text-brand-50/90 max-w-2xl mx-auto leading-relaxed mb-7">
        加入学习社区，与其他商务数据分析专业的学习者一起成长。
      </p>
      <a href="#courses" class="inline-flex items-center gap-2 bg-white text-brand-600 font-semibold px-7 py-3.5 rounded-xl shadow hover:bg-brand-50 transition">立即加入学习 →</a>
    </div>
  </div>
</section>

</main>

<footer class="bg-white border-t border-gray-100">
  <div class="max-w-6xl mx-auto px-6 py-6 text-center text-xs text-gray-400">
    &copy; 2026 DataLearn · 商务数据分析与应用 Python 学习平台 · Powered by Skulpt（浏览器内 Python）
  </div>
</footer>

<script>
(function(){
  const cards = document.querySelectorAll('.course-card');
  document.querySelectorAll('.filter-btn').forEach(function(btn){
    btn.addEventListener('click', function(){
      const lv = btn.getAttribute('data-level');
      document.querySelectorAll('.filter-btn').forEach(function(other){
        other.classList.remove('bg-brand-500','text-white','shadow');
        other.classList.add('bg-white','text-gray-700','border','border-gray-200');
      });
      btn.classList.remove('bg-white','text-gray-700','border','border-gray-200');
      btn.classList.add('bg-brand-500','text-white','shadow');
      cards.forEach(function(card){
        if(lv === 'all' || card.getAttribute('data-level') === lv){
          card.style.display = '';
        }else{
          card.style.display = 'none';
        }
      });
    });
  });
})();
</script>
</body>
</html>
""" %% (cards_html,)
    path = os.path.join(OUT, "index.html")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(index)
    print("✓ 生成 %s" %% path)


if __name__ == "__main__":
    main()
    build_index()
    print("\n共生成 %d 门课程页面 + 1 个首页。" %% len(COURSES_META))
