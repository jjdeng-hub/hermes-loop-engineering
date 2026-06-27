---
name: camofox-anti-detect-browser
description: AI agent 网页数据抓取的辅助工具，反检测浏览器服务
---
# CAMOFOX 反检测浏览器

## 用途
AI agent 网页数据抓取的辅助工具，提供反爬虫/反检测能力。

## 核心功能
- 浏览器指纹伪造（反检测）
- 自动 CAPTCHA 解决
- Session 隔离管理
- 元素引用交互（click/type/ref）
- 支持 Google/YouTube/Amazon 等主流网站

## 基础信息
- GitHub: daijro/camoufox
- 基于 Firefox 的反爬分支
- 项目路径: ~/camofox-browser
- REST API 端口: 9377
- 环境变量: CAMOFOX_URL=http://localhost:9377

## 安装步骤

### 方式1：npm（当前使用）
```bash
git clone https://github.com/jo-inc/camofox-browser && cd camofox-browser
npm install
npm run postinstall  # 下载浏览器（约300MB）
npm start
```

### 方式2：Docker（推荐）
```bash
docker run -d --network host -e CAMOFOX_PORT=9377 jo-inc/camofox-browser
```

## 已知问题
- WSL 访问 GitHub 限速，Windows 正常
- npm run postinstall 需从 GitHub 下载 Firefox 浏览器二进制
- 下载脚本: C:\Users\jjdeng\Downloads\install-camoufox.bat
- 需求文档: C:\Users\jjdeng\Downloads\camofox-installation-requirements.md

## 验证命令
```bash
curl http://localhost:9377/health
curl http://localhost:9377/v1/browser/start
```