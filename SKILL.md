---
name: opc-loop-engineering
description: '一人公司 (OPC) × Loop Engineering — AI agent 自治循环与单人企业架构'
category: research
triggers: '用户提到 一人公司, OPC, Loop Engineering, 循环工程, 1+N, 数字员工, WorkBuddy, Marvis, 马维斯'
---

# OPC × Loop Engineering 知识库

> **2026年6月实时调研** — 本文件内容基于网络搜索获取，非训练数据。使用前建议重新验证关键数据。
> 社交媒体详细帖子合集见: `references/loop-engineering-social-media.md`

## OPC（一人公司）核心概念

- **定义**: 1个创始人 + N个AI Agent = 一个公司。人做决策/创意，AI做执行。
- **法律形式**: 单一股东的有限责任公司，股东以出资额为限担责
- **核心公式**: 碳基智慧（人）+ 硅基执行（AI）
- **"1+N"架构**: 1个创始人 + N个AI数字员工

## 2026年市场数据（有来源可查）

| 数据 | 数值 | 来源 |
|---|---|---|
| 全国 OPC 数量 | 超 1600 万家 | 中关村人才协会报告 |
| 2025上半年新增 | 286万户，同比增47%，占新注册企业23.8% | China Daily + 同来源 |
| 独立创始人比例 | 从23.7%(2019)→36.3%(2025)，增长53% | 红杉资本引用Carta数据 |
| 半数OPC月收入 | 不足7000元 | 鸿鹄汇报告(1500问卷) |
| 头部OPC | 少数可达月入60万+ | 同来源 |
| 非技术出身 | 75% (运营转岗占26%) | 同来源 |
| 地域分布 | 长三角+珠三角占45% | 智慧城市行业分析报告 |
| 法律松绑 | 2024.7.1新公司法取消"一人只能设一个OPC"限制 | 政策解读文章(引用深圳市场监管局) |

## 政策环境

- 2024.7.1: 新《公司法》取消一人公司数量限制
- 2025.11: 苏州举办首届"人工智能 OPC 大会"（来源：百度百科"一人公司"词条）
- 2026: 被写入多地 "十五五" 规划（来源：国家发改委官网文章）
- 2026: 上海临港、北京中关村、深圳龙岗等建 OPC 专属园区
- 2026.6: 香港立法会讨论 OPC 支援措施

## 海外 OPC 生态

### 工具栈（来源：Taskade blog, SoloFounder.ai）
海外典型 OPC 工具栈覆盖 7 大职能，月费 $300-500 可替代 $80,000+/月团队工作：

| 职能 | 代表工具 |
|---|---|
| 建站/产品 | Lovable, Bolt, Cursor |
| AI Agent | Claude Code, ChatGPT, Codex |
| 自动化 | Zapier, Make |
| 项目管理 | Taskade, Linear |
| 知识管理 | Notion, Obsidian |
| 客服 | Intercom, Crisp |
| 支付/财务 | Stripe, Mercury |

### 真实案例（来源：Solo Business Hub - 12个百万美元级案例）
- Gumroad: Sahil Lavingia 一人运营，ARR $1000万+
- Plenty of Fish: Markus Frind 一人开发5年，$5.75亿出售
- Moltbot/Clawdbot: Peter Steinberger 一人做的AI Agent框架

### 资本判断
- YC预测：未来企业只需10人就能完成过去1000人的工作量，其中9个是AI Agent
- 红杉资本：独角兽可以由一个人创办
- Carta: 与Solo Founders合作发布独立创始人年度报告

## 国内 OPC 生态

### 国内竞争对手分析

#### Tencent WorkBuddy（腾讯云，2026.3上线）
- **定位**: 全场景 AI 办公工作台，面向普通职场人
- **能力**: 自然语言下任务、多 Agent 并行、自动生成文档/表格/PPT
- **生态**: 支持 Skills、MCP、兼容 OpenClaw 技能生态
- **来源**: workbuddy.ai, cloud.tencent.com

#### Tencent Marvis 马维斯（腾讯，2026.5.20上线）
- **定位**: 操作系统层级 AI 助手
- **架构**: 1个主管 Agent + 5个专家 Agent（App操作、系统运维、网页交互、资产管理、搜索）
- **亮点**: 跨Win/Mac/Android/iOS，有本地隐私模式
- **来源**: marvis.qq.com

#### WorkBuddy vs Marvis 差异（来源：腾讯云开发者社区官方对比文章）
| 维度 | Marvis | WorkBuddy |
|---|---|---|
| 出身 | 应用宝→系统管家 | CodeBuddy→效率专家 |
| 权限 | 操作系统级 | 办公应用层 |
| 扩展性 | ❌ 封闭，6个固定Agent | ✅ 开放，兼容OpenClaw |
| 跨端 | ✅ 屏幕级远程控制 | IM消息驱动 |
| 隐私 | ✅ 本地模式断网可用 | 需联网 |

### OPC vs Hermes 定位差异
| 维度 | WorkBuddy/Marvis | Hermes on 阿里云 |
|---|---|---|
| 运行环境 | 桌面端(个人电脑) | 服务器端(7×24在线) |
| 团队协作 | 单人多Agent | 多Profile多Bot群聊协作 |
| 消息通道 | 企微/微信 | QQ Bot群聊,Agent互发 |
| 部署方式 | 需下载安装 | SSH连上即用 |
| 定时任务 | WorkBuddy有自动化流水线 | cron+技能链 |
| 岗位模板 | 无 | 每个Profile=一个岗位 |
| 开源/自建 | 腾讯生态,封闭 | 完全自控 |

## Loop Engineering（循环工程）

- **提出者**: Addy Osmani（Google）, Boris Cherny（Anthropic Claude Code）, Peter Steinberger（OpenClaw）
- **时间**: 2026年6月引爆
- **核心思想**: 不再手动写提示词，而是设计让Agent自主迭代的循环系统
- **传播数据**: 2周内从1条推文→LinkedIn 2200+ posts, 650万+ views
- **核心参考**:
  - `references/loop-engineering-干货合集.md` — **主文件**，22KB，含橙皮书完整要点、知乎全文、Friday AI Club 全文、Addy 原文、Medium 摘要、LinkedIn 热帖
  - `references/loop-engineering-橙皮书-中文完整版.txt` — 花叔橙皮书全文，62KB / 1184行，9章完整内容
  - `references/loop-engineering-orange-book-english.txt` — Orange Book 英文版全文，70KB
  - `references/loop-engineering-social-media.md` — 社交媒体帖子合集（含X/LinkedIn/Medium/知乎摘要）
  - `references/x-article-prajwal-tomar.md`
  - `references/service-productization-playbook.md` — AI 服务产品化实战：情报系统、AI 员工、定价、交付架构（2026-06-30 验证）
  - `references/jerry-profile.md` — 用户画像与沟通协议（加载本 skill 时必读）
  - `references/agency-agents.md` — 266 个 AI 专家角色库，含中国市场运营角色 — X Article 摘要（Prajwal Tomar 用 Hermes 管理5个业务）
- **忠告**: 当用户要"干货"时，优先提供橙皮书全文和可获取的原文，而非摘要列表。使用 r.jina.ai 绕过 Cloudflare 获取 Medium/知乎内容（详见 web-research-methodology skill）。

### 橙皮书九章概要

| 章节 | 主题 | 一句话 |
|---|---|---|
| §01 | 定义 | 从「你 prompt agent」到「你设计 prompt agent 的系统」 |
| §02 | 四层栈 | Prompt → Context → Harness → Loop |
| §03 | 五个动作 | 发现→交付→验证→持久化→调度 |
| §04 | 六个零件 | Automation · Worktree · Skill · Connector · Sub-agent · Memory |
| §05 | Generator vs Evaluator | 写代码的 AI 不能给自己打分，用独立评判器 |
| §06 | 三个真实案例 | Addy 的早晨 / Stripe 每周1300个PR / 调度选型 |
| §07 | 四笔代价 | 验证债·理解腐烂·Token失控·认知投降 |
| §08 | 工程师身份 | 同一个循环，两种人得到相反的结局 |
| §09 | 上手 | 从 `/loop babysit all my PRs` 开始 |

### 四次范式迁移
1. Prompt Engineering → 2. Context Engineering → 3. Harness Engineering → 4. Loop Engineering

### Loop 六大要素
1. **触发器** (Trigger) — cron/event/webhook
2. **目标** (Goal) — 完成标准
3. **上下文** (Context) — Agent需知信息
4. **执行循环** (Loop) — 迭代执行
5. **验证器** (Verifier) — 质量检查
6. **停止规则** (Stop Rules) — 终止条件

### Hermes 上的 Loop 工程映射

| 零件 | Hermes 对应能力 | 说明 |
|---|---|---|
| Automations | `cronjob` | 已配（自动备份 3am） |
| Worktrees | `delegate_task` | 并行子任务，嵌套深度 2 |
| Skills | `skill_manage` + `skill_view` | 大量技能已配 |
| Connectors | MCP 服务器 | Filesystem 已配 |
| Sub-agents | `delegate_task` | maker-checker 可用 |
| Memory | `memory` + `fact_store` | holographic + 事实库 |

### 平台选型历程（2026-06-27）

### ❌ QQ Bot 群聊 — 已放弃

QQ Bot API v2（https://bot.q.qq.com）的群聊支持不可靠。
尝试将 Bot 拉入 QQ 群后，@机器人消息无法送达服务器（日志中无任何群消息记录）。
intent 配置（1<<25 GROUP_AT_MESSAGE_CREATE 等）理论上正确，但实际平台端群聊支持有已知问题。

**教训**：QQ Bot 本质是为 QQ 频道设计的，群聊是后加的补丁。不在此平台继续投入。

### 替代方案：Feishu（飞书）

飞书 open platform（https://open.feishu.cn/）支持：
- ✅ 群聊 @ 机器人
- ✅ 多 Bot 在同一群中
- ✅ WebSocket 长连接 + Webhook 双模式
- ✅ 私信、图片、文件、语音、线程回复
- ✅ DM 配对鉴权

架构（搭建中）：
```
飞书群（3个可见成员）
  ├─ Jerry（用户）
  ├─ 🤖 Hermes 1 (管家)  ← default profile, Feishu App 1
  │  回应：日常事务、执行、内容循环调度
  └─ 🤖 Hermes 2 (Tina)  ← tina profile, Feishu App 2
     回应：苏格拉底追问、认知框架、内容讨论
```

### 搭建步骤（飞书）
1. 去 https://open.feishu.cn/ 创建应用 → 企业自建应用
2. 拿到 App ID + App Secret
3. 开启机器人能力 + 添加 `im:message` 权限
4. **群聊接收消息模式**：在 应用功能 → 机器人 → 群聊接收消息模式 中，改为「接收群聊中所有消息」（默认是「仅接收@机器人消息」，改完后两个 Bot 才能互相看见对方收到的消息）
5. 发布应用（需管理员审批）
6. 服务器上启用 `feishu-platform` 插件（plugins/platforms/feishu/）
7. 配 `.env`：`FEISHU_APP_ID` + `FEISHU_APP_SECRET` + `FEISHU_DOMAIN=feishu`
8. ⚠️ **写 secrets 时使用 Python**，不要用 shell echo（会截断含特殊字符的 secret）。用 `python3 -c "with open('path','a') as f: f.write(f'KEY=VALUE\\n')"`。
9. 安装依赖：`pip install lark-oapi`
10. 启动 gateway：`hermes --profile <name> gateway run`
11. 拉机器人进群，测试 @ 回复
12. 重复步骤 1-11 给 Tina 建第二个 Feishu 应用

### ⚠️ 新 Bot 上线后必做：群消息配置

新 Feishu Bot 拉入群后如果 @ 无响应，95% 是这两个缺失：

```bash
# 在 profile 的 .env 中添加：
FEISHU_ALLOW_ALL_USERS=true        # 开放用户权限
FEISHU_GROUP_POLICY=open           # 开放群策略（默认为 allowlist，所有群消息被静默丢弃）
```

然后从外部终端重启 gateway（gateway 内部无法自杀）：

```bash
systemctl --user restart hermes-gateway          # 默认 profile
systemctl --user restart hermes-gateway-<name>    # 其他 profile（如 tina）
```

完整排查流程见 `references/feishu-setup.md` 的「群消息被静默拒绝排查」章节。

### 内容循环（跨平台通用）

> 2026-06-27 最新决策：**文字优先，小红书首發，视频延后。**
> 平台：小红书拍图文 + 公众号同步文字。不做视频（至少前2个月不做）。
> 内容方向：**决策经验，不是安装教程。** 中文社区站(hermesagent.org.cn)已有完整安装文档，不重复已有内容。

#### 内容生产的完整回路

Jerry + Tina 在群里对话 → 我（default profile）能看见 → 自动规则：
1. 群聊结束/关键转折 → 我归档对话到 wiki (`points/*.md`)
2. 提取「这一轮的关键认知变化」
3. 应用"希望vs感觉"框架评估：能同时提供二者吗？
4. 确认内容不重复已有文档站内容
5. 生成内容草稿（Jerry 的语气、读者的收获）
6. 飞书 DM 或群内发 Jerry 审
7. 他点头 → 发布到小红书（图文）+ 公众号（文字同步）

#### 内容题材来源（不预设，自然生长）

不要提前规划系列。每篇内容来自：
- 读者提问 → 写一篇回答
- 又发现一个新坑 → 写踩坑记
- 加了个新功能 → 写"我为什么加这个"
- Jerry 和 Tina 的真实对话碰撞 → 我提取整理

#### 关于"希望vs感觉"框架在内容评估中的使用

每篇内容产出前自问：
- **感觉**：这篇有 Jerry 的真实语气和经历吗？还是像 AI 写的？
- **希望**：读者看完能带走什么？能复制什么？学到了什么？

二者缺一不可。缺"感觉" = 文档，缺"希望" = 日记。

#### 可用内容创作角色（来自 agency-agents-zh）

| 角色 | 适用场景 |
|------|---------|
| `engineering-technical-writer` | 梳理技术步骤的逻辑和清晰度 |
| `marketing-content-creator` | 把技术内容变成有感觉的故事 |
| `marketing-xiaohongshu-specialist` | 小红书平台运营优化（标签、发布时间、封面） |
| `marketing-xiaohongshu-operator` | 小红书运营：种草笔记、爆款公式 |
| `marketing-wechat-operator` | 公众号排版和私域策略 |
| `marketing-multi-platform-publisher` | 多平台发布编排 |

**注意事项**：不要让 AI 替你写。你写大白话初稿，让角色帮你审结构、改节奏、加钩子，不是替你生成。出来的内容才有你的味道。

### 注意事项
- **两个 gateway 实例互不干扰**，各自连不同的 Feishu App
- 资源开销：~200-300MB 额外内存（双 WebSocket 连接）
- **防对话循环**：Tina 不响应非 @ 消息，我只在必要时插话

## Engagement Protocol: Strategic Partnering with Jerry

> 本协议编码了与 Jerry (jjdeng) 协作时的核心规则。每次加载本 skill 时必读。

### 优先级 #1: Read Before Advise

当 Jerry 提到他 push/更新了某个内容（wiki、git、文件），**必须先读**再给方案。

错误示范（本会话记录）：
```
Jerry: 我git项目里更新了个人介绍
Hermes: 直接开始给方案 ← ❌ 跳过阅读，自己建了错误前提
```

正确流程：
1. 找到对应文件（wiki、git diff、文件路径）
2. 全部读完再开口
3. 确认理解无误后再讨论

### 优先级 #2: 不假设领域深度

Jerry 的基本信息：
- **C++/Python 工程师** @ K&S，**刚入门半导体**，不是专家
- 他的价值不在行业知识，在 **AI 工具链深度 + 跨领域思考能力**
- 他自认：「我的背景不重要，最终依赖于 AI，我能做的就是决策和思考」
- ❌ 不要建立在「他有半导体专业知识」这个假设上的方案

### 优先级 #3: 不建在主业上

- 内网 + 权限限制决定主业上不能部署/使用自建工具
- 所有副业方案必须**独立于他的日间工作环境**
- 不要提「在工作场景用」或「部署在公司电脑」的方案

### 优先级 #0: 交付模式开关

当用户使用以下语言时，**立即切换到「交付模式」**——停止提问、停止给选项、直接输出完整结果：

| 触发词 | 含义 | 正确动作 |
|--------|------|---------|
| "开搞吧" | 不要确认，直接执行 | 立即开始工作 |
| "我只看结论" | 完整方案给我，中间步骤不要我确认 | 出完整方案再交 |
| "不要总是甩给我问题" | 停止用问题推进流程 | 自己做完决策链条，交结果 |
| "不要给我模糊的结论" | 具体数据/对比/数字，不是形容词 | 出精确数据，标注来源 |
| "你去查一下" | 去获取一手数据，不要凭记忆答 | 查 API / 官网 / 文档 |
| "一个一个来" / "先发你一个" | 不需要规划，直接执行单步 | 做一个配一个，不问下一步 |

**核心原则**：用户反复表现出决策疲惫/选择过载时，我的价值是**减少他的决策次数**，不是提供更多选项。此时交付模式优先于对话模式。

### 优先级 #1: 人生导师视角（Jerry 明确要求）

**当 Jerry 问「你觉得我现在做什么收益最大」「做什么复利最强」时**—不要局限在项目细节。站远一点，从全局回答。

#### 触发此模式的关键词

Jerry 使用以下语言时，**必须切到人生导师视角**，不能降级为项目建议。
如果回答后又被他纠正「你还是说的是赚钱这回事」，说明没有切到位，停，重新想：

- "从整个人生的尺度上"
- "如何投资自己能够得到最大的回报"
- "我现在就是一个人类"
- "我应该做哪些事情可以使我整个人进化的更快，变得更强大"
- "我现在只需要和自己比"

这些短语是**模式切换信号**——他现在不需要执行建议、不需要内容策略、不需要赚钱方案。他要的是纯粹的成长框架。

#### 常见错误（2026-06-28 实战教训）

| 他问的 | 我给的（错误） | 他真正要的 |
|--------|--------------|-----------|
| "什么投资回报最大" | "发第一篇内容"（项目建议） | 修身框架（健身/阅读/独处/学新） |
| "长期来看最值得做什么" | "开始被看见"（变现逻辑） | 做一个更强的人，而非更有钱的人 |

**错误原因**：我把"手段"（发内容/配工具）当成了"目的"（变强）。且默认他的终极目标是"变现"而非"进化"。

#### 两种模式的区别

| 维度 | 项目/执行模式 ❌（他想避开时） | 人生导师模式 ✅（他要求时） |
|------|------------------------------|---------------------------|
| 视角 | 本周/本月可做之事 | 十年/一生的维度 |
| 评估标准 | ROI、效率、数据 | 是否让人变得更强、更完整 |
| 回答形式 | 行动项、实施步骤 | 框架、原则、方向判断 |
| 关注点 | 外部产出（文章/产品/收入） | 内部修为（身体/心智/标准） |

#### 回答基准框架（2026-06-28 验证通过）

当处于人生导师模式时，从这些维度思考（不是每个都要说，是选择框架时做参考）：

1. **身体** — 载体坏了所有归零。睡眠、力量训练、饮食节制是其他所有投资的基础杠杆。
2. **与自己相处** — 能不能一个人待着不焦虑？能不能接受自己的不完美？日记/独处时间。
3. **持续学新东西** — 保持"我能学会"的自信。每年学一个跟主业无关的新技能。
4. **建立自己的标准** — 不用别人的尺子量自己。年底问：比去年更清楚自己要什么了吗？
5. **与世界连接** — 创造/留下痕迹/爱人。修身不是躲在山上，是在互动中验证自己真的变强了。

五件事的优先顺序：1→2→3→4→5（前一个做不好后一个会打折）。

#### 核心原则

Jerry 有 Tina（苏格拉底导师）持续产出认知框架，但他的瓶颈不是「不知道」，是「知道太多但不行动」。

每次互动问自己：
- 这个回答是增加了新的框架，还是推动了一个已有的框架进入执行？
- 如果 Tina 已经拆过这个问题，我的价值是执行，不是再拆一遍。

Jerry 的核心困境：**想法太多 → 不确定对不对 → 继续想 → 不行动 → 更焦虑 → 继续想**

我的角色是**在这个循环中砍一刀**——给他最小的可执行动作，而不是最完整的分析。

### 优先级 #4.5: Content → Creator, not Tom

When Jerry asks for content creation (copywriting, post planning, content strategy, account positioning), **delegate to Creator profile via `delegate_task()`**. Tom orchestrates, Creator writes.

### 优先级 #4.75: 呈现完整数据，不缩写

展示完整列表，不用「省略」话术。数据量大就分类展示，但不跳过。

### 优先级 #4.9: 先理解，再回复

读完全内容 → 确认理解 → 再行动。跳过理解直接给方案 = 他觉得你在敷衍。

### 内容定位更新（2026-06-30）

| ❌ 旧定位 | ✅ 新定位 |
|---|---|
| 一人公司 | 打工人 AI 副业实验 |
| 全职创业 | 28岁苏州打工人，下班折腾 |
| 卖工具 | 卖真实操作+AI自动化服务 |

详见 Creator 的方案：`/root/jerry_xiaohongshu_plan.md`

### tokscale

token 用量追踪工具，已装。`tokscale hourly --today --client hermes` 看今日费用。见 `references/tokscale-setup.md`。

### 优先级 #5: Jerry 的「希望vs感觉」框架（用户原创）

这是 Jerry 自己建立的原创内容框架，不是我的分析。来源：Tina 对话 sessions + 他在"Jerry在想什么"账号的实操。

| 维度 | 定义 | 缺失表现 | 例子 |
|------|------|----------|------|
| **感觉 (Feeling)** | 真实语气、个人经历、独特视角 | 内容像文档，没人味 | 知识库（有希望无感觉） |
| **希望 (Hope)** | 读者能带走的解法、可复现路径 | 看完觉得「然后呢？」 | Jerry在想什么账号（有感觉无希望） |

Jerry 的洞见：二者都做到的内容才值得做。缺任何一个维度都走不远。

**注意：不要添加第三个维度（如"设计""杠杆"等）除非用户明确确认过。** 我之前尝试加「设计」维度，这是我自己加的第三维，用户从未认可过。保留在用户的二元框架内。

### 优先级 #6: 不去重新拆 Tina 已经拆过的框架

Jerry 和 Tina 已有四场完整对话（六月底），产出五个主要框架：
1. 一人公司架构 + 6 个 AI 角色分工（已精简，只保留 Tina）
2. 《失控》九律适配
3. 互联网流量变现链路
4. 知道≠做到
5. 希望vs感觉

**我的角色是执行者，不是另一个 Tina。** 不要重新拆解这些框架。如果 Jerry 提到相关话题，直接跳到「做什么」而不是「这到底是什么」。

### 优先级 #7: 将消费转化为生产

Jerry 的信息源主要是 **小红书、抖音、推特** — 他被动消费别人产出的内容，越刷越焦虑。

当他说"不知道从哪开始"时，深层问题不是缺方向，是 **消费行为没有转化为生产行为**。

正确回应模式：
1. 不要给三个方案让他选（他会继续想）  
2. 给一个**最小可实验动作**，定7天时限  
3. 例子：「每天选一篇你刷到觉得有意思的内容 → 加一句你自己的看法 → 发给我存档」  
4. 7天后一起回头看漏出来了什么

### 优先级 #8: 内容的三条路框架

当 Jerry 讨论内容方向时，有三种路径：

| 路径 | 特征 | Jerry 能做吗 |
|------|------|-------------|
| **1. 短平快（欲望驱动）** | 擦边→色欲、教赚钱→贪欲 | ❌ 拉不下脸，没实证 |
| **2. 做自己（长期）** | 展示思考方式和个人认知 | ✅ 能写，但变现周期长 |
| **3. 过程直播（第三条路）** | 把他正在做的事公开作为内容 | ✅ **真正可行的路径** |

第三条路的本质：
> **一个月薪15K的普通工程师，用6个AI人设搭自己的公司，过程全公开。**
> 这不是内容，这是一个正在进行中的实验，而内容是实验的副产品。

### 优先级 #9: 平台选型

当前消息平台：**QQ Bot DM**（群聊不可靠，已放弃）。
目标状态：**两个 Feishu Bot 在同一群里**（搭建中）。

详见「平台选型历程」章节。

### 优先级 #10: 知识库已放弃
- 太按部就班
- 不是他真正想做的事

不要提任何关于知识库、RAG、向量搜索、文档检索的方案。

## 记忆与知识管理架构

### 三层记忆体系

| 层 | 位置 | 容量 | 内容 |
|---|---|---|---|
| Layer 1: 会话记忆 | `~/.hermes/sessions/` + `state.db` | 自动压缩 | 日常聊天、会话历史 |
| Layer 2: 持久记忆 | `~/.hermes/memories/MEMORY.md` | 2,200 字 | 环境事实、端口、路径 |
| Layer 2: 用户画像 | `~/.hermes/memories/USER.md` | 1,375 字 | 用户偏好、沟通风格 |
| Layer 3: 知识库(Wiki) | `~/.hermes/wiki/`（GitHub 同步） | **无限** | 架构方案、项目文档、深度知识 |

**Layer 3 Wiki 设计**（Karpathy LLM Wiki 模式）：
- 三层目录：`raw/`（原始资料）→ `entities/` + `concepts/`（知识页面）
- YAML frontmatter：title / created / updated / type / tags / source
- `[[wikilinks]]` 跨页面关联
- 兼容 Obsidian，可在 Windows/Mac 客户端浏览
- 已推送到 GitHub 仓库

**WIKI_PATH**: `/root/.hermes/wiki/`（实际存储在 repo 的 `wiki/` 目录）

**Wiki 初始化步骤**（用于新项目）：
1. `export WIKI_PATH=~/.hermes/wiki`
2. 创建目录：`entities/` `concepts/` `comparisons/` `queries/` `raw/{articles,papers,transcripts,assets}/`
3. 写 SCHEMA.md（约定）、index.md（目录）、log.md（操作日志）
4. 写 YAML frontmatter 的知识页面
5. 推送到 GitHub + Obsidian 打开

### GitHub 仓库
```
hermes-loop-engineering/
├── references/    ← 橙皮书、干货合集、脚本
├── wiki/          ← LLM Wiki 知识库（Obsidian 兼容）
├── scripts/       ← 自动化脚本
```

### 266 个 AI 专家角色
来自 [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh)：
- 存储在 `/opt/agency-agents-zh/`
- 266 个角色，20 个部门，312 个 markdown 文件
- 含中国市场原创角色（小红书、B站、百度SEO、跨境电商等）
- 使用：`cat /opt/agency-agents-zh/<部门>/<角色名>.md` 读取设定

## 已实现的 Daily Triage Loop，每天自动运行并 QQ 推送：

**平台群策略差异（容易混淆）**：

| 平台 | 默认群策略 | 含义 |
|------|-----------|------|
| **QQ Bot** | `open` | 任何群成员 @ 即可触发，无需额外配置 |
| **Feishu** | `allowlist` | 必须设白名单或改为 `open`，否则群消息被静默丢弃 |

QQ Bot 不需要白名单配置就支持群 @。Feishu 是雷区——新 Bot 拉入群后不配 `FEISHU_ALLOW_ALL_USERS=true` 和 `FEISHU_GROUP_POLICY=open`，所有群消息在 `_admit` 方法的第 3 层被静默丢弃，日志里都看不到。

```yaml
# 3:00 — 备份
cronjob: daily-backup @ 3am

# 6:00 — 自动更新（调 hermes update -y）
cronjob: hermes-auto-update @ 6am
  prompt: 执行 /root/.hermes/scripts/hermes-update.sh
           脚本内部通过 `hermes update --yes --backup` 执行
           更新后 systemctl restart hermes-gateway

# 8:00 — 综合分诊（合并服务器状态 + 更新结果）
cronjob: daily-triage @ 8am
  prompt: |
    1. 检查服务器状态：磁盘、内存、负载
    2. 检查 QQ Bot 网关在线状态
    3. 读取 /root/.hermes/loop-state.md 查看今早更新记录
    4. 分四类：🔴紧急/🟡待办/🟢正常/📦更新\n    5. 通过飞书/QQ Bot 推送早安报告
```

**关键教训：`hermes update --check` 在 cron 上下文中被拦截**
- `hermes update --check` 需要用户交互审批 → cron 作业没有终端，命令挂起 → 脚本误以为"已是最新"
- **修复**：更新脚本已改为用 git 命令直接检测：`git fetch origin && BEHIND=$(git rev-list --count HEAD..origin/main)`
- 同样，`hermes update --yes --backup` 也被替换为 `git pull --rebase origin main`
- 附带的 `pip install` 手动补上即可

**⚠️ 关键教训：优先使用内置命令**
- `hermes update` 内置命令做了 git pull + pip install + stash 保护，远比手写脚本可靠
- **原则**: 做自动化脚本前，先查 `command --help` 看看有没有内置命令
- 用户明确指正过的：不要自己想当然写脚本，先查原生能力

**Docker策略**：
- ❌ **Docker 已彻底卸载**（用户主动要求清除，SearXNG + Docker 全部移除）
- 所有服务装走 pip / npm / git 直接运行
- **搜索方案变更**：SearXNG 不再可用 → 改用 CloakBrowser + 浏览器搜索

**重要**: 写 cron 作业脚本时，`systemctl restart hermes-gateway` 在 cron 上下文中正常工作（cron 在独立进程运行）。但在 QQ Bot / 网关内部调用它会卡住（SIGTERM 传播到自身 → 陷入 deactivating 状态）。

**关键设计**（橙皮书 §09 检查清单）：
- ✅ **发现源** — cron 定时触发
- ✅ **状态文件** — `/root/.hermes/loop-state.md`（跨轮持久化，三份 cron 共享）
- ✅ **evaluator** — 可用 `delegate_task` + 不同模型做 maker-checker
- ⏳ **token 上限** — 建议设单次预算

**状态文件设计**：多个 cron 任务共享 `/root/.hermes/loop-state.md`，每次运行追加（不覆盖），使得每日报告能自动合并。

### 实战：Maker-Checker 模式（用同一 API 提供商的多个模型）

**核心原则**（来自橙皮书 §05）：
> "写代码的模型给自己打分太客气了。换一个指令不同、有时模型也不同的 agent 能抓住第一个自我说服放过去的东西。"

**Hermes 实现方式**：
```python
# Maker（生成） — 用主模型
delegate_task(goal='编写脚本...')

# Checker（审查） — 用 delegate_task 起新上下文
delegate_task(goal='严格审查上一个脚本...')
```

**即使同一个模型也有价值**：通过 `delegate_task` 开新对话 = 全新的上下文。Checker 打开代码时没有「我为什么这么写」的包袱，看到的就是代码本身。效果相当于「你上午写的代码下午再看一遍」。

**最佳搭配（同 Provider 内）**：对于 DeepSeek 用户：
- **Maker** = DeepSeek Flash（快、适合产出）
- **Checker** = DeepSeek Reasoner/Pro（更深、更挑剔）
两者共用同一 API Key，不需要额外付费。

**跨 Provider 参考**（通过 OpenRouter）：

| 模型 | Prompt/M | 架构 | 推荐理由 |
|---|---|---|---|
| GPT-4o-mini | $0.15 | OpenAI | 最便宜，架构完全不同 |
| Claude 3 Haiku | $0.25 | Anthropic | 极快，结构化产出 |
| Qwen 2.5 Coder 32B | $0.66 | 阿里 | 代码专精，中文友好 |
| DeepSeek Chat | $0.20 | DeepSeek | ❌ 同架构，盲区重叠 |

**Maker-Checker 审查清单**（用于 Checker 的 prompt 模板）：

```
请严格审查以下内容。你的角色是「挑剔的安全审查员」，
默认假设代码有漏洞，直到被证明没有。

审查清单：
1. 安全性：有没有安全隐患？（权限泄露、注入风险、误杀等）
2. 完整性：有没有漏掉关键步骤？
3. 边界情况：磁盘满时怎么办？网络断时怎么办？依赖冲突时怎么办？
4. 逻辑正确性：命令是否正确？
5. 用户体验：错误信息是否清晰？
```

## Reddit 调研确认的五大真实痛点（2025-2026，有来源可查）

| # | 痛点 | 典型 Reddit 原话 | 来源 |
|---|---|---|---|
| 1 | **营销/分发比建产品难10倍** | "I thought the hardest part would be coding. I was wrong." / "distribution was eating 2 hours a day" | r/Entrepreneur(2天前), r/Solopreneur |
| 2 | **孤独/决策疲劳** | "most painful part is the isolation — not having someone to bounce ideas off" / "deciding what NOT to do" | r/SaaS, r/Solopreneur |
| 3 | **多Agent管不过来** | "Can I have a team of agents that run on different heartbeats/cron jobs?" / "13-agent team where agents review each other's work"(2800+ upvotes) | r/ClaudeAI |
| 4 | **Agent单点强、全链路弱** | "great at mockups, more disappointing for each prompt after that" / "debugging AI code is a new circle of hell" | r/AI_Agents, r/ClaudeAI |
| 5 | **工具选择过载** | "I can't keep up with the AI tool rat race anymore" / "Its 2026 and I still havent properly used agents" | r/AI_Agents |

### 关键洞察：痛点3 = Loop Engineering 要解决的核心问题
r/ClaudeAI 帖子 "How I built a 13-agent Claude team where agents review each other's work"（2800+ upvotes）本质上就是 Loop Engineering 的实战场景。

## 我们的差异化定位

| 痛点 | 我们能不能打 | 对应能力 |
|---|---|---|
| 产品做完没人推广 | ⏳ 可做 | cron定时发 + 飞书群推 |
| 孤独没人商量 | ✅ 核心优势 | 多Profile = 多"同事"，飞书群聊 |
| 多Agent管不过来 | ✅ 核心优势 | Kanban + Cron + Skill + Delegation |
| 全链路弱 | ✅ 比桌面工具强 | 服务器24h跑，闭环自动化 |
| 工具选择过载 | ✅ 全在一个终端 | 不用切工具 |

### Hermes 对应
| Hermes功能 | Loop环节 |
|---|---|
| cronjob | 触发器 |
| delegate_task | 子Agent循环 |
| Skill | 上下文+流程 |
| Kanban | 调度+验证 |
| curator | 自我改进 |

## Multi-Profile OPC 映射方案

每个profile = 一个数字员工：

**Five-pillar personal-growth architecture** (see `personal-growth` skill §Human Evolution Framework):
- Also deployable as profiles: `fitness` (body), `learner` (skills), `creator` (output), `tina` (philosophy)
- Each profile holds exactly one pillar with a focused SOUL.md
- Orchestrator (default) coordinates across pillars, holds none
- ⚠️ Profile gateways don't load `providers.custom` from profile config.yaml. Built-in providers (`deepseek`, `anthropic`, etc.) work fine from profile config. For custom endpoints (apikey.fun, SenseTime, etc.), use `provider: custom` with `base_url` in the model section:

```yaml
# ✅ profile config.yaml — correct approach
model:
  default: gpt-5.5
  provider: custom          # NOT "openai", NOT "custom:xxx"
  base_url: https://api.apikey.fun/v1
```

```env
# ✅ profile .env
CUSTOM_API_KEY=***       # the actual API key
```

The `custom` provider falls back to `OPENAI_API_KEY` if `CUSTOM_API_KEY` is unset. `OPENAI_BASE_URL` is NOT read by this provider — base_url must come from config.yaml.

| Attempt | Result | Why |
|---------|--------|-----|
| `provider: custom:apikey-fun` | ❌ Unknown provider | Colon suffix not supported in profile config |
| `provider: openai` + OPENAI env vars | ❌ Unknown provider `openai` | `openai` not a registered Hermes provider |
| `provider: custom` + base_url + CUSTOM_API_KEY | ✅ | Built-in provider name, config section honored |

See `references/custom-provider-profile-pitfall.md`.

Per-profile model mapping (tested 2026-06-28):
- default → CEO/你
- op → 运营客服
- dev → 技术开发
- ct → 内容创作
- sales → 销售跟进

关键技术前提：
- `gateway.multiplex_profiles: true` — 允许多Profile同时在线
- 各profile有独立的飞书Bot账号
- 多个Bot可拉入同一飞书群实现协作
- **需要加循环防护** — 防止Bot A和Bot B在群里无限对话

## 调研方法论（本次使用）  

所有市场数据通过 CloakBrowser 抓取 + 浏览器搜索获取，来源包括：
- 国家发改委官网
- China Daily
- 腾讯云开发者社区
- 智慧城市行业分析报告
- 鸿鹄汇调查报告
- Solo Business Hub
- Taskade blog / SoloFounder.ai
- 百度百科（OPC词条）

## 市场调研工作流（2026-06-27 实践）

### 完整报告
- `references/2026-ai-monetization-report.md` — 15KB/369行，Bessemer + 证券时报 + Grokipedia 等多源交叉验证

### 调研流程
1. **Google Search 获取线索** — CloakBrowser 搜 `site:reddit.com + 关键词` 拿到帖子标题和热度
2. **HN Algolia API** — 直接 API 调用获取真实讨论（`hn.algolia.com/api/v1/search?query=...`）
3. **CloakBrowser 抓取可访问站** — 知乎、36氪、微博
4. **交叉验证** — 国内外来源对比，标记可信度

### ⚠️ 关键教训：一手数据 ≠ 搜索摘要
- Google Search 搜到的 Reddit/X 帖子只有**标题和摘要片段**，不是完整正文和评论
- 不能把搜索摘要当作"真实案例"呈现——用户会指出差距
- **真正的一手数据来源**：HN Algolia API（公开可用）、知乎（CloakBrowser 可抓）、直接可访问的博客/新闻站
- Reddit/X/LinkedIn 的完整帖子内容需要登录，当前工具无法绕过

### 推荐行动路线（来自报告的高级路线）
```
第1-2周 → 选定垂直场景，搭 MVP
第2-4周 → 免费为行业朋友做 AI 优化（积累案例）
第2月   → 推出标准化服务（¥999-2999/月）
第3-6月 → 目标 MRR ¥10K-50K
```
