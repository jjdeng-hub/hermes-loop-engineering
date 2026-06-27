#!/bin/bash
# 企业 RAG 知识库 — 前后端分离启动脚本模板
# 后端: FastAPI :8000
# 前端: Python HTTP Server :3000

VENV=~/.hermes/hermes-agent/venv/bin/python3
DIR="$(cd "$(dirname "$0")" && pwd)"

# 国内镜像
export HF_ENDPOINT=https://hf-mirror.com

# 企业配置
export RAG_TOKEN=${RAG_TOKEN:-enterprise-token-change-me}
export WATCH_DIR=${WATCH_DIR:-$DIR/data}
export LLM_PROVIDER=${LLM_PROVIDER:-deepseek}

mkdir -p "$WATCH_DIR"

echo "================================================"
echo "  企业知识库启动"
echo "================================================"
echo "  后端 API: http://localhost:8000"
echo "  前端界面: http://localhost:3000"
echo "  监控目录: $WATCH_DIR"
echo "  登录令牌: $RAG_TOKEN"
echo "  LLM 模式: $LLM_PROVIDER"
echo "================================================"

# 启动后端
$VENV $DIR/api.py &
API_PID=$!

# 启动前端
cd "$DIR" && python3 -m http.server 3000 --bind 0.0.0.0 &
WEB_PID=$!

sleep 5

# 打开浏览器 (WSL)
explorer.exe "http://localhost:3000" 2>/dev/null || true

cleanup() {
    echo "停止服务..."
    kill $API_PID 2>/dev/null
    kill $WEB_PID 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM
wait
