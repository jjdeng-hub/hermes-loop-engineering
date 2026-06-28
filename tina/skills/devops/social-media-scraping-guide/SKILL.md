---
name: social-media-scraping-guide
description: Guide for scraping content from social media platforms (X/Twitter, Reddit, etc.) for tutorial/content library purposes. Covers methods, API options, and setup instructions.
---

# Social Media Content Scraping

## Overview

Guide for scraping content from social media platforms (X/Twitter, Reddit, etc.) for tutorial/content library purposes.

## Platform-Specific Challenges

### X/Twitter (Most Difficult)

| Method | Status | Reason |
|--------|--------|--------|
| `browser_navigate` | ❌ Timeout | Requires JS rendering + login state |
| Direct HTTP request | ❌ Timeout | Cloudflare protection blocks non-browser requests |
| Nitter mirrors | ❌ Offline | All public Nitter instances are down |
| Playwright | ⚠️ Works locally | Needs `playwright install chromium` |
| Camoufox | ⚠️ Works locally | Needs `camoufox fetch` |
| Firecrawl API | ✅ Works | Needs API key (free tier: 500/month) |
| Exa API | ✅ Works | Needs API key (free tier available) |
| Serper/Brave Search | ✅ Works | Needs API key (free tier available) |

### Reddit (Moderate)

| Method | Status | Notes |
|--------|--------|-------|
| Reddit API | ✅ Works | Register at https://www.reddit.com/prefs/apps |
| Pushshift | ⚠️ Limited | Rate limits, some endpoints deprecated |
| Nitter-style mirrors | ❌ Rare | Few working mirrors exist |

### Other Platforms

| Platform | Difficulty | Recommended Method |
|----------|------------|-------------------|
| Medium | 🟢 Easy | Direct HTTP + BeautifulSoup |
|知乎 | 🟡 Medium | Need cookies/session |
|掘金 | 🟢 Easy | Direct HTTP works |
|微信公众号 | 🟢 Easy | 搜狗搜索 + Playwright（已验证全套流程，含图片下载）。详见 `wechat-article-scraper` 技能。 |

## Setup for Local X/Twitter Scraping

### Option 1: Playwright (Recommended for local use)

```bash
# Install browser
playwright install chromium
```

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # WSL 需要 --no-sandbox
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page()
    # ⚠️ 用 domcontentloaded，不要用 networkidle（中国站点会挂起）
    page.goto("https://x.com/username/status/POST_ID",
              wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)  # 等 JS 渲染
    content = page.evaluate("() => document.body.innerText")
    browser.close()
```

### Option 2: Camoufox (Anti-detect browser)

```bash
# Install camoufox
camoufox fetch

# Then use in Python
from camoufox import Camoufox

with Camoufox(headless=True) as browser:
    page = browser.new_page()
    page.goto("https://x.com/username/status/POST_ID")
    content = page.evaluate("() => document.body.innerText")
```

### Option 3: Firecrawl API (Recommended for production)

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="your_api_key")
result = app.scrape_url(
    "https://x.com/username/status/POST_ID",
    params={'formats': ['markdown'], 'onlyMainContent': True}
)
print(result['markdown'])
```

**Free tier**: 500 credits/month at https://www.firecrawl.dev

### Option 4: Twitter API v2 Bearer Token (Best for cloud servers)

The simplest programmatic access to read tweets — no login session needed. Free tier: 500k tweets/month.

```python
import urllib.request, json, urllib.parse

token = urllib.parse.unquote("YOUR_BEARER_TOKEN")
tweet_id = "2070789303978840351"
url = f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=note_tweet,text"

req = urllib.request.Request(url)
req.add_header("Authorization", f"Bearer {token}")
resp = urllib.request.urlopen(req, timeout=15)
data = json.loads(resp.read())
```

**Pitfall**: The token from the developer portal often contains URL-encoded characters (`%2B`, `%3D`). Always `unquote()` it first. 401 errors are commonly caused by this, not by invalid tokens.

**Pitfall 2**: If 401 persists after decoding, the app may need a few minutes to propagate, or needs to be activated in developer portal settings.

**Full setup guide + troubleshooting**: `references/twitter-api-bearer-token.md`

### Option 5: Exa Search API

```python
from exa_py import Exa

exa = Exa(api_key="your_api_key")
result = exa.get_contents(
    ids=["https://x.com/username/status/POST_ID"],
    contents_kwargs={"text": True, "highlights": True}
)
```

**Free tier**: Available at https://exa.ai

## Environment Setup

Add API keys to environment:

```bash
export FIRECRAWL_API_KEY="your_key"
export EXA_API_KEY="your_key"
export SERPER_API_KEY="your_key"
```

## Alternative: Manual Collection

For low-volume use cases:

1. Open X/Twitter in browser
2. Use browser extension to copy content:
   - "Copyfish" (OCR for images)
   - "Web Scraper" (structured extraction)
   - "SingleFile" (save full page)
3. Paste into tutorial database

## Lessons Learned

1. **X/Twitter is intentionally hard to scrape** - Cloudflare + JS rendering + login wall
2. **Nitter is dead** - All public mirrors have shut down
3. **API services are the reliable path** - Firecrawl, Exa, Serper all work
4. **Local browser automation works** - Playwright/Camoufox but requires setup
5. **Check API key availability first** - Don't waste time on methods that need keys you don't have

### 2026-05-07 实战经验总结

**环境检查结果**（当前 WSL 环境）：

| 方法 | 状态 | 原因 |
|------|------|------|
| Playwright | ❌ 未安装浏览器 | 需要运行 `playwright install chromium` |
| Camoufox | ❌ 未初始化 | 需要运行 `camoufox fetch` |
| Firecrawl API | ❌ 无 API Key | 需注册 https://www.firecrawl.dev |
| Exa API | ❌ 无 API Key | 需注册 https://exa.ai |
| Serper API | ❌ 无 API Key | 需注册 https://serper.dev |
| Brave Search | ❌ 无 API Key | 需注册 https://brave.com/search/api |

**结论**：当前环境无可用 X 爬取方案，建议：
1. 手动复制内容到教程库（短期）
2. 注册 Firecrawl 免费账户获取 API Key（中期）
3. 关注作者在其他平台的发布（Medium、知乎等，更容易爬取）

**推荐替代平台**：

| 平台 | 爬取难度 | 推荐方法 |
|------|----------|----------|
| Medium | 🟢 简单 | 直接 HTTP + BeautifulSoup |
| 知乎 | 🟡 中等 | 需要 cookies/session |
| 掘金 | 🟢 简单 | 直接 HTTP 工作 |
| 微信公众号 | 🟡 中等 | 使用 `wechat-article-scraper` skill |

## Quick Diagnostic Script

```python
import os

def check_scraping_options():
    """Check which scraping methods are available"""
    options = {
        "Playwright (chromium)": "playwright install chromium",
        "Camoufox": "camoufox fetch",
        "Firecrawl API": "FIRECRAWL_API_KEY",
        "Exa API": "EXA_API_KEY",
        "Serper API": "SERPER_API_KEY",
        "Brave Search API": "BRAVE_SEARCH_API_KEY",
    }
    
    print("Available scraping options:")
    for name, check in options.items():
        if check.startswith("export ") or check.startswith("playwright") or check.startswith("camoufox"):
            # Check if command exists or env var is set
            import subprocess
            result = subprocess.run(["which", check.split()[0]], capture_output=True)
            is_available = result.returncode == 0
        else:
            is_available = bool(os.environ.get(check))
        
        status = "✅" if is_available else "❌"
        print(f"  {status} {name}")

check_scraping_options()
```