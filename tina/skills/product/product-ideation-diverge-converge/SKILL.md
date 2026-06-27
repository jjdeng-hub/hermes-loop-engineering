---
name: product-ideation-diverge-converge
description: Structured brainstorming for indie product ideas — iterate through multiple angles, collect all candidates, then filter. Used when a previous product direction failed and the user needs fresh ideas.
---

# Product Ideation: Diverge → Converge

## When to use
- User says "my current product/plan isn't working" and needs new ideas
- User wants to brainstorm product directions but doesn't know where to start
- Previous product failed (competition, no market, no stickiness)
- User is a solo developer / indie hacker looking for fast变现 side projects

## Methodology

### Phase 1: Understand constraints (before diverging)
Ask / identify:
- What went wrong with the previous attempt? (competition? market? stickiness?)
- User's tech stack & skills
- User's personal pain points (they understand these best)
- Time/money constraints for development
- Preferred monetization model (subscription? one-time? freemium?)
- Platform for promotion (Xiaohongshu? Douyin? WeChat?)

### Phase 2: Diverge — iterate through angles

Systematically brainstorm from multiple distinct angles. **One angle at a time.** Keep asking "what else?" until the user runs out of ideas for that angle, then switch angles.

**Recommended angles to rotate through:**

1. **Tool type angle** — what kind of tool? (format tool? decision aid? anti-AI?)
2. **Audience angle** — college students? 9-5 workers? moms? creators? devs?
3. **Emotion angle** — what emotion does it address? (anxiety? FOMO? insecurity?)
4. **Contrarian angle** — what's everyone doing? go the opposite direction
5. **Social currency angle** — does the output make people want to share it?
6. **Hyper-specific pain angle** — narrowest possible single scenario
7. **Data moat angle** — does it get better with more usage? (stickiness)
8. **Physical/printable angle** — virtual things are forgettable, physical things aren't
9. **Conversation/confession angle** — sometimes people just want to be heard
10. **Anti-hustle angle** — when everyone is anxious, "not being anxious" is differentiation
11. **Soft skills angle** — as AI replaces hard skills, soft skills become premium

**Cross-pollinate:** After collecting ideas from multiple angles, combine them. E.g., Emotion × Social Currency = AI焦虑测试分享卡.

### Phase 3: Collect & format

Every idea needs to be presented as:
- **Name** — memorable label
- **One-liner** — explain it in one sentence
- **Monetization** — how do you charge?
- No need for full product spec at this stage

### Phase 4: Converge (deferred to later session)

The actual filtering happens in a separate session. Steps:
1. Let the user pick 3-5 favorites
2. Deep-dive each one: product structure, competition, dev cost, promotion strategy
3. Pick ONE to execute
4. Create a development plan (MVP scope, timeline, tech stack)

## User preferences to respect
- Ask "any more angles you want to explore?" before converging
- Save the full list to memory for reference in future sessions
- User may want to add more ideas during filtering — that's normal, keep collecting
- Each idea needs both: (1) what it is (2) how it makes money
- User likes questionnaires/tests that generate shareable report cards (like MBTI format)

## Pitfalls
- Don't start converging too early — user wants to see ALL options first
- Don't dismiss any idea during divergence phase — collect first, judge later
- Don't propose AI-wrapper products — user explicitly rejected "用户也能在AI上做" ideas
- Don't propose products where AI is the main selling point — user wants AI hidden in the backend
- Don't make assumptions about user's skills (e.g., Dify) without verifying
- **Don't assume what the customer needs beyond the tool.** When a user wants a tool installed, they already have their own use case. Don't pitch "and I'll also teach you what to do with it" — the value is in the installation/configuration, not in defining their workflow
- **Don't embellish the user's work context.** When the user says "I write C++ at a desk," don't romanticize it into "on the production line at the intersection of hardware and AI." Ask what their day-to-day actually looks like before drawing conclusions about their unique advantages
- **Don't flip-flop on constraints mid-conversation.** If you agree on a constraint (e.g., "don't worry about income, just build for yourself"), do NOT ask the opposite question two messages later ("but do you care more about learning or income?"). Hold constraints steady once set. If you genuinely think a constraint needs revisiting, flag it explicitly: "We said X earlier — do you want to revisit that?"
- ⚠️ **CRITICAL: Don't build without problem validation.** When a user proposes building something (a system, a tool, a platform), do NOT jump to coding. Stop and ask: "You already do [related activity] naturally — where's the actual pain? What breaks in your current flow?" If the user can't articulate a clear pain point, the solution is premature. A tracking system layered on top of an already-smooth habit is friction, not value. This pitfall caused the gameification system failure — 3 Flutter iterations built for a problem that didn't exist. Apply Product Intuition Rule #1 from SOUL.md: 先找问题，不要跳到方案。
