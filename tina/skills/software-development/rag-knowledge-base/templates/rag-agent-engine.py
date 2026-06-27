"""
RAG Engine Template — Keyword-based retrieval (no embedding deps)
=================================================================
Copy this file as your starting point. Only needs LangChain + langchain-openai.
"""

import os
from pathlib import Path

# ── Direct .env parser ───────────────────────────────────────
def _load_env():
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))
_load_env()

# ── LLM ──────────────────────────────────────────────────────
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com/v1",
    temperature=0.1,
    max_tokens=2048,
)

# ── Custom Text Splitter ─────────────────────────────────────
def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    paragraphs = text.replace('\r\n', '\n').split('\n\n')
    chunks = []
    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        sentences = para.replace('。', '。|||').replace('；', '；|||').split('|||')
        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue
            if len(current) + len(sent) > chunk_size and current:
                chunks.append(current.strip())
                current = (current[-overlap:] if len(current) > overlap else "") + sent
            else:
                current += sent
    if current.strip():
        chunks.append(current.strip())
    return chunks if chunks else [text]

# ── In-Memory Store ──────────────────────────────────────────
_store: list[tuple[str, dict]] = []

def ingest_text(text: str, source: str = "manual") -> int:
    chunks = split_text(text)
    for chunk in chunks:
        _store.append((chunk, {"source": source}))
    return len(chunks)

def keyword_search(query: str, k: int = 4) -> list[str]:
    keywords = set(query.lower())
    scored = [(sum(1 for kw in keywords if kw in chunk.lower()), chunk, meta)
              for chunk, meta in _store if any(kw in chunk.lower() for kw in keywords)]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [f"[来源: {m.get('source', 'unknown')}]\n{c}" for _, c, m in scored[:k]]

def query(question: str, k: int = 4) -> str:
    rel = keyword_search(question, k=k)
    if not rel:
        return "No matching content found."
    context = "\n\n---\n\n".join(rel)
    prompt = f"Based on this knowledge base:\n\n{context}\n\nQuestion: {question}"
    return llm.invoke(prompt).content
