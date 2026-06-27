# Ollama 国内安装与模型导入

> 适用场景：WSL/本地部署本地大模型，数据不出本机。国内网络环境下 ollama.com 和 GitHub 可能无法直连。

---

## 安装策略：Windows + WSL 混合

### 为什么这样装

| 方式 | 国内可行性 |
|------|-----------|
| `curl ollama.com/install.sh` | ❌ 大概率超时 |
| `apt install ollama` | ❌ 没有官方 apt 源 |
| GitHub release 直下 | ❌ 被墙 |
| Windows 浏览器下载安装包 | ✅ 通常可用 |
| WSL 调 `ollama.exe` | ✅ 已验证可行 |

### 步骤

1. **Windows 浏览器**打开 https://ollama.com/download/windows → 下载安装包
2. 安装完成后，在 WSL 终端验证：
   ```bash
   ollama.exe --version
   ```
3. 若提示 `command not found`，添加 Windows 路径：
   ```bash
   export PATH="$PATH:/mnt/c/Users/<用户名>/AppData/Local/Programs/Ollama"
   ```

---

## 模型下载：绕过 ollama.com 注册表

`ollama pull qwen2.5:7b` 在国内极慢（走的 ollama.com CDN）。改用 **GGUF 文件 + 本地导入**。

### 国内可用的 GGUF 源

| 源 | URL | 速度 |
|----|-----|------|
| ModelScope | https://modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct-GGUF/files | ✅ 快 |
| HF-Mirror | https://hf-mirror.com/Qwen/Qwen2.5-7B-Instruct-GGUF | ✅ 快 |

### 导入流程

```bash
# 1. 下载 GGUF 文件（选 q4_K_M，4-bit 量化，~4.5GB）
#    浏览器打开 ModelScope，下载 qwen2.5-7b-instruct-q4_K_M.gguf
#    保存到 WSL: ~/models/

# 2. 创建 Modelfile
cat > ~/models/Modelfile.qwen << 'EOF'
FROM ./qwen2.5-7b-instruct-q4_K_M.gguf
PARAMETER temperature 0.7
PARAMETER top_p 0.8
PARAMETER num_ctx 4096
EOF

# 3. 导入 Ollama
ollama.exe create qwen2.5:7b-cn -f ~/models/Modelfile.qwen

# 4. 验证
ollama.exe run qwen2.5:7b-cn "你好，用中文回答"
```

---

## 模型选择建议

| 模型 | 大小 | 内存需求 | 适用场景 |
|------|------|---------|---------|
| Qwen2.5:7B (q4_K_M) | 4.5GB | ~6GB | 通用问答、翻译、RAG |
| Qwen2.5:14B (q4_K_M) | 8.5GB | ~12GB | 需更强推理能力 |
| Qwen2.5:3B (q4_K_M) | 2GB | ~3GB | 轻量、低延迟 |

> 15GB 内存的 WSL 推荐 Qwen2.5:7B (q4_K_M)，留足余量给 ChromaDB + 嵌入模型。

---

## 接入 RAG 项目

修改 `.env`：
```bash
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:7b-cn
OLLAMA_BASE_URL=http://localhost:11434
```

若 Ollama 服务在 Windows 侧运行，WSL 中通过 `localhost` 即可访问（WSL2 自动端口转发）。

启动 Ollama 服务（Windows 侧）：
```powershell
ollama serve
```
