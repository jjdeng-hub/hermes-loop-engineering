# 四领域独立修行体系设计

## 架构

四个固定领域，各自独立境界和 XP，总等级汇总计算。

| 领域 | 体系 | 风格 | Lv.1→Lv.6 等级名 |
|------|------|------|------------------|
| 💪 健身 | 炼体流 | 金属、力量 | 凡躯→铁骨→铜皮→银血→金身→不灭 |
| 🗣️ 英语 | 文修流 | 墨迹、知识 | 启蒙→断字→识文→通言→妙语→圣言 |
| 📚 阅读 | 道修流 | 玄妙、智慧 | 开卷→知理→明道→洞玄→悟真→化境 |
| 💼 副业 | 商修流 | 财富、经营 | 学徒→匠人→掌柜→东家→商贾→财神 |

## 数据模型

UserProfile 中每个领域独立存储 XP 和 Level：

```dart
class UserProfile {
  int fitnessXp, fitnessLevel;
  int englishXp, englishLevel;
  int readingXp, readingLevel;
  int sideBusinessXp, sideBusinessLevel;
}
```

每次任务完成时，按领域分别加 XP 并重新计算该领域的等级（通过 `calculateLevel()` 函数）。

## 主页布局

角色中心十字布局：
- 中央：角色核心（总等级 + 总 XP）
- 上方：健身分身卡片
- 下方：副业分身卡片
- 左：阅读分身卡片
- 右：英语分身卡片

每张分身卡片显示：领域图标、等级数字、境界名称、迷你进度条。

## 领域详情页

进入领域后直接展示任务列表，每任务分两种类型：

- **二进制任务**：一次完成，点击勾选圆环
- **计数器任务**：累计进度，点击 [+] 按钮递增，每次 +1 立刻获得部分 XP

任务 XP 规则：
- 计数器每次 +1：获得 `totalXp ÷ targetCount` 的 XP
- 全部达成额外奖励：`totalXp - (perActionXp × targetCount)`
- 二进制直接完成：获得全部 XP

## 模板系统

每个领域 3 个预设模板，领域详情页的 + 按钮选择模板，自动创建 Goal 和关联 Tasks。

模板任务定义格式：
```json
{
  "title": "本周完成运动",
  "xp": 30,
  "difficulty": 2,
  "type": "counter",
  "count": 3
}
```
