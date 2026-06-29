---
title: Hermes Agent 从入门到精通
created: 2026-06-30
updated: 2026-06-30
type: concept
tags: [hermes, guide, tutorial, setup, cron, skills, memory, profiles, gateway]
---

# Hermes Agent 从入门到精通

> 来源: 官方文档 (hermes-agent.nousresearch.com/docs) + 实战经验
> 版本: v0.17.0 (2026.6) | 最后更新: 2026-06-30

---

# 第一篇：入门篇

## 1. Hermes Agent 是什么

由 **Nous Research** 开发的开源自主 AI Agent 框架。跟 IDE 里的编码助手不同——Hermes 是一个**常驻的自主 Agent**，能跑在任何地方（VPS、笔记本、服务器），通过 21+ 个消息平台跟你对话。

**核心特性：**
- **模型无关** — 支持 OpenAI、Anthropic、DeepSeek、OpenRouter、本地模型
- **持久记忆** — 跨会话记住用户偏好和关键信息
- **技能系统** — Agent 自己创建、维护、改进的文档化工作流
- **消息网关** — 飞书、QQ、Telegram、Discord、微信等 21 个平台
- **定时任务** — 原生 cron 调度器
- **子代理** — 并行分发任务给独立子 Agent
- **Loop Engineering** — 自驱动循环系统
- **开源 (MIT)** — 可自托管、可修改、无厂商锁定

## 2. 安装

### Linux / macOS / WSL2

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

### Windows (PowerShell)

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

### 验证安装

```bash
hermes --version
# 输出: Hermes Agent v0.17.0 (2026.6.19)
```

### 最快速的起步

```bash
hermes setup --portal
```
一次 OAuth 认证覆盖模型 + 四个 Tool Gateway 工具（网页搜索、图片生成、TTS、浏览器）。

## 3. 首次对话

```bash
# 配置好 API Key 环境变量（.env 文件）
# ~/.hermes/.env:
DEEPSEEK_API_KEY=sk-xxx

# 启动交互模式
hermes

# 非交互模式
hermes -p "Hello, what can you do?"
```

## 4. 目录结构

```
~/.hermes/
├── config.yaml              # 主配置
├── .env                     # API Key 等密钥
├── SOUL.md                  # 人格文件
├── scripts/                 # 自定义脚本
├── cron/output/             # 定时任务输出
├── profiles/                # 多 profile 配置
│   ├── default/             # 默认 profile
│   └── tina/                # 其他 profile
│       ├── config.yaml
│       ├── skills/
│       ├── cron/
│       └── memories/
├── skills/                  # 技能文件
├── logs/                    # 运行日志
└── backups/                 # 备份目录
```

## 5. 配置 Provider

```yaml
# config.yaml
providers:
  deepseek:
    model: deepseek-v4-flash
    api_key_env: DEEPSEEK_API_KEY
    base_url: https://api.deepseek.com/v1

  # 备用 provider
  sensenova:
    model: deepseek-v4-flash
    api_key_env: SENSENOVA_API_KEY
    base_url: https://api.sensenova.com/v1
```

---

# 第二篇：基础使用

## 6. CLI 基础命令

```bash
hermes                    # 启动交互模式
hermes -p "query"         # 非交互模式
hermes --profile tina     # 指定 profile
hermes -p "query" --model deepseek-v4-flash  # 指定模型

# 会话管理
hermes session list       # 查看会话
hermes session search "关键词"  # 搜索历史

# Profile 管理
hermes profile list       # 列出所有 profile
hermes cron list          # 查看定时任务
hermes cron status        # 检查 scheduler 状态
hermes tools              # 查看可用工具集
```

## 7. 会话命令（交互模式内）

| 命令 | 作用 |
|------|------|
| `/new` | 开始新会话 |
| `/clear` | 清除当前上下文 |
| `/model [provider:model]` | 切换模型 |
| `/sethome` | 设置当前对话为 home channel |
| `/status` | 查看会话状态 |
| `/help` | 帮助 |
| `/memory` | 查看/管理记忆 |
| `/personality <name>` | 切换人格 |

## 8. 配置文件详解

```yaml
# ~/.hermes/config.yaml 核心配置

hermes:
  version_check: true
  auto_update: true

providers:
  deepseek:
    model: deepseek-v4-flash
    api_key_env: DEEPSEEK_API_KEY
    base_url: https://api.deepseek.com/v1

# 备用 provider 链
fallback_providers:
  - provider: deepseek
    model: deepseek-v4-flash
  - provider: sensenova
    model: deepseek-v4-flash-lite

# Provider 路由
provider_routing:
  sort: price             # price / throughput / latency
  only: []                # 只允许的 provider
  ignore: []              # 跳过的 provider

# 工具集配置
tools:
  terminal:
    enabled: true
  web:
    search_backend: searxng
    extract_backend: searxng
  browser:
    enabled: true
  delegation:
    max_concurrent_children: 3

# 记忆配置
memory:
  enabled: true
  max_chars: 2200

# 定时任务
cron:
  max_parallel: 3

# 网关
gateway:
  ticker_interval: 60      # scheduler 心跳间隔(秒)
  delivery_retry: 3
```

## 9. Profiles 多角色架构

每个 profile 是完全独立的运行环境，有自己的 skills/plugins/cron/memories。

```yaml
# ~/.hermes/profiles/tina/config.yaml
name: tina
description: 苏格拉底式导师
shell: linux
providers:
  deepseek:
    model: deepseek-v4-flash
```

**多 profile 网关运行：**
```bash
# 启动不同 profile 的网关
hermes --profile tina gateway run
hermes --profile creator gateway run

# 作为 systemd 服务
systemctl start hermes-gateway          # default profile
systemctl start hermes-gateway-tina     # tina profile
```

### Jerry 的实际架构（6 profile）

| Profile | 职责 | 平台 |
|---------|------|------|
| default | 云端管家（我） | 飞书 + QQ |
| tina | 苏格拉底导师 | 飞书 |
| creator | 内容创作者 | 仅后端 |
| fitness | 健身教练 | 仅后端 |
| learner | 学习助手 | 仅后端 |
| office-mgr | 独立给他人用 | 无飞书 |

---

# 第三篇：核心功能

## 10. 技能系统 (Skills)

Skills 是按需加载的知识文档。Hermes 会在需要时自动加载对应的技能。

### Skill 文件格式

```markdown
---
name: my-skill
description: 我的自定义技能
version: 1.0.0
author: user
---

# My Skill

## 背景
这个技能用于完成某类任务。

## 步骤
1. 第一步做什么
2. 第二步做什么
3. 第三步做什么

## 注意事项
- 注意点1
- 注意点2
```

### 技能管理

```bash
# 技能存放在 ~/.hermes/skills/ 下
hermes skill list          # 列出所有技能
hermes skill view my-skill # 查看技能内容
```

Skills 遵循**渐进式披露**模式——只有需要时才加载，最小化 token 消耗。

### 推荐实践
- 技能的触发条件写在 description 里，让 Hermes 自动识别何时加载
- 用 `skill_view(name)` 加载技能
- 技能内容越具体越好（含精确命令、示例、陷阱提示）
- 定期用 curator 检查和清理过时技能

## 11. 记忆系统 (Memory)

Hermes 有三层记忆架构：

### 第一层：会话记忆（session_search）
- 每次对话的完整记录
- 用 FTS5 全文搜索
- 可以跨会话检索（`session_search(query=...)`）

### 第二层：持久事实（memory tool）
- `memory` — 我的笔记（环境、约定、工具偏好）
- `user` — 用户画像（姓名、偏好、风格）
- 每轮对话自动注入，上限 ~2200 字符

### 第三层：深度记忆（fact_store）
- 结构化事实存储
- 支持实体推理（probe/reason/related）
- 信用评分系统（`fact_feedback`）

### 记忆操作

```bash
# 保存事实
hermes memory add "user prefers Chinese"

# 搜索记忆
hermes memory search "preference"

# 深度记忆
hermes fact store add --content "..." --entity "user"
hermes fact store probe --entity "jerry"
```

**最佳实践：**
- 偏好/纠错/环境事实 → memory tool
- 可复用的工作流 → 存为 skill
- 跨赛值得追溯的内容 → vault / wiki

## 12. 上下文文件 (Context Files)

Hermes 自动加载项目上下文文件，优先级：

1. `.hermes.md` / `HERMES.md`（最高优先级）
2. `AGENTS.md`（次高）
3. `CLAUDE.md`
4. `.cursorrules` / `.cursor/rules/*.mdc`
5. `SOUL.md`（独立加载，用于人格定义）

SOUL.md 用于定义 Agent 的永久人格和思维法则。当前 SOUL 包含：
- 苏格拉底式提问
- 第一性原理
- 奥卡姆剃刀
- Loop Engineering
- 故障模式工程
- 第六感：Vault 更新
- 幕僚长过滤器
- 自主进化

## 13. 工具集 (Tools)

| 工具类别 | 包含 |
|---------|------|
| **file** | read_file, write_file, patch, search_files |
| **terminal** | 命令行执行 |
| **web** | web_search, web_extract |
| **browser** | browser_navigate, click, snapshot, scroll, type |
| **delegation** | delegate_task（子代理） |
| **cron** | cronjob（定时任务） |
| **code** | execute_code（Python 脚本执行） |
| **memory** | memory, fact_store, fact_feedback |
| **skill** | skill_view, skill_manage, skills_list |
| **vision** | vision_analyze, image_generate |
| **session** | session_search |
| **mcp** | MCP 服务器工具 |
| **process** | 后台进程管理 |

---

# 第四篇：自动化

## 14. 定时任务 (Cron)

Cron 是 Hermes 最强大的自动化特性之一。

### 创建定时任务

```bash
# 从 prompt 创建
hermes cron create \
  --schedule "0 8 * * *" \
  --prompt "Run daily server health check" \
  --deliver origin

# 更多参数
hermes cron create \
  --name daily-triage \
  --schedule "0 8 * * *" \
  --prompt "# 日常巡检任务..." \
  --deliver feishu:oc_xxx \
  --skills terminal,file \
  --no-agent false
```

### 静默脚本模式（no_agent）

```yaml
name: vault-backup
script: vault-backup.sh    # ~/.hermes/scripts/ 下的脚本
no_agent: true             # 跳过 LLM，直接跑脚本
schedule: "0 */6 * * *"
deliver: local             # 只存文件不投递
```

### 投递目标

| deliver 值 | 效果 |
|-----------|------|
| `origin` | 发送回创建时的对话 |
| `local` | 保存文件不投递 |
| `feishu:chat_id` | 发送到指定飞书对话 |
| `qqbot:chat_id` | 发送到指定 QQ 对话 |
| `all` | 广播到所有已连接平台 |

### 实用模式：watchdog

```bash
# no_agent + 脚本静默检查，有变化才通知
hermes cron create \
  --name disk-watch \
  --schedule "every 30m" \
  --script watch-disk.sh \
  --no-agent true \
  --deliver origin
```
脚本无输出 = 静默；有输出 = 自动投递。

### Jerry 的 cron 架构

| Job | 时间 | 作用 |
|-----|------|------|
| daily-backup | 每天 3AM | Hermes 配置备份 |
| daily-triage | 每天 8AM | 服务器巡检 + 状态报告 |
| hermes-auto-update | 每天 6AM | 自动更新 Hermes |
| vault-backup | 每 6h | Obsidian vault git push |

## 15. 子代理 (Delegation)

`delegate_task` 是 Hermes 并行能力的核心——把任务分发给多个独立子 Agent。

### 单任务模式

```
delegate_task(
  goal="修复 auth.py 中的 bug",
  context="bug 描述: 登录后 session 3 秒超时",
  toolsets=["terminal", "file"]
)
```

### 并行批处理（最多 3 个并行）

```
delegate_task(
  tasks=[
    {"goal": "研究方案A", "toolsets": ["web"]},
    {"goal": "研究方案B", "toolsets": ["web"]},
    {"goal": "研究方案C", "toolsets": ["web"]}
  ]
)
```

### 架构模式

```
扇形分发 → 交叉验证 → 合并 → 一个干净的输出
  Fan out  → Cross-verify → Merge → One clean answer
```

### 实战示例

```python
# 研究多个角度
delegate_task(
  goal="从4个不同角度研究AI Agent落地",
  context="..."
)
# → 4 个子 Agent 并行研究 → 合并一份报告

# 并行开发
delegate_task(
  tasks=[
    {"goal": "写后端API"},
    {"goal": "写前端界面"},
    {"goal": "写测试用例"}
  ]
)
```

## 16. Kanban 多 Agent 编排

Kanban 系统用于协调多个 Hermes profile 协同工作，SQLite 持久化。

- 创建任务 → 分配到工作队列
- 不同 profile 的 Hermes 实例可以消费同一个队列
- 支持 worker lane（不同执行器类型）
- 通过 KanbanCodexLane 调用 Codex CLI

## 17. 持久目标 (Goals)

设置一个长期目标，Hermes 会在多轮对话中持续推进直到完成。

```
[GOAL] "完成第一篇一人公司内容的撰写和发布"
[STATUS] in_progress
[STEPS]
  - [x] 确定主题
  - [ ] 撰写草稿
  - [ ] 审核修改
  - [ ] 发布到小红书
```

## 18. Hooks（生命周期钩子）

在 Hermes 的关键生命周期点执行自定义代码：

| Hook | 触发时机 |
|------|---------|
| `SessionStart` | 会话开始时 |
| `PreToolUse` | 工具调用前（可拦截） |
| `PostToolUse` | 工具调用后 |
| `Stop` | Agent 回复完成 |
| `UserPromptSubmit` | 用户提交消息时 |

示例：每次文件修改后自动运行 linter。

---

# 第五篇：消息网关

## 19. 网关架构

Hermes Gateway 是常驻后台的守护进程，同时连接多个消息平台。

```bash
hermes gateway run      # 启动网关（默认 profile）
hermes gateway status   # 查看状态
```

### systemd 服务配置

```ini
[Unit]
Description=Hermes Agent Gateway
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/lib/hermes-agent/venv/bin/python -m hermes_cli.main gateway run
Restart=always
User=root
WorkingDirectory=/root/.hermes
```

## 20. 平台适配

### 飞书 (Feishu/Lark)

```yaml
# .env 配置
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_DOMAIN=feishu
FEISHU_ALLOW_ALL_USERS=true
FEISHU_GROUP_POLICY=open        # open = 无需白名单即可入群
FEISHU_HOME_CHANNEL=oc_xxx     # 默认投递会话
```

### QQ Bot

```yaml
# config.yaml
platforms:
  qqbot:
    app_id: xxx
    token: xxx
    bot_app_secret: xxx
```

**要点：**
- 群消息需 Bot 被拉入群后才能接收
- 支持 C2C 私聊和群聊
- WebSocket 连接，自动重连
- Gateway 重启后 WebSocket 自动恢复

### Telegram / Discord / 微信 等

21+ 个平台均通过类似配置接入。详情见官方文档。

---

# 第六篇：高级功能

## 21. MCP 集成

Model Context Protocol 允许 Hermes 连接外部工具服务器：

```bash
# 添加 MCP 服务器
hermes config set -- mcp.servers.filesystem.command "npx @modelcontextprotocol/server-filesystem /path"

# 在 config.yaml 中配置
mcp:
  servers:
    filesystem:
      command: npx
      args: ["@modelcontextprotocol/server-filesystem", "/root"]
    agentmail:
      command: npx
      args: ["agentmail-mcp"]
```

## 22. 插件系统

Hermes 插件可以注入自定义工具和钩子：

- 放在 `~/.hermes/plugins/` 下
- 用 `plugin.yaml` + 实现代码定义
- 支持 `model-sherpa` 等内置插件（自动注入提示/校验）
- `disk-cleanup` 等内置清理插件

## 23. 浏览器自动化

Hermes 使用 `agent-browser` 驱动 Chromium：

```bash
# 安装浏览器依赖
npx agent-browser install --with-deps
```

浏览器工具集：
- `browser_navigate` — 导航到 URL
- `browser_click` — 点击元素
- `browser_snapshot` — 获取页面结构
- `browser_type` — 输入文本
- `browser_vision` — 截图分析
- `browser_scroll` — 滚动页面
- `browser_console` — 获取浏览器日志

## 24. 语音模式

支持实时语音对话（CLI、Telegram、Discord）：

- CLI 语音模式（按空格录音，释放发送）
- Telegram 语音消息
- Discord 语音频道
- TTS (Text-to-Speech) 播报

## 25. 安全模型

```yaml
# config.yaml 安全配置
security:
  approve_dangerous: true    # 危险命令需确认
  allowed_toolsets: []       # 限制可用工具集
  sandbox:                   # Docker 沙箱
    enabled: false
    image: hermes-sandbox
```

- 文件写入有 cross_profile 保护
- .env 文件有凭据泄漏防护
- 危险命令需要用户手动确认
- SSRF 防护（内置 URL 安全检查）

---

# 第七篇：实战方案

> 基于 Jerry 的实际部署经验

## 26. 一人公司架构

### 角色分工

```
Jerry（决策者）
    │
    ├─ 我（default）— 云端管家 · 7×24 在线
    │   ├─ 群聊中回答 + 调度
    │   ├─ 每日巡检（cron）
    │   ├─ 自动更新（cron）
    │   ├─ 配置管理
    │   └─ Obsidian vault 知识管理
    │
    ├─ Tina — 苏格拉底导师
    │   ├─ 深层思考碰撞
    │   ├─ 内容方向把关
    │   └─ 人生/战略建议
    │
    ├─ Creator — 内容创作者
    │   ├─ 小红书图文
    │   └─ 内容策略执行
    │
    ├─ Fitness — 健身教练
    │   └─ 训练计划跟踪
    │
    ├─ Learner — 学习助手
    │   └─ 知识获取整理
    │
    └─ office-mgr — 独立角色
        └─ 给其他人使用，完全隔离
```

### 文件架构

```bash
/root/.hermes/
├── .env                       # default API keys
├── config.yaml                # default 配置
├── SOUL.md                    # 我的人格文件
├── scripts/
│   ├── vault-backup.sh        # Obsidian 自动备份
│   └── hermes-update.sh       # Hermes 自动更新
├── profiles/
│   ├── tina/.env + config.yaml
│   ├── creator/.env + config.yaml
│   ├── fitness/.env + config.yaml
│   ├── learner/.env + config.yaml
│   └── office-mgr/.env + config.yaml
└── skills/
    ├── note-taking/obsidian/
    ├── autonomous-ai-agents/
    └── research/opc-loop-engineering/
```

## 27. Obsidian Vault 知识管理

```
vault path:
  /root/.hermes/skills/research/opc-loop-engineering/wiki/

结构:
  Knowledge/
    entities/       — 人员/工具/平台档案
    concepts/       — 框架/方法论
    comparisons/    — 跨工具对比
    queries/        — 研究问题与发现
    raw/            — 源材料
  Projects/         — 在进行的项目
  Archive/          — 已完成的项目
  Inbox/            — 快速捕获
  points/           — 会话摘要（YYYY-MM-DD-标题.md）
  log.md            — 追加式动作日志
  index.md          — 人类可读目录
  SCHEMA.md         — 完整 schema

自动备份: 每6小时 git commit + push 到 GitHub
```

## 28. 定时任务流水线

```
凌晨 3:00 ── daily-backup（配置备份）
           └── 执行 hermes curator backup → 保留最近5份

清晨 6:00 ── hermes-auto-update（自动更新）
           └── git fetch → 检测commit → pull → 重启gateway

早晨 8:00 ── daily-triage（服务器巡检）
           ├── df -h /        ← 磁盘
           ├── free -h        ← 内存
           ├── uptime         ← 负载
           └── ps aux         ← 网关在线
           投递到 飞书

每 6小时 ── vault-backup（Obsidian 备份）
           └── git add → commit → push
```

## 29. 多 Bot 群聊方案

在同一个飞书群里加入多个 Bot，实现多角色协作：

1. 每个 Bot 用不同的飞书 App ID
2. 配置 `FEISHU_ALLOW_ALL_USERS=true` + `FEISHU_GROUP_POLICY=open`
3. 在群里 @不同 Bot 即可调用
4. 多个 Bot 共享 vault 知识库（通过 git 同步）

## 30. 更新策略

```bash
# 手动更新
hermes update -y

# 自动更新（cron job）
# hermes-auto-update 每天6AM执行:
#   git fetch origin
#   git rev-list --count HEAD..origin/main
#   如果 > 0 → git pull → 重启 gateway

# 备份先行
hermes curator backup
```

---

# 第八篇：最佳实践与陷阱

## 31. 省钱技巧

- 主力用 DeepSeek V4 Flash（$0.14/M tokens）
- 免费层：SenseTime 等国产 API
- 视觉任务用免费模型（sensenova-6.7-flash-lite）
- 仅复杂推理才切付费模型（Claude Opus）
- `--max-turns` 限制子 Agent 循环次数
- 利用缓存（cache hit 率可达 90%+）

## 32. 性能优化

- 启动加速：YAML 解析用 CSafeLoader（快 ~6x）
- 最小化工具集：cron job 指定 `enabled_toolsets`
- 记忆精简：定期清理过时事实
- 技能管理：curator 自动归档未使用的技能

## 33. 常见陷阱

**Git 仓库分叉：**
- hermes-update.sh 的 `git pull --rebase` 在历史错乱时会失败
- 应急：`git fetch origin && git reset --hard origin/main`

**Gateway 无法从内部重启：**
- `systemctl restart hermes-gateway` 会杀死当前会话
- 需要从 SSH 或其他 profile 执行

**model-sherpa 插件崩溃：**
- 修复：`(error_message or "").strip()` 代替 `error_message.strip()`

**飞书群消息静默拒绝：**
- 设置 `FEISHU_ALLOW_ALL_USERS=true, FEISHU_GROUP_POLICY=open`

**DeepSeek API 不稳定：**
- 配置 fallback_providers 备用链
- cron job 增加重试逻辑

## 34. 推荐的 Loop Engineering 模式

### Maker-Checker 分离
```
delegate_task(goal="写代码", role="leaf")
→ 子 Agent 写完后
delegate_task(goal="审查代码", role="leaf")
```

### 定时研究循环
```
cron job: 每 4h → 搜索关键词 → 提取 → 摘要 → 投递
```

### 自动知识捕获
```
会话结束后 → 检查是否有关键决策 → 
  是 → 写入 vault points/ 并同步 log.md + index.md
```

### 质量门禁
```
每次交付前 → 现实检验者自问:
  有没有证据支持这个结论？
  "完成了"不等于"生产就绪"
  首次通常需要 2-3 轮迭代
```
