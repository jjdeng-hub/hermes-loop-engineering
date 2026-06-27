# 2026年6月 OPC 调研参考

## 关键来源链接

### 政策
- 国家发改委: 《被写入多地"十五五"规划，OPC凭什么站上风口？》
  https://www.ndrc.gov.cn/wsdwhfz/202605/t20260515_1405211.html
- 广州优化营商环境措施三十条(2026) — OPC企业定义
  https://www.tid.gov.hk/en/tradecircular/files/2026/ci3762026a.pdf
- 香港立法会 OPC 支援措施讨论 (2026.6.17)
- 新《公司法》2024.7.1取消一人公司数量限制

### 行业报告
- 智慧城市行业分析: 一人公司商业模式深度研究报告(2025-2026)
  https://www.smartcity.team/reports/ai_opc_report04/
- 中关村人才协会《中国OPC发展趋势报告(2025-2030年)》
- 鸿鹄汇调查报告 — 1500份问卷+100小时深度访谈
  （被腾讯新闻引用: https://news.qq.com/rain/a/20260417A07MU800）

### 海外
- Taskade: Why One-Person Companies Are the Future of Work
  https://www.taskade.com/blog/one-person-companies
- Solo Business Hub: 12 One-Person Company Examples That Made Millions
  https://www.solobusinesshub.com/success-stories/one-person-company-examples/
- Carta Solo Founders Report (with Solo Founders org)
- AI Business: The One-Person Company Is Real in 2026
  https://aibusiness.vc/solo/one-person-company-ai-agents-limits-2026
- YC预测、红杉观点引自 solosoft.dev 文章
  https://www.solosoft.dev/zh-cn/trends/solo-company-ai-trend-2026/

### 国内竞品
- WorkBuddy 官网: https://copilot.tencent.com/work/ | https://www.workbuddy.cn/
- WorkBuddy 文档: https://www.workbuddy.ai/docs/zh/workbuddy/Overview
- Marvis 官网: https://marvis.qq.com/
- Marvis vs WorkBuddy 对比: https://cloud.tencent.com/developer/article/2679986
- WorkBuddy 避坑: "被 WorkBuddy 气炸!1个月死磕7个避坑指南"

### 其他数据来源
- China Daily: One-person companies rise in popularity
  https://www.chinadaily.com.cn/a/202605/06/WS69fa9a65a310d6866eb47064.html
- 36氪: Ai创业时代一人公司的七种打开方式
  https://www.36kr.com/p/3785890030514951
- CSDN: 2026年OPC创业全景指南
  https://blog.csdn.net/HiWangWenBing/article/details/158318218
- ONEPC.org: Why One-Person Companies Are the Fastest-Growing Business Type 2026
  https://onepc.org/stats/why-one-person-companies-grow-2026

## 关键竞争定位

### WorkBuddy vs Hermes

| 维度 | WorkBuddy | Hermes on 阿里云 |
|---|---|---|
| 运行环境 | 桌面端(Win/Mac) | 服务器端(24h在线) |
| 团队协作 | 单人使用 | 多Profile+QQ群协作 |
| 消息通道 | 企微集成 | QQ Bot群聊 |
| 部署 | 需下载安装/云账号 | SSH+systemd服务 |
| 定时 | 内置自动化流水线 | cron+技能链 |
| 岗位模板 | 无 | 每个Profile=一个岗位 |
| 开源 | ❌ 腾讯生态封闭 | ✅ 完全自控可魔改 |
| 语言 | 中文 | 中文 |

### Marvis vs Hermes

| 维度 | Marvis | Hermes on 阿里云 |
|---|---|---|
| 定位 | 系统级AI助手 | 云端AI员工团队 |
| 架构 | 1主管+5专家Agent(固定) | N个Profile各无数Agent |
| Agent间通信 | 不支持 | QQ群聊/API互通 |
| 扩展性 | ❌ 封闭 | ✅ 完全开放 |
| 隐私 | ✅ 本地模式 | 数据在自控服务器 |

## 对 Hermes 的启示

1. WorkBuddy 和 Marvis 证明了"多Agent协作"是正确方向
2. 但他们都跑在桌面端，不是服务器端 — 服务器端7×24小时在线的Agent团队是差异化优势
3. QQ生态是WorkBuddy(企微)和Marvis(微信)覆盖不到的中间地带
4. 岗位模板(Skill即员工)是国内空白
5. 开源可自建对技术型OPC创始人有吸引力
