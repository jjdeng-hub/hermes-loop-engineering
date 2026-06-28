# Custom Provider Pitfall: Profile-Level Gateways

Discovered 2026-06-28 when deploying creator/fitness/learner profiles alongside default.

## The Problem

When a Hermes profile's `config.yaml` defines a custom provider under `providers.custom`, the profile's gateway does NOT resolve it at runtime. The error:

```
Primary provider auth failed: Unknown provider 'custom:sn-sensenova'.
```

or:

```
Primary provider auth failed: Unknown provider 'custom:apikey-fun'.
```

This happens even when `providers.custom` is correctly indented in the profile's `config.yaml`.

## Root Cause

Profile-level gateways load model configuration from the profile's `config.yaml` but do NOT load the `providers.custom` definitions from it. The gateway log confirms:
```
hermes_cli.config: providers.custom: unknown config keys ignored: <name>
```

Built-in providers (`deepseek`, `anthropic`, etc.) work fine because they are registered globally via `plugins/model-providers/<name>/__init__.py`, not per-profile.

## The Workaround: Use Built-in `custom` Provider

Hermes has a built-in `custom` provider (`plugins/model-providers/custom/`) designed for OpenAI-compatible endpoints. It reads `base_url` from the model config section and API key from `CUSTOM_API_KEY` (or `OPENAI_API_KEY` as fallback).

### In the profile's `config.yaml`:

```yaml
model:
  default: gpt-5.5            # your desired model
  provider: custom            # NOT "openai", NOT "custom:apikey-fun"
  base_url: https://api.apikey.fun/v1
```

### In the profile's `.env`:

```env
CUSTOM_API_KEY=sk-your-key-here
```

The `custom` provider falls back to `OPENAI_API_KEY` if `CUSTOM_API_KEY` is unset. `OPENAI_BASE_URL` is NOT read by this provider — the base URL must come from `config.yaml` model section.

## What Does NOT Work

| Attempt | Error | Why |
|---------|-------|-----|
| `provider: custom:apikey-fun` | Unknown provider `custom:apikey-fun` | Colon suffix not supported in profile config |
| `provider: openai` | Unknown provider `openai` | No `openai` registered provider in Hermes |
| `providers.custom` in config.yaml | `unknown config keys ignored` | Profile gateway ignores this section |

## What Works

| Approach | Result |
|----------|--------|
| `provider: deepseek` (built-in) + DEEPSEEK_API_KEY in .env | ✅ Works immediately |
| `provider: custom` + base_url in model config + CUSTOM_API_KEY in .env | ✅ Works for any OpenAI-compatible endpoint |
| `provider: anthropic` (built-in) + ANTHROPIC_API_KEY in .env | ✅ Works immediately |

## Key Detail: Key Writing Avoid `***` in execute_code

Keys written via `execute_code()` or `f`-strings with `***` may be corrupted (written as literal 8-char `Ellipsis`). Always write secrets via `terminal()` with a heredoc:

```bash
python3 << 'EOF'
# read key, write directly
with open('path/.env', 'w') as f:
    f.write(f'CUSTOM_API_KEY={actual_key}\n')
EOF
```

## Verification

After writing both files, restart the gateway from SSH/Web Console:

```bash
systemctl --user restart hermes-gateway-<profile-name>
```

Check the gateway log for the error:
```bash
tail -20 ~/.hermes/profiles/<profile>/logs/errors.log
```

A successful startup shows:
```
✓ feishu connected
```

No `Primary provider auth failed` in the log after a test message.

## Affected Configurations (from session 2026-06-28)

| Profile | Model | Original (broken) | Working |
|---------|-------|-------------------|---------|
| creator | gpt-5.5 | `provider: custom:apikey-fun` | `provider: custom` + base_url + CUSTOM_API_KEY |
| fitness | deepseek-v4-flash | `provider: custom:sn-sensenova` | `provider: custom` + base_url + CUSTOM_API_KEY |
| learner | deepseek-v4-flash | `provider: deepseek` | ✅ Always worked (built-in provider) |

The `default` profile was unaffected because its gateway resolves `providers.custom` from the main `~/.hermes/config.yaml`.
