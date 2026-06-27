# Codex `/goal` — Jerry's First-Hand Experiment (2026-06-20)

## Test Setup

Goal given to Codex CLI (Windows desktop, `gamify` project folder):

> In the current project directory (gamify), do the following:
> 1. Create a subfolder called `test-loops/`
> 2. Inside it, write a Python script `file-analyzer.py` that scans `test-loops/` for .txt files, counts lines, non-empty lines, Chinese characters, and English words — outputs markdown report to `test-loops/report.md`
> 3. Create 3 test .txt files with mixed EN/CN content
> 4. Run the analysis and **verify the report is correct** (self-test step)
> 5. ONLY declare done when all steps work AND self-test passed

## What Happened

Codex produced:
- `file-analyzer.py` — fully written, Chinese comments, Unicode CJK regex for char counting, markdown report generation
- 3 test .txt files with mixed Chinese and English content
- `report.md` with correct counts (manually verified by Jerry/Tom)

Turn count: unknown (Jerry didn't count, but it completed in one session).

## Key Finding: Self-Test Step Was Skipped

The goal explicitly requested step 4 (self-verification) and step 5 (only declare done when verified). **The generated script contained zero verification logic** — no assertions, no validation against known data, no cross-checking of counts. The report's numerical accuracy was entirely coincidental (Tom manually verified all counts were correct — they happened to be right, but there was no mechanism ensuring this).

This is consistent with Jerry's diagnosis: **the judge checks "did you produce output X?" not "is output X actually correct?"** The binary done/continue check only sees file existence, not semantic correctness.

## Implication for Loop Engineering Maturity

This experiment confirms the Level 1 ceiling described in the main skill:

- ✅ **Level 1 (execution loop)**: agent → judge → continue/done
- ❌ **Level 2 (corrective feedback)**: The judge didn't notice that "verify results" was a required step that got silently dropped. A Level 2 judge would parse the goal's sub-steps and check each one individually.
- ❌ **Level 3 (evolutionary)**: No cross-session learning — next session's Codex won't know it dropped the self-test step.

## Jerry's Definition of Loop Engineering (derived from this experiment)

After the experiment, Jerry articulated a more precise definition than the mainstream literature:

> **"在工作流的合理节点嵌入有质量的反馈修正回路，让系统自动收敛到更优的结果。"**
> (Embed quality feedback-correction loops at the right workflow nodes, so the system converges to better outcomes autonomously.)

This reframes the mainstream definition ("design a system that prompts agents") in terms of **control theory**: the question isn't "does the loop run?" but "does the loop converge?" — and convergence requires correct placement and signal quality of feedback nodes, not just a binary done/not-done judge at the end.

## Structural Diagnosis: Three Levels of Loop Maturity

The experiment maps to three levels of loop maturity:

| Level | Name | Feedback Signal | What it does | Status in Codex /goal |
|-------|------|----------------|--------------|----------------------|
| **L1** | Execution loop | Boolean (done/not done) | Write script → run → judge says done | ✅ Exists — this is what Codex ran |
| **L2** | Corrective loop | Vector (error msg, specific failure) | Analyze judge's reason → adjust strategy → retry with different approach | ❌ Missing — judge outputs a reason string but agent doesn't read it to change approach |
| **L3** | Evolutionary loop | Cross-session patterns | Track which goals fail → adjust prompts/skills/memory → next session starts smarter | ❌ Missing — every session starts from zero |

**Current `/goal` is a `while` loop, not a feedback loop.** It checks "are we there?" but never asks "why aren't we there? what should we change?"

## Key Takeaways for Future Loop Design

1. **Explicit verification gates**: A goal like "create script, run it, and verify output against known test data" needs an explicit assertion step. A judge that doesn't check sub-step completeness is unreliable for quality-sensitive goals.
2. **The maker/checker split matters**: The agent that wrote the code graded its own homework. Even a separate judge model used the same oversimplified success criterion.
3. **Workflow node placement**: The self-test should have been a separate node (a gate between "code written" and "declared done") with its own verification logic. The current architecture has no such node — it's all one flat loop.
4. **For Jerry's use case (semiconductor knowledge products)**: A judge that can't distinguish "output exists" from "output is correct" would ship inaccurate alarm code explanations or wrong process parameters to customers. This is the real risk of deploying L1 loops in production.
