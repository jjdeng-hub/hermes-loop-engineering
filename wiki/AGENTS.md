# AGENTS.md — Vault Agent Instructions

> Universal rules for ANY AI agent working in this vault.
> Last updated: 2026-06-29

## Vault Structure

```
wiki/
├── Inbox/              # Quick captures, unprocessed ideas
│   └── MANIFEST.md
├── Knowledge/          # Permanent knowledge
│   ├── entities/       # One file per notable person/tool/platform
│   ├── concepts/       # One file per framework/methodology
│   ├── comparisons/    # Cross-tool/framework comparisons
│   ├── queries/        # Research questions and findings
│   ├── raw/            # Source material (articles, transcripts)
│   └── MANIFEST.md
├── Projects/           # Active work items
│   └── MANIFEST.md
├── Archive/            # Completed/inactive items
│   └── MANIFEST.md
├── points/             # Session summaries by date
├── AGENTS.md           # ← You are here
├── MANIFEST.md         # Root index (read first!)
├── index.md            # Human-readable catalog
├── log.md              # Append-only action log
└── SCHEMA.md           # Full schema reference
```

## Cardinal Rules

### ALWAYS
1. **Read MANIFEST.md first** — Before searching or scanning any directory, read its MANIFEST.md. It tells you what's in there without scanning every file.
2. **Run sync-manifests.py after changes** — After adding, removing, or renaming any file, run `python3 ~/.hermes/scripts/sync-manifests.py` to regenerate MANIFEST files.
3. **Use [[wikilinks]]** — Link related notes using `[[Note Name]]`. This builds the knowledge graph.
4. **Update log.md** — Append every significant action to log.md with `## [YYYY-MM-DD] action | subject`.

### ASK FIRST
- Before deleting files
- Before major reorganisation

### NEVER
- Create files at vault root (put them in the right directory)
- Commit without a clear message
- Write to two files with the same information

## File Routing

| Content goes to | Directory |
|----------------|-----------|
| Raw idea, process later | `Inbox/` |
| Active project/work | `Projects/` |
| Reference, permanent knowledge | `Knowledge/` |
| Completed project | `Archive/` |
| Session recording | `points/` |

## File Naming

| Type | Format | Example |
|------|--------|---------|
| Knowledge file | `lowercase-hyphens.md` | `loop-engineering.md` |
| Session note | `YYYY-MM-DD-title.md` | `2026-06-29-五路并行角色体系搭建.md` |
| Entity | `entity-name.md` | `hermes-config.md` |
| Concept | `concept-name.md` | `memory-architecture.md` |

## Frontmatter (every file)

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [tag1, tag2]
---
```

## This Vault Serves All Roles

This vault is the shared second brain for Jerry's entire AI role system:
- **Tom** — writes session notes, maintains Knowledge
- **Tina** — saves philosophical insights from conversations
- **Maker** — records execution workflows and action plans
