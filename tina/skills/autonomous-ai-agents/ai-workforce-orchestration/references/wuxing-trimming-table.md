# 五路并行 · 技能修剪参考表

> 源自 2026-06-29 会话：Jerry 修正了四个角色的第一性原理定义，然后修剪了各 profile 的技能。**修剪已执行（`rm -rf` 删除无关技能目录）**，四个角色各重启了 gateway。

## 架构

```
Jerry
  ├── Tom (我) — 总助手，不绑桩子，调度所有角色
  ├── Creator  — ⑤留下痕迹 → 实现个人价值
  ├── Tina     — ②独处 + ④自建标准
  ├── Fitness  — ①身体 → 了解并掌控身体
  └── Learner  — ③持续学新 → 学会任何东西
```

## 第一性原理定义演进

| 角色 | 原定义（表面） | 新定义（底层） | 变化本质 |
|------|-------------|-------------|---------|
| Creator | 帮 Jerry 把想法变成内容发出去 | 帮 Jerry 在世界上留下他的痕迹，实现个人价值 | 不绑死在「写文章」这个形式上 |
| Learner | 帮 Jerry 学英语，每天提醒 | 帮 Jerry 学会任何他想学的东西，用 AI 时代最聪明的方式 | 不限英语，不守旧方法 |
| Fitness | 健身教练，催训练 | 帮 Jerry 了解并掌控自己的身体，让它越来越强 | 覆盖生理、营养、恢复、原理 |
| Tina | 苏格拉底提问 | 帮 Jerry 独处和建立自己的标准 | ✅ 本质够深，没变 |

## 技能修剪表

### Tina（哲思导师）
保留：`note-taking`
删除：autonomous-ai-agents, computer-use, creative, data-science, dogfood, email, github, media, mlops, productivity, research, smart-home, social-media, software-development, yuanbao

### Creator（痕迹催化剂）
保留：`creative`, `social-media`, `media`, `note-taking`, `email`
删除：apple, autonomous-ai-agents, computer-use, data-science, dogfood, github, mlops, productivity, research, smart-home, software-development, yuanbao

### Learner（学习引擎）
保留：`research`, `note-taking`, `email`
删除：apple, autonomous-ai-agents, computer-use, creative, data-science, dogfood, github, media, mlops, productivity, smart-home, social-media, software-development, yuanbao

### Fitness（身体导师）
保留：`note-taking`
删除：apple, autonomous-ai-agents, computer-use, creative, data-science, dogfood, email, github, media, mlops, productivity, research, smart-home, social-media, software-development, yuanbao

## 执行命令（以 Tina 为例）

```bash
cd ~/.hermes/profiles/tina/skills
for d in apple autonomous-ai-agents computer-use creative data-science dogfood email github media mlops productivity research smart-home social-media software-development yuanbao; do
  rm -rf "$d"
done
```

## 新增的进化章节

所有角色（包括 Tom）的 SOUL 中新增了「进化」章节，要点：
- **主动学习** — 遇到不懂的去查去搜，不拿训练数据当避风港
- **保持饥饿** — 发现更好方法就吸收，更新自己的工作方式
- **自驱迭代** — 连续两周同样方式做同样事，就问自己有没有更好的做法

## 各角色 SOUL 文件位置

- Tom: `/root/.hermes/SOUL.md`
- Tina: `/root/.hermes/profiles/tina/SOUL.md`
- Creator: `/root/.hermes/profiles/creator/SOUL.md`
- Learner: `/root/.hermes/profiles/learner/SOUL.md`
- Fitness: `/root/.hermes/profiles/fitness/SOUL.md`
