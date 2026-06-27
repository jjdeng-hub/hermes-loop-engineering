---
name: install-python-packages-cn
description: 在 WSL/Linux 国内网络环境下安装 Python 包的可靠方法，使用 uv + 清华镜像源解决 pip 超时问题
version: 1.0.0
---

# skill: install-python-packages-cn

## 触发条件
- 在 WSL/Linux 环境中安装 Python 包时遇到网络超时（files.pythonhosted.org 连接失败）
- pip install 失败，报错 `ReadTimeoutError` / `TLS connection error`
- 需要安装较大的 Python 包（如 dspy、litellm 等含大量依赖的项目）

## 环境前提
- WSL (Ubuntu) 环境
- 已安装 uv (`~/.local/bin/uv`)
- 目标 Python 版本 3.11+

## 操作步骤

### 1. 尝试常规 pip 安装（先试，失败则继续）
```bash
cd /path/to/project
pip install -e ".[dev]"
```
如果报错 `ReadTimeoutError` 或 `TLS connection was non-properly terminated`，继续下一步。

### 2. 使用 uv + 清华镜像源安装（推荐方案）
```bash
# 创建虚拟环境
uv venv .venv --python 3.11

# 使用清华镜像源安装（关键：--index-url 参数）
uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple -e ".[dev]"
```

**为什么有效：**
- uv 比 pip 快 10-100 倍，下载速度快很多
- 清华镜像源在国内网络环境下稳定
- `--index-url` 参数覆盖默认 PyPI 源

### 3. 验证安装
```bash
.venv/bin/python -c "import <package_name>; print('OK')"
```

### 4. 如果是 hermes-agent-self-evolution 这类可编辑安装
```bash
# 确保指向正确的 hermes-agent 仓库路径
export HERMES_AGENT_REPO=~/.hermes/hermes-agent

# 干跑验证
.venv/bin/python -m evolution.skills.evolve_skill --skill <skill_name> --dry-run
```

## 已知坑

| 坑 | 现象 | 解决 |
|---|---|---|
| pip 下载超时 | `ReadTimeoutError: HTTPSConnectionPool...` | 用 uv + 清华镜像 |
| uv --system 被拒绝 | `externally managed` 错误 | 不用 --system，创建 venv |
| 可编辑安装找不到模块 | `ModuleNotFoundError` | 检查 `.pth` 文件路径是否正确 |
| LiteLLM 模型价格表超时 | `Failed to fetch remote model cost map` | 可忽略，自动回退本地备份 |
| sentence-transformers 拉取巨量 CUDA 依赖 | 安装 `sentence-transformers` 时自动拉 torch (~500MB) + CUDA (~1GB)，清华源也可能超时 | 对于 RAG 项目，先用关键词检索做备用版（秒启动），语义版等网络好的时候再装 |
| **用户终端 python3 找不到 venv 里的包** | `ModuleNotFoundError: No module named 'langchain_openai'` — `uv pip install` 装到了 Hermes venv，但用户终端没激活该 venv | **不要指望用户激活 venv。** 创建 `run.sh` 用 venv 的完整 Python 路径：`~/.hermes/hermes-agent/venv/bin/python3 script.py` |
| **uv pip install 装到了 Hermes venv 而非项目 venv** | 项目目录下已有 `.venv/`，但 `uv pip install` 输出 `Using Python ... environment at: ~/.hermes/hermes-agent/venv`，包装到了全局而非项目本地 | 这是 uv 的默认行为——当前激活的 venv 优先于目录下的 `.venv`。解决：`~/.hermes/hermes-agent/venv/bin/python` 是运行时路径，验证包时用这个 Python；如果确实要装到项目 venv，用 `uv pip install --python .venv/bin/python ...` 显式指定 |
| **Hermes terminal 误判 pip install 为服务** | `uv pip install` 在 foreground 模式下被 terminal 工具拒绝，报 "This foreground command appears to start a long-lived server" | 改用 `background=true` + `notify_on_complete=true`。或用 `process(action='wait')` 等结果 |

## 交付给用户的启动脚本

当项目依赖装在 Hermes 全局 venv 时，用户终端 `python3` 可能找不到包。标准做法：

```bash
#!/bin/bash
cd /path/to/project && ~/.hermes/hermes-agent/venv/bin/python3 main.py
```

`chmod +x` 后用户直接 `./run.sh` 即可，无需了解 venv 机制。

## 分阶段安装策略（大项目）

当项目依赖包含 `sentence-transformers`、`torch`、`dspy` 等重型包时：
1. **先装轻量核心**：`uv pip install --index-url <mirror> langchain langchain-openai chromadb pypdf python-dotenv`
2. **后台装重包**：`uv pip install --index-url <mirror> "sentence-transformers>=3.0.0"` 放后台 (`background=true, notify_on_complete=true`)
3. **期间用备用方案**：先跑不依赖重包的备用版 Demo，不浪费时间等待

## 注意事项
- 安装 hermes-agent-self-evolution 需要 `HERMES_AGENT_REPO` 环境变量指向 hermes-agent 仓库
- 真正运行演化需要配置 `OPENAI_API_KEY`
- `--dry-run` 不需要 API key，适合先验证配置

## 参考
- 项目：https://github.com/NousResearch/hermes-agent-self-evolution
- 镜像源：https://pypi.tuna.tsinghua.edu.cn/simple