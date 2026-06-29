---
title: 日常自动化循环
created: 2026-06-27
updated: 2026-06-27
type: entity
tags: [hermes, cron, loop-engineering]
---

## 概述

三个 cron 任务构成每日自动化流水线，实现「睡觉时也在跑」的 Loop Engineering。

## 流水线

```
 3:00  备份  →  6:00  自动更新  →  8:00  分诊报告
 backup     hermes update -y     triage → QQ
```

## 任务详情

### 1. daily-backup (3:00 AM)
- 命令: `hermes curator backup`
- 交付: local（本地存储）
- 保留最近 5 个备份

### 2. hermes-auto-update (6:00 AM)
- 执行: `/root/.hermes/scripts/hermes-update.sh`
- 使用内置 `hermes update -y` 命令
- 包含: 并发锁 / 磁盘检查 / 配置备份 / 网关重启 / 健康检查
- 交付: QQ 推送（有更新才推送）

### 3. daily-triage (8:00 AM) 
- 检查: 磁盘、内存、负载、网关状态
- 读取: 更新结果、cron 输出
- 写入: `/root/.hermes/loop-state.md`
- 交付: QQ 推送（含更新概要）

## Maker-Checker 模式

采用橙皮书 §05 的生成者-评判者分离原则：
- Maker: `delegate_task` 用 DeepSeek Flash 生成
- Checker: 另一个 `delegate_task` 用 DeepSeek Reasoner 审查
- 新鲜上下文避免自我说服

## 相关页面

- [[hermes-config]]
- [[loop-engineering]]
