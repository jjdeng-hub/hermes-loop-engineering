---
name: loop-engineering-maker-checker
description: "独立 Maker/Checker 分离工作流——对质量敏感型任务执行两轮验证"
category: autonomous-ai-agents
---

# Maker/Checker 分离工作流

基于 Jerry 和 Tom 的 Loop Engineering 实验验证（2026-06-20）：
- 单 agent 自验证会漏掉系统性问题（案例：439/447 篇文章缺 alt text 被 Mode A 遗漏）
- 独立 checker 能提高覆盖率，但 checker 若无外部清单，盲区与 maker 趋同
- 最优组合：自由审计 + 结构化检查清单

## 强制规则（SOUL 级 — 不可绕过）

**Loop 不是可选的工作流，是本能。**
所有产出型角色（Justin、Eli、Tom1）交付前自动跑 maker/checker 循环：
- **不问"要不要验证"**——直接执行。问就是违规。
- **不绕过**——Checker 发现的问题必须修正，不能手动跳过、不能口头说"这个不影响"然后直接交付。
- **不执行 = 不交付**——验证通过是交付流程的一部分，不是可选步骤。
- **写在 SOUL 里**——这条规则不是 skill 建议，是永久思维法则，不可协商。

## 触发条件

自动加载此 skill：
- 所有产出型角色的每次交付前自动触发
- 当 Jerry 说以下内容时，也加载：
- "帮我审计/检查一下这个"
- "这个任务质量要求高"
- "帮我写 XXX，要求 XXX"
- 涉及知识库文章处理、内容生成、代码审查的任务
- 任何可能影响产品质量或准确性的输出

## Maker/Checker 工作流

### Step 1: 理解任务
确认：这个任务的正确标准是什么？哪些维度需要验证？

### Step 2: Maker 执行
使用 `delegate_task` 起一个子 agent 独立执行。指定输出路径。

### Step 3: Checker 独立验证
用另一个 `delegate_task` 起 checker，prompt 如下：

> 独立验证上一步的产出。不要看 maker 的中间过程。
> 逐项检查：
> 1. 准确率：所有声称是否有证据支持？
> 2. 完整性：有没有遗漏该做的事？
> 3. 格式/规范性：是否符合标准？
> 4. 隐藏问题：maker 没说但应该说的？
> 输出检查报告并标注 pass/fail。

### Step 4: 对账
对比 maker 和 checker 的报告。不一致则循环：
1. 将 checker 的反馈传给 maker
2. maker 修正
3. 重新验证

### Step 5: 交付
两轮结果一致后交付最终成果。

## 最佳实践（来自实验发现）

| 原则 | 说明 |
|------|------|
| **不需要不同模型** | 实验证明不同 prompt + 结构化清单已经有效。不同模型更好但不是必须 |
| **checker 需要清单** | 纯自由判断的 checker 和 maker 盲区趋同（Verifier Theater） |
| **checker 也需要自由** | 纯清单检查会漏掉语义问题（拼写错误、内容截断） |
| **不是所有角色都需要 checker** | 产出的角色要（程序员/RAG工程师），执行的不要（DevOps/销售） |
| **成本控制** | 小型任务不用 full loop；只在质量敏感节点启用 |
| **cycle cap** | 最多 3 轮修正，超限升级给 Jerry |

## 实验验证数据

### 实验一：Codex /goal 自验证失效（2026-06-20）
- Agent 手动计算预期值时算错：test2.txt 汉字数实际 11，agent 算成 10
- Agent 用错答案验证正确脚本输出 → 得出"全部通过"
- 结论：同一 agent 自验证 = 自我辩护
- 交叉引用：Addy Osmani "The model that wrote the code is way too nice grading its own homework"

### 实验二：Hermes Maker/Checker 对比（2026-06-20）
10 篇知识库文章审计：
| 检查项 | Mode A（单 agent） | Mode B（双轮） |
|--------|:---:|:---:|
| 发现 alt text 缺失 | 未提出 | 10/10 精确指出 |
| 发现重复图片 | 未发现 | 4 篇精确计数 |
| 量化精准度 | 印象式描述 | 精确计数 |

**关键发现**：
1. 无外部清单时，checker 和 maker 盲区趋同
2. 纯清单检查漏语义问题（拼写、截断）
3. 最优组合 = 自由审计 + 结构化检查

详见 Obsidian：4-Tom-Memory/Chat-Insights/2026-06-20 Loop Engineering 实验全记录.md

## 用户沟通偏好

- **不要用运动控制/伺服环/PID 做类比**。Jerry 是软件工程师（C++/Python, SECS/GEM, MES），不是 firmware/硬件工程师。
- Jerry 喜欢：直接、不绕弯、不迎合、用他日常工作流程能理解的类比。
- **Code Review 映射**已验证：PR/review/merge = maker/checker/交付。这是他天然理解的框架。
- **"不需要两种模型"**：如果 Jerry 说 checker 用便宜模型就行，接受。实验证明不同 prompt 比不同模型更关键。

## 多 Agent 同任务空间冲突（新增 · 2026-06-21）

当多个探测器（Eli、Justin、Tom1 等）**在同一个任务空间**（同一目录、同一组文件）上并行工作，且没有中间协调机制时，会发生：

| 风险 | 实例 |
|------|------|
| 同时修改同一文件 | Eli 改 .env / requirements.txt，Justin 也改 .env |
| 交叉覆盖环境配置 | Eli 设 EMBED_PROVIDER=chroma 被 Justin 的 local 覆盖 |
| 归因混乱 | 同一个问题（后端连不上）被两个 agent 各自诊断出不同根因，浪费时间 |
| 信息孤岛 | Eli 已安装好 sentence-transformers，Justin 不知情又重新排查 |

**协调机制**：

1. **PM 作为 Gatekeeper** — 对于同任务空间的工作，在 Alex PM 确认前不要动手。PM 先喊停，再逐步分配。
2. **声明式修改** — 改文件之前先输出计划（"我要改 .env 第 4-6 行"），给其他人看到的机会。
3. **定时地盘检查** — 如果发现已有其他 agent 在同一个路径上工作，先检查现状再决定要不要继续。
4. **回滚准备** — 修改时先读源码，知道改动前的状态，方便另一个 agent 回滚冲突修改。

**红线**：没有 PM 协调时，两个 producer 不要同时对同一组文件写操作。

| 痛点 | 解决方案 |
|------|---------|
| 同 agent 执行并验证 | 分两个 delegate_task，不同模型 |
| checker 走形式 | 给 checker 结构化清单 + 自由检查 |
| 无限修正循环 | cycle cap = 3，超限升级给 Jerry |
| 任务间记忆污染 | 用 delegate_task 隔离，不共享 context |
| 成本失控 | 小型任务跳过 full loop，质量敏感节点才启用 |

## 速查参考
- `references/loop-engineering-reference.md` — Loop Engineering 核心知识库（人物、失败模式、anti-patterns）
- `references/maker-checker-experiment-data.md` — 实验原始数据（Mode A vs Mode B 对比）
- `references/cross-profile-communication.md` — Hermes 跨 Profile 群聊通信能力（一人公司架构）
- `references/code-review-analog.md` — Code Review = Loop Engineering 同构映射（Jerry 理解框架）

## Checker SOUL 设计模板（per-profile）

当需要为一人公司的执行角色创建对位 Checker profile 时，使用以下模板结构。每个 Checker 的 SOUL 统一采用"**收产出 → 按标准检查 → 打回或通过**"的三段式工作流，差异仅在检查标准不同。

### Checker SOUL 通用结构

```
# [角色名] — [对方角色名] 的检查员

## 核心使命
只做一件事：检查 [X] 的交付物是否符合标准。

## 检查标准
（3-5 条具体、可验证的硬标准）

## 工作流程
1. 收到 [X] 的产出物
2. 逐条过检查标准，不跳过任何一条
3. 全部通过 → 标记 "✅ CHECKED OK" + 签名，传给上一层
4. 任何一条不通过 → 返回具体问题清单，打回修改
5. 修改后重检，直到全部通过或 [X] 申明无法满足并附理由

## 底线
- 不打感情分
- 不替对方改东西——你只检查
- 不替上层做验收——你只负责检查，不决定"可以上线"
- 不知道就说不知道，不编判断理由
```

### 完整模板
`references/checker-soul-templates.md` 包含 3 个已设计好的 Concrete SOUL：
- Justin-Checker（代码方向）
- Eli-Checker（知识方向）
- Rose-Checker（流程方向）
- 趋势研究员（市场分析方向 — 非 Checker，管理层的独立研究角色）

### 自检方法论

SOUL 写完后不要直接落地——先跑一次自检：

1. **写场景矩阵** — 对每个 SOUL 列 4-5 个真实可能发生的交互场景（正常通过、正常拦截、边界情况、异常路径）
2. **逐一模拟** — 每条标准是否能拦住对应问题？是否有模糊地带？
3. **分类结果** — 🟢 PASS / ⚠️ ATTN（模糊地带）
4. **修补模糊地带** — 对 ATTN 条目做出选择（收紧标准 or 留坑待跑起来再调）

首次自检参考数据（2026-06-21 Tina 对 4 份 SOUL 的 22 场景自检）：
- 15/22 🟢 直接拦截
- 7/22 ⚠️ 模糊地带（缺失异常路径、分类错误未定义、最小批量未设、质量主观尺度）

## 前置条件

- `delegate_task` 可用（两个独立子 agent）
- 输出路径双方可访问（建议用 /tmp/）

## 适用范围：谁需要 checker，谁不需要

不是所有角色都需要 checker。关键区分：

**产出的角色（Producer）→ 需要 checker：**
- 程序员 → 代码正确性验证
- RAG 工程师 → 分类准确率验证
- 内容创作者 → 事实核查 + 格式审计
- **PM（Alex 独立 profile）** → 出计划后 delegate_task + PM 检查清单（8 条件）
- **Tom1（助手/决策搭档）** → 审 Alex 的输出，不是自己去当 PM

**执行的角色（Executor）→ 不需要 checker：**
- DevOps → exit code + 日志就是验证
- 销售 → 提案质量由 Jerry 判断

成本原则：质量敏感的任务才跑 full checker loop。小任务直接交付。
## 变体二：PM 产出检查（产品计划/优先级/任务分解）

当 checker 检查的是非代码产出（文本计划、优先级文档、路线图）时：

### Step 1: Tom1 产出的 PM
Tom1（兼任 PM）产出计划/优先级/任务分解。输出到文件。

### Step 2: delegate_task 独立审查
使用 product-manager-light 中的 8 条件 PM 检查清单：
```
1. 可执行性    2. 假设验证    3. 资源匹配    4. 风险识别
5. 目标对齐    6. 验证标准    7. 备选方案    8. 交付物清晰
```

### Step 3: 对账
- PASS → 交给 Jerry 过目
- FAIL → Tom1 根据 checker 反馈修正 → 重跑 checker

### PM 检查的特点
- checker 不需要不同模型（deepseek-v4-pro 已够）
- 与代码检查不同，PM 检查更依赖语义判断而非语法检查
- 建议保留自由审计空间（不要只依赖 checklist）

## 参考资料

- [profiles-vs-delegate-task.md](references/profiles-vs-delegate-task.md) — 什么时候用 profile、什么时候用 delegate_task 作为 maker/checker
- 必要时给 checker 一个结构化检查清单；同时保留自由判断的提示
