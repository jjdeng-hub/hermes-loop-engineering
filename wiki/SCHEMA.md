# Wiki Schema

## Domain

Hermes Agent 配置与自动化 / 一人公司 (OPC) / Loop Engineering

## Conventions

- File names: lowercase, hyphens, no spaces
- Every wiki page starts with YAML frontmatter
- Use `[[wikilinks]]` to link between pages
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md`
- Every action must be appended to `log.md`

## Frontmatter

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [hermes, loop-engineering, opc, server, tool, skill]
source: raw/articles/source-name.md
---
```

## Tag Taxonomy

- **hermes**: 核心配置、技能、插件
- **loop-engineering**: Loop Engineering 相关
- **opc**: 一人公司架构
- **server**: 服务器配置、部署
- **tool**: 安装的工具（CloakBrowser, Lupin等）
- **github**: GitHub 集成
- **memory**: 记忆管理
- **cron**: 定时任务
- **gateway**: QQ Bot 等消息网关
- **proxy**: 代理配置
- **security**: 安全、护栏

## Page Thresholds

- **Create a page** when an entity/concept appears in 2+ sources
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions
- **Split a page** when it exceeds ~200 lines

## Entity Pages

One page per notable entity. Include:
- Overview / what it is
- Key facts and dates
- Relationships to other entities ([[wikilinks]])
- Configuration details

## Concept Pages

One page per concept or topic. Include:
- Definition / explanation
- Current state
- Related concepts ([[wikilinks]])
