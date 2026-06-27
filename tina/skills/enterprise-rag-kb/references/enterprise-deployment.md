# 企业化部署特征与配置

## 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| DEEPSEEK_API_KEY | - | DeepSeek API 密钥 |
| LLM_PROVIDER | deepseek | deepseek 或 ollama |
| OLLAMA_MODEL | qwen2.5:7b | Ollama 本地模型名 |
| OLLAMA_BASE | http://localhost:11434/v1 | Ollama 地址 |
| HF_ENDPOINT | https://hf-mirror.com | HuggingFace 国内镜像 |
| WATCH_DIR | ./data | 文件监控目录 |
| WATCH_INTERVAL | 30 | 扫描间隔(秒) |
| RAG_TOKEN | 随机生成 | 管理令牌 |

## 部署前检查清单

- [ ] `LLM_PROVIDER=ollama` 确保数据不出厂
- [ ] `RAG_TOKEN` 设固定值，不要随机
- [ ] 先 `ollama pull qwen2.5:7b` 下载模型
- [ ] 断网测试：启动 → 上传文档 → 查询 → 确认无外部请求
- [ ] WATCH_DIR 指向企业共享文件夹或固定数据目录
- [ ] ChromaDB 目录有足够磁盘空间
- [ ] 防火墙放行 8000 端口（如需外部访问）
- [ ] Docker 镜像在目标机器上构建或预构建传输

## 文件格式支持

| 格式 | 解析器 | 备注 |
|---|---|---|
| .pdf | pypdf | 不支持扫描件（需 OCR） |
| .docx | python-docx | 只取段落文字，不取表格 |
| .xlsx | openpyxl | 最多解析 5 个 sheet |
| .txt/.md/.csv/.log | 内置 | UTF-8 直接读取 |

## 鉴权模式

当前: 单一 Bearer Token（启动时打印，固定后通过 RAG_TOKEN 环境变量配置）

企业升级路径:
1. 固定 Token → RAG_TOKEN 环境变量
2. 多用户 → 数据库存储用户+哈希密码+角色
3. LDAP/AD → FastAPI LDAP 中间件
4. SSO → OAuth2/OIDC 对接企业 IdP

## Docker 部署

```bash
# 仅 RAG（使用 DeepSeek 云端）
docker-compose up -d rag

# 全本地（含 Ollama）
docker-compose --profile local up -d

# 模型下载（需在 Ollama 容器内执行）
docker exec -it rag-agent-ollama-1 ollama pull qwen2.5:7b
```
