---
name: nextjs-api-debug
description: Next.js API 路由调试指南 - 解决 rewrite 冲突、localhost DNS、静态渲染等问题
tags: [nextjs, api, debugging, deployment]
---

# Next.js API 路由调试指南

## 适用场景
- Next.js App Router 项目中 API 路由返回空数据或错误
- 前端 API 路由与后端代理 rewrite 配置冲突
- 生产模式下 fetch 请求失败

## 常见症状
- API 返回 `[]` 或空对象
- API 返回 `{"error": "Backend unreachable"}`
- 数据库有数据但前端显示为空

## 排查步骤

### 1. 检查 rewrite 配置冲突
**问题**: `next.config.ts` 中的 rewrite 规则可能覆盖前端自己的 API 路由

```typescript
// ❌ 错误配置 - 覆盖所有 /api/*
{
  source: '/api/:path*',
  destination: 'http://localhost:8002/api/:path*',
}

// ✅ 正确配置 - 只重写特定路径
{
  source: '/api/backend/:path*',
  destination: 'http://localhost:8002/api/:path*',
}
```

**验证方法**:
```bash
# 检查后端直接返回
curl http://localhost:8002/api/tools

# 检查前端 API 返回
curl http://localhost:3000/api/tools
```

### 2. 检查 localhost DNS 问题
**问题**: 生产模式下 Next.js 的 fetch 可能无法正确解析 `localhost`

```typescript
// ❌ 可能失败
const res = await fetch('http://localhost:8002/api/tools');

// ✅ 推荐
const res = await fetch('http://127.0.0.1:8002/api/tools');
```

### 3. 检查静态渲染 vs 动态渲染
**问题**: API 路由默认静态渲染，fetch 在构建时执行而非运行时

```typescript
// ✅ 强制动态渲染
export const dynamic = 'force-dynamic'

export async function GET() {
  const res = await fetch('http://127.0.0.1:8002/api/tools');
  return Response.json(await res.json());
}
```

**验证**: 构建日志中 API 路由应显示为 `ƒ (Dynamic)` 而非 `○ (Static)`

### 4. 检查后端服务状态
```bash
# PM2 检查
pm2 status

# 检查端口监听
ss -tlnp | grep 8002

# 测试后端直接访问
curl http://127.0.0.1:8002/api/tools
```

## 完整修复示例

### next.config.ts
```typescript
async rewrites() {
  return [
    {
      source: '/api/backend/:path*',
      destination: 'http://127.0.0.1:8002/api/:path*',
    },
  ];
}
```

### src/app/api/tools/route.ts
```typescript
export const dynamic = 'force-dynamic'
const BACKEND_URL = 'http://127.0.0.1:8002'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  let url = `${BACKEND_URL}/api/tools`
  // ... 处理参数
  try {
    const res = await fetch(url)
    return Response.json(await res.json())
  } catch (e) {
    console.error('Backend fetch error:', e)
    return Response.json({ error: "Backend unreachable" }, { status: 503 })
  }
}
```

## 部署后验证清单
- [ ] 后端服务运行中 (`pm2 status`)
- [ ] 后端端口监听 (`ss -tlnp`)
- [ ] 后端 API 直接访问正常 (`curl localhost:8002/api/...`)
- [ ] 前端 API 返回数据 (`curl localhost:3000/api/...`)
- [ ] 浏览器访问网站数据正常显示

### 5. 检查 Nginx 代理配置（外部访问时）
**问题**: Nginx 的 `location /api/` 规则可能覆盖 Next.js 自己的 API 路由

```nginx
# ❌ 错误配置 - 拦截所有 /api/
location /api/ {
    proxy_pass http://127.0.0.1:8002/;
}

# ✅ 正确配置 - 只对 /api/backend/ 进行代理
location /api/backend/ {
    proxy_pass http://127.0.0.1:8002/;
}
# 其他 /api/* 由 Next.js 处理
location / {
    proxy_pass http://127.0.0.1:3000;
}
```

**验证方法**:
```bash
# 本地访问（绕过 Nginx）
curl http://localhost:3000/api/tools

# 外部访问（经过 Nginx）
curl http://服务器IP/api/tools

# 如果本地正常但外部返回 {"detail":"Not Found"} → Nginx 配置问题
```

**检查 Nginx 日志**:
```bash
tail -f /var/log/nginx/error.log
```

## 排查顺序（推荐）
1. **后端直接访问** → `curl localhost:8002/api/tools`
2. **前端本地访问** → `curl localhost:3000/api/tools`
3. **外部访问** → `curl 服务器IP/api/tools`
4. 根据哪一步失败定位问题层级

## 教训总结
1. **先验证后端**：确保后端 API 本身正常，再排查前端
2. **注意 rewrite 范围**：避免覆盖前端自己的 API 路由
3. **localhost vs 127.0.0.1**：生产环境优先使用 IP
4. **动态渲染标记**：运行时 fetch 必须添加 `dynamic = 'force-dynamic'`
5. **Nginx 代理优先级**：外部访问时 Nginx 的 `location /api/` 会覆盖 Next.js 的 API 路由，需使用 `/api/backend/` 前缀区分