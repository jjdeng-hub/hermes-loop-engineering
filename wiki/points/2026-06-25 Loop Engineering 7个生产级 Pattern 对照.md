---
title: Loop Engineering 7个生产级 Pattern 对照
date: 2026-06-25
source: cobusgreyling/loop-engineering
tags: [loop-engineering, patterns, workflows]
---

# 7 个生产级 Pattern

## 症状 → 模式 速查

| 症状 | 推荐模式 | 起步建议 |
|------|---------|---------|
| CI 主分支/PR 报错 | CI Sweeper | L2, 15分钟间隔, 最多3次尝试 |
| PR 等审核/CI/变基 | PR Babysitter | L1 观察 → L2 辅助修复 |
| 每天早上不知道该做什么 / Issue 噪声 | Daily Triage + Issue Triage | **L1 报告模式第一周** — 低风险 |
| 依赖过期 / CVE 告警 | Dependency Sweeper | L2 只打安全补丁, 屏蔽大版本 |
| 合并后 TODO/清理堆积 | Post-Merge Cleanup | L1 低峰期, 只修小型问题 |
| 更新日志过期/缺失 | Changelog Drafter | **L1**（只出草稿），极低风险 |

## Pattern 详细说明

### ⭐ Daily Triage（每日分类）
- 节奏：每天 / 每2小时
- 预期第1周产出：L1 报告
- Token 消耗：低
- 适合：项目健康检查

### PR Babysitter（PR 保姆）
- 节奏：5-15分钟
- 适合：PR 排队严重时
- Token 消耗：高
- 注意：先 L1 观察，不要一上来就自动修复

### CI Sweeper（CI 清扫）
- 节奏：5-15分钟
- 适合：CI 频繁崩溃时
- Token 消耗：极高
- 注意：设定 max 3 attempts

### Dependency Sweeper（依赖更新）
- 节奏：6小时~1天
- 适合：依赖库多、安全漏洞多
- Token 消耗：中
- 注意：只修补丁版本，不更新大版本

### Changelog Drafter（更新日志）
- 节奏：每天或打标签时
- Token 消耗：低
- 风险极低，适合第一个试水的 loop

---

## 成本意识推荐

预算紧张时优先：Changelog Drafter、Daily Triage (L1)、Post-Merge
预算充足时再加：CI Sweeper、PR Babysitter

## 重叠规则

| 组合 | 规则 |
|------|------|
| CI Sweeper + PR Babysitter | CI Sweeper 负责失败的 CI 检查；PR Babysitter 在同一小时内不重复修同一分支 |
| Daily Triage + 其他 | Daily Triage 只出报告；动作型 loop 执行。L1 阶段不自动修复 |
| Dependency + CI Sweeper | CI 主分支红色时暂停 Dependency Sweeper |
| 多个 loop | 不同 concern 需要协调规则，详见 multi-loop.md |

## Hermes 对应实现思路

- Daily Triage → cronjob 每天一次 + skill 做检查 + 生成报告发送
- CI Sweeper → cronjob 定期 + delegate_task 执行修复 + checker 验证
- PR Babysitter → 需要 MCP GitHub 连接器
