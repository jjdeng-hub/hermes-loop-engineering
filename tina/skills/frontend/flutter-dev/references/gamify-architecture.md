# Gamify 项目架构参考

## 项目定位

个人成长游戏化系统（修仙主题），四领域：副业 / 健身 / 英语 / 阅读。

## 技术栈

- Flutter 3.x + Dart
- Riverpod（状态管理）
- shared_preferences（本地存储，Web 兼容）
- CustomPaint（角色系统，第二周实现）

## 数据模型

- **UserProfile**: 总 XP、等级、徽章、连击天数、各领域 XP
- **Goal**: 标题、领域、难度、目标 XP、进度、拆解树
- **Task**: 所属目标、标题、基础 XP、难度、状态

## XP 系统

- 等级增长 1.4× 指数（RPG 标准）
- 20 级修仙境界：凡人 → 练气 → 筑基 → 金丹 → 元婴 → 化神 → 合体 → 大乘 → 渡劫 → 仙尊
- XP 公式：baseXp × difficultyMultiplier × completionMultiplier
- 连击加成：7 天 +15%，14 天 +30%，30 天 +50%

## 角色系统（Week 2）

五层叠加：身材（健身）→ 装备（总XP）→ 光环（等级）→ 表情（综合）→ 背景

## MVP 路线

- Week 1: 骨架 — 数据层 + CRUD + 主页
- Week 2: 灵魂 — 角色 + 动画 + 统计
