---
name: rag-rich-content-rendering
description: RAG 系统中内联富媒体内容（图片、表格）的渲染方案 — 知识库标记语法、前端正则解析、检索参数调优、LLM prompt 指令的四层对齐。
triggers:
  - "图片在回答里不显示"
  - "RAG 怎么带图"
  - "markdown 图片 RAG"
  - "知识库配图"
  - "回答里嵌入图片"
  - "[img:"
allowed-tools: Bash, Read, Write, Edit, Grep
---

# RAG 富媒体内联渲染

> 核心原则：**标记语法 → 检索覆盖 → LLM 保留 → 前端渲染，四层必须全部对齐，缺一不可。**

---

## 1. 知识库标记语法

在源文档中用统一标记内联图片：

```
步骤6：将M3内六角扳手插入调节螺丝处（如下图 [img:images/step6_tool.png]所示）。
```

**规则：**
- 格式：`[img:相对路径]`
- 图片紧跟引用文本，**不要**放在文件末尾独立"图片链接"区
- 路径相对于前端 HTTP 服务的根目录（如 `data/images/xxx.png`）
- 支持扩展名：png, jpg, jpeg, gif, webp

---

## 2. Chunk 策略 — 确保图片块被检索到

❌ **常见陷阱**：图片标记和引用它的文本被 chunk 边界切开，导致 RAG 只命中文本块、漏掉图片块。

**症状：** 回答中有"如下图所示"但图不显示

**原因排查（SQLite 直查 ChromaDB）：**
```sql
SELECT em.string_value, em2.string_value as source
FROM embedding_metadata em
JOIN embedding_metadata em2 ON em.id = em2.id AND em2.key = 'source'
WHERE em.key = 'chroma:document' AND em.string_value LIKE '%[img:%'
```

**修复手段（按优先级）：**

| 优先级 | 手段 | 效果 |
|--------|------|------|
| 1 | 增大 `top_k`（如 4→6） | 更多候选块进入上下文，覆盖图片块 |
| 2 | 减小 chunk_size（如 500→300） | 减少单块覆盖范围，降低切分风险 |
| 3 | 增大 chunk_overlap（如 50→100） | 滑动窗口更大，图片块被多份复制 |
| 4 | 数据预处理：图片紧跟引用文本 | 结构性保证不分离 |

**验证：** 查询后检查 LLM 的 `【知识库】` 上下文是否包含 `[img:` 标签。

---

## 3. LLM Prompt 指令

❌ **常见陷阱**：LLM 看到 `[img:...]` 会当作"标记语法"自动省略。

**必须在 System Prompt 末尾显式要求保留：**

```
⚠️ 重要：知识库中的 [img:图片路径] 标签必须原样复制到回答中，
放在对应段落后，不要删除或改写。
```

**验证：** 对已知含图文档提问，检查回答原始内容是否包含 `[img:` 字符串。

---

## 4. 前端渲染正则

❌ **常见陷阱**：用 `[\w.\/-]+` 匹配文件名，中文和特殊字符被跳过。

**正确写法：**

```javascript
function renderMsg(html) {
  return html.replace(/\[img:([^\]]+)\]/gi, (m, src) => {
    const ext = src.split('.').pop().toLowerCase();
    if (!['png','jpg','jpeg','gif','webp'].includes(ext)) return m;
    return `<br><img src="data/${src}" class="msg-img"
      onclick="this.classList.toggle('zoomed')" loading="lazy"
      onerror="this.style.display='none'"><br>`;
  });
}
```

**要点：**
- 用 `[^\]]+` 而非 `[\w.\/-]+` — 支持中文文件名
- 扩展名白名单校验 — 防止非图片内容被当图片渲染
- `onerror` 兜底 — 图片不存在时静默隐藏
- `loading="lazy"` — 多图时不阻塞页面

**CSS 配套：**
```css
.msg-img { max-width: 100%; max-height: 300px; border-radius: 6px;
  cursor: pointer; margin: 8px 0; border: 1px solid var(--border); }
.msg-img:hover { border-color: var(--accent); }
.msg-img.zoomed { position: fixed; top: 50%; left: 50%;
  transform: translate(-50%,-50%); z-index: 2000;
  max-width: 90vw; max-height: 90vh; border: none; }
```

---

## 5. 完整调试清单

当"图片不显示"时，按顺序排查：

```
□ 1. 数据层：ChromaDB 中是否有含 [img:] 的 chunk？
     → SQLite 查询 embedding_metadata，确认标记存在
□ 2. 检索层：含图 chunk 是否在 top_k 结果中？
     → 增大 top_k 或调小 chunk_size，验证检索结果
□ 3. LLM 层：回答原文是否包含 [img:] 标签？
     → 抓取 /api/query 返回的 data 字段，搜索 "[img:"
□ 4. 渲染层：前端正则是否匹配文件名？
     → 检查正则是否用了 [^\]]+ 而非 [\w.\/-]+
□ 5. 资源层：图片 URL 是否可访问？
     → curl 直接请求图片路径，确认 HTTP 200
```
