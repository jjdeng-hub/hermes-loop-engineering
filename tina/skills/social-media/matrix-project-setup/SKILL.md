---
name: matrix-project-setup
category: social-media
description: Matrix 项目安装与测试技能 - 在 WSL/Linux 环境下安装短视频矩阵分发系统
---

# Matrix 项目安装与测试技能

## 概述

Matrix 是一个基于 Python + Playwright 的短视频矩阵内容分发系统，支持抖音、小红书、快手、视频号等平台。本技能记录在 WSL/Linux 环境下安装和测试该项目的完整流程。

## 项目信息

- **仓库**: https://github.com/kebenxiaoming/matrix
- **Stars**: 881
- **语言**: Python 3.8+
- **核心依赖**: Playwright, xhs, pymysql, redis, qrcode

## 安装流程

### 1. 克隆项目（网络受限环境）

由于国内网络 git clone 容易超时，使用 GitHub API 下载：

```bash
# 使用 GitHub API 获取文件列表和内容
# 下载主要文件到项目目录
```

关键文件列表：
- `conf.py` - 配置文件
- `user_queue_login.py` - 登录脚本
- `publish_video_queue.py` - 发布脚本
- `requirements.txt` - 依赖列表
- `database/matrix.sql` - 数据库结构
- `douyin_uploader/main.py` - 抖音模块
- `xhs_uploader/main.py` - 小红书模块
- `kuaishou/main.py` - 快手模块
- `tencent_uploader/main.py` - 视频号模块
- `xhs-api/app2024.py` - 小红书签名服务

### 2. 安装 Python 依赖

使用 uv + 清华镜像源：

```bash
cd /path/to/matrix
uv pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
uv pip install Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 安装 Playwright 浏览器

```bash
uv pip install playwright
python3 -m playwright install chromium
```

验证安装：
```bash
python3 -m playwright --version  # 应显示 Version 1.59.0
```

### 4. 数据库配置（SQLite 替代方案）

原项目依赖 MySQL + Redis，在无法安装的情况下使用 SQLite 替代：

```python
# 创建 init_sqlite_db.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "matrix.db"

tables = [
    "mx_account_info",       # 账号信息
    "mx_account_login_queue", # 登录队列
    "mx_video_publish_queue", # 视频发布队列
    "mx_publish_record",      # 发布记录
    "mx_cookie_cache",        # Cookie 缓存
]
```

运行初始化：
```bash
python3 init_sqlite_db.py
```

### 5. 配置 conf.py

修改配置文件适配 SQLite：

```python
BASE_PATH = str(BASE_DIR / "videos" / "")
SQLITE_CONF = {"database": str(BASE_DIR / "matrix.db")}
```

### 6. 创建账号配置

```ini
# accounts.ini
[xiaohongshu]
account1 = test_xhs_001

[douyin]
account1 = test_douyin_001
```

## 登录测试流程

### 问题：xhs 库需要签名函数

```python
from xhs import XhsClient
client = XhsClient()  # ❌ TypeError: 'NoneType' object is not callable
```

**原因**: `get_qrcode()` 方法内部调用 `self.post()`，需要 `external_sign` 签名函数。

### 解决方案 A：使用 Playwright 直接获取二维码

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.xiaohongshu.com/login")
    
    # 查找二维码元素
    qr_img = page.query_selector(".qrcode-img")
    qr_src = qr_img.get_attribute("src")  # data:image/png;base64,...
    
    # 解码 base64 保存
    import base64
    image_data = base64.b64decode(qr_src.split(",", 1)[1])
    with open("qrcode.png", "wb") as f:
        f.write(image_data)
```

### 解决方案 B：启动签名服务

```bash
cd xhs-api
python3 app2024.py  # Flask 签名服务
```

然后在 conf.py 中配置：
```python
XHS_SERVER = "http://127.0.0.1:5005"
```

### 解决方案 C：在 Windows 主机运行

WSL 无显示环境限制自动检测，建议在 Windows 上运行：

```bash
# Windows 主机
pip install -r requirements.txt
python3 user_queue_login.py 3  # 可显示浏览器窗口
```

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `pip install` 超时 | 网络问题 | 使用清华镜像 `-i https://pypi.tuna.tsinghua.edu.cn/simple` |
| `git clone` 超时 | 网络问题 | 使用 GitHub API 下载 |
| MySQL 未安装 | 权限不足 | 使用 SQLite 替代 |
| Redis 未安装 | 权限不足 | 部分功能受限，可手动管理 Cookie |
| `xhs` 库报错 `NoneType` | 缺少签名函数 | 启动签名服务或使用 Playwright 直接获取 |
| 浏览器无法启动（WSL） | 无 X 服务器 | 使用 `headless=True` 或 Windows 主机运行 |
| 二维码 URL 过长 | data URI 格式 | 直接解码 base64 保存，而非生成新二维码 |

## 目录结构

```
matrix/
├── conf.py                    # 配置
├── init_sqlite_db.py          # SQLite 初始化
├── user_queue_login.py        # 登录脚本
├── publish_video_queue.py     # 发布脚本
├── matrix.db                  # SQLite 数据库
├── accounts.ini               # 账号配置
├── videos/                    # 视频目录
├── douyin_uploader/           # 抖音
│   └── account/               # Cookie 存储
├── xhs_uploader/              # 小红书
│   └── account/               # Cookie 存储
├── kuaishou/                  # 快手
│   └── account/               # Cookie 存储
├── tencent_uploader/          # 视频号
│   └── account/               # Cookie 存储
├── utils/                     # 工具函数
└── xhs-api/                   # 签名服务
    └── app2024.py
```

## 数据库状态码

| 状态 | 含义 |
|------|------|
| 0 | 待登录 |
| 1 | 登录中 |
| 2 | 登录成功 |
| 3 | 登录失败 |

## 副业应用建议

1. **短期验证**: 在 Windows 上测试完整登录 + 发布流程
2. **中期产品**: 封装成"小红书自动登录+发布"服务
3. **长期扩展**: 多平台矩阵发布解决方案（抖音 + 快手 + 视频号）

## 参考项目

- 原项目: https://github.com/kebenxiaoming/matrix
- 参考项目: https://github.com/dreammis/social-auto-upload

---

*创建时间: 2026-05-05*
*适用场景: WSL/Linux 环境下安装社交媒体自动发布项目*