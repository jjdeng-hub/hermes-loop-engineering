# 爬取后知识库清洗与图片分类

## 概述

爬取公众号文章后，需要进行两轮清洗：
1. **内容清洗** — 移除引导图、模板文字、非技术文章
2. **图片分类** — 用视觉模型区分技术内容图 vs 装饰引导图

本文件基于实战经验（142 篇 K&S 焊线机公众号文章、689 张配图的清洗）。

---

## 第一轮：内容清洗（文字层面）

### 移除模板文字

公众号文章常见模板垃圾：
- "点击上方蓝字关注我们"
- "声明：本文仅供学习交流..."
- "热门内容导读" + 推荐文章列表
- 文末的 "END" / "更多精彩内容" / 广告

用正则批量删除：
```python
import re

patterns = [
    r'点击上方.*关注.*\n?',
    r'声明[：:][\s\S]*?(?=\n\n|\Z)',
    r'热门内容[导引]读[\s\S]*?(?=\n\n|\Z)',
    r'END\s*\n+更多精彩[\s\S]*',
]
for pat in patterns:
    content = re.sub(pat, '', content)
```

### 移除非技术文章

判断标准：
- 标题不含设备型号/技术关键词
- 内容以法律声明、平台规则为主
- 从公众号"自动附带"的文章（如微信平台投诉指引）

清理方式：整篇目录删除。

---

## 第二轮：图片分类（视觉模型）

### 为什么需要

公众号文章配图分两类：
- **技术内容图**（应保留）：操作界面截图、参数表格、设备照片、SEM 电镜图、流程图
- **引导装饰图**（应删除）："点击蓝字关注"、"分享收藏点赞在看"、引导 GIF

### 分类策略：按嫌疑度采样

不用全部 689 张都跑视觉模型。按嫌疑度分批采样：

| 类别 | 特征 | 嫌疑度 |
|------|------|--------|
| GIF 文件 | 公众号常用引导模板 GIF | 🔴 高 |
| 极小文件 (<10KB) | 可能是装饰图标 | 🟡 中 |
| 文章首张图 (img_001) | 常为封面/引导图 | 🟡 中 |
| PNG/JPG 大图 | 大概率技术内容 | 🟢 低 |

### 视觉模型 API 调用（Hermes 环境）

当 Hermes 内置 `vision_analyze` 工具未配置视觉 provider 时，直接从 `config.yaml` 读取 API key 调用：

```python
import yaml, base64, requests

# 1. 读取 API key（从 custom_providers 中找支持视觉的）
config = yaml.safe_load(open("C:/Users/jjdeng/.hermes/config.yaml"))
fc = [p for p in config['custom_providers'] if p['name'] == 'fun-claude'][0]
api_key = fc['api_key']
base_url = fc['base_url']
model = fc['model']

# 2. Base64 编码图片
with open(img_path, 'rb') as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')

# 3. 调用 Anthropic Messages API（视觉）
payload = {
    "model": model,
    "max_tokens": 60,
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": "用中文一句话回答：这是技术内容图还是公众号引导/装饰图？如果是技术图，简述内容。"},
            {"type": "image", "source": {
                "type": "base64",
                "media_type": "image/png",  # 或 image/jpeg, image/gif
                "data": img_data
            }}
        ]
    }]
}

resp = requests.post(
    f"{base_url}/v1/messages",
    json=payload,
    headers={
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    },
    timeout=30
)

answer = resp.json()["content"][0]["text"]
```

### 批量分类步骤

1. 按嫌疑度排序：先测所有 GIF，再测极小图，再测文章首图
2. 每批测试后有结论时，用文件大小/命名规律批量处理同类图
3. 例：发现所有 68KB GIF 都是同一张引导模板 — 直接批量删除，无需逐个 API 调用



---

## 1.5 尾部垃圾全面清洗（v2 增强）

第二个公众号（KNS焊线机入门指南）尾部含大量促销内容，所有文章一致。按以下顺序清洗：

### 清洗顺序（从高优先级到低）

```python
import re

def clean_footer(content):
    original = content
    
    # 1. "免费阅读权益" + "往期推荐" + 完整文章索引（最长，最先清）
    # 格式：免费阅读权益 → 后台回复 → 往期推荐 → PREVIOUS RECOMMENDATIONS → 文章列表
    content = re.sub(
        r'免费阅读权益。[\s\S]*?(?=\n---\n\n\*爬取|\n---$)', '',
        content
    )
    
    # 2. "一个人的学习是孤单的" 知识星球推广（第二个公众号通用尾）
    # 格式：一个人的学习是孤单的，一群人的成长是高效的 → 加群/扫码 → 尾图
    content = re.sub(
        r'一个人的学习是孤单的[\s\S]*?(?=\n---\n\n\*爬取|\n---$)',
        '', content
    )
    
    # 3. "温馨提示" 案例声明（仅当是纯免责声明时清，非技术内容）
    content = re.sub(
        r'温馨提示[：:][\s\S]*?(?=\n---\n\n\*爬取|\n---$|$)',
        '', content
    )
    
    # 4. 社交提示（"点点赞" "点在看" "转发点赞在看"）
    content = re.sub(r'\*\*点点赞\*\*\s*\n', '', content)
    content = re.sub(r'\*\*点在看\*\*\s*\n', '', content)
    content = re.sub(r'\*\*转发，点赞，在看，安排一下[？?]\*\*\s*\n', '', content)
    
    # 5. 尾部标记
    content = re.sub(r'\nEND\n', '\n', content)
    content = re.sub(r'案例来源[：:][^\n]*\n?', '', content)
    content = re.sub(r'问题来源[^\n]*\n?', '', content)
    
    # 6. 保留的合法尾部内容（不要误删）：
    #    - "案例仅供参考，具体问题具体分析" — 作者在案例文章末尾的正当声明
    #    - "详情请看上一篇" / "参考前文" — 内容引用
    
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    return content
```

### 注意事项

- **不要删除"案例仅供参考"**：这是作者在案例文末的正当免责声明，不是推广
- **互动答题时间**：部分文章末尾有选择题互动（"ZTC温度正常是几度？"），这是作者设计的知识检验，不是推广，保留
- 第二批公众号约305篇有统一的"知识星球"推广尾，全部清洗后节省约15%存储

---

## 实战案例：K&S 焊线机知识库清洗两轮结果

### 第一轮（原始清洗）
```
原始：142 篇 MD + 689 张图片
├── 文字层：移除 23,311 字模板文字、60 张引导图引用
├── 图片层：
│   ├── 68 张 68KB GIF → 🗑️ 全部删除（同一张"引导分享"模板）
│   ├── 14 张"名誉保护投诉指引"配图 → 🗑️ 整篇删除（非技术文章）
│   └── 607 张技术内容图 → ✅ 保留
└── 最终：141 篇有效文章 + 607 张图片
```

### 第二轮（全量重爬 + 模板图片 MD5 去重 + 尾部垃圾清理）
```
追加第二公众号（305篇）后总计 447 篇
├── 图片层：
│   ├── 模板图识别：18 种 MD5 hash 类型，分布 30-133 篇文章
│   │   └── 删除标准：同一 hash 出现在 30+ 篇文章中 = 微信模板
│   ├── 删除 1,315 张模板图（78MB）
│   └── 保留 2,600 张技术内容图（69MB）
├── 文字层：
│   ├── 清理 162 篇 article.md 尾部垃圾（往期推荐/免费权益/星球引流）
│   └── 清理 84 篇 .txt 文件对应内容
└── 最终：447 篇有效文章 + 2,600 张技术图片
```

## 1.6 模板图片 MD5 去重流程

从大批量公众号图片中识别模板（引导图/关注图/装饰图）的高效方法：

```python
import os, hashlib
from collections import Counter

# 1. 扫描所有文章目录，建立 hash → [(文章, 文件名, 大小)] 映射
hash_map = {}
for img_dir in all_img_dirs:
    for f in os.listdir(img_dir):
        fpath = os.path.join(img_dir, f)
        with open(fpath, 'rb') as fh:
            h = hashlib.md5(fh.read()).hexdigest()
        hash_map.setdefault(h, []).append((img_dir, f))

# 2. 找出跨文章出现的重复图片
dup_hashes = {h: files for h, files in hash_map.items() if len(files) >= 2}

# 3. 按出现频率排序，高频 = 模板
dup_by_count = {h: len(files) for h, files in dup_hashes.items()}
sorted_dups = sorted(dup_by_count.items(), key=lambda x: -x[1])
#   出现 70+ 次：肯定模板（微信引导 GIF）
#   出现 30-69 次：大概率模板（可能的 QR 码/装饰图）
#   出现 10-29 次：存疑（可能是复用技术图）
#   出现 2-9 次：可能是跨文章引用的相同技术图，保留

# 4. 删除标准：出现 30+ 次的全部删除
#   同时清理 article.md 中对其的引用
template_hashes = [h for h, c in dup_by_count.items() if c >= 30]
for h in template_hashes:
    for img_dir, fname in hash_map[h]:
        os.remove(os.path.join(base_dir, img_dir, fname))
        # 同步清理 article.md 引用
        ...
```

### 特征规律（微信公众号）

| MD5 类型 | 文件特征 | 出现频率 | 判断 |
|----------|---------|---------|------|
| `68KB GIF` | 同引导关注模板 | 130/447 篇 | 🗑️ 删 |
| `59KB GIF` | 同引导分享模板 | 133/447 篇 | 🗑️ 删 |
| `97KB GIF` | 同知识星球迷你广告 | 121/447 篇 | 🗑️ 删 |
| `37KB PNG` | 同二维码模板 | 81/447 篇 | 🗑️ 删 |
| `475KB GIF` | 同大尺寸动画 | 76/447 篇 | 🗑️ 删 |
| `45KB GIF` | 同引导图 | 45/447 篇 | 🗑️ 删 |

其他出现在 2-9 篇的技术图（相同对话框截图、标准操作界面）→ 保留。

---

## 知识领域覆盖分析

清洗后对知识库做关键词扫描，了解覆盖了哪些领域、缺少哪些：

```python
from collections import Counter

keyword_groups = {
    '焊线工艺': [r'焊线|bond', r'线弧|loop|PSA|PSL'],
    '报警/故障排查': [r'报警|alarm', r'故障|报错|排查|消解'],
    'SECS/GEM/通信': [r'SECS|GEMS|HSMS|通信|协议'],
    '参数配置': [r'参数|parameter|RPM|PBI|MHS'],
    '校准/对位': [r'校准|calibrat|PRS|十字线'],
    # ... 更多领域
}

all_terms = Counter()
for article in articles:
    for group, patterns in keyword_groups.items():
        for pat in patterns:
            matches = re.findall(pat, content, re.IGNORECASE)
            if matches:
                all_terms[group] += len(matches)
```

结果示例 — 发现 SECS/GEM 仅命中 1 次，确认该领域是空白，需要用户专业知识补充。
