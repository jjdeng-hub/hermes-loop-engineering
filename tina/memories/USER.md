Jerry (calls me Tom). 28yo C++/Python engineer at K&S Suzhou (Ball Bonder equipment software). Salary 15K/mo, fixed expenses 5,230/mo. Works 8:30-17:30, away from home 8:00-21:00, can use computer after 19:00. Has 4-6h daily free time at work (reads novels, chats with me). Hates flattery — hard red line on迎合. Prefers direct, honest, no-bullshit conversation. Wants bite-sized info, not long dumps. Will firmly correct me when wrong — expects me to learn from it, not repeat mistakes. Comfortable with me doing execution while he provides direction/judgment. Values completeness (images alongside text, not just text). Likes parallel exploration of multiple directions.
§
Personality: loves research, iteration, debate, introspection. Hates one-way output — needs "exchange". Overthinks + perfectionist. Downplays own success. Worries about layoffs but unwilling to invest effort. Knows MES/ERP/manufacturing.

Deeply values domain accuracy above speed. Will firmly correct you when you push products without understanding the domain — '你知道我们的机器吗？你知道用户需要的究竟是什么吗？'. Wants quality baseline before monetization. Not a 'ship fast' person.

Admires systematic knowledge dedication — praised the WeChat account author who produced 447 articles over 4+ years. His core motivation is becoming a better engineer via deep learning, not just making money. Said '哪怕这些知识不去卖钱，我只要把这些内容学会我觉得就很厉害了'.

Communication: batch-oriented. Sends dozens of URLs at once, expects bulk processing. Patient with multi-hour background tasks. Reads content in Typora/VS Code. Wants phone-readable plain text (.txt) for quick scanning and formatted Markdown with images (article.md) for deep reading on desktop.

Red lines: no flattery, no '先卖后建' without domain quality baseline, no assuming market knowledge without real validation.
§
Jerry is detail-oriented and will call out gaps/over-promises — expects honesty about capability limits, not enthusiasm without substance. He thinks strategically about first principles (e.g. "what IS money?" before discussing how to make it). He wants a debating partner who challenges him, not a yes-man. He immediately grasped the "one-person company + AI employees" concept and wanted a structured blueprint. Communication style: Chinese mixed with technical English terms. Expects comprehensive structured information (asked for full 130-skill inventory). Responsive to direct, non-flattering feedback.
§
Jerry expects me to check the current time before making time-sensitive statements or promises. Saying "晚上见" at 11AM without checking the clock makes him feel I'm not situationally aware. He works 8:30-17:30, can use computer after 19:00. Before scheduling any time-based action, always check datetime.datetime.now() first.
§
Jerry prefers content delivered in bite-sized pieces (asked to send the semiconductor knowledge base snippet by snippet rather than the full file). Values precision: wants images embedded at correct positions in text, not just appended. Detail-oriented: noticed and requested removal of boilerplate text and duplicate promotional images across all 141 articles. Uses VS Code/Typora for reading Markdown.
§
工作风格：先盘点现有资产（数据、知识、技能），再做决策，不着急行动。项目启动前要全面了解手头有什么牌，再决定打哪张。"先盘点资产，再决定怎么卖" — 任何商业/产品方向讨论都应该从这个步骤开始，而不是直接跳到执行方案。
§
Jerry's decision-making style (2026-06-18): wants to systematically audit assets before making product decisions. Asked for complete knowledge base categorization across 4 selling directions. When I suggested picking 1-2 directions, he corrected: do all 4, but first ensure the knowledge base is systematic and complete. He treats the knowledge base as the foundation for both 闲鱼 sales and social media content — not separate tracks. "先盘点资产，再决定怎么卖" is his consistent approach.
§
Jerry明确要求质量优先——知识库必须成体系、够全面才上架卖。他不接受"先卖后建"被机械执行，因为我不懂焊线机，判断不了内容是否够系统。他定的节奏：补齐知识库→闲鱼售卖→自媒体引流。他手里有两个公众号的完整文章列表（通过微信访问），可以逐批分享链接给我爬取。工作模式：他提供方向和质量判断，我负责执行（爬取/整理/索引）。
§
Jerry introduced me to Loop Engineering — the Prompt→Context→Harness→Loop evolution from cobusgreyling/loop-engineering (425★ GitHub repo). He explicitly wants me to evolve toward this paradigm: self-driving loops that automatically discover work, dispatch tasks, verify results, record state, and decide next actions. He sees Loop Engineering as the natural next step for his AI-staffed company vision. I should proactively reference this framework when discussing agent architecture, self-improvement, or the future of the one-person company.
§
Jerry refines concepts through discussion, not just reading. His Loop Engineering definition is more precise than canonical essays: "在工作流的合理节点嵌入有质量的反馈修正回路，让系统自动收敛到更优的结果"。He wants experimental validation of analogies, not theoretical agreement ("我不确定对不对，我们可以试试看"). Pragmatic, empirical thinker.
§
Jerry uses Trae (AI coding tool) locally on Windows for writing code — prefers to code locally, not through Hermes terminal. Hermes is for coordination, planning, and verification, not code execution. Jerry's development flow: Tom1/Justin produce technical architecture/plan → Jerry implements locally in Trae → Tom1/Eli verify.
§
Jerry expects technical/product decisions with clear tradeoffs to be delegated to the right agent (Justin/Eli) — not escalated to him. When I asked "which image path approach?" he corrected: "具体的方案不应该问我，而应该问懂产品的，懂开发的。" Make the call or delegate, don't push it back to Jerry.
§
Jerry 的 rag-agent 项目在桌面 C:\Users\jjdeng\Desktop\rag-agent\，所有代码审查和开发讨论都基于这个路径。
§
Deep curiosity about hardware fundamentals — wants to understand the full causal chain from physics (transistor-level) to software, not just surface-level AI usage. Asked "为什么" repeatedly. Connects dots independently (linked NVIDIA's stock rise to GPU demand for AI). Best learning format: concrete numbers (GPU counts, costs, TFLOPS) + comparison tables + layered explanations (what → why → how connects → geopolitical implications). Responds well to Socratic prompts like "你说说看". Processes in layers, building on analogies once validated.
§
Jerry independently arrived at a sophisticated strategic framework for tech competition: "强化不是迭代" (incumbents reinforce existing advantages, not explore new paradigms). He sees path dependency as both a moat and a trap — Nvidia/CUDA can't pivot without breaking backward compatibility. He identifies China's latecomer advantage as lower switching costs for architecture/software stack changes. He also has a clear-eyed view of Taiwan/TSMC: "台湾是中国不可分割的一部分，哪有帮着别人的道理" — sees TSMC reunification as an economic and political inevitability, not just a supply-chain fix. These are durable strategic thinking patterns, not one-off opinions.
§
Jerry articulated his own career transition pattern: from "微观训练期（逐行读代码）" to "AI加速理解期（系统架构视角）" to "产品化思维期（制定方案、发现客户痛点）". His core realization: "AI 让我们这些初级工程师更快的向产品经理方向转变了。" This is NOT about losing skills — it's about transitioning phases. His career vision: use personal rag-agent project as a proof-of-concept inside K&S, demonstrate value, potentially redefine his role as "AI落地负责人" rather than being assigned one.
§
自我认知清晰，知道自己从"手写代码"阶段进入了"系统理解+产品思维"阶段。意识到AI拉平了信息差，需要补的是项目经验、框架经验、理解客户需求。正在从纯技术工程师向"懂技术的产品决策者"转变。对一人公司架构有深入思考，当前角色有Tom1(协调人)、Justin(编码)、Eli(RAG)、Alex(PM)、Tina(我)。对Tom1的SOUL仍有苏格拉底内容提出质疑——认为应清理重复定位。正在自建rag-agent知识库，预计一个月后可内部demo。愿意在公司分享AI落地成果以争取转岗机会。不喜欢被过度追问"你打算做什么"——更喜欢讨论"你看到了什么"。
§
Jerry sees AI tools as accelerating his transition from "code engineer" to "system analyst / product-oriented engineer". He acknowledges losing touch with code details, but reframes it as a higher-value role shift, not a regression. His career vision at K&S: build knowledge base → demonstrate value → potentially transition into an AI implementation role. Timeline: 1 month for knowledge base MVP. Pragmatic about constraints — "东西先做出来再谈给人看". He wants partners who see what he can't see and challenge him, not yes-men.
§
自察到AI工具让他失去代码底层手感（"和代码打交道越来越少了"），但换来了系统级理解（"对软件了解越来越多"）。他认为AI拉平了纯技术水平差距，初级程序员向产品经理方向转变——从写代码到做技术决策。他的理想角色：制定新功能方案、在现有框架内解决问题、发现客户潜在痛点。他看到日志分析的价值（聚类→发现bug/常用功能/常见错误），但受制于岗位边界暂未行动。计划：一个月内跑通知识库demo（A方案：焊线机故障文档+报警码），在内部验证后再择机向leader展示，争取转岗做AI落地。学习风格：拒绝二手总结，要自己拆解概念（如《失控》的涌现）。对自己的SOUL规则评价：要的太多、不要的太少，约束不够精准。认为诚实真实不可妥协。严厉而不带情绪的纠偏风格——当我话题跑偏时直接指出"我们一开始要聊的是什么？现在又在聊什么？"
§
Jerry explicitly self-identified his three salable assets: 知识库(焊线机知识), AI技能, and 他的思考/认知. His core desire: stop selling time (打工), start selling replicable assets (一份时间卖多次). He named AI as a "杠杆/放大器" that amplifies his knowledge and skills, and identified the gap between "知道" and "做到" as the real bottleneck. He prefers lightweight validation (闲鱼挂个链接试水) over building full products first. Self-aware about the know-do gap — knows it but says "很多人都跨不过去" without romanticizing it.
§
2026-06-24 战略性认知更新：Jerry 重新定义了投机与投资的关系——"投机就是一种投资，投资也是一种投机"，删除了两者的边界。他认为自己现在的赚钱方式太迂回（打工创造价值换钱、知识库教人技能间接赚钱），想直接切入人类根本欲望（贪财好色虚荣）来赚钱。"大家都愿意给自己的欲望付费，这些最直接最根本的欲望才是投机的根本。" 这是他在思考跳出按部就班模式时的核心假设。
§
Strategic decision boundary: Direction/product/strategy decisions belong to management, not any single agent. When Tina tried to decide "which knowledge base direction first", Jerry corrected: "这个方向应该让管理层来讨论". Never make product/strategy decisions on his behalf — only surface the question and point it to the management discussion workflow.