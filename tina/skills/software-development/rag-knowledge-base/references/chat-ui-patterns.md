---
name: rag-chat-ui-patterns
description: RAG 知识库对话界面模式 — Markdown 渲染、来源可点击、多会话管理、代码复制、流式输出。适用于 FastAPI + 纯 HTML/JS 的聊天前端。
---

RAG 对话界面通用 UI 模式。当需要为 RAG/LLM 聊天构建或增强前端时使用。

## 触发条件
- 构建/修改 RAG 聊天界面（FastAPI 后端 + 纯前端）
- LLM 输出显示 `**`、`*`、`#` 等 Markdown 原始字符
- 需要来源溯源、多会话、代码复制等功能

## 核心模式

### 1. Markdown 渲染（5 步管道）

LLM 返回 Markdown，前端需逐级转换，**顺序不可颠倒**：

```
Step 1: 保护 code 块 → %%CODEBLOCK_N%% 占位（防止被后续正则破坏）
Step 2: 转义 HTML  → &lt; &gt; &amp;
Step 3: 转换 Markdown → 标题/粗体/斜体/列表/分隔线/换行
Step 4: 恢复 code 块 → 还原占位符
Step 5: 后处理       → 来源链接化、内联图片
```

关键正则参考 `references/markdown-render-pipeline.md`。

### 2. 来源可点击

**后端**：新增 `GET /api/source?file=xxx`，调用 `collection.get(where={"source": filename})` 返回全部 chunk。

**前端**：`renderMsg()` Step 5 中，将 `📎 参考文档: xxx.txt` 转为 `<span class="source-link" onclick="viewSource(...)">`。

**弹窗**：模态框展示文件所有 chunk，带序号分隔。

### 3. 多会话管理

- 会话数据存 `localStorage`：`{id, title, messages[{role, content}], createdAt}`
- 新建/切换/删除 → 更新 localStorage + 重绘侧边栏
- 提问时 `session_id` 传给后端 `/api/query/stream`，后端独立存储多轮历史
- 切换会话时 `clearChat()` → `loadActiveSession()` 重放消息
- `saveSessions()` 在每次消息收发后调用

### 4. 代码块复制

- 代码块生成时包裹 `<div class="code-wrapper"><pre><code>...</code></pre><button class="copy-btn">📋 复制</button></div>`
- 按钮默认 `opacity:0`，hover `.code-wrapper` 时显示
- `navigator.clipboard.writeText()` + 2 秒 "✅ 已复制" 反馈

### 5. CSS 注意事项

- `.msg-bubble` **不要** `white-space: pre-wrap`——和 Markdown `<br>` 冲突导致双倍换行
- 代码块用 `.code-wrapper` 包裹，`position:relative` 承载绝对定位的复制按钮

## 验锅

- `curl http://localhost:8000/api/source?file=中文文件名.txt` 返回 chunks
- `curl http://localhost:3000/` 返回 200
- 前端提问后 LLM 回答 `**粗体**` 渲染为粗体，`📎 参考文档` 可点击

## 参考文件

- `references/markdown-render-pipeline.md` — Markdown 渲染 5 步管道详细代码
