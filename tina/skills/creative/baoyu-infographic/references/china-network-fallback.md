# Chinese Network Image Generation Fallback

When `image_generate` is unavailable (no Hermes Web UI, or provider unreachable in China), use Python with a Chinese image-generation API directly.

## Verified Providers

| Provider | Models | Free Tier | Endpoint |
|----------|--------|-----------|----------|
| SiliconFlow | Tongyi-Z-Image-Turbo, Qwen-Image, Kolors | 14 RMB welcome credit | `https://api.siliconflow.cn/v1/images/generations` |

## Python Integration Pattern

```python
import urllib.request, json, os

def generate_image(prompt, output_path, model="Tongyi-MAI/Z-Image-Turbo", size="1024x1024", api_key=None):
    """Generate an image via SiliconFlow API and save to local path."""
    if api_key is None:
        api_key = API_KEY  # define or pass in
    
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size
    }).encode()
    
    req = urllib.request.Request(
        "https://api.siliconflow.cn/v1/images/generations",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    
    with urllib.request.urlopen(req, timeout=90) as resp:
        result = json.loads(resp.read().decode())
    
    # SiliconFlow returns {"images": [{"url": "..."}]}
    img_url = result["images"][0]["url"]
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    urllib.request.urlretrieve(img_url, output_path)
    return output_path
```

## Model Selection Guide for Chinese APIs

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| `Tongyi-MAI/Z-Image-Turbo` | Fast (~10s) | Good | Quick tests, batch generation |
| `Qwen/Qwen-Image` | Medium | Best | High-quality outputs |
| `Kwai-Kolors/Kolors` | Medium | Good | Artistic styles |

## Prompt Adaptation

Chinese models (Qwen-Image, Z-Image-Turbo) work best with:
- **Detailed Chinese descriptions** — be explicit about layout, style, colors, labels
- **Simpler compositions** — they handle text-in-image less reliably than Flux/SD
- **Avoid English-only prompts** — write the image text labels in the target language
- **Explicit style keywords** — "手绘卡通风格", "信息图风格", "现代简约", "奶油色背景"

## Size Support

Not all models support all sizes. Stick to these:
- `1024x1024` — safest, all models support it
- `1536x1024` — 3:2, some models support it
- `1024x1536` — 2:3, some models support it

When in doubt, use `1024x1024` and crop later.

## Known Issues

- **Z-Image-Turbo** sometimes ignores text labels in prompts — use simpler text or add explicit "清晰标注文字在图中" instructions
- **Free quota runs out** — SiliconFlow free credits are typically 14 RMB (~140 images at 0.1 RMB each). Monitor with `GET /v1/user/info`.
- **API keys may be short-lived** — SiliconFlow trial keys can expire. If getting 401, tell the user to regenerate the key on cloud.siliconflow.cn.
- **No `write_file` fallback** — on Windows Hermes Desktop with space-in-path issues, `write_file` may fail. Always use `execute_code` with Python `open()` to save the image path reference.
