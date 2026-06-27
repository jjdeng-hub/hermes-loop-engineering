---
title: Loop Engineering
created: 2026-06-27
updated: 2026-06-27
type: concept
tags: [loop-engineering, opc]
---

## 定义

> Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead. — Addy Osmani

循环工程：把「负责 prompt agent 的人」从自己换成一套系统。

## 核心人物

| 人物 | 角色 | 名言 |
|---|---|---|
| Addy Osmani (Google) | 命名+奠基 | "Design the system that prompts the agent" |
| Peter Steinberger (OpenClaw) | 引爆者 | "Design loops that prompt your agents" |
| Boris Cherny (Anthropic) | 实践者 | "My job is to write loops" |

## 四层技术栈

| 层 | 管什么 |
|---|---|
| Prompt Engineering | 写好一次的提示词 |
| Context Engineering | 这一刻窗口里放什么 |
| Harness Engineering | 单次运行的武装 |
| **Loop Engineering** | 在 harness 之上调度 |

## 六个零件

| 零件 | 作用 | Hermes 对应 |
|---|---|---|
| **Automation** | 定时自动发现和调度 | `cronjob` |
| **Worktree** | 隔离并行 agent 的工作目录 | `delegate_task` |
| **Skill** | 固化项目知识 | `skill_manage` |
| **Connector** | MCP 连接外部系统 | MCP Filesystem |
| **Sub-agent** | 生成者与评判者分离 | `delegate_task` Maker-Checker |
| **Memory** | 磁盘上的持久状态 | `memory` + `fact_store` + wiki |

## 五个动作

1. **发现** — 自己找出这圈该做的事
2. **交付** — 把任务隔离着交给 agent
3. **验证** — 换个 agent 说「不」
4. **持久化** — 把状态写到对话之外
5. **调度** — 让它一圈圈自动转

## 四笔代价

| 代价 | 防它 |
|---|---|
| 验证债 | 独立的评判者 |
| 理解腐烂 | 定期读产出 |
| 认知投降 | 执行可外包，拿主意不行 |
| Token 失控 | 钉死预算和重试上限 |

## 相关页面

- [[daily-automation-loop]]
- [[opc-one-person-company]]
