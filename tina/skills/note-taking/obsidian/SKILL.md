---
name: obsidian
description: Read, search, create, and edit notes in Jerry's Obsidian vault (myBrain). Use also for saving chat insights, decisions, and knowledge learned during Hermes conversations.
platforms: [linux, macos, windows]
---

# Obsidian Vault — myBrain（第二大脑）

This skill covers Jerry's Obsidian vault at `C:\Users\jjdeng\Desktop\myBrain`, configured via `OBSIDIAN_VAULT_PATH` in `~/.hermes/.env`.

## Vault path

**Hardcoded vault path: `C:\Users\jjdeng\Desktop\myBrain`**

The path is set in `~/.hermes/.env` as `OBSIDIAN_VAULT_PATH`. Always resolve to the concrete path above — do NOT pass `$OBSIDIAN_VAULT_PATH` to file tools. Use `read_file`, `write_file`, `patch`, `search_files` with the resolved path.

## Vault folder structure

```
myBrain/
├── 0-Inbox/              # Quick capture, unsorted items
├── 1-Journal/            # Daily/weekly notes
│   ├── Daily/
│   └── Weekly/
├── 2-Knowledge/          # Permanent knowledge by domain
│   ├── 半导体/
│   ├── 编程技术/
│   ├── 商业思考/
│   ├── 副业探索/
│   └── 个人成长/
├── 3-Projects/           # Active projects
│   ├── RAG知识库产品/
│   ├── 内容工厂/
│   └── AI自动化服务/
├── 4-Tom-Memory/         # Chat-derived memory (Tom maintains)
│   ├── Chat-Insights/    # Key insights from conversations
│   ├── Decisions/        # Decisions we made together
│   ├── Learned/          # Facts Tom learned about Jerry
│   └── Skills-Index/     # Tom's capability inventory
├── 5-Archive/            # Completed/abandoned items
├── 6-MOCs/               # Maps of Content (index pages)
├── Templates/            # Note templates
└── Assets/               # Images, attachments
```

## Available sub-skills (kepano/obsidian-skills)

These are installed under `note-taking/` and extend Obsidian-specific capabilities:

| Sub-skill | Use when |
|-----------|----------|
| **obsidian-markdown** | Creating/editing notes with wikilinks, callouts, embeds, frontmatter, tags, footnotes, math, mermaid. Load this before writing any note. |
| **obsidian-bases** | Creating `.base` files for database-like views with filters, formulas, summaries. |
| **json-canvas** | Creating `.canvas` files for visual mind maps, flowcharts, project boards. |
| **obsidian-cli** | Interacting with a running Obsidian instance via CLI (requires Obsidian open). |
| **defuddle** | Extracting clean markdown from web pages before saving to vault. |

## ⚠️ Windows Path Encoding Pitfall

**On this Windows host, `read_file` and `write_file` tools fail with paths containing emoji (e.g., `🏠-Home.md`) or Chinese characters.** The tools pass paths through bash which mangles Unicode.

**Fallback: use `execute_code` with Python for ALL vault I/O on this host:**

```python
import os
vault = "C:/Users/jjdeng/Desktop/myBrain"

# Read a note
path = os.path.join(vault, "🏠-Home.md")
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Write a note
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# List notes in a directory
for f in os.listdir(os.path.join(vault, "4-Tom-Memory/Decisions")):
    print(f)
```

**When doing bulk vault operations (creating/updating many notes), batch all writes into a single `execute_code` call** — one Python script that writes every file. This is faster and avoids the encoding issues entirely.

`search_files` with `target: "files"` still works for listing files, but for reading their contents, fall back to `execute_code`.

## Read a note

**Primary method:** `execute_code` with Python `open()` (see pitfall above).

`read_file` works for ASCII-only paths (e.g., `4-Tom-Memory/Decisions/决策日志.md`) but fails on emoji paths. When in doubt, use Python.

## List notes

Use `search_files` with `target: "files"` and the vault path.

- List all markdown: `pattern: "*.md"` under vault path
- List a subfolder: search under the subfolder's absolute path

## Search

Use `search_files` for both filename and content searches.

- Filenames: `search_files` with `target: "files"` + filename `pattern`
- Contents: `search_files` with `target: "content"` + regex `pattern` + `file_glob: "*.md"`

## Create a note

**Primary method:** `execute_code` with Python `open()` (reliable on Windows). Batch all writes into one `execute_code` call when creating/updating many notes at once — one script that opens and writes every file.

`write_file` works for ASCII-only paths but fails on emoji paths. When in doubt, use Python.

**obsidian-markdown sub-skill:** For complex notes with wikilinks, callouts, or mermaid diagrams, load it before writing. For plain markdown notes (most project overviews, decisions, insights), the sub-skill is not required.

## Append to a note

- Read target with `read_file`
- Use `patch` for anchored append (e.g., adding section after heading)
- Use `write_file` when rewriting the whole note is simpler

## Templates

Templates live in `Templates/`:

| Template | For |
|----------|-----|
| `Daily.md` | Daily journal entry |
| `Chat-Insight.md` | Saving key insights from Hermes chat |
| `Decision.md` | Recording decisions made with Jerry |
| `Project.md` | New project overview |
| `Knowledge.md` | Permanent knowledge note |

To use a template, read the template file, fill in `{{placeholders}}`, then write to the target folder.

## Second Brain Workflow — When to Save to Vault

**After every significant conversation with Jerry**, save notes. File naming convention: `YYYY-MM-DD Topic.md` (topic = 3-8 Chinese chars about the main thread).

### Categories & what goes where

| Category | Path | When | Content shape |
|----------|------|------|---------------|
| **Chat Insights** | `4-Tom-Memory/Chat-Insights/` | Each session with Jerry | Session narrative: topics covered, key exchanges, independent discoveries. Use `Chat-Insight.md` template. |
| **Decisions** | `4-Tom-Memory/Decisions/` | Jerry made a clear strategic call | Context → options → decision → rationale. Use `Decision.md` template. |
| **Learned** | `4-Tom-Memory/Learned/` | New stable facts about Jerry (prefs, style, skills) | Concrete facts. Also save to `memory` tool. Obsidian = long-term record. |
| **Knowledge** | `2-Knowledge/` | Technical topics, business frameworks | Reusable frameworks. File under correct subfolder (半导体/编程技术/商业思考/副业探索/个人成长). Use `Knowledge.md` template. |
| **Project Updates** | `3-Projects/` | Progress on active projects | Milestones, blockers, decision logs. Update existing project note, don't create new one per session. |

### Skip rules

- **No Decisions this session** → skip Decisions folder. No empty placeholders.
- **No new facts about Jerry** → skip Learned.
- **Pure execution, no new frameworks** → skip Knowledge. Chat-Insights alone covers it.
- **Never write same fact to both Chat-Insights and Knowledge.** If it belongs in Knowledge, write it there only and link from Chat-Insights.

## Wikilinks

Use `[[Note Name]]` syntax. When creating notes, link to related content — this is how Obsidian builds the knowledge graph.

## Workflow rules (vault-resident)

The active workflow rules live in the vault at `4-Tom-Memory/工作流规则.md`. Read it to understand **what** gets saved and **when**. This SKILL.md covers HOW to operate on the vault; 工作流规则.md defines the trigger conditions and content categories.

## Quick Reference: Common Paths

| Purpose | Path |
|---------|------|
| Home note | `C:\Users\jjdeng\Desktop\myBrain\🏠-Home.md` |
| Today's daily | `C:\Users\jjdeng\Desktop\myBrain\1-Journal\Daily\YYYY-MM-DD.md` |
| Skills index | `C:\Users\jjdeng\Desktop\myBrain\4-Tom-Memory\Skills-Index\技能总览.md` |
| Decision log | `C:\Users\jjdeng\Desktop\myBrain\4-Tom-Memory\Decisions\决策日志.md` |
| 半导体 MOC | `C:\Users\jjdeng\Desktop\myBrain\6-MOCs\半导体知识地图.md` |
| 副业 MOC | `C:\Users\jjdeng\Desktop\myBrain\6-MOCs\副业地图.md` |
