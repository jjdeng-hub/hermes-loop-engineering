---
name: wechat-article-scraper
description: 微信公众号文章爬取完整方案 - 通过搜狗搜索 + Playwright 绕过反爬
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [Web Scraping, WeChat, Playwright, Sogou, Article Extraction]
    homepage: https://github.com/kebenxiaoming/matrix
---

# 微信公众号文章爬取技能

## 概述

通过搜狗微信搜索 + Playwright 绕过反爬，成功获取微信公众号文章内容。

## 核心难点与解决方案

| 难点 | 原因 | 解决方案 |
|------|------|----------|
| 直接访问 mp.weixin.qq.com | 几乎全部被屏蔽 | 通过搜狗搜索获取链接 |
| 搜狗返回加密链接 | `/link?url=<编码>` 格式 | Playwright 自动跟随重定向 |
| 搜狗反爬拦截 | 检测到自动化请求 | Playwright + 防检测脚本 |
| 标题/元数据提取 | HTML 结构动态变化 | 使用 `//ul[@class="news-list"]//li` 选择器 |
| WSL 无显示环境 | 无法运行 headed browser | 使用 headless=True + 防检测脚本 |
| **page.goto 无限挂起** | `networkidle` 等待第三方资源（国内站 tracker/广告超时） | **改用 `wait_until="domcontentloaded"` + `wait_for_timeout`** |
| **Chromium 启动失败 (WSL)** | WSL 缺少沙箱支持 | **添加 `args=["--no-sandbox"]`** |
| **微信图片防盗链** | 图片需要微信 Cookie + Referer，直接 requests 被拒 | **Playwright 页面内 `fetch()` 下载 → base64 → 存本地** |

## 完整工作流程

```
搜索关键词 → 搜狗微信搜索 → 提取文章列表 → 解码加密链接 
    → Playwright 访问 → 获取真实 URL → 爬取文章内容 → 保存 JSON/Markdown
```

## 使用方法

### 1. 基础搜索

```bash
cd /home/jjdeng/.hermes/projects/matrix
python3 wechat_scraper.py search <关键词>
```

### 2. 完整爬取（推荐）

```bash
python3 wechat_full_crawl.py <关键词>
# 或指定第 N 篇文章
python3 wechat_full_crawl.py <关键词> <索引>
```

### 3. 直接爬取已知链接

```bash
python3 wechat_scraper.py scrape <文章链接>
```

## 核心代码片段

### 搜狗搜索（正确选择器）

```python
# 文章列表选择器
article_items = tree.xpath('//ul[@class="news-list"]//li')

# 标题提取
title_elem = item.xpath('.//h3/a/text()')
title = title_elem[0].strip() if title_elem else "无标题"

# 来源提取
source_elem = item.xpath('.//span[@class="all-time-y2"]/text()')
source = source_elem[0].strip() if source_elem else "未知"

# 发布时间（从 JavaScript 中提取时间戳）
time_elem = item.xpath('.//span[@class="s2"]/text()')
ts_match = re.search(r"timeConvert\('(\d+)'\)", time_elem[0])
```

### Playwright 防检测配置

```python
context = browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    viewport={"width": 1920, "height": 1080}
)

# 添加防检测脚本
context.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    window.chrome = {runtime: {}};
    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
    Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh']});
""")
```

### 文章正文提取

```python
# 等待内容加载
page.wait_for_timeout(3000)

# 提取标题
article_title = page.title()

# 提取公众号
source_text = page.inner_text('//a[@class="rich_media_meta_nickname"]')

# 提取正文
content_text = page.inner_text('//div[@id="js_content"]')
content_html = page.inner_html('//div[@id="js_content"]')

# 提取图片
images = page.eval_on_selector_all(
    '//div[@id="js_content"]//img',
    "imgs => imgs.map(img => img.src || img.getAttribute('data-src'))"
)
```

## 输出格式

### JSON 结构

```json
{
  "title": "文章标题",
  "source": "公众号名称",
  "pub_time": "2026-05-06",
  "url": "https://mp.weixin.qq.com/s?src=...",
  "content_text": "正文文本内容",
  "content_html": "正文 HTML 内容",
  "images": ["图片 URL 列表"],
  "search_query": "搜索关键词",
  "search_index": 0,
  "crawl_time": "2026-05-06T08:47:44"
}
```

### Markdown 结构

```markdown
# 文章标题

**来源：** 公众号名称  
**发布时间：** 2026-05-06  
**原文链接：** https://mp.weixin.qq.com/s?...

---

## 正文

正文内容...

---

*爬取时间：2026-05-06 08:47:44*
```

## 依赖安装

```bash
uv pip install requests lxml playwright
playwright install chromium
```

## 注意事项

| 项目 | 说明 |
|------|------|
| ⚠️ **不要过度工程化** | 用户给直接 URL 时，用 `requests` 即可——**不要装 Playwright**。Playwright 只用于搜狗搜索的加密链接重定向。在直接 URL 上装 Playwright + Chromium 是浪费时间。 |
| **Playwright Chromium 下载 (国内)** | `playwright install chromium` 默认从外网下载 150MB+，国内大概率超时。npm mirror (`PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/`) 也可能失败。**结论：能用 requests 就别装 Playwright。** |
| **反爬检测** | 单篇文章用 requests+Referer 即可，不需要 Playwright |
| **图片防盗链** | 下载图片时设 `Referer` 为文章 URL；MD5 去重过滤模板 GIF |
| **图片位置** | ⭐ 用 `html_to_markdown()` 先替换 img 再 strip 标签，图片保留在原位置（见 `references/html-to-markdown-with-images.md`） |
| **元数据提取 (source)** | `id="js_name"` 文本跨行，正则必须加 `re.DOTALL`：`re.search(r'id="js_name"[^>]*>\s*(.*?)\s*</', html, re.DOTALL)` |
| **元数据提取 (pub_time)** | 微信 JS 动态注入时间戳到 DOM，raw HTML 中 `<em id="publish_time">` 始终为空。从 script 标签 JSON 提取不可靠（多次请求内容不同）。**直接跳过，使用爬取时间。** |
| **搜狗搜索现状** | 搜狗结果页已完全 JS 渲染，raw HTML 中无文章链接。**绕过 antispider 方法**：先用 iPhone UA（`Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15`）访问首页 `https://weixin.sogou.com/` 获取 cookie（`SUID`、`ABTEST`），再用同 session 搜索可绕过反爬看到「找到约104条结果」。但文章链接仍在 JS 中，无法从 raw HTML 提取。**结论：搜狗方案无法用于实际爬取，让用户通过微信App直接分享文章 URL。** |
| **Playwright 安装 (国内)** | `playwright install chromium` 默认源和 `npmmirror.com` 镜像均下载失败。Chromium 150MB+ 无法通过国内网络获取。**单篇文章用 requests 即可，不依赖 Playwright。** |
| **发布时间** | 微信 JS 动态渲染，raw HTML 取不到。回退到爬取时间 |
| **内容完整性** | 尾部自动清理以下微信模板文字：`**热门内容快速导读**` 及后续列表、`特别声明：...` 版权段落、`扫描二维码.*?关注` 引导图文字、`长按识别.*?关注`、`阅读原文` |
| **链接加密** | 搜狗返回加密链接，需 Playwright 解码（仅批量搜狗搜索时需要） |
| **法律合规** | 仅用于学习研究，商业使用需获得授权 |
| **批量重爬** | 已有知识库升级时：从旧 .txt 提取 URL → 去重 → 逐篇 `crawl_single_article()` → 新输出覆盖旧文件。143篇约250秒。 |

## 文件位置

```
~/.hermes/skills/web-scraping/wechat-article-scraper/
├── SKILL.md                                    # 本文件
├── references/
│   ├── page-goto-pitfalls.md                   # page.goto 常见坑 (networkidle/--no-sandbox)
│   ├── post-crawl-cleanup.md                   # 爬取后清洗：图片分类 + 模板清理 + 领域分析
│   └── html-to-markdown-with-images.md         # ⭐ HTML→Markdown（图片原位嵌入 + 微信垃圾清洗）
├── scripts/
│   ├── wechat_scraper.py                       # 基础搜索脚本
│   └── wechat_full_crawl.py                    # 完整爬取脚本（推荐）
```

实战脚本（已验证可运行）：

```
~/rag-agent/
├── crawl_ks_account.py               # 公众号全量文章爬取（搜狗搜索 → 逐篇爬取）
├── download_images.py                # 微信图片批量下载（页面内 fetch → base64 → 本地）
└── data/
    ├── KS_*.txt                       # 爬取的文章文本
    └── images/                        # 下载的图片
```

## 微信图片下载（绕过防盗链）

微信图片有严格防盗链：需要正确的 Cookie + Referer，直接 `requests.get()` 被拒。方案：在 Playwright 页面内用 JS `fetch()` —— 自动继承浏览器的 Cookie 和 Referer。

```python
import base64

# 1. 获取所有图片 URL（用 data-src，懒加载前的原始链接画质更高）
imgs = page.query_selector_all('//div[@id="js_content"]//img')
urls = [img.get_attribute("data-src") or img.get_attribute("src") 
        for img in imgs if img.get_attribute("data-src")]

# 2. 页面内 fetch 下载 → base64 → 解码存本地
for i, img_url in enumerate(urls):
    result = page.evaluate("""
        async (url) => {
            try {
                const resp = await fetch(url);
                const blob = await resp.blob();
                const reader = new FileReader();
                return new Promise((resolve) => {
                    reader.onloadend = () => resolve(reader.result);
                    reader.readAsDataURL(blob);
                });
            } catch(e) { return null; }
        }
    """, img_url)
    
    if result and result.startswith("data:"):
        header, b64 = result.split(",", 1)
        img_data = base64.b64decode(b64)
        # 根据 MIME 确定扩展名
        ext = "png" if "png" in header else "jpg"
        Path(f"images/article_{i+1:02d}.{ext}").write_bytes(img_data)
```

### Chromium 启动（WSL 兼容 + 缓存版本自动检测）

```python
import os
from pathlib import Path

# 自动检测已缓存的 Chromium 版本（避开 Playwright 官方 CDN 下载慢的问题）
chromium_path = None
cache_dir = Path.home() / ".cache" / "ms-playwright"
if cache_dir.exists():
    for d in sorted(cache_dir.iterdir(), reverse=True):
        chrome = d / "chrome-linux64" / "chrome"
        if chrome.exists():
            chromium_path = str(chrome)
            break

browser = p.chromium.launch(
    headless=True,
    executable_path=chromium_path,  # 指定缓存版本
    args=["--no-sandbox"],          # WSL 必须
)
```

## 爬取后清洗（重要）

爬取完成后必须进行知识库清洗，详见 [references/post-crawl-cleanup.md](references/post-crawl-cleanup.md)：

1. **文字层面** — 正则删除模板文字（"点击关注"、"声明"、"热门导读"等）
2. **图片分类** — 用视觉模型（Claude/Gemini/Qwen-VL）区分技术内容图 vs 引导装饰图
3. **非技术文章识别** — 删除与主题无关的自动附带文章
4. **知识覆盖分析** — 扫描关键词统计领域覆盖，找空白缺口

### 视觉模型 API 回退方案

当 Hermes 内置 `vision_analyze` 工具不可用（提示 "No LLM provider configured for task=vision"），直接从 `config.yaml` 的 `custom_providers` 中读取 API key，调用 Anthropic Messages API 做图片分类。详见参考文档。

## 轻量单篇爬取 — `crawl_single_article()`（⭐推荐）

**核心发现：** 直接访问 `mp.weixin.qq.com/s/...` 的微信文章 URL，用 `requests + 正确 User-Agent` 即可获取完整 HTML，**不需要 Playwright**。Playwright 仅用于搜狗搜索的加密链接重定向。

### 全集成函数（一键调用）

实战脚本：`Desktop/rag-data/crawl_ks_account.py` → `crawl_single_article(url, output_dir)`

```python
from crawl_ks_account import crawl_single_article

result = crawl_single_article(
    "https://mp.weixin.qq.com/s/XXXX",
    "C:/Users/jjdeng/Desktop/rag-data"
)
# 输出：{title}_imgs/article.md（图片在原位置）+ {title}.txt（纯文本，RAG用）
```

### 函数内部流程

```python
# 1. requests 获取 HTML（含完整正文和图片 data-src）
resp = requests.get(url, headers=headers)

# 2. 提取元数据
source = re.search(r'id="js_name"[^>]*>\s*(.*?)\s*</', html, re.DOTALL)
# ⚠️ 发布时间是 JS 动态渲染，raw HTML 取不到，跳过

# 3. 提取正文 <div id="js_content">
content_html = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.DOTALL)

# 4. 下载图片（Referer 绕过防盗链 + MD5 去重）
for img_url in img_urls:
    r = requests.get(img_url, headers={"Referer": article_url})
    # MD5 去重过滤微信模板 GIF

# 5. HTML→Markdown（图片原位嵌入）⭐核心
md_body = html_to_markdown(content_html, img_map)  # 详见 references/html-to-markdown-with-images.md

# 6. 尾部垃圾清洗
# - **热门内容快速导读** + 推荐文章列表
# - 特别声明：... 版权段落
# - 扫描二维码/长按识别 引导文字

# 7. 双输出
# - {title}_imgs/article.md  → 完整 Markdown（图片在原位置）
# - {title}.txt              → 纯文本（去图，用于 RAG 索引）
```

### 批量重爬已有知识库

当旧版知识库（图片堆末尾）需要升级时：

```python
# 1. 从旧 .txt 提取所有 URL
urls = []
for f in os.listdir(rag_dir):
    m = re.search(r'链接[：:]?\s*(https?://mp\.weixin\.qq\.com/s/[^\s\n]+)', content)
    if m: urls.append(m.group(1))

# 2. 去重后逐篇重爬
unique_urls = list(dict.fromkeys(urls))

# 3. 备份旧文件后批量跑
for url in unique_urls:
    crawl_single_article(url, rag_dir)

# 4. 清理旧残留（旧 _imgs 目录 + 旧 .md 文件）
# 保留新格式：{title}.txt + {title}_imgs/
```

143篇约 250 秒，成功率 ~99%。

## 扩展应用

| 场景 | 实现方式 |
|------|----------|
| 定时监控 | 配合 cronjob 定时搜索关键词 |
| 内容聚合 | 批量爬取后存入数据库 |
| AI 改写 | 结合 LLM 对文章进行改写/摘要 |
| 自动发布 | 整合到 Matrix 项目实现"爬取→发布"闭环 |
| 知识库清洗 | 参考 post-crawl-cleanup.md — 图片分类 + 模板清理 + 领域分析 |

---

*创建时间：2026-05-06*
*最后更新：2026-06-17 — 新增爬取后清洗流程*
*测试环境：WSL + Python 3.11 + Playwright 1.59*