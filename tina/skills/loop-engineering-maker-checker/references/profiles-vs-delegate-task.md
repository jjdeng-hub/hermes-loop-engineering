# Profiles vs delegate_task：什么时候用哪个

## 核心区别

| 维度 | Profile | delegate_task |
|------|---------|---------------|
| 身份 | 固定——有名字、SOUL.md、自己的 memory 和 skills | 无——用完即弃的临时角色 |
| 技能 | 自己的 skills 目录，跨 session 积累 | 每次重新灌入 |
| 记忆 | 持久——越用越熟悉领域知识 | 零——不跨 session |
| 角色 | 独立的 SOUL.md/persona，固定身份 | prompt 里写什么就是什么 |
| 沟通 | 可在群聊里 @profile 直接对话 | 只能通过分配者中转 |
| 启动成本 | 需要创建 profile + 配模型 + 启动 gateway | 零——直接 delegate |

## 决策规则

**当你要做这些事时，用 Profile：**
- 需要固定身份和角色一致性的长期任务（如 DevOps 定期维护）
- 需要在群聊里跟用户或总指挥直接对话
- 需要跨 session 积累领域知识
- 需要独立的技能配置

**当你要做这些事时，用 delegate_task：**
- 一次性任务——用完不保留上下文
- 测试某个想法或快速实验
- 需要并行执行多个无关子任务
- maker/checker 分离的工作流（两轮验证的每个环节）

## 验证案例（2026-06-20）

Jerry 明确说：delegate_task 的角色定位比较随机（用完即弃），
profile 才是真正的永久员工。

## 实例场景

### 场景 1：知识库质量审计
→ 用 **delegate_task**。一次性的审计任务，不需要身份。
Maker 和 checker 各一个 delegate_task，彼此隔离。

### 场景 2：日常服务器维护
→ 用 **Profile**。需要它记住上个月修过什么、有什么已知问题。
Justin 或专门的 DevOps profile 更适合。

### 场景 3：内容创作 + 校对
→ 混合。
Profile（内容主编身份）写初稿 → delegate_task（独立 checker）校稿。
