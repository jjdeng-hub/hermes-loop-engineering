# HTML→Markdown 转换（保留图片位置）

> 解决微信公众号文章爬取的核心问题：图片嵌入原文正确位置，而非堆在末尾。

## 核心函数

```python
import re

def html_to_markdown(html, img_map=None):
    """HTML转Markdown：图片保留在原位置，转换标题/粗体/列表"""
    md = html
    
    # Step 1: 替换图片为 Markdown（在原位置，最先处理）
    if img_map:
        for src, local_name in img_map.items():
            md = re.sub(
                r'<img[^>]*' + re.escape(src) + r'[^>]*>',
                '\n\n![](' + local_name + ')\n\n',
                md
            )
    md = re.sub(r'<img[^>]*>', '', md)  # 移除未匹配的图片
    
    # Step 2: 换行和段落
    md = re.sub(r'<br\s*/?>', '\n', md)
    md = re.sub(r'<p[^>]*>', '\n\n', md)
    md = re.sub(r'</p>', '', md)
    
    # Step 3: 标题 (h1-h4)
    md = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', md)
    md = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', md)
    md = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', md)
    md = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', md)
    
    # Step 4: 粗体/强调
    md = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', md)
    md = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', md)
    md = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', md)
    
    # Step 5: 列表
    md = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', md)
    md = re.sub(r'</?[ou]l[^>]*>', '\n', md)
    
    # Step 6: Section/div/span — 提取文本
    md = re.sub(r'</?section[^>]*>', '\n', md)
    md = re.sub(r'<div[^>]*>', '\n', md)
    md = re.sub(r'</div>', '', md)
    md = re.sub(r'</?span[^>]*>', '', md)
    
    # Step 7: 特殊字符
    md = md.replace('&amp;', '&').replace('&lt;', '<')
    md = md.replace('&gt;', '>').replace('&quot;', '"')
    md = md.replace('&nbsp;', ' ')
    
    # Step 8: 移除剩余标签
    md = re.sub(r'<[^>]+>', '', md)
    
    # Step 9: 清理空行
    md = re.sub(r'\n{4,}', '\n\n\n', md)
    md = md.strip()
    
    return md
```

## 处理顺序关键

**必须先替换图片，再 strip 剩余标签。** 错误顺序导致图片信息丢失：

```
❌ 错误: strip所有标签 → 图片全没了 → 末尾追加 → 位置丢失
✅ 正确: 替换图片为 ![]() → 再 strip 剩余标签 → 图片在原位置
```

## 微信文章尾部垃圾清洗

```python
# 这些模式在微信文章末尾反复出现，需自动过滤
cleanup_patterns = [
    r'扫描二维码.*?关注',
    r'长按识别.*?关注',
    r'点击上方.*?关注',
    r'\*\*KS焊线机技术进阶热门内容快速导读[：:]?\*\*.*',  # 推荐文章列表
    r'特别声明[：:].*',  # 版权声明
    r'热门内容快速导读[：:]?.*',
    r'阅读原文.*?\n',
]

for pat in cleanup_patterns:
    md_body = re.sub(pat, '', md_body, flags=re.DOTALL)
md_body = re.sub(r'\n{4,}', '\n\n\n', md_body).strip()
```

## 图片下载（绕过微信防盗链）

```python
import requests, hashlib

def download_wechat_images(img_urls, article_url, output_dir):
    """下载微信文章图片，自动去重模板GIF"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": article_url,  # 关键：Referer 设为文章URL绕过防盗链
    }
    
    img_map = {}
    seen_hashes = set()
    
    for idx, img_url in enumerate(img_urls[:50]):
        try:
            r = requests.get(img_url, headers=headers, timeout=10)
            if r.status_code != 200:
                continue
            
            # 去重（微信模板图 MD5 相同）
            h = hashlib.md5(r.content).hexdigest()
            if h in seen_hashes:
                continue
            seen_hashes.add(h)
            
            # 确定扩展名
            ct = r.headers.get('Content-Type', '')
            ext = 'png' if 'png' in ct else 'gif' if 'gif' in ct else 'jpg'
            
            fname = f"img_{idx+1:03d}.{ext}"
            with open(os.path.join(output_dir, fname), 'wb') as f:
                f.write(r.content)
            img_map[img_url] = fname
        except Exception:
            continue
    
    return img_map
```

## 已知限制

- **发布时间不可靠**：微信用 JS 动态渲染时间，raw HTML 中 `<em id="publish_time">` 为空。时间戳藏在 URL 编码的 JSON 里（`publish_time%22%3A...`），提取不稳定。回退方案：使用爬取时间。
- **HTML 结构变化**：微信可能修改 `#js_content` 选择器。回退到 `.rich_media_content`。
- **模板 GIF 误下载**：68KB 左右的 GIF 且 MD5 相同的是微信引导关注图，通过 MD5 去重自动过滤。
