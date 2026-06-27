"""
FastAPI Backend Template — REST API for RAG Agent
==================================================
Copy and customize for any RAG project.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import your RAG engine (adjust import path)
from rag_engine import ingest_text, query, keyword_search

app = FastAPI(title="RAG Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngestRequest(BaseModel):
    text: str
    source: str = "manual"

class QueryRequest(BaseModel):
    question: str

@app.post("/api/ingest")
def api_ingest(req: IngestRequest):
    n = ingest_text(req.text, req.source)
    return {"success": True, "data": {"chunks_added": n}}

@app.post("/api/query")
def api_query(req: QueryRequest):
    if not _store_total():
        return {"success": False, "error": "Knowledge base is empty"}
    answer = query(req.question)
    return {"success": True, "data": answer}

@app.get("/api/stats")
def api_stats():
    return {"success": True, "data": {"total_chunks": _store_total()}}

def _store_total():
    from rag_engine import _store
    return len(_store)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
