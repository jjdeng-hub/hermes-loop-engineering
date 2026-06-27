"""
RAG Fallback Template — 关键词检索版
=====================================
可直接复制，修改 SAMPLE_DATA 和查询即可运行。
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── LLM ────────────────────────────────────────────────────────
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com/v1",
    temperature=0.1,
    max_tokens=2048,
)

# ── 文本切分 ────────────────────────────────────────────────────
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "；", "，", " ", ""],
)

# ── 内存存储 ────────────────────────────────────────────────────
_store: list[tuple[str, dict]] = []


def ingest_text(text: str, source: str = "manual") -> int:
    docs = splitter.create_documents([text], metadatas=[{"source": source}])
    for doc in docs:
        _store.append((doc.page_content, doc.metadata))
    return len(docs)


def _keyword_search(query: str, k: int = 4) -> list[str]:
    keywords = set(query.lower())
    scored = []
    for chunk, meta in _store:
        score = sum(1 for kw in keywords if kw in chunk.lower())
        if score > 0:
            scored.append((score, chunk, meta))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [
        f"[来源: {m.get('source', 'unknown')}]\n{c}"
        for _, c, m in scored[:k]
    ]


def query(question: str, k: int = 4) -> str:
    rel = _keyword_search(question, k=k)
    if not rel:
        return "⚠️ 知识库中未找到相关内容。"

    context = "\n\n---\n\n".join(rel)
    prompt = f"""你是一个{领域}专家。
请基于以下知识库内容回答用户的问题。

【知识库内容】
{context}

【用户问题】
{question}"""

    return llm.invoke(prompt).content


def stats() -> dict:
    return {"total_chunks": len(_store)}


# ═══════════════════════════════════════════════════════════════
#  Demo (修改下面的 SAMPLE_DATA 和 queries)
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    SAMPLE_DATA = """你的脱敏数据放这里"""

    print("📥 加载数据...")
    ingest_text(SAMPLE_DATA, "source_name")

    queries = ["问题1", "问题2", "问题3"]
    for q in queries:
        print(f"\n🔍 {q}")
        print(query(q))
