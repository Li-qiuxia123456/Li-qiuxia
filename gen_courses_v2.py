"""
10 门课程的数据 (course1~course10)
每个课程返回一个 dict:
  idx, title, subtitle, level, hours, rating, tags,
  goals, audience, prereq,
  sections: [{title, body, code}]   # 知识点讲解（可折叠）
  default_code: 字符串              # 在线代码练习默认示例
  quiz: [{q, options, answer, explain}]
  thinking: 字符串                  # 编程题思路 & 常见错误
  summary: [{title, body}]
"""

def course1():
    return dict(
      idx=1, title="零售门店客流数据分析",
      subtitle="用 Pandas 处理时间序列数据、分析客流时段分布、输出门店运营建议",
      level="beginner", hours="9 小时", rating="4.8",
      tags=["Pandas","时间处理","客流统计","零售运营","Matplotlib"],
      goals="1) 掌握用 Pandas 处理时间序列数据与日期字段\n2) 按小时/日/周统计客流并做对比\n3) 理解高峰时段与周末效应\n4) 输出门店运营优化与排班建议",
      audience="零售运营人员、门店店长、商业数据分析师、入门 Python 学习者",
      prereq="Python 基础语法、Pandas DataFrame、Matplotlib 基础",
      sections=[
        dict(title="① 核心业务指标",
             body="""<p>零售门店客流分析最常用的 4 个业务指标：</p>
             <ul class="list-disc list-inside space-y-1 text-sm mt-2 text-gray-700">
             <li>日均客流 = 统计期总客流 / 天数</li>
             <li>时段客流分布 = 每天各小时的平均客流</li>
             <li>周末效应 = 周末客流均值 / 工作日客流均值</li>
             <li>进店转化率 = 成交订单数 / 进店人数</li>
             </ul>
             <p class="text-sm text-gray-600 mt-2">通过客流分布可反推排班、促销窗口、库存补货时点。</p>""",
             code="""# 示例：一个简单的 3 天客流表
import pandas as pd
df = pd.DataFrame({
    'date': pd.to_datetime(['2024-09-01','2024-09-01','2024-09-02','2024-09-02']),
    'hour': [12, 18, 12, 18],
    'traffic': [80, 150, 70, 140],
})
print('每日总客流:')
print(df.groupby(df['date'].dt.date)['traffic'].sum())
"""),
        dict(title="② 时间字段处理",
             body="""<p>时间字段是客流分析的关键：</p>
             <ol class="list-decimal list-inside space-y-1 text-sm mt-2 text-gray-700">
             <li><code>pd.to_datetime()</code> 把字符串转 datetime</li>
             <li><code>Series.dt.hour / .dt.day_name() / .dt.weekday</code> 提取小时/周几</li>
             <li><code>groupby('hour')</code> 聚合各时段平均值</li>
             <li>区分"工作日 / 周末"发现周末效应</li>
             </ol>""",
             code="""df['hour'] = df['date'].dt.hour
df['weekday'] = df['date'].dt.day_name()
df['is_weekend'] = df['date'].dt.weekday >= 5
print(df)
"""),
        dict(title="③ 可视化：折线图",
             body="""<p>折线图最适合展示"随时间变化"的趋势；柱状图用于对比各时段绝对值。</p>""",
             code="""import matplotlib.pyplot as plt
hourly = df.groupby('hour')['traffic'].mean().reset_index()
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(hourly['hour'], hourly['traffic'], marker='o', color='#165DFF', linewidth=2)
ax.set_title('门店各时段平均客流'); ax.set_xlabel('小时'); ax.set_ylabel('客流')
ax.grid(alpha=0.3); plt.tight_layout(); plt.show()
"""),
      ],
      default_code="""import pandas as pd
import matplotlib.pyplot as plt

# ===========================
# 示例：某门店一周的客流数据
# ===========================
rows = [
    ('2024-09-01',  9,  30), ('2024-09-01', 12,  80), ('2024-09-01', 18, 150),
    ('2024-09-02',  9,  28), ('2024-09-02', 12,  75), ('2024-09-02', 18, 140),
    ('2024-09-03',  9,  32), ('2024-09-03', 12,  88), ('2024-09-03', 18, 160),
    ('2024-09-04',  9,  25), ('2024-09-04', 12,  70), ('2024-09-04', 18, 130),
    ('2024-09-05',  9,  40), ('2024-09-05', 12,  95), ('2024-09-05', 18, 170),
    ('2024-09-06',  9,  45), ('2024-09-06', 12, 110), ('2024-09-06', 18, 180),
    ('2024-09-07',  9,  60), ('2024-09-07', 12, 130), ('2024-09-07', 18, 210),
    ('2024-09-08',  9,  70), ('2024-09-08', 12, 140), ('2024-09-08', 18, 230),
]
df = pd.DataFrame(rows, columns=['date','hour','traffic'])
df['date'] = pd.to_datetime(df['date'])

# 1) 每日总客流
daily = df.groupby(df['date'].dt.date)['traffic'].sum().reset_index()
daily.columns = ['日期','总客流']
print('==== 每日总客流 ====')
print(daily.to_string(index=False))

# 2) 按小时平均客流
hourly = df.groupby('hour')['traffic'].mean().reset_index()
hourly.columns = ['小时','平均客流']
print('\\n==== 按小时平均客流 ====')
print(hourly.to_string(index=False))

# 3) 绘制折线图
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(hourly['小时'], hourly['平均客流'], marker='o', color='#165DFF', linewidth=2)
ax.set_title('门店各时段平均客流趋势')
ax.set_xlabel('小时'); ax.set_ylabel('平均客流（人）')
ax.set_xticks(range(9, 24, 2)); ax.grid(alpha=0.3)
plt.tight_layout(); plt.show()

# 4) 自动生成量化运营建议
max_hour = int(hourly.loc[hourly['平均客流'].idxmax(), '小时'])
avg_traffic = hourly['平均客流'].mean()
print(f'\\n🧭 运营建议：')
print(f'· 客流峰值出现在 {max_hour}:00 左右，建议在该时段增加销售人手；')
print(f'· 平均每小时客流约 {avg_traffic:.0f} 人，可据此调整午餐/晚餐促销窗口；')
print(f'· 周末客流明显高于工作日，建议在周末安排重点活动或加大库存。')
""",
      quiz=[
        dict(q='在客流分析中，"日均客流"的正确计算方式是？',
             options=['统计期总客流 / 天数','统计期总客流 / 小时数','统计期平均每天订单数','统计期总订单数 / 2'],
             answer=0, explain='日均客流 = 统计期总客流 / 统计天数，用于判断门店每日承载能力。'),
        dict(q='提取时间字段的小时，最方便的 Pandas 写法是？',
             options=['df["date"].dt.hour','df["date"].hour','df["date"].dt.strftime','df["date"].get_hour()'],
             answer=0, explain='Series.dt.hour 是 Pandas 提供的便捷访问器，可返回小时整数。'),
        dict(q='下列哪项最能体现"周末效应"？',
             options=['周末客流均值 / 工作日客流均值','总订单数 / 总库存','小时客流 / 日客流','成交订单 / 进店人数'],
             answer=0, explain='周末客流 ÷ 工作日客流 > 1.5 时，表明周末明显更忙，是典型的周末效应。'),
      ],
      thinking="""核心思路：
① 先把日期字符串 -> datetime (pd.to_datetime)，避免当作普通字符串处理；
② 用 groupby + 聚合函数 (sum / mean / max) 得到按天、按小时的统计；
③ 用 idxmax / idxmin 找到峰值，为业务决策提供支撑；
④ 绘图时设置合适的标题、轴标签、刻度，让业务方可直接看懂。

常见错误：
- 忘记把字符串转 datetime，导致访问 .dt.hour 时报错；
- 聚合前后列名不一致，建议显式指定 columns；
- 图形尺寸太小，轴标签重叠，建议 figsize 至少 (7,4)。
""",
      summary=[
        dict(title="关键知识点", body="时间字段 (pd.to_datetime)、分组聚合 (groupby)、折线图 (plt.plot)。"),
        dict(title="核心代码", body="df.groupby('hour')['traffic'].mean()；df['date'].dt.day_name()；plt.plot()。"),
        dict(title="业务价值", body="为门店排班、促销时点、库存补货提供量化依据，直接影响运营效率与顾客体验。"),
      ]
    )


def course2():
    return dict(
      idx=2, title="电商订单数据异常检测",
      subtitle="识别重复订单、金额异常、虚假订单，掌握数据治理基础方法",
      level="beginner", hours="8 小时", rating="4.7",
      tags=["数据异常检测","订单分析","Pandas 筛选","去重"],
      goals="1) 识别订单数据中的重复行与缺失值\n2) 用 3 倍标准差法判断金额异常\n3) 掌握基于条件筛选的异常记录定位\n4) 学会清洗、标记、汇总异常数据",
      audience="电商数据分析师、数据治理岗位、初级 Python 数据工程师",
      prereq="Python 基础、Pandas 筛选与聚合",
      sections=[
        dict(title="① 重复订单识别", body="""<p>同一条订单出现多次往往是接口重试、数据库主键冲突或 ETL 重复导致。</p>
             <ul class="list-disc list-inside space-y-1 text-sm mt-2 text-gray-700">
             <li><code>duplicated(subset=['order_id'])</code> 标记重复行</li>
             <li><code>drop_duplicates(subset=['order_id'])</code> 去重</li>
             <li>保留最早/最新一条，视业务规则而定</li>
             </ul>""",
             code="""import pandas as pd
orders = pd.DataFrame({
    'order_id': ['A1','A1','A2','A3','A4','A4'],
    'amount': [100, 100, 250, 88, 1500, 1500],
})
dup = orders[orders.duplicated(subset=['order_id'], keep=False)]
print('疑似重复订单:')
print(dup)
print('去重后记录数:', orders.drop_duplicates(subset=['order_id']).shape[0])
"""),
        dict(title="② 3 倍标准差法金额异常", body="""<p>对于近似正态分布的数值，可用均值 ± 3×标准差作为异常阈值，落在区间外的视为异常。</p>
             <ul class="list-disc list-inside space-y-1 text-sm mt-2 text-gray-700">
             <li>计算 <code>mean, std</code>；</li>
             <li>上界 = mean + 3*std；下界 = max(0, mean - 3*std)</li>
             <li>对非正态分布，推荐用 IQR / 分位数法</li>
             </ul>""",
             code="""amount = pd.Series([100, 120, 95, 110, 2000, 130, 105])
mean, std = amount.mean(), amount.std()
upper = mean + 3*std; lower = max(0, mean - 3*std)
print(f'mean={mean:.1f}, std={std:.1f}, 上界={upper:.1f}, 下界={lower:.1f}')
print('异常金额:', list(amount[(amount > upper) | (amount < lower)]))
"""),
        dict(title="③ 缺失值处理", body="""<p>常见做法：删除 (dropna)、填充 (fillna)、按业务规则 (如金额为 0) 处理。</p>""",
             code="""df = pd.DataFrame({'a':[1,2,None,4],'b':[None,2,3,4]})
print('每列缺失数:\\n', df.isna().sum())
print('填充后:\\n', df.fillna(0))
"""),
      ],
      default_code="""import pandas as pd
import numpy as np

# ========================================
# 示例：构造一批模拟订单数据
# ========================================
data = {
    'order_id': ['O1','O1','O2','O3','O4','O5','O6','O6','O7','O8','O9','O10'],
    'amount':   [100, 100, 250, 88, 1500, 120, 110, 110, 3500, 95, 130, 105],
    'user_id':  ['u1','u1','u2','u3','u4','u5','u6','u6','u7','u8','u9','u10'],
    'status':   ['paid','paid','paid','paid','paid','refund','paid','paid','paid','paid','paid','paid'],
}
orders = pd.DataFrame(data)

print('==== 原始订单 (前 10 行) ====')
print(orders.head(10).to_string(index=False))
print()

# 1) 检测重复订单
dup_mask = orders.duplicated(subset=['order_id'], keep=False)
dups = orders[dup_mask]
print(f'⚠ 发现 {dups.shape[0]} 条疑似重复订单:')
print(dups.to_string(index=False))
print()

# 2) 3 倍标准差法检测金额异常
amounts = orders['amount']
mean, std = amounts.mean(), amounts.std()
upper = mean + 3 * std
abnormal = orders[(orders['amount'] > upper) | (orders['amount'] <= 0)]
print(f'📊 金额统计：mean={mean:.2f}, std={std:.2f}, 上界={upper:.2f}')
print(f'⚠ 检测到 {abnormal.shape[0]} 条金额异常订单：')
print(abnormal.to_string(index=False))
print()

# 3) 检查退款订单
refunds = orders[orders['status'] == 'refund']
print(f'🔁 退款订单共 {refunds.shape[0]} 条：')
print(refunds.to_string(index=False))
print()

# 4) 汇总治理建议
clean = orders.drop_duplicates(subset=['order_id'], keep='first')
print('==== 清洗后 ====')
print(f'原始订单数：{len(orders)}；清洗后订单数：{len(clean)}；')
print(f'正常订单总金额：{clean[(clean["status"]=="paid")]["amount"].sum()} 元')
print('建议：对异常金额订单二次核实，并同步订单系统修复重复记录。')
""",
      quiz=[
        dict(q='用 Pandas 检测某列重复行，最直接的方法是？',
             options=['df.duplicated(subset=[...])','df.isnull()','df.replace()','df.dropna()'],
             answer=0, explain='duplicated() 返回布尔掩码，标记重复行；配合 keep 参数可保留首条。'),
        dict(q='3 倍标准差法中，"异常值"通常指？',
             options=['绝对值大于 1','落在 mean ± 3*std 之外','数值为整数','值小于 mean'],
             answer=1, explain='近似正态分布时，约 99.7% 的数据落在 mean±3*std，之外的数据视为较罕见的异常。'),
        dict(q='下列哪种做法不适合作为异常值的后续处理？',
             options=['结合业务二次核实','标记 flag 后单独汇总','直接删除所有异常再出报表','与业务方沟通后修正或保留'],
             answer=2, explain='简单粗暴直接"删除所有异常"可能丢掉关键业务信号（如大额订单、欺诈订单等），需结合业务判断。'),
      ],
      thinking="""核心思路：
① duplicated(subset=['order_id']) 先识别重复订单；
② 对数值字段做 mean ± 3*std 的简单异常检测；
③ 使用布尔索引 df[condition] 筛选异常行；
④ 对订单状态（如 refund）进行专项分析。
最终把数据治理结论输出给业务方，促进系统规范化。

常见错误：
- 忘记 subset 导致把完全相同的行才视为重复；
- std 基于异常数据计算，循环依赖，建议先肉眼观察；
- 忽略业务含义，把"大额高价值订单"误判为异常直接删除。
""",
      summary=[
        dict(title="关键知识点", body="重复检测 (duplicated / drop_duplicates)、3-sigma 异常检测、条件筛选、缺失值处理。"),
        dict(title="核心代码", body="df.duplicated(subset=['order_id'])；mean + 3*std 阈值；df[df.status=='refund']。"),
        dict(title="业务价值", body="发现订单异常可减少坏账、识别系统 bug、支撑数据治理与审计工作。"),
      ]
    )


def course3():
    return dict(
      idx=3, title="用户分层与精准营销分析（RFM）",
      subtitle="基于 RFM 模型对用户进行价值分层，制定差异化营销策略",
      level="intermediate", hours="13 小时", rating="4.9",
      tags=["RFM 模型","用户分层","营销分析","Pandas 聚合"],
      goals="1) 理解 RFM 三大指标的业务含义\n2) 学会用 Pandas 计算每位用户的 R/F/M\n3) 按 RFM 将用户分层并制定对应策略\n4) 输出可执行的营销建议与话术",
      audience="CRM / 用户运营 / 数据产品 / 商业数据分析师",
      prereq="Pandas 分组聚合、时间字段处理",
      sections=[
        dict(title="① RFM 三指标", body="""<ul class="list-disc list-inside space-y-1 text-sm text-gray-700">
             <li><b>Recency (R)</b>：最近一次购买距今的天数，越小越活跃</li>
             <li><b>Frequency (F)</b>：统计期内购买次数，越大越忠诚</li>
             <li><b>Monetary (M)</b>：统计期内消费总金额，越大越有价值</li>
             </ul>
             <p class="text-sm text-gray-600 mt-2">R 小、F 大、M 大 → 高价值用户。</p>""",
             code="""import pandas as pd
orders = pd.DataFrame({'user':['u1','u1','u2','u2','u3'],'days_ago':[2,10,5,30,60],'amount':[100,200,80,300,50]})
rfm = orders.groupby('user').agg(R=('days_ago','min'), F=('amount','count'), M=('amount','sum')).reset_index()
print(rfm)
"""),
        dict(title="② 分位数打分", body="""<p>将 R / F / M 分别按分位数划分为 1-5 分：</p>
             <ul class="list-disc list-inside space-y-1 text-sm text-gray-700">
             <li>R 越小越有价值，所以 R 越小得分越高</li>
             <li>F / M 越大得分越高</li>
             <li>使用 <code>pd.qcut</code> 做等频划分</li>
             </ul>""",
             code="""rfm['R_score'] = pd.qcut(rfm['R'], q=5, labels=[5,4,3,2,1]).astype(int)
rfm['F_score'] = pd.qcut(rfm['F'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)
rfm['M_score'] = pd.qcut(rfm['M'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)
print(rfm)
"""),
        dict(title="③ 规则分层", body="""<p>用简单的规则将用户划分为：重要价值、重要发展、一般价值、流失预警等。</p>""",
             code="""def tier(r, f, m):
    if r >= 4 and f >= 4 and m >= 4: return '重要价值用户'
    if r >= 4 and (f < 4 or m < 4):   return '重要发展用户'
    if r < 3  and f >= 3 and m >= 3:  return '重要保持用户'
    if r < 3  and f < 3  and m < 3:   return '流失预警用户'
    return '一般用户'
rfm['tier'] = rfm.apply(lambda x: tier(x.R_score, x.F_score, x.M_score), axis=1)
print(rfm['tier'].value_counts())
"""),
      ],
      default_code="""import pandas as pd

# ========================================
# 构造订单（user / 距今天数 / 金额）
# ========================================
orders = pd.DataFrame({
    'user':     ['u1','u1','u2','u2','u3','u4','u4','u5','u6','u6','u7','u8','u9','u10'],
    'days_ago': [2,  10,  5,  30, 60,  20, 40,  90,  3,  15,  70,  12, 25,  45],
    'amount':   [120,200, 80, 300, 50, 600, 150, 60, 400, 300, 40,  180, 90, 110],
})

# 1) 计算每位用户的 R/F/M
rfm = orders.groupby('user').agg(
    R=('days_ago', 'min'),
    F=('amount',   'count'),
    M=('amount',   'sum'),
).reset_index()

# 2) 分位数打分 (R 越小得分越高，F/M 越大得分越高)
rfm['R_score'] = pd.qcut(rfm['R'], q=5, labels=[5,4,3,2,1]).astype(int)
rfm['F_score'] = pd.qcut(rfm['F'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)
rfm['M_score'] = pd.qcut(rfm['M'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)

# 3) 分层规则
def tier(r, f, m):
    if r >= 4 and f >= 4 and m >= 4: return '① 重要价值用户'
    if r >= 4 and (f < 4 or m < 4):   return '② 重要发展用户'
    if r < 3  and f >= 3 and m >= 3:  return '③ 重要保持用户'
    if r < 3  and f < 3  and m < 3:   return '④ 流失预警用户'
    return '⑤ 一般用户'

rfm['分层'] = rfm.apply(lambda x: tier(x.R_score, x.F_score, x.M_score), axis=1)

print('==== RFM 用户分层总表 ====')
print(rfm.sort_values(['R_score','F_score','M_score'], ascending=[False,False,False]).to_string(index=False))
print()
print('==== 各分层用户数 ====')
print(rfm['分层'].value_counts().sort_index().to_string())
print()

# 4) 输出营销建议
print('🧭 差异化营销建议：')
print('· 重要价值用户：VIP 礼遇、专属客服、定制化推荐')
print('· 重要发展用户：发放首单/复购优惠券，提升购买频次')
print('· 重要保持用户：触达召回，推送高价值商品')
print('· 流失预警用户：限时优惠 + 个性化召回，配合流失调研')
print('· 一般用户：常规内容运营，提高活跃度')
""",
      quiz=[
        dict(q='RFM 模型中"R"指的是？',
             options=['用户总消费金额','最近一次购买距离今天的天数','用户购买总次数','用户注册时间'],
             answer=1, explain='R = Recency：最近一次购买距今天的天数，越小越活跃。'),
        dict(q='R 指标在 qcut 打分时，下列哪个说法正确？',
             options=['R 越小得分越高','R 越大得分越高','得分与 R 无关','所有用户得分相同'],
             answer=0, explain='R 越小说明用户近期越活跃，价值越高，得分越高。'),
        dict(q='一位用户 R 高分 5、F 低分 1、M 低分 1 最可能属于？',
             options=['重要价值用户','重要发展用户','流失预警','已流失用户'],
             answer=1, explain='近期活跃但频次/金额低，说明有潜力但未深度转化，属于重要发展用户。'),
      ],
      thinking="""核心思路：
① groupby + agg 计算每位用户 R/F/M 三个核心数值；
② qcut 按分位数把三个指标映射为 1-5 分（rank(method='first') 避免重复值报错）；
③ 用 if/elif 规则对用户分层（实际项目常结合 K-Means 等聚类）；
④ 对每一层输出差异化的运营/营销动作与话术。

常见错误：
- R 的分位数标签方向搞反（R 越小越有价值，所以分数应越大）；
- 未对 F/M 使用 rank(method='first')，导致重复值时 qcut 报错；
- 没有把分层统计结果与业务动作结合，停留在"算完就结束"。
""",
      summary=[
        dict(title="关键知识点", body="RFM 概念、分组聚合 (groupby.agg)、分位数划分 (qcut)、规则分层。"),
        dict(title="核心代码", body="rfm.groupby('user').agg(R=('days_ago','min'),F=('amount','count'),M=('amount','sum'))；pd.qcut()；apply + 规则。"),
        dict(title="业务价值", body="支撑 CRM 体系：召回流失用户、识别高价值用户、制定差异化营销策略、提升 ROI。"),
      ]
    )


def course4():
    return dict(
      idx=4, title="电商商品关联推荐分析（Apriori）",
      subtitle="挖掘商品组合关系，用于购物篮推荐与套餐设计",
      level="intermediate", hours="14 小时", rating="4.8",
      tags=["Apriori","关联规则","购物篮分析","组合推荐"],
      goals="1) 理解支持度、置信度、提升度三大关联指标\n2) 用 Python 实现简单的购物篮频次分析\n3) 识别高价值商品组合，落地到套餐与推荐",
      audience="电商推荐、产品运营、商品策略岗位",
      prereq="Pandas 数据处理、基本集合运算",
      sections=[
        dict(title="① 指标定义", body="""<ul class="list-disc list-inside space-y-1 text-sm text-gray-700">
             <li><b>支持度 (Support)</b>：商品(组合)出现的订单 / 总订单</li>
             <li><b>置信度 (Confidence)</b>：A -> B = P(B|A) = Support(A,B)/Support(A)</li>
             <li><b>提升度 (Lift)</b>：Confidence(A->B)/Support(B)；>1 说明比随机推更好</li>
             </ul>""",
             code="""baskets = [['牛奶','面包'],['牛奶','面包','鸡蛋'],['牛奶','饼干'],['面包','饼干']]
total = len(baskets)
# 牛奶 + 面包 支持度
count_ab = sum(1 for b in baskets if '牛奶' in b and '面包' in b)
print(f'Support(牛奶,面包) = {count_ab}/{total} = {count_ab/total:.2%}')
"""),
        dict(title="② 手工计算支持度", body="""<p>遍历所有订单，用 itertools.combinations 枚举所有 2-商品组合并计数。</p>""",
             code="""from itertools import combinations
from collections import Counter
baskets = [['A','B'],['A','B','C'],['A','D'],['B','C','D']]
counter = Counter()
for b in baskets:
    for pair in combinations(sorted(b), 2):
        counter[pair] += 1
for pair, cnt in counter.most_common():
    print(f'{pair} -> {cnt} 次，支持度 {cnt/len(baskets):.0%}')
"""),
        dict(title="③ 置信度与提升度", body="""<p>利用计数推导 P(B|A) 与提升度。</p>""",
             code="""single = Counter()
for b in baskets:
    for x in b: single[x] += 1
a, b = 'A', 'B'
conf = counter[(a,b)] / single[a]
lift = conf / (single[b] / len(baskets))
print(f'Confidence({a}->{b})={conf:.2%}, Lift={lift:.2f}')
"""),
      ],
      default_code="""from itertools import combinations
from collections import Counter

# ========================================
# 模拟订单：每一条是一个购物篮
# ========================================
baskets = [
    ['牛奶','面包'],
    ['牛奶','面包','鸡蛋'],
    ['牛奶','饼干'],
    ['面包','饼干','可乐'],
    ['牛奶','鸡蛋','饼干'],
    ['啤酒','薯片'],
    ['啤酒','薯片','牛奶'],
    ['面包','黄油','果酱'],
    ['鸡蛋','牛奶','黄油'],
    ['可乐','薯片'],
]

# 1) 单一商品计数 & 支持度
single = Counter()
for b in baskets:
    for x in b: single[x] += 1
total = len(baskets)
print('==== 单一商品支持度 ====')
for item, cnt in single.most_common():
    print(f'  {item}: {cnt}/{total} = {cnt/total:.0%}')

# 2) 2-商品组合计数 & 支持度
pair_counter = Counter()
for b in baskets:
    for pair in combinations(sorted(set(b)), 2):
        pair_counter[pair] += 1

print('\\n==== Top 2-商品组合 (支持度) ====')
for pair, cnt in pair_counter.most_common():
    print(f'  {pair}: {cnt}/{total} 支持度 {cnt/total:.0%}')

# 3) 计算置信度 A->B 与提升度
print('\\n==== 高置信度关联规则 (A→B) ====')
rules = []
for (a, b), cnt_ab in pair_counter.items():
    conf_ab = cnt_ab / single[a]
    lift_ab = conf_ab / (single[b] / total)
    conf_ba = cnt_ab / single[b]
    lift_ba = conf_ba / (single[a] / total)
    rules.append((a, b, conf_ab, lift_ab))
    rules.append((b, a, conf_ba, lift_ba))

rules.sort(key=lambda r: (-r[2], -r[3]))
for (a, b, conf, lift) in rules[:8]:
    flag = '⭐' if lift >= 1.2 else ''
    print(f'  {a:>4} → {b:>4}  置信度 {conf:.0%}  提升度 {lift:.2f} {flag}')

print('\\n🧭 业务建议：把支持度 & 提升度均高的商品组合设计为"搭配套餐"，')
print('并在详情页、购物车、结算页做关联推荐，可有效提高客单价。')
""",
      quiz=[
        dict(q='支持度 (Support) 的正确理解是？',
             options=['某个商品的总销售额','某个商品组合出现的订单数 / 总订单数','购买 A 的用户中购买 B 的比例','用户重复购买的次数'],
             answer=1, explain='支持度 = 商品(组合)出现的订单数 / 总订单数，代表"常见度"。'),
        dict(q='置信度 (Confidence) A→B 的公式是？',
             options=['P(A) / P(B)','P(A,B) / P(A)','P(A,B) / P(B)','P(A) + P(B)'],
             answer=1, explain='Confidence(A→B) = P(B|A) = Support(A,B) / Support(A)。'),
        dict(q='提升度 (Lift) > 1 意味着？',
             options=['规则没有意义','该组合比随机推荐 B 更有效','两个商品互相排斥','应立即下架'],
             answer=1, explain='Lift = Confidence / Support(B)；>1 代表规则比随机推荐有效，是值得采纳的组合。'),
      ],
      thinking="""核心思路：
① 先把每条订单视为"集合"；
② 用 Counter 统计单项 & 2-item 组合频次；
③ 通过频次推导支持度、置信度、提升度；
④ 按置信度排序后，挑选出业务上可用的组合，作为套餐/搭配推荐依据。

常见错误：
- 组合去重：combinations 已去重，但集合内的商品要先 set 去重；
- 小样本下置信度可能很高但不具业务意义，仍要结合支持度与提升度；
- 把组合的商品顺序搞反 (A→B 与 B→A 不同)。
""",
      summary=[
        dict(title="关键知识点", body="支持度 / 置信度 / 提升度、Counter 计数、combinations 组合枚举。"),
        dict(title="核心代码", body="combinations(sorted(basket),2) + Counter；Confidence = cnt_ab/single[a]；Lift = conf / (single[b]/total)。"),
        dict(title="业务价值", body="支撑搭配套餐、跨品类推荐、购物车推荐、结算页凑单，显著提升客单价与订单关联度。"),
      ]
    )


def course5():
    return dict(
      idx=5, title="企业员工绩效数据分析",
      subtitle="多表合并、透视表、分组统计，分析部门效能与人员表现",
      level="intermediate", hours="11 小时", rating="4.6",
      tags=["多表融合","透视表","人力数据分析","Pandas 实战"],
      goals="1) 掌握多表合并 (pd.merge) 的基础逻辑\n2) 使用透视表 (pivot_table) 做多维度对比\n3) 对部门、职级等维度做绩效统计与排序\n4) 从数据中识别高/低绩效群体",
      audience="HR 数据分析师、人力 BI、运营数据岗",
      prereq="Pandas 合并与透视表",
      sections=[
        dict(title="① 多表合并", body="""<p>常见 HR 数据分布在多张表：员工表、部门表、绩效表。使用 <code>pd.merge</code> 整合。</p>""",
             code="""import pandas as pd
emp = pd.DataFrame({'emp_id':[1,2,3],'name':['小王','小李','小赵'],'dept':['销售','研发','销售']})
perf = pd.DataFrame({'emp_id':[1,2,3,4],'score':[92,88,75,65]})
merged = pd.merge(emp, perf, on='emp_id', how='left')
print(merged)
"""),
        dict(title="② 按部门聚合", body="""<p>使用 <code>groupby</code> 聚合统计各部门平均分、最高分、人数等。</p>""",
             code="""summary = merged.groupby('dept')['score'].agg(['mean','max','count']).reset_index()
summary.columns = ['部门','平均分','最高分','人数']
print(summary.sort_values('平均分', ascending=False))
"""),
        dict(title="③ 透视表", body="""<p><code>pivot_table</code> 可在行/列上同时做多维统计，方便对多维度交叉分析。</p>""",
             code="""merged['level'] = ['P6','P7','P5','P6']
pt = merged.pivot_table(index='dept', columns='level', values='score', aggfunc='mean', fill_value=0)
print('部门 × 职级 平均绩效透视表:')
print(pt.round(1))
"""),
      ],
      default_code="""import pandas as pd

# ========================================
# 构造：员工表、绩效表
# ========================================
employees = pd.DataFrame({
    'emp_id': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
    'name':   ['小王','小李','小赵','小刘','小陈','小孙','小杨','小周'],
    'dept':   ['销售部','研发部','销售部','研发部','市场部','市场部','销售部','研发部'],
    'level':  ['P6','P7','P5','P6','P5','P6','P7','P5'],
    'city':   ['北京','上海','北京','深圳','上海','上海','北京','深圳'],
})

performance = pd.DataFrame({
    'emp_id': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
    'KPI':    [92, 88, 75, 82, 80, 78, 95, 70],
    'attendance': [98, 95, 88, 92, 95, 90, 96, 85],
    'bonus':  [8000, 7200, 5500, 6400, 6000, 5800, 9000, 5200],
})

# 1) 合并
merged = pd.merge(employees, performance, on='emp_id', how='left')
print('==== 合并后的员工-绩效总表 ====')
print(merged.to_string(index=False))
print()

# 2) 按部门聚合
dept_stat = merged.groupby('dept').agg(
    人数=('emp_id','count'),
    平均分=('KPI','mean'),
    最高分=('KPI','max'),
    平均奖金=('bonus','mean'),
).reset_index().sort_values('平均分', ascending=False)
print('==== 各部门绩效统计 (降序) ====')
print(dept_stat.round(1).to_string(index=False))
print()

# 3) 部门 × 职级 透视
print('==== 部门 × 职级 KPI 均值透视表 ====')
pt = merged.pivot_table(index='dept', columns='level', values='KPI', aggfunc='mean', fill_value=0)
print(pt.round(1).to_string())
print()

# 4) 识别高低绩效群体
mean_kpi = merged['KPI'].mean()
top = merged[merged['KPI'] >= mean_kpi + 5]
low = merged[merged['KPI'] <= mean_kpi - 5]
print(f'整体平均 KPI: {mean_kpi:.1f}')
print(f'🏆 高于均值 +5 的高绩效员工 ({len(top)} 人)：')
print(top[['name','dept','level','KPI']].to_string(index=False))
print(f'\n⚠ 低于均值 -5 的低绩效员工 ({len(low)} 人)：')
print(low[['name','dept','level','KPI']].to_string(index=False))

print('\\n🧭 结论 & 建议：')
print('· 销售部整体表现较好，可推广其管理经验；')
print('· 对低绩效员工开展专项辅导与提升计划；')
print('· P7 职级的 KPI 均值高于 P5，建议分析其能力差异并沉淀培训资料。')
""",
      quiz=[
        dict(q='合并多张表最常用的 Pandas 函数是？',
             options=['pd.concat','pd.merge','pd.pivot_table','df.apply'],
             answer=1, explain='pd.merge 按主键 (on) 将多表连接，类似 SQL JOIN。'),
        dict(q='做"部门平均绩效"统计，最常用的方法是？',
             options=['df.head()','df.groupby("dept")["KPI"].mean()','df.T','df.dropna()'],
             answer=1, explain='groupby(部门) + 聚合函数 (mean/max/count) 是最标准写法。'),
        dict(q='透视表 (pivot_table) 的主要用途是？',
             options=['去除重复数据','做多维度的交叉统计','连接两张表','把数据按时间排序'],
             answer=1, explain='pivot_table 支持在行/列上做多维聚合，快速对比多维度结果。'),
      ],
      thinking="""核心思路：
① 先将多表用 pd.merge 合并成"一张大宽表"；
② 用 groupby + agg 对部门/城市做聚合统计，识别优劣势群体；
③ 用 pivot_table 做多维交叉，如"部门 × 职级"；
④ 对高于/低于均值的员工进行识别，给出管理动作建议。

常见错误：
- 使用 how='inner' 丢失无绩效记录的员工；
- 聚合列命名不一致，导致后续展示混乱；
- pivot_table 的 index/columns/values 三要素搞反。
""",
      summary=[
        dict(title="关键知识点", body="pd.merge、groupby + agg、pivot_table、基于阈值的高/低绩效识别。"),
        dict(title="核心代码", body="pd.merge(employees, perf, on='emp_id', how='left')；groupby('dept').agg(...)；pivot_table(index='dept', columns='level', values='KPI')。"),
        dict(title="业务价值", body="帮助 HR / 管理团队快速识别部门效能差距、高低绩效群体，落地针对性的人才管理动作。"),
      ]
    )


def course6():
    return dict(
      idx=6, title="餐饮门店营收数据分析",
      subtitle="分析菜品销量、时段营收、识别爆款与低效时段",
      level="intermediate", hours="10 小时", rating="4.7",
      tags=["营收统计","餐饮运营","柱状图","分组聚合"],
      goals="1) 按菜品/时段统计营收与销量\n2) 识别爆款菜品、低效菜品\n3) 输出营业时间与运营建议\n4) 用柱状图、折线图做可视化",
      audience="餐饮运营、门店店长、商业数据分析师",
      prereq="Pandas 分组聚合、基础可视化",
      sections=[
        dict(title="① 菜品销量统计", body="""<p>按菜品分组聚合 (sum) 得到销量/营收排名，识别 Top/N。</p>""",
             code="""import pandas as pd
sales = pd.DataFrame({'dish':['麻婆豆腐','宫保鸡丁','麻婆豆腐','鱼香肉丝','宫保鸡丁'],
                      'amount':[28,32,28,35,32]})
print(sales.groupby('dish')['amount'].agg(['count','sum']).sort_values('sum', ascending=False))
"""),
        dict(title="② 时段营收分析", body="""<p>按时段 (lunch / dinner 等) 聚合，比较高低峰营收贡献。</p>""",
             code="""sales['时段'] = ['午餐','午餐','晚餐','晚餐','午餐']
print(sales.groupby('时段')['amount'].sum())
"""),
        dict(title="③ 柱状图可视化", body="""<p>plt.bar 绘制菜品销售柱状图，直观对比各菜品贡献。</p>""",
             code="""import matplotlib.pyplot as plt
dish_stat = sales.groupby('dish')['amount'].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(7,4))
ax.bar(dish_stat.index, dish_stat.values, color='#165DFF')
ax.set_title('菜品销售额'); ax.set_ylabel('金额 (元)')
plt.xticks(rotation=20); plt.tight_layout(); plt.show()
"""),
      ],
      default_code="""import pandas as pd
import matplotlib.pyplot as plt

# ========================================
# 构造：菜品销售明细
# ========================================
sales = pd.DataFrame([
    ('麻婆豆腐', 28, '午餐'), ('宫保鸡丁', 32, '午餐'),
    ('鱼香肉丝', 35, '午餐'), ('麻婆豆腐', 28, '午餐'),
    ('红烧肉', 68, '晚餐'), ('清蒸鲈鱼', 88, '晚餐'),
    ('宫保鸡丁', 32, '晚餐'), ('麻婆豆腐', 28, '晚餐'),
    ('红烧肉', 68, '晚餐'), ('可乐',   8, '午餐'),
    ('米饭',   3, '午餐'), ('米饭',   3, '晚餐'),
    ('凉拌黄瓜', 12, '晚餐'),('清蒸鲈鱼', 88, '晚餐'),
    ('麻婆豆腐', 28, '晚餐'),('鱼香肉丝', 35, '晚餐'),
], columns=['dish','amount','period'])

# 1) 菜品销量排名
dish_stat = sales.groupby('dish').agg(
    销量=('amount','count'),
    营收=('amount','sum'),
).reset_index().sort_values('营收', ascending=False)
print('==== 菜品销售额排名 ====')
print(dish_stat.to_string(index=False))
print()

# 2) 时段营收
period_stat = sales.groupby('period')['amount'].agg(['count','sum']).reset_index()
period_stat.columns = ['时段','单数','总金额']
print('==== 时段销售 ====')
print(period_stat.to_string(index=False))

# 3) 柱状图：菜品销售额
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(dish_stat['dish'], dish_stat['营收'], color=['#165DFF','#0ea5e9','#22c55e','#f59e0b','#ef4444','#a855f7','#64748b','#06b6d4'])
ax.set_title('菜品销售额排名'); ax.set_ylabel('销售额 (元)')
plt.xticks(rotation=25)
plt.tight_layout()
plt.show()

print('\\n🧭 运营建议：')
print('· "清蒸鲈鱼 / 红烧肉" 为高营收菜品，应保障备货与品控；')
print('· "米饭 / 可乐" 作为搭配品，可与主菜设计套餐；')
print('· 晚餐时段贡献较高，可安排更多人手与重点推荐活动；')
print('· 低贡献菜品 (如凉拌黄瓜) 可考虑优化组合或调整价格。')
""",
      quiz=[
        dict(q='识别"爆款菜品"最直观的指标是？',
             options=['菜品名称长度','菜品总销售额 (sum)','下单用户性别','用户年龄'],
             answer=1, explain='销售额 / 销量最高的菜品就是业务视角的爆款。'),
        dict(q='对比"时段营收"最适合的聚合方式是？',
             options=['df.mean()','df.groupby("时段")["amount"].sum()','df.sample()','df.T'],
             answer=1, explain='按时段分组 + 金额 sum，即可得到时段营收贡献。'),
        dict(q='下列哪个动作对提升晚餐时段营收最有帮助？',
             options=['停止营业晚餐','在晚餐推出高毛利套餐与限时活动','把所有菜品涨价 5 倍','不再提供晚餐餐具'],
             answer=1, explain='基于数据分析的合理运营动作：在高峰时段加强菜品推荐与套餐设计。'),
      ],
      thinking="""核心思路：
① 把销售明细按菜品/时段/城市等维度聚合统计；
② 用 sort_values 找出 Top/N；
③ 用柱状图直观对比；
④ 结合业务知识（菜品毛利、成本、备货难度）进行运营决策。

常见错误：
- 只看销量不看金额，导致把高频低价品误判为爆款；
- 绘图时忘记旋转 x 轴标签，导致文字重叠；
- 结论只停留在数字，没有与备货/人效/营销结合。
""",
      summary=[
        dict(title="关键知识点", body="分组聚合、排序、柱状图 (plt.bar)、业务转化建议。"),
        dict(title="核心代码", body="df.groupby('dish').agg(销量=('amount','count'),营收=('amount','sum'))；ax.bar(...)。"),
        dict(title="业务价值", body="帮助门店精准识别爆款/低效菜品，优化菜单结构、备货策略与排班。"),
      ]
    )


def course7():
    return dict(
      idx=7, title="库存销量预测分析（时间序列）",
      subtitle="用简单移动平均/加权移动平均实现销量预测，辅助库存周转",
      level="advanced", hours="16 小时", rating="4.9",
      tags=["时间序列","销量预测","移动平均","库存优化"],
      goals="1) 掌握简单移动平均 / 加权移动平均原理\n2) 用 Python 实现日/周销量预测\n3) 结合实际值与预测值，识别备货风险\n4) 辅助库存周转优化",
      audience="供应链/库存运营/采购数据分析岗",
      prereq="Pandas 时间序列、基础可视化",
      sections=[
        dict(title="① 简单移动平均 (SMA)", body="""<p>SMA(t) = 最近 N 期均值。<code>df['y'].rolling(window=N).mean()</code></p>""",
             code="""import pandas as pd
s = pd.Series([10,12,11,13,15,14,16])
print('SMA(window=3):', list(s.rolling(3).mean().round(2)))
"""),
        dict(title="② 加权移动平均", body="""<p>近期数据权重更高：使用自定义权重 rolling.apply(weighted_mean)。</p>""",
             code="""import numpy as np
weights = np.array([0.1,0.2,0.3,0.4])
def wma(x): return (x * weights).sum()
print('WMA(window=4):', list(s.rolling(4).apply(wma).round(2)))
"""),
        dict(title="③ 对比实际 vs 预测", body="""<p>可视化实际值与预测值折线图，帮助判断模型与业务异常。</p>""",
             code="""import matplotlib.pyplot as plt
df = pd.DataFrame({'actual':[10,12,11,13,15,14,16]})
df['SMA3'] = df['actual'].rolling(3).mean()
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(df.index, df['actual'], marker='o', label='actual', color='#165DFF')
ax.plot(df.index, df['SMA3'],   marker='s', label='SMA3', color='#f59e0b', linestyle='--')
ax.legend(); ax.set_title('实际 vs 简单移动平均'); plt.tight_layout(); plt.show()
"""),
      ],
      default_code="""import pandas as pd
import matplotlib.pyplot as plt

# ========================================
# 构造：某商品过去 14 天的销量
# ========================================
days = pd.date_range(start='2024-09-01', periods=14, freq='D')
sales = pd.Series([120, 135, 125, 140, 155, 150, 170, 180, 175, 190, 200, 210, 205, 220], index=days)
df = sales.reset_index()
df.columns = ['日期','销量']

# 1) 简单移动平均 window=3 / window=7
df['SMA3'] = df['销量'].rolling(3).mean()
df['SMA7'] = df['销量'].rolling(7).mean()

# 2) 加权移动平均（近 4 天权重：0.1/0.2/0.3/0.4）
import numpy as np
weights = np.array([0.1, 0.2, 0.3, 0.4])
def wma(x): return (x * weights).sum()
df['WMA4'] = df['销量'].rolling(4).apply(wma)

# 3) 打印表格
print('==== 实际销量 vs 移动平均预测 ====')
print(df.round(2).to_string(index=False))
print()

# 4) 可视化
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(df['日期'], df['销量'],  marker='o', color='#165DFF', linewidth=2, label='实际销量')
ax.plot(df['日期'], df['SMA3'],  marker='s', color='#f59e0b', linewidth=1.6, label='SMA-3')
ax.plot(df['日期'], df['SMA7'],  marker='^', color='#22c55e', linewidth=1.6, label='SMA-7')
ax.plot(df['日期'], df['WMA4'],  marker='D', color='#a855f7', linewidth=1.6, label='WMA-4')
ax.set_title('销量时间序列 vs 移动平均预测')
ax.set_xlabel('日期'); ax.set_ylabel('销量 (件)')
ax.legend(); ax.grid(alpha=0.3)
plt.xticks(rotation=30); plt.tight_layout(); plt.show()

# 5) 评估 & 决策建议
actual = df['销量'].iloc[7:]
pred   = df['SMA7'].iloc[7:]
mae = (actual - pred).abs().mean()
print(f'🧮 评估: SMA7 在后续 7 天的 MAE ≈ {mae:.2f} 件')
print('🧭 库存建议：')
print('· 以 WMA4 / SMA7 作为下一日销量预测；')
print('· 加上一定安全库存 (如 1.3×预测值) 进行补货；')
print('· 当实际销量持续高于预测时，应提高安全库存水位；')
print('· 当实际销量持续低于预测时，应启动库存清理与促销。')
""",
      quiz=[
        dict(q='简单移动平均 (SMA) 的主要用途是？',
             options=['生成随机数','对时间序列平滑并预测近期趋势','删除缺失值','合并多张表'],
             answer=1, explain='移动平均通过取最近 N 期均值来平滑噪声并做简单预测。'),
        dict(q='对 SMA 说法正确的是？',
             options=['window 越大越灵敏','window 越小越平滑','window 越小越灵敏，window 越大越平滑','窗口大小对平滑度无影响'],
             answer=2, explain='窗口越小越跟随近期波动（灵敏），窗口越大越平滑，但也越滞后。'),
        dict(q='评估预测效果常用的指标 MAE 指？',
             options=['最大绝对误差','平均绝对误差 (mean(|actual-pred|))','最大百分比误差','和'],
             answer=1, explain='MAE = mean(|实际-预测|)，越接近 0 预测越准。'),
      ],
      thinking="""核心思路：
① 把历史销量按时间排序，构造时间序列；
② 用 rolling(window=N).mean() 得简单移动平均；
③ 用自定义权重做加权移动平均 (近期权重更高)；
④ 画图比较不同方法的预测效果，并用 MAE 量化；
⑤ 结合业务规则给出库存建议与促销动作。

常见错误：
- 时间序列未按日期排序导致 rolling 错位；
- window 选择过小/过大，导致过度抖动或过于平滑；
- 未考虑节假日/促销等业务事件的强影响因子。
""",
      summary=[
        dict(title="关键知识点", body="移动平均、rolling.mean / rolling.apply、折线图、MAE 评估、库存转化建议。"),
        dict(title="核心代码", body="df['col'].rolling(3).mean()；自定义加权函数 rolling.apply(wma)；plt.plot() 对比。"),
        dict(title="业务价值", body="帮助采购/仓储优化补货节奏，降低断货与积压风险，提升库存周转。"),
      ]
    )


def course8():
    return dict(
      idx=8, title="金融信贷风险评估分析",
      subtitle="数据清洗、缺失值处理、风控特征构造，掌握风控建模基础",
      level="advanced", hours="18 小时", rating="4.8",
      tags=["特征工程","风控分析","缺失值处理","分类模型"],
      goals="1) 掌握信贷数据的常见清洗方法\n2) 学会缺失值识别与处理\n3) 构造简单但有效的风险特征\n4) 使用逻辑回归做基础分类模型",
      audience="风控建模、金融数据分析、数据科学岗",
      prereq="Pandas 数据清洗、Sklearn 基础",
      sections=[
        dict(title="① 缺失值处理", body="""<p>风控数据常有缺失，统计每列缺失率，按业务填充或标记。</p>""",
             code="""import pandas as pd, numpy as np
data = pd.DataFrame({'age':[25,30,np.nan,40,28],'income':[10,12,8,np.nan,11],'default':[0,0,1,1,0]})
print('缺失率:\\n', data.isna().mean().round(3))
data_filled = data.fillna(data.median(numeric_only=True))
print('填充后:\\n', data_filled)
"""),
        dict(title="② 简单特征构造", body="""<p>对收入分箱、年龄段分档、交叉特征。</p>""",
             code="""data_filled['income_bin'] = pd.cut(data_filled['income'], bins=3, labels=['low','mid','high'])
print(data_filled)
"""),
        dict(title="③ 逻辑回归基础", body="""<p>使用 sklearn 训练简单分类模型，输出预测概率。</p>""",
             code="""from sklearn.linear_model import LogisticRegression
X = data_filled[['age','income']]
y = data_filled['default']
model = LogisticRegression().fit(X, y)
print('预测概率 (违约=1):', model.predict_proba(X)[:,1].round(3))
"""),
      ],
      default_code="""import pandas as pd
import numpy as np

# ========================================
# 构造：模拟的借款人特征表
# ========================================
np.random.seed(42)
n = 300
data = pd.DataFrame({
    'age':      np.random.choice([25,30,35,40,45,50,np.nan], n, p=[0.15,0.2,0.2,0.15,0.1,0.1,0.1]),
    'income':   np.random.choice([8,10,12,15,20,25,30,np.nan], n, p=[0.1,0.15,0.15,0.2,0.15,0.1,0.05,0.1]),
    'loan':     np.random.choice([5,10,15,20,30,50,80], n),
    'duration': np.random.choice([12,24,36,48,60], n),
    'default':  np.random.choice([0,1], n, p=[0.8, 0.2]),
})

print('==== 数据概览 ====')
print('总行数:', len(data))
print('每列缺失率:')
print((data.isna().mean() * 100).round(2).to_string())
print()

# 1) 缺失值处理：数值用中位数
filled = data.copy()
for col in ['age','income']:
    median = filled[col].median()
    filled[col] = filled[col].fillna(median)
    filled[f'{col}_ismissing'] = data[col].isna().astype(int)  # 是否缺失作为额外特征

# 2) 特征工程
filled['income_per_age'] = filled['income'] / filled['age']
filled['loan_income_ratio'] = filled['loan'] / filled['income'].replace(0, np.nan)
filled['loan_income_ratio'] = filled['loan_income_ratio'].fillna(filled['loan_income_ratio'].median())

print('==== 特征表样例 (前 5 行) ====')
print(filled.head().round(2).to_string(index=False))
print()

# 3) 关键群体统计
by_default = filled.groupby('default').agg(
    人数=('age','count'),
    平均年龄=('age','mean'),
    平均收入=('income','mean'),
    平均贷款额=('loan','mean'),
).reset_index()
by_default.columns = ['是否违约','人数','平均年龄','平均收入','平均贷款额']
print('==== 违约 vs 非违约群体对比 ====')
print(by_default.round(1).to_string(index=False))
print()

# 4) 阈值规则：高负债收入比 -> 潜在高风险
ratio_q80 = filled['loan_income_ratio'].quantile(0.8)
high_risk = filled[filled['loan_income_ratio'] >= ratio_q80]
print(f'⚠ Top 20% 高负债收入比客户数 = {len(high_risk)}，违约率 = {high_risk["default"].mean():.1%}')

print('\\n🧭 风控结论（示例）：')
print('· 缺失值处理：数值字段以中位数填充，同时保留"是否缺失"特征；')
print('· 负债收入比是核心风险信号，Top 20% 人群需重点审核；')
print('· 可进一步训练逻辑回归 / GBDT 模型做概率评分与额度策略。')
""",
      quiz=[
        dict(q='数值字段缺失时，最稳妥的填充方式是？',
             options=['填 0','填均值/中位数','填列最大值','随机填'],
             answer=1, explain='均值/中位数对异常值更稳健，适合作为缺失值的第一处理方式。'),
        dict(q='下列哪个特征最能代表借款人"还款压力"？',
             options=['年龄','贷款额/月收入 (负债收入比)','贷款期限','随机列'],
             answer=1, explain='负债收入比 (贷款额/收入) 是衡量还款压力的核心指标。'),
        dict(q='建模前对数值特征做"分箱"的主要目的是？',
             options=['让模型更慢','引入非线性/增强可解释性、提升鲁棒性','仅为了画图','给数据加噪声'],
             answer=1, explain='分箱 (pd.cut / qcut) 把非线性关系拆成分段，提升模型可解释性与鲁棒性。'),
      ],
      thinking="""核心思路：
① 快速统计每列缺失率 -> 制定填充策略；
② 构造交叉特征 (负债收入比、收入/年龄) 捕捉非线性关系；
③ 分组对比违约/非违约用户差异；
④ 利用阈值规则初步识别高风险人群，为后续模型铺垫。

常见错误：
- 对 0 值做除法分母时报错 (需 replace 0 为 NaN 再填充)；
- 盲目填充 0 代替缺失值，会严重误导模型；
- 不做业务上的特征验证，纯依赖自动化模型。
""",
      summary=[
        dict(title="关键知识点", body="缺失值统计与处理、特征工程 (比值特征、缺失标记特征)、分组对比、阈值规则。"),
        dict(title="核心代码", body="df.isna().mean()；df.fillna(median)；df['loan']/df['income']；groupby + agg；分位数阈值。"),
        dict(title="业务价值", body="支撑风控审核、授信额度与定价策略，降低坏账率，提升信贷组合稳定性。"),
      ]
    )


def course9():
    return dict(
      idx=9, title="平台用户流失预测分析",
      subtitle="挖掘用户行为轨迹，构造流失特征，训练简单预测模型",
      level="advanced", hours="17 小时", rating="4.7",
      tags=["流失预测","行为建模","特征工程","机器学习"],
      goals="1) 理解流失定义与观察/表现窗口\n2) 从原始行为日志中构造用户级特征\n3) 训练基础分类模型并评估\n4) 总结流失核心原因与召回策略",
      audience="互联网运营、用户增长、数据科学岗",
      prereq="Pandas 特征工程、sklearn 训练/测试划分",
      sections=[
        dict(title="① 流失定义", body="""<p>常见：观察期无登录/付费行为即视为流失。需要明确"观察窗口 / 表现窗口"。</p>""",
             code="""import pandas as pd
users = pd.DataFrame({'user':['u1','u2','u3'],'last_login_days_ago':[2,60,180]})
users['churn'] = users['last_login_days_ago'] >= 30
print(users)
"""),
        dict(title="② 构造行为特征", body="""<p>从日志中构造：近 30 天活跃天数、近 30 天消费次数、平均消费金额等。</p>""",
             code="""features = pd.DataFrame({
    'user':['u1','u2','u3','u4'],
    'active_days_30':[25,12,5,0],
    'pay_count_30':[5,2,0,0],
    'pay_total_30':[500,180,0,0],
})
print(features)
"""),
        dict(title="③ 训练/测试拆分与评估", body="""<p><code>train_test_split</code> 拆分后，用 <code>LogisticRegression</code> 训练，AUC 评估。</p>""",
             code="""from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import numpy as np
X = np.array([[25,5,500],[12,2,180],[5,0,0],[0,0,0],[30,8,800],[10,1,60],[6,0,0],[2,0,0]])
y = np.array([0,0,1,1,0,0,1,1])
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=0)
model = LogisticRegression().fit(Xtr, ytr)
prob = model.predict_proba(Xte)[:,1]
print(f'Test AUC = {roc_auc_score(yte, prob):.3f}')
"""),
      ],
      default_code="""import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report

# ========================================
# 构造：用户行为特征 + 流失标签
# ========================================
np.random.seed(0)
n = 200
data = pd.DataFrame({
    'active_days_30': np.random.randint(0, 31, n),
    'pay_count_30':   np.random.randint(0, 10, n),
    'pay_total_30':   np.random.randint(0, 2000, n),
    'session_duration_min': np.random.randint(1, 120, n),
})
# 生成标签：越不活跃、越少付费 -> 流失概率越高
churn_score = -0.6 * data['active_days_30'] - 0.8 * data['pay_count_30'] - 0.002 * data['pay_total_30'] + 15
noise = np.random.randn(n) * 3
data['churn'] = ((churn_score + noise) > 10).astype(int)

print('==== 数据总览 ====')
print('样本数:', len(data))
print('流失用户数:', data['churn'].sum())
print('流失率:', f"{data['churn'].mean():.1%}")
print()

# 1) 特征 vs 流失对比
print('==== 流失 vs 非流失用户特征均值对比 ====')
cmp = data.groupby('churn').agg(
    平均活跃天数=('active_days_30','mean'),
    平均付费次数=('pay_count_30','mean'),
    平均付费金额=('pay_total_30','mean'),
    平均会话时长=('session_duration_min','mean'),
).reset_index()
cmp.columns = ['流失','平均活跃天数','平均付费次数','平均付费金额','平均会话时长(分钟)']
print(cmp.round(1).to_string(index=False))
print()

# 2) 训练/测试拆分
features = ['active_days_30','pay_count_30','pay_total_30','session_duration_min']
X = data[features].values
y = data['churn'].values
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

# 3) 模型训练
model = LogisticRegression(max_iter=500).fit(Xtr, ytr)
prob = model.predict_proba(Xte)[:, 1]
pred = (prob >= 0.5).astype(int)

print(f'🧮 Test AUC = {roc_auc_score(yte, prob):.3f}')
print('🧮 分类报告:\n', classification_report(yte, pred, zero_division=0))

# 4) 特征系数解读（正系数越高越易流失）
coef_df = pd.DataFrame({'feature': features, 'coef': model.coef_[0]}).sort_values('coef', ascending=False)
print('🧮 模型系数 (正为增加流失风险):')
print(coef_df.round(3).to_string(index=False))

# 5) 策略建议
print('\\n🧭 策略建议：')
print('· 活跃天数低、付费次数少的用户为高风险人群，优先推送召回券；')
print('· 会话时长过低的用户，可优化产品引导与新手体验；')
print('· 对预测流失概率高的用户，做定向 A/B 召回实验。')
""",
      quiz=[
        dict(q='下列哪种说法最能定义"流失用户"？',
             options=['注册时间最早的用户','过去 30 天没有登录或核心行为的用户','最近一次购买金额过低','VIP 用户'],
             answer=1, explain='流失定义必须基于明确观察窗口，如"过去 30 天未登录/未下单"。'),
        dict(q='以下哪个特征最能反映用户活跃程度？',
             options=['用户昵称长度','近 30 天活跃天数','注册时间','员工 ID'],
             answer=1, explain='近 30 天活跃天数是衡量活跃程度的强特征。'),
        dict(q='训练分类模型后，下列哪项最重要？',
             options=['查看特征系数/特征重要性并做业务解读','把模型文件打包保存','立即上线','删除特征'],
             answer=0, explain='模型输出背后的"业务可解释性"是落地关键，系数/重要性排序能指导后续运营动作。'),
      ],
      thinking="""核心思路：
① 先以业务视角明确"流失标签"定义 (观察窗口)；
② 从日志中抽取窗口内关键行为特征 (活跃、付费、时长等)；
③ 训练简单分类模型 (LR/GBDT)；
④ 用 AUC/报告评估模型，并结合系数解读驱动运营动作。

常见错误：
- 标签窗口与特征窗口相互泄漏，导致模型虚假高 AUC；
- 特征工程不充分，只用"总次数"而没有"最近 N 天"等时间窗口特征；
- 只输出模型，没有把结论转化为可落地的运营策略。
""",
      summary=[
        dict(title="关键知识点", body="流失定义、行为特征 (活跃/付费/时长)、LR 训练、AUC 评估、模型系数解读。"),
        dict(title="核心代码", body="train_test_split；LogisticRegression；predict_proba；roc_auc_score；coef_ 输出。"),
        dict(title="业务价值", body="驱动召回运营、提升留存率、优化新用户引导、识别核心价值用户保护策略。"),
      ]
    )


def course10():
    return dict(
      idx=10, title="A/B 测试数据分析",
      subtitle="设计 A/B 实验、校验数据、计算转化率与显著性检验",
      level="advanced", hours="12 小时", rating="4.8",
      tags=["A/B 测试","假设检验","转化率","显著性检验"],
      goals="1) 理解 A/B 测试的基本设计要点\n2) 学会转化率对比与显著性检验\n3) 掌握实验数据校验 (样本量、均衡性)\n4) 输出实验结论与上线建议",
      audience="产品经理、数据分析师、增长运营",
      prereq="基础统计学、Pandas 数据筛选",
      sections=[
        dict(title="① 实验设计要点", body="""<ul class="list-disc list-inside space-y-1 text-sm text-gray-700">
             <li>单一变量：两组只改一个维度</li>
             <li>随机分流：保证样本可比</li>
             <li>充足样本量：避免过早偷看</li>
             </ul>""",
             code="""n_users = 10000
conv_a, conv_b = 520, 590
rate_a, rate_b = conv_a/n_users, conv_b/n_users
print(f'对照组转化率: {rate_a:.2%}, 实验组转化率: {rate_b:.2%}')
print(f'提升率: {(rate_b/rate_a-1):.2%}')
"""),
        dict(title="② 两比例 Z 检验", body="""<p>合并转化率 <code>p_pool</code> 用于计算标准误；Z = (rate_b-rate_a)/se。</p>""",
             code="""from math import sqrt
p_pool = (conv_a+conv_b)/(2*n_users)
se = sqrt(p_pool*(1-p_pool)*(1/n_users + 1/n_users))
z = (rate_b - rate_a) / se
print(f'Z = {z:.3f}')
"""),
        dict(title="③ p 值 & 结论", body="""<p>双侧 p 值，若 p<0.05 则差异显著；结合提升率置信区间给出业务建议。</p>""",
             code="""from math import erf
phi = lambda z: 0.5*(1+erf(z/sqrt(2)))
p_val = 2*(1 - phi(abs(z)))
print(f'p = {p_val:.4f}', '=> 差异显著 🟢' if p_val<0.05 else '=> 差异不显著 🟡')
"""),
      ],
      default_code="""from math import sqrt, erf
import pandas as pd

# ========================================
# 假设：某次按钮改版 A/B 实验
# ========================================
experiment = pd.DataFrame({
    'group':   ['control','experiment'],
    'users':   [10000, 10000],
    'convert': [520,   590],
})
experiment['rate'] = experiment['convert'] / experiment['users']
print('==== 分组数据 ====')
print(experiment.to_string(index=False))
print()

# 1) 关键指标
rate_a, rate_b = experiment['rate'].values
total_a, total_b = experiment['users'].values
conv_a, conv_b = experiment['convert'].values
uplift = (rate_b / rate_a - 1)
print(f'对照组转化率 = {rate_a:.2%}，实验组转化率 = {rate_b:.2%}')
print(f'相对提升率 = {uplift:.2%}')
print()

# 2) 两比例 Z 检验
p_pool = (conv_a + conv_b) / (total_a + total_b)
se = sqrt(p_pool * (1 - p_pool) * (1/total_a + 1/total_b))
z = (rate_b - rate_a) / se
phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))
p_val = 2 * (1 - phi(abs(z)))
print(f'Z 统计量 = {z:.3f}')
print(f'p 值     = {p_val:.4f}')
print()

# 3) 95% 置信区间
se_diff = sqrt(rate_b*(1-rate_b)/total_b + rate_a*(1-rate_a)/total_a)
diff = rate_b - rate_a
ci = (diff - 1.96*se_diff, diff + 1.96*se_diff)
print(f'提升率绝对差 = {diff:.2%}')
print(f'95% CI = [{ci[0]:.2%}, {ci[1]:.2%}]')
print()

# 4) 结论
if p_val < 0.05 and ci[0] > 0:
    verdict = '✅ 差异显著且正向：建议实验组方案全量上线，并持续观察核心指标'
elif p_val < 0.05 and ci[1] < 0:
    verdict = '❌ 差异显著且负向：建议保留对照组方案并复盘实验假设'
else:
    verdict = '⚠ 差异不显著：建议延长实验或加大样本量后再决策'

print('==== 实验结论 ====')
print(verdict)
print('\\n🧭 建议：')
print('· 实验结论仅在样本量、分流随机、观测周期合理的前提下成立；')
print('· 若效果显著，还需同时观察对次要指标 (如客单价、退款率) 的影响；')
print('· 建议做 1-2 周的灰度/全量上线验证，再做最终决策。')
""",
      quiz=[
        dict(q='A/B 测试中 "p 值 < 0.05" 最常表示？',
             options=['实验组一定赚钱','两组差异在统计上显著','转化率必高于 5%','样本量不足'],
             answer=1, explain='p<0.05 说明在"两组相同"的原假设下出现当前数据的概率小于 5%，差异显著。'),
        dict(q='下列哪种做法是错误的？',
             options=['保证单变量改动','随机分配流量','实验中多次偷看并提前停止实验','使用相同的统计口径'],
             answer=2, explain='多次偷看/提前停止会破坏显著性检验，导致"钓鱼 p 值"。'),
        dict(q='95% 置信区间全为正数说明？',
             options=['实验组效果显著差于对照组','实验组效果显著优于对照组','两组相同','无意义'],
             answer=1, explain='CI 下限 > 0 说明提升率在 95% 的信心下大于 0，实验方案显著更优。'),
      ],
      thinking="""核心思路：
① 检查实验数据是否满足基本假设 (随机、样本量、数据口径一致)；
② 计算两组的转化率与相对提升率；
③ 使用两比例 Z 检验计算 Z 与 p 值；
④ 给出提升率的 95% 置信区间；
⑤ 结合统计结论与业务背景，输出是否上线/复盘实验。

常见错误：
- 忽视样本量直接看转化率差异；
- 对低基数指标强行解读显著性；
- 把"统计显著"等同于"业务有价值"，忽略 ROI 考量。
""",
      summary=[
        dict(title="关键知识点", body="两比例 Z 检验、p 值、95% 置信区间、显著性解读、实验设计。"),
        dict(title="核心代码", body="p_pool / se / Z；用 erf 近似正态分布；diff ± 1.96*se 得到 CI。"),
        dict(title="业务价值", body="帮助产品/运营用数据科学方式做改版决策，避免拍脑袋，提高迭代效率与收益。"),
      ]
    )


def build_course(course_data):
    # 构造一节 HTML (知识点)
    num = course_data['idx']
    title = course_data['title']
    sub = course_data['subtitle']
    level = course_data['level']
    hours = course_data['hours']
    rating = course_data['rating']
    tags_html = "".join([f'<span class="bg-brand-50 text-brand-700 text-xs px-2 py-1 rounded">{t}</span>' for t in course_data['tags']])
    level_tag_map = {'beginner':'初级','intermediate':'中级','advanced':'高级'}
    level_cn = level_tag_map.get(level, '中级')
    # level badge color
    level_badge = f'<span class="text-xs font-bold px-2 py-1 rounded-full tag-{level}">{level_cn}</span>'

    sections_html_parts = []
    for idx, section in enumerate(course_data['sections'], 1):
        body = section['body']
        code = section['code']
        parts = []
        if body: parts.append(f'<div class="text-sm text-gray-700 leading-7">{body}</div>')
        if code: parts.append(f'<pre class="code-snippet mt-3"><code>{code}</code></pre>')
        sections_html_parts.append(f'''
        <details class="border border-gray-200 rounded-xl bg-gray-50/60" open>
            <summary class="px-4 py-3 font-semibold text-gray-800 cursor-pointer list-none flex items-center justify-between">
                <span>{section["title"]}</span>
                <span class="caret text-brand-500">▶</span>
            </summary>
            <div class="px-4 pb-4 pt-2 space-y-2">{"".join(parts)}</div>
        </details>''')
    sections_html = "\n".join(sections_html_parts)

    quiz_questions_html = []
    for q_idx, q in enumerate(course_data['quiz'], 1):
        options_html = "".join([
            f'<label class="flex items-start cursor-pointer py-2 px-3 rounded-lg hover:bg-brand-50/60 hover:border-brand-200 border border-gray-200 transition" data-q-idx="{q_idx-1}" data-opt-idx="{i}"><input type="radio" name="q{q_idx-1}" value="{i}" class="mt-1 mr-3"><div><span class="font-semibold">{chr(65+i)}.</span> {opt}</div></label>'
            for i, opt in enumerate(q['options'])
        ])
        quiz_questions_html.append(f'''
        <div class="border border-gray-100 rounded-xl p-4 md:p-5 bg-white">
            <div class="font-semibold text-gray-800 mb-3">Q{q_idx}. {q['q']}</div>
            <div class="space-y-2">{options_html}</div>
            <div id="qresult_{q_idx-1}" class="mt-3 text-sm hidden"></div>
        </div>''')
    quiz_html = "\n".join(quiz_questions_html)

    # 参考答案与解析
    answer_quiz_html = []
    for q_idx, q in enumerate(course_data['quiz'], 1):
        answer_letter = chr(65 + q['answer'])
        answer_quiz_html.append(f'''
        <div class="border border-gray-100 rounded-xl p-4 bg-gray-50/60">
            <div class="font-semibold text-gray-800 mb-2">Q{q_idx}. {q['q']}</div>
            <div class="text-sm text-gray-700 leading-7">
                正确答案：<b class="text-brand-500">{answer_letter}</b>（{q['options'][q['answer']]}）<br>
                {q['explain']}
            </div>
        </div>''')
    answer_quiz_html_str = "\n".join(answer_quiz_html)

    summary_parts_html = "".join([
        f'<div class="border border-gray-100 rounded-xl p-5 bg-gradient-to-br from-brand-50/60 to-white hover-lift"><div class="text-xs font-bold text-brand-500 mb-2">要点 {i+1}</div><div class="text-base font-bold text-gray-900 mb-1">{s["title"]}</div><div class="text-sm text-gray-600 leading-7">{s["body"]}</div></div>'
        for i, s in enumerate(course_data['summary'])])

    # 难度样式
    if level == 'beginner':
        level_class, level_color = 'tag-beginner', 'text-green-700 bg-green-50'
    elif level == 'advanced':
        level_class, level_color = 'tag-advanced', 'text-violet-700 bg-violet-50'
    else:
        level_class, level_color = 'tag-intermediate', 'text-brand-700 bg-brand-50'

    hero = f'''
    <div class="bg-gradient-to-br from-brand-500 to-brand-700 text-white rounded-3xl p-7 md:p-10 shadow-soft relative overflow-hidden">
        <div class="absolute -top-10 -right-10 w-56 h-56 bg-white/10 rounded-full"></div>
        <div class="absolute -bottom-16 -left-16 w-64 h-64 bg-white/10 rounded-full"></div>
        <div class="relative">
          <div class="flex flex-wrap items-center gap-2 mb-4 text-xs">
            <span class="bg-white/20 px-3 py-1 rounded-full font-semibold">课程 {num} / 10</span>
            <span class="{level_color} px-3 py-1 rounded-full font-semibold">{level_cn}</span>
            <span class="bg-white/20 px-3 py-1 rounded-full">⏱ {hours}</span>
            <span class="bg-white/20 px-3 py-1 rounded-full star">★ {rating}</span>
          </div>
          <h1 class="text-2xl md:text-4xl font-extrabold mb-3 leading-tight">{title}</h1>
          <p class="text-brand-50/90 text-base md:text-lg leading-relaxed max-w-3xl">{sub}</p>
          <div class="grid md:grid-cols-3 gap-3 md:gap-4 mt-6">
            <div class="bg-white/10 rounded-xl p-4"><div class="text-xs text-brand-100 mb-1">🎯 学习目标</div><div class="text-sm leading-6 whitespace-pre-line">{course_data['goals']}</div></div>
            <div class="bg-white/10 rounded-xl p-4"><div class="text-xs text-brand-100 mb-1">👥 适合人群</div><div class="text-sm leading-6">{course_data['audience']}</div></div>
            <div class="bg-white/10 rounded-xl p-4"><div class="text-xs text-brand-100 mb-1">📖 前置知识</div><div class="text-sm leading-6">{course_data['prereq']}</div></div>
          </div>
          <div class="flex flex-wrap gap-2 mt-5">{tags_html}</div>
        </div>
    </div>
    '''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} | DataLearn</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {{ theme: {{ extend: {{ colors: {{ brand: {{ 50:"#EEF4FF", 100:"#DBE8FF", 200:"#B8D1FF", 500:"#165DFF", 600:"#0E4BDB", 700:"#0A39A8" }} }}}} }}
</script>
<style>
body {{ font-family:"PingFang SC","Microsoft YaHei",sans-serif; }}
.code-snippet {{ background:#0f172a; color:#e2e8f0; border-radius:.6rem; padding:.9rem 1rem; font-size:13px; line-height:1.6; font-family:"JetBrains Mono","Monaco",monospace; overflow:auto; border:1px solid #1e293b; white-space:pre; }}
.code-editor {{ font-family:"JetBrains Mono","Monaco",monospace; font-size:14px; line-height:1.65; background:#0f172a; color:#e2e8f0; border:1px solid #1e293b; border-radius:.75rem; padding:1rem 1.25rem; width:100%; min-height:280px; resize:vertical; white-space:pre; outline:none; }}
.code-editor:focus {{ border-color:#165DFF; box-shadow:0 0 0 3px rgba(22,93,255,.2); }}
.output-box {{ background:#020617; color:#e2e8f0; font-family:"JetBrains Mono","Monaco",monospace; font-size:13px; line-height:1.7; padding:1rem 1.25rem; border-radius:.75rem; min-height:120px; white-space:pre-wrap; border:1px solid #1e293b; max-height:520px; overflow:auto; }}
.out-err {{ color:#fca5a5; }}
.out-info {{ color:#93c5fd; }}
.out-ok {{ color:#86efac; }}
details summary {{ cursor:pointer; list-style:none; }}
details summary::-webkit-details-marker {{ display:none; }}
details[open] .caret {{ transform: rotate(90deg); }}
.caret {{ transition: transform .2s ease; display:inline-block; }}
.hover-lift {{ transition: transform .25s ease, box-shadow .25s ease; }}
.hover-lift:hover {{ transform: translateY(-2px); box-shadow: 0 8px 24px rgba(22,93,255,.12); }}
.choice-item {{ border:1px solid #e5e7eb; border-radius:.75rem; padding:.85rem 1rem; cursor:pointer; transition:all .15s ease; background:#f8fafc; display:flex; align-items:flex-start; gap:.75rem; }}
.choice-item:hover {{ border-color:#165DFF; background:#EEF4FF; }}
.choice-item.selected {{ border-color:#165DFF; background:#EEF4FF; }}
.choice-item.correct {{ border-color:#10b981; background:#ecfdf5; }}
.choice-item.wrong {{ border-color:#ef4444; background:#fef2f2; }}
</style>
</head>
<body class="bg-gray-50 text-gray-800 antialiased">

<nav class="bg-white/95 backdrop-blur border-b border-gray-100 sticky top-0 z-40">
  <div class="max-w-6xl mx-auto px-4 md:px-6 py-3 flex items-center justify-between">
    <a href="index.html" class="flex items-center gap-2 font-bold text-brand-500">
      <span class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-brand-500 text-white text-sm">D</span>
      <span class="hidden sm:inline">DataLearn</span>
    </a>
    <div class="hidden md:flex items-center gap-6 text-sm text-gray-600">
      <a href="index.html#courses" class="hover:text-brand-500 transition">全部课程</a>
      <a href="index.html#path" class="hover:text-brand-500 transition">学习路径</a>
      <a href="index.html#stack" class="hover:text-brand-500 transition">技术栈</a>
    </div>
    <a href="index.html" class="text-sm bg-brand-500 hover:bg-brand-600 text-white px-4 py-2 rounded-lg font-semibold inline-flex items-center gap-1">← 返回首页</a>
  </div>
</nav>

<main class="max-w-6xl mx-auto px-4 md:px-6 mt-8 space-y-6 pb-16">

  {hero}

  <section class="bg-white rounded-2xl shadow-soft border border-gray-100 p-6 md:p-8">
    <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-4">📖 课程核心知识点</h2>
    <div class="space-y-3">{sections_html}</div>
  </section>

  <section class="bg-white rounded-2xl shadow-soft border border-gray-100 p-6 md:p-8">
    <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-4">💻 在线代码练习</h2>
    <p class="text-sm text-gray-500 mb-5">基于 PyScript，代码在浏览器本地直接执行。可自由修改代码，点击"运行代码"查看结果。首次加载约 5-15 秒。</p>
    <div class="grid lg:grid-cols-2 gap-5">
      <div>
        <div class="flex items-center justify-between mb-2"><div class="text-sm font-semibold text-gray-700">📝 代码编辑器</div><span class="text-xs text-gray-400" id="env-status">环境加载中</span></div>
        <textarea id="code-editor" class="code-editor" spellcheck="false"></textarea>
        <div class="flex flex-wrap gap-2 mt-3">
          <button id="btn-run" class="px-5 py-2.5 bg-brand-500 hover:bg-brand-600 text-white text-sm font-semibold rounded-lg shadow hover-lift inline-flex items-center gap-1">▶ 运行代码</button>
          <button id="btn-reset" class="px-5 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-semibold rounded-lg inline-flex items-center gap-1">↺ 重置示例</button>
          <button id="btn-copy" class="px-5 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-semibold rounded-lg inline-flex items-center gap-1">📋 复制代码</button>
        </div>
        <div class="text-xs text-gray-400 mt-2 leading-6">提示：可自由修改练习；若使用 matplotlib，图形将在右侧输出区渲染。</div>
      </div>
      <div>
        <div class="flex items-center justify-between mb-2"><div class="text-sm font-semibold text-gray-700">🖥 运行结果</div><button id="btn-clear-out" class="text-xs text-gray-400 hover:text-gray-700">清空</button></div>
        <div id="output-area" class="output-box"></div>
      </div>
    </div>
  </section>

  <section class="bg-white rounded-2xl shadow-soft border border-gray-100 p-6 md:p-8">
    <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-4">📝 课程小测</h2>
    <p class="text-sm text-gray-500 mb-5">3 道单选，完成后点击"提交答案"查看得分与解析。</p>
    <div id="quiz-box" class="space-y-5">{quiz_html}</div>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mt-6 pt-5 border-t border-gray-100 gap-3">
      <div id="quiz-total" class="text-sm text-gray-700"></div>
      <div class="flex gap-2">
        <button id="btn-quiz-reset" class="px-5 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-semibold rounded-lg">↺ 重新作答</button>
        <button id="btn-quiz" class="px-5 py-2.5 bg-brand-500 hover:bg-brand-600 text-white text-sm font-semibold rounded-lg shadow hover-lift">✓ 提交答案</button>
      </div>
    </div>
  </section>

  <section class="bg-white rounded-2xl shadow-soft border border-gray-100 p-6 md:p-8">
    <details>
      <summary class="flex items-center justify-between list-none cursor-pointer">
        <h2 class="text-xl md:text-2xl font-bold text-gray-900">💡 参考答案与解析</h2>
        <span class="text-brand-500 text-sm font-semibold"><span class="caret">▶</span> 点击展开</span>
      </summary>
      <div class="mt-6 space-y-6">
        <div><h3 class="text-lg font-bold text-gray-900 mb-3">📘 选择题答案与详解</h3><div class="space-y-3">{answer_quiz_html_str}</div></div>
        <div>
          <div class="flex items-center justify-between mb-3"><h3 class="text-lg font-bold text-gray-900">💻 编程练习参考代码</h3><button id="btn-copy-ref" class="text-sm px-4 py-1.5 bg-brand-50 text-brand-700 hover:bg-brand-100 rounded-lg font-semibold">📋 一键复制</button></div>
          <pre id="answer-code" class="code-snippet"></pre>
          <p class="text-xs text-gray-400 mt-2">可将上述代码复制到上方编辑器后，点击"运行代码"观察结果。</p>
        </div>
        <div><h3 class="text-lg font-bold text-gray-900 mb-3">🧭 核心思路与常见错误</h3><pre id="answer-thinking" class="code-snippet" style="background:#f8fafc;color:#334155;border:1px solid #e5e7eb;"></pre></div>
      </div>
    </details>
  </section>

  <section class="bg-white rounded-2xl shadow-soft border border-gray-100 p-6 md:p-8">
    <h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-4">📌 学习总结</h2>
    <div class="grid md:grid-cols-3 gap-4">{summary_parts_html}</div>
    <p class="text-sm text-gray-500 mt-5 leading-7">💡 学习建议：先理解核心知识点 → 在代码编辑器中反复修改示例 → 完成小测并对照解析 → 返回首页继续下一门课程。</p>
  </section>
</main>

<footer class="bg-white border-t border-gray-100">
  <div class="max-w-6xl mx-auto px-6 py-6 text-center text-xs text-gray-400">© 2026 DataLearn · 商务数据分析与应用 Python 学习平台 · Powered by PyScript (Pyodide)</div>
</footer>

<script>
const COURSE = {{
  num: {num},
  title: {repr(title)},
  defaultCode: {repr(course_data['default_code'])},
  quiz: {repr(course_data['quiz'])},
  thinking: {repr(course_data['thinking'])}
}};

const $ = (id) => document.getElementById(id);

// ------------------- 输出区辅助 -------------------
function appendOut(text, cls='') {{
  const out = $('output-area');
  const span = document.createElement('span');
  span.textContent = text;
  if (cls) span.className = cls;
  out.appendChild(span);
  out.scrollTop = out.scrollHeight;
}}
function clearOut() {{ $('output-area').innerHTML = ''; }}

// ------------------- PyScript 环境 -------------------
let pyReady = false;
async function ensurePyodide() {{
  for (let tries=0; tries<120; tries++) {{
    try {{
      if (window.pyscript && window.pyscript.interpreter) {{
        const py = window.pyscript.interpreter.globals.get('pyodide');
        if (py) {{ pyReady = true; $('env-status').textContent = '✓ Python 环境就绪'; $('env-status').classList.add('out-ok'); return py; }}
      }}
    }} catch (e) {{}}
    await new Promise(r => setTimeout(r, 500));
  }}
  throw new Error('Pyodide 加载超时，请检查网络或刷新页面重试。');
}}

// ------------------- 运行代码 -------------------
async function runCode() {{
  const btn = $('btn-run');
  const code = $('code-editor').value.trim();
  if (!code) {{ appendOut('（代码为空，请先在编辑器中编写代码。）\\n', 'out-err'); return; }}
  btn.disabled = true;
  const originalHTML = btn.innerHTML;
  btn.innerHTML = '<span style="display:inline-block;width:14px;height:14px;border:2px solid #ffffff66;border-top-color:#fff;border-radius:50%;animation:spin 0.8s linear infinite;vertical-align:-2px;margin-right:6px;"></span>运行中...';
  // 注入一个临时动画 CSS
  if (!document.getElementById('spin-style')) {{
    const s = document.createElement('style');
    s.id = 'spin-style';
    s.textContent = '@keyframes spin {{ to {{ transform: rotate(360deg); }} }}';
    document.head.appendChild(s);
  }}
  clearOut();
  appendOut('[提示] 正在执行 Python 代码，首次运行需 5-15 秒加载依赖...\\n', 'out-info');

  let py;
  try {{
    py = await ensurePyodide();
    await py.runPythonAsync('import sys, io\\nsys.stdout = io.StringIO()\\n');
    try {{
      await py.runPythonAsync(code);
    }} catch (err) {{
      appendOut(String(err) + '\\n', 'out-err');
    }}
    const stdout = String(await py.runPythonAsync('sys.stdout.getvalue()'));
    if (stdout) appendOut(stdout);
    // 尝试渲染 matplotlib figure
    try {{
      const figCount = parseInt(await py.runPythonAsync('import matplotlib.pyplot as plt\\nlen(plt.get_fignums())'));
      if (figCount > 0) {{
        appendOut(`\\n[绘图] 检测到 ${{figCount}} 张 figure，正在渲染 PNG...\\n`, 'out-info');
        for (let i = 0; i < figCount; i++) {{
          const b64 = String(await py.runPythonAsync(
            `import matplotlib.pyplot as plt, base64, io\\nfig = plt.figure(plt.get_fignums()[${{i}}])\\nbuf = io.BytesIO()\\nfig.savefig(buf, format='png', bbox_inches='tight', dpi=120)\\nbase64.b64encode(buf.getvalue()).decode()`
          ));
          const img = document.createElement('img');
          img.src = 'data:image/png;base64,' + b64;
          img.style.maxWidth = '100%';
          img.style.borderRadius = '0.75rem';
          img.style.border = '1px solid #e5e7eb';
          img.style.marginTop = '0.5rem';
          $('output-area').appendChild(img);
        }}
        await py.runPythonAsync("plt.close('all')");
      }}
    }} catch (e) {{}}
    appendOut('\\n[完成] 代码执行结束。\\n', 'out-ok');
  }} catch (err) {{
    appendOut(String(err) + '\\n', 'out-err');
  }} finally {{
    btn.disabled = false;
    btn.innerHTML = originalHTML;
  }}
}}

// ------------------- 选择题初始化 -------------------
function initQuiz() {{
  COURSE.quiz.forEach((q, idx) => {{
    const box = document.querySelector(`#quiz-box [data-q-idx="${{idx}}"]`)?.parentElement;
  }});
}}
function submitQuiz() {{
  let correct = 0;
  COURSE.quiz.forEach((q, idx) => {{
    const chosen = document.querySelector(`input[name="q${{idx}}"]:checked`);
    const labels = document.querySelectorAll(`#quiz-box [data-q-idx="${{idx}}"]`);
    const resultDiv = document.getElementById(`qresult_${{idx}}`);
    labels.forEach(l => l.classList.remove('correct','wrong'));
    labels[q.answer].classList.add('correct');
    resultDiv.classList.remove('hidden');
    if (!chosen) {{
      resultDiv.innerHTML = `<span class="text-rose-500">未作答</span>。正确答案：<b>${{String.fromCharCode(65+q.answer)}}</b>。<br/>解析：${{q.explain}}`;
      return;
    }}
    const v = parseInt(chosen.value, 10);
    if (v === q.answer) {{
      correct++;
      resultDiv.innerHTML = `<span class="text-emerald-600 font-semibold">✓ 回答正确</span><br/>解析：${{q.explain}}`;
    }} else {{
      labels[v].classList.add('wrong');
      resultDiv.innerHTML = `<span class="text-rose-500 font-semibold">✗ 回答错误</span>，正确答案：<b>${{String.fromCharCode(65+q.answer)}}</b>。<br/>解析：${{q.explain}}`;
    }}
  }});
  $('quiz-total').innerHTML = `你的得分：<b class="text-brand-500 text-base">${{correct}} / ${{COURSE.quiz.length}}</b> · ${{correct===COURSE.quiz.length?"🎉 全对，知识点掌握良好！":correct>=2?"👍 不错，继续巩固。":"📚 建议再看一遍知识点与解析。"}}`;
}}

document.addEventListener('DOMContentLoaded', () => {{
  $('code-editor').value = COURSE.defaultCode;
  $('answer-code').textContent = COURSE.defaultCode;
  $('answer-thinking').textContent = COURSE.thinking;

  $('btn-run').addEventListener('click', runCode);
  $('btn-reset').addEventListener('click', () => {{
    $('code-editor').value = COURSE.defaultCode;
    clearOut();
    appendOut('↺ 已重置为默认示例代码。\\n', 'out-info');
  }});
  const copyToClipboard = (text, btn) => {{
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(text).then(() => {{
        const old = btn.textContent;
        btn.textContent = '✓ 已复制';
        setTimeout(() => (btn.textContent = old), 1200);
      }});
    }} else {{
      const ta = document.createElement('textarea');
      ta.value = text; document.body.appendChild(ta); ta.select();
      document.execCommand('copy'); document.body.removeChild(ta);
      const old = btn.textContent; btn.textContent = '✓ 已复制';
      setTimeout(() => (btn.textContent = old), 1200);
    }}
  }};
  $('btn-copy').addEventListener('click', e => copyToClipboard($('code-editor').value, e.target));
  $('btn-copy-ref').addEventListener('click', e => copyToClipboard(COURSE.defaultCode, e.target));
  $('btn-clear-out').addEventListener('click', clearOut);

  $('btn-quiz').addEventListener('click', submitQuiz);
  $('btn-quiz-reset').addEventListener('click', () => {{
    document.querySelectorAll('#quiz-box input[type="radio"]').forEach(r => r.checked = false);
    document.querySelectorAll('#quiz-box .choice-item').forEach(el => el.classList.remove('selected','correct','wrong'));
    document.querySelectorAll('#quiz-box [id^="qresult_"]').forEach(el => el.classList.add('hidden'));
    $('quiz-total').innerHTML = '';
  }});
  document.querySelectorAll('#quiz-box .choice-item').forEach(el => {{
    el.addEventListener('click', () => {{
      const qIdx = el.getAttribute('data-q-idx');
      document.querySelectorAll(`#quiz-box [data-q-idx="${{qIdx}}"]`).forEach(l => l.classList.remove('selected','correct','wrong'));
      el.classList.add('selected');
      const input = el.querySelector('input');
      if (input) input.checked = true;
    }});
  }});

  ensurePyodide().catch(() => {{
    $('env-status').textContent = '⚠ 环境加载失败，请刷新页面重试';
    $('env-status').classList.add('out-err');
  }});
}});
</script>
</body>
</html>
'''
    return html


if __name__ == "__main__":
    import os
    courses = [course1(), course2(), course3(), course4(), course5(),
               course6(), course7(), course8(), course9(), course10()]
    for c in courses:
        html = build_course(c)
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"course{c['idx']}.html")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✓ 生成 {path}")
    print(f"\n共生成 {len(courses)} 门课程页面。")
