---
name: hermes-agent-self-evolution-install
description: Install and configure hermes-agent-self-evolution in Chinese network environment. Uses uv + Tsinghua mirror to avoid pip timeouts.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes-agent, self-evolution, installation, dspy, gepa, optimization, chinese-network]
    related_skills: [github-python-install, install-python-packages-cn]
---

# Hermes Agent Self-Evolution 安装指南

## 概述

Hermes Agent Self-Evolution 是 NousResearch 官方开发的自进化增强版本，使用 DSPy + GEPA 自动优化 Hermes Agent 的技能、提示词和代码。

**仓库：** https://github.com/NousResearch/hermes-agent-self-evolution
**Stars：** 2,738+
**许可证：** MIT

## 安装步骤

### 1. 克隆仓库

```bash
cd ~/.hermes
git clone --depth 1 https://github.com/NousResearch/hermes-agent-self-evolution.git
```

> ⚠️ **注意：** 使用 `--depth 1` 可以显著减少克隆时间和失败率。如果网络不稳定，可能需要重试。

### 2. 安装依赖（关键：使用 uv + 清华镜像）

**问题：** 国内网络环境下，pip 下载经常超时失败。

**解决方案：** 使用 `uv` 包管理器 + 清华镜像源。

```bash
# 进入项目目录
cd ~/.hermes/hermes-agent-self-evolution

# 使用 uv 安装（自动使用缓存，速度快）
uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple -e ".[dev]"
```

**依赖说明：**
- `dspy>=3.0.0` - 声明式 AI 编程框架
- `gepa` - Genetic-Pareto Prompt Evolution 优化器
- `openai>=1.0.0` - API 调用
- `pytest>=7.0` - 测试框架（dev 依赖）

### 3. 设置环境变量

```bash
# 指向你的 hermes-agent 仓库
export HERMES_AGENT_REPO=~/.hermes/hermes-agent

# 设置 API Key（运行优化时需要）
export OPENAI_API_KEY=sk-xxx
```

### 4. 验证安装

```bash
# 验证模块可导入
~/.hermes/hermes-agent/venv/bin/python -c "import evolution; print('OK')"

# 验证命令行工具
~/.hermes/hermes-agent/venv/bin/python -m evolution.skills.evolve_skill --help
```

### 5. 干跑测试（推荐先做）

```bash
cd ~/.hermes/hermes-agent-self-evolution
export HERMES_AGENT_REPO=~/.hermes/hermes-agent

# 干跑模式 - 验证配置，不实际运行优化
python -m evolution.skills.evolve_skill \
    --skill github-code-review \
    --dry-run
```

## 使用方法

### 基本用法

```bash
# 演化一个技能（使用合成评估数据）
python -m evolution.skills.evolve_skill \
    --skill <skill-name> \
    --iterations 10 \
    --eval-source synthetic

# 使用真实会话历史
python -m evolution.skills.evolve_skill \
    --skill <skill-name> \
    --iterations 10 \
    --eval-source sessiondb
```

### 参数说明

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--skill` | 要演化的技能名称 | 必填 |
| `--iterations` | GEPA 迭代次数 | 10 |
| `--eval-source` | 评估数据来源 | synthetic |
| `--dataset-path` | 现有评估数据集路径 | - |
| `--optimizer-model` | GEPA 反思使用的模型 | - |
| `--eval-model` | 评估使用的模型 | - |
| `--hermes-repo` | hermes-agent 仓库路径 | 从环境变量读取 |
| `--run-tests` | 运行完整测试套件 | false |
| `--dry-run` | 验证配置，不运行优化 | false |

### 推荐实践

1. **从小迭代开始**：先用 `--iterations 3` 验证效果
2. **先干跑**：用 `--dry-run` 确认配置正确
3. **选熟悉的技能**：从你经常用的技能开始演化
4. **看 PR 再合并**：所有更改生成 PR，人工审核后合并

## 当前功能阶段

| 阶段 | 目标 | 状态 |
|---|---|---|
| Phase 1 | 技能文件 (SKILL.md) | ✅ 已实现 |
| Phase 2 | 工具描述 | 🔲 计划中 |
| Phase 3 | 系统提示词 | 🔲 计划中 |
| Phase 4 | 工具实现代码 | 🔲 计划中 |
| Phase 5 | 持续改进循环 | 🔲 计划中 |

## 常见问题

### Q: 安装时 pip 超时怎么办？

**A:** 使用 `uv` + 清华镜像：
```bash
uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple -e ".[dev]"
```

### Q: LiteLLM 报错 "Failed to fetch remote model cost map"？

**A:** 这是警告，不影响功能。LiteLLM 会自动回退到本地备份价格表。

### Q: 如何知道演化效果？

**A:** 每次演化会生成报告到 `reports/` 目录，包含：
- 原始技能 vs 演化后技能对比
- 评估分数变化
- 改进建议

### Q: 需要 GPU 吗？

**A:** 不需要。所有操作通过 API 调用完成，约 $2-10/次优化。

## 注意事项

1. **技能大小限制**：演化后的技能必须 ≤15KB
2. **测试必须通过**：100% 测试套件通过率是硬性要求
3. **语义必须保留**：不能偏离原技能的核心目的
4. **人工审核**：所有更改通过 PR，不能直接提交

## 相关资源

- [官方 README](https://github.com/NousResearch/hermes-agent-self-evolution)
- [PLAN.md](https://github.com/NousResearch/hermes-agent-self-evolution/blob/main/PLAN.md) - 完整架构和路线图
- [DSPy](https://github.com/stanfordnlp/dspy) - 声明式 AI 编程框架
- [GEPA](https://github.com/gepa-ai/gepa) - 遗传 - 帕累托提示演化