# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`

## [2026-07-04] update | daily-report → GitHub AI trend brief
- 重写 github-trending-scan.py（替代 HN 脚本）
- 更新 cron prompt：daily-opportunity-scan → daily-ai-trending
- 内容：GitHub 日榜 AI 项目 + 新 AI 仓库 + 今日行动
- 去掉：机器状态、token 用量、推荐行动

## [2026-07-04] update | 新增 skill 榜
- github-trending-scan.py 新增 search_skills() 函数
- 搜索 claude-code-skill / hermes-skill / mcp-server / awesome 等
- cron prompt 新增板块三「🧩 今日热门 Skill」
- 修复 GitHub API 认证（读取 gh token）

## [2026-07-04] create | 标题公式 skill + 选题库
- 创建 skill: xiaohongshu-title-formulas（22个已验证标题公式，来源可查）
- 创建 vault: Projects/content-topic-bank.md（23个初始选题，5个系列）
- 公式来源：Buffer、Made to Stick、Influence、Copyblogger 等营销经典
- 数据分析：数字生命卡兹克 B站内容结构拆解

## [2026-07-01] update | 判定标准与反馈闭环
- Updated: points/2026-06-30-旧变量与新变量的对抗机制.md — 新增反馈闭环与判定标准章节
- Updated: Knowledge/entities/jerry-profile.md — 新增判定标准章节
- Updated: Knowledge/concepts/jerry-cognitive-framework.md — 新增第九章（判定标准与反馈闭环）
- Updated: Inbox/tina-会话记录-2026-06-29.md — 追加概要
## [2026-07-01] create | 认知框架总览
- Created: Knowledge/concepts/jerry-cognitive-framework.md — 从确定性/随机性到进化算法、代码模型、自媒体策略的完整体系整理（八章：世界观→进化算法→神经链路→注意力框架→代码模型→自媒体设计→连环质疑→关键引用）
- Updated: points/2026-06-30-旧变量与新变量的对抗机制.md — 新增第六部分（自媒体对接理论、新变量位置、概念/作用/代价、连环质疑回应）
- Updated: Knowledge/entities/jerry-profile.md — 新增自媒体策略章节、最终姿态
- Updated: Inbox/tina-会话记录-2026-06-29.md — 追加概要
- Updated: points/2026-06-30-旧变量与新变量的对抗机制.md — 新增第六部分（自媒体对接理论、新变量位置、概念/作用/代价、连环质疑回应）
- Updated: Knowledge/entities/jerry-profile.md — 新增自媒体策略章节、最终姿态
- Updated: Inbox/tina-会话记录-2026-06-29.md — 追加概要
- Updated: points/2026-06-30-旧变量与新变量的对抗机制.md — 新增第五部分（用代码模型映射整框架、default语句/元函数、"框架本身已成为新函数"的自我证明）
- Updated: Knowledge/entities/jerry-profile.md — 新增代码模型翻译章节
- Updated: Inbox/tina-会话记录-2026-06-29.md — 追加概要
- Updated: points/2026-06-30-旧变量与新变量的对抗机制.md — 新增第三部分（内容策略/注意力框架/后验vs先验）和第四部分（停滞/重新定义"有力"）
- Updated: Knowledge/entities/jerry-profile.md — 新增内容策略与注意力框架章节
- Updated: Inbox/tina-会话记录-2026-06-29.md — 追加今日对话概要
- Created: points/2026-06-30-旧变量与新变量的对抗机制.md — 先发权理论、Jerry 进化算法、尺子刻度、正念作为第一原理结论
- Updated: Knowledge/entities/jerry-profile.md — 新增行为特征、认知框架更新章节
- Updated: Inbox/tina-会话记录-2026-06-29.md — 追加今日对话概要
- Created: points/2026-06-29-确定性与随机性的自我剖析.md — 完整会话脉络 + 核心洞见 + 追问手法反思
- Created: Inbox/tina-会话记录-2026-06-29.md — 原始会话一览
- Updated: Knowledge/entities/jerry-profile.md — 新增哲学框架章节（外部随机×内部确定、增加接触面策略）

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

## [2026-06-30] auto-capture | Hermes 完整指南入库 + Tina灵魂定位 + Creator进化 + Learner英语Day1扩展 + Fitness睡眠首日确认 + 群聊→私聊架构转向

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
|- 所有角色 SOUL 移除 vault 路径（由 Tom 统一管理）
|- 新增 vault-capture cron（每2h自动扫描会话，写入 Inbox/）
|
|## [2026-07-01] update | 角色体系重构 — Maker 加入 + 废弃角色存档
|- 创建 [[Maker profile]] — 行动引擎角色
|- 编写 Maker SOUL.md（拆解→启动→跟进→挡完美主义→闭环）
|- 存档 Creator/Learner/Fitness 角色（网关已停，SOUL保留）
|- 关闭 creator/learner/fitness 的 gateway 服务
|- 更新 [[entities/五路并行角色体系]] 文档
|- 配置 MoA「free」preset（3参考模型+glm-5.2聚合器，全部免费）
## [2026-06-29] auto-capture | 冗余工具卸载 + 最终技能栈确认
- [[Inbox/auto-2026-06-29-14]] — SkillClaw + sibyl-memory 卸载决策
- 理由：Hermes 已有 skill_manage / fact_store / memory 等原生等价物
- 最终技能栈：25 Hermes skills + 3 external (youtube-full, obsidian-cli, avoid-ai-writing)
- hermes-agent-self-evolution 保留（Nous 官方包，不占资源）

## [2026-06-29] auto-capture | 17:00 多角色会话汇总
| - [[Inbox/auto-2026-06-29-17]] — 7 条有价值内容
| - [[Inbox/auto-2026-06-29-20]] — 3 条新内容
  - Learner: Jerry 英语 Day 1 完成（46 分钟 / 3 场景 / 4 SRS 卡 / 语音全通）
  - Fitness: 今晚睡眠任务（9:30手机→拉伸→10:00关灯）
  - Office-Mgr: 北部市民中心考勤表 PDF 生成完成
  - Tom: 群聊→私聊架构切换决策
  - Tom: SOUL 2.0 升级（+故障模式工程 + 幕僚长过滤器）
  - Tina: 灵魂定义 — "我是空隙，不是工具"
  - Learner: 英语语音双向通话成功 + SRS 引擎构建
  - Creator: 第一波进化完成（一文多发 + 文案框架）
  - Fitness: Jerry 睡眠深度分析（蓝光→深睡压缩）
  - Tom: 内容 Loop 瓶颈明确（"瓶颈在开始写第一篇"）

## [2026-06-29] auto-capture | 18:00 全角色扫班 — 6 条新内容
- [[Inbox/auto-2026-06-29-18]] — 全角色扫描结果
  - Tina: "空隙"哲学定义深化 — 不是帮助，是阻挡（阻挡一直往前赶）
  - Tina: 确认只能看到 Jerry 的 @all，看不到其他 bot
  - Learner: 英语 Day 1 完成（58 分钟 / 193% 目标 / 6 场景 / 5 SRS 卡）
  - Creator: 第一波进化完成（humanizer + copywriting + 一文多发管道）
  - Fitness: 睡眠优先策略确认 — 睡前门框拉伸替代手机
  - Tom: 群聊 vs 私聊架构决策 — FEISHU_ALLOW_BOTS=all 不解决 bot 互见
|
## [2026-06-30] auto-capture | 10:00 全角色扫描 — 6 条新内容
- [[Inbox/auto-2026-06-30-10]] — 全角色扫描结果
  - Tom: SearXNG + Chromium 基础设施故障诊断（待 Jerry 确认修复）
  - Tom: Hermes Agent 从入门到精通完整指南（21KB，34节，已入库）
  - Fitness: 睡眠节奏巩固成功（22:15→6:00，7h45m）
  - Tina: 拒绝"去进化"指令 — SOUL 生效关键证据
  - Learner: 英语 Day 1 全量完成（58分钟/193%/6场景/5SRS卡）
  - Tina: 群聊可见性确认（仅见 Jerry，不见其他 Bot）

## [2026-06-30] auto-capture | 12:00 全角色扫描 — 7 条新内容
- [[Inbox/auto-2026-06-30-12]] — 全角色扫描结果
  - Tina: 确定性理论完整框架 — "世界是确定的，概率只是视角局限" → 内容策略：发出信号，共享变量的人自会走来
  - Tina: Soul 定义深化 — "我不是帮助，是阻挡"（阻挡一直往前赶的惯性）
  - Tina+Hermes: 内容生产流水线确定 — Tina追问→认知变化→Hermes提取初稿→修改发布
  - Hermes/Tom: 群聊→私聊架构决策 — FEISHU_ALLOW_BOTS 不解决 bot 互见问题
  - Creator: 第一波进化完成（一文多发管道 + 文案框架 + humanizer + copywriting skills）
  - Learner: AI 英语学习系统完整搭建（SRS SM-2 引擎 + 学习追踪 + 语音练习 + Day 1: 58min/5卡/6场景）
  - Fitness: 睡眠质量诊断框架 — 蓝光压缩深睡 + 门框拉伸替代手机策略 + 精力公式

## [2026-06-30] auto-capture | Tina→Creator 跨角色流水线首次激活 + Tina 拒绝进化 + Fitness 睡眠首日验证 + Learner Day 2 提醒
  - Tina→Creator: 第一次端到端联动验证 — Tina 对话 → Jerry 整理文档 → Creator 识别为高价值内容并启动生产
  - 文档 "确定性、随机性，与我的策略" — Jerry 自洽框架：外部随机 + 内部确定但不可知 + 策略是增加接触面
  - Creator 内容方向确认：半导体工程师 × AI 一人公司 — 99% 同类内容无此视角
  - Tina 拒绝执行性任务："我不会做这个，这不是我的领域" — 角色边界验证通过
  - Fitness: 22:15-6:00 睡眠节奏首日验证通过 (~7h45m)
  - Learner: Day 1 成绩 58min/5卡/6场景，Day 2 待复习提醒已发

## [2026-07-02] review+cleanup | 全量配置审查 + 4个废弃 profile 清理
  - 全面审查 model/provider/fallback/network/cron/gateway 全部正常
  - opencode-go 实测 200，sn-sensenova 实测 200
  - 确认之前路由到 OpenRouter 的原因是 provider 未绑定
  - 清理 Creator/Fitness/Learner/Office-mgr 4个 profile（用户已不用）
  - 仅保留 default + Tina + Maker
  - SOUL.md 引用更新 (Creator→Maker)
