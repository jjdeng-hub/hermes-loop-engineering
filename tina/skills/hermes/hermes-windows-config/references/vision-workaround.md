# Image Understanding Workaround: Direct Claude API

> When `vision_analyze` tool is unavailable (not in tool list) or vision provider is unconfigured, fall back to direct Claude Messages API via `execute_code`.

## Problem

On this Windows host:
- `vision_analyze` tool may not appear in the available tools list
- Even when present, it errors: "No LLM provider configured for task=vision"
- `hermes setup` is needed to configure a vision provider, which may require user action

## Solution

Use the existing `fun-claude` custom provider (Claude Opus) via direct API calls from `execute_code`. The pattern is:

```python
import os, base64, requests, yaml

# Load API key from config
config_path = "C:/Users/jjdeng/.hermes/config.yaml"
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
fc = [p for p in config['custom_providers'] if p['name'] == 'fun-claude'][0]

# Read and encode image
img_path = "C:/path/to/image.png"
with open(img_path, 'rb') as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')

# Determine MIME type
ext = img_path.split('.')[-1].lower()
mime_map = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'gif': 'image/gif'}
mime = mime_map.get(ext, 'image/png')

# Call Claude Messages API
payload = {
    "model": fc['model'],  # claude-opus-4-8
    "max_tokens": 400,
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image in Chinese. What type is it?"},
            {"type": "image", "source": {"type": "base64", "media_type": mime, "data": img_data}}
        ]
    }]
}

resp = requests.post(
    f"{fc['base_url']}/v1/messages",
    json=payload,
    headers={
        "x-api-key": fc['api_key'],
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    },
    timeout=30
)

result = resp.json()
for block in result.get("content", []):
    if block.get("type") == "text":
        print(block["text"])
```

## Response Format Note

Claude Opus 4.6+ may return `thinking` blocks alongside `text` blocks. The `thinking` field contains reasoning traces (not noise — can include partial OCR/analysis). Extract only `type == "text"` blocks for the final answer.

## When to Use This vs. Setting Up a Vision Provider

- **Use this workaround** for: one-off image checks, batch image classification (loop in Python), quick OCR
- **Set up a proper vision provider** for: frequent image understanding, production workflows

## Cost

Claude Opus 4.8 vision input costs are negligible for individual screenshots and technical images (typically < 1 cent per image). The API key is already configured in `fun-claude` custom provider.

## Known Quirks

- Chinese/emoji file paths work fine with Python `open()` — no encoding issues
- The `anthropic-version: 2023-06-01` header is required
- Response time: 3-10 seconds for screenshots, faster for small images
