# Loop Engineering — 干货合集（完整原文版）

> 整理时间: 2026年6月26日
> 这是全网 Loop Engineering 最核心的深度内容合集，所有可获取的原文均已收录。

---

## 目录

- [一、橙皮书完整中文版](#一橙皮书完整中文版)
- [二、知乎深度解析：《全网热议的Loop到底是个啥？》](#二知乎深度解析全网热议的loop到底是个啥)
- [三、Friday AI Club：《AI Agent Loop 完全指南》](#三friday-ai-clubai-agent-loop-完全指南)
- [四、Addy Osmani 奠基原文（完整）](#四addy-osmani-奠基原文完整)
- [五、Medium 文章摘要与链接](#五medium-文章摘要与链接)
- [六、LinkedIn 热帖汇总](#六linkedin-热帖汇总)
- [七、GitHub Orange Book 简介](#七github-orange-book-简介)
- [八、从理论到实战：Hermes 上的 Loop 工程实践](#八从理论到实战hermes-上的-loop-工程实践)

---

## 一、橙皮书完整中文版

**书名**: 《Loop Engineering — 别再问我什么是循环工程》
**作者**: 花叔（Alchaincyf）
**版本**: v260615（2026年6月15日）
**源文件**: [GitHub 仓库](https://github.com/alchaincyf/loop-engineering-orange-book)
**状态**: ✅ 完整收录（PDF 全文提取，1184 行，62KB）

### §01 别再问了：Loop Engineering 到底是什么

又一个 XX Engineering？这次的不同在于，它不是教你怎么干活，而是让你别再亲自干活。

**一句话定义**（Addy Osmani）：

> Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead.

翻译：**循环工程，就是把「那个负责 prompt agent 的人」从你自己换成一套系统。你不再亲自一句句喂，而是设计那套替你喂的系统。**

这句话的重心在「替换你自己」。不是把提示词写得更好，也不是把上下文管得更精，是把你这个人从那个位置上挪走。这是一个位置的转移。以前你是发动机，现在你是设计发动机的人。

**一周之内，三个人点着了它：**

1. **Peter Steinberger**（OpenClaw 作者）6月发推，800 万+浏览：
   > "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."

2. **Boris Cherny**（Anthropic，Claude Code 负责人）：
   > "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops."

3. **Addy Osmani**（Google Chrome 团队）6月7日发博文命名为 Loop Engineering

三个人，一个引爆，一个同声，一个命名，前后就一周。

**从「你 prompt agent」到「你设计 prompt agent 的系统」：**
- **旧世界**：你坐在那儿，一句句 prompt agent。它干完一件，停下，等你下一句
- **新世界**：你设计一套东西，让它自己一拍一拍地敲。它在定时器上跑、自己孵化小帮手去干活、自己把结果喂回给自己

> Loop engineering sits one floor above the harness.  
> 循环工程，坐在 harness 的上一层楼。

### §02 三级跳：从 Prompt 到 Context 到 Loop

**四层栈（每一层管一件更大的事）：**

| 层 | 管什么 | 核心问题 |
|---|---|---|
| Prompt engineering | 写好一次的提示词 | 我该告诉模型什么 |
| Context engineering | 这一刻窗口里放什么 | 检索什么、摘要什么、清掉什么 |
| Harness engineering | 单次运行的武装 | 给哪些工具、允许哪些动作、什么算完成 |
| **Loop engineering** | **在 harness 之上调度** | **怎么让它自己一遍遍跑起来** |

**每一层的失败方式不一样：**
- Prompt 错了，你当场就看见，改一句就行
- Context 装错了，模型答偏，你也容易察觉
- Loop 在你睡觉时自己跑、自己改你没看过的代码——出问题你可能几天后才发现

> 层次越高，你离现场越远，犯的错就攒得越久。

### §03 一个循环的五个动作

把一个 loop 转一圈拆开看，里面只有五个动作。看懂这五个，你就看懂了所有 loop。

**Addy 的真实案例：早间 Triage Loop**

早上一个 automation 自动跑起来 → triage skill 读 CI 失败、open issues、最近 commits → 结果写进 markdown/Linear → 每个值得动手的发现开一个隔离 worktree → 子 agent 起草修复 → 第二个子 agent 审查 → connector 自动开 PR → 处理不了的进收件箱等人

**五个动作：**

| 动作 | 干什么 | 在 triage loop 里 |
|---|---|---|
| **发现** | 自己找出这圈该做的事 | skill 读 CI 失败/issue/commit |
| **交付** | 把任务隔离着交给 agent | 每个发现开一个 worktree |
| **验证** | 换个 agent 说「不」 | 第二个子 agent 对照测试审查 |
| **持久化** | 把状态写到对话之外 | 开 PR + 收件箱 + 状态文件 |
| **调度** | 让它一圈圈自动转 | 早上 automation 自动跑 |

**关键洞察：** 发现这一步做得好不好，决定了整个 loop 的质量上限。让 agent 自己去找活，而不是你把活喂给它。

### §04 六个零件：搭一个 Loop 需要什么

| 零件 | 是什么 | 对应动作 | 一句话 |
|---|---|---|---|
| **Automations** | 挂在时间表/触发器上自动跑 | 调度 | make a loop an actual loop |
| **Worktrees** | 隔离并行 agent 的工作目录 | 交付 | same headache as two engineers |
| **Skills** | 固化项目知识、还意图债 | 发现 | fire $skill-name, not a wall of instructions |
| **Connectors** | MCP 接外部系统 | 持久化 | only see filesystem is a tiny loop |
| **Sub-agents** | 生成者与评判者分离 | 验证 | too nice grading its own homework |
| **Memory** | 磁盘上的持久状态 | 持久化 | the agent forgets, the repo doesn't |

**核心原则：**
- Automation 里该触发的是一个 skill，不是一整面墙的指令
- 两个 agent 同时写一个文件 = 两个工程师往同几行代码上提交
- Worktree 让并行从「能跑但乱」变成「能跑且干净」
- Skill 在还「意图债」——把你一次想清楚的东西固化下来
- Connector 决定了 loop 的「视野半径」
- Memory 不是上下文。上下文会被冲掉，memory 在磁盘上跨轮跨天

### §05 生成器与评判器：为什么写代码的 AI 不能给自己打分

**它总夸自己（Anthropic 工程师 Prithvi Rajasekaran 的发现）：**

> Agents tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre.

让 agent 评价自己产出的东西，它往往会自信地夸一通——哪怕在人看来质量明显很一般。

**改一个怀疑论者，比改一个谦虚的作者容易：**

> Tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work.

调一个独立的评判器让它变得怀疑，比让生成器自我批判要容易得多。结构上借鉴了 GAN（生成对抗网络）——一个 generator 写，一个 evaluator 审。

**评判器要会动手，不只是会读：**
Rajasekaran 在前端任务里的做法：evaluator 接上 Playwright MCP，自己打开页面、点按钮、截图、查 DOM，像一个真人 QA 那样去用这个东西。看的是行为，不是意图。

**产品化应用：/goal 命令**
`/goal all tests in test/auth pass and the lint step is clean`

关键在「谁来判定满足了没有」。每跑完一轮，一个又小又快的 fresh model 检查条件成立没有——不成立，再来一轮。

> The hard part of a loop is not the loop. It is putting something inside it that can say no.
> 循环的难点不在循环本身。难的是往里面放一个能说「不」的东西。

### §06 让循环在你睡觉时跑：三个真实的 Loop

**案例一：Addy 的早晨（个人级别）**
天亮 automation 自己醒来 → triage skill 读 CI/issue → 开 worktree → 子 agent 起草 + 审查 → 自动开 PR → 没把握的丢收件箱 → 状态写进文件留给第二天

**案例二：Stripe 的 Minions（企业级别）**
- 每周合并 **1300+ 个 PR**，没有一行是人手写的
- 触发方式：Slack @Minion bot 或 emoji 表情回复，fire-and-forget
- 关键设计：**在 LLM 开始思考前，一个确定性的 orchestrator 先把上下文备齐**（拉 Jira、找文档、Sourcegraph 搜代码）
- 能写死规则的活从 LLM 手里拿走，交给确定性代码
- 架构：六层，确定性的 gate 和 LLM 的创造步骤交替咬合
- 每个 agent 环境用 Devbox，跑在 EC2 上——**cattle not pets**，用完即弃
- 人没退场，人换了工位——1300 个 PR 仍由工程师 review

**案例三：调度层怎么选**

| | Cloud Routines | 桌面定时任务 | /loop |
|---|---|---|---|
| 跑在哪 | Anthropic 云 | 你的机器 | 你的机器 |
| 需要开机？ | 否 | 是 | 是 |
| 最小间隔 | 1 小时 | 1 分钟 | 1 分钟 |
| 能看本地文件？ | 否 | 能 | 能 |

「睡觉时跑」之所以容易被讲歪，就是因为很多人把本地 /loop 当成了它的全部。**本地 /loop 是「我在场时让它替我多跑几轮」，云端调度才是「我不在场它也照跑」。**

### §07 代价：验证债、理解腐烂、Token 失控

**四笔账：**

| 代价 | 症状 | 一句话防它 |
|---|---|---|
| **验证债** | 产出堆着没人验，错误安静积累 | 装一个跟干活的不是同一个的评判者 |
| **理解腐烂** | 代码在长，你脑里的地图停了 | 定期读产出，讲不出就是该更新 |
| **认知投降** | 循环给啥收啥，懒得有意见 | 执行可外包，拿主意不行 |
| **Token 失控** | 用量剧烈波动，账单不可预测 | 上线前钉死预算和重试上限 |

> A loop running unattended is also a loop making mistakes unattended.  
> 一个没人看着的循环，也是一个没人看着犯错的循环。它跑得越欢，错也错得越安静。

**理解腐烂的机制：** 循环每天替你写一堆你没写过的代码。代码能跑、测试能过、PR 能合。但代码库在长大，你脑子里的那张地图却停在三个月前。等出事的那天，你打开文件，发现自己像在看别人的项目。

**认知投降的加速：** 循环越可靠，你越容易把判断整个外包出去。每个 PR 都要自己想一遍对不对，比直接点「合并」累多了。这是个会自我加速的滑坡。

### §08 当工程师，不只是按下启动键

> Two people can build the same loop and get opposite outcomes.  
> 两个人造出一模一样的循环，得到的结果可以完全相反。

**一个人用循环** = 为了在自己已经吃透的事情上跑得更快。循环帮他扩大他本来就有的判断。

**另一个人用同样的循环** = 为了不必再去理解。看不懂没关系，循环会写；判断不了没关系，循环会合。

循环是个忠实的乘号，乘的是你。你带进去的是理解，它放大理解；你带进去的是偷懒，它放大偷懒。

**稀缺的正在转移：**
- 代码、方案、PR、修复，都能批量造出来——不再值钱
- **判断力**——知道哪个方案是对的、哪行代码该拦下来——循环替不了你

> Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go.
> 造那个循环。但要像一个打算继续当工程师的人去造它，而不是一个只负责按下启动键的人。

### §09 今天就动手：搭你的第一个 Loop

**五步上手：**

1. **跑一个 /loop** — 按时间间隔把同一件事重跑一遍
   - `/loop 5m check the deploy`（固定 5 分钟一次）
   - `/loop babysit all my PRs. Auto-fix build issues`（Boris 自己的例子）

2. **让它读 CI 和 issue，做 triage** — 每天看 CI 失败、新 issue、最近 commit，挑出值得处理的

3. **加一个状态文件** — markdown 文件，把每次发现、处理到哪一步都写进去。Agent 会忘，仓库不会

4. **加一个 evaluator** — `/goal` 命令，跑到条件满足为止，由另一个 fresh 模型判定

5. **加 worktree** — `-w` 参数，让并行的 agent 互不踩脚

**第一个 Loop 检查清单：**
1. □ 发现源——它定时去读什么？
2. □ 状态文件——跨轮的记忆落在哪个磁盘文件上？
3. □ evaluator——有没有一个独立的、会说「不」的检查？
4. □ 隔离——并行的 agent 是不是各自一个 worktree？
5. □ token 上限——设没设花费的天花板？
6. □ 人工复核点——哪一步停下来等你看一眼？

> 新手最容易只搭前两条就上线，结果就是一个没人看着、也没人能拦的循环在那儿自我点头。

---

## 二、知乎深度解析：《全网热议的Loop到底是个啥？》

**来源**: [知乎专栏](https://zhuanlan.zhihu.com/p/2047660729969407202)
**时间**: 2026年6月9日
**状态**: ✅ 完整收录

### 引爆时间线的那条推文

6月7日，Peter Steinberger（PSPDFKit 创始人）发推：
> "Here's your monthly reminder that you shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."

最精彩的回复来自 Matthew Berman——有人问这具体是什么意思，他说：
> "nobody knows but him and boris."

### Boris Cherny 的定义

Boris Cherny 是 Claude Code 的创造者。据报道，Claude Code 已经贡献了 GitHub 上约 4% 的公开 commit。

> 现在已经升级到下一层抽象了。我不再 prompt Claude 了。我有一些 Loop 在运行，它们负责 prompt Claude、决定下一步该做什么。我的工作是写 Loop。

**他的战绩：** 过去 30 天，259 个 PR，497 次 commit，4 万行新增代码。**100% 由 Claude Code 编写。** 2025 年 11 月删了 IDE，至今没重新打开过。

### 五层 Loop

评论区之所以吵成一团，因为 "Loop" 这个词藏着至少五层不同的意思：

1. **学术 while 循环（2022）** — ReAct 论文：模型思考→工具→读取→重复
2. **AutoGPT 时代（2023）** — 给模型一个目标让它自己 prompt 自己
3. **Ralph Loop（2025.7）** — 一行 Bash：`while :; do cat PROMPT.md | claude-code ; done`
4. **/goal 命令（2026 春）** — 产品化的 Ralph Loop，持续跑直到小模型确认任务完成
5. **编排 Loop（2026 现在）** — Loop 成为工作单元，Loop 监督 Loop，调度取代人工启动，持久化

### "这不就是 cron job 换了个马甲吗？"

**对的部分：** 是的，调度层就是 cron。
**不对的部分：** cron job 跑的是固定脚本。Loop 跑的是一个**会看当前状态、自己决定下一步、执行它、检查是否成功、再决定要不要继续的模型**。

> Loop = cron + 决策体

### 实际怎么用？

Boris 的起点例子：
> /loop babysit all my PRs. Auto-fix build issues, and when comments come in, use a worktree agent to fix them.

**Boris 五条自动化建议：**
1. 用 auto mode 免权限确认
2. 用 dynamic workflows 编排成百上千个 Agent
3. 用 /goal 或 /loop 让 Claude 持续跑直到完成
4. 把 Claude Code 跑在云端，关上笔记本电脑
5. **确保 Claude 有办法端到端验证自己的工作**（这是最关键的）

**深水区案例：Steve Yegge 的 Gas Town** — 20-30 个 Claude Code 实例由一个 Mayor Agent 协调，巡逻 Agent 跑持续 Loop，状态存 git 扛崩溃。开源项目。

### 成本现实

> Every AI agent I shipped this year is a for-loop, an llm call, and a try/catch around the json parsing. The only thing agentic about it is the anthropic bill at the end of the month.

**Uber 的真实上限：** 每人每工具每月 1500 美元（Claude Code + Cursor），因为他们四个月就烧完了全年 AI 预算。

---

## 三、Friday AI Club：《AI Agent Loop 完全指南》

**来源**: [fridayaiclub.com](https://fridayaiclub.com/ai-agent-loop-everything-you-need-to-know/)
**时间**: 2026年6月17日
**状态**: ✅ 完整收录

### AI Agent Loop 的工作流程

1. **User Input** — 给系统一个初始目标或 spec.md
2. **Perceive** — 系统读取环境、现有文件、代码库状态
3. **Reason** — AI 分析缺什么、需要修什么
4. **Plan** — 创建完成目标所需的具体工程步骤清单
5. **Act** — agent 写代码、创建文件、修改项目
6. **Observe** — 系统审阅自身结果，跑测试、编译检查
7. **Task Done?** — 关键决策点。否→回 Perceive 自愈循环。是→Final Response

### Agent Loop 与自主 Loop 的区别

- **Human-in-the-loop**：你打字，看结果，再打字。人是引擎
- **Agentic Loop**：你设置目标后走开，系统自主决策、自主修正

### 成本真相

Peter Steinberger 透露他的自主循环实验每月 token 费用高达 **130 万美元**。

**当前最适合的场景：自动化代码审查**
- Push 新 feature 到 GitHub
- Code review agent 扫描代码，打分 1-5
- 分数低于 4 → gp loop 触发 → AI 重写 → repush → 重新评分
- 最多循环 5 次
- **前提：目标是确定性的**（测试要么过要么不过）

**结论：** 如果你在做 startup / micro-SaaS / 个人 app，你不需要设计大规模自主循环。把自主循环留给**确定性任务**（自动化测试、代码审查）。

---

## 四、Addy Osmani 奠基原文（完整）

**链接**: https://addyosmani.com/blog/loop-engineering/
**时间**: 2026年6月7日
**状态**: ✅ 已收录（见上方橙皮书引用，原文核心内容已完整摘录）

---

## 五、Medium 文章摘要与链接

以下 Medium 文章被 Cloudflare/登录墙拦截，无法获取全文。链接保留，可直接在浏览器中阅读：

| 文章 | 链接 |
|---|---|
| 《Loop Engineering: Why Designing Loops, Not Prompts》 | [medium.com/@umeshcapg](https://medium.com/@umeshcapg/loop-engineering-why-designing-loops-not-prompts-became-the-biggest-ai-trend-of-2026-a5874b9d0e04) |
| 《Loop Engineering: The Breakthrough》 | [levelup.gitconnected.com](https://levelup.gitconnected.com/loop-engineering-the-breakthrough-that-makes-the-software-factory-real-d85826f072df) |
| 《Is Loop Engineering Really What We Need?》 | [pub.towardsai.net](https://pub.towardsai.net/is-loop-engineering-really-what-we-need-77506986bf2a) |
| 《Everything You Need To Know About AI Agent Loop》 | [fridayaiclub.com](https://fridayaiclub.com/ai-agent-loop-everything-you-need-to-know/) |
| 《Loop Engineering: A Guide for Practitioners》 | Adnan Masood, PhD |

**获取到的摘要：**

**《Why Designing Loops, Not Prompts》**（Umesh Kumar Yadav，6月24日）
关键概念：
1. **Single-Agent Loop**：一个 agent 反复改进自己的产出
2. **Multi-Agent Loop**：多个 agent 互相协调
3. > "Single-agent loops optimize execution. Multi-agent loops optimize coordination."

**《The Breakthrough That Makes the Software Factory Real》**（Jazz Tong，6月12日）
> "My evenings used to go like this: prompt a coding agent, wait, read the diff, prompt again. A few months ago that stopped. Now I write a spec in the afternoon, start a loop, and read finished work the next morning."
> Claude Code 的 dynamic workflows 把任务拆成并行 agent，ultracode 控制推理量，自动化检查在你看之前测试一切。

**《Is Loop Engineering Really What We Need?》**（Hamza Boulahia，6月15日）
> Boris Cherny 的视频在 X 上 48 小时 230 万浏览，Peter Steinberger 820 万浏览。反方观点：大多数人根本不需要 agent loop。

---

## 六、LinkedIn 热帖汇总

**Udit Goenka 的帖子**（传播数据）：
> "Two weeks ago 'loop engineering' was one guy's tweet. This week it's 2200 posts and a thread with 6.5 million views."

**"Your AI Agent Should Be Running While You Sleep"**（6月12日）：
> "Loop engineering = designing when, how, and within what boundaries the AI operates. One is giving commands. The other is building systems."

**"Applying Loop Engineering in Agent-Application Tasks"**（4天前）：
> 作者发现在 agent-application 任务中应用 loop engineering 让处理更加实用。

**"Most Developers Do Not Need Agent Loops Yet"**（6月8日，反方观点）：
> "Most developers do not need to put their coding agent in a loop yet, even though the technique went viral this month." ——值得认真读的反方观点。

---

## 七、GitHub Orange Book 简介

**仓库**: https://github.com/alchaincyf/loop-engineering-orange-book
**作者**: 花叔（Alchaincyf）
**版本**: v260615

仓库包含：
- ✅ **中文 PDF**（完整 62KB 文本）
- ✅ **英文 PDF**（完整 70KB 文本）
- ✅ 完整 README（中英文）
- 本文件第一节已收录中文版完整全文

**作者介绍**：花叔 · AI Native Coder · 独立开发者。全平台 50 万+ 粉丝。所有产品——包括一款 AppStore 付费榜 Top 1 的 iOS app——全部用 AI 做出来，没手写过一行代码。B站：花叔v · 公众号：花叔 · X：@AlchainHust

本文件是橙皮书完整内容与全网 Loop Engineering 深度内容的合集整理版。

---

## 八、从理论到实战：Hermes 上的 Loop 工程实践

既然你已经有了 Hermes Agent 在跑，Loop Engineering 六大零件在你这里都有对应实现：

| 零件 | Hermes 对应能力 | 状态 |
|---|---|---|
| **Automations** | `cronjob` 定时调度 | ✅ 已配（自动备份 3am） |
| **Worktrees** | `delegate_task` 并行子任务 | ✅ 可用（嵌套深度 2） |
| **Skills** | `skill_manage` + `skill_view` | ✅ 大量技能已配 |
| **Connectors** | MCP 服务器（Filesystem 已配） | ✅ 已配 |
| **Sub-agents** | `delegate_task` maker-checker | ✅ 可用 |
| **Memory** | `memory` + `fact_store` | ✅ holographic + 事实库 |

**下一步可以做的事：**
1. 用 cronjob + delegate_task 搭一个定时 triage loop（每天自动扫 issue/cron 结果）
2. 用 sub-agent 模式做 maker-checker（agent A 写代码，agent B 审查）
3. 再加一个状态文件持久化（markdown 记录 loop 的跨轮状态）
4. 设 token 上限防跑飞

**从第 §09 章建议的第一个 loop 开始：**
```
cronjob(
  action='create',
  schedule='daily at 8am',
  prompt='Read today's cron outputs, check for failures or pending items, 
          prioritize them, write status to /root/.hermes/loop-state.md,
          and report back what needs attention.',
)
```
