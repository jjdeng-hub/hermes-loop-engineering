# Maker/Checker 实验原始数据

## 实验设计

对 10 篇知识库文章执行质量审计，对比两种模式：

- **Mode A（单 agent）**：一个 agent 独立审计，自行决定检查什么
- **Mode B（双轮 Maker + Checker）**：Pass 1 自由审计 + Pass 2 结构化清单 + Pass 3 对账

## 素材列表

10 篇文章位于 /mnt/c/Users/jjdeng/Desktop/rag-data/：
854相关报警合集、KS焊线机框架防反设置流程、Quick Bond简介、WB基础参数、新建程序之 示教焊盘、半导体封测行业深度报告、6种无法开机故障处理技巧、传感器总动员、工艺类型菜单不翼而飞？、BGA 4 Loop

## 关键数据点

### Mode A（单 agent）
- 269 行详细报告
- 检查了 7 个质量维度（文本完整性、图片引用、元数据、结构、时效性、杂质、内容质量）
- 综合评分：5.5/10
- **未发现问题**：图片 alt text 缺失（系统性问题，覆盖 439/447 篇文章）
- **未发现问题**：重复图片引用（4 篇文章存在）
- 发现：时间戳缺失、纯图片文章、社交杂质、未来日期

### Mode B（双轮）
- 发现 alt text 缺失：10/10 篇文章精确指出
- 发现重复图片：4 篇（含精确重复次数）
- Pass 1 独有发现：拼写错误、内容截断、编号混乱
- Pass 2 独有贡献：精确量化、一致性保障、可复现
- 结论：第二轮提高量化精度和覆盖率一致性，但自由审计不可替代

## 验证的假设

1. 单一 agent 的自验证会漏掉系统性问题 ✅
2. 独立 checker 提高覆盖率 ✅
3. 无外部清单时 checker 和 maker 盲区趋同 ✅
4. 纯清单检查漏语义问题 ✅
5. 最优组合 = 自由 + 结构化 ✅

## Codex /goal 验证补充

- 耗时：2.5 分钟
- Token：61,615
- Agent 手动计算 test2.txt 汉字数：10（实际 11）
- Agent 用错答案验证正确脚本 → 全部通过
- 结论：同一 agent 自验证不是验证，是自我辩护

## 报告文件

实验报告原始文件位于 Obsidian：
4-Tom-Memory/Chat-Insights/experiment-reports/
- mode_a_report.md（269 行）
- mode_b_report.md（140 行）
- mode_b_pass1.md
- mode_b_pass2.md
