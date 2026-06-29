# Wiki Schema

> Vault structure and writing conventions for Jerry's Second Brain
> Based on [minimal-second-brain](https://github.com/gokhanarkan/minimal-second-brain) model

## Domain

Hermes Agent 配置与自动化 / 一人公司 (OPC) / Loop Engineering

## Vault Structure

```
wiki/
├── Inbox/              # Quick captures, unprocessed ideas — process within 3 days
├── Knowledge/          # Permanent knowledge
│   ├── entities/       # One file per notable person/tool/platform
│   ├── concepts/       # One file per framework/methodology
│   ├── comparisons/    # Cross-tool/framework comparisons
│   ├── queries/        # Research questions + findings
│   └── raw/            # Source material (articles, transcripts, papers)
├── Projects/           # Active work items with goals and deadlines
├── Archive/            # Completed/inactive projects and knowledge
├── points/             # Session summaries by date (YYYY-MM-DD-title.md)
├── AGENTS.md           # AI agent vault rules (read this!)
├── MANIFEST.md         # Auto-generated: read first before scanning directories
├── index.md            # Human-readable content catalog (manual)
├── log.md              # Append-only action log
└── SCHEMA.md           # ← You are here
```

## AI Agent Workflow

Every AI agent that touches this vault MUST follow these steps:

1. **Read MANIFEST.md** — knows what exists without scanning every file
2. **Read AGENTS.md** — knows vault rules
3. **Navigate to directory → read its MANIFEST.md** — finds the specific file
4. **Read/edit files as needed**
5. **Run `python3 ~/.hermes/scripts/sync-manifests.py`** — regenerates manifests
6. **Update log.md** with a brief action record

## File Routing

| Content | Destination |
|---------|------------|
| Quick thought, process later | `Inbox/` |
| Active project/work | `Projects/` (move to Archive/ when done) |
| Reference, permanent knowledge | `Knowledge/` (entities/concepts/comparisons) |
| Session recording | `points/` |
| Completed/inactive | `Archive/` |

## Conventions

- File names: `lowercase-hyphens.md`, no spaces (except points/ which use `YYYY-MM-DD-title.md`)
- Every wiki page starts with YAML frontmatter
- Use `[[wikilinks]]` to cross-reference between pages
- Bump `updated:` date when editing existing page
- Run `sync-manifests.py` after every addition/deletion/rename

## Frontmatter

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [hermes, loop-engineering, opc, server, tool, skill]
---
```

## Tag Taxonomy

| Tag | Scope |
|-----|-------|
| **hermes** | 核心配置、技能、插件 |
| **loop-engineering** | Loop Engineering 相关 |
| **opc** | 一人公司架构 |
| **server** | 服务器配置、部署 |
| **tool** | 安装的工具（CloakBrowser, Lupin等） |
| **github** | GitHub 集成 |
| **memory** | 记忆管理 |
| **cron** | 定时任务 |
| **gateway** | 消息网关（QQ Bot, 飞书） |
| **proxy** | 代理配置 |
| **security** | 安全、护栏 |
| **content** | 内容创作相关 |
| **role** | 角色体系（五路并行） |
| **fitness** | 身体 / 健身 |
| **learning** | 学习相关 |

## Manifest System

Every directory (Inbox/, Knowledge/, Projects/, Archive/) has an auto-generated `MANIFEST.md` that lists all `.md` files with their titles and tags.

- **Root MANIFEST.md** — overview of all directories
- **Per-directory MANIFEST.md** — file-by-file listing with metadata
- **Generation script**: `python3 ~/.hermes/scripts/sync-manifests.py`
- **Auto-run on vault-backup cron** (every 6 hours)

## Page Thresholds

- **Create a page** when an entity/concept appears in 2+ sources
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions
- **Split a page** when it exceeds ~200 lines
