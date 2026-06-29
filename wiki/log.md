# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`

## [2026-06-29] auto-capture | Tom SOUL 升级 (7→9节), 飞书5Bot群组成立, 飞书Bot间@机制限制发现

## [2026-06-27] create | Wiki initialized
- Domain: Hermes 配置 / OPC / Loop Engineering
- Structure created with SCHEMA.md, index.md, log.md

## [2026-06-27] create | 5 wiki pages
- entities/hermes-config.md — 完整配置架构
- entities/daily-automation-loop.md — 自动化流水线
- entities/cloakbrowser-lupin.md — 爬取方案
- concepts/loop-engineering.md — Loop Engineering 核心知识
- concepts/memory-architecture.md — 记忆架构设计
- WIKI_PATH set to /root/.hermes/wiki

## [2026-06-27] ingest | agency-agents-zh (266 agents)
- 克隆到 /opt/agency-agents-zh/
- 312 个文件，20 个部门
- 新增 wiki 页面: entities/agency-agents-catalog.md

## [2026-06-29] auto-capture | Tom SOUL 升级 (7→9节), 飞书5Bot群组成立, 飞书Bot间@机制限制发现

## [2026-06-29] auto-capture | 五路角色跨 profile 扫描：Tina Soul/Learner SRS+英语/Creator管道/Fitness睡眠诊断/全员进化推动

## [2026-06-29] 修复 | model-sherpa NoneType bug + vault 自动备份
- 修复 model-sherpa __init__.py:2465 和 2620 两处 `error_message.strip()` 未处理 None 的崩溃
- 新增 vault 自动备份脚本: ~/.hermes/scripts/vault-backup.sh
- 新增 cron task: vault-backup（0 */6 * * *, no_agent, 静默推送）
- 建立了内容自动保存到 vault 的工作流规则

## [2026-06-29] fix | hermes-auto-update cron 死因分析
- 6AM 的 auto-update 实际触发了，但因 DeepSeek API 不稳定 + model-sherpa 崩溃 + git 历史错乱 + gateway 重启导致未交付
- model-sherpa 已修复

## [2026-06-29] update | 五路并行角色体系搭建
- [[points/2026-06-29-五路并行角色体系搭建]] — 完整变更记录
- Creator SOUL.md 重写：痕迹催化剂定位
- Learner SOUL.md 重写：AI 原生学习引擎
- Fitness SOUL.md 重写：身体导师定位
- Tom SOUL.md 新增「自主进化」+「第六感：Vault 更新」章节
- 技能裁剪：四个角色精简技能栈（Tina: 16删剩1, Creator: 12删剩5, Learner: 14删剩3, Fitness: 16删剩1）
- Bot 互见：Tom=all / 其他=mentions
- [[entities/五路并行角色体系]] — 新建角色体系文档

## [2026-06-29] restructure | Vault 升级为 Second Brain
- 引入 [[AGENTS.md]] — AI 代理操作规范
- 引入 MANIFEST.md 自动索引系统（scans every directory）
- 新增 Inbox/ Projects/ Archive/ 目录
- 合并 entities/ concepts/ comparisons/ 到 Knowledge/
- 新增 sync-manifests.py 自动生成脚本（cron 每6h同步）
- vault-backup.sh 集成 MANIFEST 同步步骤
- [[SCHEMA.md]] 全面更新
- 所有角色 SOUL 移除 vault 路径（由 Tom 统一管理）
|- 新增 vault-capture cron（每2h自动扫描会话，写入 Inbox/）

## [2026-06-29] auto-capture | 冗余工具卸载 + 最终技能栈确认
- [[Inbox/auto-2026-06-29-14]] — SkillClaw + sibyl-memory 卸载决策
- 理由：Hermes 已有 skill_manage / fact_store / memory 等原生等价物
- 最终技能栈：25 Hermes skills + 3 external (youtube-full, obsidian-cli, avoid-ai-writing)
- hermes-agent-self-evolution 保留（Nous 官方包，不占资源）
|