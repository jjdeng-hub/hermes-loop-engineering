---
name: github-project-analysis
description: GitHub 项目分析技能 - 通过 GitHub API 获取项目信息、结构和关键代码
tags: [github, analysis, research, automation]
---

# GitHub 项目分析技能

## 触发条件
- 用户要求查看/分析 GitHub 项目
- git clone 因网络问题失败
- 需要快速获取项目结构和关键信息

## 工具
- `terminal` (git clone, curl)
- `execute_code` (Python + requests + base64)

## 步骤

### 1. 尝试直接克隆（首选）
```python
import subprocess
result = subprocess.run(["git", "clone", repo_url, target_dir], timeout=60)
```

### 2. 网络失败时切换 GitHub API
```python
import requests
import base64

# 获取仓库基本信息
api_url = f"https://api.github.com/repos/{owner}/{repo}"
response = requests.get(api_url, timeout=30)
data = response.json()
# 提取：stars, forks, description, language, license, created_at

# 获取文件列表
contents_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
response = requests.get(contents_url, timeout=30)
files = response.json()
# 遍历显示目录结构

# 获取 README
readme_url = f"https://api.github.com/repos/{owner}/{repo}/contents/README.md"
response = requests.get(readme_url, timeout=30)
data = response.json()
content = base64.b64decode(data['content']).decode('utf-8')

# 获取 requirements.txt
req_url = f"https://api.github.com/repos/{owner}/{repo}/contents/requirements.txt"
response = requests.get(req_url, timeout=30)
data = response.json()
content = base64.b64decode(data['content']).decode('utf-8')

# 获取核心代码文件
for file_path in ['conf.py', 'main.py', 'user_queue_login.py']:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    response = requests.get(url, timeout=30)
    data = response.json()
    content = base64.b64decode(data['content']).decode('utf-8')
```

### 3. 分析报告结构
```
## 📊 项目概述
- 仓库信息（stars, forks, description）
- 技术栈（语言、依赖）
- License

## 📁 目录结构
- 核心模块
- 配置文件
- 数据库结构

## 🔧 核心功能
- 主要功能点
- 技术实现

## 🚀 使用指南
- 安装步骤
- 配置要求
- 运行命令

## 💡 与用户关联
- 项目如何帮助用户目标
- 可借鉴的方案

## ⚠️ 注意事项
- 风险提示
- 合规性说明
```

## 实战案例：Matrix 项目分析（2026-05-05）

### 项目信息
- **仓库**: kebenxiaoming/matrix
- **⭐ Stars**: 881
- **📝 描述**: 视频矩阵内容分发系统，基于 Python + Playwright 实现自动化发布视频到各大社交媒体平台
- **📦 语言**: Python 3.8+
- **📄 License**: Apache-2.0

### 支持平台
| 平台 | 目录 | 状态 |
|------|------|------|
| 抖音 | `douyin_uploader/` | ✅ 完整 |
| 小红书 | `xhs_uploader/` | ✅ 完整（含签名服务） |
| 快手 | `kuaishou/` | ✅ 完整 |
| 视频号 | `tencent_uploader/` | ✅ 完整 |

### 技术架构
```
matrix/
├── conf.py              # 核心配置（Redis/MySQL/路径）
├── user_queue_login.py  # 登录队列脚本（扫码登录）
├── publish_video_queue.py  # 视频发布队列脚本
├── database/matrix.sql  # 数据库结构
├── douyin_uploader/     # 抖音上传模块
├── xhs_uploader/        # 小红书上传模块（含 stealth 签名）
├── kuaishou/            # 快手上传模块
├── tencent_uploader/    # 视频号上传模块
├── utils/               # 工具函数（缓存、文件处理等）
└── xhs-api/             # 小红书签名服务（Flask）
```

### 核心依赖
```txt
requests
playwright
eventlet
schedule
cf_clearance
pymysql
redis
qrcode
xhs
```

### 使用命令
```bash
# 安装依赖（国内镜像）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
playwright install chromium

# 配置数据库
mysql -u root -p < database/matrix.sql

# 启动登录（小红书=3）
python user_queue_login.py 3

# 启动发布
python publish_video_queue.py
```

## 常见陷阱
1. **GitHub API 速率限制**：未认证 60 次/小时，认证后 5000 次/小时
2. **base64 解码**：API 返回的内容是 base64 编码，需解码
3. **文件大小限制**：API 对大文件有返回限制，优先获取 README 和核心文件
4. **网络超时**：国内访问 GitHub API 可能超时，适当增加 timeout
5. **签名服务**：小红书需要启动 Flask 服务获取 `x-s` 和 `x-t` 签名

## 验证
- 确认获取了 README 内容
- 确认获取了 requirements.txt
- 确认获取了至少 1-2 个核心代码文件
- 分析报告结构完整

## 相关技能
- `github-content-download`: 大文件下载
- `devops/github-python-install`: Python 项目安装