---
name: ai-daily-automation
category: devops
description: AI 日报自动化抓取与部署 - 每天自动抓取 RSS，免费翻译，存入数据库
---

# AI 日报自动化抓取与部署（免费版本）

## 概述
每天自动抓取 AI 资讯 + 免费翻译，无需 API Key，可持续运行。
自动化抓取 AI 相关资讯，生成日报内容，并部署到服务器。

## 文件结构
```
site/
├── backend/
│   ├── auto_fetch_daily.py    # 自动化抓取脚本
│   ├── translate.py           # 翻译脚本（免费 API）
│   ├── migrate.py             # 数据库迁移脚本
│   ├── start_fetch.sh         # 启动脚本
│   ├── crontab.txt            # Cron 配置
│   └── logs/                  # 日志目录
├── frontend/
│   └── src/app/daily/page.tsx # 日报页面（支持中英文切换）
```

## 快速使用

### 手动运行抓取
```bash
cd /root/tool-seeker/backend
source venv/bin/activate
python3 auto_fetch_daily.py --date 2026-05-07
```

### 设置定时任务
```bash
crontab -e
# 添加:
0 8 * * * cd /root/tool-seeker/backend && source venv/bin/activate && python3 auto_fetch_daily.py >> logs/fetch.log 2>&1
```

### 部署到服务器
```bash
# 1. 同步代码
rsync -avz site/backend/ root@122.51.91.167:/root/tool-seeker/backend/
rsync -avz --delete site/frontend/src/ root@122.51.91.167:/root/tool-seeker/frontend/src/

# 2. 构建并重启
ssh root@122.51.91.167 "cd /root/tool-seeker/frontend && rm -rf .next && npm run build && pm2 restart toolseeker-web"
```

## 配置说明

### RSS 源
编辑 `auto_fetch_daily.py` 中的 `RSS_FEEDS` 配置：
```python
RSS_FEEDS = [
    {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com/rss",
        "category": "ai",
        "keywords": ["AI", "machine learning", "LLM"],
    },
    # ...
]
```

### AI 模型配置
```python
AI_CONFIG = {
    "provider": "openai",  # openai | anthropic | gemini
    "model": "gpt-4o",
    "api_key": os.environ.get("OPENAI_API_KEY", ""),
}
```

### 环境变量
```bash
export OPENAI_API_KEY="sk-xxx"  # 或 ANTHROPIC_API_KEY
```

## 数据库结构
```sql
daily_news (
    id, date, category, title, title_cn, 
    summary, summary_cn, opinion, opinion_cn,
    source_url, source_name, sort_order, created_at
)
```

## 自动翻译功能

### 概述
支持中英文双语内容，自动翻译英文内容并存储中文版本，前端可切换显示。

### 数据库迁移
```bash
# 添加翻译字段
python3 migrate.py

# 或手动执行 SQL
sqlite3 toolseeker.db <<EOF
ALTER TABLE daily_news ADD COLUMN title_cn TEXT DEFAULT '';
ALTER TABLE daily_news ADD COLUMN summary_cn TEXT DEFAULT '';
ALTER TABLE daily_news ADD COLUMN opinion_cn TEXT DEFAULT '';
EOF
```

### 翻译脚本
```bash
cd /root/tool-seeker/backend
python3 translate.py --db 50    # 翻译数据库中 50 条未翻译内容
python3 translate.py "Hello"    # 测试翻译单个文本
```

### 免费翻译 API
| API | 限额 | 质量 | 配置 |
|-----|------|------|------|
| MyMemory | 1000 字符/天 | 中等 | 无需 Key |
| LibreTranslate | 速率限制 | 中等 | 无需 Key |
| DeepL | 50 万字符/月 | 优秀 | 需 API Key |

### 前端切换功能
- 🌐 标签：显示内容已翻译
- 🔤 按钮：鼠标悬停时出现，切换原文/译文
- 默认显示中文，点击切换英文原文

### API 返回逻辑
```python
# 优先返回中文，无中文则返回原文
"title": n.title_cn or n.title
"summary": n.summary_cn or n.summary
"opinion": n.opinion_cn or n.opinion
```

### 故障排查
```bash
# 检查翻译脚本
python3 translate.py --help

# 测试翻译 API
curl "https://api.mymemory.translated.net/get?q=Hello&langpair=en|zh"

# 检查翻译状态
sqlite3 toolseeker.db "SELECT id, title, title_cn FROM daily_news LIMIT 5"
```

## 栏目分类
| 分类 | 代码 | 说明 |
|------|------|------|
| AI 圈内 | ai | 大模型/技术突破 |
| 产业落地 | industry | 企业应用/商业案例 |
| 商机雷达 | opportunity | 投资机会/创业方向 |
| 冷思考 | thinking | 深度观点/行业反思 |

## 故障排查

### RSS 抓取失败
```bash
# 测试 RSS 源
python3 -c "import feedparser; f=feedparser.parse('https://news.ycombinator.com/rss'); print(len(f.entries))"
```

### 数据库连接失败
```bash
# 检查数据库
ls -la /root/tool-seeker/backend/toolseeker.db
```

### 服务未启动
```bash
pm2 status
pm2 logs toolseeker-web --lines 20
```

## 注意事项
- 每天最多抓取 16 条新闻
- 需要配置 AI API Key 才能生成 opinion
- 日志保存在 `logs/fetch.log`