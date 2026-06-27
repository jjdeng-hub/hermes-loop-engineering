# Code Review = Loop Engineering

Jerry 的核心洞察（2026-06-20）：Code Review 本身就是 Loop Engineering。

## 同构映射

| Jerry 的日常工作 | AI Workflow |
|----------------|-------------|
| 解决 Issue / Jira Ticket | 给 Agent 一个 Goal |
| 写代码 | Maker 执行 |
| 提交 PR | Agent 输出成果 |
| Reviewer 审查，给反馈 | Checker 独立验证 |
| 根据 review 修改，重新 push | Maker 根据 checker 反馈修正 |
| CI 通过 + Approve → 合并 | 两轮一致 → 定稿交付 |

## 为什么这个类比有效

- **反馈节点**：PR review 嵌入在开发与合并之间——不是流程末尾才检查
- **独立判断者**：Reviewer 不是作者本人，避免了 Verifier Theater
- **修正回路**：Review → 修改 → 重新 review，直到满意
- **收敛条件**：Approve 不是"没问题"，而是"当前问题都解决了"

## 当需要用 Loop Engineering 说服 Jerry 时

不要说"控制论 / 反馈环 / PID"——用"Code Review for agents"来解释。
Jerry 是软件工程师（C++/Python, SECS/GEM, MES），不是硬件工程师。
他的日常就是 Code Review，这是他能天然理解的框架。
