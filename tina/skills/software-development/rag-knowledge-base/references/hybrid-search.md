---
name: rag-hybrid-search
description: BM25 + 向量语义 + RRF 混合检索 — 解决 RAG 中精确关键词与模糊语义不可兼得的经典问题
version: 1.0.0
---

# skill: rag-hybrid-search

## 触发条件
- 用户需要提升 RAG 系统检索质量
- 当前只用纯向量检索，精确查询（如错误码 "ALM-1001"）召回不准
- 当前只用纯关键词检索，模糊查询（如 "线夹关不上"）语义不匹配
- 用户提到 "混合检索"、"hybrid search"、"BM25"、"RRF"

## 问题背景

纯向量检索的痛点：用户说 "线夹关不上"，语义上等于 "线夹闭合超时"（✅），但用户说 "ALM-1001"，向量可能召回 ALM-1002/ALM-1003（❌ 精确度不够）。

纯 BM25 的痛点：用户说 "线夹关不上"，BM25 搜不到 "线夹闭合超时"（❌ 没有语义理解）。

**混合检索 = BM25 关键词 + BGE 向量语义，RRF 融合取交集。**

## 技术栈
- `rank_bm25` — 纯 Python BM25 实现，零 Java 依赖
- `jieba` — 中文分词（BM25 需要 tokenized 输入）
- `chromadb` / 任意向量数据库 — 向量端
- `sentence-transformers` — BGE 嵌入模型

## 安装

```bash
uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple rank_bm25 jieba
```

## 架构

```
用户问题
    │
    ├──→ jieba 分词 → BM25Okapi.get_scores() ──→ Top K×3 候选
    │
    └──→ BGE Embedding → Chroma.query() ────────→ Top K×3 候选
                              │
                              ▼
                    ┌── RRF 融合 (k=60) ──┐
                    │  score = Σ 1/(60+r) │
                    └─────────────────────┘
                              │
                              ▼
                         Top K 最终结果 → LLM
```

## RRF 公式

```
RRF_score(d) = Σ (1 / (k + rank_r(d)))   for each ranker r
```

- k = 60（学术界标准常数，降低极高排名的影响力差异）
- rank_r(d)：文档 d 在第 r 个检索器中的排名（从 1 开始）
- 双引擎都命中的文档自动获得更高分

## 核心实现

### BM25 索引维护

BM25 不支持增量更新，每次 `ingest()` 需重建：

```python
tokenized = [list(jieba.cut(chunk)) for chunk in chunks]
if self.bm25 is None:
    self.bm25 = BM25Okapi(tokenized)
else:
    all_tokenized = [list(jieba.cut(d)) for d in self.bm25_docs] + tokenized
    self.bm25 = BM25Okapi(all_tokenized)
self.bm25_docs.extend(chunks)
self.bm25_metas.extend(metadatas)
```

### RRF 融合实现

```python
RRF_K = 60
rrf_scores: dict[str, float] = {}
doc_pool: dict[str, tuple[str, dict, float, float]] = {}

# 向量结果入池
for rank, (doc, meta, dist) in enumerate(zip(vec_docs, vec_metas, vec_dists)):
    key = f"v_{hash(doc)}"
    rrf_scores[key] = rrf_scores.get(key, 0) + 1.0 / (RRF_K + rank + 1)
    sim = max(0.0, 1.0 - dist / 2.0) if dist else 0.5
    doc_pool[key] = (doc, meta, sim, 0.0)

# BM25 结果入池
for rank, (idx, bm25_score) in enumerate(bm25_candidates):
    doc = self.bm25_docs[idx]
    key = f"b_{hash(doc)}"
    rrf_scores[key] = rrf_scores.get(key, 0) + 1.0 / (RRF_K + rank + 1)
    if key not in doc_pool:
        doc_pool[key] = (doc, meta, 0.3, bm25_score)  # 仅BM25命中→基础分
    else:
        d, m, sim, _ = doc_pool[key]
        doc_pool[key] = (d, m, sim, bm25_score)  # 双引擎→更新分数

# 按 RRF 排序取 top k
ranked = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:k]
```

### 关键细节

1. **候选池扩大**：各引擎取 `k*3` 候选，给 RRF 足够空间精选
2. **hash 去重**：用 `hash(doc)` 做 key，同一文档在两引擎中自动合并
3. **BM25 分数 > 0 过滤**：BM25 对无匹配词返回 0，过滤掉避免噪音
4. **仅 BM25 命中时 sim=0.3**：给基础相似度，低于向量命中但高于 0

## 验证方法

```python
# 精确查询 → 应命中确切条目
docs, metas, sims = rag._hybrid_search("ALM-1001", k=3)
assert any("ALM-1001" in d for d in docs), "BM25 应精确命中"

# 模糊查询 → 应命中语义相关条目
docs, metas, sims = rag._hybrid_search("线夹关不上", k=3)
assert any("线夹闭合超时" in d for d in docs), "向量应语义匹配"
```

## 已知坑

| 坑 | 现象 | 解决 |
|---|---|---|
| BM25 需完整重建 | `ingest()` 频繁调用时性能下降 | 小规模知识库（<10K chunks）重建耗时可忽略；大规模时用定时批量重建 |
| jieba 分词对英文/数字不友好 | "ALM-1001" 可能被切成 ["ALM", "-", "1001"] | 可接受，BM25 对子串匹配天然鲁棒；如需精确，给英文术语加引号保护 |
| rank_bm25 不支持增量 | 每次 ingest 重建整个索引 | 如上，小规模无影响 |
| RRF k=60 对小数据集偏保守 | 8 条数据时排名区分度低 | k 值可调小（如 10）增加区分度，但 60 是通用安全值 |
| **`clear()` 必须同时清空 BM25** | 清空 Chroma 后 BM25 仍保留旧数据，查询返回过期结果 | `clear()` 中加 `self.bm25 = None; self.bm25_docs = []; self.bm25_metas = []` |
| **hash(doc) 对小数据集有碰撞风险** | 8 chunks 时 "ALM-1001" 和相邻 chunk 可能产生相似但不同的 key | 大数据集自动稀释；小数据集可改 key 为 `f"{引擎}_{chunk_id}"` |

## 参考

- RRF 论文：Cormack et al., "Reciprocal Rank Fusion outperforms Condorcet and individual rank learning methods", SIGIR 2009
- rank_bm25: https://github.com/dorianbrown/rank_bm25
- 完整实现参考：`~/rag-agent/rag_agent.py` 中的 `ChromaRAG._hybrid_search()` 方法
