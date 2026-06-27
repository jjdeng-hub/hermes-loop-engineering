---
name: flutter-dev
description: Flutter 项目开发工作流 — 从零搭建到部署的全流程，含 Windows/WSL 环境配置、国内镜像、Web 存储方案、Riverpod 状态管理、常见陷阱
version: 1.0.0
---

# Flutter 开发

## 触发条件

- 用户要求创建新的 Flutter 项目
- 在 gamify 项目（或其他 Flutter 项目）中开发功能
- Flutter 编译或运行时错误
- 需要选择状态管理或存储方案

---

## 环境配置（Windows + WSL）

### Flutter 安装位置

用户 Flutter 装在 Windows 下（`C:\ProgramData\flutter`），WSL 内通过 `cmd.exe /c` 调用。

### Chrome 替代方案

用户未装 Chrome，用 Edge 替代。设置环境变量：
```
setx CHROME_EXECUTABLE "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
```

> ⚠️ `flutter config --chrome-executable` 在新版 Flutter 中可能不可用。直接用 `setx CHROME_EXECUTABLE` 设置环境变量，然后重开 CMD。

验证：
```
flutter doctor
```
Web 开发只需确保 `[✓] Chrome - develop for the web` 和 `[✓] Flutter` 变绿。Android SDK / Visual Studio 的红叉可忽略。

### 国内镜像

```
setx PUB_HOSTED_URL "https://pub.flutter-io.cn"
setx FLUTTER_STORAGE_BASE_URL "https://storage.flutter-io.cn"
```

设置后**必须重新打开 CMD** 才能生效。

验证镜像是否生效：
```powershell
echo %PUB_HOSTED_URL%
echo %FLUTTER_STORAGE_BASE_URL%
```
如果为空，说明环境变量未设置或 CMD 未重启。

`pub get` 超时先检查上述两个变量。

---

## 项目初始化

```bash
cd C:\Users\jjdeng\Desktop
flutter create <project_name> --platforms=web
```

MVP 阶段只勾 `--platforms=web`，不加 Android/iOS。

---

## 技术选型

### 状态管理：Riverpod

用 `flutter_riverpod`。不需要代码生成（`riverpod_annotation`），避免 build_runner 复杂度。

关键模式：
- `StateNotifierProvider` 用于可变状态（用户、目标列表）
- `Provider` 用于无状态工具类
- `FutureProvider.family` 用于按参数查询

### 存储：shared_preferences（Web 优先）

**sqflite 在 Web 上不工作。** 用 `shared_preferences` + JSON 序列化替代。数据量小、无复杂查询的场景完全够用。

数据层模式：
- `AppStorage` 类封装所有读写
- 每个集合存一条 JSON 字符串（`goals`、`tasks`、`user_profile`）
- 模型类提供 `toMap()` / `fromMap()` 用于序列化

---

## 常见陷阱

### ConsumerWidget 的 context 访问

`ConsumerWidget.build(BuildContext context, WidgetRef ref)` 中的 `context` 是参数，不是 getter。在 build 方法外部的辅助方法中无法直接使用。**必须显式传递 `BuildContext` 参数。**

```dart
// ❌ 错误：辅助方法中直接使用 context
Widget _buildSomething() {
  return TextButton(onPressed: () => _showDialog(context)); // context 不存在
}

// ✅ 正确：显式传递
Widget _buildSomething(BuildContext context) {
  return TextButton(onPressed: () => _showDialog(context));
}
```

### StatefulBuilder 内变量持久化

`showDialog` + `StatefulBuilder` 中，**局部变量必须声明在 builder 闭包外部**，否则每次 `setDialogState` 重绘都会重置为初始值。

```dart
// ❌ 错误：变量在 builder 内部，每次 setDialogState 都重置
showDialog(builder: (ctx) => StatefulBuilder(
  builder: (ctx, setState) {
    Domain selected = Domain.fitness;  // 每次重建都重置！
    ...
  },
));

// ✅ 正确：变量在外层
Domain selected = Domain.fitness;
showDialog(builder: (ctx) => StatefulBuilder(
  builder: (ctx, setState) { ... },
));
```

### GestureDetector 嵌套 Container

当用 `GestureDetector` 包裹 `Container` 时，确保正确关闭所有括号。经常出现少一层 `)`。

### Dart switch cases fall through

Dart 的 switch 默认 **穿透（fall-through）** —— 匹配到的 case 及其后所有 case 都会执行，除非遇到 `break`。

```dart
// ❌ 错误 — 穿透到所有后续 case
switch (domain) {
  case 'fitness': newFitnessXp += xp;
  case 'english': newEnglishXp += xp;   // 也在 fitness 触发时执行！
  case 'reading': newReadingXp += xp;   // 也在 fitness/english 触发时执行！
}

// ✅ 正确 — 每个 case 后加 break
switch (domain) {
  case 'fitness':
    newFitnessXp += xp;
    break;
  case 'english':
    newEnglishXp += xp;
    break;
}
```

---

## 项目结构规范

```
lib/
├── core/          # 常量、主题、等级表、XP计算器
├── models/        # 数据模型（Goal, Task, UserProfile）
├── data/          # 存储层（AppStorage）、模板数据
├── providers/     # Riverpod providers
├── screens/       # 页面（每个页面一个文件）
└── widgets/       # 可复用组件
    └── character/ # 角色相关组件
```

文件头不需要 `app.dart`，直接在 `main.dart` 中配置 MaterialApp。

---

## 运行与调试

```bash
cd C:\Users\jjdeng\Desktop\gamify
flutter clean          # 遇到奇怪错误先 clean
flutter pub get
flutter run -d chrome
```

添加依赖后必须先 `flutter pub get`，否则 import 报错。
