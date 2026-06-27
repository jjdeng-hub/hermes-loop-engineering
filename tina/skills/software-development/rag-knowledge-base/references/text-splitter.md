# 中文文本切分器 (避免 langchain 导入过慢)

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

# 为什么不直接用 langchain.text_splitter？
# langchain_text_splitters 导入时触发重型模块加载，在 WSL 环境下卡 5-10 秒。
# 这个手写版本零依赖，效果等价，秒切。
