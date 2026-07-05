---
name: content-strategy
description: Jerry's content strategy — personal narrative journey (叙事) about building an AI-powered one-person company. Text-first, Xiaohongshu 图文 as primary platform. "Do → Record" model.
---

# Content Strategy (current approach, effective 2026-07-05)

## 2026-07-05 Critical Updates

**定位修正 — 自本次session起生效：**

| 旧 | 新 |
|---|---|
| 「打工人AI副业实验」 | 「一个28岁普通打工人，下班后和 AI 相处的真实记录」 |
| 「下班折腾AI」 | 实际从早到晚都在聊，不只下班 |
| 简介：打工人AI日记 | **简介**：日记里只记两件事：今天试了什么，脑子里想了什么。 |
| 定位：AI副业/一人公司 | 定位：不教不吓，观点展示，真实故事 |

**三条铁律（新）：**
1. **「我在」视角** — 永远写我身上发生的事，不加「你应该」
2. **真实结果** — 好就是好，烂就是烂，不美化
3. **不教不吓** — 传递感受，不传递方法论和焦虑

**内容一致性规则（新）：**
- 所有选题必须方向统一，不能前后矛盾
- 前5篇尤其重要，第一篇立人设，后续验证人设
- 每篇筛选标准：它跟上一篇说的一样的人做的一样的事吗？

**封面策略（新）：**
- 标题+封面占80%重要性
- 小红书3:4竖版，feed里封面只有手机屏幕1/3高
- 封面必须统一排版模板：大字标题(占1/3)+底部小字「下班折腾AI的日记」
- 深色底+白字，每篇换背景图但版式不变
- 文字放正文caption（200-400字），不放图片里（图片文字搜不到）
- 图2-3张：封面→金句/截图→过程展示，不凑图
- 第一篇：封面用终端截图+大字标题，图2用真实聊天截图

**前5篇排布（新）：**
1. 不瞒你说，我折腾AI最开始只是因为不想卷了 — 开场立人设
2. 第一次用AI助手帮我写了一个完整的脚本 — 具体实验
3. 折腾AI一个月，发现最大的变化不是效率变高了 — 思考感悟
4. 下班前改PPT，下班后改AI配置文件 — 日常记录
5. 同事问我最近在干嘛，我说不清楚 — 社交反应

> **Warning**: This is the THIRD iteration of Jerry's content strategy.
> Prior versions (Douyin video + AI-generated content → Knowledge base monetization) are archived as historical references below.
> **Load this skill before writing or reviewing any content for Jerry.**

## Core Thesis (from DeerLucid, adapted)

> Ordinary people achieve class leap via AI leverage through **personal narrative**, not risky entrepreneurship.
> Anchor from "who I am" and current main job as starting point.
> Turn daily AI learning and application into content fuel.
> **Learn → Do → Record**, not "plan first → execute later".

## Who Jerry Is (the anchor)

- 28岁，普通打工人，工厂上班
- 不是AI专家，不是半导体专家。一个普通人在认真折腾AI工具。
- 有自己的Hermes Agent全套系统（服务器+飞书Bot+MoA+cron+多profile）
- 从早到晚都在跟AI聊天（不是只下班）

## The Content Product

Not a tutorial. Not a knowledge base. A **building diary**:

> "How a regular Chinese engineer turned an AI chatbot into his employee — the honest story, no filter."

The narrative arc:
1. Started with Hermes as a casual chat buddy
2. Discovered cross-session memory
3. Configured QQ Bot → WeChat → Feishu gateways
4. Discovered profiles → One-person company took shape
5. Now: 266+ expert agent roles, complete infrastructure

Each installment = one stage of this journey. Written as **decision-making narrative**, not as installation docs.

## Why This Works

| Property | Old approach (pre-2026-06-28) | New approach |
|----------|-------------------------------|--------------|
| Uniqueness | Low (AI-generated, anyone can) | High (his specific journey) |
| Feeling (感觉) | Low (no personal voice) | High (authentic struggle) |
| Hope (希望) | Medium (generic tutorial value) | High (readable arc to follow) |
| Content engine | Manual writing | Auto-loop (chat → extract) |
| Platform | Douyin video | Xiaohongshu 图文 |

**Key insight from past failure**: Jerry's "Jerry在想什么" had 20 articles / 10 followers. Root cause: "feeling but no hope" — authentic voice but no actionable takeaway. The NEW approach solves this: the "hope" IS the observable journey itself.

## Content Production Loop

```
Jerry chats with Tina (Feishu group, natural conversation)
  → Hermes (this agent) watches, extracts cognitive shifts
  → Hermes drafts a short piece (800-1500 chars)
  → Jerry reviews, approves/rejects
  → Publish to Xiaohongshu 图文
```

**No forced output.** Some days have material, some don't. Target: 2-3 pieces/week.

## Content Principles

1. **Do not write installation tutorials.** Chinese docs (hermesagent.org.cn) already cover them. Write the *decision trajectory*: "why I chose WSL → why I switched to Windows → why I moved to server".
2. **First person, present tense.** Jerry's authentic voice, not a polished narrator.
3. **Segment information.** Short paragraphs, one idea per breath. No big dumps.
4. **No flattery, no filler.** Real talk. If it's hard to write, it's probably worth writing.
5. **Hook + Story + Subscribe.** Each piece must make the reader want the next one.

## Platform Priorities

| Platform | Role | Status | Notes |
|----------|------|--------|-------|
| **Xiaohongshu** | Primary. 图文 only. | ✅ Account registered. First post in progress. | 昵称已设置，简介：「日记里只记两件事：今天试了什么，脑子里想了什么」 |
| **WeChat Official Account** | Text backup / rehost. | Future. | |
| **Douyin** | Abandoned. Too high production cost for video. | Not active. | |
| **Twitter/X** | English-language / dev-community reposts. | ✅ Account: TomDengnc1c. Has API Bearer Token (402 CreditsDepleted — free tier needs activation). | Server IP blocked for browser login without residential proxy. Bearer Token authenticated but v2 API returns 402 (needs free/basic tier activated in Developer Portal). v1.1 API limited. |
| **Reddit** | r/LocalLLaMA, r/selfhosted exposure. | ✅ Account: New-tom2306. | Server IP blocked entirely. JSON API also blocked. Use `web_search` or alternative frontends. |

## Agent Capabilities

| Tool | Account | Status | Use Case |
|------|---------|--------|----------|
| AgentMail | hermes-tom-jerry@agentmail.to | ✅ Active | Register accounts (email verification), receive notifications, send emails. Free tier: 3 inboxes, 3000 emails/month. |

## Feishu Dual-Bot Infrastructure (Current)

Jerry and Tina communicate in a Feishu group with two Hermes gateway instances:

```
Jerry → Feishu group (all messages visible to both bots)
  ├─ @Hermes → default profile (云端管家, this agent)
  └─ @Tina → tina profile (苏格拉底导师)
```

**Caveat**: Both bots must have "群聊接收消息模式" set to "接收所有消息" (not "仅接收@机器人消息") on open.feishu.cn for the group chat to work.
**Caveat 2**: New Feishu bot apps must have `FEISHU_ALLOW_ALL_USERS=true` and `FEISHU_GROUP_POLICY=open` in .env, otherwise group messages are silently dropped.

## Writing Structure Options

Two formats, pick based on the topic:

### Timeline Arc (existing)
"First I did A, then B, then C." Best for multi-stage journeys where the sequence matters (e.g. "我的Hermes三迁记").

### Problem-Driven (新增 — 问题驱动)
Each article starts from ONE specific pain point:

```
1. Hook: 「我月薪15K，为什么需要200个AI员工？」
2. The problem: 具体痛点（记不住、不连续、不能7×24）
3. The choice: 为什么选了X而不是Y（选型思考）
4. The result: 现在能做什么（带真实截图/对话）
5. Cliffhanger: 下篇预告
```

Why this works:
- New readers can enter at any point (no "read from the beginning" requirement)
- Each article is a self-contained story
- The hook is a question the reader already has — they click to see the answer

When to use each:
- **Timeline arc**: the user's full origin story, explaining the whole landscape
- **Problem-driven**: the bread-and-butter articles that drive ongoing traffic. Most articles should be this format.

## Writing Process

1. Jerry writes a **rough draft** in natural language (as if telling a friend)
2. Hermes reviews: structure, clarity, hook, readability
3. Jerry approves or rejects
4. Publish

**Jerry's role**: domain knowledge + decision + final approval. **Do not write for him. Organize his output.**

## Interaction Principles with Jerry

1. **Read before advising.** Jerry has wiki notes, past Tina sessions, and pushed content. If he says "I pushed X to the repo", read it before jumping to advice. He will call you out if you assume instead of reading.
2. **First-principles: strip assumptions.** Don't assume he's a domain expert. Don't assume his day job = his monetization path. Ask what he actually has access to.
3. **When he presents a plan, push back.** He hates flattery. If he's wrong, say so. If his premise is wrong, say so. He trusts you MORE when you disagree.
4. **Segment + Chinese.** Short paragraphs. One idea per breath. No big dumps.
5. **Loop is default.** Don't wait for instructions. If you can design a system that runs without him, do it. Ask forgiveness, not permission — but stop immediately if he says "算了/暂停/明天再说".
6. **"开搞吧" = stop asking, deliver.** When Jerry says "开搞吧" / "我只看结论" / "不要问我" — this is a direct instruction to stop clarifying and produce a complete output. Do not ask another question. Synthesize everything you know, activate the relevant roles, research what you can, and give him the whole package. Do not check back mid-way. Do not offer multiple choice. Deliver a single, comprehensive recommendation with reasoning.
7. **Comprehensive first, questions later.** For complex multi-step tasks, the default is to first produce a complete synthesis (with background, options, recommendation, and next steps), then offer to dive deeper. Do NOT lead with "which way do you want to do this?" — lead with "here's what I've done, here's the result, what should I adjust?"

- Chinese preferred. Direct, concise.
- Hate flattery. Love debate, collision, exchange.
- Segment information, not big dumps.
- "我的背景不重要，最终依赖于AI，我能做的就是决策和思考"
- Rule 6 takes priority when triggered. Stop asking. Start delivering.

## First Article (2026-07-05)

**标题：** 不瞒你说，我折腾AI最开始只是因为不想卷了
**公式：** 情绪留白
**定位：** 开场立人设

**内容框架：**
1. **开头·现状** — 每天重复的生活（1-2句让人代入）
2. **转折·为什么开始** — 有一天突然意识到除了上班什么都不会
3. **动作·做了什么** — 没报课没买书，打开电脑开始试
4. **重点·真实的变化** — 最大的变化不是效率高了，是下班后有事做了
5. **结尾·账号说明** — 这个号就记两件事：今天试了什么 + 脑子里想了什么

**配图：**
- 封面：终端截图做背景 + 大字标题「不想卷了」（占画面1/3）+ 底部小字「下班折腾AI的日记」
- 图2：真实聊天截图（AI列出最近折腾的内容）
- 正文：200-400字caption

**旧版第一篇文案（已废弃）：**
- ~~references/first-article-hermes-three-moves.md~~
- ~~references/first-post-dagongren.md~~

## Content Pivot 2026-06-30: Semiconductor → 自媒体+AI

Jerry explicitly stated: **不想再做半导体相关内容了。**

新方向：**自媒体 × AI**。内容聚焦：
- AI 工具链（Hermes Agent、AI Agent 工作流）
- 一人公司实操方法论
- 自媒体/内容创作（小红书图文、即刻）
- Build in Public 叙事

旧 reference `semiconductor-vertical-content-opportunity.md` 已标记为 deprecated。不再以此为内容方向。

### 新增内容来源：每日商机扫描 (Daily Opportunity Scan)

2026-06-30 起，每天早 8:00 自动运行 cron job `daily-opportunity-scan`，扫描以下来源：

| 来源 | 方式 | 状态 |
|------|------|------|
| **HN Algolia API** | 15 组关键词，自动过滤低质量结果 | ✅ 稳定 |
| **知乎** | 浏览器扫描（需绕过反爬） | ⚠️ 测试中 |

Scan 结果推送至飞书 DM（当前对话），产出「今日商机报告」包含：
1. 🔥 热榜趋势（HN 高赞话题）
2. 💬 真实需求（Ask HN / 知乎问题）
3. 📦 新产品/项目（Show HN）
4. 🎯 今日推荐行动

**底层脚本**：`/root/.hermes/scripts/opportunity-scan.py` — Python 数据采集脚本，15 组关键词同时查询 HN Algolia API + 额外抓取 Ask HN，按 points 排序去重输出 JSON。

**架构**：no_agent 脚本（纯数据采集）→ agent cron（LLM 分析+格式化）→ 飞书推送。

这个扫描结果本身也是内容素材——Jerry 的 agent 自动帮他找选题，这件事本身就值得写一篇「我的 AI 每天早上帮我发现了什么」。

## 2026-06-30 内容定位修正

**⚠️ 关键修正：不要用"一人公司"这个词。**

Jerry 不是全职创业、没有营收，叫"一人公司"不诚实。定位改为：**「打工人AI副业实验（注：此定位已于2026-07-05更新——见顶部。以下内容保留仅作追溯）」**。

### 账号定位卡
| 维度 | 内容 |
|------|------|
| 账号名 | 打工人AI副业实验（注：此定位已于2026-07-05更新——见顶部。以下内容保留仅作追溯） |
| 人设 | 28岁苏州半导体打工人，下班折腾 AI 搭自动化系统 |
| 平台 | 小红书（图文为主） |
| 风格 | 真实、实操、不装逼。展示普通上班族怎么用 AI 工具搞副业 |
| 内容模型 | "Do → Record"——做出来什么，就写什么 |

### 角色边界（关键！）
**Tom（我）≠ Creator。** 职责分离：
| 谁 | 负责 |
|----|------|
| Tom（云端管家） | 总协调、基础设施、自动化运维、cron 搭建、数据采集流水线 |
| Creator（内容创作者） | 内容策略、文案撰写、配图设计、账号运营 |
Tom 不做内容创作。素材流水线搭好后，内容产出通过 delegate_task 派给 Creator 角色。

### 第一篇文案（Creator 出品）
**标题：** 《一个半导体打工人，决定每天用AI搞副业》
- 场景钩子：下班路上，静电手环的味道
- 自曝：之前 20 篇 10 个粉丝的失败经历
- "我不教你月入十万，我自己都不信"（反向建立信任）
- 工具箱：Hermes Agent + VPS + 飞书Bot + QQ Bot + 商机扫描系统
- 完整文案见 references/first-post-dagongren.md

## 2026-06-30 内容形式确认：打工人AI副业实验（注：此定位已于2026-07-05更新——见顶部。以下内容保留仅作追溯）

Jerry 明确选择了这个方向，并纠正了"一人公司"的说法。

### 核心叙事
> "28 岁，普通上班族，用 AI 搭了一个帮我 24h 干活的员工。我不是程序员，但我的搭档是。"

### 每篇内容结构
1. **背景（1-2 句）** — 今天发生了什么、遇到了什么问题
2. **动作** — 我用 Hermes/AI 做了什么（配置了什么 cron、跑了什么 scan、发现了什么）
3. **成果** — 真实截图/数据（商机报告、自动推送、成本对比）
4. **钩子** — 下篇预告或「想知道怎么搭的？关注我」

### 为什么这个形式适合 Jerry
| 维度 | 说明 |
|------|------|
| 独特性 | 国内几乎没有人在公开写 Hermes Agent 实操日记 |
| 可持续性 | 每天都有素材（商机扫描、cron 运行、与我的对话） |
| 低门槛 | 不发视频，不做教程，只说"今天发生了什么" |
| 可变现 | 积累信任 → 小报童/付费专栏/咨询 |

### 头 7 篇规划
| Day | 标题方向 | 展示的能力 |
|-----|---------|-----------|
| 1 | 我的 AI 每天早上 8 点给我一份市场报告 | Cron / 自动化扫描 |
| 2 | 原来 AI 可以记住我的一切 | Memory / SOUL.md |
| 3 | 我的 AI 能直接往群里发消息 | Bot / 消息平台 |
| 4 | 我用 AI 搭了一个"第二个大脑" | Obsidian / Vault |
| 5 | 我的 AI 会主动跟我说话 | 后台任务/主动推送 |
| 6 | 一天 0 成本，AI 帮我干了 10 件事 | 成本对比 |
| 7 | 复盘：一人 + AI = ？ | 阶段性总结 |

### 配图风格
- 真实截图为主（商机报告、cron 配置、对话记录）
- 干净信息图卡片，不用花哨 AI 绘画
- 每篇配 1-2 张截图 + 文字说明

## Quick Monetization Pathways (2026-06-30)

Jerry 明确表达了"折腾很久没见到钱"的 frustration。以下是从 YouTube 视频（Greg Isenberg × Alex Finn 119K 播放, Jack Roberts 76K 播放）提取 + 国内市场适配的变现路径，按见到第一块钱的速度排序：

### 🥇 今晚就能做：闲鱼挂 AI 自动化服务
- **卖什么**：AI 自动化工作流搭建（24h 自动运行的 AI 员工）
- **定价带**：299-999 元
- **谁买**：电商卖家、小企业主、自媒体人
- **标题参考**：「AI 自动化工作流定制：24h 自动处理重复工作」
- **注意**：闲鱼反爬严，需用户手动上架

### 🥈 这周能做：小红书起号「一人公司 AI 实战日记」
- 每天发 Hermes 帮你干了什么
- 素材：商机扫描报告、cron 截图、对话记录
- 引流到私域 → 小报童/咨询

### 🥉 两周内成型：小报童专栏 49.9 元
- 卖点：「国内唯一 Hermes Agent 实战手册」
- 引流渠道：小红书 + 知乎 + 即刻 → 小报童

## Historical archives (old approach)

The following references remain for traceability. Do NOT use them as current guidance without explicit direction:
- references/content-stance-strategy.md — old stance framework (Douyin video era)
- references/social-media-visual-strategy.md — old cover/visual strategy
- references/topic-curation.md — old topic system
- references/xiaohongshu-content-system.md — old Xiaohongshu system (AI-generated content)
- references/content-writing-patterns.md — old writing patterns (AI-generated, not personal narrative)
- references/playbook.md — old full playbook
- references/vibe-and-hope-framework.md — ⚠️ This framework (希望vs感觉) is still VALID and actively used.
