---
title: CloakBrowser + Lupin 爬取方案
created: 2026-06-27
updated: 2026-06-27
type: entity
tags: [hermes, tool]
---

## 概述

服务器上的网页爬取方案栈，用于绕过 Cloudflare 等反爬保护。

## CloakBrowser

- 安装: `/opt/browser-search/`（npm）
- Chromium: 206MB stealth Chromium
- 功能: 绕过 Cloudflare / Akamai / DataDome / Imperva
- 用法: `node scripts/cloak/cloak-fetch.mjs <URL>`
- 限制: 不能绕过登录墙（X/Twitter, LinkedIn）和付费墙

### 实测结果

| 网站 | 结果 |
|---|---|
| 知乎（有 Cloudflare） | ✅ 绕过成功，12 秒拿到全文 |
| Medium | ✅ Cloudflare 绕过，但会员墙还在 |
| X/Twitter | ❌ 登录墙 |

## Lupin

- 安装: `npm install -g lupin-cli`
- 架构: HTTP → Camoufox（隐身 Firefox）→ Patchright（隐身 Chrome）
- 优点: 自动升级，一次成功记住 24 小时
- 状态: Camoufox 在无 GPU 服务器有兼容 bug（`Browser.setDefaultViewport`）

### Benchmark（官方数据）

| 网站 | Lupin |
|---|---|
| Reddit | ✅ |
| X/Twitter | ✅ |
| Instagram | ✅ |
| LinkedIn | ✅ |
| Medium | ✅ |
| Cloudflare 站点 | ✅ |
| **得分** | **25/25** |

## 完整可访问能力

| 工具 | 覆盖 |
|---|---|
| 浏览器 (built-in) | Hacker News, Wikipedia, YouTube, GitHub |
| CloakBrowser | 知乎, 36氪, B站, 微博, Cloudflare 站 |
| Lupin HTTP | X/Twitter 推文内容 |
| curl | 无防护的普通网页 |

## 相关页面

- [[hermes-config]]
