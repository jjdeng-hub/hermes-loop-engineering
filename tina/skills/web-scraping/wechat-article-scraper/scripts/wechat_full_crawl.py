#!/usr/bin/env python3
"""
微信公众号文章爬取 - 终极版
使用 Playwright 完整绕过反爬
"""

import json
import time
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent / "wechat_articles"
OUTPUT_DIR.mkdir(exist_ok=True)

def full_crawl(query: str, article_index: int = 0):
    """
    完整爬取流程：搜索 → 获取真实链接 → 爬取文章
    """
    from playwright.sync_api import sync_playwright
    
    print("=" * 60)
    print(f"📱 微信公众号文章爬取 - 完整流程")
    print("=" * 60)
    print(f"\n🔍 搜索关键词：{query}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
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
        
        page = context.new_page()
        
        # 步骤 1：搜索
        print("\n📋 步骤 1：搜索文章...")
        search_url = f"https://weixin.sogou.com/weixin?type=2&query={query}"
        page.goto(search_url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(3000)
        
        # 截图搜索页面
        page.screenshot(path=str(OUTPUT_DIR / "search_page.png"))
        print("   ✅ 搜索页面已截图")
        
        # 提取文章列表
        print("\n📋 步骤 2：提取文章列表...")
        article_items = page.query_selector_all('//ul[@class="news-list"]//li')
        print(f"   找到 {len(article_items)} 篇文章")
        
        if not article_items or article_index >= len(article_items):
            print("   ❌ 未找到文章或索引超出范围")
            browser.close()
            return None
        
        # 获取指定文章
        target_item = article_items[article_index]
        
        # 提取标题（使用 CSS 选择器）
        title_elem = target_item.query_selector('h3 a')
        title = title_elem.inner_text() if title_elem else "无标题"
        print(f"   目标文章：{title}")
        
        # 获取链接
        encoded_link = title_elem.get_attribute("href") if title_elem else ""
        full_sogou_link = f"https://weixin.sogou.com{encoded_link}" if encoded_link else ""
        
        # 提取来源
        source_elem = target_item.query_selector('span.all-time-y2')
        source = source_elem.inner_text() if source_elem else "未知"
        
        # 步骤 3：访问文章（使用新页面避免反爬）
        print("\n📋 步骤 3：访问文章...")
        
        # 创建新页面访问链接
        article_page = context.new_page()
        
        # 直接访问搜狗链接
        print(f"   访问：{full_sogou_link[:80]}...")
        article_page.goto(full_sogou_link, wait_until="networkidle", timeout=30000)
        article_page.wait_for_timeout(5000)  # 等待重定向
        
        final_url = article_page.url
        print(f"   最终 URL：{final_url[:100]}...")
        
        # 检查是否被反爬
        if "antispider" in final_url:
            print("   ⚠️ 被反爬拦截，尝试其他方式...")
            # 尝试直接访问微信文章（如果 URL 包含微信域名）
            if "mp.weixin.qq.com" in final_url:
                pass  # 继续
            else:
                browser.close()
                return {"error": "被反爬拦截"}
        
        # 步骤 4：提取文章内容
        print("\n📋 步骤 4：提取文章内容...")
        
        # 等待内容加载
        article_page.wait_for_timeout(3000)
        
        # 提取标题
        article_title = article_page.title()
        print(f"   标题：{article_title}")
        
        # 提取公众号
        try:
            source_text = article_page.inner_text('//a[@class="rich_media_meta_nickname"]')
        except:
            source_text = source
        
        # 提取发布时间
        try:
            pub_time_text = article_page.inner_text('//div[@class="rich_media_meta_text"]')
        except:
            pub_time_text = ""
        
        # 提取正文
        try:
            content_text = article_page.inner_text('//div[@id="js_content"]')
            content_html = article_page.inner_html('//div[@id="js_content"]')
        except Exception as e:
            print(f"   ⚠️ 正文提取失败：{e}")
            content_text = ""
            content_html = ""
        
        # 提取图片
        try:
            images = article_page.eval_on_selector_all(
                '//div[@id="js_content"]//img',
                "imgs => imgs.map(img => img.src || img.getAttribute('data-src'))"
            )
        except:
            images = []
        
        article_page.close()
        browser.close()
        
        # 构建结果
        article = {
            "title": article_title,
            "source": source_text,
            "pub_time": pub_time_text,
            "url": final_url,
            "content_text": content_text[:5000],
            "content_html": content_html[:10000],
            "images": images[:10],
            "search_query": query,
            "search_index": article_index,
            "crawl_time": datetime.now().isoformat(),
        }
        
        # 保存文章
        safe_title = "".join(c for c in article_title if c.isalnum() or c in " -_")[:50]
        timestamp = int(time.time())
        
        json_path = OUTPUT_DIR / f"{timestamp}_{safe_title}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(article, f, ensure_ascii=False, indent=2)
        
        md_path = OUTPUT_DIR / f"{timestamp}_{safe_title}.md"
        md_content = f"""# {article_title}

**来源：** {source_text}  
**发布时间：** {pub_time_text}  
**原文链接：** {final_url}

---

## 正文

{content_text[:3000]}

---

*爬取时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*搜索关键词：{query}*
"""
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"\n✅ 爬取成功！")
        print(f"   标题：{article_title}")
        print(f"   来源：{source_text}")
        print(f"   正文：{len(content_text)} 字符")
        print(f"   图片：{len(images)} 张")
        print(f"\n📁 已保存：")
        print(f"   JSON: {json_path}")
        print(f"   Markdown: {md_path}")
        
        return article


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python3 wechat_full_crawl.py <关键词> [文章索引]")
        print("\n示例：")
        print("  python3 wechat_full_crawl.py 人工智能")
        print("  python3 wechat_full_crawl.py 人工智能 1  # 爬取第 2 篇文章")
        sys.exit(1)
    
    query = sys.argv[1]
    index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    
    result = full_crawl(query, index)
    
    if result and "error" in result:
        print(f"\n❌ {result['error']}")
        sys.exit(1)
