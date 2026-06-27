# Loop Engineering 核心知识库

## 定义（Jerry 修正版）

> 在工作流的合理节点嵌入有质量的反馈修正回路，让系统自动收敛到更优的结果。

对比业界定义（cobusgreyling/loop-engineering repo）：
> 设计一个系统来替你 prompt agent，而不是手动 prompt。

## 四代演变

Prompt → Context → Harness → Loop

## 五大构件 + Memory

| 构件 | 在循环里的角色 | Hermes 对标 |
|------|---------------|------------|
| **Automations** | 定时触发发现+分诊 | cronjob 工具（自然语言调度、skill 加载、多渠道投递、链式作业） |
| **Worktrees** | 并行执行互不干扰 | ❌ 无内建支持，手动 git worktree |
| **Skills** | 持久化项目知识 | ✅ skill_manage + SKILL.md |
| **Plugins/Connectors** | 打通真实工具 | ✅ MCP |
| **Sub-agents** | maker/checker 分离 | ✅ delegate_task |
| **Memory/State** | 跨会话的持久状态 | ✅ memory + SOUL.md |

## 关键人物

| 人物 | 来源 | 核心观点 |
|------|------|---------|
| Peter Steinberger | loop-engineering repo | "You should be designing loops that prompt your agents" |
| Boris Cherny | Anthropic Claude Code head | "I don't prompt Claude anymore. I have loops running that prompt Claude" |
| Addy Osmani | 权威文章（2026-06-07） | "Build the loop. Stay the engineer." |
| Eric Traut | OpenAI Codex | Ralph loop 模式 /goal 的作者 |

## 7 个生产模式

| Pattern | 风险 | 最适合 |
|---------|------|--------|
| Daily Triage | 低 | 每日优先事项快照 |
| PR Babysitter | 中 | 监督 PR 流程 |
| CI Sweeper | 中高 | 修复 red CI |
| Changelog Drafter | 低 | 自动生成发布说明 |
| Post-Merge Cleanup | 低 | 合并后清理 TODO |
| Dependency Sweeper | 中 | 安全依赖更新 |
| Issue Triage | 低 | 问题分类 |

## 安全等级

L1 报告 → L2 辅助修正 → L3 无人值守

## 反模式（Anti-Patterns）

| 反模式 | 导致 |
|--------|------|
| 同 agent 负责实现和验证 | 确认偏差（Verifier Theater） |
| 无尝试上限 | 无限循环、token 烧光 |
| 无状态文件 | 每次运行都失忆 |
| 所有运行都通知 | 通知疲劳 |
| 无范围限制（路径 allowlist） | 越权操作 |
| 无运行日志 | 无法排查 |

## 原始资源链接

- GitHub: https://github.com/cobusgreyling/loop-engineering (425★, MIT)
- Addy Osmani 权威文章: https://addyosmani.com/blog/loop-engineering/
- Substack 文章: https://cobusgreyling.substack.com/p/loop-engineering (网络受限可能访问不到)
- Hermes 文档: /home/jjdeng/.hermes/hermes-agent/website/docs/
