# Pandas 数据分析实战训练营 - The Implementation Plan (Decomposed and Prioritized Task List)

## [ ] Task 1: 创建目录结构与公共模块（common）
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 在 `/workspace` 下创建 `projects/`、`common/` 目录
  - 编写 `common/storage.js`：提供 localStorage 读写 API（代码保存、进度、徽章）
  - 编写 `common/pyodide_setup.js`：统一初始化 Pyodide，预装 pandas/numpy/sklearn
  - 编写 `common/code_runner.js`：提供 `runCode(code, csvData)`：执行代码、捕获 stdout、DataFrame 表格渲染
  - 编写 `common/style.css`：全局深色+科技蓝主题、卡片、动画、响应式
- **Acceptance Criteria Addressed**: AC-5, AC-8
- **Test Requirements**:
  - `programmatic` TR-1.1: `storage.js` 的 `getCode(projectId)`/`saveCode(projectId, code)`/`markComplete(projectId)`/`getProgress()` 接口正确读写 localStorage
  - `programmatic` TR-1.2: `pyodide_setup.js` 暴露 `window.pyodideReady` Promise，完成后 pandas 可 import
  - `programmatic` TR-1.3: `code_runner.js` 的 `runCode(code)` 能执行简单 print、渲染 DataFrame 为 HTML 表格、捕获错误
- **Notes**: 公共模块通过 `<script>` 标签在每个项目页中按顺序加载（storage → pyodide_setup → code_runner → style.css）。Pyodide 仅初始化一次，使用全局变量 `window.pyodide`。

## [ ] Task 2: 实现首页 `index.html`
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 使用 Vue3（CDN global build）+ TailwindCSS CDN
  - 头部：Logo + 标题 + 副标题 + 宣传语 + 进度统计（通过 `storage.getProgress()` 读取）
  - 训练营介绍：4 个要点
  - 10 大项目含义说明列表
  - 学习难度路径卡片（入门/基础/进阶/高阶/专家）
  - 10 个精美项目卡片（标题、难度、描述、完成徽章、进入按钮，链接到 `projects/XX_xxx.html`）
  - 页脚：部署说明
- **Acceptance Criteria Addressed**: AC-1, AC-2, AC-10, AC-11
- **Test Requirements**:
  - `programmatic` TR-2.1: 首页读取 localStorage 进度并显示正确数字（已完成 X/10）
  - `programmatic` TR-2.2: 10 个项目卡片跳转到正确项目页 URL
  - `human-judgement` TR-2.3: 视觉风格现代、卡片布局美观、响应式
- **Notes**: 项目 ID 约定：`01_cart_abandon`、`02_rfm_analysis`、`03_price_anomaly`、`04_kmeans_cluster`、`05_basket_analysis`、`06_behavior_sequence`、`07_promo_compare`、`08_sentiment_analysis`、`09_ltv_calculation`、`10_realtime_feature`。文件名同 ID + `.html`。

## [ ] Task 3: 实现项目页通用模板（代码编辑器、数据预览、控制台）
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 每个项目页使用相同结构：顶部导航 + 标题 + 数据集说明 + 数据预览表格 + CodeMirror 编辑器 + 按钮组 + 输出控制台 + 完成徽章按钮
  - 通过 importmap + ESM 方式加载 CodeMirror 6（`codemirror`、`@codemirror/state`、`@codemirror/view`、`@codemirror/lang-python`、`@codemirror/theme-one-dark`）
  - 页面内嵌 20+ 行 CSV 数据，表格展示
  - 默认示例代码与参考答案代码均以 `<script type="text/data" id="default-code">` 等标签嵌入
  - 页面加载时优先恢复用户代码（storage.js），否则加载默认代码
  - 运行代码按钮调用 `code_runner.runCode()`，重置按钮恢复默认代码，查看参考答案按钮切换为参考代码
  - 完成项目按钮调用 `storage.markComplete(projectId)` 并显示徽章
- **Acceptance Criteria Addressed**: AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9
- **Test Requirements**:
  - `programmatic` TR-3.1: 每个项目页数据预览表格展示 ≥20 行 CSV 数据
  - `programmatic` TR-3.2: CodeMirror 编辑器正确显示 Python 代码并高亮
  - `programmatic` TR-3.3: 运行代码按钮能调用 Pyodide 并在输出区显示结果/表格/错误
  - `programmatic` TR-3.4: 重置/参考答案 按钮正确切换代码
  - `programmatic` TR-3.5: 刷新页面后编辑器代码与完成状态正确从 localStorage 恢复

## [ ] Task 4: 编写项目 1-2（购物车放弃分析、RFM 用户分层）
- **Priority**: P0
- **Depends On**: Task 3
- **Description**:
  - `projects/01_cart_abandon.html`：user_id,item_id,add_time,payment_time,price,quantity（20+ 行）
    - 目标：按小时分组统计放弃率、加购未支付占比
  - `projects/02_rfm_analysis.html`：user_id,order_date,amount（20+ 行）
    - 目标：分位数计算 R/F/M 得分、用户分层标签（重要价值/重要保持/流失预警等）
- **Acceptance Criteria Addressed**: AC-3, AC-4, AC-5
- **Test Requirements**:
  - `programmatic` TR-4.1: 两个项目的参考代码在 Pyodide 中可成功运行，有明确 print 输出或 DataFrame 表格

## [ ] Task 5: 编写项目 3-4（价格异常检测、KMeans 用户聚类）
- **Priority**: P0
- **Depends On**: Task 3
- **Description**:
  - `projects/03_price_anomaly.html`：product_id,category,price（20+ 行）
    - 目标：IQR 方法识别异常价格
  - `projects/04_kmeans_cluster.html`：user_id,total_amount,freq,avg_session_time（20+ 行）
    - 目标：KMeans 聚类 + 轮廓系数 + 群特征分析（使用 sklearn）
- **Test Requirements**:
  - `programmatic` TR-5.1: 项目 3 参考代码可运行并输出异常商品列表
  - `programmatic` TR-5.2: 项目 4 参考代码可运行并输出聚类结果

## [ ] Task 6: 编写项目 5-7（购物篮分析、行为序列、促销对比）
- **Priority**: P1
- **Depends On**: Task 3
- **Description**:
  - `projects/05_basket_analysis.html`：order_id,product_name（20+ 行）
    - 目标：商品共现频率、支持度 TopN（手写 Apriori 思想或简单计数）
  - `projects/06_behavior_sequence.html`：user_id,date,action（20+ 行）
    - 目标：行为间隔、序列、转化路径
  - `projects/07_promo_compare.html`：user_id,date,is_promo,amount（20+ 行）
    - 目标：活动周 vs 非活动周指标对比
- **Test Requirements**:
  - `programmatic` TR-6.1: 3 个项目参考代码均可运行

## [ ] Task 7: 编写项目 8-10（情感分析、LTV、实时特征）
- **Priority**: P1
- **Depends On**: Task 3
- **Description**:
  - `projects/08_sentiment_analysis.html`：rating,comment_text（20+ 行）
    - 目标：评分分布、情感倾向（基于评分）、关键词统计
  - `projects/09_ltv_calculation.html`：user_id,reg_date,order_date,amount（20+ 行）
    - 目标：30 天 LTV、用户分群价值、累计金额
  - `projects/10_realtime_feature.html`：user_id,timestamp,amount（20+ 行）
    - 目标：1 小时滚动窗口、累计金额、滑动统计
- **Test Requirements**:
  - `programmatic` TR-7.1: 3 个项目参考代码均可运行

## [ ] Task 8: 集成验证与样式打磨
- **Priority**: P1
- **Depends On**: Task 2, Task 4, Task 5, Task 6, Task 7
- **Description**:
  - 所有页面通过 `python -m http.server` 预览验证
  - 确保响应式布局、深色主题、卡片阴影、平滑动画一致
  - 检查所有项目页的进入按钮 URL 正确
  - 验证 localStorage 进度与徽章在首页正确显示
- **Acceptance Criteria Addressed**: AC-10, AC-11, AC-12
- **Test Requirements**:
  - `programmatic` TR-8.1: 所有 11 个 HTML 文件均能在现代浏览器中无错误加载
  - `programmatic` TR-8.2: 至少 2 个项目页的参考代码可实际运行并产生 DataFrame 表格输出
  - `human-judgement` TR-8.3: 整体视觉风格一致、响应式布局正常

---

## 依赖关系图（DAG）
```
Task 1 (common 模块)
   ├──→ Task 2 (首页)
   └──→ Task 3 (项目页模板)
          ├──→ Task 4 (项目 1-2)
          ├──→ Task 5 (项目 3-4)
          ├──→ Task 6 (项目 5-7)
          └──→ Task 7 (项目 8-10)
                   └──→ Task 8 (集成验证)
```
