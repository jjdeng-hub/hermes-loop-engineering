#!/bin/bash
# Hermes Auto-Update Script v3
# 使用内置的 `hermes update` 命令，外围加锁/备份/重启/报告

set -euo pipefail

HERMES_DIR="/usr/local/lib/hermes-agent"
LOCK_FILE="/tmp/hermes-update.lock"
STATE_FILE="/root/.hermes/loop-state.md"
REPORT_FILE="/tmp/hermes-update-report.md"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_DIR="/root/.hermes/backups/$TIMESTAMP"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ===== Hermes 自动更新 (内置命令) ====="

# 1. 并发锁
exec 200>"$LOCK_FILE"
flock -n 200 || { echo "⚠️ 另一个更新进程正在运行，跳过"; exit 0; }

# 2. 环境检查
[ -d "$HERMES_DIR/.git" ] || { echo "❌ 不是 git 仓库"; exit 1; }
command -v hermes >/dev/null || { echo "❌ hermes 命令不可用"; exit 1; }

# 3. 磁盘检查
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
[ "$DISK_USAGE" -gt 90 ] && { echo "❌ 磁盘 ${DISK_USAGE}%，拒绝更新"; exit 1; }

# 4. 检查是否有更新
echo "检查更新..."
if ! hermes update --check 2>&1 | grep -q "update available"; then
    echo "✅ 已经是最新版本"
    exit 0
fi

echo "📦 发现新版本！"

# 5. 备份
mkdir -p "$BACKUP_DIR"
cp /root/.hermes/config.yaml "$BACKUP_DIR/" 2>/dev/null || true
cp /root/.hermes/.env "$BACKUP_DIR/" 2>/dev/null || true

# 6. 执行更新
echo "执行更新..."
hermes update --yes --backup 2>&1 || {
    echo "❌ 更新失败！"
    exit 1
}

# 7. 重启网关
echo "重启网关（通过 systemd）..."
systemctl restart hermes-gateway 2>&1 || {
    echo "⚠️ systemctl 重启失败，尝试 hermes gateway restart..."
    hermes gateway restart 2>&1 || true
}

# 8. 健康检查
sleep 5
NEW_PID=$(systemctl show -p MainPID hermes-gateway 2>/dev/null | grep -oP '\d+')
if [ -n "$NEW_PID" ] && [ "$NEW_PID" -ne 0 ]; then
    echo "✅ 网关已重启 (PID: $NEW_PID)"
else
    echo "⚠️ 网关重启待确认，请检查：journalctl -u hermes-gateway"
fi

# 9. 获取版本
UPDATED_VERSION=$(hermes --version 2>&1 | head -1)

# 10. 写入状态文件
{
    echo ""
    echo "## 📦 Hermes 自动更新 — $(date '+%Y-%m-%d %H:%M')"
    echo "- 目标版本: $UPDATED_VERSION"
    echo "- 备份: $BACKUP_DIR"
} >> "$STATE_FILE"

# 11. 输出摘要
echo ""
echo "========== ✅ 更新完成 =========="
echo "版本: $UPDATED_VERSION"
echo "备份: $BACKUP_DIR"
echo "================================"
hermes --version 2>&1

flock -u 200
