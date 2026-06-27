# RAG 图文并茂：内联图片展示流水线

## 总览

```
源文章图片 → download_images.py → data/images/*.png
                                        ↓
正文 "如下图 [img:images/xxx.png]"  ← 嵌入标记
                                        ↓
split_text() 切分 chunk                ← chunk 内包含 [img:]
                                        ↓
ChromaDB 存储                           ← 图片标记随文本入向量库
                                        ↓
RAG 检索 → LLM 回答                     ← system prompt 要求保留
                                        ↓
前端 renderMsg()                        ← 正则识别 → <img> 渲染
```

## 1. 数据准备：图片下载 + 内联标记

**关键原则**：`[img:]` 标记必须嵌入在引用它的段落后（同一 chunk），不要放在文件末尾。

```python
# download_images.py 核心逻辑
# 下载图片到 data/images/，然后在正文中替换：

body = body.replace(
    "如下图）", 
    f"如下图 [img:images/{article_name}_{i:02d}.png]）"
)
```

**文件名规范**：`{文章名}_{序号}.{ext}`，如 `KS_夹钳压板校准_01.png`。

## 2. 前端渲染：正则匹配 [img:...]

```javascript
// index.html renderMsg()
function renderMsg(html) {
  // ⚠️ 必须用 [^\]]+ 而非 [\w.\/-]+，因为中文文件名不匹配 \w
  return html.replace(/\[img:([^\]]+)\]/gi, (m, src) => {
    const ext = src.split('.').pop().toLowerCase();
    if (!['png','jpg','jpeg','gif','webp'].includes(ext)) return m;
    return `<br><img src="data/${src}" class="msg-img" 
      onclick="this.classList.toggle('zoomed')" 
      loading="lazy" onerror="this.style.display='none'"><br>`;
  });
}
```

CSS：
```css
.msg-img { 
  max-width: 100%; max-height: 300px; border-radius: 6px; 
  cursor: pointer; margin: 8px 0; border: 1px solid var(--border); 
}
.msg-img.zoomed { 
  position: fixed; top: 50%; left: 50%; 
  transform: translate(-50%, -50%); z-index: 2000;
  max-width: 90vw; max-height: 90vh; 
}
```

## 3. Prompt 工程：强制 LLM 保留标记

```python
# rag_agent.py _build_prompt() 末尾追加：
prompt += "\n⚠️ 重要：知识库中的 [img:图片路径] 标签必须原样复制到回答中，" \
          "放在对应段落后，不要删除或改写。"
```

**不加这句 → LLM 看到 `[img:...]` 会当 markup 省略掉**。

## 4. 检索覆盖：增大 top_k

```python
# api.py - 确保含图片的 chunk 被检索到
rag.query(req.question, k=6)  # 默认 4 不够，图片 chunk 可能语义匹配弱
```

## 5. 排查清单

图片不显示时，按顺序检查：

1. **数据端**：正文中是否有 `[img:images/xxx.png]`？ChromaDB chunk 里是否包含？
   ```python
   # 查 SQLite 确认
   SELECT string_value FROM embedding_metadata 
   WHERE key='chroma:document' AND string_value LIKE '%[img:%'
   ```

2. **前端正则**：`[\w.\/-]+` 能匹配中文文件名吗？→ 不行，换 `[^\]]+`
   
3. **LLM 输出**：回答中是否有 `[img:...]` 标签？→ 没有就是 prompt 没要求保留

4. **图片路径**：图片文件是否在 `$PROJECT_ROOT/data/images/` 下？前端 HTTP server 的 root 是否指向 `$PROJECT_ROOT/`？

## 常见陷阱

| 陷阱 | 现象 | 真相 |
|------|------|------|
| 图片放在文件末尾"图片链接"区 | LLM 回答不显示图 | chunk 切分时图片区与正文分离，检索时只命中正文 chunk |
| 文件名含中文（如 `焊线机_01.png`） | 控制台无报错但图片不显示 | `\w` 只匹配 `[a-zA-Z0-9_]` |
| `top_k=4` | 一些图的 chunk 没被检索 | 图片 chunk 的语义相似度可能不如纯文本 chunk |
| HTTP server root 不对 | 图片 404 | `http.server` 的 root 必须是 `rag-agent/`，图片 URL 是 `http://localhost:3000/data/images/xxx.png` |
