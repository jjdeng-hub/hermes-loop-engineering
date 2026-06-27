---
name: rag-agent-development
description: >
  Build domain-specific RAG (Retrieval-Augmented Generation) knowledge agents.
  Covers the complete pipeline: data ingestion → chunking → retrieval → LLM answering,
  with both CLI and web UI interfaces. Use when building a Q&A system over technical
  documentation, alarm codes, repair manuals, or any structured knowledge base.
---

# RAG Agent Development

## Trigger conditions
- Building a Q&A system over domain documents (alarm codes, manuals, SOPs)
- User needs to "ask questions" about a knowledge base
- Setting up LangChain + Vector DB + LLM pipeline
- Converting CLI tools to web interfaces

## Architecture

```
index.html (browser) → FastAPI (localhost:8000) → LangChain RAG → DeepSeek LLM
```

Three layers:
1. **Frontend**: Single HTML file with chat bubbles, no build step
2. **Backend**: FastAPI exposing /api/ingest, /api/query, /api/stats, /api/demo
3. **Engine**: LangChain + keyword/vector retrieval + LLM prompt

## Project Structure

```
rag-agent/
├── api.py              # FastAPI backend
├── rag_fallback.py     # RAG engine (keyword retrieval, no embedding deps)
├── interactive.py      # CLI interactive mode
├── index.html          # Web chat UI
├── start.sh            # One-click launch
├── run.sh              # CLI launch
├── .env                # DEEPSEEK_API_KEY
└── chroma_db/          # Vector store (auto-created)
```

## Workflow

### 1. Scaffold the engine (rag_fallback.py)
- Direct .env parser (NOT python-dotenv — different venvs break it)
- LangChain ChatOpenAI pointed at DeepSeek (`api_base="https://api.deepseek.com/v1"`)
- Custom text splitter (LangChain's RecursiveCharacterTextSplitter imports are too slow)
- Keyword-based retrieval as fallback (no sentence-transformers dependency)
- Prompt template: system role + context + question + structured answer format

### 2. Add API layer (api.py)
- FastAPI + CORS middleware (allow all origins for local dev)
- Pydantic models for request/response
- Endpoints: POST /api/ingest, POST /api/query, GET /api/stats, POST /api/demo
- Start: `python3 api.py` → http://localhost:8000

### 3. Build web UI (index.html)
- Dark theme, chat bubbles (user right-aligned, assistant left-aligned)
- Sidebar: textarea for data import + buttons (import/demo)
- Input bar at bottom with Enter-to-send
- Typing indicator animation while waiting for API
- Toast notifications for success/error
- Single file, zero dependencies, open directly in browser

### 4. Create startup scripts
- `start.sh`: launches backend + opens browser
- `run.sh`: launches CLI interactive mode
- Both use absolute venv python path: `~/.hermes/hermes-agent/venv/bin/python3`

## Semantic Search Upgrade (Day 2)

After keyword-based MVP works, upgrade to semantic search with Chroma + BGE:

```
user question → BGE embedding (512d) → Chroma cosine similarity → top-K chunks → LLM
```

### Why upgrade
Keyword search fails on Chinese synonyms: "线夹关不上" won't match "闭合超时".
BGE embeddings understand semantics — different words, same meaning.

### ChromaRAG class pattern
```python
class ChromaRAG:
    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-small-zh-v1.5", device="cpu")
        self.client = chromadb.PersistentClient(path=str(db_dir))
        self.collection = self.client.get_or_create_collection(name="kb")
        self.llm = ChatOpenAI(model="deepseek-chat", ...)

    def ingest(self, text, source) -> int:   # chunk → embed → store
    def query(self, question, k=4) -> str:   # embed → search → prompt → answer
    def count(self) -> int:                   # collection size
    def clear(self):                          # delete all
```

### Model specs
- **BGE-small-zh-v1.5**: 512 dims, ~100MB, CPU-only, excellent Chinese semantics
- **HuggingFace mirror for China**: `export HF_ENDPOINT=https://hf-mirror.com`
- Must set HF_ENDPOINT BEFORE importing sentence_transformers
- Pro tip: set it at module top in rag_agent.py so every run works

### Chroma settings
- Space: `cosine` (best for normalized embeddings)
- Persist to `chroma_db/` directory
- Collection name: domain-specific (e.g., `ball_bonder_kb`)

## Dual LLM: Cloud → Local Migration

The architecture supports swapping LLM backends with one config change:

| Mode | LLM | Data location | Use case |
|---|---|---|---|
| Dev | DeepSeek API | Cloud | Fast iteration, cheap |
| Enterprise | Ollama + Qwen2.5 7B | Local | Data never leaves factory |

### Switching to Ollama
```python
# Only change: base_url and api_key
llm = ChatOpenAI(
    model="qwen2.5:7b",                       # ollama model name
    openai_api_base="http://localhost:11434/v1",  # ollama default port
    openai_api_key="ollama",                      # dummy key
)
```
Everything else — Chroma, BGE, FastAPI, HTML frontend — stays identical.

### Enterprise deployment considerations
- **Data security**: Local LLM = no data exfiltration. Critical for factories.
- **Model size**: Qwen2.5 7B Q4 needs ~4.5GB RAM. Office PC with 16GB is fine.
- **Packaging**: Docker Compose (ollama + rag-api) for one-command install.
- **Access control**: Add basic auth or LDAP to FastAPI before production.

## Installation

### Prerequisites
```bash
uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
  langchain langchain-community langchain-openai langchain-chroma \
  chromadb pypdf python-dotenv sentence-transformers fastapi uvicorn
```

### Ollama (for local LLM)
Install on Windows host (not WSL — network is unreliable):
1. Download from https://ollama.com/download/windows
2. `ollama pull qwen2.5:7b` (4.5GB, wait a few minutes)
3. WSL connects via `http://localhost:11434`

## Key Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| LangChain imports hang | `from langchain_text_splitters` times out | Write custom splitter function |
| python-dotenv in wrong venv | `ModuleNotFoundError: dotenv` | Parse .env directly with `os.environ.setdefault()` |
| WSL python != venv python | All deps "not found" | Use absolute path: `~/.hermes/hermes-agent/venv/bin/python3` |
| pip install blocked as "server" | Terminal refuses pip commands | Use `background=true` with `notify_on_complete=true` |
| HuggingFace download fails in China | `RuntimeError: Cannot send a request` | Set `HF_ENDPOINT=https://hf-mirror.com` |
| BGE model first load times out | 60s+ on first import | Download separately first: `SentenceTransformer('BAAI/bge-small-zh-v1.5')` |
| Ollama download blocked in WSL | curl to ollama.com times out | Install Ollama on Windows host, WSL connects via localhost |
| Chroma metadata type mismatch | `list[dict]` not assignable to `Metadata` | Ignore — Pyright false positive, runs fine at runtime |

## User Preferences
- Interactive > scripted demos. Build a REPL or web UI, not a one-shot script.
- Web UI > CLI. Browser interface preferred for demo and testing.
- Action: after building core engine, immediately ask if user wants a UI.
- DeepSeek as default LLM (cheap, OpenAI-compatible API).

## User Preferences
- Interactive > scripted demos. Build a REPL or web UI, not a one-shot script.
- Web UI > CLI. Browser interface preferred for demo and testing.
- Action: after building core engine, immediately ask if user wants a UI.
- DeepSeek as default LLM for dev (cheap, OpenAI-compatible API).
- Upgrade to semantic search (BGE + Chroma) after keyword MVP works.
- Always set HF_ENDPOINT mirror for China users before embedding model import.

## Templates

Ready-to-copy starter files in `templates/`:
- `templates/rag_engine.py` — Minimal RAG engine (keyword retrieval + DeepSeek)
- `templates/chroma_rag.py` — Full semantic search engine (Chroma + BGE + dual LLM)
- `templates/api.py` — FastAPI backend wiring the engine

## Reference Project
Full working example at `~/rag-agent/`. Contains:
- `rag_agent.py` — ChromaRAG class (semantic search, production-ready)
- `rag_fallback.py` — Keyword fallback (zero deps beyond langchain-openai)
- `api.py` — FastAPI backend (loads ChromaRAG, serves frontend)
- `index.html` — Single-file chat UI (dark theme, sidebar, typing indicator)
- `demo_data.txt` — 8 Ball Bonder alarm codes for testing
- `start.sh` — One-click launch with HF_ENDPOINT preset
