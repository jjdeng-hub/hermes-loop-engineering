---
name: navigation-ux-optimization
description: 网站导航与页面跳转 UX 优化指南 - 导航高亮、返回路径、全局导航一致性
category: frontend
trigger: 当需要优化网站导航、页面跳转逻辑、全局导航一致性时
---

# Navigation UX Optimization

## 核心问题

### 问题 1：导航栏无当前页面高亮

**现象**：用户无法直观知道自己当前在哪个页面。

**解决方案**：使用 `usePathname()` 检测当前路径，匹配导航链接。

```tsx
'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';

const NAV_LINKS = [
  { href: '/daily', label: 'AI 日报' },
  { href: '/tutorials', label: '实战教程' },
  { href: '/skills', label: 'Skill 库' },
  { href: '/tools', label: '工具导航' },
];

export default function Nav() {
  const pathname = usePathname();

  return (
    <nav>
      {NAV_LINKS.map((link) => {
        // 精确匹配或前缀匹配（处理子页面）
        const isActive = pathname === link.href || 
                         (link.href !== '/' && pathname.startsWith(link.href + '/'));
        
        return (
          <Link
            key={link.href}
            href={link.href}
            className={isActive ? 'active-style' : 'normal-style'}
          >
            {link.label}
          </Link>
        );
      })}
    </nav>
  );
}
```

**样式建议**：
```css
/* 激活状态：品牌色背景 + 品牌色文字 */
.active-style {
  background: var(--blue)/10;
  color: var(--blue);
}

/* 正常状态：默认文字色 */
.normal-style {
  color: var(--body);
}
```

---

### 问题 2：详情页返回路径不合理

**现象**：用户从列表页进入详情页，点击"返回"跳回首页，而不是返回列表页。

**解决方案**：提供智能返回路径，优先返回来源页面。

```tsx
'use client';

import { useRouter } from 'next/navigation';

export default function DetailPage() {
  const router = useRouter();

  // 智能返回路径
  const getBackPath = () => {
    // 从 document.referrer 判断来源
    if (document.referrer.includes('/tools')) {
      return '/tools';
    }
    if (document.referrer.includes('/tutorials')) {
      return '/tutorials';
    }
    // 默认返回对应列表页
    return '/tools';
  };

  const handleBack = () => {
    router.push(getBackPath());
  };

  return (
    <button onClick={handleBack}>
      ← 返回列表
    </button>
  );
}
```

**UX 原则**：
- 用户从哪来，就回哪去
- 避免"迷路"感
- 保持浏览路径连贯

---

### 问题 3：Footer 链接不完整

**现象**：Footer 缺少部分主要板块入口，用户需要回到顶部才能导航。

**解决方案**：Footer 包含所有主要板块链接。

```tsx
const FOOTER_LINKS = [
  { href: '/daily', label: 'AI 日报' },
  { href: '/tutorials', label: '实战教程' },
  { href: '/skills', label: 'Skill 库' },
  { href: '/tools', label: '工具导航' },
  { href: '/submit', label: '提交工具' },
];

export default function Footer() {
  return (
    <footer>
      {FOOTER_LINKS.map((link) => (
        <Link key={link.href} href={link.href}>
          {link.label}
        </Link>
      ))}
    </footer>
  );
}
```

**UX 原则**：
- Footer 是全局导航的最后一道防线
- 所有主要板块都应有入口
- 保持 Nav 和 Footer 的一致性

---

### 问题 4：搜索使用硬跳转

**现象**：使用 `window.location.href` 触发完整页面刷新。

**解决方案**：使用表单提交，语义更清晰。

```tsx
// ❌ 不推荐： onKeyDown 硬跳转
<input
  onKeyDown={(e) => {
    if (e.key === 'Enter') {
      window.location.href = `/tools?search=${query}`;
    }
  }}
/>

// ✅ 推荐：表单提交
<form onSubmit={(e) => {
  e.preventDefault();
  window.location.href = `/tools?search=${query}`;
}}>
  <input type="search" value={query} onChange={...} />
</form>
```

**注意**：如果追求 SPA 体验，可以使用 `router.push()` 替代 `window.location.href`。

---

## 检查清单

### 导航栏检查
- [ ] 当前页面有高亮状态
- [ ] 高亮样式与品牌色一致
- [ ] 移动端菜单也有高亮
- [ ] 子页面能正确匹配父级导航

### 返回路径检查
- [ ] 详情页有"返回"按钮
- [ ] 返回目标是来源列表页
- [ ] 使用 `router.push()` 保持 SPA 体验

### Footer 检查
- [ ] 包含所有主要板块链接
- [ ] 与 Nav 链接一致
- [ ] 移动端友好显示

### 搜索检查
- [ ] 使用 `<form>` 语义
- [ ] Enter 键触发搜索
- [ ] 搜索结果 URL 清晰

---

## 相关文件

- `components/Nav.tsx` - 主导航组件
- `components/Footer.tsx` - 页脚导航
- `app/page.tsx` - 首页搜索
- `app/tools/[id]/page.tsx` - 工具详情页返回

---

## 实践总结（2026-05-08）

1. **导航高亮**：使用 `usePathname()` + 前缀匹配，支持子页面
2. **返回路径**：优先从 `document.referrer` 判断来源，默认返回对应列表页
3. **Footer 一致性**：与 Nav 使用相同的链接配置，避免遗漏
4. **搜索语义**：使用 `<form>` 替代 `onKeyDown`，更符合 HTML 语义