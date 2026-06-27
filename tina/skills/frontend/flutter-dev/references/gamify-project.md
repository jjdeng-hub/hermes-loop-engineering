# Gamify 修仙游戏化系统 — 项目实现规范

## UI 质量标准 🔴

用户期望的是**高级、现代、有质感的 UI**，不接受基础 Material Design：

- **必须用**：玻璃态毛玻璃效果（`BackdropFilter` + `ImageFilter.blur`）、发光阴影、渐变边框
- **必须用**：自定义绘制角色（`CustomPaint`），不能用占位 Icon
- **推荐用**：粒子/浮动动画背景、`BouncingScrollPhysics`、Overlay XP 飘出动画
- **配色**：深邃宇宙暗色底（`#070B1A`）+ 金色点缀，不要纯黑或灰底
- **字体**：不要太小，层次分明
- **禁止**：纯色块卡片、Material 原生进度条、无动画交互

## 项目结构

```
C:\Users\jjdeng\Desktop\gamify\
├── lib/
│   ├── main.dart              # 入口，ProviderScope + 种子数据
│   ├── core/
│   │   ├── theme.dart         # 主题色、境界色、领域色、发光工具
│   │   ├── constants.dart     # Domain/TaskStatus/GoalStatus/Difficulty 枚举
│   │   ├── levels.dart        # XP 等级公式 (growthRate=1.4, baseXp=60)
│   │   └── xp_calculator.dart # XP 计算器
│   ├── models/
│   │   ├── user_profile.dart  # 用户档案（四领域独立 XP/Level）
│   │   ├── goal.dart          # 目标模型
│   │   └── task.dart          # 任务模型（binary/counter + TaskType 枚举）
│   ├── data/
│   │   ├── database.dart      # SharedPreferences 存储
│   │   ├── templates.dart     # 四领域 12 模板（DomainTemplates.templates）
│   │   └── seed_data.dart     # 首次启动自动填充
│   ├── providers/
│   │   └── all_providers.dart # Riverpod: UserNotifier, GoalsNotifier, TaskActions
│   ├── screens/
│   │   ├── home_screen.dart   # 主页：粒子背景 + Q 版角色 + 四领域卡片
│   │   └── domain_screen.dart # 领域页：境界面板 + 目标/任务列表
│   └── widgets/
│       ├── q_character.dart   # Q 版修仙角色（CustomPaint，呼吸浮动动画）
│       ├── particles.dart     # 灵气粒子背景
│       └── glass_card.dart    # 玻璃态卡片 + 发光进度条 + XP 飘出动画
```

## 核心技术栈

- **Flutter 3.44.1** stable, Web 优先（Chrome 调试）
- **Riverpod** 状态管理
- **SharedPreferences** 本地存储（Web 不支持 sqflite）
- **uuid** 包生成 ID
- **动画**：`AnimationController` + `AnimatedBuilder` + `TweenAnimationBuilder`

## 关键 UI 组件模式

### 玻璃态卡片
```dart
ClipRRect(
  borderRadius: BorderRadius.circular(16),
  child: BackdropFilter(
    filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
    child: Container(
      decoration: BoxDecoration(
        color: Colors.white.withAlpha(20),
        border: Border.all(color: Colors.white.withAlpha(15)),
        gradient: LinearGradient(/* 微妙的白色渐变 */),
      ),
      child: /* 内容 */,
    ),
  ),
)
```

### 发光进度条
容器外发光 shadow，内部渐变色填充，FractionallySizedBox 控制宽度。

### Overlay XP 飘出动画
```dart
// Overlay.of(context).insert(OverlayEntry)
// TweenAnimationBuilder: translateY(0→-60) + opacity(1→0)
```

### Q 版角色
```dart
// CustomPaint + AnimationController(3s reverse repeat)
// 绘制：光环(radial gradient) → 身体/道袍 → 腰带 → 圆脸+腮红 → 大眼+高光 → 微笑 → 头发+呆毛 → 境界光环
```

## ⚠️ 已知陷阱

### 1. Domain 枚举名匹配（🔴 曾导致 XP 始终为 0）
`Domain.sideBusiness.name` 返回 `"sideBusiness"`（camelCase），**不是** `"side-business"`。
所有 switch-case 必须用 `'sideBusiness'`，包括：
- `UserProfile.domainXp()` / `domainLevel()`
- `UserNotifier.addXp()`
- `AppTheme.domainLevelColor()` / `domainLevelName()`
- 任何其他根据 domain 字符串做判断的地方

### 2. TaskType 定义唯一位置
`TaskType` 枚举只在 `models/task.dart` 中定义。`constants.dart` 中**不包含** TaskType。
如果两处都有定义会导致编译歧义。

### 3. 死代码清理
`goal_detail_screen.dart` 已被 `domain_screen.dart` 完全替代，已删除。
如需目标详情页功能，在 `domain_screen.dart` 内扩展，不要恢复旧文件。

### 4. SharedPreferences 替代 SQLite
Web 环境不支持 `sqflite` 包，所有持久化用 `SharedPreferences` + JSON 序列化。

### 5. 首次启动种子数据
`main.dart` 调用 `seedDataIfEmpty()` 自动创建 12 个模板目标 + 所有任务。
如果数据异常，清空浏览器 SharedPreferences 重启即可。

### 6. 🔴 异步 Provider 加载竞态（曾导致任务消失）
**症状**：进领域页无数据、返回再进任务消失、需要手动点 `+` 重新添加。

**根因**：在 `initState` 中用 `ref.read(goalsProvider)` 只读到初始空数组 `[]`，
因为 `GoalsNotifier._load()` 是异步的，数据还没从 `SharedPreferences` 加载完。
之后即使数据到了，`initState` 只执行一次，不会重建 UI。

**❌ 错误模式**：
```dart
// initState 里一次性读取 → 读到 [] 然后永远不更新
void initState() { _load(); }
Future<void> _load() async {
  final goals = ref.read(goalsProvider).where(...);  // ← 竞态！
  setState(() { ... });
}
```

**✅ 正确模式**：在 `build()` 中用 `ref.watch` 响应式监听，目标变化时自动重载任务：
```dart
Widget build(BuildContext context) {
  final allGoals = ref.watch(goalsProvider);  // ← 响应式，变化时自动重建
  final goals = allGoals.where((g) => g.domain == widget.domain).toList();
  _syncTasks(goals);  // 异步加载任务，_goalsSame() 去重防止无限循环
  // ...
}
```

**去重关键**：`_syncTasks()` 内部用 `_prevGoals` + `_goalsSame()` 比较，只在 goals 真正变化时才重新加载任务，避免 `build()` 每次重建都触发异步调用。

**完成后刷新**：任务完成后调用 `ref.invalidate(goalsProvider)` 触发全链路刷新。

### 7. CustomPaint 角色局限 & 素材方向
CustomPaint 能画基础几何形状（圆脸、道袍），但画不出真正好看的 Q 版角色。
用户期望的"高级感"需要**真实美术资产**：
- 方案 A：下载免费 Q 版修仙角色 PNG → `Image.asset()` 加载
- 方案 B：AI 生成角色图 → 存入 `assets/images/`
- 加载后用 `AnimatedBuilder` + `Transform.translate` 做浮动动画替代 CustomPaint
- 境界光环可以用径向渐变 `BoxShadow` 叠加在 Image 上

素材来源建议：itch.io 免费像素/二次元包、花瓣/B站找 CC0 修仙角色、Midjourney/DALL·E 生成。
