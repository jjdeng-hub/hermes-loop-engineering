---
name: github-content-download
description: GitHub 内容下载网络故障排除方案 - 使用 GitHub API 替代 git clone/curl
tags: [github, network, workaround, download]
---

# GitHub Content Download - Network Workaround

> 当 git clone / curl 下载 GitHub 内容失败时，使用 GitHub API 获取内容的可靠方法

## 触发条件

- git clone 超时或失败
- curl 下载 raw.githubusercontent.com 超时
- 需要从 GitHub 获取文件内容但网络受限

## 核心发现

**GitHub API 通常可用，即使直接下载失败**

| 方法 | 可用性 | 说明 |
|------|--------|------|
| `git clone` | ❌ 经常超时 | 需要完整传输 |
| `curl raw.githubusercontent.com` | ❌ 经常超时 | 需要完整传输 |
| `api.github.com/repos/.../contents` | ✅ 通常可用 | 返回 base64 编码内容 |
| `api.github.com/repos/.../readme` | ✅ 通常可用 | 返回 README 内容 |
| `api.github.com/repos/.../git/trees` | ✅ 通常可用 | 返回文件树结构 |

## 使用方法

### 获取单个文件

```bash
curl -s --max-time 30 "https://api.github.com/repos/{owner}/{repo}/contents/{path}" | \
python3 -c "
import sys, json, base64
d = json.load(sys.stdin)
content = base64.b64decode(d['content']).decode('utf-8')
print(content)
"
```

### 保存到文件

```bash
curl -s --max-time 30 "https://api.github.com/repos/{owner}/{repo}/contents/{path}" > api_response.json && \
python3 -c "
import json, base64
with open('api_response.json') as f:
    d = json.load(f)
content = base64.b64decode(d['content']).decode('utf-8')
with open('output.md', 'w') as f:
    f.write(content)
print(f'Written {len(content)} chars')
"
```

### 获取目录树

```bash
curl -s --max-time 30 "https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1" | \
python3 -c "
import sys, json
d = json.load(sys.stdin)
for f in d.get('tree', []):
    print(f'{f[\"type\"]}: {f[\"path\"]}')
"
```

### 批量下载文件

```bash
for path in file1.md file2.md file3.md; do
  curl -s --max-time 30 "https://api.github.com/repos/{owner}/{repo}/contents/$path" > tmp.json && \
  python3 -c "
import json, base64
with open('tmp.json') as f:
    d = json.load(f)
content = base64.b64decode(d['content']).decode('utf-8')
with open('${path}', 'w') as f:
    f.write(content)
print('Downloaded: ${path}')
" && rm tmp.json
done
```

## 注意事项

1. **API 限制**: GitHub API 有速率限制（未认证 60 次/小时，认证 5000 次/小时）
   - ⚠️ **速率限制触发**: 返回 `{"message":"API rate limit exceeded"}` 时，需等待或改用其他方式
   - **解决方案**: 分批下载，每批之间等待 1-2 分钟；或使用认证 token 提升限额
2. **内容大小**: 单个文件超过 1MB 会被截断，需使用 `git` 树 API 配合 `sha` 下载
3. **base64 解码**: 必须使用 Python 的 `base64.b64decode()` 解码
4. **错误处理**: 
   - API 返回 403 表示速率限制
   - API 返回 404 表示文件不存在
   - API 返回 `{"message": ...}` 无 `content` 字段时，检查错误信息

## 实战经验 (2026-05-05)

### 成功下载 agency-agents-zh (37 个文件)

**命令模板**（已验证可用）：
```bash
# 1. 先获取目录结构
curl -s --max-time 30 "https://api.github.com/repos/jnMetaCode/agency-agents-zh/git/trees/main?recursive=1" | \
python3 -c "import sys,json; d=json.load(sys.stdin); [print(f['path']) for f in d.get('tree',[]) if f['type']=='blob' and f['path'].endswith('.md')]"

# 2. 批量下载（注意速率限制，分批进行）
for f in file1.md file2.md file3.md; do
  curl -s --max-time 30 "https://api.github.com/repos/jnMetaCode/agency-agents-zh/contents/marketing/${f}" 2>&1 > tmp.json && \
  python3 -c "
import json, base64
with open('tmp.json') as f:
    d = json.load(f)
if 'content' in d:
    content = base64.b64decode(d['content']).decode('utf-8')
    with open('marketing/${f}', 'w') as f:
        f.write(content)
    print('Downloaded: marketing/${f}')
else:
    print('Error:', d.get('message', 'unknown'))
" && rm -f tmp.json
done

# 3. 检查速率限制状态
curl -s -I "https://api.github.com/rate_limit" | grep -i x-ratelimit
```

### 失败案例与解决方案

| 失败方式 | 原因 | 解决方案 |
|----------|------|----------|
| `git clone` 超时 | 网络连接 GitHub 不稳定 | 改用 GitHub API |
| `curl raw.githubusercontent.com` 超时 | 需要完整传输 | 改用 GitHub API |
| API 速率限制 | 未认证请求 60 次/小时 | 分批下载，或等待 |
| `KeyError: 'content'` | API 返回错误而非文件内容 | 检查 `d.get('message')` |

### 转换 OpenClaw 格式到 Hermes 格式

agency-agents-zh 等仓库使用 OpenClaw 的 agent 文件格式：

```markdown
---
name: AI 工程师
description: ...
color: purple
---

# AI 工程师

你是**AI 工程师**...
```

**Hermes 格式需要**: `SKILL.md` 文件，包含触发条件、使用方法、可用资源等。

### 转换步骤

1. 读取 OpenClaw agent 文件
2. 提取 frontmatter 中的 name/description
3. 创建 `SKILL.md` 描述如何使用这些角色
4. 将 agent 文件保存到 `agents/` 子目录
5. 使用时告诉 AI 激活哪个角色

## 转换 OpenClaw 格式到 Hermes 格式

agency-agents-zh 等仓库使用 OpenClaw 的 agent 文件格式：

```markdown
---
name: AI 工程师
description: ...
color: purple
---

# AI 工程师

你是**AI 工程师**...
```

**Hermes 格式需要**: `SKILL.md` 文件，包含触发条件、使用方法、可用资源等。

### 转换步骤

1. 读取 OpenClaw agent 文件
2. 提取 frontmatter 中的 name/description
3. 创建 `SKILL.md` 描述如何使用这些角色
4. 将 agent 文件保存到 `agents/` 子目录
5. 使用时告诉 AI 激活哪个角色

## 验证

```bash
# 检查文件是否下载成功
ls -la ~/.hermes/skills/{skill-name}/

# 检查文件内容是否可读
head -20 ~/.hermes/skills/{skill-name}/agents/*.md
```

## 相关技能

- `github-python-install` - Python 项目安装
- `awesome-hermes-agent` - Hermes 生态资源导航