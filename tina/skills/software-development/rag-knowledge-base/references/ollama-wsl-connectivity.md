# Ollama Windows + WSL 连接配置

> 场景：Windows 装 Ollama，WSL 里 rag-agent 调 `ollama.exe` 或 HTTP API

---

## 问题：WSL 连不上 Windows Ollama

**症状：**
```
curl http://localhost:11434/api/tags → Connection refused (exit 7)
curl http://<WINDOWS_IP>:11434/api/tags → 超时
```

**根因：** Ollama Windows 默认只监听 `127.0.0.1:11434`，不响应来自 WSL 虚拟网卡的请求。

---

## 修复

### 临时（本次会话）

Windows PowerShell 执行：
```powershell
$env:OLLAMA_HOST="0.0.0.0"
ollama serve
```

### 永久（推荐）

1. 打开 Windows 系统环境变量设置
2. 新增用户变量：`OLLAMA_HOST` = `0.0.0.0`
3. 重启 Ollama（任务栏右下角退出 → 重新打开）

---

## 验证

WSL 内执行：
```bash
curl http://localhost:11434/api/tags
```

应返回模型列表 JSON。

---

## 架构总览

```
Windows:  ollama.exe serve (OLLAMA_HOST=0.0.0.0:11434)
               ↑
               │ HTTP
               ↓
WSL:      rag-agent (api.py) ──→ http://localhost:11434
                ──→ ChatOpenAI(base_url="http://localhost:11434/v1")
```

模型存储在 Windows 侧 (`C:\Users\<user>\.ollama\models\`)，WSL 不重复占用空间。

---

## 备选方案：Ollama 模型手动导入

如果 `ollama pull` 太慢，从 ModelScope 下载 GGUF：

```bash
# 从 ModelScope 下载（国内满速）
# 然后在 Ollama 中创建
ollama create qwen2.5:7b -f Modelfile
```

Modelfile 示例：
```
FROM ./qwen2.5-7b-instruct-q4_k_m.gguf
```
