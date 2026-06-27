---
title: Loop Engineering 跨工具对比矩阵
date: 2026-06-25
source: cobusgreyling/loop-engineering docs/primitives-matrix.md
tags: [loop-engineering, tools, comparison]
---

# 跨工具对比矩阵

五大工具 vs Hermes 的 loop 构件对比。

## 基础构件对比

| 构件 | Grok | Claude Code | Codex | **Hermes** |
|------|------|------------|-------|-----------|
| **自动调度** | `/loop [interval]` | `/loop`, cron, hooks | Automations 标签页 | **cronjob** ✅ |
| **Run-until-done** | `/goal` | `/goal` | `/goal` | **/goal (Level 1)** ✅ |
| **Worktrees** | subagent isolation | `--worktree` | 内置 | **缺** ❌ |
| **Skills** | `.grok/skills/SKILL.md` | `.claude/skills/SKILL.md` | Agent Skills | **skill 系统** ✅ |
| **MCP 连接器** | CallMcpTool | MCP servers | Connectors (MCP) | **MCP** ✅ |
| **子 Agent** | Task + subagent_type | `.claude/agents/` | `.codex/agents/` TOML | **delegate_task** ✅ |
| **状态/记忆** | STATE.md | AGENTS.md, Linear | Markdown/Linear | **memory + SOUL** ✅ |

## 子 Agent 模式

| 拆分方式 | 何时使用 | Hermes 实现 |
|---------|---------|------------|
| **Implementer → Verifier** | 任何无人值守的代码变更 | Justin → Checker ✅ |
| **Explorer → Implementer** | 不熟悉的大型代码库 | 可用 delegate_task |
| **Triage only** | 只出报告不出手 | cronjob + skill |

## 状态文件规范

推荐文件名（每个项目挑一个）：
- `STATE.md` — 通用 loop 记忆（daily triage）
- `issue-triage-state.md` — Issue 队列健康
- `pr-babysitter-state.md` — PR 监视状态
- `ci-sweeper-state.md` — 活跃 CI 失败 + 尝试次数

## Hermes 的独特优势

相比 Grok/Claude Code/Codex 这些工具：
1. Hermes 有 **profile 系统**（角色分离），这是其他工具没有的
2. Hermes 的 **SOUL 机制**（每个 profile 独立思维规则）比纯 SKILL.md 更深层
3. Hermes 有 **cronjob 持久化运行**，不像 Cursor 依赖外部 cron
4. Hermes **多渠道投递**（QQ、Telegram、本地）——其他工具主要只输出到终端

## Hermes 的缺口

1. **Worktrees** — 必须依赖外部 git 管理或手动隔离
2. **Goal Engineering 的 L2/L3** — 当前 /goal 只有 while-loop，缺持续误差信号→修正
