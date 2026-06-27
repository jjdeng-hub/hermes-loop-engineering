---
title: Goal Engineering 与 Loop 的关系
date: 2026-06-25
source: cobusgreyling/goal-engineering
tags: [loop-engineering, goal-engineering, companion]
---

# Goal Engineering（目标工程）

GitHub: cobusgreyling/goal-engineering（Loop Engineering 的伴生项目）

## 一句话定义

一个 **goal** 是一个有可验证完成条件的自动目标。与 loop（按计划触发）不同，goal **跨会话持续存在**，直到标记完成、阻塞或暂停。

三个层次：
- **Prompt** = 一次对话，一个回答
- **Loop** = 按节奏循环发现 + 分类
- **Goal** = 持续执行直到完成（或被阻塞/暂停）

## Goal vs Loop

| 维度 | Goal | Loop |
|------|------|------|
| **触发器** | 你设定一个目标 | 调度（`/loop`）或自动化 |
| **持续时间** | 直到完成/阻塞/清除 | 永远循环（或被取消） |
| **最适合** | 完成一个有边界的任务 | 持续发现 + 分类待办 |
| **状态文件** | `GOAL.md` | `STATE.md`, `LOOP.md` |

**组合使用：** Loop 发现了可修复的项目 → **交给 Goal 去执行**（run-until-done）

## Goal 的四个构件

| 构件 | 作用 |
|------|------|
| **目标（Objective）** | 一句话 + 可验证的完成条件 |
| **验证器（Verifier）** | 独立的检查 — 实现者不能给自己打分 |
| **状态（State）** | `GOAL.md` 或等效的外部记忆 |
| **预算（Budget）** | Token/轮次上限 + 终止开关 |

## Goal 的典型流程

```
/goal <目标> → 定义范围+完成条件
    → 写入 GOAL.md 状态
    → 实现者轮次
    → 验证子 agent / 测试
    → 完成？→ update_goal(completed: true)
        阻塞？→ update_goal(blocked_reason)
    → 未完成 → 继续实现者轮次
```

## Grok Build API（Goal 命令）

| 命令 | 用途 |
|------|------|
| `/goal <objective>` | 设定新目标 |
| `/goal status` | 查看当前目标状态 |
| `/goal pause / resume` | 暂停或继续 |
| `/goal clear` | 退出目标模式 |

## 可用 Pattern

| 模式 | 用法 |
|------|------|
| Tests Green | CI 红色变绿色 + 验证器门控 |
| Migrate Module | API/模块迁移 + 导入扫描 |
| Implement Feature | 有边界的功能 + 验收标准 |
| Fix Bug | 复现 → 修复 → 回归测试 |
| Refactor Safely | 保持行为不变的代码重构 |
| Coverage Target | 将测试覆盖率提升到阈值 |

## 对 Jerry 项目的启示

1. **/goal 在 Hermes 里已有 L1**（while-loop 判断），可以进化到 L2/L3
2. Goal 和 Loop 的组合模式正是 Jerry 想要的一人公司架构
3. 用于知识库场景的 Goal 比如："GOAL: 完成半导体知识库的目录构建"→ verifier 检查完整性和一致性
