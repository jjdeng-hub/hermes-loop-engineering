---
date: "2026-06-29"
tags: [session-summary, cron, vault-backup, model-sherpa, obsidian, auto-save]
updated: "2026-06-29"
---

# 2026-06-29 Session: 定时任务修复 + Obsidian Vault 自动备份

## 定时任务故障

### 现象
- hermes-auto-update（6AM）未交付结果到用户
- 实际触发了（06:00:52），但未完成

### 死因链
1. DeepSeek API 不稳定：4 次 stream stale（每次卡 180 秒），CloudFront 返回空响应
2. model-sherpa 插件 bug：`__init__.py` L2465 和 L2620 的 `error_message.strip()` 未处理 `None`
3. Git 仓库历史错乱：本地比 origin/main 多了 6424 个幽灵提交，无共同祖先
4. 更新脚本 `systemctl restart hermes-gateway` 杀死了正在跑的 cron agent
5. Gateway 重启后 scheduler 把 next_run_at 算成了明天

### 修复
- model-sherpa 两处 NoneType bug 已修（`(error_message or "").strip()`）
- Git 仓库历史待重置（需用户确认）

## Obsidian Vault 自动备份

### 现状
- Vault 路径：`/root/.hermes/skills/research/opc-loop-engineering/wiki/`（Obsidian 兼容）
- 27 个 markdown 文件，`.obsidian` 配置完整
- 远程仓库：`https://github.com/jjdeng-hub/hermes-loop-engineering.git`
- 之前没有定时备份，内容未自动写入

### 新增
- 备份脚本：`/root/.hermes/scripts/vault-backup.sh`（git add -A + commit + push）
- 定时任务：`vault-backup`（0 */6 * * *, no_agent 模式，静默推送）
- 首次备份：8 个文件已推送到 GitHub（2026-06-29 07:32）

### Auto-Save 工作流（新规）
以下情况必须自动写入 vault：
- 关键决策定稿 → `points/YYYY-MM-DD-标题.md`
- 新增实体/工具/平台 → `entities/entity-name.md`
- 新增概念 → `concepts/concept-name.md`
- 每次写入必须同时更新 `log.md`（动作日志）和 `index.md`（目录索引）
