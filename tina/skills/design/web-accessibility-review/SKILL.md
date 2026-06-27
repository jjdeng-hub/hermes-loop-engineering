---
name: web-accessibility-review
description: 网站无障碍与视觉设计审查工作流 — WCAG 对比度分析、ARIA 标签添加、主题切换实现
---

# Web 无障碍与设计审查工作流

> 系统化审查网站设计，确保符合 WCAG 2.1 AA 标准，提升用户体验和可访问性

## 触发条件

当用户要求：
- "帮我审视网站设计"
- "检查无障碍问题"
- "优化网站可访问性"
- "改进设计系统"

## 工作流

### 第一步：角色激活

**必须激活以下角色**：
1. `design-ui-designer` - 视觉设计系统专家
2. `design-ux-architect` - UX 基础设施专家

```bash
# 加载角色文件作为系统提示词
cat ~/.hermes/skills/agency-agents-zh/agents/design/design-ui-designer.md
cat ~/.hermes/skills/agency-agents-zh/agents/design/design-ux-architect.md
```

### 第二步：WCAG 对比度分析

**使用 Python 脚本计算对比度**：

```python
def relative_luminance(r, g, b):
    """计算相对亮度 (WCAG 2.1 公式)"""
    def adjust(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

def contrast_ratio(hex1, hex2):
    """计算两个颜色的对比度"""
    def hex_to_rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    l1 = relative_luminance(*hex_to_rgb(hex1))
    l2 = relative_luminance(*hex_to_rgb(hex2))
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)

def wcag_rating(ratio):
    """WCAG 评级"""
    if ratio >= 7: return "AAA ✅"
    elif ratio >= 4.5: return "AA ✅"
    elif ratio >= 3: return "AA Large ⚠️"
    else: return "Fail ❌"
```

**检查标准**：
| 文本类型 | 最小对比度 | 说明 |
|----------|-----------|------|
| 正常文本 | 4.5:1 | 小于 18pt 或 14pt 粗体 |
| 大文本 | 3:1 | 大于 18pt 或 14pt 粗体 |
| UI 组件 | 3:1 | 按钮、输入框边框等 |

### 第三步：优先级分类

| 优先级 | 改进项 | 影响 | 工作量 |
|--------|--------|------|--------|
| **P0** | 对比度不达标 | 无障碍合规 | 低 |
| **P0** | 缺少主题切换 | 用户体验 | 中 |
| **P1** | 缺少 ARIA 标签 | 无障碍合规 | 低 |
| **P1** | 图片无懒加载 | 性能 | 中 |
| **P2** | Hero 信息密度高 | 视觉焦点 | 低 |
| **P2** | 缺少空状态引导 | 用户体验 | 低 |
| **P3** | 缺少数据缓存 | 性能 | 中 |

### 第四步：执行改进

#### P0-1：修复对比度

```css
/* 修复示例：accent-green 从 #10B981 (2.54:1 ❌) → #0B875E (4.52:1 ✅) */
:root {
  /* 对比度检查: vs #FFFFFF = 4.52:1 ✅ AA */
  --accent-green: #0B875E;
}
```

**技巧**：使用 `find_compliant_color()` 函数自动找到符合 AA 标准的替代色。

#### P0-2：主题切换组件

```tsx
'use client';
import { useState, useEffect } from 'react';

export function ThemeToggle() {
  const [theme, setTheme] = useState<'light' | 'dark' | 'system'>('system');
  
  useEffect(() => {
    // 从 localStorage 读取或检测系统偏好
    const stored = localStorage.getItem('theme');
    const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    // ... 应用主题
  }, []);
  
  // 监听系统偏好变化
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', () => {
      if (theme === 'system') applyTheme(mediaQuery.matches ? 'dark' : 'light');
    });
  }, [theme]);
}
```

#### P1-1：ARIA 标签

| 元素 | ARIA 属性 | 示例 |
|------|----------|------|
| 搜索框 | `aria-label`, `aria-describedby`, `type="search"` | `<input aria-label="搜索 AI 工具" type="search">` |
| 按钮组 | `role="group"`, `aria-label` | `<div role="group" aria-label="主要行动按钮">` |
| 导航 | `role="navigation"`, `aria-label` | `<nav role="navigation" aria-label="主导航">` |
| 动态菜单 | `aria-expanded`, `aria-controls` | `<button aria-expanded={open} aria-controls="menu">` |
| 错误提示 | `role="alert"`, `aria-live="polite"` | `<div role="alert">` |

#### P1-2：图片懒加载

```tsx
import Image from 'next/image';

<Image
  src={tool.logo_url}
  alt={`${tool.name} 图标`}  /* 语义化 alt */
  width={44}
  height={44}
  className="w-11 h-11 rounded-lg"
  loading="lazy"  /* 懒加载 */
  unoptimized={tool.logo_url.startsWith('http')}  /* 外部图片支持 */
/>
```

### 第五步：验证

1. **对比度验证**：重新运行 Python 脚本确认所有颜色符合 AA
2. **ARIA 验证**：使用 Chrome DevTools Accessibility 面板检查
3. **主题切换验证**：手动切换亮色/暗色/系统，确认平滑过渡
4. **图片加载验证**：使用 Lighthouse 检查 CLS（布局偏移）

## 交付模板

```markdown
# [项目名称] 无障碍与设计审查报告

## WCAG 对比度分析

### 亮色主题
| 颜色 | 原值 | 新值 | 对比度 | 状态 |
|------|------|------|--------|------|
| --blue | #3B82F6 | #3473DA | 4.55:1 | ✅ AA |

### 暗色主题
| 颜色 | 值 | 对比度 | 状态 |
|------|-----|--------|------|
| --heading | #F1F5F9 | 13.35:1 | ✅ AAA |

## ARIA 标签添加

| 元素 | 添加的 ARIA | 说明 |
|------|-------------|------|
| 搜索框 | aria-label, type="search" | 屏幕阅读器可识别 |

## 主题切换

- ✅ 亮色/暗色/系统三模式
- ✅ localStorage 持久化
- ✅ 系统偏好自动检测

## 改进优先级

| 优先级 | 状态 |
|--------|------|
| P0 | ✅ 完成 |
| P1 | ✅ 完成 |
| P2 | ✅ 完成 |
| P3 | ⏳ 待执行 |
```

## 常见陷阱

1. **CSS 变量硬编码**：不要在组件中硬编码颜色值，使用 CSS 变量
2. **忽略暗色主题**：修复亮色主题时，同步检查暗色主题对比度
3. **ARIA 过度使用**：语义化 HTML 优先，ARIA 作为补充
4. **图片 alt 为空**：装饰性图片用 `alt=""`，内容图片必须描述内容

## 成功指标

- 所有文本对比度 ≥ 4.5:1（AA）
- 关键交互元素有 ARIA 标签
- 主题切换平滑无闪烁
- Lighthouse Accessibility 评分 ≥ 90