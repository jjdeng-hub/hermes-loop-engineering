# Knowledge Base Quality Audit — Experimental Design (2026-06-20)

## Background

Jerry's semiconductor packaging knowledge base has 447 articles (~2,600 images) across 7 domains. This experiment was designed to test the Loop Engineering thesis: **does a single-agent loop ("write code and judge if done") miss quality issues that a maker/checker split would catch?**

## The Claim Being Tested

Jerry's precise definition of Loop Engineering (derived from the Codex `/goal` experiment):

> **"在工作流的合理节点嵌入有质量的反馈修正回路，让系统自动收敛到更优的结果。"**

The corollary: a single-agent loop with a binary judge (done/not-done) at the end is **not** a "feedback correction circuit" — it's a `while` loop with a boolean sensor. It cannot detect subtle quality failures because it has no vector signal, only a pass/fail check.

The test: **does a single-agent audit (Mode A) miss the same class of issues that Codex `/goal` missed — specifically, quality defects that don't cause crashes but matter for product quality?**

## Experiment Design: Mode A vs Mode B

**Task**: Audit 10 knowledge base articles for quality issues.

**Mode A (single agent, mirrors Codex `/goal`)**:
- One agent does the full audit independently
- Uses its own judgment about what "quality" means
- No checklist, no second opinion
- Writes report to `/tmp/mode_a_report.md`

**Mode B (two-pass maker/checker, mirrors Jerry's Loop Engineering definition)**:
- Pass 1 (FREE AUDIT): Same as Mode A — independent judgment, no checklist
- Pass 2 (SYSTEMATIC CHECKER): Against explicit quality checklist:
  1. Image alt text: `![](...)` vs `![描述](...)`
  2. Duplicate image references
  3. Article length (under 200 chars?)
  4. Image count (over 30?)
  5. Any other structural issues
- Pass 3 (RECONCILIATION): Compare two passes, identify what each caught and missed
- Writes report to `/tmp/mode_b_report.md`

**Input**: 10 articles with known issues from the knowledge base:
- 854相关报警合集, KS焊线机框架防反设置流程, Quick Bond简介, WB基础参数, 新建程序之示教焊盘, 半导体封测行业深度报告, 6种无法开机故障处理技巧, 传感器总动员, 工艺类型菜单不翼而飞？, BGA 4 Loop

**Isolation**: Both modes run as separate delegate_task subagents with zero shared context. Neither knows the other exists. Neither knows what "answers" we're looking for.

**Important**: Mode A does NOT get the quality checklist. Mode B gets it ONLY for Pass 2 (checker pass). This is intentional — we want to see if a single agent naturally discovers alt text issues, and whether a second-pass checker with a checklist adds value over the free audit.

## KB Structure

```
Desktop/rag-data/
├── 6种无法开机故障处理技巧.txt           # RAG plain text
├── 6种无法开机故障处理技巧_imgs/
│   ├── article.md                        # Markdown with inline images
│   ├── image1.png
│   ├── image2.png
│   └── ...
└── ... (447 .txt + 447 _imgs dirs total)
```

## Key Finding #1: Universal Missing Alt Text

**439 out of 447 articles (98.2%) have empty alt text on all images.**

Example: `![](...)` instead of `![焊线机报警界面截图](...)`.

**Why this matters**: 
- Accessibility (screen readers for visually impaired engineers)
- SEO for the knowledge base if published online
- Semantic quality: a knowledge product sold to customers should not have "image here" placeholders

## Key Finding #2: Image Quality Issues

| Issue | Affected Articles | Details |
|-------|------------------|---------|
| Duplicate images | ~5 articles | Same image referenced multiple times — may be intentional (article uses same diagram in different sections) or accidental (crawl artifact) |
| High image density (>30) | ~5 articles | Articles like "WB基础参数" (50 images) may be image-heavy by nature, but warrants review |
| Very short content | 1-2 articles | Articles under 200 chars may be incomplete |

## Key Finding #3: No Structural Defects

- **0 orphan .txt files** (all 447 have matching _imgs dirs)
- **0 orphan _imgs dirs** (all 447 have matching .txt files)
- **0 missing image references** (every `![alt](path)` in the markdown resolves to an actual file)
- **0 broken markdown** (no unclosed image syntax, no stray HTML img tags)

The crawl script produced structurally clean output. The quality gap is semantic (alt text, not broken links).

## Experimental Design (Experiment C, deferred)

The planned experiment was:

**Task**: Audit 10 knowledge base articles for quality issues (alt text, duplicate images, content completeness).

**Mode A (single agent)**: One agent does the full audit independently. Hypothesis: it will miss the alt text issue because it's not a "crash" or "error" — the code runs, files exist, so the judge says "done."

**Mode B (maker/checker)**: 
- Maker: same audit task
- Checker: separate sub-agent with different instructions, specifically prompted to look for `![]` patterns and verify each finding independently
- Maker/checker dispute resolution loop

**Expected outcome**: Mode B catches the alt text issue; Mode A misses it. This would validate Jerry's thesis that a single `while` loop with a binary judge is insufficient for quality-sensitive work.

## Results: Mode A vs Mode B

### Mode A (single agent, Codex-style)

**Finding count**: 7 issue categories discovered.
**Report**: 269 lines, 11,504 bytes — thorough, well-structured.

**What it found**:
- Timestamp missing (7/10 articles)
- Future date error: 2037-12-25 (Quick Bond简介)
- Pure-image / zero-text content (2 articles: WB基础参数, 半导体封测行业深度报告)
- Social media boilerplate (3 articles)
- Structurally weak content (4 articles — too short, case descriptions too brief)
- Content disorganization (2 articles — mixed EN/CN, no transitions)
- Outdated content (2 articles from 2011)

**What it MISSED (critical)**:
- **Image alt text missing**: 439/447 articles (98.2%) in the full KB have empty `![](...)` format. Mode A did not flag this as a systematic issue. It mentioned "案例7和案例9只有图片没有描述文字" casually but did not identify it as a quality category.
- **Duplicate images**: "KS焊线机框架防反设置流程" has 12 duplicate image references (img_001.gif x5, img_002.gif x5, img_003.png x6). Mode A called this article "the highest quality" with "no issues found."
- **Quantitative precision**: Issues described qualitatively ("几个问题", "部分文章"), no exact counts.

**Score**: 7/10 issue categories found, but the two most pervasive issues (alt text, duplicates) were completely missed.

### Mode B (two-pass: free audit + systematic checker)

**Finding count**: ~32 individual issues detected, ~26 shared by both passes, 6 unique to Pass 1.

**What BOTH passes found**:
- Alt text missing (10/10 articles, with precise counts per article)
- Duplicate image references (4 articles, with exact duplication counts)
- Pure-image articles (2: WB基础参数, 半导体封测行业深度报告)
- Social media boilerplate (3 articles)
- Future date error (Quick Bond简介)

**What ONLY Pass 1 (free audit) found**:
- Spelling error: "stsich" → "stitch" (checklist never covers this)
- Content truncation: .txt file ends mid-sentence (semantic issue)
- Numbering chaos: mixed digit/Chinese numbering in same article
- Decorative text: "春日限定" unrelated opening text (semantic understanding)
- Layout issue: "教/程" split across line break (visual check)
- Missing video: article says "video attached" but no video file (needs cross-reference)

**What ONLY Pass 2 (checker) contributed**:
- Precise quantification of every issue (exact image counts, exact missing alt counts, exact word counts)
- Consistency guarantee — every article checked against the same criteria
- Verifiable, reproducible results — checklist can be automated

**Pass 2's explicit discovery vs Pass 1's casual mention**:
| Issue | Mode A report | Mode B Pass 2 report |
|-------|--------------|---------------------|
| Alt text missing | Not flagged | ✅ "10/10 articles, 232 images total — 100% missing alt text" |
| Duplicate images | Not flagged | ✅ "4 articles — KS 框架防反: 12 dupes, Quick Bond: 2 dupes, 示教焊盘: 2 dupes, 工艺类型菜单: 3 dupes" |

### Key Finding: Checklist Determines Coverage Ceiling

The biggest lesson: **Pass 2 found alt text and duplicate issues because its checklist explicitly asked for them. It did NOT find spelling errors, content truncation, or decorative text because those weren't in the checklist.**

This directly answers a question Jerry raised: "If Mode A had the same checklist, would it find the same things?" The answer is **yes — but it still wouldn't find the things NOT in the checklist.**

The optimal design is not "mode A vs mode B" but **"mode A + mode B combined"** — a free audit pass for serendipitous discovery, followed by a systematic checklist pass for coverage completeness, with a reconciliation phase that integrates both.

### The Code Review Analogy (Jerry's insight)

Jerry connected the experimental result to his daily workflow:

> **Developer writes code → pushes PR → Reviewer gives feedback → Developer fixes → Merge → Better code**

This maps directly:
| Code Review Step | Loop Engineering Analog |
|-----------------|------------------------|
| Developer writes code | Maker agent produces output |
| Push PR | Write results to file / deliver |
| Reviewer reviews, gives feedback | Checker agent independently verifies |
| Developer fixes based on feedback | Maker revises output based on discrepancy |
| Merge (after all issues resolved) | Final report / deliverable when maker=checker agree |

**The insight**: Code review *is* Loop Engineering — it's a feedback correction node embedded at the right point in the workflow (between "code written" and "merged to main"). The decades-old engineering practice of peer code review is structurally identical to the maker/checker split in AI loops. Jerry's job already follows the Loop Engineering pattern; the question is whether AI tools will adopt the same discipline.

## Implications for Loop Engineering

1. **Content quality loops need semantic judges, not file-existence judges.** A judge that checks "did the agent produce audit_report.md?" vs "did the agent find all instances of pattern X?" are fundamentally different capabilities.
2. **Alt text is the perfect "hidden defect"** — obvious once you know to look, invisible to a generic "does it work?" check. It's the AI equivalent of missing null checks in compiled code.
3. **For the knowledge product**, running a pre-release quality audit loop (single issue: "check all images have descriptive alt text") would be a quick L1 loop that adds real value before any customer-facing deployment.
