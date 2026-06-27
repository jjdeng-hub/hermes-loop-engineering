---
name: sqlite-database-git-exclusion
description: SQLite 数据库文件 git 排除指南 — 解决数据库被 git 跟踪导致数据丢失的问题
trigger: 当 SQLite 数据库文件被 git 跟踪导致数据丢失时（常见于开发环境数据库被 git pull 回滚）
---

# sqlite-database-git-exclusion

## 触发条件
当 SQLite 数据库文件被 git 跟踪导致数据丢失时（常见于开发环境数据库被 git pull 回滚）

## 问题诊断

| 症状 | 原因 |
|------|------|
| 数据突然消失 | 数据库文件被 git 跟踪，`git pull` 回滚到空版本 |
| 部分数据能看到 | 只有 git 中有提交的数据能恢复，新增数据丢失 |
| 每次部署数据重置 | 服务器 `git pull` 覆盖本地数据库 |

## 解决方案

### 1. 从 git 中移除数据库文件跟踪

```bash
# 添加数据库文件到 .gitignore
echo "backend/toolseeker.db" >> .gitignore

# 从 git 缓存中移除（保留本地文件）
git rm --cached backend/toolseeker.db

# 提交更改
git commit -m "chore: 移除数据库文件跟踪（本地数据不提交）"
git push origin <branch>
```

### 2. 服务器端同步

```bash
# 在服务器上拉取 .gitignore 更新
ssh root@<server> "cd /root/tool-seeker && git pull origin <branch>"

# 如果服务器数据库被覆盖，需要手动恢复
# 方案 A: 从本地 scp 数据库到服务器
scp backend/toolseeker.db root@<server>:/root/tool-seeker/backend/

# 方案 B: 重新运行初始化脚本
ssh root@<server> "cd /root/tool-seeker/backend && python3 init_tutorials.py"
```

### 3. 验证

```bash
# 检查数据库文件是否还在 git 跟踪中
git ls-files backend/toolseeker.db  # 应返回空

# 检查数据库数据
sqlite3 backend/toolseeker.db "SELECT COUNT(*) FROM <table>;"
```

## 预防措施

1. **开发初期就配置 .gitignore**
   - 在项目初始化时就把数据库文件加入 .gitignore
   - 避免后续补救

2. **使用环境变量管理数据库路径**
   ```python
   # config.py
   import os
   DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./toolseeker.db")
   ```

3. **分离配置和数据**
   - 数据库文件：本地数据，不提交
   - 配置文件：提交到 git
   - 初始化脚本：提交到 git，用于重建空数据库

4. **备份策略**
   ```bash
   # 部署前备份
   cp backend/toolseeker.db backend/toolseeker.db.bak

   # 部署后验证
   ssh root@<server> "cd /root/tool-seeker/backend && python3 verify_db.py"
   ```

## 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `git rm --cached` 报错 | 文件不在 git 跟踪中 | 先 `git add` 再 `git rm --cached` |
| 服务器数据库为空 | `git pull` 覆盖了本地文件 | 手动 scp 恢复或重新初始化 |
| 数据库连接失败 | 文件权限问题 | `chmod 644 backend/toolseeker.db` |
| **数据反复丢失** | 服务器执行 `git reset --hard` 恢复旧版本 | 每次重置后需重新运行初始化脚本 |
| **部署后看不到数据** | 前端是客户端渲染，需要硬刷新 | 浏览器 Ctrl+Shift+R / Cmd+Shift+R |

## ⚠️ 关键教训（2026-05-07 实践总结）

### 教训 1：git reset --hard 会恢复旧版本数据库

**场景**：服务器代码不同步时，执行 `git reset --hard origin/develop` 会：
1. 恢复 git 历史中的旧版本数据库文件
2. 所有本地添加的数据（日报、教程、Skill）全部丢失

**解决方案**：
```bash
# 每次 git reset --hard 后，必须重新初始化数据
ssh root@<server> "cd /root/tool-seeker/backend && python3 init_tutorials.py"
ssh root@<server> "cd /root/tool-seeker/backend && python3 add_daily_news.py"
```

### 教训 2：前端 API 路由调用后端 API 的陷阱

**场景**：Next.js 前端 API 路由直接 fetch 后端 API 时，可能返回 HTML 而非 JSON。

**原因**：
- Next.js 的 `fetch` 有缓存机制，可能返回缓存的 HTML 页面
- localhost DNS 解析问题

**解决方案**：
```typescript
// ❌ 错误：Next.js fetch 可能返回 HTML
const res = await fetch('http://localhost:8002/api/tutorials');

// ✅ 正确：使用 Node.js http 模块
import http from 'http';
const res = await new Promise((resolve, reject) => {
  http.get('http://127.0.0.1:8002/api/tutorials', (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => resolve(JSON.parse(data)));
  }).on('error', reject);
});
```

### 教训 3：better-sqlite3 在 Next.js 中不可用

**场景**：前端尝试使用 `better-sqlite3` 直接访问 SQLite 数据库。

**原因**：`better-sqlite3` 是原生模块，在 Next.js 构建时会失败。

**解决方案**：前端 API 路由通过 HTTP 调用后端 FastAPI 服务，后端使用 `sqlite3` 或 `SQLAlchemy`。

## 相关技能

- `deploy-environment-verify`: 验证服务器环境
- `ai-daily-automation`: AI 日报自动化抓取与部署