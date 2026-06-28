---
name: content-strategy
description: Jerry's content strategy — personal narrative journey (叙事) about building an AI-powered one-person company. Text-first, Xiaohongshu 图文 as primary platform. "Do → Record" model.
---

# Content Strategy (current approach, effective 2026-06-28)

> **Warning**: This is the THIRD iteration of Jerry's content strategy.
> Prior versions (Douyin video + AI-generated content → Knowledge base monetization) are archived as historical references below.
> **Load this skill before writing or reviewing any content for Jerry.**

## Core Thesis (from DeerLucid, adapted)

> Ordinary people achieve class leap via AI leverage through **personal narrative**, not risky entrepreneurship.
> Anchor from "who I am" and current main job as starting point.
> Turn daily AI learning and application into content fuel.
> **Learn → Do → Record**, not "plan first → execute later".

## Who Jerry Is (the anchor)

- 28, Suzhou, married, C++/Python engineer at K&S (Ball Bonder equipment)
- Salary 15K/mo, expenses 5230/mo
- First job, no industry connections
- **Not an AI expert, not a semi expert.** A regular engineer who happens to run AI agents deeply.

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
| **Xiaohongshu** | Primary. 图文 only. | Not yet started. | Needs account registration (phone number required). |
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

- Chinese preferred. Direct, concise.
- Hate flattery. Love debate, collision, exchange.
- Segment information, not big dumps.
- "我的背景不重要，最终依赖于AI，我能做的就是决策和思考"

## First Article Template

Title: "我把AI员工从合租搬到了独栋别墅——我的Hermes三迁记"

**Full outline + checklist**: `references/first-article-hermes-three-moves.md`

Structure:
1. Hook: Three installs. Three different eras.
2. WSL phase: what it felt like, why it worked, why it didn't
3. Windows phase: upgrade but still constrained
4. Server phase: the endgame
5. Comparison table: which stage fits which user
6. Cliffhanger: next episode — how to get a free Alibaba Cloud server

## Historical archives (old approach)

The following references remain for traceability. Do NOT use them as current guidance without explicit direction:
- references/content-stance-strategy.md — old stance framework (Douyin video era)
- references/social-media-visual-strategy.md — old cover/visual strategy
- references/topic-curation.md — old topic system
- references/xiaohongshu-content-system.md — old Xiaohongshu system (AI-generated content)
- references/content-writing-patterns.md — old writing patterns (AI-generated, not personal narrative)
- references/playbook.md — old full playbook
- references/vibe-and-hope-framework.md — ⚠️ This framework (希望vs感觉) is still VALID and actively used.
