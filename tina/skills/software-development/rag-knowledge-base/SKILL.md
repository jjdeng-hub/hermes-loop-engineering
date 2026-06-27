---
name: rag-knowledge-base
description: 构建本地 RAG 知识库系统 — Chroma + BGE 语义搜索 + FastAPI 后端 + Web 界面，支持云端/本地 LLM 切换和企业化部署（文件上传、鉴权、Docker）
version: 1.0.0
---

# RAG 知识库系统搭建

## 触发条件
- 用户要搭建知识库问答系统（RAG）
- 需要文档检索 + LLM 回答的本地应用
- 需要将知识库打包为企业可部署的系统
- 涉及 Chroma / LangChain / BGE Embedding / Ollama

## 架构

```
用户上传文件 → 文本解析 → 切分 → BGE 向量化 → Chroma 存储
用户提问 → BGE 向量化 → Chroma 语义搜索 → LLM 回答
```

## 关键技术选型

### LLM 层
- **云端**：DeepSeek（OpenAI 兼容 API，便宜）
- **本地**：Ollama + Qwen2.5:7b（数据不出厂，适合企业）
- 切换方式：`LLM_PROVIDER` 环境变量，一行配置切换

### Embedding 层
- 模型：`BAAI/bge-small-zh-v1.5`（384 维，中文效果好）
- 国内镜像：`HF_ENDPOINT=https://hf-mirror.com`（必须设置！）

### 向量库
- Chroma（本地持久化，零配置，Python 原生）

## 项目结构

```
rag-agent/
├── rag_agent.py      # ChromaRAG 类（核心引擎）
├── api.py             # FastAPI 后端（上传/查询/鉴权）
├── index.html          # 单页面前端（聊天界面）
├── Dockerfile          # 容器化
├── docker-compose.yml  # 一键部署（含 Ollama）
├── start.sh            # 本地启动脚本
└── demo_data.txt       # 演示数据
```

## RAG 图文并茂：内联图片展示

当知识源包含图片（如公众号文章配图），需要把图片展现在 RAG 回答的对应段落位置。

**数据流**：`源文章图片 → 下载到本地 → 正文插入 [img:路径] → RAG 检索 → LLM 回答保留 [img:] → 前端渲染 <img>`

详见 [参考文档](references/image-rendering-pipeline.md)。

### 图片不显示的排查清单（按顺序）

| # | 检查点 | 常见问题 | 修复 |
|---|--------|---------|------|
| ① | 前端正则 | `[\w.\/-]+` 不匹配中文文件名 | 改为 `[^\]]+`，再加扩展名校验 |
| ② | 检索覆盖 | `top_k` 太小，图片 chunk 未被检索到 | 增大 `top_k`（如 4→6） |
| ③ | LLM 保留 | LLM 看到 `[img:]` 但自动省略 | system prompt 加"必须原样复制 [img:...] 标签" |

## 常见坑

| 坑 | 现象 | 解决 |
|---|---|---|
| HuggingFace 超时 | 下载模型卡住 | 设 `HF_ENDPOINT=https://hf-mirror.com` |
| langchain text splitter 导入慢 | 卡 5 秒以上 | 手写 `split_text()`，200 行纯 Python |
| python-dotenv 缺失 | `ModuleNotFoundError: dotenv` | 手写 `_load_env()` 读 .env 文件 |
| pip install 被误判为服务 | terminal 工具拒绝 | 用 `background=true` + `notify_on_complete=true` |
| Ollama 下载慢/被墙 | WSL 内 curl 超时 | 从 Windows 浏览器下载安装包；WSL 内可调 `ollama.exe`（路径 `C:\Users\<user>\AppData\Local\Programs\Ollama\ollama.exe`，WSL 映射为 `/mnt/c/Users/<user>/AppData/Local/Programs/Ollama/ollama.exe`） |
| Ollama 拉模型慢/被墙 | `ollama pull` 极慢 | 从 ModelScope 下载 Qwen2.5 GGUF 文件（国内满速），再用 `ollama create` 导入 |
| WSL 连不上 Windows Ollama | `curl localhost:11434` 连接拒绝/超时 | Ollama Windows 默认只监听 127.0.0.1。在 Windows PowerShell（管理员）执行 `$env:OLLAMA_HOST=\"0.0.0.0\"` 然后重启 Ollama。或永久设置：Windows 系统环境变量 `OLLAMA_HOST=0.0.0.0`，再重启 Ollama。详见 [references/ollama-wsl-connectivity.md] |
| 扫描器不跟 symlink | 子目录文件被忽略 | `iterdir()`→`rglob('*')`，详见上方「子目录和 Symlink 扫描」 |
| 图片不显示 | 回答只有文字没有图 | 按上方"图片不显示排查清单"①②③依次排查 |

## 文件解析

支持格式：PDF（pypdf）、Word（python-docx）、Excel（openpyxl）、纯文本

解析后用 `split_text()` 切分，500 字符/块，50 字符重叠。

### 英文 PDF → 中文问答

pypdf 可直接提取英文 PDF 文字，无需额外处理。LLM（DeepSeek）在接收到英文上下文 + 中文问题时，自然给出中文回答。不需要单独的翻译步骤。

实测示例：丢入英文 `test_alarms_en.pdf` → 问"ALM-1001是什么，怎么修？" → 4 秒返回中文排查步骤 + 报警代码表。

### 子目录和 Symlink 扫描

❌ **常见陷阱**：`scanner` 用 `WATCH_DIR.iterdir()` 只扫顶层，不跟随 symlink 到子目录。

**修复**：改为 `WATCH_DIR.rglob('*')`，递归扫描所有子目录：

```python
files = sorted([
    f for f in WATCH_DIR.rglob('*') 
    if f.is_file() and f.suffix.lower() in SUPPORTED_EXT
])
```

适用场景：用户将 `~/rag-agent/data/` 通过 symlink 指向 `桌面/rag-data/`，子目录中的文件需要被自动发现。

## 数据导入前的审计流程（必须先做，不要跳步）

❌ **常见错误**：拿到数据目录直接写导入脚本灌库，发现图片缺失、格式不匹配、重复内容，浪费大量时间。

**正确步骤：**

### 第一步：盘清数据目录结构

```bash
# 总数统计
ls rag-data/ | wc -l                         # 总条目
ls rag-data/*.txt 2>/dev/null | wc -l         # 文本文件数
ls -d rag-data/*_imgs/ 2>/dev/null | wc -l   # 图片目录数
```

### 第二步：检查文本文件是否含图片引用

```bash
# 抽 3-5 篇代表性文章检查
grep -c '\[img' rag-data/xxx.txt            # [img:path] 格式
grep -c '!\[\](' rag-data/xxx.txt           # Markdown 图片格式
```

### 第三步：检查 _imgs 子目录结构

常见的 twin 结构（尤其中文公众号爬取）：

```
rag-data/
├── 854相关报警合集.txt              # 纯文本，无图片
├── 854相关报警合集_imgs/
│   ├── article.md                   # 含图片的完整 Markdown
│   ├── img_001.jpg
│   └── img_002.jpg
```

**关键判断**：如果 .txt 无图片引用但 _imgs 目录下有 article.md→以 article.md 为数据源，不是 .txt。

### 第四步：检查多源重复

多个公众号来源的文章可能有重叠（按标题+首段模糊匹配）。导入前做一次去重标记。

### 第五步：决定导入策略

| 数据形态 | 推荐导入方式 |
|:---------|:-----------|
| 全文本（无图片） | 直接通过 WATCH_DIR 扫描或 API upload |
| txt + _imgs/article.md | 导入 article.md，重写图片为绝对路径 |
| 纯 Markdown 文件 | 直接导入，注意[图片路径需可访问](#) |

---

## 交互设计偏好

- **不要预编脚本式 Demo**：用户要的是交互式查询（输入问题→得答案），不是自动跑 5 个预定义查询
- **要做 Web 界面**：纯 HTML 单页面，不需要 Next.js 脚手架
- **界面布局**：左侧边栏（文件上传+管理）+ 右侧聊天气泡
- **前端技术**：纯 HTML/CSS/JS，fetch 调 FastAPI，零框架依赖

## 文件传输（公司→家庭）

公司电脑与家庭电脑隔离时的文件流转方案，见 [file-transport-patterns.md](references/file-transport-patterns.md)。

## 扩展参考（详细专题）

以下专题文档从 RAG 技能家族合并而来，涵盖开发、部署、检索、UI 各层面的详细指南：

### 开发策略
- **[双轨开发策略](references/dual-track-development.md)** — 备用版（关键词检索，秒启动）→ 完整版（Chroma + BGE 语义搜索）的渐进开发方法
- **[Agent 开发指南](references/agent-development.md)** — Web UI、API 层、ChromaRAG 类、Dual LLM 切换的完整参考
- **[领域故障排查工作流](references/domain-troubleshooting.md)** — 从领域调研 → 模拟数据 → 关键词 MVP → 语义升级的企业部署路径

### 检索增强
- **[混合检索 (BM25 + 向量 + RRF)](references/hybrid-search.md)** — BM25 关键词 + BGE 向量语义的双引擎融合，解决精确匹配与模糊语义不可兼得的问题
- **[富媒体内联渲染](references/rich-content-rendering.md)** — RAG 回答中嵌入图片的四层对齐方案（标记语法 → 检索覆盖 → LLM 保留 → 前端渲染）

### 前端 UI
- **[聊天界面模式](references/chat-ui-patterns.md)** — Markdown 渲染 5 步管道、来源可点击、多会话管理、代码复制、流式输出
- **[Markdown 渲染管道](references/markdown-render-pipeline.md)** — 前端 Markdown → HTML 的详细正则实现
- **[ChromaDB 来源查询](references/chromadb-source-lookup.md)** — 后端来源溯源 API 实现

### 模板
- **[rag-agent-api.py](templates/rag-agent-api.py)** — FastAPI 后端模板
- **[rag-agent-engine.py](templates/rag-agent-engine.py)** — 最简 RAG 引擎（关键词检索 + DeepSeek）
- **[rag-agent-chroma.py](templates/rag-agent-chroma.py)** — 完整语义搜索引擎（Chroma + BGE + 双 LLM）
- **[rag-fallback.py](templates/rag-fallback.py)** — 关键词备用版模板（零重依赖）

### 工具参考
- **[LLM Provider 切换](references/llm-provider-switch.md)**
- **[Ollama WSL 连接](references/ollama-wsl-connectivity.md)**
- **[文本切分器](references/text-splitter.md)**
- **[图片渲染管道](references/image-rendering-pipeline.md)**
