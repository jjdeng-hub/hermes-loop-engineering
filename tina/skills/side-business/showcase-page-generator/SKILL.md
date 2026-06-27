---
name: showcase-page-generator
description: 快速生成独立 HTML 展示页面用于接单/商业展示——4种风格覆盖 SaaS、Dashboard、App、Portfolio 四种场景，单文件零依赖，可直接截图发闲鱼/即刻等平台
---

# 展示页面生成器

> 为卖服务而生。生成的是**让人想买单的页面**，不是功能完整的网站。

## 触发条件

- 用户要在闲鱼、即刻、小红书等平台发布设计/开发服务
- 用户需要展示自己能做出什么样的页面效果
- 用户需要 Before/After 对比素材

## 四种风格模板

| 风格 | 文件名 | 配色 | 字体 | 适用场景 |
|---|---|---|---|---|
| 暗色奢华 | `1-saas-landing.html` | 黑底+金色 | 系统无衬线体 | SaaS 产品、工具型产品 |
| 洁净瑞士 | `2-dashboard.html` | 白底+灰 | 系统无衬线体 | 后台管理、数据分析 |
| 霓虹科技 | `3-neon-app.html` | 全黑+青紫渐变 | 系统无衬线体 | AI 产品、App 展示 |
| 编辑杂志 | `4-portfolio.html` | 奶白底+黑 | Georgia 衬线体 | 品牌设计、创意工作室 |

## 页面设计原则

以下原则来自 Impeccable、Taste Skill、UI/UX Pro Max 三个 Skill 的核心规则：

1. **反 AI 模板化**: 不用 Inter 字体、不用紫蓝渐变、不用居中 Hero + 三等分卡片。每个页面有自己的视觉性格。
2. **玻璃态毛玻璃**: `background: rgba(255,255,255,.04); backdrop-filter: blur(24px); border: 1px solid rgba(255,255,255,.08);`
3. **金色点缀**: 不是大面积金色，是细节处一小块（标题高亮、按钮、标签颜色）——奢华感来自克制。
4. **呼吸感**: 充足的留白、32px+ 的卡片间距、48px+ 的区块间隔。密 = 廉价。
5. **字重对比**: 标题 700、正文 400、小字 11-13px——层级分明，用户扫描时天然知道看哪里。

## 交付物

所有页面都是**单个 HTML 文件、零外部依赖、纯内联 CSS**。用户在桌面双击即可在 Chrome 打开。

## 与真实项目的关系

这些页面是**展示素材**，不是生产代码。如果需要交付真实项目，请使用 `website-design-upgrade` 或 `website-feature-development` skill。

## 截图方法

1. Chrome 打开 HTML 文件
2. F11 全屏
3. Ctrl+Shift+P 输入 Capture full size screenshot
4. 保存 PNG

## 替代方案（推荐）

如果用户有图生 API Key（推荐 SiliconFlow，新用户送 14 元额度），直接用 baoyu-infographic 替代——生成一张高密度信息图的效果远好于 HTML 截图。参见 baoyu-infographic / baoyu-article-illustrator / baoyu-comic 技能。

## 与真实项目的关系

参考 `references/templates.md` 获取四个已验证模板的完整源码。
