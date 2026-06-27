# Loop Engineering Experiment Protocol

> Absorbed from `loop-engineering-experiment` skill (2026-06-17).
> A/B test framework for comparing single-agent (Mode A) vs maker+checker (Mode B) workflows.

## When to Use

Use when you need to **compare** the quality of a single-agent workflow vs a multi-node feedback workflow. After running a Codex/Claude Code `/goal` experiment and you need to replicate with Hermes.

## Core Insight: Code Review IS Loop Engineering

The pattern tested here is structurally identical to daily code review:

| Software development | AI Workflow |
|---|---|
| Developer writes code | Maker agent executes |
| Submits PR | Outputs results |
| Reviewer gives feedback | Checker independently verifies |
| Developer revises | Maker corrects based on feedback |
| CI + Approve to Merge | Two-pass agreement to Deliver |

Code review has been a validated feedback node for decades. AI agents skipping it is the root cause of self-verification failure.

## Isolation Rules

**CRITICAL**: Never share context between Mode A and Mode B. Each must be a `delegate_task` subagent with **no session memory** of each other.

```
Input data → Prepare input file
                ├── delegate_task: Mode A (Single agent audit)
                └── delegate_task: Mode B (Maker + Checker)
                ├── mode_a_report.md
                └── mode_b_report.md
```

## Mode A (Single agent — simulates current /goal state)

```
Goal: Audit N articles for quality issues. Write report to /tmp/mode_a_report.md.
Context: Input file with article paths. No quality rubric provided — agent decides what matters.
```

The agent self-verifies — same problem Codex has: confirmation bias built in.

## Mode B (Maker + Checker — Loop Engineering)

**Phase 1 (MAKER)**: Same prompt as Mode A. Reports findings.

**Phase 2 (CHECKER)**: Separate subagent with explicit quality criteria:

1. Check if ALL images have non-empty alt text (`![desc](file)` not `![](`file`)`)
2. Check for duplicate image references (same image file used >1x)
3. Check for very short articles (<200 chars in md file)
4. Verify every claim in maker's report by re-examining the source
5. Flag any discrepancy

**Phase 3 (RESOLUTION)**: Maker reviews checker's findings, revises report.

## Self-contained outputs

**CRITICAL**: Each mode writes its own structured report. Do NOT rely on yourself to observe and measure during the run. The reports should contain ALL metrics the comparison needs:

- Issues found (per category, per article)
- Issue severity and count
- Quality score (if applicable)
- Methodology description (what they checked and why)

This avoids two problems:
1. The human cannot observe both runs simultaneously
2. Post-hoc analysis introjects bias into the comparison

## Comparison Metrics

| Metric | Mode A | Mode B |
|--------|--------|--------|
| Issues found | Count | Count |
| False positives | Count | Count |
| Missed issues (undetected issues you later find manually) | Count | Count |
| Token cost | From subagent summary | From subagent summary |
| Time to complete | From subagent summary | From subagent summary |

## Known Result: Token Cost

In the 2026-06-20 experiment on 10 articles:
- Mode A (single agent, comprehensive report): ~17K tokens output, ~1M tokens input
- Mode B (two-pass, full verification): ~20K tokens output, ~1.2M tokens input
- The 20% overhead of mode B caught critical systematic issues that Mode A entirely missed

For knowledge base / content quality use cases, the overhead is justified. For trivial tasks, single-pass may be sufficient.

## Key Finding: Free Audit + Structured Checklist

Mode A (single agent, free audit) wrote a 269-line comprehensive report with 7 quality dimensions. **It still missed the most systematic issue: 439/447 articles had empty image alt text.** Mode B's structured checklist in Pass 2 caught it, while Pass 1 (free audit) caught semantic issues the checklist missed.

**Conclusion**: The optimal is NOT one or the other — it's **free audit + structured checklist** combined. Free audit catches non-obvious semantic issues; structured checklist ensures systematic coverage. This mirrors human code review: an experienced reviewer + linter/CI automation.

## Verifier Theater

If the checker is the same model without an external standard (checklist, reference data, or different model), its blind spots converge with the maker. This is "Verifier Theater" — verification looks like it's happening but no new issues surface.

**Signs**: checker agrees with maker on everything, both miss the same systematic issue.

**Mitigations**:
- Give the checker an explicit quantitative checklist
- Different model for checker (if available)
- Checker's job: "find reasons to reject," not "confirm"

## Pitfalls

- Do NOT tell either mode what the "expected" issues are — that ruins the experiment
- Always write input/output to /tmp/ paths for isolation
- Both modes read the SAME input file so results are comparable
- Run Mode A first, then Mode B — do not let Mode B's design contaminate Mode A's prompt
- **Self-verification is not verification**. A single agent writing and verifying is confirmation bias — the agent is too nice grading its own homework. Always use a separate checker subagent.

## References

- cobusgreyling/loop-engineering: failure-modes.md (Verifier Theater, Same-agent-implements-and-verifies)
- Addy Osmani Loop Engineering essay: "The model that wrote the code is way too nice grading its own homework"
