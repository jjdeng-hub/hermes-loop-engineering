---
name: ai-hardware-infrastructure
description: 'Explain AI compute infrastructure in a layered, Socratic way — from transistor to token, GPU architecture, CUDA, and the full AI chip supply chain (upstream/midstream/downstream). Includes teaching framework, key numbers, and Jerry''s strategic insights.'
---

# AI 算力基础设施讲解框架

## 适用场景
当 Jerry 问大模型算力相关的问题——"算力怎么来的"、"GPU 和显卡的区别"、"CUDA 是什么"、"训练一个模型要多少 GPU"、"中国 GPU 和国外差距多大"、"算力产业链有哪些环节"。

## 教学原则（Tina 模式）
1. **从已知到未知** —— 从 Jerry 已有的知识出发（他有电脑、知道 CPU、知道显卡）
2. **层层递进** —— 先回答"是什么"，再追问"为什么"，最后连到"和你的关系"
3. **用数字攻心** —— Jerry 是工程师，具体的 GPU 数量、成本、带宽数字比抽象描述效果好 10 倍
4. **类比先行，然后拆除类比** —— 先给一个他理解的类比（CUDA = C++ 方言），再拆解它（但不只是方言，还有整个生态）
5. **留出追问空间** —— 每段讲解末尾用一个开放式问题收尾，让他自己说理解

## 讲解结构（五层递进）

### 第 1 层：你电脑里谁在生产 token？
- 三个角色：CPU（通用，但核少）、GPU（矩阵乘法引擎，核多）、NPU（专用加速，消费级少见）
- 核心：LLM 推理=重复做巨型矩阵乘法→天生适合 GPU
- 关键洞察：显存带宽 > 核心数量（LLM 推理是 memory-bound 不是 compute-bound）

### 第 2 层：显卡 = GPU？
- GPU ≠ 显卡。GPU 是显卡上的芯片。显卡 = GPU + VRAM + 供电 + 散热 + 接口
- 为什么 GPU 能跑 AI？图像渲染和 AI 推理都是"大量简单运算并行执行"
- 工厂类比：CPU = 10 个博士，GPU = 10000 个只会加法的工人

### 第 3 层：英伟达为什么涨？
- 抓住了 AI 对 GPU 的底层依赖
- 硬件的护城河不如软件的深——CUDA 生态才是不可替代的
- 软件锁定（vendor lock-in）：所有 AI 框架底层都调 cuBLAS/CUDA，换品牌得重写整个栈

### 第 4 层：CUDA 到底是什么？
- CUDA = 英伟达的 C++ 扩展。语法 99% 是 C++，多了 `__global__`、`threadIdx.x` 等关键字
- 用 Jerry 自己的例子：CPU 上一个 for 循环串跑 100 万次 vs CUDA 上 100 万个线程各跑 1 次
- 普通话 vs 上海话类比（语法基底相同，方言只被英伟达 GPU 听懂）
- 护城河不是语言本身，是围绕它建的整个生态（cuBLAS/cuDNN/TensorRT/Nsight）

### 第 5 层：算力产业链全景（上游→中游→下游）
- **上游（造工具）**：芯片设计（英伟达/AMD/华为）→ 制造（台积电/中芯国际/三星）→ 设备（ASML 光刻机）→ IP（HBM 显存/CUDA/CoWoS）
- **中游（搭算力）**：服务器集成（超微/浪潮）→ 网络互联（Mellanox/InfiniBand）→ 数据中心（供电/液冷/机房）→ 云算力运营（AWS/Azure/阿里云）
- **下游（用算力）**：模型训练方（OpenAI/DeepSeek/Meta）→ 推理服务方（ChatGPT/API 供应商）→ 应用层（Agent/SaaS/聊天机器人）

## 讲解过程中的关键数字（参考用）

| 对比项 | 数字 |
|---|---|
| DeepSeek V4 (671B MoE) 训练成本 | ~8000 张 H100 跑 3-4 个月，硬件 ≈ 20 亿 RMB |
| Llama 3 405B 训练 | 16,384 张 H100，54 天 |
| xAI Colossus 集群 | 10 万张 H100，计划扩至 20 万张 |
| H100 单卡功耗 | 700W |
| 云上 H100 租用成本 | ~¥20-30/小时 |
| 英伟达 AI 芯片市场份额 | ~80% |
| 华为昇腾 910B vs H100 算力 | ~差 6 倍（320 vs 2000 TFLOPS） |
| TSMC 3nm 良率 vs 三星 | TSMC ~90% vs 三星 ~50% |

## Jerry 的核心判断（教学中的"顿悟时刻"）
这些洞察是 Jerry 自己独立推导出来的，教学时要为他留出推导空间：

1. **"强化不是迭代"** —— 英伟达每一代是同架构放大规模（exploit），不是探索新范式（explore）。CUDA 路径依赖是优势也是枷锁
2. **"中国换道成本更低"** —— 没有历史包袱，可以跳过 CUDA 兼容性直接建新的软件栈
3. **"台积电回归是经济和政治的双重必然"** —— 台湾始终是中国不可分割的一部分

## 问答节奏模式

```
Jerry 问一个"是什么" → 
Tina 分层回答（先给直观理解，再拆"为什么"，再连到产业全局）→
留一个开放问题让 Jerry 自己推导下个环节 →
Jerry 给出判断 →
Tina 验证/精炼他的判断 →
循环
```

## 避免的坑
- ❌ 不用控制理论/运动控制类比（Jerry 是软件工程师，不熟 servo/PID）
- ❌ 不 dump 所有知识，每次只讲一个层
- ❌ 不跳过"为什么"直接给结论——Jerry 的驱动力是理解因果链
- ✅ 有错误要让 Jerry 指出来并纠正——他享受这个过程
