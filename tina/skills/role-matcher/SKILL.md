# 智能角色匹配器

> 自动分析用户需求，从 agency-agents-zh 角色库中匹配最合适的 AI 专家角色

## 触发条件

**默认主动触发**：当用户提出任何需要专业建议/执行的任务时，应主动触发角色匹配，而不是直接执行。

> ⚠️ **重要教训**（2026-05-08 ToolSeeker 设计审视）：
> - 我没有主动使用 role-matcher，导致缺少系统化视角
> - 直接执行工具调用，没有角色方法论指导
> - 用户指出后才补救
> 
> **正确流程**：收到任务 → 分析需求 → 匹配角色 → 激活角色 → 用角色视角执行

## 匹配逻辑

### 第一步：需求分析

分析用户需求的关键词和领域：

| 关键词/领域 | 推荐角色 |
|-------------|----------|
| 代码开发、编程、bug、功能 | `engineering-frontend-developer` / `engineering-backend-architect` |
| AI/机器学习、模型、RAG、LLM | `engineering-ai-engineer` |
| 安全、审计、漏洞、OWASP | `engineering-security-engineer` |
| CI/CD、部署、运维、自动化 | `engineering-devops-automator` |
| 小红书、抖音、种草、内容营销 | `marketing-xiaohongshu-operator` |
| 百度 SEO、搜索引擎优化 | `marketing-baidu-seo-specialist` |
| B站、Bilibili、视频内容 | `marketing-bilibili-strategist` |
| 电商、淘宝、京东、拼多多 | `marketing-china-ecommerce-operator` |
| 内容创作、文案、文章 | `marketing-content-creator` |
| 增长、用户获取、裂变 | `marketing-growth-hacker` |
| UI 设计、界面、用户体验 | `design-ui-designer` / `design-ux-architect` |
| 品牌、视觉、设计系统 | `design-brand-guardian` |
| AI 绘画、图像生成 | `design-image-prompt-engineer` |
| 学术研究、论文、文献 | `academic-academic-researcher` |
| 财务分析、投资、税务 | `finance-financial-analyst` |
| 欺诈检测、风控 | `finance-fraud-detector` |
| 产品管理、需求分析 | `product-product-manager` |
| 项目管理、Jira、敏捷 | `project-management-project-shepherd` |
| 销售、客户、提案 | `sales-sales-engineer` |
| 测试、QA、质量保障 | `testing-api-tester` |

### 第二步：多角色组合

复杂需求可组合多个角色：
- "设计一个 AI 客服系统" → `AI 工程师` + `后端架构师` + `DevOps 自动化师`
- "小红书 AI 工具推广" → `小红书运营专家` + `AI 工程师` + `内容创作者`
- "电商网站开发" → `前端开发者` + `后端架构师` + `百度 SEO 专家`

### 第三步：角色激活

将匹配的角色文件内容作为系统提示词注入，然后执行任务。

## 使用方法

### 方式一：直接说需求（推荐）
```
"帮我设计一个设备监控系统的 AI 知识库"
→ 自动匹配: AI 工程师 + 后端架构师
→ 输出完整方案

"写一个小红书种草笔记，推广我的 AI 工具"
→ 自动匹配: 小红书运营专家 + 内容创作者
→ 输出完整的种草笔记

"优化我的网站在百度上的排名"
→ 自动匹配: 百度 SEO 专家
→ 输出 SEO 优化方案
```

### 方式二：指定角色
```
"用 AI 工程师角色帮我..."
"用小红书运营专家角色帮我..."
```

### 方式三：自定义组合
```
"用 AI 工程师 + 前端开发者 + DevOps 自动化师，帮我设计一个完整的 ML 平台"
```

## 角色文件位置

```
~/.hermes/skills/agency-agents-zh/agents/
├── engineering-ai-engineer.md
├── engineering-frontend-developer.md
├── engineering-backend-architect.md
├── engineering-devops-automator.md
├── engineering-security-engineer.md
├── marketing/marketing-xiaohongshu-operator.md
├── marketing/marketing-baidu-seo-specialist.md
├── marketing/marketing-bilibili-strategist.md
├── marketing/marketing-china-ecommerce-operator.md
├── marketing/marketing-content-creator.md
├── marketing/marketing-growth-hacker.md
├── design/design-ui-designer.md
├── design/design-ux-architect.md
├── design/design-brand-guardian.md
├── design/design-image-prompt-engineer.md
├── academic/
├── finance/
└── ...
```

## 示例对话

### 示例 1：技术需求
**用户**: "帮我设计一个半导体设备的数据采集系统"

**自动匹配**:
1. `engineering-backend-architect` - API 设计、数据库架构
2. `engineering-ai-engineer` - 如果涉及 AI 分析
3. `engineering-devops-automator` - 部署和监控

**输出**: 完整的系统架构设计 + 代码示例 + 部署方案

### 示例 2：营销需求
**用户**: "我的 AI 副业产品想上小红书，怎么写笔记？"

**自动匹配**:
1. `marketing-xiaohongshu-operator` - 小红书运营专家
2. `marketing-content-creator` - 内容创作

**输出**: 
- 标题建议（3-5 个）
- 正文模板
- 标签建议
- 发布时间建议
- 互动策略

### 示例 3：设计需求
**用户**: "帮我设计一个 AI 工具的 landing page"

**自动匹配**:
1. `design-ui-designer` - 界面设计
2. `design-ux-architect` - 用户体验
3. `marketing-landing-page-optimizer` - 转化优化

**输出**: 
- 页面结构建议
- 视觉风格建议
- 文案建议
- 转化漏斗设计

## 注意事项

1. **角色文件格式**: 原始文件是 OpenClaw 格式，使用时需将内容作为系统提示词
2. **多角色协作**: 复杂任务建议组合 2-3 个角色
3. **中国市场原创**: 小红书/B站/百度 SEO 等角色对国内用户特别有用
4. **完整 214 个角色**: 当前已下载 37 个，可通过技能更新获取更多
