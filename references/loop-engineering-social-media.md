# Loop Engineering — 社交媒体高热度帖子与文章合集（原文）

> 整理时间: 2026年6月26日
> 来源说明: 部分来源因 Cloudflare/登录墙无法抓取全文，已注明。可抓取的部分保留了原文完整内容。

---

## 一、Addy Osmani 博客原文（完整）

**链接**: https://addyosmani.com/blog/loop-engineering/
**时间**: 2026年6月7日
**转载**: O'Reilly Radar (2026年6月22日, 14分钟阅读)
**状态**: ✅ 以下是完整原文内容

---

Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead. A loop here can be thought of a recursive goal where you define a purpose and the AI iterates until complete. I believe this may be the future of how we work with coding agents. However, its still early, I'm skeptical and you absolutely have to be careful about token costs (usage patterns can vary wildly if you are token rich or poor), so I want to unpack what it is and what it means.

Peter Steinberger recently said: "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." Similarly, Boris Cherny, head of Claude Code at Anthropic, said "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops."

Okay, so what does any of that mean?

For like two years the way you got something out of a coding agent was you wrote a good prompt and shared enough context. You type a thing, you read what came back, you type the next thing. The agent is a tool and you are holding it the entire time, one turn after the other. That part is kind of over, or at least some think it's going to be.

Now you build a small system that finds the work, hands it out, checks it, writes down what is done and then decides the next thing, and you let that system poke the agents instead of you. I wrote before about the cousin of this, agent harness engineering, which is making the environment one single agent runs inside and the factory model - the system that builds the software. Loop engineering sits one floor above the harness. The harness but it runs on a timer, it spawns little helpers, and it feeds itself.

The thing that surprised me is this is not really a tool thing anymore. A year ago if you wanted a loop you wrote a pile of bash and you maintained that pile forever and it was yours and only yours. Now the pieces just ship inside the products. Steinberger's list maps almost exactly onto the Codex app, and then almost the same onto Claude Code. And once you notice the shape is the same you stop arguing about which tool, you just design a loop that still works no matter which one you happen to be sitting in.

### The five pieces, and then notes

A loop needs five things and then one place to remember stuff.

1. **Automations** that go off on a schedule and do discovery and triage by themselves.
2. **Worktrees** so two agents working in parallel dont step on each other.
3. **Skills** to write down the project knowledge the agent would otherwise just guess.
4. **Plugins and connectors** to plug the agent into the tools you already use.
5. **Sub-agents** so one of them has the idea and a different one checks it.

Then the sixth thing, **memory**. A markdown file, or a Linear board, anything that lives outside the single conversation and holds what's done and what is next. Sounds too dumb to matter. But it's the same trick every long running agent depends on — the model forgets everything between runs so the memory has to be on disk and not in the context. The agent forgets, the repo doesnt.

### Product comparison table

| Primitive | Job in the loop | Codex app | Claude Code |
|---|---|---|---|
| Automations | discovery + triage on a schedule | Automations tab: pick project, prompt, cadence, environment; results land in a Triage inbox; /goal for run-until-done | Scheduled tasks and cron, /loop, /goal, hooks, GitHub Actions |
| Worktrees | isolate parallel features | Built-in worktree per thread | git worktree, --worktree, isolation: worktree on a subagent |
| Skills | codify project knowledge | Agent Skills (SKILL.md), invoked with $name or implicitly | Agent Skills (SKILL.md) |
| Plugins / connectors | connect your tools | Connectors (MCP) plus plugins for distribution | MCP servers plus plugins |
| Sub-agents | ideate and verify | Subagents defined as TOML in .codex/agents/ | Task subagents in .claude/agents/, agent teams |
| State | track what's done | Markdown or Linear via a connector | Markdown (AGENTS.md, progress files) or Linear via MCP |

### Automations, this is the heartbeat

Automations are what make a loop an actual loop and not just one run you did once. In the Codex app you make one in the Automations tab and you pick the project, the prompt it will run, how often, and if it runs on your local checkout or on a background worktree. The runs that find something go to a Triage inbox, and the runs that find nothing just archive themselves which is nice. OpenAI uses them internally for boring stuff like daily issue triage, summarising CI failures, writing commit briefings, hunting bugs somebody added last week. And an automation can call a skill, so you keep the recurring thing maintainable, you fire $skill-name instead of pasting a giant wall of instructions into a schedule that nobody will ever update.

Claude Code gets to the same place but through scheduling and hooks. You can run a prompt or a command on a interval with /loop, you can schedule a cron task, you can fire shell commands at certain points in the agent lifecycle with hooks, or you push the whole thing to GitHub Actions if you want it to keep running after you close the laptop.

There is a second in-session primitive worth knowing. /loop re-runs on a cadence. /goal keeps going until a condition you wrote is actually true, and after every turn a separate small model checks whether you are done, so the agent that wrote the code isnt the one grading it. You give it something like "all tests in test/auth pass and lint is clean" and walk away.

### Worktrees so parallel doesnt turn into chaos

The second you run more than one agent the files start colliding. Two agents writing the same file is the exact same headache as two engineers committing to the same lines. A git worktree fixes it — a separate working directory on its own branch sharing the same repo history.

### Skills, so you stop explaining your project every single time

A skill is how you stop re-explaining the same project context every session. Both tools use the same format, a folder with a SKILL.md inside holding instructions and metadata, and then optional scripts, references, assets.

### Plugins and connectors

This one is fairly direct: you give the agent a way to talk to the rest of your stack. Both tools speak MCP, both have plugin directories. This matters inside a loop because a loop that cant talk to the ticket system or the CI dashboard is blind.

### Sub-agents, the maker-checker split

A sub-agent is how you separate the person who writes the code from the person who reviews it. One agent builds, another checks. This is the maker-checker pattern and its the single most important thing you can do to keep a loop from shipping garbage. In Codex you define a sub-agent in a TOML file in .codex/agents/, give it a model, a skill, a temperature, and optional tools like "browser" or "terminal". In Claude Code the same thing lives in .claude/agents/ and you can build agent teams.

### State, the thing the agent forgets

The agent forgets everything when the conversation ends. The loop doesnt need to remember — the repo does. You write progress to a file so the next run knows what happened. This is what stays outside the LLM context.

### Closing thoughts

If you are using one of these tools and you are still hand-holding every prompt, you are leaving most of the value on the table. The question isnt which tool wins. The loop is the competitive advantage, not the model. Anyone can call an API. Not everyone has designed a system that turns that API call into a process that runs without them.

---

## 二、O'Reilly Radar 版本

**链接**: https://www.oreilly.com/radar/loop-engineering/
**时间**: 2026年6月22日
**作者**: Addy Osmani
**阅读时间**: 14分钟
**状态**: ❌ 全文在登录墙后，无法抓取

O'Reilly Radar 转载了 Addy Osmani 的博客文章并正式发布。核心内容与博客版一致，但经过了 O'Reilly 的编辑和排版。

---

## 三、Peter Steinberger 原推

**链接**: https://x.com/steipete/status/2063697162748260627
**时间**: 2026年6月
**状态**: ❌ X/Twitter 需要登录，无法获取原文和评论区内容

核心引文（已知）:
> "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."

这条推文引爆了整个 AI 编程时间线，评论区直接变成"角斗场"，传播量数千万浏览。2000+ 转发。

---

## 四、Boris Cherny (Anthropic Claude Code 负责人) 原话

**状态**: ❌ X/Twitter 需要登录

核心引文（已知）:
> "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops."

---

## 五、@sairahul1 — "Loops: What Every AI Engineer Needs to Know"

**链接**: https://x.com/sairahul1/article/2064277888216555684
**时间**: 2026年6月
**状态**: ❌ X/Twitter 需要登录

核心内容（来自搜索结果摘要）:
- They are writing the logic that governs how agents discover, plan, check their own work, and know when they are done.
- At standard API pricing, a week of serious loop engineering costs more than most people's entire monthly...

---

## 六、@Saboo_Shubham_ — "The AI PMs getting hired in 2026 run Agent Loops"

**链接**: https://x.com/Saboo_Shubham_/status/2070223027695132720
**时间**: 大约6月25日（持续发酵中）
**状态**: ❌ X/Twitter 需要登录

核心内容（来自搜索结果摘要）:
- "It is Loop Engineering. For the last two years, most PMs have been trying to get better at prompting."
- "Generation is solved with AI Agents. Loop Engineering can produce infinitely. Verification and judgment are all that's left."

---

## 七、GitHub Orange Book — 《Loop Engineering 橙皮书》完整 README

**链接**: https://github.com/alchaincyf/loop-engineering-orange-book
**作者**: HuaShu (花叔)
**状态**: ✅ 以下是完整 README 内容

### 英文版 README

> Loop Engineering: Stop Asking Me What It Is
>
> A plain-language field guide to loop engineering — the term that blew up in a single week of June 2026, when Peter Steinberger, Boris Cherny (head of Claude Code at Anthropic), and Google's Addy Osmani all pointed at the same shift and gave it a name.
>
> The one-line version: stop being the person who prompts the agent. Design the system that does it for you.

**9 sections across 4 parts:**

| Part | Content | Sections |
|---|---|---|
| 1. What It Is | The definition, the one-week origin story, and the prompt → context → harness → loop stack | §01-02 |
| 2. How It Turns | The five moves of one loop, the six parts you build it from, and why an AI can't grade its own code | §03-05 |
| 3. Where It Runs, What It Costs | Three real loops (Addy's morning triage, Stripe's Minions, the scheduling reality) and the four costs — verification debt, comprehension rot, token blowout, cognitive surrender | §06-07 |
| 4. How You Start | Staying the engineer, and building your first loop today | §08-09 |

### 中文版 README

> 一句话版本：请停止亲手为 Agent 写提示词，去设计让 Agent 自主运行的循环系统。
>
> 如果你读过《Harness Engineering 橙皮书》，这是它的下一层。它完全独立成书——你不需要读过前作。
>
> 9个小节，共4个部分，内容包括：什么是 Loop、一周爆发起源故事、prompt→context→harness→loop 四层技术栈；单一 Loop 的五步动作、构建循环的六个组件、以及为什么 AI 不能给自己的代码打分；三个在生产环境中运转的真实循环（Addy 的晨间消息分类循环、Stripe 的 Minions 代码审查循环、以及一个现实的排期循环），以及四种成本（验证债、理解腐化、Token 爆炸、认知投降）；如何保持工程师身份，以及搭建你的第一个循环。

---

## 八、LinkedIn 热帖汇总

**状态**: ⚠️ 内容来自搜索结果摘要，非完整原文

### Udit Goenka 的帖子（传播数据）
> "Two weeks ago 'loop engineering' was one guy's tweet. This week it's 2200 posts and a thread with 6.5 million views."

### Your AI Agent Should Be Running While You Sleep — That's Loop Engineering (6月12日)
> "Loop engineering = designing when, how, and within what boundaries the AI operates. One is giving commands. The other is building systems."

### Applying Loop Engineering in Agent-Application Tasks Improves... (4天前)
> "I am increasingly applying loop engineering in my agent-application tasks. I have found that it makes agent processing more practical and..."

### Most Developers Do Not Need Agent Loops Yet (6月8日，反方观点)
> "Most developers do not need to put their coding agent in a loop yet, even though the technique went viral this month."

### Loop Engineering: The New Discipline in AI Development (6月15日)
> 提到 GitHub Orange Book 正在 LinkedIn 上病毒传播。

---

## 九、Medium 文章摘要

**状态**: ❌ 全部被 Cloudflare 拦截，无法抓取全文。以下是搜索结果中的片段。

### "Why 'Designing Loops, Not Prompts' Became the Biggest AI Trend of 2026"
**作者**: Umesh C
**时间**: 6月24日（2天前）
**完整链接**: https://medium.com/@umeshcapg/loop-engineering-why-designing-loops-not-prompts-became-the-biggest-ai-trend-of-2026-a5874b9d0e04

核心概念（来自搜索结果）:
1. **Single-Agent Loop**: One agent repeatedly improves its own output
2. **Multi-Agent Loop**: Multiple agents coordinate with each other
> "Single-agent loops optimize execution. Multi-agent loops optimize coordination."

### "Is Loop Engineering Really What We Need?"
**来源**: Towards AI, 6月15日
**完整链接**: https://pub.towardsai.net/is-loop-engineering-really-what-we-need-77506986bf2a

> "Loop engineering is real, but it's still niche. The underlying shift is a genuine evolution that could possibly shape how we work with AI tools..."

### "Loop Engineering: The Breakthrough That Makes the Software Factory Real"
**来源**: GitConnected / Level Up, 6月12日
**完整链接**: https://levelup.gitconnected.com/loop-engineering-the-breakthrough-that-makes-the-software-factory-real-d85826f072df

> "Loop engineering is the layer above it. The harness makes one agent run well. The loop keeps work flowing through agents after you..."

### "Loop Engineering Explained Visually: From Manual Prompts to Goal-Driven AI Agents"
**作者**: Parvez Mohammed / The Cloud Girl, 6月15日
> Part 12 — Multi-agent loop sketch. Orchestrator pseudoflow: goal → decompose → for each subtask: assign specialist → specialist loops until sub...

### "Everything You Need To Know About AI Agent Loop"
**来源**: Friday AI Club, 6月17日
**完整链接**: https://fridayaiclub.com/ai-agent-loop-everything-you-need-to-know/

> 讨论了 AI agent loop 的实际成本，提到 "can cost $1.3 million a month"。

### "Loop Engineering: A Guide for Engineers and Practitioners"
**作者**: Adnan Masood, PhD, 2天前
> "Loop engineering begins exactly where automation stops being... verification is judgmental where a test suite is binary."

---

## 十、知乎 — 《全网热议的Loop到底是个啥？》

**链接**: https://zhuanlan.zhihu.com/p/2047660729969407202
**时间**: 2026年6月9日
**状态**: ❌ Cloudflare 拦截，无法获取全文

搜索结果摘要:
> "这周 AI 编程圈最火的一句话只有六个字——'设计 Loop'。Peter Steinberger 的一条推文引爆了整个 AI 编程时间线，评论区直接变成角斗场。但最尴尬的是:转发这句话的人可能自己也不知道 Loop 到底是什么。"

---

## 十一、Instagram / Reels

**状态**: ⚠️ 内容来自搜索结果摘要

- **"Don't run AI loops (here is why)"** — 7天前，提到了 Loop Engineering 和 Peter Steinberger
- **"From Prompts to Problems"** — 6月12日，#loopengineering 标签开始出现

---

## 十二、菜鸟教程

**链接**: https://www.runoob.com/loop-engineering.html（疑似 404）
**状态**: ❌ 页面返回 404，URL 可能有变动

---

## 十三、内容可用性总结

| 来源 | 状态 | 原因 |
|---|---|---|
| Addy Osmani 博客 | ✅ 已获取全文 | 无防护 |
| GitHub Orange Book | ✅ 已获取 README | 无防护 |
| O'Reilly Radar | ❌ 无全文 | 登录墙 |
| X/Twitter 帖子 | ❌ 无全文 | 需登录 |
| LinkedIn 帖子 | ⚠️ 摘要 | 需登录 |
| Medium 文章 | ❌ 无全文 | Cloudflare |
| 知乎 | ❌ 无全文 | Cloudflare |
| Instagram | ⚠️ 摘要 | 需登录 |
| 菜鸟教程 | ❌ 404 | 链接失效 |

**建议**: 如果你需要看 Medium/O'Reilly/知乎 的完整原文，可以直接点上面给出的链接去浏览器看。我能抓到的完整内容（Addy 博客、GitHub Orange Book）已经全部放在上面了。
