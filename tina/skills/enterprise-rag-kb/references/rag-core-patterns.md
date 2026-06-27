# RAG 核心实现细节

## BGE Embedding 模型

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-zh-v1.5", device="cpu")
embedding = model.encode("线夹闭合超时", normalize_embeddings=True)
# 输出: 512 维向量

# 批量编码
embeddings = model.encode(chunks, normalize_embeddings=True).tolist()
```

**国内镜像**: 设置 `HF_ENDPOINT=https://hf-mirror.com`

## ChromaDB 配置

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="kb",
    metadata={"hnsw:space": "cosine"}  # 余弦相似度
)

# 写入
collection.add(ids=[...], embeddings=[...], documents=[...], metadatas=[...])

# 查询（返回 distances）
results = collection.query(query_embeddings=[...], n_results=4)
# results = {"ids": [...], "documents": [...], "metadatas": [...], "distances": [...]}
```

## 中文文本切分

不使用 langchain.text_splitter（导入太慢），手写：

```python
def split_text(text: str, chunk_size=400, overlap=50) -> list[str]:
    paragraphs = text.replace("\r\n", "\n").split("\n\n")
    chunks = []
    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para: continue
        sentences = para.replace("。", "。|||").replace("；", "；|||").split("|||")
        for sent in sentences:
            sent = sent.strip()
            if not sent: continue
            if len(current) + len(sent) > chunk_size and current:
                chunks.append(current.strip())
                current = current[-overlap:] + sent if len(current) > overlap else sent
            else:
                current += sent
    if current.strip(): chunks.append(current.strip())
    return chunks if chunks else [text]
```

## 置信度计算

```python
distances = results.get("distances", [[]])[0]
if distances:
    sims = [max(0, 1 - d/2) for d in distances]  # 余弦距离→相似度
    top1 = sims[0]
    avg_topk = sum(sims) / len(sims)
    confidence = round((top1 * 0.6 + avg_topk * 0.4) * 100)
else:
    confidence = 50
```

## 流式输出模式

后端 (rag_agent.py):
```python
def stream(self, question: str, k=4, session_id=None):
    prompt, source_note, conf = self._build_prompt(question, k, session_id)
    full_answer = ""
    for chunk in self.llm.stream(prompt):
        if chunk.content:
            full_answer += chunk.content
            yield chunk.content
    self._save_history(session_id, question, full_answer)
    yield f"\n\n📎 参考文档: {source_note}\n🎯 匹配度: {conf}%"
```

API (api.py):
```python
@app.post("/api/query/stream")
def api_query_stream(req: QueryRequest):
    def generate():
        for token in rag.stream(req.question, session_id=req.session_id):
            yield token
    return StreamingResponse(generate(), media_type="text/plain")
```

前端 (index.html):
```javascript
const reader = response.body.getReader();
const decoder = new TextDecoder();
let raw = '';
while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    raw += decoder.decode(value, {stream: true});
    bubble.innerHTML = highlightText(raw, query);
    chat.scrollTop = chat.scrollHeight;
}
```
