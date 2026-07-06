# 2026-07-06 Creator Profile 搭建完成

## 做了什么

1. **Creator profile 创建**
   - 路径: `/root/.hermes/profiles/creator/`
   - 主模型: deepseek/deepseek-v4-flash
   - MoA: opencode-go (glm-5.2 / qwen3.7-max / deepseek-v4-pro)

2. **飞书 Bot 凭证确认**
   - 共 5 个 bot，凭证存于 `wiki/entities/feishu-bots.md`
   - Creator 用 `cli_aacba44c0638dbc9`
   - fitness / learner 待用

3. **Soul 重写**
   - 底层 OS = Jerry 认知框架（旧变量/新变量/进化算法/自主性）
   - 二层 = 外部成熟 skill
   - 不代笔、不教不吓

4. **从 GitHub 安装了 3 个成熟 skill**
   - `xhs-title-skill` — 8个标题模板+情绪化叠加（来源: ren644, ⭐19）
   - `rednote-write` — 小红书写作流程+两道关审查（来源: aislinn-yang）
   - `human-pen` — 零AI痕迹写作+黑名单词库（来源: ymstar, ⭐4）

5. **选题库多维表格升级**
   - 新增「正文」字段
   - 第一篇正文已回填

6. **Gateway 启动**
   - Creator 飞书 bot 已连接

## 当前状态

- Tom (default) → 系统运维、cron、对抗审查
- Tina (tina) → 哲学追问
- Creator (creator) → 内容创作（新）
