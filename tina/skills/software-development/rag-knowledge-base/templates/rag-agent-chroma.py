"""
ChromRAG — 基于 Chroma + BGE 的语义搜索引擎
============================================
模板文件。复制此文件，修改 collection_name 和 prompt 模板即可用于任意领域。

依赖: chromadb, sentence-transformers, langchain-openai
首次运行前: export HF_ENDPOINT=https://hf-mirror.com (国内)
"""

import os
from pathlib import Path

# 国内 HuggingFace 镜像（必须在 import sentence_transformers 之前设置）
if "HF_ENDPOINT" not in os.environ:
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings as ChromaSettings

# ── 环境变量 (.env 文件) ─────────────────────────────────────
def _load_env():
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("\"'"))
_load_env()

# ── 中文文本切分 ────────────────────────────────────────────
def split_text(text: str, chunk_size=400, overlap=50) -> list[str]:
    """按中文标点 + 段落切分，保证 chunk 大小均匀"""
    paragraphs = text.replace("\r\n", "\n").split("\n\n")
    chunks = []
    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        sentences = para.replace("。", "。|||").replace("；", "；|||").split("|||")
        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue
            if len(current) + len(sent) > chunk_size and current:
                chunks.append(current.strip())
                current = current[-overlap:] + sent if len(current) > overlap else sent
            else:
                current += sent
    if current.strip():
        chunks.append(current.strip())
    return chunks if chunks else [text]


# ═══════════════════════════════════════════════════════════════
#  ChromaRAG — 复用此 class，改 3 个地方即可
# ═══════════════════════════════════════════════════════════════

class ChromaRAG:
    """语义搜索 RAG 引擎。改 collection_name + prompt 模板 → 任意领域。"""

    def __init__(self, collection_name="my_kb", model_name="BAAI/bge-small-zh-v1.5"):
        # 1. Embedding 模型 (BGE 中文, 512 维, ~100MB)
        self.model = SentenceTransformer(model_name, device="cpu")

        # 2. Chroma 向量数据库 (本地持久化)
        db_dir = Path(__file__).parent / "chroma_db"
        db_dir.mkdir(exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=str(db_dir),
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

        # 3. LLM — 改这里切换云/本地模型
        from langchain_openai import ChatOpenAI
        self.llm = ChatOpenAI(
            model="deepseek-chat",                  # 或 "qwen2.5:7b" (Ollama)
            openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
            openai_api_base="https://api.deepseek.com/v1",  # 或 "http://localhost:11434/v1"
            temperature=0.1,
            max_tokens=2048,
        )

    def ingest(self, text: str, source: str = "manual") -> int:
        """切分 → 向量化 → 存入 Chroma"""
        chunks = split_text(text)
        if not chunks:
            return 0
        embeddings = self.model.encode(chunks, normalize_embeddings=True).tolist()
        existing = self.collection.count()
        ids = [f"chunk_{existing + i}" for i in range(len(chunks))]
        self.collection.add(ids=ids, embeddings=embeddings, documents=chunks,
                            metadatas=[{"source": source} for _ in chunks])
        return len(chunks)

    def query(self, question: str, k: int = 4) -> str:
        """语义搜索 → LLM 回答"""
        if self.collection.count() == 0:
            return "⚠️ 知识库为空。"
        q_emb = self.model.encode([question], normalize_embeddings=True).tolist()
        results = self.collection.query(query_embeddings=q_emb, n_results=k)
        docs = results["documents"][0] if results["documents"] else []
        if not docs:
            return "⚠️ 未找到相关内容。"

        context = "\n\n---\n\n".join(f"[{i+1}] {d}" for i, d in enumerate(docs))

        # ── 改这里的 prompt 模板适配你的领域 ──
        prompt = f"""你是领域专家。基于以下知识库内容回答用户问题。
信息不足时说明"根据现有资料无法确定"。

【知识库】
{context}

【用户问题】
{question}

【要求】先给结论，再列排查步骤（按优先级），附关键信息。"""

        return self.llm.invoke(prompt).content

    def count(self) -> int:
        return self.collection.count()

    def clear(self):
        ids = self.collection.get()["ids"]
        if ids:
            self.collection.delete(ids=ids)
