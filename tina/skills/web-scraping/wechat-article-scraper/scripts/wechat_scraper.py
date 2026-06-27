#!/usr/bin/env python3
"""
微信公众号文章爬取工具
支持：搜索公众号 → 获取文章列表 → 爬取文章内容
"""

import requests
from lxml import html
import re
import json
import time
from pathlib import Path
from urllib.parse import quote, urlparse, parse_qs

# 配置
OUTPUT_DIR = Path(__file__).parent / "wechat_articles"
OUTPUT_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
}

def search_wechat(query: str, page: int = 1) -> dict:
    """
    搜狗微信搜索
    
    Args:
        query: 搜索关键词
        page: 页码
    
    Returns:
        搜索结果列表
    """
    url = "https://weixin.sogou.com/weixin"
    params = {
        "type": "2",  # 2=文章，1=公众号
        "query": query,
        "ie": "utf8",
        "s_from": "input",
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        
        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}"}
        
        # 检查是否触发反爬
        if "验证码" in response.text or "anti-spam" in response.text:
            return {"error": "触发反爬（验证码）"}
        
        # 解析 HTML
        tree = html.fromstring(response.text)
        
        # 提取文章列表（使用正确的选择器）
        articles = []
        article_items = tree.xpath('//ul[@class="news-list"]//li')
        
        for item in article_items[:20]:  # 取前 20 条
            try:
                # 提取标题（在 h3>a 中）
                title_elem = item.xpath('.//h3/a/text()')
                title = title_elem[0].strip() if title_elem else "无标题"
                
                # 提取链接（搜狗加密链接）
                link_elem = item.xpath('.//h3/a/@href')
                encoded_link = link_elem[0] if link_elem else ""
                
                # 构建完整的搜狗链接
                if encoded_link:
                    link = f"https://weixin.sogou.com{encoded_link}"
                else:
                    link = ""
                
                # 提取公众号名称（在 span.all-time-y2 中）
                source_elem = item.xpath('.//span[@class="all-time-y2"]/text()')
                source = source_elem[0].strip() if source_elem else "未知"
                
                # 提取发布时间（在 span.s2 中，但内容是 JavaScript）
                time_elem = item.xpath('.//span[@class="s2"]/text()')
                pub_time = ""
                if time_elem:
                    # 尝试提取时间戳
                    time_text = time_elem[0]
                    if "timeConvert" in time_text:
                        # 提取时间戳
                        import re
                        ts_match = re.search(r"timeConvert\('(\d+)'\)", time_text)
                        if ts_match:
                            ts = int(ts_match.group(1))
                            from datetime import datetime
                            pub_time = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                
                # 提取摘要
                desc_elem = item.xpath('.//p[@class="txt-info"]/text()')
                desc = ""
                if desc_elem:
                    desc = desc_elem[0].strip()
                    # 移除高亮标记
                    desc = desc.replace("<!--red_beg-->", "").replace("<!--red_end-->", "")
                
                if title and link:
                    articles.append({
                        "title": title,
                        "link": link,
                        "source": source,
                        "pub_time": pub_time,
                        "description": desc,
                    })
            except Exception as e:
                continue
        
        return {
            "query": query,
            "page": page,
            "total": len(articles),
            "articles": articles,
        }
        
    except Exception as e:
        return {"error": str(e)}


def scrape_article(url: str) -> dict:
    """
    爬取单篇微信公众号文章
    
    Args:
        url: 文章链接
    
    Returns:
        文章内容（标题、正文、图片等）
    """
    try:
        headers = HEADERS.copy()
        headers["Referer"] = "https://weixin.sogou.com/"
        
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}"}
        
        # 检查是否被屏蔽
        if "redirect" in response.text.lower() or "微信" not in response.text:
            return {"error": "文章可能被屏蔽或已删除"}
        
        tree = html.fromstring(response.text)
        
        # 提取标题
        title = tree.xpath('//h1[@id="activity-name"]/text()')
        title = title[0].strip() if title else "无标题"
        
        # 提取公众号名称
        source = tree.xpath('//a[@class="rich_media_meta_nickname"]/text()')
        source = source[0].strip() if source else "未知公众号"
        
        # 提取发布时间
        pub_time = tree.xpath('//div[@class="rich_media_meta_text"]/text()')
        pub_time = pub_time[0].strip() if pub_time else ""
        
        # 提取正文内容
        content_div = tree.xpath('//div[@id="js_content"]')
        content_html = ""
        content_text = ""
        
        if content_div:
            content_html = html.tostring(content_div[0], encoding='utf-8').decode('utf-8')
            content_text = content_div[0].text_content().strip()
        
        # 提取图片
        images = tree.xpath('//div[@id="js_content"]//img/@data-src')
        if not images:
            images = tree.xpath('//div[@id="js_content"]//img/@src')
        
        # 提取作者
        author = tree.xpath('//span[@class="rich_media_meta_text"]/text()')
        author = author[0].strip() if author else ""
        
        return {
            "title": title,
            "source": source,
            "author": author,
            "pub_time": pub_time,
            "url": url,
            "content_html": content_html,
            "content_text": content_text[:5000],  # 限制长度
            "images": images[:10],  # 限制图片数量
        }
        
    except Exception as e:
        return {"error": str(e)}


def save_article(article: dict, output_dir: Path = OUTPUT_DIR) -> str:
    """
    保存文章到文件
    
    Args:
        article: 文章数据
        output_dir: 输出目录
    
    Returns:
        保存的文件路径
    """
    # 生成安全文件名
    safe_title = re.sub(r'[\\/*?:|"<>]', '_', article.get("title", "untitled"))[:50]
    timestamp = int(time.time())
    
    # 保存 JSON
    json_path = output_dir / f"{timestamp}_{safe_title}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    
    # 保存 Markdown
    md_path = output_dir / f"{timestamp}_{safe_title}.md"
    md_content = f"""# {article.get('title', '无标题')}

**来源：** {article.get('source', '未知')}  
**作者：** {article.get('author', '')}  
**发布时间：** {article.get('pub_time', '')}  
**原文链接：** {article.get('url', '')}

---

## 正文

{article.get('content_text', '无法获取正文')[:3000]}

---

*爬取时间：{time.strftime('%Y-%m-%d %H:%M:%S')}*
"""
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return str(json_path)


def main():
    import sys
    
    print("=" * 60)
    print("📱 微信公众号文章爬取工具")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n用法：")
        print("  搜索：python3 wechat_scraper.py search <关键词>")
        print("  爬取：python3 wechat_scraper.py scrape <文章链接>")
        print("\n示例：")
        print("  python3 wechat_scraper.py search 人工智能")
        print("  python3 wechat_scraper.py scrape https://mp.weixin.qq.com/s/xxx")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "search":
        if len(sys.argv) < 3:
            print("❌ 请提供搜索关键词")
            sys.exit(1)
        
        query = sys.argv[2]
        print(f"\n🔍 搜索关键词：{query}")
        
        result = search_wechat(query)
        
        if "error" in result:
            print(f"❌ 搜索失败：{result['error']}")
            sys.exit(1)
        
        print(f"✅ 找到 {result['total']} 篇文章\n")
        
        for i, article in enumerate(result["articles"], 1):
            print(f"{i}. {article['title']}")
            print(f"   来源：{article['source']}")
            print(f"   链接：{article['link']}")
            print()
        
        # 保存搜索结果
        search_file = OUTPUT_DIR / f"search_{query}_{int(time.time())}.json"
        with open(search_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"📁 搜索结果已保存：{search_file}")
        
    elif action == "scrape":
        if len(sys.argv) < 3:
            print("❌ 请提供文章链接")
            sys.exit(1)
        
        url = sys.argv[2]
        print(f"\n📄 爬取文章：{url}")
        
        article = scrape_article(url)
        
        if "error" in article:
            print(f"❌ 爬取失败：{article['error']}")
            sys.exit(1)
        
        print(f"✅ 标题：{article['title']}")
        print(f"   来源：{article['source']}")
        print(f"   正文长度：{len(article.get('content_text', ''))} 字符")
        
        # 保存文章
        file_path = save_article(article)
        print(f"📁 文章已保存：{file_path}")
        
    else:
        print(f"❌ 未知操作：{action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
