---
title: Loop Engineering 六大基础构件详解
date: 2026-06-25
source: cobusgreyling/loop-engineering
tags: [loop-engineering, primitives, architecture]
---

# 六大基础构件详解

## 1. Automations / Scheduling（自动调度）

循环的"心跳"。没有调度，就只是一次性 agent 运行。

**各工具实现方式：**
- Grok: `/loop [interval] <prompt>`
- Claude Code: `/loop`, cron, hooks
- Codex: Automations tab
- Cursor: Cloud Agent + Automations (cron/webhook)
- Windsurf: Workflows (`/workflow-name`)
- **Hermes: cronjob** ✅

关键属性：间隔、立即触发、循环/一次性、持久化（重启后存活）

## 2. Worktrees（工作树）

无混乱的并行执行。两个 agent 同时编辑同一文件 = merge 地狱。
Git worktree（或等效的隔离 checkout）让每个 agent 有自己的工作目录。

- **Hermes: 缺** ❌ （这是最大缺口）

## 3. Skills（技能）

意图的持久记忆。一个 skill 编码：
- 项目约定
- "我们不用这种方式因为 X 事故"
- 构建/测试/lint 命令
- 审查标准
- 领域知识

没有 skill，loop 每次从头推导一切（意图债务）。

**Hermes: skill 系统** ✅

## 4. Plugins & Connectors (MCP)

连接外部工具：Linear/Jira、Slack/Discord、数据库、内部 API、GitHub PR。

MCP 已成为通用协议。

**Hermes: MCP 支持** ✅

## 5. Sub-agents（子 Agent）- Maker/Checker 分离

最关键的可靠性模式。写代码的 agent 不能审自己的代码。
常用分拆：Explorer → Implementer → Verifier

**Hermes: delegate_task** ✅（已实现 maker/checker 分离）

## + Memory / State（状态持久化）

模型没有跨会话的长期记忆。
loop 必须读写持久化存储：`STATE.md`、`LOOP-STATE.json`、数据库行。

好状态应回答：
- 我们现在在做什么？
- 上次试了什么，结果如何？
- 什么在等人工决策？

**Hermes: memory 系统 + SOUL** ✅

---

## 最小可行 Loop

大多数 loop 从这开始：**调度 + 一个 triage skill + 状态文件**

然后逐渐添加：
- 需要改代码时加 Worktree 隔离
- 需要自动执行时加子 agent 验证
- 需要驱动工单/PR 时加连接器

最佳 loop 是那些每加一个新构件时，前一个版本已经证明了自己的价值（和失败模式）的 loop。
