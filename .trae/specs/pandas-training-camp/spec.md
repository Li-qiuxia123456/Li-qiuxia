# Pandas 数据分析实战训练营 - Product Requirement Document

## Overview
- **Summary**: 构建一个纯前端、无后端、可直接部署到 Cloudflare Pages 的 "Pandas 数据分析实战训练营" 学习网站。网站提供 10 个精选实战项目，用户可在浏览器中直接运行 Python（Pandas/Numpy/Sklearn）代码，通过 CodeMirror 编辑器与 Pyodide 运行时实现沉浸式学习。

## 学习路径：入门 → 基础 → 进阶 → 高阶/专家，每个项目包含内置数据集、示例代码、参考答案、数据预览、代码运行、进度保存与徽章激励系统。

- **Purpose**: 解决数据分析初学者无需配置 Python 环境即可上手实战；通过真实业务场景与循序渐进的学习路径帮助用户系统掌握 Pandas 核心技能。

- **Target Users**: 数据分析初学者、希望入门数据科学的产品/运营/风控从业者、想在浏览器环境中练习 Pandas 的学习者

## Goals
- 提供一个零配置、可本地预览的纯静态学习平台
- 以 10 个真实业务场景帮助用户从入门到专家
- 通过浏览器内 Python 运行环境实现 "看 → 写 → 跑 → 验证" 的闭环学习
- 通过 localStorage 实现进度、代码、徽章的本地持久化

## Non-Goals (Out of Scope)
- 不包含用户账号系统、不做用户跨设备同步（仅 localStorage 仅本地）
- 不包含后端 API / 数据库
- 不包含实时协作、代码共享
- 不做高级图表渲染（使用表格与文本输出即可）
- 不做视频/音频多媒体内容

## Background & Context
- Vue3 + TailwindCSS + CodeMirror 6 + Pyodide 均通过 CDN 加载
- 深色 + 科技蓝主题，卡片式布局
- 文件结构固定，部署方式为纯静态，支持 `python -m http.server` 预览或 Cloudflare Pages 部署

## Functional Requirements

### 首页
- **FR-1**: 头部展示网站 Logo、标题、副标题、宣传语、完成进度统计（已完成/10）
- **FR-2**: 训练营介绍区（为什么学、零配置、真实数据集、循序渐进）
- **FR-3**: 10 大项目含义说明区
- **FR-4**: 学习难度路径图（入门/基础/进阶/高阶/专家）
- **FR-5**: 10 个项目卡片（标题、难度、描述、完成徽章、进入按钮）
- **FR-6**: 页脚含部署说明

### 项目页（共 10 个）
- **FR-7**: 顶部导航栏 + 返回首页按钮
- **FR-8**: 项目标题 + 难度标签 + 项目介绍
- **FR-9**: 数据集说明 + 字段解释
- **FR-10**: 数据预览面板（内嵌 ≥20 行 CSV，表格展示）
- **FR-11**: CodeMirror 代码编辑器（默认加载示例代码）
- **FR-12**: 运行代码 / 重置代码 / 查看参考答案 按钮
- **FR-13**: 输出控制台（print、DataFrame 表格、错误信息）
- **FR-14**: 完成项目按钮（打徽章、保存进度）
- **FR-15**: 页面加载时自动恢复 localStorage 中的用户代码与进度
- **FR-16**: 自动保存用户代码编辑（自动/手动）

### 公共模块
- **FR-17**: `pyodide_setup.js`：统一加载 Pyodide，预装 pandas/numpy/sklearn
- **FR-18**: `code_runner.js`：代码执行、输出捕获、DataFrame 渲染表格
- **FR-19**: `storage.js`：localStorage 管理（代码、进度、徽章）
- **FR-20**: `style.css`：全局样式（深色 + 科技蓝主题）

## Non-Functional Requirements
- **NFR-1 (性能)**: Pyodide 首次加载需在合理时间内完成（首屏 < 30s，缓存后 < 5s）
- **NFR-2 (可用性)**: 响应式布局，手机/平板/PC 均可正常使用
- **NFR-3 (可靠性)**: 纯静态文件，无需构建，直接运行
- **NFR-4 (兼容性)**: Chrome/Edge/Firefox/Safari 现代版本均可运行
- **NFR-5 (可访问性)**: 所有资源通过 CDN 加载

## Constraints
- **Technical**: Vue3 + TailwindCSS + CodeMirror 6 + Pyodide，均通过 CDN 加载；无打包构建
- **Business**: 纯静态部署；无需后端服务
- **Dependencies**: Vue3 CDN（全局脚本方式使用；TailwindCSS CDN Play CDN；CodeMirror 6 通过 ESM CDN；Pyodide via CDN 官方

## Assumptions
- 用户使用现代浏览器（支持 ES modules、WebAssembly、localStorage）
- 用户网络可访问 CDN 资源（unpkg / jsdelivr / cdn.jsdelivr等）
- 数据集为模拟真实业务数据，可嵌入页面
- 每个项目的参考答案代码在 Pyodide + pandas/numpy/sklearn 环境下可成功运行

## Acceptance Criteria

### AC-1: 首页完整渲染
- **Given**: 用户访问 `/index.html`
- **When**: 页面在现代浏览器中加载
- **Then**: 页面成功渲染，包含头部、介绍区、10 大项目说明、难度路径、10 个项目卡片、页脚
- **Verification**: `human-judgment`

### AC-2: 首页进度统计
- **Given**: 用户已完成若干项目
- **When**: 访问首页
- **Then**: 进度数字显示 "已完成 X/10" 与对应徽章
- **Verification**: `programmatic`

### AC-3: 项目页数据预览
- **Given**: 进入任意项目页
- **When**: 页面加载完成
- **Then**: 数据预览面板显示 ≥20 行 CSV 数据表格
- **Verification**: `programmatic`

### AC-4: 代码编辑器加载
- **Given**: 进入任意项目页
- **When**: 页面加载完成
- **Then**: CodeMirror 编辑器显示默认示例代码，支持语法高亮
- **Verification**: `human-judgment`

### AC-5: 代码执行与输出
- **Given**: 编辑器内有可运行代码
- **When**: 用户点击"运行代码"
- **Then**: Pyodide 执行代码，输出控制台显示 print 输出 / DataFrame 表格 / 错误信息
- **Verification**: `programmatic`

### AC-6: 重置代码
- **Given**: 用户修改了代码
- **When**: 点击"重置代码"
- **Then**: 编辑器恢复为默认示例代码
- **Verification**: `programmatic`

### AC-7: 查看参考答案
- **Given**: 用户点击"查看参考答案"
- **When**: 点击按钮
- **Then**: 编辑器切换为参考答案代码
- **Verification**: `programmatic`

### AC-8: 代码与进度持久化
- **Given**: 用户修改代码、完成项目
- **When**: 重新打开项目页
- **Then**: localStorage 中保存用户代码与完成徽章；下次访问自动恢复
- **Verification**: `programmatic`

### AC-9: 完成徽章与进度
- **Given**: 用户完成项目
- **When**: 点击"完成项目"按钮"
- **Then**: 徽章显示，首页进度 +1
- **Verification**: `programmatic`

### AC-10: 响应式布局
- **Given**: 浏览器尺寸变化
- **When**: 在手机/平板/PC 尺寸下访问
- **Then**: 布局自动适配
- **Verification**: `human-judgment`

### AC-11: 文件结构正确性
- **Given**: 项目文件输出结构正确
- **When**: 检查文件列表
- **Then**: 严格匹配文件结构：index.html、projects/01-10.html、common/*.js、common/style.css
- **Verification**: `programmatic`

### AC-12: 本地运行验证
- **Given**: 在项目根目录运行 `python -m http.server`
- **When**: 浏览器访问 localhost:8000
- **Then**: 所有页面可正常加载、代码可运行
- **Verification**: `programmatic`

## Open Questions
- [x] 技术栈已固定为 Vue3 + TailwindCSS + CodeMirror + Pyodide
- [x] 文件结构与 10 个项目名称与内容已确定
- [x] 数据集字段已确定
- [x] 参考答案代码核心目标已确定
