---
title: Hermes Agent 完整配置
created: 2026-06-27
updated: 2026-06-27
type: entity
tags: [hermes, server]
---

## 概述

Alibaba Cloud ECS 上的 Hermes Agent 配置，用于个人开发与自动化。

## 基础信息

| 项目 | 值 |
|---|---|
| 服务器 | Alibaba Cloud ECS (华东) |
| IP | 47.86.180.83 |
| 系统 | Ubuntu 22.04 |
| Hermes 版本 | v0.17.0 |
| Python | 3.11 |
| 后端模式 | local（非 Docker） |

## 模型配置

| 角色 | 模型 | Provider |
|---|---|---|
| 主模型 | deepseek-v4-flash | DeepSeek API |
| Maker（生成者） | deepseek-v4-flash | DeepSeek API |
| Checker（评判者） | deepseek-reasoner | DeepSeek API |
| Vision | sensenova-6.7-flash-lite | SenseNova |

## API Keys

| Key | 用途 |
|---|---|
| `DEEPSEEK_API_KEY` | 主模型 |
| `OPENROUTER_API_KEY` | 模型路由备用 |
| `SN_CHAT_API_KEY` | 视觉能力 |

## 消息网关

- **QQ Bot**: 已配置并运行（App ID: 1903867252）
- 其他平台: 暂未配置

## 代理 (Tinyproxy)

| 项目 | 值 |
|---|---|
| IP | 47.86.180.83 |
| 端口 | 443（DPI 规避） |
| 认证 | jjdeng |
| 安全组 | 对家宽 IP 开放 |

## 自动更新

- 脚本: `/root/.hermes/scripts/hermes-update.sh`
- 使用内置 `hermes update -y` 命令
- 每天 6:00 自动执行
- 失败时自动回滚（git reset + 配置恢复）

## 记忆管理

- **MEMORY.md**: `/root/.hermes/memories/MEMORY.md`（2,200 字上限）
- **USER.md**: `/root/.hermes/memories/USER.md`（1,375 字上限）
- **Wiki**: `/root/.hermes/wiki/`（不限容量，LLM Wiki 格式）
- **Holographic 记忆**: state.db + fact_store

## 相关页面

- [[daily-automation-loop]]
- [[memory-architecture]]
- [[cloakbrowser-lupin]]
