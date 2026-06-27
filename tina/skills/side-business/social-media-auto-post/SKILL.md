---
name: social-media-auto-post
description: 社交媒体自动发布 MVP 开发指南 — 使用 Playwright/Camoufox 操控网页版社交媒体平台，实现一键多平台发布
category: side-business
tags: [social-media, automation, playwright, camoufox, side-business, xiaohongshu]
---

# 社交媒体自动发布 MVP 开发指南

## 概述

本技能指导你快速开发社交媒体自动发布工具，用于副业验证。核心目标：**72 小时内做出 MVP，验证市场需求**。

## 核心痛点

- 副业多次失败，缺乏反馈循环
- 需要"3 天内有反馈"的快速验证机制
- 技术能力足够（Python），但需要正确的方向

## 技术栈

| 组件 | 选择 | 说明 |
|------|------|------|
| **浏览器自动化** | Playwright | Python 库，稳定可靠 |
| **反检测** | Camoufox | 反爬虫/反检测，适合长期自动化 |
| **语言** | Python 3.11+ | 已有环境 |
| **部署** | 本地运行 → 云服务器 | 初期本地，验证后部署 |

## 安装步骤

### 1. 安装 Playwright

```bash
uv pip install playwright --index-url https://pypi.tuna.tsinghua.edu.cn/simple
python -m playwright install chromium
```

### 2. 安装 Camoufox（可选，用于反检测）

```bash
uv pip install camoufox --index-url https://pypi.tuna.tsinghua.edu.cn/simple
# 注意：浏览器二进制下载可能失败（GitHub 限流），可先用 Playwright
```

### 3. 验证安装

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://www.baidu.com')
    print(f'Title: {page.title()}')
    browser.close()
```

## 小红书自动化流程

### 步骤 1：登录状态处理

**问题：** 所有浏览器会话都是独立的，无法直接继承本地登录状态。

**解决方案：** Cookie 导入

```python
from playwright.sync_api import sync_playwright

# 1. 用户在本地浏览器导出 Cookie（JSON 格式）
# 2. 加载 Cookie

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    
    # 加载 Cookie
    cookies = [
        {
            "name": "cookie_name",
            "value": "cookie_value",
            "domain": ".xiaohongshu.com",
            "path": "/",
            "expires": 1700000000,
            "httpOnly": False,
            "secure": False,
            "sameSite": "Lax"
        }
    ]
    context.add_cookies(cookies)
    
    page = context.new_page()
    page.goto('https://creator.xiaohongshu.com/new/home')
    # 现在应该是登录状态！
```

**如何导出 Cookie：**
1. 安装浏览器扩展：**Cookie Editor**（Chrome/Edge 商店）
2. 打开小红书页面（确保已登录）
3. 点击扩展 → Export → Copy to clipboard
4. 把内容粘贴到 JSON 文件

### 步骤 2：定位发布按钮

```python
# 截图分析页面元素
page.screenshot(path='xiaohongshu_home.png')

# 查找发布按钮
publish_buttons = page.locator('button:has-text("发布"), [class*="publish"], [class*="create"]').all()
print(f"找到 {len(publish_buttons)} 个可能的发布按钮")

for i, btn in enumerate(publish_buttons):
    try:
        text = btn.inner_text()
        print(f"按钮 {i+1}: {text}")
    except:
        pass
```

### 步骤 3：输入内容并发布

```python
# 点击发布按钮
publish_buttons[0].click()

# 等待发布页面加载
page.wait_for_selector('textarea, [contenteditable]')

# 输入内容
content_input = page.locator('textarea, [contenteditable]').first
content_input.fill('🤖 测试：AI 自动化发布测试内容')

# 上传图片（可选）
# page.set_input_files('input[type="file"]', 'image.jpg')

# 点击发布
page.click('button:has-text("发布")')

# 验证发布成功
page.wait_for_selector('.success, .toast:has-text("成功")')
```

## 72 小时验证计划

### Day 1：单平台 MVP

| 时间 | 任务 |
|------|------|
| 第 1-2 小时 | 研究小红书页面结构，定位发布按钮 |
| 第 3-4 小时 | 写单平台发布脚本（小红书） |
| 第 5 小时 | 自己测试 3 次，确保稳定 |
| **完成标准** | 能手动触发发布，内容正确出现在平台上 |

### Day 2：多平台 + 自动排版

| 时间 | 任务 |
|------|------|
| 第 1-2 小时 | 扩展第 2 个平台（微博） |
| 第 3 小时 | 添加自动排版功能（根据平台规则调整格式） |
| 第 4 小时 | 找 3 个朋友/同事免费试用 |
| **完成标准** | 3 人试用，收集反馈 |

### Day 3：反馈 + 决策

| 时间 | 任务 |
|------|------|
| 第 1 小时 | 收集 3 人的使用反馈 |
| 第 2 小时 | 问关键问题：'这个工具对你有用吗？愿意付费吗？多少钱合适？' |
| 第 3 小时 | 根据反馈决定：继续 / 调整 / 放弃 |

## 反馈评估标准

| 类型 | 信号 |
|------|------|
| **✅ 继续**（满足 2 个以上） | 试用者说"这对我很有用"、有人主动问"多少钱"、有人愿意付费、有人愿意推荐 |
| **⚠️ 调整**（满足 1 个） | 说"有用"但不愿意付费、提出具体改进建议、使用频率低但有潜力 |
| **❌ 放弃**（0 个正向） | 试用后无反馈、说"还行"但无后续、明确表示不需要 |

## 定价策略

| 版本 | 价格 | 功能 |
|------|------|------|
| **基础版** | 99 元/月 | 1 个平台，unlimited 发布 |
| **专业版** | 199 元/月 | 3 个平台 + 定时发布 |
| **企业版** | 499 元/月 | 无限平台 + 团队协作 |
| **早期用户** | 5 折 | 前 10 个付费用户 |

## 正循环设计

```
自己使用 → 优化产品 → 吸引更多用户
    ↓
用户反馈 → 产品迭代 → 口碑传播
    ↓
内容获客 → 用户增长 → 收入增加
```

## 风险与应对

| 风险 | 应对 |
|------|------|
| **平台 API 限制** | 先用 Selenium/Playwright 模拟浏览器，后续再换 API |
| **账号封禁风险** | 模拟人类操作节奏，添加随机延迟，不频繁发布 |
| **无用户试用** | 扩大招募范围（技术群、朋友圈、V2EX），提供小激励 |
| **无人付费** | 问清楚原因（价格太高？功能不够？），调整方向或换场景 |

## 全自动运营：可行性评估

**用户最终目标**：把账号完全交给 Agent，自动完成登录→发布→互动，零人工参与。

**核心瓶颈**：小红书/抖音网页版只支持扫码登录，Cookie 有效期 1-3 天。

详细分析见 [`references/full-automation-reality-check.md`](references/full-automation-reality-check.md)，包含：
- 三阶段实现路径（Cookie 半自动 → Windows Native → 反检测增强）
- Cookie 过期检测 + 自动提醒方案
- 交互自动化风险警告

云端浏览器方案（Browserbase / browse.sh）调研见 [`references/browse-sh-integration-research.md`](references/browse-sh-integration-research.md)。

## 扩展方向

验证成功后，可扩展：

1. **多平台支持**：小红书、微博、抖音、B 站、知乎
2. **定时发布**：设置发布时间，自动发布
3. **内容模板**：预设内容模板，一键生成
4. **数据分析**：发布后自动分析互动数据
5. **AI 内容生成**：集成 AI 自动生成文案

## 参考代码

测试脚本位置：`~/.hermes/scripts/test_xiaohongshu.py`

---

## 快速开始

```bash
# 1. 确保 Playwright 已安装
python -m playwright install chromium

# 2. 准备 Cookie（用户手动操作）
# 3. 运行测试脚本
python ~/.hermes/scripts/test_xiaohongshu.py
```