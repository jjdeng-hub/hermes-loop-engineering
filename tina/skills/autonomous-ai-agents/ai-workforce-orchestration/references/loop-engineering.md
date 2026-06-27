# Loop Engineering — Reference Knowledge Bank

> Source: github.com/cobusgreyling/loop-engineering (425★, MIT)
> Canonical essay: Addy Osmani, "Loop Engineering" (June 7, 2026)
> Substack essay: Cobus Greyling, "Loop Engineering" (2026)

## Definition

**Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead.**

A loop is a recursive goal: you define a purpose and the AI iterates (often with sub-agents, verification, and external state) until the goal is complete or the loop decides to hand off to you.

## The Evolution

```
Prompt  →  Context  →  Harness  →  Loop
怎么问      给什么信息    怎么组织      怎么持续产出
                        AI 能力      结果
```

- **Prompt**: Manual prompt-crafting, one turn at a time
- **Context**: RAG, long context windows, project-aware prompting
- **Harness**: Tool use, agent frameworks, MCP, skills (current state of Hermes)
- **Loop**: Self-driving, timed, recursive — agents prompt agents

## Key Quotes

| Person | Role | Quote |
|--------|------|-------|
| Peter Steinberger | — | "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." |
| Boris Cherny | Head of Claude Code, Anthropic | "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops." |
| Addy Osmani | Director, Google Cloud AI | "Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go." |

## Five Building Blocks + Memory

### 1. Automations / Scheduling
The heartbeat of a loop. Discovery + triage on a cadence.
- Codex: Automations tab — pick project, prompt, cadence, environment; results land in a Triage inbox; `/goal` for run-until-done
- Claude Code: Scheduled tasks and cron, `/loop`, `/goal`, hooks, GitHub Actions
- **Hermes**: ✅ Full cron with: natural language scheduling (`"every 2h"`, `"0 9 * * *"`), skill-backed jobs, no-agent script-only mode (`no_agent=True`), job chaining via `context_from`, `wakeAgent` gate for cheap $0 pre-run checks, delivery to any platform. ✅ `/goal` command for run-until-condition-met loops inside sessions (with judge model, turn budget, `/subgoal` for mid-loop criteria, persistence across sessions).

**Key primitive: `/goal`** — keeps going until a verifiable stopping condition is true. After every turn, a separate small model checks whether the goal is met (maker/checker split on the stop condition itself).

### 2. Worktrees
Safe parallel execution. Two agents cannot write the same file.
- Codex: Built-in worktree per thread
- Claude Code: `git worktree`, `--worktree` flag, isolation: worktree on subagent
- Hermes: Not yet available

### 3. Skills
Codify project knowledge so agents don't re-derive it every run.
- Codex: Agent Skills (SKILL.md), invoked with `$name` or implicitly
- Claude Code: Agent Skills (SKILL.md)
- Hermes: ✅ SKILL.md system — fully aligned

**Skill vs Plugin**: The skill is the authoring format. A plugin is how you ship it (bundle multiple skills + connectors).

### 4. Plugins & Connectors (MCP)
Reach into real tools — issue trackers, databases, Slack.
- All three tools speak MCP. Connectors written for one usually work in the others.

### 5. Sub-agents
The most useful structural element: keep the maker away from the checker.
- Codex: Subagents defined as TOML in `.codex/agents/`
- Claude Code: Subagents in `.claude/agents/`, agent teams
- Hermes: ✅ delegate_task — aligned

**The critical insight**: The model that wrote the code is too nice grading its own homework. A second agent with different instructions (and sometimes a different model) catches what the first one talked itself into.

### + Memory / State
The spine outside any conversation. A markdown file, a Linear board — anything that lives outside the single conversation.
- Agents forget everything between runs. Memory must be on disk, not in context.
- Hermes: ✅ memory + SOUL.md — aligned

## 7 Production Patterns

| Pattern | Cadence | Starter | Safety Level | Token Cost |
|---------|---------|---------|-------------|------------|
| Daily Triage | 1d–2h | minimal-loop | L1 (report only) | Low |
| PR Babysitter | 5–15m | pr-babysitter | L1 (watch mode) | High |
| CI Sweeper | 5–15m | ci-sweeper | L2 (cautious fixes) | Very high |
| Dependency Sweeper | 6h–1d | dependency-sweeper | L2 (patch-only) | Medium |
| Changelog Drafter | 1d or tag | changelog-drafter | L1 (draft only) | Low |
| Post-Merge Cleanup | 1d–6h | post-merge-cleanup | L1 (off-peak) | Low |
| Issue Triage | 2h–1d | issue-triage | L1 (propose-only) | Low |

## Anatomy of a Loop (flow)

```
Schedule / Automation
  → Triage Skill (reads CI failures, open issues, recent commits)
    → Read + Write STATE / Memory
      → Isolated Worktree
        → Implementer Sub-agent
          → Verifier Sub-agent (tests + gates)
            → MCP / Git / Tickets
              → Human Gate?
                ├─ safe / allowlisted → Commit / PR / Action
                └─ risky / ambiguous → Escalate to human with full context
```

## Safety Levels

| Level | Behavior | When to Use |
|-------|----------|------------|
| **L1 (Report only)** | Loop observes, logs findings. No auto-fixes. | First week of any new loop. Safe for production. |
| **L2 (Assisted fixes)** | Loop proposes changes, acts on allowlisted patterns. Human confirms. | After L1 runs clean for 1 week. Known-safe operations. |
| **L3 (Unattended)** | Full autonomous operation within defined safety boundaries. | Requires verified maker/checker split. Budget alerts configured. Kill switch tested. |

## Caveats (from Addy Osmani)

1. **Token costs can explode** with sub-agents and long-running loops.
2. **Verification is still on you.** Unattended loops make unattended mistakes.
3. **Comprehension debt grows faster** unless you read what the loop ships.
4. **Two people can run the same loop and get opposite results.** One uses it to move faster on work they understand deeply. The other uses it to avoid understanding the work at all. The loop doesn't know the difference.
5. **Comfortable posture is dangerous.** When the loop runs itself, it's tempting to stop having an opinion. "Designing the loop is the cure when you do it with judgment and the accelerant when you do it to avoid thinking."

## Codex-specific Loop Engineering (Jerry's tool)

Jerry uses **Codex CLI** (OpenAI), not Claude Code. Codex has first-class Loop Engineering support:

### Codex's built-in Loop primitives

| Primitive | Codex Name | How to use |
|-----------|-----------|------------|
| **Goal loop** | `/goal` | Give a verifiable condition ("all tests in test/auth pass and lint is clean"). A separate judge model checks after each turn. Supports pause/resume/clear. |
| **Automations** | Automations tab | GUI-based: pick project, prompt, cadence (interval or cron), environment. Results land in a Triage inbox. Can call skills with `$skill-name`. |
| **Skills** | Agent Skills | SKILL.md in `.codex/skills/`. Invoked with `$name` or automatically when task matches description. Plugins bundle skills + connectors for sharing. |
| **Sub-agents** | Subagents | TOML files in `.codex/agents/` each with name, description, instructions, optional model and reasoning effort. Security reviewer can be a strong model on high effort while explorer is a fast read-only thing. |
| **Worktrees** | Built-in | Each thread gets its own worktree automatically. No collision between parallel agents. |

### Key Codex flags for Loop Engineering

| Flag | Use |
|------|-----|
| `codex exec "prompt"` | One-shot execution |
| `/goal <condition>` | Keep going until condition is met |
| `--full-auto` | Auto-approve sandboxed changes |
| `$skill-name` | Call a skill by name in your prompt |

### Codex Automation → Hermes cron mapping

| Codex Feature | Hermes Equivalent |
|--------------|-------------------|
| Automations tab | `hermes cron create` + `/cron add` |
| Triage inbox | Delivery to platform (Telegram file, etc.) |
| Skill calling in automations | `--skill` flag on cron jobs |
| `/goal` | `/goal` (same concept, independent implementation) |
| Per-thread worktree | No built-in equivalent |

Reference: https://github.com/openai/codex
