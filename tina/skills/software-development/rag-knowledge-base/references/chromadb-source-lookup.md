# ChromaDB 按来源反查知识块

后端新增 `GET /api/source?file=xxx`，从 ChromaDB 按 source metadata 检索原文。

## ChromaRAG 新增方法

```python
def get_chunks_by_source(self, filename: str) -> list[str]:
    """返回指定文件的所有已索引 chunk"""
    try:
        results = self.collection.get(where={"source": filename})
        if results and results["documents"]:
            return results["documents"]
    except Exception:
        pass
    return []
```

## FastAPI 端点

```python
@app.get("/api/source")
def api_source(file: str = "", _=Depends(require_auth)):
    """按文件名查询原始知识块"""
    if not file:
        return {"success": False, "error": "缺少 file 参数"}
    try:
        chunks = get_rag().get_chunks_by_source(file)
        return {"success": True, "data": {"filename": file, "chunks": chunks, "count": len(chunks)}}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## 前提

- 导入时 metadata 必须存 `{"source": filename}`
- ChromaDB 支持 `where={"source": "xxx"}` 过滤查询
