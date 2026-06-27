# Mode A vs Mode B 实验数据

日期：2026-06-20

## 实验说明

对知识库 10 篇半导体封装文章做质量审计，验证 maker/checker 分离是否能提升审计质量。

完整实验过程和结论见 Obsidian：
- `4-Tom-Memory/Chat-Insights/2026-06-20 Loop Engineering 实验全记录.md`
- `4-Tom-Memory/Chat-Insights/experiment-reports/mode_a_report.md`
- `4-Tom-Memory/Chat-Insights/experiment-reports/mode_b_report.md`
- `4-Tom-Memory/Chat-Insights/experiment-reports/mode_b_pass1.md`
- `4-Tom-Memory/Chat-Insights/experiment-reports/mode_b_pass2.md`

## 关键发现

| 指标 | Mode A（单 agent） | Mode B（maker + checker） |
|------|:---:|:---:|
| 发现 alt text 缺失 | ❌ 未提出 | ✅ 10/10 篇 |
| 发现重复图片引用 | ❌ 未发现 | ✅ 4 篇含精确次数 |
| 量化精准度 | 印象式 | 精确计数 |
| 报告长度 | 269 行 | 140 行 + 两份中间稿 |
| Token 消耗 | 中（单轮） | 更高（双轮） |

## 核心结论

1. 没外部清单时，checker 和 maker 盲区趋同（Verifier Theater）
2. 纯清单检查发现不了语义问题（拼写错误、内容截断）
3. 最优 = 自由审计 + 结构化检查（human reviewer + CI/lint）
