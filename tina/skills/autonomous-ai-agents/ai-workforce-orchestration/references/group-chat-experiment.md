# Group Chat 实验记录

## 轮次 1（2026-06-20）：Gateway Stopped
- Profile tom2-devops 加入群聊但没有配置模型（model = "—"）
- Gateway 状态：未设置
- 结果：Tom2 在群里注册为参与者，但不会响应 @mention

## 轮次 2（2026-06-20）：Gateway Running, No Model
- Profile tom2-devops：gateway 已运行，但模型字段为 "—"
- 结果：@Tom2 后返回 `Error: Agent bridge request timed out after 120000ms`
- 结论：gateway 运行不等于 agent 能工作。模型必须配置。

## 轮次 3（2026-06-20）：Model Configured + SOUL.md on Disk
- Profile justin-coder：模型 deepseek-v4-flash，gateway 运行
- SOUL.md 写入 `~/.hermes/profiles/justin-coder/SOUL.md` → gateway restart
- 结果：
  - ✅ @Justin 秒回
  - ✅ Justin 回答有自己的三条法则（契约编程/可验证交付/最小意外），不是默认 SOUL
  - ✅ SOUL 从文件系统加载（写入 + 重启 gateway 后生效）

## 最终确认

| 条件 | @mention 响应？ | 备注 |
|------|:-----------:|------|
| 无 gateway | ❌ | 存在但静默 |
| Gateway 运行 + 无模型 | ❌ | 报超时错误 |
| Gateway 运行 + 有模型 + SOUL.md | ✅ | SOUL 从文件系统读取 |

## SOUL 加载流程

1. 写文件：`~/.hermes/profiles/<name>/SOUL.md`
2. 重启 gateway：`POST /api/hermes/profiles/{name}/gateway/restart`
3. 验证：在群聊 @该 agent，看回复是否符合独立 SOUL
