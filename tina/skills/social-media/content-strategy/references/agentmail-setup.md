# AgentMail Setup Reference

## Quick Config

Add to `~/.hermes/config.yaml`:
```yaml
mcp_servers:
  agentmail:
    command: "npx"
    args: ["-y", "agentmail-mcp"]
    env:
      AGENTMAIL_API_KEY: "am_us_..."
```

Requires Node.js 18+ (pre-installed on this server).

## Known Credentials

- Email: hermes-tom-jerry@agentmail.to
- API key format: `am_us_<hex>` (starts with `am_us_`)

## Verification

```python
from hermes_tools import terminal
# Check inboxes with: mcp_agentmail_list_inboxes
# Check threads with: mcp_agentmail_list_threads(inboxId="hermes-tom-jerry@agentmail.to")
```

## Free Tier Limits

- 3 inboxes
- 3,000 emails/month
- @agentmail.to domain only
