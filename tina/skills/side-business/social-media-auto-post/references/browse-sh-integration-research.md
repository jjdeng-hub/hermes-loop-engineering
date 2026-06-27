# browse.sh 集成调研

**日期**：2026-05-22
**来源**：https://browse.sh ， Browserbase 出品

## 是什么

`browse.sh` 是 Browserbase 的 Agent 浏览器工具目录，提供：
- `browse` CLI（`npm install -g browse`）
- 云端浏览器会话（Browserbase cloud sessions）
- 预置的网站交互技能库（Amazon、Airbnb、Glassdoor 等）
- Cookie 同步（本地 Chrome → 云端持久化上下文，约 30 天有效）
- 反检测能力（Verified browsers + CAPTCHA 自动解决 + 住宅代理）

## 集成路径

```
用户本地 Chrome（登录小红书/抖音）
    ↓ browse cookie-sync
Browserbase 云端持久化上下文（~30天）
    ↓ browse cloud sessions create --context <ID>
Hermes Agent → 云端浏览器 → 自动发布/抓数据
```

## 三步接入

1. `npm install -g browse`
2. `browse cloud contexts create` → `browse cookie-sync --context <ID>`
3. Agent 通过 `browse cloud browse` 命令操控已登录浏览器

## 对我们的价值

| 能力 | 当前方式 | browse.sh 方式 |
|------|---------|---------------|
| 发布 | 用户手动 | Agent 自动 |
| 数据抓取 | 用户截图 | Agent 自动抓 |
| 登录持久化 | Cookie 文件 1-3 天 | 云端 30 天 |
| 电脑依赖 | 必须开机 | 云端运行 |

## 已知风险

- **没有现成的小红书/抖音 skill**：需自己写自动化脚本
- **Browserbase 付费**：免费额度有限
- **IP 风控**：小红书对国外 IP 敏感；Browserbase 服务器位置待确认
- **cookie-sync 未验证**：对中文社交平台是否有效未知

## 验证计划

1. 安装 `browse` CLI → 测试 cookie-sync 对小红书是否生效
2. 写简单的发布脚本 → 发一条测试帖验证整条链路
3. 两条都通 → 正式接入发布 + 数据抓取工作流
