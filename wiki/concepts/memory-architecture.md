---
title: 记忆架构
created: 2026-06-27
updated: 2026-06-27
type: concept
tags: [memory, hermes]
---

## 概述

Hermes 的记忆系统由三层构成，各司其职。

## 三层架构

### Layer 1: 会话记忆（自动压缩）
- **存储**: `~/.hermes/sessions/` + `state.db`
- **用途**: 当前聊天的完整上下文
- **压缩**: 接近 token 上限时自动摘要压缩
- **查询**: `session_search` 工具可回溯历史

### Layer 2: 持久记忆（有限容量）
- **存储**: `~/.hermes/memories/MEMORY.md`（2,200 字）
- **存储**: `~/.hermes/memories/USER.md`（1,375 字）
- **用途**: 跨会话的核心事实
- **注入**: 每轮会话开始时光标注入到 system prompt
- **管理**: `memory` 工具的 add/replace/remove

### Layer 3: 知识库（无限容量）
- **存储**: `~/.hermes/wiki/`（LLM Wiki 格式）
- **用途**: 架构方案、项目文档、深度知识
- **格式**: Markdown + YAML frontmatter
- **关联**: `[[wikilinks]]` 跨页面链接
- **查看**: 兼容 Obsidian，可在 Windows 上浏览

## 数据流

```
对话中产生知识
    ↓
重要且轻量? → MEMORY.md / USER.md (2,200 字上限)
    ↓
重要但深度? → WIKI (无限)
    ↓
不重要? → 留在会话记录 (session_search 可查)
```

## MEMORY.md 当前内容

- Server: Alibaba Cloud ECS, Ubuntu 22.04
- Proxy: 47.86.180.83:443, auth jjdeng
- QQ Bot: App ID 1903867252, 网关运行中
- 后端: local (非 Docker)
- Docker: 已卸载
- 搜索: CloakBrowser + 浏览器 + curl
- Maker-Checker: Flash + Reasoner
- Cron: 3:00 备份 / 6:00 更新 / 8:00 分诊

## 相关页面

- [[hermes-config]]
- [[daily-automation-loop]]
