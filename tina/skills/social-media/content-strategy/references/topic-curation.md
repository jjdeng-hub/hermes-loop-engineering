
# 选题自动推送系统

## 概述

为「Jerry在想什么」账号提供 AI 选题。**主动源**：AIHOT API（卡兹克自建，168 信源，免费公开）；**补充源**：用户在小红书刷到的感兴趣内容。

## 使用方式

### 主动源：AIHOT

已安装为 skill（`aihot`）。用户说「来选题」或「今天 AI 圈有什么」时，调用 AIHOT API 拉取精选内容，筛选适合的观点/分析型选题，输出角度 + 姿态。

```bash
UA="Mozilla/5.0 aihot-skill/0.2.0"
curl -sH "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?mode=selected&category=tip&take=20"
```

AIHOT 提供了 5 个分类，最适合观点选题的是 `category=tip`（技巧与观点）和 `category=industry`（行业动态）。

### 补充源：用户自发发现

用户在小红书刷到感兴趣的内容 → 发链接/描述给 agent → agent 帮助展开为选题。

### 已废弃的方案

cron 自动推送方案已停用（信源不可靠：知乎需登录、Bing 中文结果被 SEO 污染、掘金偏技术教程）。AIHOT 是更优替代。

## 筛选原则

三道筛子：
1. 我妈能看懂标题吗？
2. 看完想评论/转发吗？
3. Jerry 有资格说吗（程序员经历/AI 使用体感/副业尝试）？

排除：纯技术教程、工具介绍、融资新闻、需要专业知识才能看懂的话题。

## 输出格式

| # | 标题 | 你的角度 | 姿态 |
|---|------|---------|------|
| 1 | [原话/标题] | [从 Jerry 什么经历/体感切入] | 站队型/提问型/安抚型 |

末尾附 TOP 3 推荐及原因。姿态分类参考 `content-stance-strategy`。

内容结构模式参考 `references/content-patterns.md`——当选题池有多条看似独立的候选时，优先尝试「双新闻合成」结构。
