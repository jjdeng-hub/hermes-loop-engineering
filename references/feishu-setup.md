# Feishu 平台搭建笔记

> 用于 opc-loop-engineering skill 的飞书集成

## 插件位置

`/usr/local/lib/hermes-agent/plugins/platforms/feishu/`
- `adapter.py` — 主适配器（5512行）
- `plugin.yaml` — 插件声明
- `feishu_comment.py` / `feishu_comment_rules.py` — 文档评论事件
- `feishu_meeting_invite.py` — 会议邀请处理

## 所需环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `FEISHU_APP_ID` | ✅ | 飞书开放平台应用 ID |
| `FEISHU_APP_SECRET` | ✅ | 飞书开放平台应用 Secret |
| `FEISHU_DOMAIN` | ❌ | 国内用 `feishu`，海外用 `lark`（默认 feishu） |
| `FEISHU_ALLOWED_USERS` | ❌ | 允许使用 Bot 的用户 ID，逗号分隔 |
| `FEISHU_ALLOW_ALL_USERS` | ❌ | 开放所有用户使用 Bot（true/false，开发调试） |
| `FEISHU_GROUP_POLICY` | ❌ | 群聊策略：`allowlist`（默认，仅白名单用户可触发）、`open`（开放）、`disabled`（关闭）、`admin_only` |  
| `FEISHU_ALLOW_BOTS` | ❌ | Bot 间通讯策略：`none`（默认，拒绝所有 Bot 消息）、`mentions`（仅 @ 时响应）、`all`（接收所有 Bot 消息） |
| `FEISHU_HOME_CHANNEL` | ❌ | 推送默认聊天 ID |
| `FEISHU_HOME_CHANNEL_NAME` | ❌ | 首页频道名 |

## 注册步骤

1. 去 https://open.feishu.cn/ → 创建应用 → 企业自建应用
2. 拿到 App ID + App Secret
3. 开启机器人能力（应用详情 → 机器人 → 开启）
4. 权限管理 → 添加权限：`im:message` 相关
5. 发布应用（需管理员审批）
6. 把 `FEISHU_APP_ID` + `FEISHU_APP_SECRET` 写入 `.env`
7. 启动 gateway `hermes gateway run` 测试连接
8. 飞书搜索 App 名称 → 添加 Bot 到群
9. 群里 @Bot 测试回复

## 第二条 Bot（Tina）

同一个 Hermes 实例上挂多个飞书 Bot = 每个 Bot 需要一个独立的 Hermes profile + 独立的 gateway 进程。

原理：飞书插件（`feishu-platform`）每个进程只支持一套 `FEISHU_APP_ID`/`FEISHU_APP_SECRET`。要实现多 Bot，不是在同一 profile 里配多个凭证，而是建多个 profile，各自跑 gateway。

### 完整步骤

```bash
# 1. 创建新 profile
hermes profile create tina

# 2. 写入第二套飞书凭证到新 profile 的 .env
#   write_file 对 .env 可写（read_file 被阻止，但 write_file 工作）
#   注意：不要截断 secret，写完整的 32 字符
write_file(path='~/.hermes/profiles/tina/.env', content=...)

# 3. 启用飞书插件（每个 profile 独立启用）
hermes --profile tina plugins enable feishu-platform

# 4. 安装 gateway 服务（自动命名为 hermes-gateway-<profile>）
hermes --profile tina gateway install

# 5. 验证连接
hermes --profile tina gateway status
journalctl --user -u hermes-gateway-tina -n 20 --no-pager
```

### 验证清单

你的日志中应该有：
```
[Feishu] Connected in websocket mode (feishu)
```

两个 gateway 进程互不干扰。在服务器上的开销约 +200-300MB 内存。

### 注意事项

- 第二个 Bot 需要在飞书开放平台**新建应用**，不是复用第一个 App
- 发布应用后才能被拉入群
- 两个 Bot 可以拉入**同一个飞书群**，实现双 Bot 协作（注意防对话循环）

## 群消息被静默拒绝排查

这是新 Bot 上线后最常见的坑。群里 @了 Bot，Bot 没反应，但也没报错。

### 原因

飞书插件对群消息有三层过滤（`_admit` 方法）：

```
第 1 层：自回声检查  → 如果消息发自 Bot 自身，丢弃
第 2 层：Bot 检查    → 如果消息发自另一个 Bot，看 FEISHU_ALLOW_BOTS 策略
                       默认 "none" 意味着所有 Bot 消息被拒
第 3 层：群策略检查  → 看 FEISHU_GROUP_POLICY 和 FEISHU_ALLOWED_USERS
                       默认 "allowlist" + 空白名单 = 所有用户被拒
第 4 层：@提及检查   → 如果 require_mention=true（默认），必须 @Bot 才响应
```

**最常见的情况**：新配的 Bot 在 `.env` 里没有设 `FEISHU_ALLOW_ALL_USERS=true` 也没有设 `FEISHU_ALLOWED_USERS`，`FEISHU_GROUP_POLICY` 默认是 `allowlist`，所有群消息在第 3 层被静默丢弃。

### 修复

在 `.env` 里添加：

```bash
FEISHU_ALLOW_ALL_USERS=true        # 允许所有用户
FEISHU_GROUP_POLICY=open           # 开放群策略
```

然后**从外部终端**重启 gateway。详见下方「Gateway 重启阻塞」章节。

### 验证

排查时看 gateway 日志：

```bash
journalctl --user -u hermes-gateway -n 50 --no-pager | grep -i "dropping\|admit\|reject"
```

如果看到 `dropping inbound event: group_policy_rejected` 就是群策略问题。
如果看到 `dropping inbound event: bots_disabled` 就是 Bot 消息被拒（用于多 Bot 同群场景）。

如果群里 @ 的消息根本没出现在日志里，说明飞书开放平台权限不够——检查应用权限中是否开启了 `im:message` 相关的事件推送。

## 安装步骤

```bash
# 1. 安装依赖（Hermes host venv）
source /usr/local/lib/hermes-agent/venv/bin/activate
pip install lark-oapi

# 2. 启用插件
hermes plugins enable feishu-platform

# 3. 写 .env 凭证（见下方注意事项）
# 4. 重启 gateway（见下方注意事项）
```

## 已知注意

### 🔴 .env 读写保护差异
`.env` 文件的读写保护行为不一致，容易踩坑：

| 操作 | 状态 | 说明 |
|------|------|------|
| `write_file` | ✅ **可写** | 直接写 `.env` 路径即可（已验证可行） |
| `patch` | ❌ 被阻止 | 无法对 `.env` 做 patch |
| `read_file` | ❌ 被阻止 | 返回 "Access denied: secret-bearing environment file" |
| `terminal("cat .env")` | ⚠️ 值已脱敏 | 所有 secret value 被替换为 `***` 形式 |

**不要在 terminal 里 cat .env 然后写回去** —— 你会把脱敏后的值（如 `KEY=sk-***xxxx`）写回文件，截断所有密钥。

**不要用 shell echo/printf 写凭证** —— 特殊字符（& ^ $ # !）会被静默截断。

### 🔴 Gateway 重启阻塞
从 gateway 进程内（例如通过 QQ Bot 网关对话）无法重启 gateway。以下命令在 gateway 内部会报错 BLOCKED：

```bash
hermes gateway restart           # ❌ SIGTERM 传播到子进程
systemctl --user restart hermes-gateway  # ❌ 同样被拦截
nohup bash -c 'sleep 1 && ...'   # ❌ hard block
```

**解决方法**：让用户在外部终端（SSH/Web Console）执行 `systemctl --user restart hermes-gateway`。

### 其他注意
- 依赖 `lark-oapi` SDK（如缺失需 `pip install lark-oapi`）
- 启用插件：`hermes plugins enable feishu-platform`（下次会话生效）
- 飞书使用三种用户 ID：open_id（app 级别）、user_id（租户级）、union_id（开发者级）
- Bot 自身在飞书群内的身份由 App ID 确定
- 群聊 @ 触发需要 Bot 发布后在群里有响应权限
