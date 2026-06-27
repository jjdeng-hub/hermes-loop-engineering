---
name: rag-development
description: RAG (Retrieval-Augmented Generation) 项目搭建与开发 — LangChain + Chroma + DeepSeek，含国内网络适配方案和备用检索策略
version: 1.0.0
---

# RAG Development

## 触发条件
- 搭建 RAG 知识库/问答系统
- 用 LangChain + Chroma 做本地向量检索
- 用 DeepSeek/通义千问等国内 LLM API 做 RAG
- 需要"先用轻量版跑通，再升级语义版"的开发节奏

## 技术栈
- **LLM**: DeepSeek (`deepseek-chat`，OpenAI 兼容 API)
- **编排**: LangChain + langchain-openai
- **向量库**: Chroma (本地持久化)
- **Embedding**: `BAAI/bge-small-zh-v1.5` (通过 sentence-transformers)
- **环境**: WSL / 国内网络

## 项目结构模板

```
project/
├── .env                  # DEEPSEEK_API_KEY
├── run.sh                # 启动脚本 (venv Python 完整路径)
├── rag_agent.py          # 完整版: Chroma + HuggingFace Embedding
├── rag_fallback.py       # 备用版: 关键词检索，零重依赖
├── demo_day1.py          # 演示脚本 (引用 rag_agent)
├── demo_fallback.py      # 演示脚本 (引用 rag_fallback)
└── chroma_db/            # 向量库存储 (自动生成)
```

## 双轨开发策略

### 备用版 (rag_fallback.py) — 先跑通
- **检索方式**: 纯关键词匹配（`_keyword_search`）
- **依赖**: 仅 `langchain-openai` + `langchain-community`
- **优点**: 秒启动，零 Embedding 模型下载
- **适用**: Day 1 验证想法、API 连通性测试、快速 Demo

### 完整版 (rag_agent.py) — 后升级
- **检索方式**: Chroma 向量库 + BGE 中文 Embedding
- **依赖**: + `sentence-transformers` (+ torch ~500MB)
- **优点**: 语义搜索，"线夹关不上" 能命中 "闭合超时"
- **适用**: 正式版本，部署后长期使用

## 核心代码模式

### .env 加载 (不依赖 python-dotenv)

```python
import os
from pathlib import Path

def _load_env():
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

_load_env()
```

### DeepSeek LLM 初始化

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com/v1",
    temperature=0.1,    # 知识检索类任务压低温度
    max_tokens=2048,
)
```

### Prompt 模板 (排查类任务)

```python
prompt = f"""你是一个[领域]专家。请基于以下知识库内容回答用户的问题。

【知识库内容】
{context}

【用户问题】
{question}

【回答要求】
1. 先给出直接结论
2. 列出可能的排查步骤（按优先级排序）
3. 如果匹配到代码/编号，明确列出"""
```

## 已知坑

| 坑 | 现象 | 解决 |
|---|---|---|
| `langchain.text_splitter` 导入超时 | 卡住 10s+ | 手写 `_split_text()` 函数 |
| `python-dotenv` 用户终端找不到 | `ModuleNotFoundError` | 直接 `Path.read_text()` 解析 .env |
| 用户 `python3` 找不到 venv 包 | 各种 `ModuleNotFoundError` | 用完整 venv Python 路径 |
| HuggingFace 下载被墙 | `RuntimeError: Cannot send a request` | `export HF_ENDPOINT=https://hf-mirror.com`，必须在 import 前设置 |
| Ollama 下载在 WSL 被限速 | curl 到 ollama.com 超时 | 在 Windows 宿主机安装 Ollama，WSL 通过 `localhost:11434` 连接 |
| Chroma metadata 类型报错 | Pyright `list[dict]` vs `Metadata` | 忽略——Pyright 误报，运行正常 |

## 企业部署：云端 → 本地迁移

同一套 Chroma + BGE + FastAPI 代码，只改 LLM 连接即可从开发切到生产：

```python
# 开发（云端 DeepSeek）
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com/v1", api_key=sk)

# 生产（本地 Ollama）
llm = ChatOpenAI(model="qwen2.5:7b", base_url="http://localhost:11434/v1", api_key="ollama")
```

- Qwen2.5 7B Q4: ~4.5GB RAM，16GB 办公电脑可跑
- 数据不出厂，满足工厂安全要求
- 详见 `rag-agent-development` skill（更完整的 Web UI + 语义搜索指南）

## 启动脚本 (run.sh)

```bash
#!/bin/bash
cd /path/to/project && ~/.hermes/hermes-agent/venv/bin/python3 demo_fallback.py
```

`chmod +x run.sh` 后用户一键启动，无需了解 venv。

## 参考
- DeepSeek API: https://platform.deepseek.com
- BGE Embedding: https://huggingface.co/BAAI/bge-small-zh-v1.5
