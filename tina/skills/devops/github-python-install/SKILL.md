---
name: github-python-install
description: Install Python projects from GitHub — handles network issues, uv vs pip, editable installs, and verification.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitHub, Python, Installation, Network, uv, pip, editable]
    related_skills: [github-auth]
---

# GitHub Python 项目安装技能

## 触发条件

当用户要求从 GitHub 克隆并安装 Python 项目时触发。

## 标准流程

### 1. 先确认项目存在

```bash
curl -s "https://api.github.com/repos/{owner}/{repo}" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f'Stars: {d.get(\"stargazers_count\",\"N/A\")}')
print(f'Desc: {d.get(\"description\",\"N/A\")}')
print(f'URL: {d.get(\"html_url\",\"N/A\")}')
"
```

如果找不到项目，搜索变体：
```bash
curl -s "https://api.github.com/search/repositories?q={keywords}&sort=stars&per_page=5"
```

### 2. 克隆仓库

```bash
cd ~/.hermes && git clone --depth 1 https://github.com/{owner}/{repo}.git
```

**注意：** 如果网络有问题（GnuTLS 错误），尝试：
- 先 `git clone` 失败，再重试
- 使用 `--depth 1` 减少下载量

**备选方案：GitHub API 逐个文件下载**（当 git clone 完全不可用时）

```python
import requests
import base64
import os

base_url = "https://api.github.com/repos/{owner}/{repo}/contents"
files_to_download = ["conf.py", "main.py", ...]  # 从 GitHub API 获取目录结构

for file_path in files_to_download:
    url = f"{base_url}/{file_path}"
    response = requests.get(url)
    data = response.json()
    content = base64.b64decode(data['content']).decode('utf-8')
    
    full_path = os.path.join(project_dir, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
```

**获取目录结构：**
```bash
curl -s "https://api.github.com/repos/{owner}/{repo}/contents"
```

### 3. 检查项目依赖数据库（MySQL/Redis）

### 3. 检查 pyproject.toml 或 setup.py

```bash
cat ~/.hermes/{repo}/pyproject.toml
```

确认依赖和安装方式。

### 3b. 处理数据库依赖（MySQL/Redis 无法安装时）

**检查项目是否依赖 MySQL/Redis：**
```bash
grep -r "pymysql\|mysql\|redis" requirements.txt
```

**如果无法安装 MySQL/Redis（无 sudo 权限），使用 SQLite 替代：**

```python
# 创建 SQLite 初始化脚本
import sqlite3

conn = sqlite3.connect('matrix.db')
cursor = conn.cursor()

# 创建与原 MySQL 表结构兼容的表
cursor.execute('''
    CREATE TABLE mx_account_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        queue_id INTEGER DEFAULT 0,
        uid INTEGER DEFAULT 0,
        account_id TEXT DEFAULT '',
        username TEXT DEFAULT '',
        avatar TEXT DEFAULT '',
        extend TEXT DEFAULT '',
        type INTEGER DEFAULT 0,
        status INTEGER DEFAULT 0,
        created_at INTEGER DEFAULT 0,
        updated_at INTEGER DEFAULT 0
    )
''')
conn.commit()
conn.close()
```

**修改配置文件**，将 MySQL 配置替换为 SQLite：
```python
# conf.py
SQLITE_CONF = {
    "database": "/path/to/matrix.db"
}
```

### 4. 安装依赖（网络问题处理）

**首选方案：uv + 清华镜像（最快最稳）**

```bash
cd ~/.hermes/{repo}
uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple -e ".[dev]"
```

**备选方案（如果 uv 不可用）：**

```bash
# 先创建 venv
uv venv .venv --python 3.11
source .venv/bin/activate
pip install -e ".[dev]"
```

**如果 pip 超时：**
- 使用清华镜像：`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e ".[dev]"`
- 或阿里云镜像：`pip install -i https://mirrors.aliyun.com/pypi/simple/ -e ".[dev]"`

### 5. 验证安装

```bash
# 检查模块能否导入
~/.hermes/hermes-agent/venv/bin/python -c "import {module}; print('OK')"

# 检查 CLI 命令
python -m {module.subcommand} --help
```

**Playwright 浏览器验证：**
```bash
# 安装 Chromium 浏览器
python3 -m playwright install chromium

# 运行测试脚本
python3 test_playwright.py
```

测试脚本示例：
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.xiaohongshu.com")
    print(f"✅ 页面加载成功：{page.title()}")
    browser.close()
```

### 6. 配置环境变量（如需要）

```bash
export HERMES_AGENT_REPO=~/.hermes/hermes-agent
export OPENAI_API_KEY=sk-xxx  # 如果需要调用 LLM
```

## 常见问题

### Q: pip 下载超时
**A:** 使用清华镜像 `https://pypi.tuna.tsinghua.edu.cn/simple`

### Q: uv 提示 externally managed
**A:** 不要加 `--system` 标志，或者创建独立 venv：
```bash
uv venv .venv
uv pip install -e ".[dev]"  # 自动使用 .venv
```

### Q: editable install 没生效
**A:** 检查 `.pth` 文件指向的路径是否正确，确认 Python 使用的是正确的 venv

### Q: 模块导入失败
**A:** 确认使用的是安装时的 Python 环境：
```bash
which python  # 应该是 venv 中的 python
```

## 经验教训

1. **uv 比 pip 快得多** — 优先使用 uv，尤其是国内网络环境
2. **清华镜像是必备** — 国内服务器必配，避免超时
3. **editable install 路径要匹配** — 如果项目依赖 hermes-agent，确保安装在 hermes-agent 的 venv 中
4. **先 dry-run 验证** — 安装后先用 `--dry-run` 或 `--help` 验证配置
5. **不要假设项目名** — 用户说的项目名可能不准确，先搜索确认
6. **git clone 超时 → GitHub API 下载** — 当 git clone 超时（国内网络），用 GitHub API 逐个文件下载
7. **MySQL/Redis 无法安装 → SQLite 替代** — 无 sudo 权限时，用 SQLite 替代 MySQL，用文件存储替代 Redis
8. **Playwright 浏览器需单独下载** — `playwright install chromium` 下载浏览器二进制文件
9. **项目结构分析** — 先用 GitHub API 获取目录结构，了解项目组成后再决定安装策略

## 示例：安装 hermes-agent-self-evolution

```bash
# 1. 确认项目
curl -s "https://api.github.com/repos/NousResearch/hermes-agent-self-evolution"

# 2. 克隆
cd ~/.hermes && git clone --depth 1 https://github.com/NousResearch/hermes-agent-self-evolution.git

# 3. 安装（使用 uv + 清华镜像）
cd ~/.hermes/hermes-agent-self-evolution
uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple -e ".[dev]"

# 4. 验证
~/.hermes/hermes-agent/venv/bin/python -m evolution.skills.evolve_skill --help

# 5. 配置
export HERMES_AGENT_REPO=~/.hermes/hermes-agent
```

## 适用场景

- 安装任何 GitHub 上的 Python 项目
- 特别是需要 editable install 的 AI/LLM 相关项目
- 在 WSL/Linux 环境下安装 Python 包