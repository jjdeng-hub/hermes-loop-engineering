# WeChat Official Account Article Harvesting

> Technique discovered 2026-06-16 while building a RAG knowledge base from the "Kns焊线机入门指南" account.
> Result: 141 articles, 750 images, ~400KB text harvested in one afternoon.

## Key Discovery: No Playwright Needed for Single Articles

Contrary to `wechat-official-account-scraper` (which uses Playwright for Sogou search), **direct article URLs can be fetched with plain Python `requests`**:

```python
import requests
url = "https://mp.weixin.qq.com/s/2vS8j8fI2_eiyONkdJCp8A"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
resp = requests.get(url, headers=headers, timeout=30)
# resp.status_code → 200
# resp.text → full HTML with article content in #js_content div
```

Playwright is only needed for **Sogou search** (to follow encrypted redirects). If you have direct `mp.weixin.qq.com/s/...` URLs, use `requests` directly.

## Extracting Article Content

```python
import re
from datetime import datetime

html = resp.text

# Title
title_match = re.search(r'var msg_title\s*=\s*["\'](.*?)["\']', html)
title = title_match.group(1) if title_match else "Unknown"

# Publication time
ct_match = re.search(r'var ct\s*=\s*["\']?(\d+)["\']?', html)
pub_time = datetime.fromtimestamp(int(ct_match.group(1))).strftime('%Y-%m-%d') if ct_match else ""

# Nickname (公众号名称)
nick_match = re.search(r'var nickname\s*=\s*["\'](.*?)["\']', html)
source = nick_match.group(1) if nick_match else "Unknown"

# Body text (strip HTML)
body_match = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.DOTALL)
if body_match:
    text = re.sub(r'<[^>]+>', '', body_match.group(1))
    text = re.sub(r'\s+', ' ', text).strip()
```

## Image Download (Bypassing Anti-Hotlinking)

WeChat images on `mmbiz.qpic.cn` require the article URL as `Referer`:

```python
img_url = "https://mmbiz.qpic.cn/..."  # from data-src attribute
img_headers = {
    "User-Agent": headers["User-Agent"],
    "Referer": article_url,  # ← THIS is the key
}
img_resp = requests.get(img_url, headers=img_headers, timeout=20)
```

## Identifying and Removing Promotional Images

68KB GIF with identical MD5 hash `b156eaf6ef9c...` appearing as:
- Last image in 45 articles (引导点赞图)
- First image in 16 articles (封面图)

```python
import hashlib
from collections import Counter

for img in images:
    with open(img_path, "rb") as f:
        h = hashlib.md5(f.read()).hexdigest()
    hash_counter[h] += 1

# Remove images whose hash appears in 3+ articles
common = {h for h, count in hash_counter.items() if count >= 3}
```

## Boilerplate Text Patterns (Remove from Every Article)

```
Pattern 1: 特别声明：本公众号发布内容除原创文字和图片外...
Pattern 2: 本公众号发布之见解均为个人思考之结果仅作建议...
Pattern 3: 所有文章欢迎署名转载
Pattern 4: KS焊线机技术进阶热门内容快速导读：...
```

## Output Format for RAG

Best format is **Markdown with embedded local image references**:

```markdown
# Title

**Source:** 公众号名称
**Published:** 2026-04-28
**Link:** https://mp.weixin.qq.com/s/...

Body text paragraph...

![alt text](article-title-folder/img_001.jpg)

Next paragraph...
```

### Image Embedding Algorithm

Re-fetch the article HTML, split the `#js_content` inner HTML by `<img>` tags.
Text chunks → strip HTML, keep text. Image chunks → replace with local path (mapped by index order).

### Directory Structure

```
rag-data/
├── Article-Title.md        ← Markdown with embedded images
├── Article-Title.txt       ← Plain text for RAG indexing
├── Article-Title/          ← Image folder
│   ├── img_001.jpg
│   └── ...
```
