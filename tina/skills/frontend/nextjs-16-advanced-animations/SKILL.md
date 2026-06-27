---
name: nextjs-16-advanced-animations
description: Next.js 16 + Tailwind CSS 高级动画集成指南 - 解决 framer-motion 兼容性问题，使用纯 CSS 实现高级视觉效果
---

# Next.js 16 高级动画集成指南

## 触发条件

当需要为 Next.js 16 + Tailwind CSS 项目添加高级动画效果（鼠标跟随光效、卡片悬停动画、文字逐字显示等）时。

## 核心问题

### 问题 1：framer-motion 与 Next.js 16 Turbopack 兼容性问题

**现象**：
```
Type error: Cannot find module 'framer-motion' or its corresponding type declarations.
Argument of type '{ [x: string]: MotionValue<any>; }' is not assignable to parameter of type 'number'.
```

**根因**：
- framer-motion v12 的 TypeScript 类型与 Next.js 16 Turbopack 存在兼容性问题
- 即使源码中没有使用 framer-motion，TypeScript 缓存仍可能引用旧类型定义

**解决方案**：
使用纯 CSS + Tailwind 动画替代 framer-motion：

```tsx
// ❌ 避免使用
import { motion, useSpring, useTransform } from 'framer-motion';

// ✅ 改用纯 CSS
<div className="transition-all duration-300 hover:-translate-y-1">
  {/* 内容 */}
</div>
```

### 问题 2：文件冲突（新旧组件目录）

**现象**：
构建失败，但检查 src/ 目录发现没有 framer-motion 引用

**根因**：
- 存在两个同名组件文件：
  - `components/ui/card-hover-effect.tsx`（旧，使用 framer-motion）
  - `src/components/ui/card-hover-effect.tsx`（新，纯 CSS）
- Next.js 可能优先加载非 src/ 目录的文件

**解决方案**：
```bash
# 检查所有同名文件
find . -name "card-hover-effect.tsx" -type f

# 删除旧目录中的冲突文件
rm -rf components/ui/
```

### 问题 3：TypeScript 缓存导致构建失败

**现象**：
删除 framer-motion 后构建仍报错

**根因**：
TypeScript 增量编译缓存（.tsbuildinfo）仍引用旧类型

**解决方案**：
```bash
# 彻底清理所有缓存
rm -rf .next node_modules/.cache
rm -rf .next/cache/.tsbuildinfo

# 重新构建
npm run build
```

### 问题 4：Next.js 16 部署输出目录变化

**现象**：
使用 `out/` 目录部署失败

**根因**：
Next.js 16 默认使用 App Router + Server Components，输出在 `.next/` 目录

**解决方案**：
```bash
# 正确部署方式
rsync -avz --delete .next/ root@server:/root/tool-seeker/.next/
rsync -avz --delete public/ root@server:/root/tool-seeker/public/
rsync -avz package.json root@server:/root/tool-seeker/

# 重启服务
ssh root@server "pm2 restart toolseeker-web"
```

## 推荐动画方案

### 1. Spotlight 鼠标跟随光效

```tsx
'use client';

import { useState, useEffect } from 'react';

interface SpotlightProps {
  className?: string;
  fill?: string;
}

export function Spotlight({ className = '', fill = 'white' }: SpotlightProps) {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div
      className={`pointer-events-none absolute inset-0 ${className}`}
      style={
        {
          '--spotlight-x': `${mousePosition.x}px`,
          '--spotlight-y': `${mousePosition.y}px`,
          '--spotlight-fill': fill,
        } as React.CSSProperties
      }
    />
  );
}
```

### 2. CardHoverEffect 卡片悬停动画

```tsx
'use client';

import { cn } from '@/lib/utils';

interface CardHoverEffectProps {
  children: React.ReactNode;
  className?: string;
}

export function CardHoverEffect({ children, className = '' }: CardHoverEffectProps) {
  return (
    <div className={cn(
      'relative group cursor-pointer transition-all duration-300 hover:-translate-y-1',
      className
    )}>
      <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-blue-500/20 to-purple-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      <div className="relative">{children}</div>
    </div>
  );
}
```

### 3. TextReveal 文字逐字显示

```tsx
'use client';

interface TextRevealProps {
  text: string;
  className?: string;
}

export function TextReveal({ text, className = '' }: TextRevealProps) {
  const words = text.split(' ');

  return (
    <div className={className}>
      {words.map((word, i) => (
        <span
          key={i}
          className="inline-block mr-2 animate-in fade-in slide-in-from-bottom-4"
          style={{ animationDelay: `${i * 0.1}s`, animationFillMode: 'forwards' }}
        >
          {word}
        </span>
      ))}
    </div>
  );
}
```

## 完整集成步骤

### Step 1：创建动画组件

```bash
mkdir -p src/components/ui
# 创建 spotlight.tsx, card-hover-effect.tsx, text-reveal.tsx
```

### Step 2：在页面中导入使用

```tsx
import { Spotlight } from '@/components/ui/spotlight';
import { TextReveal } from '@/components/ui/text-reveal';
import { CardHoverEffect } from '@/components/ui/card-hover-effect';

// Hero 区域
<section className="relative overflow-hidden">
  <Spotlight fill="#3b82f6" className="opacity-60" />
  {/* 内容 */}
</section>

// 卡片
<CardHoverEffect>
  <div className="bg-white rounded-xl p-5">...</div>
</CardHoverEffect>
```

### Step 3：清理旧文件

```bash
# 检查并删除冲突文件
find . -name "*.tsx" -exec grep -l "framer-motion" {} \;
rm -rf components/ui/  # 如果存在非 src/ 目录
```

### Step 4：清理缓存并构建

```bash
rm -rf .next node_modules/.cache
npm run build
```

### Step 5：部署

```bash
rsync -avz --delete .next/ root@server:/root/tool-seeker/.next/
rsync -avz --delete public/ root@server:/root/tool-seeker/public/
ssh root@server "pm2 restart toolseeker-web"
```

## 验证清单

- [ ] 构建成功（无 TypeScript 错误）
- [ ] 网站返回 HTTP 200
- [ ] Hero 区域显示鼠标跟随光效
- [ ] 卡片悬停时显示渐变光效
- [ ] 文字逐字显示动画正常
- [ ] 无 framer-motion 依赖

## 性能优化建议

1. **使用 CSS 动画而非 JS 动画** - 更流畅，不阻塞主线程
2. **添加 `will-change: transform`** - 提前告知浏览器优化
3. **限制动画触发频率** - 使用 `requestAnimationFrame` 或防抖
4. **移动端降级** - 对不支持的浏览器提供降级方案

## 替代方案

如果确实需要 framer-motion 的高级功能：

1. **降级到 Next.js 14** - 使用 Webpack 而非 Turbopack
2. **等待 framer-motion 官方修复** - 关注 GitHub issues
3. **使用 Figma 导出纯 CSS** - 将设计稿转为 CSS 动画

## 参考资源

- [Tailwind CSS 动画文档](https://tailwindcss.com/docs/animation)
- [Aceternity UI](https://ui.aceternity.com/) - 高级动画组件库
- [Framer Motion GitHub](https://github.com/framer/motion)