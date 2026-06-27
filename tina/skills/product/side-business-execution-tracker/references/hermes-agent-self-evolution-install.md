# hermes-agent-self-evolution 安装指南

## 项目信息
- **仓库**：https://github.com/NousResearch/hermes-agent-self-evolution
- **Stars**：2,738
- **许可证**：MIT
- **核心依赖**：DSPy 3.2.0, GEPA 0.0.27, LiteLLM

## 安装步骤

### 1. 克隆仓库
```bash
cd ~/.hermes
git clone --depth 1 https://github.com/NousResearch/hermes-agent-self-evolution.git
```

### 2. 安装依赖（使用 uv + 清华镜像，解决网络超时问题）
```bash
cd ~/.hermes/hermes-agent-self-evolution
uv venv .venv --python 3.11
uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple -e ".[dev]"
```

> ⚠️ 注意：pip 直接从 files.pythonhosted.org 下载容易超时，使用 uv + 清华镜像可大幅加速。

### 3. 验证安装
```bash
cd ~/.hermes/hermes-agent-self-evolution
. ~/.hermes/hermes-agent/venv/bin/activate
python -m evolution.skills.evolve_skill --skill github-code-review --dry-run
```

### 4. 配置环境变量
```bash
export HERMES_AGENT_REPO=~/.hermes/hermes-agent
export OPENAI_API_KEY=sk-xxx  # 真实运行时必需
```

## 使用示例

### 演化一个技能（合成评估数据）
```bash
python -m evolution.skills.evolve_skill \
    --skill github-code-review \
    --iterations 10 \
    --eval-source synthetic
```

### 使用真实会话历史
```bash
python -m evolution.skills.evolve_skill \
    --skill github-code-review \
    --iterations 10 \
    --eval-source sessiondb
```

### 干跑模式（验证配置）
```bash
python -m evolution.skills.evolve_skill \
    --skill github-code-review \
    --dry-run
```

### 运行完整测试套件
```bash
python -m evolution.skills.evolve_skill \
    --skill github-code-review \
    --iterations 10 \
    --run-tests
```

## 当前功能阶段
| 阶段 | 目标 | 状态 |
|---|---|---|
| Phase 1 | 技能文件 (SKILL.md) | ✅ 已实现 |
| Phase 2 | 工具描述 | 🔲 计划中 |
| Phase 3 | 系统提示词 | 🔲 计划中 |
| Phase 4 | 工具实现代码 | 🔲 计划中 |
| Phase 5 | 持续改进循环 | 🔲 计划中 |

## 注意事项
1. **LiteLLM 网络超时警告** — 不影响功能，会自动回退到本地备份
2. **真实运行需要 OpenAI API Key** — dry-run 不需要
3. **每个变体必须通过测试** — 100% 测试套件通过率是约束门
4. **所有更改通过人类审查** — 不会直接 commit
