# Tokscale Token Tracking Setup

Installed 2026-06-30 via shell script:
```bash
curl -fsSL https://raw.githubusercontent.com/xdevplatform/xurl/main/install.sh | bash
```

## What it does
Open-source CLI (Rust, 4K⭐) that reads local state.db from 25+ AI coding tools including Hermes Agent directly from `~/.hermes/state.db`. Shows token usage and estimated cost by model, by hour/day/month.

## Key commands

```bash
tokscale hourly --today --client hermes   # today's usage by hour
tokscale models                           # all-time model usage + cost
tokscale monthly                          # monthly breakdown
tokscale clients                          # scan detection status
tokscale tui                              # interactive TUI
```

## Cost accuracy
Tokscale calculates costs based on provider pricing it maps internally. For DeepSeek V4 Flash (Jerry's main model):
- Input (cache miss): $0.14/M
- Cache read: $0.0028/M  ← bulk of tokens
- Output: $0.28/M
- Total cost all-time (June 2026): ~$2.31

## Daily cron
`daily-token-report` (job `78bed683886a`): no_agent cron at 21:00 daily, script `daily-token-report.sh`, delivers cost summary to origin.
