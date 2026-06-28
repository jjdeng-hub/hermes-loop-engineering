# LLM Wiki 架构与使用指南

## 位置
`~/.hermes/wiki/`（软链接 → repo 的 `wiki/` 目录）
WIKI_PATH 已设置于 `.env`

## 物理位置
实际存储在 GitHub 仓库: `hermes-loop-engineering/wiki/`
可通过 Obsidian 在 Windows/Mac 上直接打开。

## 三层目录
```
wiki/
├── SCHEMA.md           # 规则约定（标签体系、frontmatter 模板）
├── index.md            # 页面索引
├── log.md              # 操作日志
├── raw/                # Layer 1: 原始资料（不可修改）
│   ├── articles/
│   ├── papers/
│   └── transcripts/
├── entities/           # Layer 2: 实体知识（配置、工具、服务）
├── concepts/           # Layer 2: 概念知识（Loop Engineering 等）
├── comparisons/        # Layer 2: 对比分析
└── queries/            # Layer 2: 存档的查询结果
```

## Frontmatter 模板
```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [hermes, loop-engineering, server]
source: raw/articles/source-name.md
---
```

## 页面间链接
使用 `[[wikilinks]]` 语法，兼容 Obsidian Graph View。
创建新页面时必须：
1. 写 frontmatter
2. 添加至少 2 个 [[wikilinks]]
3. 更新 index.md
4. 更新 log.md

## 当前页面（6个）
见 wiki/index.md
