# Markdown 转换 v2 — 图片位置保留 + 格式转换

> 2026-06-18：Jerry 反馈旧爬虫太粗暴——HTML→纯文本 strip 标签，图片全堆在末尾，位置丢失。

## 旧版问题

```python
# 旧：strip 所有标签，图片位置丢失
md_body = re.sub(r'<[^>]+>', '', content_html)
# 图片堆在末尾
for img_name in result["images"]:
    md_content += f"![{img_name}]({img_name})\n\n"
```

## v2：`html_to_markdown()` 核心函数

```python
def html_to_markdown(html, img_map=None):
    """HTML转Markdown：保留图片在原位置，转换标题/粗体/列表"""
    import re
    md = html
    
    # 1. 图片替换（在原位置，最先执行）
    if img_map:
        for src, local_name in img_map.items():
            md = re.sub(
                r'<img[^>]*' + re.escape(src) + r'[^>]*>',
                '\n\n![](' + local_name + ')\n\n',
                md
            )
    md = re.sub(r'<img[^>]*>', '', md)  # 移除未匹配的图片
    
    # 2. 换行和段落
    md = re.sub(r'<br\s*/?>', '\n', md)
    md = re.sub(r'<p[^>]*>', '\n\n', md)
    md = re.sub(r'</p>', '', md)
    
    # 3. 标题 h1-h4 → #-####
    md = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', md)
    md = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', md)
    md = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', md)
    md = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', md)
    
    # 4. 粗体/强调
    md = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', md)
    md = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', md)
    md = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', md)
    
    # 5. 列表
    md = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', md)
    md = re.sub(r'</?[ou]l[^>]*>', '\n', md)
    
    # 6. section/div/span → 提取文本
    md = re.sub(r'</?section[^>]*>', '\n', md)
    md = re.sub(r'<div[^>]*>', '\n', md)
    md = re.sub(r'</div>', '', md)
    md = re.sub(r'</?span[^>]*>', '', md)
    
    # 7. HTML 实体
    md = md.replace('&amp;', '&').replace('&lt;', '<')
    md = md.replace('&gt;', '>').replace('&quot;', '"').replace('&nbsp;', ' ')
    
    # 8. 移除剩余标签
    md = re.sub(r'<[^>]+>', '', md)
    
    # 9. 清理多余空行
    md = re.sub(r'\n{4,}', '\n\n\n', md)
    return md.strip()
```

## 单篇文章爬取（纯 requests，无 Playwright）

```python
def crawl_single_article(url, output_dir):
    """爬取单篇微信文章——纯requests，图片嵌入正确位置"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",
        "Referer": "https://mp.weixin.qq.com/",
    }
    
    # 1. 获取页面
    resp = requests.get(url, headers=headers, timeout=15)
    html = resp.text
    
    # 2. 提取元数据
    title_m = re.search(r'id="activity-name"[^>]*>(.*?)</h1', html, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else "?"
    
    # 3. 提取正文HTML
    content_m = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.DOTALL)
    content_html = content_m.group(1)
    
    # 4. 提取+下载图片（Referer绕过防盗链，MD5去重模板图）
    img_urls = re.findall(r'<img[^>]*data-src="([^"]+)"[^>]*>', content_html)
    img_map = {}
    seen_hashes = set()
    for idx, img_url in enumerate(img_urls[:50]):
        ih = headers.copy(); ih["Referer"] = url
        r = requests.get(img_url, headers=ih, timeout=10)
        if r.status_code == 200:
            h = hashlib.md5(r.content).hexdigest()
            if h in seen_hashes: continue  # 跳过重复模板图
            seen_hashes.add(h)
            ext = 'png' if 'png' in r.headers.get('Content-Type','') else 'jpg'
            fname = f"img_{idx+1:03d}.{ext}"
            with open(os.path.join(img_dir, fname), 'wb') as f:
                f.write(r.content)
            img_map[img_url] = fname
    
    # 5. 转换 Markdown（图片在正确位置）
    md_body = html_to_markdown(content_html, img_map)
    
    # 6. 清理微信模板文字
    for pat in [r'扫描二维码.*?关注', r'长按识别.*?关注', r'点击上方.*?关注']:
        md_body = re.sub(pat, '', md_body, flags=re.DOTALL)
    
    # 7. 保存（Markdown有图 + TXT纯文本给RAG）
    # Markdown: 图片在原文位置
    md_content = f"# {title}\n\n> 来源：{source} | 时间：{pub_time}\n> 原文：{url}\n\n---\n\n{md_body}"
    # TXT: 去掉图片标记，用于RAG索引
    txt_body = re.sub(r'!\[.*?\]\(.*?\)', '', md_body)
    txt_content = f"标题：{title}\n来源：{source}\n时间：{pub_time}\n链接：{url}\n\n{txt_body}"
```

## 改进对比

| | 旧版 | v2 |
|------|------|-----|
| 图片 | 堆在末尾 | 嵌入原文位置 `![]()` |
| 标题 | 纯文本 | `# ## ### ####` |
| 粗体 | 丢失 | `**text**` |
| 列表 | 无 | `- item` |
| 输出 | `.txt`（无图） | `.md`（有图）+ `.txt`（去图，RAG用） |
| 模板文字 | 手动删 | 自动正则过滤 |
| 依赖 | Playwright | 纯 `requests` |
