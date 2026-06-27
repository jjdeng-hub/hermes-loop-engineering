---
name: website-deploy-protection
description: 网站部署与数据保护 - 防止数据库丢失、部署失败、缓存问题的完整解决方案
---

# 网站部署与数据保护技能

## 触发条件
当需要部署 Next.js + FastAPI + SQLite 网站，或排查数据丢失、部署失败问题时。

## 核心问题根因

### 问题 1：数据库文件被 git 跟踪
```
现象: 本地有数据，服务器部署后数据丢失
原因: .gitignore 没有排除数据库文件，git pull/reset 回滚到旧版本
解决: 
  1. .gitignore 添加: backend/toolseeker.db
  2. git rm --cached backend/toolseeker.db
  3. git commit -m "chore: 移除数据库文件跟踪"
```

### 问题 2：服务器与远程不同步
```
现象: 新代码没有生效
原因: 服务器落后于远程仓库
解决: 使用 git pull 而不是 git reset --hard
  ❌ git reset --hard origin/develop  (会丢失未提交更改)
  ✅ git pull origin develop          (安全同步)
```

### 问题 3：客户端缓存
```
现象: 代码已更新但浏览器显示旧内容
原因: 浏览器缓存了旧的 JS/CSS 文件
解决:
  1. 版本号机制: 在组件中定义 APP_VERSION，每次部署更新
  2. API 防缓存: fetch(`/api/data?t=${Date.now()}`)
  3. 用户提示: 显示"硬刷新页面 (Ctrl+Shift+R)"
```

## 一键部署脚本 (deploy.sh)

```bash
#!/bin/bash
# 用法: ./deploy.sh

REMOTE_SERVER="root@你的服务器IP"
REMOTE_PATH="/path/to/project"
BRANCH="develop"

# 1. 本地推送
git add -A && git commit -m "feat: xxx" && git push origin $BRANCH

# 2. 服务器备份数据库
ssh $REMOTE_SERVER "cd $REMOTE_PATH && \
    if [ -f backend/toolseeker.db ]; then \
        cp backend/toolseeker.db backend/toolseeker.db.bak.$(date +%Y%m%d_%H%M%S); \
    fi"

# 3. 服务器同步代码
ssh $REMOTE_SERVER "cd $REMOTE_PATH && git pull origin $BRANCH"

# 4. 安装依赖
ssh $REMOTE_SERVER "cd $REMOTE_PATH/frontend && npm install"

# 5. 构建
ssh $REMOTE_SERVER "cd $REMOTE_PATH/frontend && npm run build"

# 6. 重启
ssh $REMOTE_SERVER "pm2 restart toolseeker-web toolseeker-api --update-env"

# 7. 验证
ssh $REMOTE_SERVER "curl -s -o /dev/null -w '%{http_code}\n' http://localhost/"
```

## 部署检查清单

- [ ] `.gitignore` 包含 `backend/toolseeker.db`
- [ ] 数据库文件不在 git 跟踪中 (`git ls-files backend/toolseeker.db` 应为空)
- [ ] 本地代码已提交并推送
- [ ] 服务器代码与远程同步
- [ ] 关键文件存在（API 路由、后端脚本）
- [ ] 部署后验证所有页面 HTTP 200
- [ ] 部署后验证所有 API 返回数据
- [ ] 版本号已更新（强制浏览器刷新）

## 常见问题排查

### Q: 部署后数据为空？
```bash
# 检查数据库
ssh root@IP "cd /path && python3 -c 'from main import SessionLocal, DailyNews; db=SessionLocal(); print(db.query(DailyNews).count())'"

# 检查 API
curl -s http://localhost:3000/api/daily/latest

# 检查后端日志
pm2 logs toolseeker-api --lines 20
```

### Q: 构建失败？
```bash
# 检查语法错误
cd frontend && npm run build 2>&1 | grep -A5 "error"

# 检查依赖
cd frontend && npm install

# 清理缓存
cd frontend && rm -rf .next node_modules/.cache && npm run build
```

### Q: 页面 502 错误？
```bash
# 检查 PM2 状态
pm2 status

# 检查端口
netstat -tlnp | grep 3000
netstat -tlnp | grep 8002

# 重启服务
pm2 restart all
```

### Q: Next.js API 路由被 Nginx 覆盖？
**现象**：前端 API 路由（如 `/api/tutorials`）返回 404 或 502，但后端 API 正常。

**原因**：Nginx 配置将 `/api/*` 全部代理到后端 FastAPI，覆盖了 Next.js 的 API 路由。

**解决方案**：
```nginx
# ❌ 错误配置：覆盖所有 /api/*
location /api/ {
    proxy_pass http://127.0.0.1:8002;
}

# ✅ 正确配置：只对后端 API 代理
location /api/backend/ {
    proxy_pass http://127.0.0.1:8002;
}
# Next.js API 路由由 Next.js 自身处理
```

**验证方法**：
```bash
# 检查 Nginx 配置
ssh root@<server> "cat /etc/nginx/conf.d/toolseeker.conf"

# 测试 API 路由
curl -s http://localhost:3000/api/tutorials  # 应返回 JSON（Next.js 处理）
curl -s http://localhost:8002/api/tutorials   # 应返回 JSON（FastAPI 处理）
```

### Q: 客户端看不到新数据？
```bash
# 1. 检查 API 是否正常
curl -s http://localhost:3000/api/tutorials

# 2. 检查前端 fetch 是否有错误
# 打开浏览器开发者工具 → Network → 查看 API 请求状态

# 3. 强制刷新
# Ctrl+Shift+R (Windows/Linux) 或 Cmd+Shift+R (Mac)
```

## 最佳实践

1. **数据库永远不要提交到 git**
   - 本地开发：数据库在本地
   - 服务器：数据库在服务器，定期备份

2. **部署前备份**
   ```bash
   cp backend/toolseeker.db backend/toolseeker.db.bak
   ```

3. **使用版本号强制刷新**
   ```typescript
   const APP_VERSION = '2.2.0'; // 每次部署更新
   ```

4. **API 添加时间戳防缓存**
   ```typescript
   fetch(`/api/data?t=${Date.now()}`)
   ```

5. **部署脚本自动化**
   - 减少人为错误
   - 确保每次部署一致
   - 自动备份和验证

6. **⚠️ Next.js API 路由调用后端 API 的陷阱（2026-05-07 实践总结）**
   ...（原有内容保持不变）...

7. **⚠️ Nginx 配置不要覆盖 Next.js API 路由（2026-05-07 实践总结）**
   ...（原有内容保持不变）...

8. **⚠️ 服务器文件同步问题（2026-05-08 实践总结）**

   **问题**：本地构建成功，服务器构建失败，提示找不到文件。

   **原因**：服务器存在旧的目录结构（如 `frontend/components/`），与新的 `frontend/src/components/` 冲突。

   **解决方案**：
   ```bash
   # 部署前检查服务器文件结构
   ssh root@<IP> "find /root/tool-seeker/frontend -name '*.tsx' | head -20"
   
   # 清理可能冲突的旧目录
   ssh root@<IP> "rm -rf /root/tool-seeker/frontend/components /root/tool-seeker/frontend/public"
   
   # 重新构建
   ssh root@<IP> "cd /root/tool-seeker/frontend && npm run build"
   ```

   **预防措施**：
   - 部署前检查服务器文件结构
   - 保持本地和服务器目录结构一致
   - 使用 `git stash` 清理服务器本地修改

## 相关文件

- `.gitignore` - 排除数据库文件
- `deploy.sh` - 一键部署脚本
- `DEPLOY_GUIDE.md` - 详细部署指南
- `frontend/src/app/page.tsx` - 包含版本号和刷新机制