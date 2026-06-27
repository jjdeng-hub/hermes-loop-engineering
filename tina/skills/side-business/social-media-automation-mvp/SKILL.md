---
name: social-media-automation-mvp
description: 社交媒体自动发布 MVP 验证技能 — 使用 Playwright/Camoufox 操控网页版社交媒体平台，快速验证自动化发布需求
category: side-business
tags: [副业, 社交媒体, 自动化, playwright, mvp, 验证]
---

# 社交媒体自动发布 MVP 验证技能

## 用途

快速验证"社交媒体自动发布"副业方向的可行性，使用浏览器自动化技术操控小红书、微博等平台的网页版，实现一键发布、自动排版等功能。

## 核心价值

- **不依赖行业经验**：任何行业的企业/个人都有社交媒体运营需求
- **反馈循环强**：客户付费即反馈，解决"做着做着没动力"的核心痛点
- **正循环设计**：自己使用 → 优化产品 → 吸引更多用户
- **启动快**：72 小时内可完成 MVP 验证

## 技术栈

| 组件 | 说明 | 安装命令 |
|------|------|---------|
| **Playwright** | 浏览器自动化核心库 | `uv pip install playwright` |
| **Camoufox** | 反检测浏览器（可选） | `uv pip install camoufox` |
| **Python 3.11+** | 运行环境 | 已预装 |

## 72 小时验证计划

### Day 1：做出单平台发布 MVP

**目标**：能手动触发发布，内容正确出现在平台上

**任务**：
1. 研究平台集成方案（小红书/微博 API 或 Selenium/Playwright）
2. 写一个脚本，能发布文字 + 图片到 1 个平台
3. 自己测试 3 次，确保稳定

**完成标准**：能手动触发发布，内容正确出现在平台上

**时间投入**：3-4 小时

### Day 2：扩展多平台 + 自动排版

**目标**：3 人试用，收集反馈

**任务**：
1. 支持第 2 个平台
2. 添加自动排版功能（根据平台规则调整格式）
3. 找 3 个朋友/同事免费试用

**关键动作**：在朋友圈/技术群发：'我做了个工具自动发小红书/微博，免费试用，有兴趣的私我'

**时间投入**：3-4 小时

### Day 3：收集反馈 + 决策

**目标**：明确决策（继续/调整/放弃）

**任务**：
1. 收集 3 人的使用反馈
2. 问关键问题：'这个工具对你有用吗？愿意付费吗？多少钱合适？'
3. 根据反馈决定：继续 / 调整 / 放弃

**时间投入**：2-3 小时

## 反馈评估标准

### ✅ 继续的信号（满足 2 个以上）

- 试用者说"这对我很有用"
- 有人主动问"多少钱"
- 有人愿意付费（哪怕 10 元）
- 有人愿意推荐给其他人

### ⚠️ 调整的信号（满足 1 个）

- 说"有用"但不愿意付费
- 提出具体改进建议
- 使用频率低但有潜力

### ❌ 放弃的信号（0 个正向）

- 试用后无反馈
- 说"还行"但无后续
- 明确表示不需要

## 定价策略

| 版本 | 价格 | 功能 |
|------|------|------|
| **基础版** | 99 元/月 | 1 个平台，unlimited 发布 |
| **专业版** | 199 元/月 | 3 个平台 + 定时发布 |
| **企业版** | 499 元/月 | 无限平台 + 团队协作 |
| **早期用户优惠** | 50-100 元/月 | 前 10 个付费用户 5 折 |

## 技术实现示例

### 基础发布脚本

```python
from playwright.sync_api import sync_playwright

def post_to_xiaohongshu(content: str, image_path: str = None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()
        
        # 导航到小红书
        page.goto('https://www.xiaohongshu.com')
        
        # 等待登录状态（用户需手动登录）
        page.wait_for_selector('.user-avatar', timeout=30000)
        
        # 点击发布按钮（需要根据实际页面调整选择器）
        publish_btn = page.locator('button:has-text("发布")').first
        publish_btn.click()
        
        # 输入内容
        content_input = page.locator('textarea, [contenteditable]').first
        content_input.fill(content)
        
        # 上传图片（如果有）
        if image_path:
            # 小红书图片上传需要处理文件选择器
            pass
        
        # 点击发布
        submit_btn = page.locator('button:has-text("发布")').last
        submit_btn.click()
        
        # 验证发布成功
        page.wait_for_timeout(3000)
        page.screenshot(path='post_success.png')
        
        browser.close()
```

### 反检测模式（Camoufox）

```python
from camoufox.sync_api import Camoufox

def post_with_anti_detection(content: str):
    with Camoufox() as browser:
        page = browser.new_page()
        page.goto('https://www.xiaohongshu.com')
        # ... 同上
```

## 风险与应对

| 风险 | 应对 |
|------|------|
| **平台 API 限制** | 先用 Playwright 模拟浏览器，后续再换 API |
| **账号封禁风险** | 模拟人类操作节奏，添加随机延迟，不频繁发布 |
| **无用户试用** | 扩大招募范围（技术群、朋友圈、V2EX），提供小激励 |
| **无人付费** | 问清楚原因，调整方向或换场景 |

## 正循环设计

```
循环 1：自己使用 → 优化产品
  → 你用这个工具发自己的自媒体内容
  → 使用过程中发现痛点 → 优化产品
  → 产品更好用 → 吸引更多用户

循环 2：用户反馈 → 产品迭代
  → 用户提出需求 → 优先开发
  → 用户满意 → 口碑传播 → 新用户
  → 新用户付费 → 收入 → 投入更多开发

循环 3：内容获客 → 用户增长
  → 用工具发内容 → 内容展示工具效果
  → 内容吸引用户 → 用户试用 → 付费
  → 付费用户 → 口碑 → 更多用户
```

## 快速启动

```bash
# 1. 安装依赖
uv pip install playwright

# 2. 安装浏览器
playwright install chromium

# 3. 运行测试脚本
python ~/.hermes/scripts/test_xiaohongshu.py
```

## 关联技能

- `side-business-execution-tracker`：副业执行追踪与规划
- `camofox-anti-detect-browser`：反检测浏览器服务
- `xurl`：X/Twitter 官方 API CLI

## 注意事项

1. **不要追求完美**：MVP 阶段只需能用的最小版本
2. **保持登录状态**：网页版需要用户先登录，保持会话
3. **遵守平台规则**：不要频繁发布，模拟人类操作节奏
4. **快速试错**：3 天内无正向信号 → 果断放弃，换方向