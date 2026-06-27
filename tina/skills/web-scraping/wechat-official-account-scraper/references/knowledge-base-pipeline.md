# Knowledge Base Post-Processing Pipeline

> 将爬取的微信文章转换为 RAG-ready 知识库的完整工作流
> 已验证：141 篇微信文章 → 图文 Markdown + 纯文本 + 图片文件夹

## 整体流程

```
爬取阶段（模式A：直接URL抓取）
  ↓
每篇文章输出：
  ├── 文章标题.txt           ← 纯文本（元数据 + 正文）
  └── 文章标题/               ← 图片文件夹
      ├── img_001.jpg
      └── ...
  ↓
转换阶段：TXT → Markdown（图文嵌入）
  ↓
清洗阶段：去模板文字 + 去重复图片
  ↓
RAG 索引（ChromaDB / LlamaIndex）
```

## 阶段一：TXT → Markdown 图文转换

### 问题
TXT 文件只有纯文字，750 张图片散落在各自文件夹中，检索时看不到图。

### 方案
重新抓取原文 HTML，解析正文结构，按原始顺序将 `<img>` 替换为本地路径。

```python
def html_to_md_with_images(html, img_files, safe_title):
    """解析 HTML，按原文顺序将图片嵌入文本"""
    # 提取 js_content 内部结构
    cm = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.DOTALL)
    if not cm:
        return None
    inner = cm.group(1)
    
    # 按图片标签切分 HTML
    parts = re.split(r'(<img[^>]*data-src="https?://[^"]+"[^>]*>)', inner)
    
    md_parts = []
    img_idx = 0
    
    for part in parts:
        if part.startswith('<img'):
            # 用本地图片替代
            if img_idx < len(img_files):
                alt_match = re.search(r'alt="([^"]*)"', part)
                alt = alt_match.group(1) if alt_match else f"图{img_idx+1}"
                rel_path = f"{safe_title}/{img_files[img_idx]}"
                md_parts.append(f"\n![{alt}]({rel_path})\n")
                img_idx += 1
        else:
            # 清理 HTML 标签
            text = re.sub(r'<[^>]+>', '', part)
            text = re.sub(r'&nbsp;', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            if text:
                md_parts.append(text)
    
    return '\n\n'.join(md_parts), img_idx
```

### Markdown 头部格式

```markdown
# 文章标题

**来源：** 公众号名称
**发布时间：** 2026-01-22
**原文链接：** https://mp.weixin.qq.com/s/XXX

---

正文段落文字...

![示意图描述](文章标题/img_001.jpg)

更多段落文字...

![步骤图示](文章标题/img_002.jpg)

---
```

### 关键点
- 图片按 `<img>` 在 HTML 中的出现顺序与本地 `img_001.jpg` ~ `img_XXX.jpg` 一一对应
- 使用 `data-src` 而非 `src`（微信文章的懒加载机制）
- 清理 HTML 实体：`&nbsp;` → 空格, `&lt;` → `<`, `&gt;` → `>`, `&amp;` → `&`

## 阶段二：清洗重复内容

### 问题
微信文章有大量模板性结尾（免责声明、转载声明）和重复图片（引导点赞图、封面图）。

### 清洗内容

| 类别 | 模式 | 识别方法 |
|------|------|---------|
| 免责声明 | `特别声明：本公众号发布内容除原创...` | 正则匹配，出现率 >90% |
| 转载声明 | `所有文章欢迎署名转载` | 正则匹配 |
| 尾部引导图 | 68KB GIF，出现在 45/141 篇文章末尾 | MD5 hash 去重 |
| 头部封面图 | 68KB GIF，出现在 16/141 篇文章开头 | MD5 hash 去重 |

### 文本清洗代码

```python
boilerplate_patterns = [
    r'特别声明[：:].*?(?:\n|$)',
    r'本公众号?发布之见解均为个人思考之结果仅作建议[，,].*?(?:\n|$)',
    r'所有文章欢迎署名转载.*?(?:\n|$)',
    r'所有文章欢迎转载.*?(?:\n|$)',
    r'欢迎各位道友转发.*?(?:\n|$)',
]

def clean_text(text):
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()
```

### 图片去重代码

```python
import hashlib
from collections import Counter

# 收集所有图片的 hash
img_hashes = Counter()
folder_data = []

for f in os.listdir(output_dir):
    fpath = os.path.join(output_dir, f)
    if os.path.isdir(fpath):
        imgs = sorted([i for i in os.listdir(fpath) if i.startswith('img_')])
        # 检查尾部的 hash
        if imgs:
            last_path = os.path.join(fpath, imgs[-1])
            with open(last_path, "rb") as fh:
                h = hashlib.md5(fh.read()).hexdigest()
            img_hashes[h] += 1
            folder_data.append((f, imgs, h))

# 出现次数超阈值 = 模板图片
COMMON_THRESHOLD = 3
for h, count in img_hashes.most_common():
    if count >= COMMON_THRESHOLD:
        # 这就是模板图，从所有文件夹中删除该 hash 的图片
        ...
```

## 阶段三：图片下载（反防盗链）

### 微信防盗链原理
微信 CDN（`mmbiz.qpic.cn`）检查 HTTP `Referer` 头，只允许来自 `mp.weixin.qq.com` 的请求。

### 解决方案：直接 requests + Referer

```python
def download_wechat_image(img_url, article_url, output_path):
    """下载微信图片：关键在 Referer header"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
        "Referer": article_url,  # ★ 核心：设为文章链接
        "Accept": "image/*,*/*;q=0.8",
    }
    resp = requests.get(img_url, headers=headers, timeout=20)
    if resp.status_code == 200 and len(resp.content) > 1000:
        with open(output_path, "wb") as f:
            f.write(resp.content)
        return True
    return False
```

**验证结果**：141 篇文章，301 张图片，100% 成功率。

### 高频出现的模板图片确认
同一篇 MD5 hash 的图片出现在多篇文章末尾 = 引导点赞/关注图。在验证的 141 篇文章中：
- 尾部引导图（hash `b156ea...`）：45 篇，68KB GIF
- 头部封面图（同 hash）：16 篇，68KB GIF

## 推荐输出目录结构

```
rag-data/
├── 文章标题1.txt          ← 纯文本（用于 RAG 索引）
├── 文章标题1.md           ← Markdown（图文版，用于阅读）
├── 文章标题1/              ← 图片文件夹
│   ├── img_001.jpg
│   └── ...
├── 文章标题2.txt
├── 文章标题2.md
├── 文章标题2/
├── ...
├── _article_list.json     ← 元数据索引
└── _knowledge_base_summary.json
```

这种结构：
- `.txt` → ChromaDB 直接索引
- `.md` → 人类阅读（VS Code 或 Typora 打开即见图文）
- 图片文件夹 → 独立目录，不干扰索引
