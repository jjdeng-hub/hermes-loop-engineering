---
name: website-design-upgrade
description: 为 Next.js + Tailwind CSS 项目生成完整的设计升级规范文档
version: 1.0
created: 2026-05-06
---

# 网站设计升级规范生成

> 为 Next.js + Tailwind CSS 项目生成完整的设计升级规范文档，涵盖色彩、字体、组件、动效、暗色模式等。

## 触发条件

- 用户需要重构/升级现有网站的设计
- 用户希望让网站"更高级、更好看、更好用"
- 项目使用 Next.js + Tailwind CSS 技术栈

## 工作流程

### 1. 网站现状诊断

```bash
# 访问网站获取 HTML 内容
curl -s "http://your-site.com" | head -c 5000

# 或使用浏览器工具
browser_navigate(url="http://your-site.com")
browser_snapshot()
```

### 2. 技术分析

提取以下信息：
- **技术栈**：Next.js 版本、Tailwind CSS、shadcn/ui 等
- **色彩系统**：当前使用的颜色变量、CSS 变量
- **字体系统**：Google Fonts、字体层级
- **布局系统**：容器宽度、网格配置、断点
- **组件样式**：按钮、卡片、导航栏等现有样式
- **交互效果**：动画、过渡、Hover 效果

### 3. 设计规范生成

创建 `design-spec.md` 文件，包含以下章节：

#### 3.1 色彩系统

```javascript
// tailwind.config.js 语义化颜色配置
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: { 50: '#...', 500: '#3B82F6', ... },
        accent: { purple: '#8B5CF6', cyan: '#06B6D4', ... },
        neutral: { 50: '#FAFBFC', 900: '#111827', ... },
      },
    },
  },
}
```

```css
/* globals.css CSS 变量（支持主题切换） */
:root {
  --color-primary: #3B82F6;
  --text-primary: #111827;
  --bg-primary: #FAFBFC;
  /* ... */
}
.dark {
  --color-primary: #60A5FA;
  --text-primary: #F1F5F9;
  --bg-primary: #0F172A;
  /* ... */
}
```

#### 3.2 字体系统

```html
<!-- Google Fonts 引入 -->
<link href="https://fonts.googleapis.com/css2?family=Inter&family=Noto+Sans+SC&family=Noto+Serif+SC&display=swap" rel="stylesheet"/>
```

| 元素 | 字体 | 大小 | 字重 | 行高 |
|------|------|------|------|------|
| H1 | Noto Serif SC | 48px | 700 | 1.1 |
| 正文 | Noto Sans SC | 16px | 400 | 1.7 |

#### 3.3 组件规范

为每个组件提供完整的 Tailwind 类名：

```tsx
/* 按钮 */
.btn-primary {
  @apply inline-flex items-center justify-center;
  @apply px-6 py-3 bg-primary-500 hover:bg-primary-600;
  @apply text-white rounded-lg font-medium;
  @apply transition-all duration-200 shadow-md hover:shadow-lg;
  @apply hover:-translate-y-0.5 active:translate-y-0;
}

/* 卡片 */
.card {
  @apply bg-bg-secondary rounded-xl border border-border-light;
  @apply shadow-sm transition-all duration-300;
}
.card-hover {
  @apply cursor-pointer hover:-translate-y-1 hover:shadow-lg;
}
```

#### 3.4 交互与动效

```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in { animation: fadeIn 0.3s ease-out; }
.stagger-1 { animation-delay: 0.05s; }
.stagger-2 { animation-delay: 0.1s; }
```

#### 3.5 暗色模式

```tsx
// components/ThemeToggle.tsx
'use client';
import { useEffect, useState } from 'react';

export function ThemeToggle() {
  const [isDark, setIsDark] = useState(false);
  
  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDark);
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  }, [isDark]);
  
  return (
    <button onClick={() => setIsDark(!isDark)}>
      {isDark ? '☀️' : '🌙'}
    </button>
  );
}
```

### 4. 实施优先级

| 优先级 | 任务 | 预估时间 |
|--------|------|---------|
| 🔴 P0 | 暗色模式完整支持 | 2-3 天 |
| 🔴 P0 | Hero 区域重构 | 1-2 天 |
| 🔴 P0 | 色彩系统重构 | 0.5 天 |
| 🟡 P1 | 卡片设计升级 | 2 天 |
| 🟡 P1 | 微交互完善 | 2-3 天 |
| 🟢 P2 | 字体系统优化 | 0.5 天 |
| 🟢 P2 | 性能优化 | 1-2 天 |

### 5. 输出文件

将规范保存到项目根目录：

```
design-spec.md
```

用户可将其导入 coding 软件（Cursor/Claude Code），输入：

```
请根据 design-spec.md 中的设计规范，帮我重构网站。
优先实现 P0 任务。
```

## 注意事项

1. **保持克制**：动效要适度，过度动画会显得廉价
2. **一致性**：建立统一的设计系统（颜色/间距/字体/圆角）
3. **先做减法**：强化品牌属性，而非纯工具列表风格
4. **暗色模式必做**：技术类网站用户普遍偏好暗色
5. **对比度检查**：确保文字与背景对比度 ≥ 4.5:1

## 相关文件

- `design-spec.md` — 生成的设计规范文档
- `tailwind.config.ts` — 需要更新的 Tailwind 配置
- `app/globals.css` — 需要更新的 CSS 变量

## 经验总结

- 使用语义化颜色命名（primary、accent、neutral）而非随意色值
- CSS 变量 + Tailwind 类名组合，支持主题切换
- 组件规范提供完整 Tailwind 类名，可直接复制使用
- 优先级排序帮助用户聚焦核心改进

---

## V2 横向布局设计模式（新增）

### 触发条件

- 用户反馈网站"太竖屏化"、"信息过于居中"、"页面太长"
- 希望提升信息密度，让内容"铺展开"而非"堆叠起来"

### 核心设计原则

| 原则 | 说明 |
|------|------|
| **横向优先** | Hero 区域左右分栏，内容区主栏 + 侧边栏 |
| **信息密度** | 减少 section 间距，压缩卡片内边距 |
| **Dashboard 风格** | 顶部 Tab 导航，固定侧边栏，主内容滚动 |
| **视觉层次** | 主内容区 1400px（非 800px），卡片 3-4 列 |

### 布局配置

```css
/* 容器宽度 */
@media (min-width: 1280px) {
  .container { max-width: 1400px; }  /* 横向布局最大宽度 */
}

/* 主内容 + 侧边栏布局 */
@media (min-width: 1024px) {
  .dashboard-grid {
    display: grid;
    grid-template-columns: 1fr 320px;  /* 65% + 35% */
    gap: 24px;
  }
  .sidebar {
    position: sticky;
    top: 64px;  /* 导航栏高度 */
    height: calc(100vh - 64px);
  }
}
```

### 间距压缩对比

| 用途 | V1（竖屏） | V2（横向） |
|------|-----------|-----------|
| Section 间距 | `py-12 lg:py-16` | `py-6 lg:py-8` |
| 卡片内边距 | `p-6` | `p-3.5` |
| 卡片间距 | `gap-4 sm:gap-6` | `gap-3 sm:gap-4` |
| Hero 高度 | `py-16 sm:py-20` | `py-8 lg:py-12` |
| 导航栏高度 | `h-14 (56px)` | `h-12 (48px)` |
| 圆角 | `rounded-xl (16px)` | `rounded-lg (8px)` |

### 响应式断点

| 断点 | 宽度 | 布局 |
|------|------|------|
| Mobile | < 640px | 单列堆叠 |
| Tablet | 640-1024px | 2 列网格，无侧边栏 |
| Desktop | 1024-1280px | 3 列网格，无侧边栏 |
| Wide | ≥ 1280px | 主内容 + 侧边栏，4 列网格 |

### Hero 区域左右分栏模式

```tsx
<section className="py-8 lg:py-12">
  <div className="max-w-[1400px] mx-auto px-4 lg:px-6">
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
      {/* Left: Title + Search + CTA */}
      <div className="order-1">
        <h1>...</h1>
        <input placeholder="搜索..." />
        <div className="flex gap-3">...</div>
      </div>
      {/* Right: Stats + Quick Access */}
      <div className="order-2 flex flex-col gap-4">
        <div className="bg-[var(--bg)] rounded-lg p-4">
          <div className="grid grid-cols-3 gap-3">
            <div>73+ 工具</div>
            <div>5 日报</div>
            <div>12 免费</div>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <Link>AI 写作</Link>
          <Link>AI 绘画</Link>
          ...
        </div>
      </div>
    </div>
  </div>
</section>
```

---

## 部署自动化流程

### SSH 密钥部署（推荐）

1. **生成专用 SSH 密钥**：
   ```bash
   ssh-keygen -t ed25519 -C "deploy@yourdomain.com" -f ~/.ssh/id_ed25519_deploy
   ```

2. **配置 SSH config**：
   ```
   Host gitee.com
       HostName gitee.com
       User git
       IdentityFile ~/.ssh/id_ed25519_deploy
       IdentitiesOnly yes
   ```

3. **添加 Gitee host key**：
   ```bash
   ssh-keyscan -t ed25519 gitee.com >> ~/.ssh/known_hosts
   ```

4. **切换 Git 远程仓库**：
   ```bash
   git remote set-url origin git@gitee.com:user/repo.git
   ```

### 服务器部署流程

```bash
# 1. 同步代码（rsync 高效增量同步）
rsync -avz --delete ./frontend/src/ root@server:/root/project/frontend/src/

# 2. 服务器构建
cd /root/project/frontend
npm run build

# 3. PM2 重启服务
pm2 delete web-app
pm2 start npm --name web-app -- start
pm2 save

# 4. 验证
curl -s -o /dev/null -w "HTTP: %{http_code}\n" http://localhost:3000
pm2 status web-app
```

### 构建故障排除

**lightningcss 原生模块缺失**：
```bash
# 症状：Cannot find module '../lightningcss.linux-x64-gnu.node'
# 解决：清理缓存后重新构建
rm -rf .next
npm run build
```

**端口冲突**：
```bash
# 检查端口占用
ss -tlnp | grep 3000
# 停止旧进程
pm2 stop web-app && pm2 delete web-app
# 重新启动
pm2 start npm --name web-app -- start
```

### 自动化部署脚本（可保存为 skill）

```bash
#!/bin/bash
# deploy.sh - 一键部署脚本

SERVER="122.51.91.167"
PROJECT="/root/tool-seeker/frontend"

echo "🚀 开始部署..."

# 同步代码
rsync -avz --delete ./src/ root@$SERVER:$PROJECT/src/

# 服务器构建 + 重启
ssh root@$SERVER << 'EOF'
cd /root/tool-seeker/frontend
pm2 stop toolseeker-web 2>/dev/null || true
npm run build
pm2 delete toolseeker-web 2>/dev/null || true
pm2 start npm --name toolseeker-web -- start
pm2 save
curl -s -o /dev/null -w "HTTP: %{http_code}\n" http://localhost:3000
EOF

echo "✅ 部署完成"
```