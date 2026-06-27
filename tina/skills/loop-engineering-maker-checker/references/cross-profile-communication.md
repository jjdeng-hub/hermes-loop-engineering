# 跨 Profile 通信（Group Chat）

## 已验证的通信能力（2026-06-20）

1. **@mention 让 agent 响应** ✅
   - 用户在群聊 @agent 名称 → agent 在一个新的 session 中响应
   - agent 的 SOUL.md 生效（写入后需重启 gateway）

2. **Agent 之间不能直接通信** ❌
   - 群聊 API 没有"以 agent 身份发消息"的接口
   - Tom1 不能在群里发一条 @Justin 的消息来叫醒他

3. **Gateway 必须运行 + 模型必须配置** ✅
   - gateway 未运行 → agent 不响应
   - 有 gateway 但模型为空 → "Agent bridge request timed out after 120000ms"

## 实际工作流

```
CEO 给 Tom1 任务
    → Tom1 用 delegate_task 起子 agent（扮演 Justin/Eli/其他角色）
        → 子 agent 独立执行
        → 结果回到 Tom1
    → Tom1 review → 汇报给 CEO
```

群聊只用于 CEO @特定员工直接指挥的场景，不用于 agent 间调度。

## 重要限制

- **No 'send message as agent' API** — agents cannot post to the room programmatically via the REST API
- **Fresh session on each @mention** — no cross-session context for the agent
- **No agent-to-agent @mention tested** — unknown if one profile agent can @mention another
