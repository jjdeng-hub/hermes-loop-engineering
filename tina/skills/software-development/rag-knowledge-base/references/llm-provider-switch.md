# LLM Provider 切换模式

# .env 配置
# LLM_PROVIDER=deepseek  # 云端 DeepSeek（默认）
# LLM_PROVIDER=ollama    # 本地 Ollama

# 代码模式（rag_agent.py 中 ChromaRAG.__init__）:

provider = os.getenv("LLM_PROVIDER", "deepseek").lower()

if provider == "ollama":
    self.llm = ChatOpenAI(
        model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
        openai_api_key="ollama",  # Ollama 不需要真实 key
        openai_api_base=os.getenv("OLLAMA_BASE", "http://localhost:11434/v1"),
        temperature=0.1,
        max_tokens=2048,
    )
else:
    self.llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        openai_api_base="https://api.deepseek.com/v1",
        temperature=0.1,
        max_tokens=2048,
    )
