---
name: rag-domain-troubleshooting
description: 构建工业领域 RAG 故障排查系统 — 从领域调研、模拟数据到可演示 Demo 的完整工作流
version: 1.0.0
---

# RAG Domain Troubleshooting

## 触发条件
- 用户想用 RAG 解决某个专业领域的排查/检索问题（设备报警、医疗诊断、法律条文等）
- 用户有行业知识但没有整理好的数据
- 需要快速跑通一个可演示的 RAG Demo

## 核心原则

### 1. 先理解领域，再写代码
不要拿到需求就写 RAG 代码。先搞清楚：
- 用户在哪个行业、什么岗位
- 他接触的数据长什么样（报警代码表？维修手册？通信日志？）
- 谁会使用这个系统（客户工程师？内部同事？）

### 2. 总是先搭"关键词备用版"
`sentence-transformers` 会拉 500MB+ 的 PyTorch + CUDA 依赖，国内网络下可能下载 5-10 分钟。
**第一天永远先写关键词检索版本，秒级启动，当天看到效果。** 语义版第二天再升级。

### 3. 用用户自己的数据做 Demo
不要用通用数据。抽 5-10 条用户真实接触的信息（脱敏），这就是最好的 Demo 数据。
用户看到自己熟悉的报警代码被 AI 匹配到正确答案，比任何 PPT 都有说服力。

## 技术选型（国内环境）

| 组件 | 选择 | 原因 |
|---|---|---|
| LLM | DeepSeek (`deepseek-chat`) | 便宜（1元/百万token），OpenAI 兼容，中文好 |
| 向量库 | Chroma (本地) | 零配置，Python 原生，Demo 够用 |
| 检索（备用版）| 关键词匹配 | 秒启动，无外部依赖 |
| 检索（完整版）| BGE 中文 Embedding | 免费本地运行，中文语义检索最优 |
| 框架 | LangChain | 生态最全，但 Demo 可以只用最简子集 |

## 操作步骤

### Step 1: 领域调研
1. 搜索用户公司/行业的公开资料
2. 确认用户的具体岗位和日常接触的数据类型
3. 和他确认：数据长什么样？谁会用？什么场景下用？

### Step 2: 编写模拟数据
基于用户描述的数据格式，编写 5-15 条脱敏的 Demo 数据。格式要接近真实：
```
ALM-1001 | 线夹闭合超时
含义: ...
可能原因:
1. ...
排查步骤: 第一步... → 第二步...
```

### Step 3: 创建项目骨架
参考 `references/project-structure.md` 中的标准项目结构。

### Step 4: 先写备用版（关键词检索）
- 用 `RecursiveCharacterTextSplitter` 切分文本
- 内存存储 `[(chunk, metadata), ...]`
- 关键词交集打分检索
- DeepSeek 做最终回答生成

### Step 5: 跑通 Demo
用备用版跑 3-5 个查询，验证：
- 检索能命中相关内容
- LLM 能基于检索结果组织答案
- 答案格式符合预期（结论 + 排查步骤 + 报警代码映射）

### Step 6: 升级到完整版（语义检索）
- 安装 `sentence-transformers`
- 用 `BAAI/bge-small-zh-v1.5` 做本地 Embedding
- 替换关键词检索为 Chroma vector similarity search
- 对比检索质量提升

## 代码模板
参考 `templates/rag_fallback.py` — 可直接复制修改的备用版模板。

## 已知坑
- `sentence-transformers` 安装会拉 torch (507MB) + CUDA 库 (~1GB)，国内网络下可能超时。**先用备用版。**
- **HuggingFace 被墙**: BGE 模型首次加载失败 `RuntimeError: Cannot send a request` → 在 import 前 `os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"`
- DeepSeek 的 `ChatOpenAI` 参数名是 `openai_api_key` 和 `openai_api_base`，不是 `api_key`
- Chroma 的 `persist_directory` 必须是绝对路径，否则可能存到临时目录
- Chroma 的 embedding function 一旦设置不可更改 — 换 embedding 模型需要删库重建
- **Ollama 在 WSL 下载失败**: 在 Windows 宿主机装 Ollama，WSL 通过 `localhost:11434` 连接

## 企业部署路径

Demo → 语义升级 → 本地 LLM → Docker 打包：

```
Day 1-2: 关键词 Demo (DeepSeek API) → 跑通想法
Day 3: 语义搜索 (BGE + Chroma) → "线夹关不上"命中"闭合超时"
Week 2: 本地 LLM (Ollama + Qwen2.5 7B) → 数据不出厂
Week 3: Docker Compose → 一键部署到客户电脑
```

关键技术: 同一套 Chroma + BGE + FastAPI 代码，只换 LLM 连接即可。
详见 `rag-agent-development` skill 的 Dual LLM 章节。
