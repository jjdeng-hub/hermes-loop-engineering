# Cron Loop 实现参考 — Hermes 上的 Loop Engineering 实战

> 实现于 2026-06-26，基于 Loop Engineering 橙皮书理论

## 架构：三阶段循环链

```
  3:00                        6:00                        8:00
  ┌──────────┐               ┌──────────┐               ┌──────────┐
  │ 备份     │               │ 更新     │               │ 分诊     │
  │ backup   │ ──→ state ──→ │ update   │ ──→ state ──→ │ triage   │ ──→ QQ 推送
  │ cron     │    file       │ cron     │    file       │ cron     │     报告
  └──────────┘               └──────────┘               └──────────┘
```

每个阶段的输出写入 `/root/.hermes/loop-state.md`，三阶段读取同一文件实现跨轮记忆。

## 任务详情

### ⏰ 3:00 — 自动备份（daily-backup）
- **命令：** `hermes curator backup`
- **保留：** 最近 5 次备份
- **交付：** local（仅本地保存）

### ⏰ 6:00 — 自动更新（hermes-auto-update）
- **命令：** 执行 `/root/.hermes/scripts/hermes-update.sh`
- **脚本逻辑：** `hermes update --yes --backup` → systemctl restart → 健康检查
- **交付：** origin（QQ）
- **更新分析：** cron 任务会分析更新内容，标记安全修复和 QQ Bot 相关改动

### ⏰ 8:00 — 日常分诊（daily-triage）
- **检查项：** 磁盘、内存、负载、网关 PID
- **更新状态：** 读取 loop-state.md 中 6:00 的更新记录
- **状态文件：** 追加写入 `/root/.hermes/loop-state.md`
- **交付：** origin（QQ），格式化为结构化中文报告

## 状态文件格式

```markdown
# Loop State — YYYY-MM-DD

## 🔴 紧急
- ...

## 🟡 待办
- ...

## 🟢 正常
- 磁盘: XX% · 内存: XX · 负载: XX · 网关: ✅

## 📦 Hermes 自动更新 — YYYY-MM-DD HH:MM
- 版本变化: v0.17.0 → v0.18.0
- 新增 XX 个 commit
- 备份: /root/.hermes/backups/YYYYMMDD_HHMMSS/

## 下一步
- ...
```

## 橙皮书零件映射

| 零件 | Hermes 对应 | 在此循环中的角色 |
|---|---|---|
| **Automations** | `cronjob()` | 三个 cron 任务 |
| **Memory** | `/root/.hermes/loop-state.md` | 跨轮状态文件（§04 零件六） |
| **Sub-agents** | `delegate_task` | maker-checker 审查流 |
| **Skills** | `skill_manage` / `skill_view` | 固化项目知识 |
| **Worktrees** | `delegate_task` 并行 | 并行子任务隔离 |
| **Connectors** | MCP / QQ 交付 | 汇报送达 QQ |

## 注意事项

- Gateway 重启：从 QQ Bot 内部 `systemctl restart` 会因 SIGTERM 传播而卡住。cron 任务跑在独立进程，不受此限制
- 更新后验证：脚本使用 `systemctl show -p MainPID` 获取新 PID + `ss` 检查端口监听
- 回滚机制：`hermes update` 内置备份，失败自动回滚
