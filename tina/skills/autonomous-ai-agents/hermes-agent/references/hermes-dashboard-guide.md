# Hermes Dashboard 快速指南

> Hermes v0.13.0+ 新增 Web 管理面板
> 启动命令：`hermes dashboard`（默认端口 9119）

## 启动

```bash
hermes dashboard              # 启动并打开浏览器
hermes dashboard --no-open    # 启动但不打开浏览器
hermes dashboard --port 8080  # 自定义端口
hermes dashboard --stop       # 停止所有 dashboard 进程
hermes dashboard --status     # 查看 dashboard 进程状态
```

## 安全配置

```bash
# 默认只绑定 127.0.0.1（安全）
# 如需远程访问（⚠️ 危险：暴露 API Key 到网络）
hermes dashboard --host 0.0.0.0 --insecure
```

## 导航页面

| 页面 | 功能 |
|------|------|
| **SESSIONS** | 搜索/浏览/删除历史会话。显示模型名称、消息数、时间戳、来源平台 |
| **ANALYTICS** | Token 消耗统计、使用频率分析 |
| **MODELS** | 查看/切换当前模型和 Provider |
| **LOGS** | 实时日志查看（替代 `tail -f`） |
| **CRON** | 定时任务管理（创建/编辑/删除） |
| **SKILLS** | 浏览/安装/更新技能 |
| **PLUGINS** | 插件管理 |
| **PROFILES : MULTI AGENTS** | 多配置文件管理（见下方详细介绍） |
| **CONFIG** | 网页端编辑 config.yaml |
| **KEYS** | API Key 和凭证池管理 |
| **DOCUMENTATION** | 内嵌官方文档 |

## 侧边栏系统控制

- **Gateway Status**: 显示网关运行状态和活跃会话数
- **Restart Gateway**: 一键重启消息网关
- **Update Hermes**: 一键更新到最新版
- **Switch theme**: 明暗主题切换
- **Switch to Chinese/English**: 多语言切换

## Profiles 多 Agent 配置详解

### 是什么？

Profiles 是 Hermes 的**多实例隔离系统**。每个 Profile 是一个完全独立的 Hermes 实例，拥有自己的配置、技能、会话、记忆。

```
┌─ Profile: default ─────┐   ┌─ Profile: work ────────┐
│  Config (DeepSeek)     │   │  Config (Kimi)         │
│  Skills (日常)         │   │  Skills (自动化)       │
│  Sessions (个人)       │   │  Sessions (客户项目)   │
│  Memory (个人偏好)     │   │  Memory (工作数据)     │
│  Cron (个人任务)       │   │  Cron (客户任务)       │
└────────────────────────┘   └────────────────────────┘
```

### 适用场景

| 场景 | 推荐 |
|------|------|
| 个人日常 + 副业项目隔离 | 2 个 Profile |
| 多个客户项目互不干扰 | 每个客户 1 个 Profile |
| 测试新技能/新模型 | 1 个 sandbox Profile |
| 不同平台不同配置 | 每个平台关联不同 Profile |

### Dashboard 操作

在 **PROFILES : MULTI AGENTS** 页面可以：
- 查看所有 Profile 列表
- 创建新 Profile
- 切换默认 Profile
- 导出/导入 Profile
- 删除 Profile

### CLI 等效命令

```bash
hermes profile list              # 列表
hermes profile create work       # 创建
hermes profile use work          # 设为默认
hermes profile show work         # 详情
hermes profile delete work       # 删除
hermes profile export work       # 导出
hermes profile import file.tar.gz # 导入
hermes --profile work            # 指定启动
```

### 使用建议

- Profile 之间**数据完全隔离**，客户 A 的信息不会泄漏到客户 B
- 每个 Profile 可以在 Dashboard 的 CONFIG 页面独立配置不同的模型和 Provider
- 切换 Profile 后，之前 Profile 的 Gateway 连接不会中断
