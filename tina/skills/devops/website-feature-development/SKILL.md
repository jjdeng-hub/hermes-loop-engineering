---
name: website-feature-development
description: 为 Next.js + FastAPI + SQLite 网站添加新功能（数据库模型 → API → 前端页面 → 数据初始化 → 部署）
category: devops
trigger: 当需要为 ToolSeeker 类网站添加新功能模块时
---

# website-feature-development

## 触发条件
当需要为 ToolSeeker 类网站添加新功能模块（如教程、Skill 库、服务页面等）时。

## 步骤

### 步骤 1: 更新后端数据库模型

在 `backend/main.py` 中添加新的 SQLAlchemy 模型类：

```python
class Tutorial(Base):
    __tablename__ = "tutorials"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    category = Column(String, nullable=False)
    # ... 其他字段
```

添加对应的 Pydantic schema：

```python
class TutorialCreate(BaseModel):
    title: str
    slug: str
    category: str
    # ...
```

添加 API 路由：

```python
@app.get("/api/tutorials")
def get_tutorials(...):
    # 列表查询

@app.get("/api/tutorials/{slug}")
def get_tutorial(slug: str, ...):
    # 详情查询

@app.post("/api/tutorials")
def create_tutorial(...):
    # 创建
```

添加分类/难度等常量映射字典：

```python
CATEGORY_LABELS_TUTORIAL = {
    "ai-dev": "AI 开发实战",
    "ai-workflow": "AI 自动化工作流",
}
```

### 步骤 2: 创建前端页面

**列表页**: `frontend/src/app/{feature}/page.tsx`
- 筛选栏（分类、难度等）
- 卡片网格布局
- 空状态提示

**详情页**: `frontend/src/app/{feature}/[slug]/page.tsx`
- 面包屑导航
- 内容渲染（Markdown 简化解析）
- 返回按钮

> ⚠️ **重要**：前端 API 路由不能直接访问 SQLite 数据库（better-sqlite3 是原生模块，构建时会失败）。必须通过 HTTP 调用后端 FastAPI 服务。

### 步骤 3: 更新导航栏

在 `frontend/src/components/Nav.tsx` 的 `NAV_LINKS` 数组中添加新入口：

```typescript
const NAV_LINKS = [
  { href: '/daily', label: 'AI 日报' },
  { href: '/tutorials', label: '实战教程' },  // 新增
  { href: '/skills', label: 'Skill 库' },      // 新增
  { href: '/tools', label: '工具导航' },
];
```

### 步骤 4: 创建数据初始化脚本

创建 `backend/init_{feature}.py`：

```python
import json  # 重要！

tutorials = [
    Tutorial(
        title="...",
        tags=json.dumps(["tag1", "tag2"]),  # 用 json.dumps() 序列化
        ...
    ),
]
```

**重要**: SQLite 的 Text 字段不能直接存储 list/dict，必须用 `json.dumps()` 序列化。

检查数据是否已存在：

```python
existing = db.query(Tutorial).count()
if existing > 0:
    print(f"已有数据: {existing} 个")
    return
```

### 步骤 5: 本地测试

```bash
# 运行初始化脚本
cd backend && python init_tutorials.py

# 验证 API
curl http://localhost:8002/api/tutorials
```

### 步骤 6: 提交并部署

```bash
# 本地提交
git add -A
git commit -m "feat: 新增教程和 Skill 栏目"
git push origin develop

# SSH 到服务器
ssh root@122.51.91.167

# 拉取代码（如有冲突先 stash）
cd /root/tool-seeker
git stash && git pull origin develop

# 部署前端
cd frontend && npm install && npm run build

# 部署后端（如有需要）
cd backend && source .venv/bin/activate && pip install -r requirements.txt

# 初始化数据
python init_tutorials.py

# 重启服务
pm2 restart toolseeker-web toolseeker-api --update-env

# 验证
curl -s -o /dev/null -w "%{http_code}" http://localhost/tutorials
curl -s -o /dev/null -w "%{http_code}" http://localhost/skills
pm2 status
```

## 常见陷阱

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| SQLite 报错 "type 'list' is not supported" | 直接存储 list 到 Text 字段 | 用 `json.dumps()` 序列化 |
| `venv/bin/activate: No such file` | venv 未被 git 跟踪 | 确保 requirements.txt 完整，服务器上重新创建 venv |
| `Your local changes would be overwritten` | 服务器有本地修改 | `git stash` 后再 pull |
| `detected dubious ownership` | git safe.directory 配置 | `git config --global --add safe.directory /path` |
| `Host key verification failed` | SSH known_hosts 缺失 | `ssh-keyscan -H IP >> ~/.ssh/known_hosts` |
| `Permission denied (publickey)` | SSH 密钥未配置 | 复制私钥到服务器并配置 SSH config |
| 前端构建失败 | node_modules 缺失 | 先 `npm install` 再 `npm run build` |
| API 返回空数据 | 数据库表未创建或数据未初始化 | 运行初始化脚本，检查表是否创建 |
| **部署后看不到数据** | 前端是客户端渲染，需要硬刷新 | 浏览器 Ctrl+Shift+R / Cmd+Shift+R 清除缓存 |
| **Next.js fetch 返回 HTML** | fetch 缓存或 localhost DNS 问题 | 改用 Node.js `http` 模块，使用 `127.0.0.1` 替代 `localhost` |
| **better-sqlite3 安装失败** | 原生模块在 Next.js 构建时失败 | 前端 API 路由通过 HTTP 调用后端 FastAPI |
| **新分类/Slug 不显示** | 只更新了后端，前端 category 列表未同步 | 同时更新 `frontend/src/app/{feature}/page.tsx` 的 categories 数组 和 `backend/main.py` 的 CATEGORY_LABELS 字典 |
| **新记录 is_active 为 NULL** | 数据库字段默认 NULL，API 查询过滤 `is_active == 1` | 插入时显式设置 `is_active=1` |
| **view_count 报错 TypeError** | 数据库字段为 NULL，`+= 1` 无法操作 None | 改为 `view_count = (view_count or 0) + 1` |
| **Nginx API 代理失败** | 只配置了 `/api/backend/`，但前端调用 `/api/tutorials/` | 为每个 API 端点添加独立的 location 块 |
| **URL 无斜杠导致 301 循环** | Nginx 精确匹配缺失 | 添加 `location = /api/tutorials` 精确匹配（无斜杠） |
| **数据库文件未同步** | toolseeker.db 在 .gitignore 中 | 手动 scp 同步数据库到服务器 |
| **SSH 密钥混淆** | 不同服务使用不同密钥 | 服务器用 `id_ed25519`，Gitee 用 `id_ed25519_gitee` |

## 验证清单

- [ ] API 返回正确数据: `curl http://localhost:8002/api/{feature}`
- [ ] 列表页返回 200: `curl -s -o /dev/null -w "%{http_code}" http://localhost/{feature}`
- [ ] 详情页可访问: `curl -s -o /dev/null -w "%{http_code}" http://localhost/{feature}/{slug}`
- [ ] PM2 状态正常: `pm2 status`
- [ ] 导航栏显示新入口
- [ ] 筛选功能正常工作
- [ ] 空状态提示正确显示
- [ ] **新分类显示正常**: 检查前端 categories 数组和后端 CATEGORY_LABELS 字典都包含新分类
- [ ] **新记录 is_active=1**: 检查数据库 `SELECT is_active FROM {table} WHERE slug='{new_slug}'`
- [ ] **Nginx 代理正常**: `curl http://127.0.0.1/api/{feature}` 返回后端数据而非前端 HTML
- [ ] **外部访问正常**: `curl http://{server_ip}/api/{feature}` 返回 200