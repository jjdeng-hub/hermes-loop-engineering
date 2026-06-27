#!/usr/bin/env python3
"""
爬取指定公众号的全部文章 → 导入 RAG 知识库
============================================
用法: python3 -u crawl_account.py "公众号名称"
输出: ~/rag-agent/data/ 目录下，每篇文章一个 .txt 文件

关键设计决策:
  - wait_until="domcontentloaded" (非 networkidle，国内网站会卡死)
  - --no-sandbox (WSL 必须)
  - executable_path 自动检测已缓存的 Chromium (避免下载新版)
  - type=2&query=公众号名 → 按 source 过滤 (搜狗搜索)
"""
import sys, time, re
from pathlib import Path
from urllib.parse import quote
from datetime import datetime

# ═══════════════════════ 配置 ═══════════════════════
OUTPUT_DIR = Path.home() / "rag-agent" / "data"
MAX_PAGES = 10          # 最多翻页数
PAGE_DELAY = 3          # 页间延迟（秒）
ARTICLE_DELAY = 2       # 文章间延迟

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def find_chromium() -> str | None:
    """自动查找已缓存的 Chromium（避免下载新版）"""
    cache = Path.home() / ".cache" / "ms-playwright"
    if cache.exists():
        for d in sorted(cache.iterdir(), reverse=True):
            for sub in ["chrome-linux64/chrome", "chrome-headless-shell-linux64/chrome-headless-shell"]:
                p = d / sub
                if p.exists():
                    return str(p)
    return None


def search_articles(page, query: str, page_num: int = 1) -> list[dict]:
    """搜索公众号文章，返回 [{title, source, link, pub_time}]"""
    encoded = quote(query)
    url = f"https://weixin.sogou.com/weixin?type=2&query={encoded}&page={page_num}"
    print(f"  🔍 搜索第 {page_num} 页...")
    
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(3000)
    except Exception as e:
        print(f"  ⚠️ 页面加载超时: {e}")
        return []
    
    items = page.query_selector_all('//ul[@class="news-list"]//li')
    if not items:
        content = page.content()
        if "antispider" in content.lower() or "验证" in content:
            print("  ❌ 被反爬拦截！")
        return []
    
    results = []
    for item in items:
        try:
            title_el = item.query_selector('h3 a')
            title = title_el.inner_text().strip() if title_el else ""
            
            link = title_el.get_attribute("href") if title_el else ""
            if link and link.startswith("/"):
                link = f"https://weixin.sogou.com{link}"
            
            source_el = item.query_selector('span.all-time-y2')
            source = source_el.inner_text().strip() if source_el else ""
            
            time_el = item.query_selector('span.s2')
            pub_time = ""
            if time_el:
                time_text = time_el.inner_text()
                m = re.search(r"timeConvert\('(\d+)'\)", time_text)
                if m:
                    ts = int(m.group(1))
                    pub_time = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            
            if title and source:
                results.append({
                    "title": title,
                    "source": source,
                    "link": link,
                    "pub_time": pub_time,
                })
        except Exception:
            continue
    
    return results


def crawl_article(context, article_info: dict) -> dict | None:
    """爬取单篇文章的完整内容（文字 + 图片链接）"""
    link = article_info["link"]
    if not link:
        return None
    
    art_page = context.new_page()
    try:
        print(f"    📄 {article_info['title'][:40]}...")
        art_page.goto(link, wait_until="domcontentloaded", timeout=25000)
        art_page.wait_for_timeout(4000)
        
        if "antispider" in art_page.url.lower():
            print(f"    ⚠️ 被反爬，跳过")
            return None
        
        try:
            h1 = art_page.query_selector('//h1[@id="activity-name"]')
            title = h1.inner_text().strip() if h1 else article_info["title"]
        except Exception:
            title = article_info["title"]
        
        try:
            content = art_page.inner_text('//div[@id="js_content"]')
        except Exception:
            content = ""
        
        try:
            imgs = art_page.eval_on_selector_all(
                '//div[@id="js_content"]//img',
                "els => els.map(el => el.getAttribute('data-src') || el.src)"
            )
        except Exception:
            imgs = []
        
        return {
            "title": title,
            "source": article_info["source"],
            "pub_time": article_info.get("pub_time", ""),
            "url": art_page.url,
            "content": content,
            "images": imgs,
            "crawl_time": datetime.now().isoformat(),
        }
    except Exception as e:
        print(f"    ❌ 爬取失败: {e}")
        return None
    finally:
        art_page.close()


def save_for_rag(article: dict) -> Path:
    """保存为 RAG 可索引的 txt 文件"""
    safe_name = re.sub(r'[\\/*?:"<>|]', '', article["title"])[:60]
    fname = f"KS_{safe_name}.txt"
    fpath = OUTPUT_DIR / fname
    
    parts = [
        f"# {article['title']}",
        f"来源: {article['source']}",
        f"时间: {article['pub_time']}",
        f"原文: {article['url']}",
        "",
        "---",
        "",
        article["content"],
    ]
    
    if article.get("images"):
        parts.append("\n---\n【图片链接（需手动查看）】")
        for i, img_url in enumerate(article["images"], 1):
            parts.append(f"  图{i}: {img_url}")
    
    fpath.write_text("\n".join(parts), encoding="utf-8")
    return fpath


def main():
    from playwright.sync_api import sync_playwright
    
    if len(sys.argv) < 2:
        print("用法: python3 -u crawl_account.py <公众号名称>")
        sys.exit(1)
    
    account_name = sys.argv[1]
    
    print("=" * 60)
    print(f"📱 爬取公众号: {account_name}")
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print("=" * 60)
    
    all_articles = []
    
    with sync_playwright() as p:
        chromium_path = find_chromium()
        if chromium_path:
            print(f"  使用 Chromium: {chromium_path}")
        
        browser = p.chromium.launch(
            headless=True,
            executable_path=chromium_path,
            args=["--no-sandbox"],
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = {runtime: {}};
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh']});
        """)
        
        page = context.new_page()
        
        print("\n📋 阶段 1: 搜索文章列表...")
        for pg in range(1, MAX_PAGES + 1):
            results = search_articles(page, account_name, pg)
            if not results:
                print(f"  第 {pg} 页无结果，停止翻页")
                break
            
            matched = [r for r in results if account_name in r["source"]]
            print(f"  第 {pg} 页: {len(results)} 条 → 匹配 {len(matched)} 条")
            
            if not matched:
                break
            
            all_articles.extend(matched)
            time.sleep(PAGE_DELAY)
        
        print(f"\n📊 共找到 {len(all_articles)} 篇文章")
        
        if not all_articles:
            print("❌ 未找到任何文章")
            browser.close()
            return
        
        print("\n📋 阶段 2: 逐篇爬取内容...")
        success = 0
        for i, art in enumerate(all_articles):
            print(f"\n[{i+1}/{len(all_articles)}]", end=" ")
            full = crawl_article(context, art)
            if full and full["content"].strip():
                fpath = save_for_rag(full)
                imgs = len(full.get("images", []))
                print(f"    ✅ {len(full['content'])}字 | {imgs}图 → {fpath.name}")
                success += 1
            else:
                print(f"    ⚠️ 内容为空")
            time.sleep(ARTICLE_DELAY)
        
        browser.close()
    
    print("\n" + "=" * 60)
    print(f"✅ 完成！成功 {success}/{len(all_articles)} 篇")
    print(f"📁 {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
