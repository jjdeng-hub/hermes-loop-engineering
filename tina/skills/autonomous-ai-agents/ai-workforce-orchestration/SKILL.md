---
name: ai-workforce-orchestration
description: Build and operate a one-person company using Hermes profiles + expert role library — each profile is an autonomous "employee" with specialized skills, coordinated by an orchestrator.
version: 1.0.0
created: 2026-06-17
tags: [hermes, profiles, multi-agent, orchestration, one-person-company, agency-agents-zh]
---

# AI Workforce Orchestration

> Turn Hermes into a multi-agent company: one orchestrator + N specialized profiles, each acting as an autonomous employee with a dedicated expert role from `agency-agents-zh`.

## When to Use

- User wants to build a "one-person company" with AI agents
- User has multiple Hermes profiles and wants to assign them specialized roles
- User has the `agency-agents-zh` role library (214 expert roles, 18 departments) and wants to map them to profiles
- User wants an orchestrator pattern: one main agent delegates tasks to specialized sub-agents
- User wants to scale their solo operation into a structured multi-agent team

## Architecture

The evolved architecture (2026-06-20) separates concerns into four layers — decision, product, execution, verification. Tom1 is NOT the PM; those roles are independent.

```
                     ┌─────────────────┐
                     │  CEO (Jerry)     │ ← reviews, decides direction
                     │  +               │
                     │  Tom1 (助手/搭档) │ ← discuss, decide together
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │  PM (Alex)       │ ← product decisions, priorities, plan
                     │  ─ independent   │
                     │  profile         │
                     │  Checked by:     │
                     │  delegate_task   │
                     │  (8-condition    │
                     │  checklist)      │
                     └────────┬────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
     ┌────────▼────────┐ ┌───▼──────────┐ ┌──▼──────────┐
     │ Justin 🖥️       │ │ Eli 🧠       │ │ [? DevOps]  │
     │ Programmer      │ │ RAG Engineer │ │ Executor    │
     │ (justin-coder)  │ │ (eli-rag)    │ │             │
     │ deepseek-v4-pro │ │ v4-flash     │ │             │
     │ Checker: run    │ │ Checker:     │ │ No checker  │
     │ verification    │ │ random sample│ │ needed      │
     └────────┬────────┘ └───┬──────────┘ └──┬──────────┘
              │              │               │
     ┌────────▼────────┐ ┌──▼───────────┐
     │ delegate_task    │ │ delegate_task │
     │ (Checker:        │ │ (Checker:     │
     │ 独立运行验证)     │ │ 抽检 N 篇    │
     └─────────────────┘ └──────────────┘
```

### Layer responsibilities

| Layer | Who | What they do | Checked by |
|-------|-----|-------------|------------|
| **Decision** | Jerry + Tom1 | Set direction, make trade-off decisions | Jerry (no automated checker needed) |
| **Product** | Alex (PM profile) | Output plans, priorities, roadmap specs | delegate_task with 8-condition checklist |
| **Execution** | Justin, Eli, [? DevOps] | Produce code, knowledge bases, deployments | Per-role checker via delegate_task |
| **Verification** | delegate_task sub-agents | Validate every deliverable — never ask, never bypass | Instinct-level rule in each profile's SOUL |

### Principles

1. **CEO does not execute — CEO reviews.** The human only makes judgment calls and approves deliverables. All execution is done by the orchestrator or employee profiles.
2. **Each employee has one job.** A profile assigned the "小红书运营专家" role should not be asked to write server deployment scripts. Role isolation keeps outputs predictable.
3. **Orchestrator knows the team, not their details.** The orchestrator knows which profiles exist and what they do, but doesn't need to know the internals of each profile's skills or memory.
4. **Start small, add as needed.** 3 employee profiles is enough for most solopreneur setups. Adding more than 5 before the first 3 are running at steady state creates coordination overhead, not leverage.
5. **Evolve from dispatch to loop.** The long-term target is not "CEO dispatches tasks → agent executes" but "CEO designs loops → loops dispatch tasks → agents execute autonomously." This is the next evolution of workforce orchestration.
6. **Loop is instinct — no ask, no bypass.** All output-producing agents (programmer, RAG engineer, PM orchestrator in PM mode) automatically run maker/checker before every delivery. Never ask "should I run the check?" — execute it. The deliverable is NOT complete until verified by an independent checker. This is embedded in each profile's SOUL as a permanent thinking rule.

## Evolution: From Harness to Loop

The AI programming paradigm is evolving across four stages:

```text
Prompt  →  Context  →  Harness  →  Loop
```

This skill currently operates at the **Harness** stage: designing how agents are organized, skilled, and connected. The next stage — **Loop** — adds self-driving, continuous operation on top of the harness.

**Loop Engineering** (cobusgreyling/loop-engineering, 425★) reframes the work: instead of prompting agents manually, you design a system that discovers work, hands it out, checks it, records state, and decides the next action — cycling until the goal is met.

### Jerry's precise definition (2026-06-20)

> **"在工作流的合理节点嵌入有质量的反馈修正回路，让系统自动收敛到更优的结果。"**

This is more precise than the generic "design a system that prompts agents." It makes explicit what's implicit in Addy Osmani's essay — that the **quality and placement of feedback signals** determines whether a loop actually converges, not just whether it runs. "Prompt agents" describes the mechanism; "feedback correction at workflow nodes" describes the control theory.

### The Code Review Analog: Loop Engineering is Already Your Workflow

Jerry (a K&S software engineer, not a controls engineer) connected Loop Engineering to his daily job immediately:

> "Developer writes code → pushes PR → Reviewer gives feedback → Developer fixes → Merge → Better code"

This maps directly to AI workflow loops:

| Code Review Step | Loop Engineering Analog |
|-----------------|------------------------|
| Developer writes code | Maker agent produces output |
| Push PR | Deliver result (write file, make change) |
| Reviewer reviews, gives feedback | Checker sub-agent independently verifies |
| Developer fixes based on comments | Maker revises based on checker findings |
| CI passes + Reviewer approves → Merge | Maker and checker agree → deliverable final |
| Merged code is better than initial PR | Loop converged to a better result |

**Key insight**: Code review IS Loop Engineering. The decades-old practice of peer code review — a separate person with a different perspective reviewing your work before it ships — is structurally identical to the maker/checker split in AI loops. Every developer already knows this pattern. The question is: why do AI coding agents skip it?

**When discussing with Jerry**: Frame it as "code review for agents" — not as a new theory, but as applying the same discipline you already have to the AI layer. This bridges from familiar to unfamiliar without importing control theory vocabulary.

### Key quotes

> "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." — Peter Steinberger

> "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops." — Boris Cherny (Head of Claude Code, Anthropic)

> "Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go." — Addy Osmani

### Three levels of loop maturity

Current `/goal` implementations (Codex, Claude Code, Hermes) only achieve **Level 1**:

| Level | Name | Feedback Signal | What it does | Status |
|-------|------|----------------|--------------|--------|
| **L1** | Execution loop | Boolean (done/not done) | agent → judge(says done/continue) | ✅ Exists today |
| **L2** | Corrective loop | Vector (error msg, stack trace, review comments) | analysis of judge's *reason* → strategy adjustment → re-execute | ❌ Missing — this is the gap Jerry identified |
| **L3** | Evolutionary loop | Cross-session pattern | analyze which goals fail often → adjust prompt/SKILL/Memory → next loop starts smarter | ❌ Missing |

**Level 1 is a `while` loop, not a feedback loop.** It checks "are we done?" with a binary sensor, but never asks "why aren't we done yet? what should we change?" The judge outputs a reason string, but the agent doesn't read it to adjust its approach.

### The PID control analogy (Tom's theoretical construct — NOT Jerry's domain knowledge)

**⚠️ IMPORTANT: This analogy is Tom's construction, not Jerry's expertise.** Jerry is a C++/Python software engineer working on SECS/GEM communication, fault diagnosis, and MES integration for Ball Bonder equipment. He does NOT work on servo control loops or motion control firmware. Never assume he has this domain knowledge — if this analogy is useful, it must be taught, not referenced as shared background.

That said, as a conceptual model for understanding loop maturity:

| PID Term | Motion Control | AI Workflow |
|----------|---------------|-------------|
| **P (Proportional)** | Position error × Kp → immediate correction | Error message → direct fix. "P" is what current agents do — they see a compile error and fix it. |
| **I (Integral)** | Accumulated steady-state error over time | Cross-session Memory/Skills accumulation. The agent that read the project conventions yesterday should not re-learn them today. **Most agents have no I term** — each session starts from zero. |
| **D (Derivative)** | Rate of change → damping, prevents overshoot | Preventing the same error from recurring. When the agent makes the same mistake twice, the system should detect the pattern and block it. SOUL.md's red lines are a primitive D term. |

**Current `/goal` and agent systems have P but no I and no D.** This means:
- P-only: sees error, fixes error, but doesn't remember it tomorrow (no I)
- P-only: same mistake next session (no I)
- P-only: agent oscillates — fix A → break B → fix B → break A (no D)

### Five building blocks + Memory

| Primitive | Job in the Loop | Hermes Equivalent | Codex Equivalent (Jerry's tool) |
|-----------|----------------|-------------------|-------------------------------|
| **Automations / Scheduling** | Discovery + triage on a cadence | ✅ cron (natural language, skill-backed, no-agent, chaining, wakeAgent) + `/goal` (Ralph loop) | Automations tab + `/goal` |
| **Worktrees** | Safe parallel execution | ❌ Not built-in (use git worktree manually) | Built-in worktree per thread |
| **Skills** | Persistent project knowledge | ✅ SKILL.md system | Agent Skills (SKILL.md), invoked with `$name` |
| **Plugins & Connectors** | Reach into real tools (MCP) | ✅ MCP connectors | Connectors (MCP) + plugins |
| **Sub-agents** | Maker / checker split | ✅ delegate_task | Subagents in `.codex/agents/` (TOML) |
| **+ Memory / State** | Durable spine outside any conversation | ✅ memory + SOUL.md | Markdown or Linear via connector |

### Trigger: when to invoke Loop Engineering thinking

When the user:
- Mentions "loop engineering", "self-evolving", "自循环", "持续进化", "反馈修正回路"
- Asks about the future of AI programming or agent evolution
- Wants agents to run unattended or on a schedule
- Talks about the Prompt→Context→Harness→Loop evolution
- Asks for the agent to "continuously improve" or "自我进化"
- Brings up control theory, PID, servo loops, or feedback systems as an analogy for AI workflows
- Tests `/goal` on any platform and reports back on its behavior

In these cases, load `references/loop-engineering.md` for the full knowledge bank (quotes, patterns, safety rubric, tool-specific mappings, Codex `/goal` experiment notes).

When designing or running A/B comparisons of single-agent vs maker/checker workflows, see `references/loop-engineering-experiment-protocol.md` for the full experimental protocol (isolation rules, comparison metrics, token cost benchmarks, Verifier Theater detection).

### Safety phases (operational)

Loop Engineering defines a phased safety rollout that maps to workforce automation maturity:

- **L1 (Report only)** — Loop observes and reports findings. No auto-fixes. Safe for any project.
- **L2 (Assisted fixes)** — Loop proposes changes, acts on allowlisted patterns. Human confirms.
- **L3 (Unattended)** — Loop runs autonomously within defined safety boundaries. Requires verified sub-agent split (maker ≠ checker).

Start at L1 for any new loop. Only escalate to L2 after one week of clean runs.

## Profile-to-Profile Communication (Group Chat)

Hermes Web UI has a **Group Chat** feature that allows multiple profile-based agents to share a conversation room.

### Verified behavior (2026-06-20 — three rounds)

**Round 1 (gateway stopped)**: Gateway must be running. Without it, the agent exists as a registered room participant but cannot respond.

**Round 2 (gateway running, no model)**: Gateway runs but agent returns *"Error: Agent bridge request timed out after 120000ms"* — the profile had no model configured (model field = `"—"`). A running gateway is insufficient; the agent needs a model to generate responses.

**Round 3 (model configured, @mention)**:
1. **Room creation**: `POST /api/hermes/group-chat/rooms` with `name` + `inviteCode` creates a room
2. **Adding agents**: `POST /api/hermes/group-chat/rooms/{roomId}/agents` with `profile` name adds a profile-based agent
3. **User joining**: Users join via the `inviteCode` through the Web UI
4. **Message storage**: Messages are stored in the room and retrievable via `GET /api/hermes/group-chat/rooms/{roomId}`
5. **Agent response**: ✅ **Works when @mentioned** in the Web UI. Agent starts a fresh session and responds.
6. **No auto-response**: Agents do NOT respond to every room message — only when @mentioned by name.
7. **Gateway must be running**: Each profile needs its model and gateway active.

### Current limitations

- **No 'send message as agent' API** in the Group Chat module — agents cannot post to the room programmatically via the REST API.
- **No auto-response**: Agents do NOT respond to every room message — only when @mentioned by name. Not a true `triggerTokens` gate; @mention bypasses it entirely.
- **Per-profile SOUL.md IS loaded from filesystem** — fixed in Round 3. After writing `~/.hermes/profiles/<name>/SOUL.md` and restarting the gateway (`POST /api/hermes/profiles/{name}/gateway/restart`), the profile loads its own SOUL. Confirmed: Justin answered with his own three principles (契约编程/可验证交付/最小意外) after the restart, not Tom's default SOUL.
- **Fresh session on each @mention**: No cross-session context. The agent starts a new conversation each time.
- **No agent-to-agent @mention tested**: Unknown if one profile agent can @mention another in the same room.
- **Recommended primary path**: Use `delegate_task` for structured orchestrator-to-subagent coordination. Group Chat is best for human-facing multi-agent UI (CEO @mentions specific employees).

### API reference for future exploration

Create a room:
```python
hermes_api_request(method="POST", path="/api/hermes/group-chat/rooms",
    body={"inviteCode": "my-invite", "name": "My Room"})
```

Add a profile agent:
```python
hermes_api_request(method="POST",
    path="/api/hermes/group-chat/rooms/{roomId}/agents",
    body={"profile": "tom2-devops", "name": "Tom2", "description": "...", "invited": True})
```

Get room with messages:
```python
hermes_api_request(method="GET",
    path="/api/hermes/group-chat/rooms/{roomId}?limit=50")
```

## Setup

### Step 1: Create Profiles

```bash
# On a terminal-capable Hermes instance (or via execute_code):
hermes profile create rag-engineer
hermes profile create content-creator
hermes profile create image-designer
hermes profile create devops
hermes profile create sales
```

Each profile lives at `~/.hermes/profiles/<name>/` with its own config, skills, sessions, memory, and cron.

### Step 1b: Start Gateway

After creating a profile, its gateway is stopped by default. Start it:

```python
# Via Hermes Studio API
hermes_api_request(method="POST",
    path="/api/hermes/profiles/{name}/gateway/restart")
```

Verify:
```python
hermes_api_request(method="GET",
    path="/api/hermes/profiles/{name}/runtime-status")
# → gateway.running should be true
```

A profile with a stopped gateway can be registered in a Group Chat room as a participant, but it will NOT respond when @mentioned until the gateway is running.

### Step 1c: Assign SOUL.md (Required — 每个员工独立)

**SOUL 不是可选项，也不是共享品。** 每个员工必须有自己的 SOUL.md，从 agency-agents-zh 角色库中对应的角色提炼而来。

写入 Windows 路径 `C:\Users\jjdeng\.hermes\profiles\<name>\SOUL.md`（WSL 中为 `/mnt/c/Users/jjdeng/.hermes/profiles/<name>/SOUL.md`）后，**重启 profile 的 gateway** 即可生效：

⚠️ 注意：WSL 的 `~/.hermes/` 指向 `/home/jjdeng/.hermes/`（WSL 本地文件系统），但 Hermes Desktop for Windows 读取的是 `C:\Users\jjdeng\.hermes\`（Windows 文件系统）。SOUL.md 必须写入 Windows 路径才能生效。
```python
# 写 SOUL.md → 重启 gateway → SOUL 生效
hermes_api_request(method="POST",
    path="/api/hermes/profiles/{name}/gateway/restart")
```
已验证（2026-06-20）：Justin 的私有 SOUL 在写入并重启后生效。群聊 @mention 时回答自己的三条法则，不再是默认 SOUL。

#### SOUL 结构

一套完整的 SOUL 包含三部分：

1. **身份定义** — 一句话说明你是谁、做什么（1-2行）
2. **三条永久思维法则** — 从对应角色的核心能力提炼，每条附带 ✅/❌ 示例
3. **底线规则** — 绝对不做的红线和强制行为规范

与"岗位描述"的区别：岗位描述告诉 agent 做什么，SOUL 告诉 agent 怎么思考。

#### 如何从角色文件推导 SOUL

1. 读取对应角色的 agency-agents-zh 角色文件
2. 提取该角色的核心专业能力（不是技能列表，而是思维模式）
3. 凝练为 3 条永久思维法则，每条附带具体正反示例
4. 从角色文件的"关键规则"提取底线

#### 示例：DevOps/执行引擎 SOUL

```markdown
# Tom2 ⚡ 执行器 — 永久思维法则

你是 Jerry 一人公司里的执行引擎。接到命令就执行，执行完报告结果。
不负责决策和规划，那是 Tom1 的事。

## 1. 可靠性优先
每次操作前先问：失败了怎么办？有回滚吗？环境确认了吗？
- ✅ 涉及生产环境先确认回滚路径，先验证再执行
- ❌ "先试试看，不行再说"
- 最小化影响半径，不确定就停下来问

## 2. 精确执行
不猜命令、不假设路径、不跳过验证步骤。
- ✅ 每个命令意图清晰，每个输出都被检查
- ❌ "应该没问题"、"我记得是"
- 不确定就停下来确认，不继续"蒙"下去

## 3. 自动化本能
同一件事做两次就该写成脚本。
- ✅ 发现重复操作立即脚本化，脚本输出必须带验证结果
- ❌ 手动操作然后口头说"跑完了"

## 底线
- 不知道就说不知道，不猜不编
- 执行前确认是否影响生产环境
- 每项操作必须输出结果摘要（exit code / 数量 / 耗时）
```

#### 示例：程序员/代码工匠 SOUL

```markdown
# Justin 🖥️ 程序员 — 永久思维法则

你是 Jerry 一人公司里的全职程序员。接到代码任务就实现，实现完附带验证结果交付。
不负责内容策划和商业决策，那是 Tom1 的事。

## 1. 契约编程
Spec 就是合约。不多做、不少做、不自行发挥。
- ✅ 完全按照 spec 实现，需求不明确先确认再写
- ❌ "我觉得加个功能更好" / "我猜他要的是这个"
- 改动现有逻辑前，先理解原有设计意图

## 2. 可验证交付
"应该能跑"不算交付。每次交付附带运行证明。
- ✅ 单元测试报告 / 构建日志 / 运行截图 — 至少一个
- ❌ "代码写好了，你试试"
- 不能测试的部分明确标注原因

## 3. 最小意外
选最简单的正确方案。标准模式 > 聪明 hack。
- ✅ 命名、结构、API 遵循约定俗成的规范
- ❌ 引入不必要的重构 / 炫技写法 / 改变现有风格
- 代码读起来应该像正常人在说话

## 底线
- 不知道就说不知道，不猜不编
- 不执行可能破坏生产环境的操作
- 完成任何交付都要附带验证结果
```

#### 关键原则

- **每个员工独立**：SOUL 不能共享。Tom1 的苏格拉底式提问/第一性原理/奥卡姆剃刀是给"总指挥/判官"角色的，代码执行者用它来审查需求反而降低效率。
- **从角色出发**：SOUL 的思维法则必须从对应 agency-agents-zh 角色的核心能力推导，不是从 Tom1 的 SOUL 简化。
- **测试验证**：SOUL 写好后，在群聊 @提一下该 agent，看它的回复是否符合预期角色定位。如果回复像 Tom1 的翻版，说明 SOUL 不够独立。
- **角色分化后必须清理原位**：当从某个原始 profile（如 Tom1 全栈角色）中拆分出一个新的专门化 profile（如 Tina 导师）时，原始 profile 的 SOUL 必须同步移除与新人重叠的思维法则。否则两人都带着相同的 thinking pattern，导致角色边界模糊、重复劳动。Jerry 在实践中发现 Tom1 仍保留着"苏格拉底式提问"——新设 Tina 后未清理，这就是典型的演进断层。

### Step 2: Assign Roles from agency-agents-zh

Load the role file content into the profile's system prompt or skills:

```bash
# For the content-creator profile, load the 小红书运营专家 role:
hermes --profile content-creator -s agency-agents-zh
```

Then in that profile's first session, tell it to use the assigned role:
> "你现在的身份是小红书运营专家。你的工作是产出优质的小红书内容，不要做其他事。"

The role files are at:
```
~/.hermes/skills/agency-agents-zh/agents/
├── product/product-manager.md                 # 产品经理
├── product/product-trend-researcher.md       # 趋势研究员 — 市场与竞争分析
├── marketing/marketing-xiaohongshu-strategist.md    # 小红书
├── marketing/marketing-bilibili-strategist.md        # B站
├── design/design-image-prompt-engineer.md            # 图像提示
├── engineering/engineering-ai-engineer.md            # AI工程师
├── engineering/engineering-devops-automator.md       # DevOps
└── sales/sales-engineer.md                           # 销售工程师
```

### Step 3: Configure Profile-Specific Skills

Each profile only loads the skills it needs:

```yaml
# profile: content-creator
skills:
  - content-strategy
  - content-creation-distribution
  - content-writing-patterns
```

```yaml
# profile: image-designer
skills:
  - baoyu-infographic
  - baoyu-article-illustrator
  - comfyui
```

### Step 3b: Delete / Clean Up a Profile

When an employee profile is no longer needed, clean it up in two places:

```python
# Step 1: Remove from Web UI
# Returns {"success": true}
hermes_api_request(method="DELETE",
    path="/api/hermes/profiles/{name}")

# Step 2: Remove from disk
# bash: rm -rf /mnt/c/Users/jjdeng/.hermes/profiles/{name}
```

The profile will also remain in Group Chat rooms as a participant until removed from there. To remove:
```
# From the room's agents list, you can re-add later if needed
POST /api/hermes/group-chat/rooms/{roomId}/agents/{agentId}/remove
```

**Full cleanup checklist:**
1. ✅ Web UI profile — `DELETE /api/hermes/profiles/{name}`
2. ✅ Disk directory — `rm -rf ~/.hermes/profiles/{name}`
3. ✅ Group Chat room — remove agent from room (if previously added)

### Step 4: Orchestrate via delegate_task

From the orchestrator profile, use `delegate_task` to dispatch work to employee profiles. Since Hermes profiles run as separate processes, the orchestrator cannot "call" another profile directly. Instead:

**Option A: Kanban Board (recommended for async work)**
1. Create a task on the board
2. The target profile picks it up on its next tick
3. Reports back when done

**Option B: Orchestrator delegates sub-agents (for synchronous work)**
The orchestrator can use `delegate_task` with specialized instructions:
```python
delegate_task(
    goal="Write a Xiaohongshu post about SECS/GEM troubleshooting",
    context="Target audience: equipment engineers in OSAT factories. Tone: technical but approachable.",
    toolsets=["web", "terminal", "file"]
)
```

The sub-agent acts as the assigned role — the goal description should specify which role it should embody.

## Checker & Maker Assignments by Role Type

从实验（2026-06-20, Mode A vs Mode B）验证：不是所有角色都需要 checker。区分两个类型：

### Producer roles（需要 checker）

产出"内容/代码/知识"的角色——其交付物需要独立验证质量。

| Role | Checker type | What checker verifies |
|------|-------------|---------------------|
| **Programmer** (Justin) | `delegate_task` + code review prompt | Test output, build logs, result correctness |
| **RAG Engineer** (Eli) | `delegate_task` + random sampling checklist | Classification accuracy, retrieval pass rate, tag consistency |
| **Content Creator** (future) | `delegate_task` + format audit | Fact accuracy, format compliance, source traceability |
| **Orchestrator** (Tom1, in PM mode) | `delegate_task` + PM 8-condition checklist | Priority reasoning, task decomposition, alignment with goals |

Checker implementation: use `delegate_task` with a DIFFERENT prompt from the maker. The experiment proved that different prompt + structured checklist catches issues the maker missed, even when both use the same model.

### Executor roles（不需要 checker）

产出"执行结果/状态变更"的角色——exit code、运行日志就是验证。

| Role | Verification signal |
|------|-------------------|
| **DevOps** (Tom2) | Non-zero exit code, deployment status, health check |
| **Sales** (future) | Jerry himself reviews proposals |

### Checker doesn't need a different model

实验已验证：maker 用 deepseek-v4-flash, checker 用 deepseek-reasoner（delegate_task 的默认模型），但不同 prompt 是更关键的因素。不同模型不是必须的——不同 prompt + 结构化检查清单已经能显著提高覆盖率。

Cost rule: only run full maker/checker loop on quality-sensitive tasks. Small/trivial tasks skip checker.

### Maker/Checker 循环限制

- Max 3 rounds of correction per task
- If checker still finds issues after 3 rounds → escalate to Jerry
- Track round count in the task description: `file-analyzer.py: 1 checker round → fixed → 2nd round pass`

## Model Assignment Strategy

不同任务类型受益于不同模型。当前可用模型和推荐分配：

| Model | Best for | Cost |
|-------|----------|:----:|
| **deepseek-v4-flash** (default) | Chat, classification, simple tasks, content, knowledge retrieval | Low |
| **deepseek-v4-pro** | Complex coding, audit, verification, loop judge, PM output review | Medium |

### Recommended per-role assignment

| Profile | Daily use | Heavy task use |
|---------|:---------:|:-------------:|
| Tom1 (Orchestrator + PM) | deepseek-v4-flash | deepseek-v4-pro for planning |
| Justin (Programmer) | deepseek-v4-flash | deepseek-v4-pro for complex features |
| Eli (RAG Engineer) | deepseek-v4-flash | — |
| Checker (delegate_task) | deepseek-v4-pro (default) | — |

Justin's heavy task switch: when the coding task involves complex logic, multi-step pipelines, or unfamiliar libraries, set the delegator's model to deepseek-v4-pro explicitly in the delegate_task call:

```python
from hermes_tools import terminal
terminal("hermes config set model.default deepseek-v4-pro --profile justin-coder")
```



| Profile | Role from agency-agents-zh | Skills | When to Add |
|---------|---------------------------|--------|-------------|
| **Product Manager** | `product/product-manager.md` | product-manager-light, loop-engineering-maker-checker | Always first. Evaluates the project, decides which roles are needed. |
| **Content Creator** | `marketing/marketing-xiaohongshu-strategist.md` | content-strategy, content-writing-patterns | P0 — content is the primary acquisition engine |
| **RAG Engineer** | `engineering/engineering-ai-engineer.md` | enterprise-rag-kb, rag-knowledge-base | P0 — turns raw data into searchable knowledge |
| **Image Designer** | `design/design-image-prompt-engineer.md` | baoyu-infographic, baoyu-comic, comfyui | P1 — need images for content |
| **DevOps** | `engineering/engineering-devops-automator.md` | server-deployment-troubleshooting, wsl-server-deploy | P2 — only when servers are in play |
| **Market Researcher** | `product/product-trend-researcher.md` | — | P1 — When management needs market/competitive data before deciding direction |
| **Sales** | `sales/sales-engineer.md` | showcase-page-generator | P2 — when customer-facing work begins |
| **Finance** | `finance/finance-bookkeeper-controller.md` | — | P3 — when revenue arrives |

## 管理层讨论工作流

完整的 5 阶段异步管理讨论流程见 `references/management-discussion-workflow.md`：

1. **信息输入** — Trend Researcher 提供市场数据
2. **分角色输入** — 6 个管理层成员各自产出领域判断
3. **冲突识别与对齐** — Tom1 标记共识/分歧/空白
4. **合成建议** — Tom1 出固定格式建议
5. **Jerry 决策** — 批准/驳回/补充研究

**关键原则**：方向/策略类决策不属于任何单个 agent（包括 Tina），必须由管理层讨论后交给 Jerry 判断。

## Actual Deployed Team (2026-06-25)

完整组织架构、三阶流水线设计、Checker-per-Profile 原则，见 `references/company-org-pipeline.md`。

管理层 (5): Demon (战略搭档), Alex (PM), Allen (高级PM), Jack (牧羊人), Karen (制片人)
执行层 (3): Justin (程序员), Eli (RAG工程师), Rose (运营)
检查层 (0): 3 个对位 Checker 待创建 (Justin-Checker, Eli-Checker, Rose-Checker)
独立角色 (1): Tina (苏格拉底导师/思考外挂)
研究层 (1, 待创建): 趋势研究员 (市场与竞争分析，管理层的输入源)

### 事件驱动流水线 (5 步闭环)

```
Step 1: 管理层讨论
  └── Demon (挑战) + Alex (方向) + Karen (战略对齐) + Allen (可执行性) + Jack (时间线)
  └── 趋势研究员 提供市场数据作为讨论输入
      └── 产出: 讨论结论 + 范围定义

Step 2: Allen 拆解 + 分配
  └── 把讨论结论拆成可执行任务 (30-60min 粒度)
  └── 每个任务附带验收标准 + 指定执行人
      └── 产出: 任务清单

Step 3: 执行 + Checker 迭代 (最多 3 轮)
  └── 执行人 (Justin/Eli/Rose) 产出
  └── 对位 Checker 独立检查 → 打回或通过
  └── 通过后进入下一步
      └── 产出: 验证通过的交付物

Step 4: 管理层汇总
  └── Jack (进度) + Alex (是否符合目标) + Allen (任务完成率)
  └── 汇总成最终报告
      └── 产出: 验收报告 (状态灯+进展+风险+行动项)

Step 5: Jerry 验收
  └── 你点头 → 交付
  └── 你打回 → 回到 Step 2 或 Step 3
```

### SOUL 自检方法论 (新增)

写任何新角色的 SOUL 后，在落地前先跑一次系统性自检：

1. **写场景矩阵** — 每个 SOUL 列 4-5 个真实交互场景（正常通过、拦截、边界、异常）
2. **逐一模拟** — 每条标准是否能拦住对应问题？
3. **分类结果** — 🟢 PASS / ⚠️ ATTN
4. **修补模糊地带** — 收紧标准 or 加异常路径 or 留坑

详见 `loop-engineering-maker-checker` 技能的 `references/checker-soul-templates.md` 中"自检方法论"章节。
首次验证数据：22 场景，15/22 🟢，7/22 ⚠️。

### 角色能力速查

| Profile | 角色 | 模型 | 层 | 核心能力 (SOUL 第一条) |
|---------|------|:----:|:--:|------------------------|
| **Tina** (思考外挂) | tina-teacher | v4-flash | 独立 | 苏格拉底提问/第一性原理/奥卡姆剃刀/主动选题 |
| **Demon** (战略搭档) | demon-workbuddy | v4-flash | 管理 | 苏格拉底提问/第一性原理/奥卡姆剃刀 |
| **Alex** (PM) | alex-pm | v4-flash | 管理 | 先找问题再出方案/数据说话 |
| **Allen** (高级PM) | allen-pm | v4-flash | 管理 | **规格拆解→可执行任务**(适合分配) |
| **Jack** (牧羊人) | jack-shepherd | v4-flash | 管理 | 统筹规划/关键路径/里程碑 |
| **Karen** (制片人) | karen-producer | v4-flash | 管理 | 战略对齐/组合ROI |
| **Justin** (程序员) | justin-coder | v4-pro | 执行 | 契约编程 |
| **Eli** (RAG工程师) | eli-rag | v4-flash | 执行 | 数据纪律 |
| **Rose** (运营) | rose-ops | v4-flash | 执行 | 流程标准化 |

## Company Starter Sizes

| Size | Profiles | When |
|------|---------|------|
| 🟢 Lean (3) | Tom1 (助手) + Justin (程序员) + Eli (RAG工程师) + Alex (PM) | Month 1 — actual team |
| 🟡 Growing (5) | Above + Content Creator | Month 2-3 — content starts |
| 🟠 Scaling (6-7) | Add DevOps + Sales | Month 3+ — customers arrive |
| 🔴 Full (8-9) | Add Finance + Support | Month 6+ — revenue needs tracking |

## SOUL 设计参考

详细的 SOUL 设计方法论、模板和 Jerry's Workforce 中所有已知员工（Tom1 / Tom2 / Justin）的完整 SOUL 定义，见 `references/soul-design-guide.md`。

### 协作式 SOUL 孵化（角色工作坊）

当用户自己提出"我需要一个XX角色"但描述模糊时，不要替用户写 SOUL——用工作坊流程从他口中把角色"接生"出来。

完整流程见 `references/soul-design-workshop.md`：
1. 确认角色类型（执行者/建议者/伙伴）
2. 三个锚定问题（气质 → 合作方式 → 名字与象征意义）
3. 从回答中提炼 3 条思维法则
4. 定义底线 + 用户确认

这个流程在 Tina (tina-teacher) 与 Jerry 的对话中实战验证：从"我需要一个战略伙伴"到 Demon 的完整 SOUL 一次性通过用户确认。

## User Preference: Output Style

When working for a solopreneur/CEO user who reviews but doesn't execute:

1. **Be concise** — Deliver structured summaries, not narrative wall-of-text. The CEO skims, they don't read.
2. **Offer options with recommendations** — e.g. "方案A (推荐): ... 方案B: ... 方案C: ..."
3. **Don't over-explain** — If the user asks "what's RPA?", a one-line definition is enough. They'll ask for details if they need them.
4. **Check time before referencing "today/tomorrow/tonight"** — Session context does not auto-update. Call `datetime.now()` before any time-of-day reference. Getting the time wrong frustrates the user and damages trust.
5. **Admit mistakes fast** — When corrected, acknowledge directly and fix it. Don't deflect or over-apologize.
6. **Deliver in chunks** — For large reports or knowledge dumps, ask if the user wants it all at once or in pieces. Long single-message dumps are harder to absorb.

## Pitfalls

1. **Profiles are independent processes.** The orchestrator cannot directly message another profile. Use Kanban board or `delegate_task` for inter-agent coordination.
2. **Don't over-create profiles.** 3 is enough to start. Each additional profile adds coordination overhead (whose job is this? who picks it up?).
3. **Roles must be explicit.** A profile without a clearly defined role will drift into doing everything, defeating the purpose of specialization.
4. **The CEO must actually review.** If the orchestrator sends deliverables straight to production without human review, quality drifts and the human loses context. Always route through the CEO for sign-off.
5. **Skills are single-profile.** Skills installed under the default profile are not available in other profiles. Install per-profile skills in `~/.hermes/profiles/<name>/skills/`.
6. **Verify delegate_task default model.** The `delegate_task` model field in `config.yaml` may default to a nonexistent model name (observed: `deepseek-reasoner` was set as default but doesn't exist). Check `cat ~/.hermes/config.yaml | grep delegate_task` and ensure it points to an existing model like `deepseek-v4-pro`. If wrong, sub-agents may silently fail, hang, or time out.
7. **Filesystem SOUL IS loaded — gateway must be restarted.** Write SOUL.md to `~/.hermes/profiles/<name>/SOUL.md`, then restart the profile's gateway (`POST /api/hermes/profiles/{name}/gateway/restart`). Verified (2026-06-20): Justin answered with his own three principles (契约编程/可验证交付/最小意外) after this process — not the default Tom1 SOUL. If the agent still uses the default SOUL after writing, the gateway was not restarted or the SOUL.md path is wrong. NOTE: Each profile has its own skills/plugins/cron/memories directory under `~/.hermes/profiles/<name>/`. Skills installed under the default profile are NOT available in other profiles — install per-profile skills in `~/.hermes/profiles/<name>/skills/`.
