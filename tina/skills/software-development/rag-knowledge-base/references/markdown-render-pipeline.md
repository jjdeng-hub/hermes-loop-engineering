# Markdown 渲染 5 步管道

全文见 `index.html` 的 `renderMsg()` 函数。以下是各步关键正则和代码：

## Step 1: 保护 code 块

```javascript
const codeBlocks = [];
// 围栏代码块
html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (m, lang, code) => {
  const escaped = code.replace(/</g,'&lt;').replace(/>/g,'&gt;');
  codeBlocks.push(`<div class="code-wrapper"><pre><code>${escaped}</code></pre><button class="copy-btn" onclick="copyCode(this)">📋 复制</button></div>`);
  return `%%CODEBLOCK_${codeBlocks.length-1}%%`;
});
// 内联代码
html = html.replace(/`([^`]+)`/g, (m, code) => {
  codeBlocks.push(`<code style="background:#1a1a2e;padding:2px 6px;border-radius:3px;font-size:13px">${code.replace(/</g,'&lt;').replace(/>/g,'&gt;')}</code>`);
  return `%%CODEBLOCK_${codeBlocks.length-1}%%`;
});
```

## Step 2: 转义 HTML

```javascript
html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
```

## Step 3: Markdown → HTML

```javascript
// 标题
html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
// 粗体+斜体组合 ***text***
html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
// 粗体 **text**
html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
// 斜体 *text*  — 必须在粗体之后
html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
// 无序列表
html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
// 有序列表
html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');
// 连续 li 包装为 ul
html = html.replace(/((?:<li[^>]*>.*?<\/li>\n?)+)/g, '<ul>$1</ul>');
// 水平线
html = html.replace(/^---$/gm, '<hr>');
// 换行
html = html.replace(/\n/g, '<br>');
```

## Step 4: 恢复 code 块

```javascript
html = html.replace(/%%CODEBLOCK_(\d+)%%/g, (m, i) => codeBlocks[parseInt(i)] || '');
```

## Step 5: 后处理

```javascript
// 来源链接化
html = html.replace(/📎 参考文档: (.+?)(?:<br>|$)/g, (m, files) => {
  const links = files.split(/, ?/).map(f =>
    `<span class="source-link" onclick="viewSource('${f.trim()}')">${f.trim()}</span>`
  ).join(', ');
  return `📎 参考文档: ${links}`;
});

// 内联图片
html = html.replace(/\[img:([^\]]+)\]/gi, (m, src) => {
  const ext = src.split('.').pop().toLowerCase();
  if (!['png','jpg','jpeg','gif','webp'].includes(ext)) return m;
  return `<br><img src="data/${src}" class="msg-img" onclick="this.classList.toggle('zoomed')" loading="lazy" onerror="this.style.display='none'"><br>`;
});
```

## ⚠️ 重要

- **顺序不可颠倒**：先保护 code，再转义，再 MD→HTML，最后恢复 code
- **正则 `[^\]]+`** 支持中文文件名（而非 `[\w.\/-]+`）
- `.msg-bubble` 不要 `white-space: pre-wrap`——与 `<br>` 冲突
