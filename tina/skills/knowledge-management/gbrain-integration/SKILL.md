---
name: gbrain-integration
category: knowledge-management
description: Guide for integrating GBrain knowledge brain system with Hermes Agent
created: 2026-05-05
---

# GBrain Integration Skill

## Overview

**GBrain** (https://github.com/garrytan/gbrain) is a comprehensive personal knowledge brain system by the same developer as GStack. It's NOT a Hermes skill — it's a standalone CLI tool + MCP server that provides:

- Hybrid RAG search (keyword + vector)
- Knowledge graph with typed links
- Multi-brain/multi-source architecture
- Live sync from markdown repos
- MCP server for AI agent integration
- Security: RLS, OAuth 2.1, access tokens

**Version:** v0.26.8 (as of 2026-05-04)

## Installation

```bash
# Clone and install
git clone https://github.com/garrytan/gbrain.git ~/gbrain
cd ~/gbrain
curl -fsSL https://bun.sh/install | bash
export PATH="$HOME/.bun/bin:$PATH"
bun install && bun link

# Verify
gbrain --version

# API keys (required for vector search)
export OPENAI_API_KEY=your_key
export ANTHROPIC_API_KEY=optional_key
```

⚠️ **Important:** Do NOT use `bun install -g github:garrytan/gbrain` — global install blocks postinstall hooks, schema migrations won't run.

## Core Concepts

### Brains (DB axis)
- A brain is a database (PGLite file, Postgres, or Supabase)
- Each brain has its own pages, chunks, embeddings tables
- Multiple brains can be mounted for team collaboration

### Sources (repo axis)
- A source is a named content repo inside a brain
- One brain can hold multiple sources (e.g., wiki, gstack, openclaw)
- Slugs are unique per source, not globally

### Routing Precedence

```
WHICH BRAIN?                    WHICH SOURCE?
1. --brain <id>                 1. --source <id>
2. GBRAIN_BRAIN_ID env          2. GBRAIN_SOURCE env
3. .gbrain-mount dotfile        3. .gbrain-source dotfile
4. longest-prefix mount path    4. longest-prefix source path
5. fallback: 'host'             5. fallback: 'default'
```

## Basic Usage

### Initialize a brain
```bash
gbrain init                           # PGLite (zero-config)
gbrain doctor --json                  # Verify all checks pass
```

### Import and index
```bash
gbrain import ~/brain/ --no-embed     # Import markdown files
gbrain embed --stale                  # Generate vector embeddings
gbrain query "key themes across these documents?"
```

### Live sync (keep index current)
```bash
gbrain sync --repo /path/to/brain && gbrain embed --stale
gbrain sync --watch --repo /path/to/brain --interval 60
```

### Query and search
```bash
gbrain query "what did we decide about X?"
gbrain search "caching strategies"
gbrain graph-query <slug> --depth 2   # Relationship traversal
```

## MCP Server Integration with Hermes

### Local stdio (zero setup)
```bash
gbrain serve
```
Works with Claude Code, Cursor, Windsurf, and any MCP client.

### Remote over HTTP (v0.26.0+)
```bash
gbrain serve --http --port 3131
ngrok http 3131 --url your-brain.ngrok.app
gbrain serve --http --port 3131 --public-url https://your-brain.ngrok.app
```

### Token management
```bash
gbrain auth create "hermes-client"
gbrain auth list
gbrain auth revoke "hermes-client"
```

### Security notes
- **Never use open OAuth client registration** — attackers can register clients and access all brain data
- Use `gbrain serve --http` with managed tokens, or require secrets for registration
- RLS must be enabled on all public tables (v0.26.8 auto-enforces via DDL trigger)

## GBrain Skills (available in ~/.hermes/gbrain/skills/)

| Skill | Description |
|-------|-------------|
| ingest | Route content to specialized ingestion skills |
| query | Answer questions using 3-layer search + synthesis |
| maintain | Brain health checks: back-links, citations, stale info |
| enrich | Enrich pages with tiered protocol, templates |
| briefing | Compile daily briefing with meeting context |
| migrate | Universal migration from Obsidian, Notion, Logseq, etc. |
| setup | Set up GBrain: auto-provision Supabase/PGLite |
| publish | Share brain pages as password-protected HTML |
| signal-detector | Ambient signal capture on every message |
| brain-ops | Core read/write cycle with source attribution |

## Recommended Schema

Follow `docs/GBRAIN_RECOMMENDED_SCHEMA.md` for MECE directory structure:
- `people/` — Person pages
- `companies/` — Company pages
- `deals/` — Deal pages
- `meetings/` — Meeting notes
- `projects/` — Project pages
- `concepts/` — Concept pages
- `inbox/` — Unfiled items (signals schema needs to evolve)

Each directory has a `README.md` resolver explaining what goes there.

## Evals & Benchmarks

```bash
# Capture queries for eval
export GBRAIN_CONTRIBUTOR_MODE=1

# Export baseline
gbrain eval export --since 7d > baseline.ndjson

# Replay against baseline
gbrain eval replay --against baseline.ndjson
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `gbrain` not found | Restart shell or add `~/.bun/bin` to PATH |
| Sync shows 0 pages | Use Session mode pooler (port 6543), not Transaction mode |
| Doctor fails RLS check | Run `ALTER TABLE public.<name> ENABLE ROW LEVEL SECURITY` |
| PGLite works, Postgres fails | Check pooler mode — Transaction mode breaks `engine.transaction()` |

## Relationship to Hermes

GBrain is a **complementary system**, not a replacement:
- **Hermes** = AI agent platform (skills, terminal, browser, memory)
- **GBrain** = Personal knowledge brain (RAG, knowledge graph, sync)

Integration options:
1. **MCP client** — Hermes can connect to GBrain MCP server as a tool
2. **Shared memory** — Store GBrain query results in Hermes memory files
3. **Skill wrapper** — Create a Hermes skill that calls `gbrain query`

For the user's sub-business goals, GBrain could be valuable for:
- Building a knowledge base for AI tool tutorials
- Tracking customer interactions and feedback
- Organizing product documentation
- Multi-team collaboration (mount team brains)

## Resources

- Repo: https://github.com/garrytan/gbrain
- Docs: `~/.hermes/gbrain/docs/`
- Architecture: `docs/architecture/brains-and-sources.md`
- Security: `SECURITY.md`, `docs/guides/rls-and-you.md`
- MCP Deploy: `docs/mcp/DEPLOY.md`
- Live Sync: `docs/guides/live-sync.md`
- Eval Benchmarks: `docs/eval-bench.md`