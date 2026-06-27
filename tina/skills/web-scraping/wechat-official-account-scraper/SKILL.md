---
name: wechat-official-account-scraper
description: 微信公众号文章爬取方案 - 搜狗搜索 + Playwright 绕过反爬
version: 1.0.0
created: 2026-05-06
tags: [scraping, wechat, playwright, python]
---

# WeChat Official Account Scraper

## Overview

爬取微信公众号文章的技术方案。**两个模式**：

| 模式 | 适用场景 | 所需工具 |
|------|---------|---------|
| **直接抓取** | 用户提供直接 mp.weixin.qq.com/s/... 链接 | 仅 `requests` |
| **搜狗搜索+Playwright** | 未知文章列表，需搜索发现 | Playwright + Chromium |

**核心发现**：`mp.weixin.qq.com/s/...` 直接链接可以直接用 `requests.get()` 抓取，不需要 Playwright。Playwright 仅用于跟随搜狗的加密重定向链接。

## Architecture

```
模式A（直接链接，推荐）：
  用户提供 mp.weixin.qq.com/s/XXX → requests.get() → 正则提取 → 保存

模式B（搜狗搜索）：
  搜狗微信搜索 → 获取加密链接 → Playwright 访问 → 重定向到真实文章 → 提取内容
```

## Quick Start

### 模式A：直接抓取（用户提供链接时）

最简单的模式，仅需 `requests`，无需额外安装。

```python
import requests, re
from datetime import datetime

def crawl_wechat_direct(url):
    """直接抓取 mp.weixin.qq.com/s/... 文章，无需 Playwright"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    }
    resp = requests.get(url, headers=headers, timeout=30)
    html = resp.text
    
    # 提取标题
    title_match = re.search(r'var msg_title\s*=\s*["\'](.*?)["\']', html)
    if not title_match:
        title_match = re.search(r'<title>(.*?)</title>', html)
    title = re.sub(r'<[^>]+>', '', title_match.group(1).strip()) if title_match else "未知标题"
    
    # 提取公众号名称
    nickname_match = re.search(r'var nickname\s*=\s*["\'](.*?)["\']', html)
    source = nickname_match.group(1) if nickname_match else "未知来源"
    
    # 提取发布时间（Unix timestamp）
    time_match = re.search(r'var ct\s*=\s*["\']?(\d+)["\']?', html)
    pub_time = datetime.fromtimestamp(int(time_match.group(1))).strftime('%Y-%m-%d %H:%M:%S') if time_match else ""
    
    # 提取正文HTML
    content_match = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.DOTALL)
    content_html = content_match.group(1) if content_match else ""
    
    # 提取+下载图片（Referer绕过防盗链，MD5去重模板图）
    img_urls = re.findall(r'<img[^>]*data-src="([^"]+)"[^>]*>', content_html)
    img_map = {}; seen_hashes = set()
    for idx, img_url in enumerate(img_urls[:50]):
        ih = headers.copy(); ih["Referer"] = url
        r = requests.get(img_url, headers=ih, timeout=10)
        if r.status_code == 200:
            h = hashlib.md5(r.content).hexdigest()
            if h in seen_hashes: continue
            seen_hashes.add(h)
            ext = 'png' if 'png' in r.headers.get('Content-Type','') else 'jpg'
            fname = f"img_{idx+1:03d}.{ext}"
            with open(os.path.join(img_dir, fname), 'wb') as f:
                f.write(r.content)
            img_map[img_url] = fname
    
    # v2: html_to_markdown() 保留图片位置，详见 references/markdown-conversion-v2.md
    md_body = html_to_markdown(content_html, img_map)
    
    # 清理微信模板文字
    for pat in [r'扫描二维码.*?关注', r'长按识别.*?关注']:
        md_body = re.sub(pat, '', md_body, flags=re.DOTALL)
    
    # 保存 Markdown（图片在正确位置）
    md_path = os.path.join(os.path.dirname(output_dir), safe_title, "article.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n> 来源：{source} | 时间：{pub_time}\n> 原文：{url}\n\n---\n\n{md_body}")
    
    # 保存 TXT（RAG用，去图片标记）
    txt_body = re.sub(r'!\[.*?\]\(.*?\)', '', md_body)
    txt_path = os.path.join(output_dir, f"{safe_title}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"标题：{title}\n来源：{source}\n时间：{pub_time}\n链接：{url}\n\n{txt_body}")
    
    return {"title": title, "source": source, "time": pub_time, "chars": len(txt_body), "imgs": len(img_map)}
```

提取的 HTML 选择器（与 Playwright 方案共享）：

| 字段 | CSS/JS 变量 | 正则 |
|------|-------------|------|
| 标题 | `var msg_title = "..."` | `r'var msg_title\s*=\s*["\'](.*?)["\']'` |
| 公众号 | `var nickname = "..."` | `r'var nickname\s*=\s*["\'](.*?)["\']'` |
| 发布时间 | `var ct = "unix_ts"` | `r'var ct\s*=\s*["\']?(\d+)["\']?'` |
| 正文 | `<div id="js_content">` | `<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script` |
| 图片 | `data-src` 属性 | `r'data-src="https?://[^"]+"'` |

> **优势**：零依赖、极快（单篇 1-2s）、可批量并行大规模爬取（已验证 141 篇 / 60 分钟）。  
> **图片下载**：直接用 `requests` + `Referer` header 即可成功下载微信图片——实测 750 张图 100% 成功率，无需 Playwright。详见 `references/image-download.md` 中的"直接 requests + Referer"方案。

### 模式B：搜狗搜索 + Playwright

### 1. 安装依赖

```bash
uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple playwright
# Chromium 如果下载慢，可复用已缓存的旧版本（见 Pitfalls）
```

### 2. 运行爬取

```bash
# 关键词搜索文章
python3 wechat_full_crawl.py 人工智能

# 爬取指定文章（第 2 篇）
python3 wechat_full_crawl.py 人工智能 1

# 爬取特定公众号的全部文章（推荐）
python3 -u crawl_account.py "KS焊线机技术进阶之路"
```

### 3. 搜狗 URL 参数说明

| 参数 | 含义 | 示例 |
|------|------|------|
| `type=2` | 搜索文章 | `?type=2&query=公众号名` |
| `type=1` | 搜索公众号 | `?type=1&query=公众号名` |
| `page=N` | 翻页 | `&page=2` |

**按公众号搜索全部文章**：直接用 `type=2&query=公众号名`，然后在结果中按 `source` 字段过滤即可。

## Key Technical Findings

### 搜狗微信搜索

| 问题 | 解决方案 |
|------|----------|
| 直接 requests 请求成功 | ✅ 可获取搜索结果 HTML |
| 返回加密中间链接 | `/link?url=<编码>&type=2&query=...` |
| 直接访问加密链接被反爬 | ❌ 重定向到 antispider 页面 |
| Playwright 访问可绕过 | ✅ 成功获取真实微信链接 |

### 反爬绕过技巧

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    context = p.chromium.launch_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
        viewport={"width": 1920, "height": 1080}
    )
    
    # 添加防检测脚本
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        window.chrome = {runtime: {}};
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh']});
    """)
    
    page = context.new_page()
    page.goto("https://weixin.sogou.com/weixin?type=2&query=人工智能")
```

### 文章链接流程

```
1. 搜狗搜索返回：https://weixin.sogou.com/link?url=<加密URL>
2. Playwright 访问该链接
3. 服务器重定向到：https://mp.weixin.qq.com/s?src=11&timestamp=...&signature=...
4. 提取文章内容
```

## HTML Selectors

### 搜狗搜索结果页

```css
/* 文章列表项 */
//ul[@class="news-list"]//li

/* 标题 */
h3 a

/* 公众号名称 */
span.all-time-y2

/* 发布时间（JavaScript 渲染） */
span.s2  /* 内容格式：timeConvert('1778022702') */
```

### 微信公众号文章页

```css
/* 文章标题 */
//h1[@id="activity-name"]

/* 公众号名称 */
//a[@class="rich_media_meta_nickname"]

/* 发布时间 */
//div[@class="rich_media_meta_text"]

/* 正文内容 */
//div[@id="js_content"]

/* 图片 */
//div[@id="js_content"]//img/@data-src
```

## Output Format

### JSON 结构

```json
{
  "title": "文章标题",
  "source": "公众号名称",
  "pub_time": "发布时间",
  "url": "真实文章链接",
  "content_text": "正文文本（前 5000 字符）",
  "content_html": "正文 HTML（前 10000 字符）",
  "images": ["图片 URL 列表"],
  "search_query": "搜索关键词",
  "search_index": 0,
  "crawl_time": "2026-05-06T02:36:30"
}
```

### 批量输出目录结构（大规模爬取模式）

当批量爬取多篇文章时，推荐每篇文章一个文件夹 + 同级 .txt 文件的布局，便于后续 RAG 索引和人工查阅：

```
output_dir/
├── 文章标题1.txt               # 纯文本文件：标题+来源+时间+链接+正文
├── 文章标题1/                   # 同名文件夹：该文章的配图
│   ├── img_001.jpg
│   ├── img_002.png
│   └── ...
├── 文章标题2.txt
├── 文章标题2/
│   ├── img_001.jpg
│   └── ...
├── _article_list.json          # 所有文章元数据（可选）
└── _knowledge_base_summary.json # 知识库汇总统计（可选）
```

这种布局的好处：
- `.txt` 文件可直接被 RAG 系统索引（ChromaDB 支持按文件批量导入）
- 图文字分离，RAG 仅需文本，图片保留用于人工查阅
- 每篇文章独立文件夹，不会互相干扰

```markdown
# 文章标题

> 来源：公众号名称 | 时间：2026-05-06
> 原文：https://mp.weixin.qq.com/s?...
>
> ---

正文内容...

![](img_001.png)    ← 图片在原文位置

继续正文...

---

*爬取时间：2026-05-06 08:47:44*
```

> **v2 改进**：图片不再堆在末尾，嵌入原文HTML中 `<img>` 标签的原位置。详见 `references/markdown-conversion-v2.md`。

## Limitations

| 限制 | 说明 |
|------|------|
| ⚠️ **不要过度工程化** | 用户给直接 URL 时，用 `requests` 即可——**不要装 Playwright + Chromium**。本 session 验证：Playwright 仅用于搜狗搜索的加密链接重定向，直接 URL 完全不需要。 |
| **内容完整性** | 部分图片/样式可能丢失 |
| **登录态需求** | 部分公众号文章需要登录才能查看 |
| **法律合规** | 仅用于学习研究，商业使用需授权 |

## Integration with Matrix

可整合到 Matrix 视频矩阵项目中，实现：

1. **内容源**：自动爬取热点文章
2. **素材收集**：建立行业文章知识库
3. **竞品分析**：监控特定公众号内容策略
4. **发布闭环**：爬取 → 改写 → 多平台发布

## Files

```
skills/web-scraping/wechat-official-account-scraper/
├── SKILL.md
├── references/
│   └── image-download.md        # 🆕 图片下载绕过防盗链完整方案
├── scripts/
│   ├── wechat_scraper.py
│   ├── wechat_full_crawl.py
│   ├── crawl_account.py
│   └── decode_sogou_link.py
├── assets/
│   └── sogou_search.png
```

实际项目文件（matrix）:
```
/home/jjdeng/.hermes/projects/matrix/
├── wechat_full_crawl.py
├── wechat_scraper.py
├── wechat_articles/          # 输出目录
│   ├── *.json / *.md / *.png
```

RAG 知识库导入:
```
~/rag-agent/
├── crawl_ks_account.py       # 公众号爬取脚本
└── data/                     # 爬取结果自动索引
    └── KS_*.txt              # 每篇文章一个文件
```

## Pitfalls (踩过的坑)

### ⚠️ `wait_until="networkidle"` 在境内网站卡死

**现象**：`page.goto(url, wait_until="networkidle")` 永远不返回，60 秒+ 无响应。

**原因**：国内网站加载了大量被墙的第三方脚本（Google Analytics、Facebook SDK 等），`networkidle` 要求所有网络请求在 500ms 内无新请求才算完成，被墙的脚本永远 pending，导致死等。

**解决**：所有国内网站（搜狗、微信文章页）必须使用 `wait_until="domcontentloaded"`，然后手动 `wait_for_timeout(3000)` 等待 JS 渲染。

```python
# ❌ 错误 — 国内网站会卡死
page.goto(url, wait_until="networkidle", timeout=20000)

# ✅ 正确
page.goto(url, wait_until="domcontentloaded", timeout=20000)
page.wait_for_timeout(3000)
```

### ⚠️ WSL 必须 `--no-sandbox`

**现象**：`chromium.launch()` 报错或无响应退出。

**原因**：WSL 没有完整的 Linux 命名空间支持，Chrome 的沙箱机制无法工作。

**解决**：启动参数加 `--no-sandbox`。

```python
browser = p.chromium.launch(
    headless=True,
    executable_path=CHROMIUM_PATH,
    args=["--no-sandbox"],
)
```

### ⚠️ Playwright 版本与 Chromium 版本不匹配

**现象**：`playwright install chromium` 下载慢 >5 分钟（国内网络问题），或 `BrowserType.launch: Executable doesn't exist at .../chromium_headless_shell-1223/...`。

**原因**：`uv pip install playwright` 装了最新 Python 包，但对应的 Chromium 浏览器没下载完或下载失败。

**解决**：复用已缓存的旧版 Chromium，通过 `executable_path` 显式指定路径，版本差异通常可兼容。

```python
import os, glob

def find_cached_chromium():
    """自动查找已缓存的 Chromium 二进制（跨平台）"""
    # Windows cache paths
    win_paths = [
        os.path.expanduser("~/AppData/Local/ms-playwright"),
        os.path.expanduser("~/Documents/Codex/playwright-browsers "),
    ]
    # Linux/WSL cache paths
    lin_paths = [
        os.path.expanduser("~/.cache/ms-playwright"),
    ]
    
    for cache in win_paths + lin_paths:
        if os.path.isdir(cache):
            for d in sorted(os.listdir(cache), reverse=True):
                d_path = os.path.join(cache, d)
                if not os.path.isdir(d_path):
                    continue
                # Try all platform binary locations
                for pattern in [
                    "chrome-win/chrome.exe",
                    "chrome-win64/chrome.exe",
                    "chrome-linux64/chrome",
                    "chrome-linux/chrome",
                    "chromium-*/chrome.exe",
                    "chromium-*/chrome",
                ]:
                    matches = glob.glob(os.path.join(d_path, pattern))
                    if matches:
                        return matches[0]
    return None
```

### ⚠️ 后台进程输出被缓冲

**现象**：`terminal(background=True)` 后 `process(action='log')` 无输出。

**解决**：Python 脚本加 `-u` 参数关闭输出缓冲：`python3 -u script.py`。

## Windows Deployment（Agent Terminal 不可用时）

当 Hermes Agent 在 Windows 上的 bash terminal 因路径空格等问题不可用时，传统的工作流（agent 写脚本 + agent 跑命令）失效。以下是经过验证的替代方案：

### 工作流：Agent 写脚本 + 用户本地运行

```
Agent (execute_code Python) → 写 .py + .bat 到 Desktop/
  → 用户双击 .bat → pip install playwright → 下载 Chromium → 运行爬取
  → 结果存到 Desktop/rag-data/ → 下次对话 agent 读取并处理
```

### 关键模式：用 execute_code 替代 terminal + write_file

当 `terminal` 和 `write_file` 都因 bash 层损坏而不可用时：

**写 Python 脚本：**
```python
# 在 execute_code 中用 Python open() 写文件
script = r'''...完整的爬虫脚本内容...'''
with open(r"C:\Users\username\Desktop\rag-data\crawl.py", "w", encoding="utf-8") as f:
    f.write(script)
```

**写 .bat 启动文件：**
```python
bat = """@echo off
chcp 65001 >nul
pip install playwright
python -m playwright install chromium
python "%USERPROFILE%\\Desktop\\rag-data\\crawl.py"
pause
"""
with open(r"C:\Users\username\Desktop\rag-data\run.bat", "w", encoding="utf-8") as f:
    f.write(bat)
```

**写说明文档：**
```python
readme = """...使用说明..."""
with open(r"C:\Users\username\Desktop\rag-data\README.md", "w", encoding="utf-8") as f:
    f.write(readme)
```

### Windows 特有的注意事项

| 注意事项 | 说明 |
|---------|------|
| **Chromium 缓存位置** | `%USERPROFILE%\AppData\Local\ms-playwright` 或 `%USERPROFILE%\Documents\Codex\playwright-browsers `（注意末尾空格） |
| **启动参数** | WSL 需要 `--no-sandbox`，Windows 原生不需要，但加上也无害 |
| **Python 路径** | Windows 上直接在 cmd 用 `python` 即可，不需要 `python3` |
| **编码问题** | `.bat` 文件第一行加 `chcp 65001 >nul` 解决中文乱码 |
| **pip 安装慢** | 推荐清华镜像：`-i https://pypi.tuna.tsinghua.edu.cn/simple` |
| **Chrome 下载慢** | Playwright 第一次下载 Chromium 约 200MB，有进度条，耐心等 |
| **Sogou 只索引 10-15%** | Windows 方法同样受此限制，无法爬全。完整方案仍需手机微信抓包 |

## Troubleshooting

### 问题：搜狗返回 antispider 页面

**原因**：直接 requests 访问加密链接被反爬

**解决**：使用 Playwright 访问，跟随重定向

### 问题：无法提取正文内容

**原因**：`#js_content` 元素未找到

**解决**：
1. 增加等待时间 `page.wait_for_timeout(5000)`
2. 检查 URL 是否正确重定向到微信文章页
3. 使用 `page.screenshot()` 查看页面状态

### 问题：图片链接无效 / 防盗链

**原因**：微信图片需要特定 Referer + Cookie，直接 `requests.get(img_url)` 或浏览器新标签打开返回 403/空白。

**解决**：在 Playwright 页面内用 `fetch` 下载——页面已有完整 Cookie 和 Referer，微信服务端认为是一次正常的图片加载。

```python
# ✅ 页面内 fetch → base64 → 解码写入本地
result = page.evaluate("""
    async (url) => {
        const resp = await fetch(url);
        const blob = await resp.blob();
        const reader = new FileReader();
        return new Promise((resolve) => {
            reader.onloadend = () => resolve(reader.result);
            reader.readAsDataURL(blob);
        });
    }
""", img_url)

if result and result.startswith("data:"):
    header, b64 = result.split(",", 1)
    img_data = base64.b64decode(b64)
    with open(output_path, 'wb') as f:
        f.write(img_data)
```

**注意事项**：
- 图片可能较大（100KB+），建议限制并发
- `data-src` 属性通常是高清原图，优先用它而非 `src`
- 滚动页面触发懒加载后再获取 `data-src`

详见 `references/image-download.md`。

### ⚠️ 搜狗只索引 10-15% 的文章

**现象**：公众号有 100+ 篇文章，搜狗只能搜到 12 篇。

**原因**：搜狗是搜索引擎而非公众号完整镜像，按算法选择性收录（阅读量、标题关键词、发布时间等因素）。

**缓解策略**：
1. **多关键词搜索**：用 50+ 个相关术语从不同角度搜同一公众号（如 "KS 劈刀"、"KS 换能器"、"KS EFO"），每个关键词可能命中不同文章子集
2. **翻页深挖**：搜狗支持 `&page=N` 翻页，同关键词翻到无结果为止
3. **已知上限后止损**：跑完 50+ 关键词 + 多页翻页后，如果无新文章即收手

**根本解决方案**（需要手机端）：
- 微信 App → 公众号主页 → 历史消息 → 抓包 `mp.weixin.qq.com/mp/profile_ext?action=home` 接口
- 该接口返回真实全量文章列表，不受搜狗算法限制

## Version History

- **2026-06-18**: 新增 `references/markdown-conversion-v2.md` + `scripts/crawl_ks_v2.py`——爬虫 v2 改进：`html_to_markdown()` 保留图片在原位置而非堆在末尾，`make_image_src_map()` 建立原始URL→本地文件映射，自动过滤微信模板文字（扫描二维码/长按关注等）。解决 Jerry 反馈的"图片位置丢失、格式粗暴"问题。
- **2026-06-17**: 新增 `references/knowledge-base-pipeline.md` 参考文件——TXT→Markdown图文转换、HTML DOM按 `<img>` 位置嵌入图片、模板文字清洗（特别声明/免责声明/转载声明）、重复图片 MD5 hash 去重（引导点赞图68KB GIF）、反防盗链图片批量下载。141篇/750图实战验证。
- **2026-06-16 (2)**: 图片下载重大突破——发现 `requests` + `Referer` header 即可 100% 下载微信图片，无需 Playwright。实测 141 篇文章 750 张图零失败。新增批量爬取的输出目录结构（每篇文章 .txt + 图片文件夹）。修正了"图片无法直接下载"的过时断言。
- **2026-06-16 (1)**: 新增「直接URL抓取」模式——`mp.weixin.qq.com/s/...` 链接可直接用 `requests` 抓取，无需 Playwright。增加完整的 Python 提取代码、HTML 选择器对照表。
- **2026-06-10**: 关键修复 — `networkidle` → `domcontentloaded`（中国站点挂起问题）、`--no-sandbox`（WSL 必须）、图片下载用页面内 fetch。
- **2026-05-06**: 初始版本，验证搜狗搜索 + Playwright 爬取方案