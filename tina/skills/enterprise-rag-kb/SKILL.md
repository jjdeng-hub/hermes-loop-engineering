---
name: enterprise-rag-kb
description: 企业级 RAG 知识库搭建 — Chroma + BGE + FastAPI，自动目录扫描、来源溯源、Ollama/DeepSeek 双引擎、Docker 部署
version: 1.0.0
category: devops
---

# enterprise-rag-kb — 企业级 RAG 知识库

## 触发条件
- 用户需要搭建企业/团队知识库检索系统
- 将 PDF/Word/Excel/TXT 等文档自动索引为可查询的 RAG 系统
- 需要离线部署（数据不出公司）、多格式文档支持、来源溯源
- 需要 Docker 化部署方案

## 架构

```
WATCH_DIR (监控目录) → 自动扫描 → 文件解析 → BGE Embedding → ChromaDB
                                                                    ↓
用户浏览器 (前端 :3000) → FastAPI (:8000) → 语义搜索 → DeepSeek/Ollama → 回答+来源
```

## 核心技术选型

| 组件 | 选项 | 说明 |
|---|---|---|
| 向量库 | ChromaDB (本地) | 零配置，Python 原生，持久化 |
| Embedding | BAAI/bge-small-zh-v1.5 | 中文语义，384 维，CPU 可跑，~100MB |
| LLM (云端) | DeepSeek Chat | 便宜，OpenAI 兼容 |
| LLM (本地) | Ollama + Qwen2.5:7b | 数据不出厂，需 4.5GB 内存 |
| 文件解析 | pypdf + python-docx + openpyxl | PDF/Word/Excel |
| 前端 | 独立 HTML (Python http.server) | 前后端分离，:3000 + :8000 |

## 项目结构

```
rag-agent/
├── api.py              # FastAPI 后端：扫描/鉴权/查询
├── rag_agent.py        # ChromaRAG 类：embedding + ChromaDB + LLM
├── index.html          # 前端界面（独立服务）
├── demo_data.txt       # 演示数据（Ball Bonder 报警代码）
├── data/               # WATCH_DIR：放文档自动索引
├── chroma_db/          # ChromaDB 持久化
├── Dockerfile
├── docker-compose.yml
├── start.sh            # 本地启动脚本
└── .env                # DEEPSEEK_API_KEY + LLM_PROVIDER
```

## 关键实现细节

### 1. 自动目录扫描

```python
WATCH_DIR = Path(os.getenv("WATCH_DIR", str(BASE_DIR / "data")))
# 启动时全量扫描，后台线程每 30s 增量扫描
# 用 MD5 检测文件变更，已索引的未变文件跳过
# 已删除文件自动从索引中移除
```

### 2. 双 LLM 引擎切换

```python
# .env 加一行：
# LLM_PROVIDER=ollama  # 切本地
# LLM_PROVIDER=deepseek  # 切云端

provider = os.getenv("LLM_PROVIDER", "deepseek").lower()
if provider == "ollama":
    llm = ChatOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
else:
    llm = ChatOpenAI(base_url="https://api.deepseek.com/v1", api_key=os.getenv("DEEPSEEK_API_KEY"))
```

### 3. 来源溯源

查询时从 ChromaDB 的 metadatas 中提取 `source` 字段，拼入 LLM prompt 上下文，并在回答末尾强制附加来源清单：

```python
sources = list(dict.fromkeys(m.get("source", "未知") for m in metas if m))
return f"{response.content}\n\n📎 参考文档: {', '.join(sources)}"
```

### 4. 前后端分离

- 后端 FastAPI 纯 API，不托管静态文件
- 前端 `python3 -m http.server 3000` 独立服务
- 前端 fetch 调用 `localhost:8000` 的 API

### 5. 鉴权

- 启动时生成/读取 `RAG_TOKEN` 环境变量
- 所有 API 需 `Authorization: Bearer *** - 前端 localStorage 存储令牌，登录弹窗输入

### 6. 国内网络注意事项

```python
# HuggingFace 被墙，必须设置镜像
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# Ollama 下载在 WSL 终端可能超时
# 推荐在 Windows 上装 Ollama，WSL 通过 localhost:11434 连接
```

## 前端设计规范（用户偏好）

- 暗色主题：`#080b12` 底 + `#0f1219` 面板 + `#161b25` 卡片
- 侧边栏：文件列表 + 扫描状态指示 + 统计数据
- 主区域：聊天气泡 + 输入框 + 欢迎页（含建议问题）
- 登录弹窗：令牌输入 → 进入系统
- 字体：PingFang SC / Microsoft YaHei
- 圆角：10px 主 / 6px 小
- 重点色：`#4f6ef7`（蓝色系）
- 成功色：`#2dd4bf`（青色）
- 前端必须「高级」——不朴素

## Docker 部署

```bash
# 本地模型模式（含 Ollama）
docker-compose --profile local up -d

# 云端 API 模式（仅 RAG 服务）
LLM_PROVIDER=deepseek DEEPSEEK_API_KEY=*** docker-compose up -d
```

## 文件格式支持

优先级：PDF > Word(docx) > Excel(xlsx) > TXT/MD/CSV/LOG
图表内容不解析，通过来源溯源引导用户查看原文件。

## 内存要求

- 完整版（BGE + Ollama + Chroma）：建议 8GB+，15GB 舒适
- 仅 BGE + Chroma + DeepSeek API：2GB 即可
- BGE 模型首次下载 ~100MB，需 HF 镜像

### 7. 前端来源可点击

用户点击回答底部的 `📎 参考文档: xxx.txt` 可查看原文。后端暴露 `/api/source?file=xxx` 端点：

```python
# rag_agent.py — ChromaRAG 新增方法
def get_chunks_by_source(self, filename: str) -> list[str]:
    results = self.collection.get(where={"source": filename})
    return results["documents"] if results and results["documents"] else []

# api.py — 新增端点
@app.get("/api/source")
def api_source(file: str = ""):
    chunks = get_rag().get_chunks_by_source(file)
    return {"success": True, "data": {"filename": file, "chunks": chunks, "count": len(chunks)}}
```

前端：`renderMsg()` 将 `📎 参考文档: xxx.txt` 转为 `<span class="source-link" onclick="viewSource('xxx.txt')">`，点击弹出 Modal 展示所有知识块。侧边栏文件列表同样可点击。

### 8. 前端多会话管理

侧边栏会话列表 + `+ 新对话` 按钮。数据存 localStorage (`rag_sessions`)：

```javascript
let sessions = JSON.parse(localStorage.getItem('rag_sessions') || '[]');
let activeSessionId = localStorage.getItem('rag_activeSession') || '';
// sessions: [{id, title, messages: [{role, content}], createdAt}, ...]
```

切换会话时 `askQuestion()` 传 `activeSessionId` 给后端，后端 `rag_agent.py` 按 session_id 维护独立对话历史。会话标题自动取第一条提问前 20 字。

### 9. 前端 Markdown 渲染 + 代码复制

`renderMsg()` 五步流水线：
1. 保护 code 块（`\`\`\`` 和 `` ` ``）→ 占位符
2. HTML 转义
3. Markdown → HTML（`**粗体**` `*斜体*` `# 标题` `- 列表` 等）
4. 恢复 code 块（加上 `.code-wrapper` + `.copy-btn`）
5. 来源链接 → 可点击
6. 内联图片 `[img:xxx]` → `<img>`

```javascript
// 代码复制
function copyCode(btn) {
  const code = btn.parentElement.querySelector('code').textContent;
  navigator.clipboard.writeText(code);
}
```

`.msg-bubble` 不能设 `white-space: pre-wrap`（与 HTML 渲染冲突导致双倍换行）。HTMLL 渲染用 `<br>` 替代 `\n`。

## VPS 部署决策框架

- **不把 LLM 模型放 VPS**（GPU 太贵），用 DeepSeek API 做推理
- **VPS 只跑 FastAPI + ChromaDB + 前端 + 爬虫**，2GB 内存够了
- **Hermes 不搬**——继续在本地 WSL，SSH 管理 VPS
- 国内访问优先选 RackNerd LA DC-02 机房（$18.66/年 2.5GB），或 CloudCone DC1/DC2（$14.49/年 2GB 但网络不稳）
- 512MB/1GB 机型不够（ChromaDB + BGE + Python Web 基础吃 800MB+）

### 10. 流式输出 (Streaming)

后端：
```python
@app.post("/api/query/stream")
def api_query_stream(req: QueryRequest):
    def generate():
        for token in rag.stream(req.question):
            yield token
    return StreamingResponse(generate(), media_type="text/plain")
```

前端：
```javascript
const reader = response.body.getReader();
while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    bubble.innerHTML += decoder.decode(value, {stream: true});
}
```

### 11. 置信度评分

从 ChromaDB 查询结果的 `distances` 计算：
- 余弦距离 d → 相似度 = max(0, 1 - d/2)
- 置信度 = top1_sim × 0.6 + avg_topk_sim × 0.4
- 距离 0 = 完全匹配 (100%)，距离 2 = 完全不相关 (0%)

### 12. 多轮对话

- ChromaRAG 内部维护 `sessions: dict[str, list[(q,a)]]`
- `_build_prompt()` 注入最近 6 轮对话历史
- 前端生成固定 session_id，每次请求携带
- 切换会话时 `clearChat()` → `loadActiveSession()` 重放消息

### 企业部署清单
1. 设固定 RAG_TOKEN（不要随机生成）
2. 配置 WATCH_DIR 指向企业共享文件夹
3. 确认 LLM_PROVIDER=ollama（数据不出厂）
4. 拔网线测试全流程
5. 对接企业 LDAP/AD（如果需要）

详细实现参考：[references/rag-core-patterns.md](references/rag-core-patterns.md) 和 [references/enterprise-deployment.md](references/enterprise-deployment.md)。

## 参考

- BGE 模型：https://hf-mirror.com/BAAI/bge-small-zh-v1.5
- Ollama：https://ollama.com
- DeepSeek API：https://platform.deepseek.com
