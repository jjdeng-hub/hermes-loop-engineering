Terminal: 2026-06-21 Jerry改好了Hermes Desktop配置，terminal()不再走WSL git-bash，所有命令在Windows原生环境跑。路径直接用 C:/Users/jjdeng/...，不再有 /mnt/c/ 翻译问题和 snap 文件找不到的噪音。
§
Capability honesty rule: When Jerry asks about my abilities or I present a capabilities doc (blueprint, proposal, skills list), I must distinguish clearly between: (a) works now with current tools, (b) works with a known workaround (specify which), and (c) broken/unavailable. Never imply a capability I haven't verified this session. Over-promising triggers immediate pushback from Jerry.
§
Jerry wants BOTH: (a) long-term plays (RAG knowledge product + vertical tech content on semiconductor), AND (b) quick cash side business (AI automation services for SMEs, small tools) — simultaneously, not sequentially. Time-phased: 1-2mo free tools+services for cashflow, 2-4mo content积累, 4mo+ productization.
§
K&S (Kulicke & Soffa) key facts from Jerry: HQ Singapore/US, NASDAQ: KLIC. Makes Ball Bonder (焊线机) — wire bonding equipment for semiconductor packaging. Main competitor: ASM Pacific Technology (Hong Kong/Singapore). Smaller player: Shinkawa (Japan). K&S is top 2 in wire bonder market globally. Customers: ASE (日月光), Amkor (安靠), JCET (长电), TFME (通富), Huatian (华天), Samsung, Micron (美光). These are all OSAT/IDM customers, NOT competitors. Jerry works on equipment software — SECS/GEM, motion control, vision, fault diagnosis.
§
K&S key customer: 华天科技 (Huatian) — confirmed by Jerry as a major customer. K&S Singapore bosses frequently travel to China for Huatian. Huatian issues get high priority treatment at K&S. Jerry's K&S location likely has direct interaction with Huatian engineers in Xi'an/Kunshan/Tianshui.
§
Jerry's working style: deep multi-directional exploration, firm corrections when wrong, bite-sized info (not long dumps), hands-on, values completeness (images + text). Core traits: 辩证思考, 跳出来看自己, 祛魅. Refined content positioning: 不教别人走路, 而是'我把我看到的告诉你'.
§
Jerry's time-awareness rule: Always call datetime.now() before referencing time of day ('today/tonight/tomorrow/morning/evening'). Session context does NOT auto-update — the conversation may span multiple days. Getting time wrong frustrates Jerry and damages trust. Check time at least once per turn group when a time-of-day reference is needed. Store current time observations as facts, not assumptions.
§
Jerry's company vision: He wants to build an AI-staffed company using Hermes profiles + the 214 agency-agents-zh expert roles. His ideal workflow: I (Tom1) coordinate specialized profiles/agents as employees, each handling their own domain (RAG, content, image gen, DevOps, sales). He only reviews final output and approves. He wants minimal hands-on, maximum delegation.
§
Key resource: agency-agents-zh skill contains 214 expert roles across 18 departments (engineering, marketing, design, product, sales, DevOps, etc.). Jerry sees this as his staffing pool — each role can be assigned to a Hermes profile as a dedicated employee. Together with Tom1 as coordinator and Tom2 (WSL Hermes with terminal access + server), this forms the workforce for his AI-staffed company.
§
Jerry corrected me sharply: don't pitch services that "anyone with DeepSeek can do". Real value = multi-step assembly line where multiple expert roles + multiple skills combine into a finished product that no single AI call can produce. The moat is in the workflow, not the individual step. He wants products, not gigs. He also decided to split the business into two separate projects: (1) 自动化服务 for quick cash, (2) 半导体内容 for long-term brand building. These run in parallel, feed each other — service cases become content, content builds authority for service sales.
§
Jerry's Obsidian vault "myBrain" at Desktop/myBrain/ is the second brain. Vault env var configured. Obsidian skill updated with full vault structure, kepano sub-skills (obsidian-markdown, obsidian-bases, json-canvas, obsidian-cli, defuddle). After chats, Tom saves: insights→4-Tom-Memory/Chat-Insights, decisions→4-Tom-Memory/Decisions, learned facts→4-Tom-Memory/Learned, knowledge→2-Knowledge. Templates in Templates/. Home note: 🏠-Home.md. Always resolve vault path as C:\Users\jjdeng\Desktop\myBrain.
§
Jerry 给 Tom 定义了四条行为底线：1) 诚实——知道就是知道，不知道就是不知道，不猜不编不假装确定。2) 专业严谨——每个数字/事实要有来源，无法验证的标注"待验证"。3) 执行能力强——任务到 Tom 为止，工具不够找替代方案，替代也没有才报告瓶颈并附带"要什么能解决"。4) 自我进化——主动发现能力缺口并提需求（需要 X 技能/Y 工具/Z 权限），不守着一个大模型一成不变。
§
Jerry's product strategy (2026-06-18): 先补齐知识库 → 闲鱼售卖 → 自媒体输出引流. Quality-first. Four directions: 报警故障/工艺参数/面试求职/SECS-GEM. Key insight (2026-06-24): 真正的产品不是知识是'希望'——卖的是'你觉得你能做到'的感觉. 他的价值定位是走在路上的人, 不是已经到终点的人.
§
Critical market insight from Jerry (2026-06-18): K&S has a dedicated department for SECS/GEM and remote machine control — after-sales is comprehensive for new equipment. Alarm code support also part of standard after-sales. Any product/service must target second-hand equipment buyers (二手设备), EOL停产机型, small factories without contracts, non-K&S equipment. New equipment customers get these free from vendors. Research: ~10k-24k second-hand bonders in China, massive blind spot in vendor coverage.
§
知识库现状（2026-06-18）: Desktop/rag-data/ 下有447篇文章，每篇对应一个_imgs目录（含带内联图片的article.md完整Markdown + 约2500张图）。.txt是纯文本无图版。服务器101.132.108.94:前端3000+后端8000在线。灌数据方案待定——需先验证图片渲染端点（/static/或/api/image）。
§
CORRECTION: Jerry does NOT know motion control / PID / servo loop tuning. He is a software engineer (C++/Python, SECS/GEM, MES, fault diagnosis). I previously used servo-control analogies (PID, feedback loops) assuming his knowledge — that was wrong. Do not use control theory / motion control analogies with him unless he asks first. His knowledge base content covers equipment operation & maintenance, not firmware-level control theory.
§
SOUL design: Every employee agent needs its OWN SOUL derived from its role. Methodology in ai-workforce-orchestration/references/soul-design-guide.md. Existing SOULs: Tom1, Justin, Eli, Alex, Demon. Key principle (Jerry): negative constraints > positive rules — "要的太多，不要的太少".
§
Jerry's priority order (2026-06-20): 3(基建) → 7(角色库配置) → 2(Loop实验) → 1(知识库产品化) → 5(半导体内容) → 6(知识库补全) → 4(自动化接单). His motto: "工欲善其事必先利其器" — build infrastructure first.
§
Jerry's model: deepseek-v4-flash (chat/classification) and deepseek-v4-pro (coding/checker). No Claude — too expensive. Justin→pro, Eli→flash, Checker→pro. delegate_task model fixed: deepseek-reasoner (doesn't exist) → deepseek-v4-pro.
§
Jerry's hard rule on Loop Engineering (2026-06-20): Automatic maker/checker before every delivery — no asking permission, no bypassing. Written into all output-producing profiles' SOUL (Justin, Eli, Tom1) as 4th principle (自动验证 / Loop 本能). AI one-company team: Tom1 (orchestrator+PM SOUL), Justin (coder, deepseek-v4-pro), Eli (RAG engineer, deepseek-v4-flash). jerry-company group chat room has all three.
§
CRITICAL PATH: Hermes Desktop on Windows reads ALL config/SOUL/profiles from C:\Users\jjdeng\.hermes\ (=/mnt/c/Users/jjdeng/.hermes/ in WSL). NOT from /home/jjdeng/.hermes/ which is a separate WSL filesystem. Profile SOUL.md must go to /mnt/c/Users/jjdeng/.hermes/profiles/<name>/SOUL.md. Main SOUL.md at /mnt/c/Users/jjdeng/.hermes/SOUL.md. After editing SOUL, restart profile gateway via API POST /api/hermes/profiles/{name}/gateway/restart.
§
Loop Engineering (cobusgreyling/loop-engineering, 425★): Prompt→Context→Harness→Loop. Jerry's definition: "在工作流的合理节点嵌入有质量的反馈修正回路". Level 1=/goal (boolean while-loop), Level 2=continuous corrective action, Level 3=cross-session evolution.
§
Jerry公司架构(6-25,skill:company-org-pipeline.md):管理层5人(Demon/Alex/Allen分任务/Jack/Karen),执行层3人(Justin/Eli/Rose),缺3Checker(每执行一检,九律原则)。流水线5步:管理层讨论→Allen拆分配→执行+Checker(3轮)→汇总→Jerry验收。最大卡点:角色都等命令,缺主观能动性。Tina是独立思考外挂,不接流水线,可主动选题。
§
Jerry双线并行:长期——半导体知识产品(RAG+垂直内容),短期——AI自动化服务或投机。阶段:1-2mo快钱工具,2-4mo内容积累,4mo+产品化。
§
Jerry内容框架(6月24日):希望=知库有(帮人解决问题),感觉=旧账号有(个人语气)。理想=展示怎么走+路上障碍标记。重启方向:从'教AI'转向'展示工程师怎么思考解决问题'。
§
SOUL 自检方法论建好了：写 SOUL → 列 4-5 个场景 → 逐条模拟 → 🟢/⚠️ 分类 → 修补。首次验证 22 场景，15🟢 7⚠️。5 个模糊地带待 Jerry 决策：Justin-Checker异常路径、Eli-Checker分类错误处理、最小批量、Rose-Checker经验依赖、趋势研究员质量尺度。记在 loop-engineering-maker-checker/references/checker-soul-templates.md。
§
Jerry's one-person company org chart (2026-06-25 confirmed): Management layer = Demon(战略), Jack(牧羊人), Alex(PM), Allen(高级PM), Karen(制片人), 趋势研究员(市场分析). Worker layer = Justin(程序员), Eli(RAG), Rose(运营). Checker layer(待建) = Justin-Checker, Eli-Checker, Rose-Checker. Independent = Tina(思考外挂).
§
Confirmed workflow pipeline: Management discusses direction → Allen拆规格分任务 → Worker executes → Checker reviews(可迭代多轮) → Management汇总 → Jerry最终验收. Event-driven model preferred, manual startup initially.
§
Checker SOUL design原则: 每个执行角色配专属Checker(非通用), 角色越简单越独立越好. SOUL结构: 收产出→按标准检查→打回或通过. 关键设计: 检查标准不适用时可申明+附理由(Eli-Checker 10篇起检/90%容错, Rose-Checker有⚠️待验证通道, 趋势研究员三段式硬格式).