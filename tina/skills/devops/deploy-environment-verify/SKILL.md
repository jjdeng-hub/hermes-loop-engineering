---
name: deploy-environment-verify
description: 验证远程服务器和代码仓库的可访问性，包括网络连通性、端口开放、认证测试
version: 1.0
created: 2026-05-06
---

# 部署环境验证

> 验证远程服务器和代码仓库的可访问性，包括网络连通性、端口开放、认证测试。

## 触发条件

- 用户需要部署项目到远程服务器
- 用户提供了服务器 IP、端口、用户名、密码/密钥
- 用户提供了代码仓库地址和访问令牌
- 需要确认部署环境是否就绪

## 工作流程

### 1. 收集部署信息

从用户获取以下信息：

| 信息类型 | 示例 | 验证方法 |
|----------|------|----------|
| 代码仓库地址 | `https://gitee.com/user/repo.git` | API 访问测试 |
| 仓库访问令牌 | Gitee/GitHub Token | API 认证测试 |
| 服务器 IP | `122.51.91.167` | ping 测试 |
| SSH 端口 | `22` | 端口扫描 |
| SSH 用户名 | `root` | 认证测试 |
| SSH 密码/密钥 | 密码或私钥文件 | 认证测试 |
| 本地代码路径 | `C:\Users\user\project` | 文件系统检查 |
| 远程部署路径 | `/root/project` | SSH 执行测试 |

### 2. 验证代码仓库

```python
import requests

# Gitee API 验证
api_url = "https://gitee.com/api/v5/repos/USER/REPO"
headers = {"Authorization": "token YOUR_TOKEN"}

response = requests.get(api_url, headers=headers, timeout=15)

if response.status_code == 200:
    data = response.json()
    print(f"✅ 仓库可访问: {data['name']}")
    print(f"   默认分支: {data['default_branch']}")
    print(f"   私有/公开: {'私有' if data['private'] else '公开'}")
elif response.status_code == 401:
    print("❌ 认证失败 - 令牌无效或已过期")
elif response.status_code == 404:
    print("❌ 仓库不存在或无权访问")
```

### 3. 验证服务器网络

```python
import subprocess

# Ping 测试
result = subprocess.run(
    ["ping", "-c", "2", "-W", "5", "122.51.91.167"],
    capture_output=True, text=True, timeout=15
)

if result.returncode == 0:
    print("✅ 服务器网络可达")
    # 提取延迟信息
    for line in result.stdout.split('\n'):
        if 'rtt' in line or 'avg' in line:
            print(f"   {line.strip()}")
```

### 4. 验证 SSH 端口

```python
import socket

# 端口扫描
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)
result = sock.connect_ex(("122.51.91.167", 22))

if result == 0:
    print("✅ SSH 端口 22 开放")
else:
    print(f"⚠️ SSH 端口未开放 (error code: {result})")
sock.close()
```

### 5. 验证 SSH 认证

#### 方法 A: 使用 sshpass（推荐）

```bash
# 安装 sshpass
apt install sshpass

# 测试连接
sshpass -p "YOUR_PASSWORD" ssh \
  -o StrictHostKeyChecking=no \
  -o ConnectTimeout=10 \
  -p 22 root@122.51.91.167 \
  "echo 'AUTH_SUCCESS' && hostname"
```

#### 方法 B: 使用 paramiko（Python）

```python
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(
        hostname="122.51.91.167",
        port=22,
        username="root",
        password="YOUR_PASSWORD",
        timeout=15
    )
    print("✅ SSH 连接成功")
    
    stdin, stdout, stderr = ssh.exec_command("hostname && uname -a")
    print(stdout.read().decode('utf-8'))
    
    ssh.close()
except paramiko.AuthenticationException:
    print("❌ 认证失败：用户名或密码错误")
except paramiko.SSHException as e:
    print(f"❌ SSH 错误：{e}")
```

#### 方法 C: 使用 SSH 密钥（最安全）

```bash
# 使用私钥连接
ssh -i ~/.ssh/id_rsa \
  -o StrictHostKeyChecking=no \
  -p 22 root@122.51.91.167 \
  "echo 'AUTH_SUCCESS'"
```

### 6. 验证结果汇总

| 项目 | 状态 | 详情 |
|------|------|------|
| Gitee 仓库 | ✅/❌/⚠️ | 可访问/不可访问/部分功能受限 |
| 服务器网络 | ✅/❌ | 可达/不可达（延迟 XXms） |
| SSH 端口 | ✅/❌ | 开放/关闭 |
| SSH 认证 | ✅/❌/⚠️ | 成功/失败/未验证 |

### 7. 安全建议

⚠️ **敏感信息处理**：

1. **不要在对话中明文传递令牌和密码**
2. 将敏感信息存储到 `~/.hermes/.env`（权限 600）：

```bash
# ~/.hermes/.env
GITEE_TOKEN=your_token_here
SERVER_IP=122.51.91.167
SERVER_PORT=22
SERVER_USER=root
SERVER_PASS=your_password_here
```

3. 从 `.env` 文件读取配置，不在对话中显示
4. **立即轮换**在对话中明文传递过的令牌和密码

### 8. 常见故障排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 仓库 401 | 令牌过期/无效 | 重新生成令牌 |
| 仓库 404 | 仓库不存在/私有 | 检查仓库名/权限 |
| ping 失败 | 防火墙阻止 ICMP | 尝试端口扫描 |
| 端口关闭 | SSH 服务未运行 | 检查服务器 SSH 配置 |
| 认证失败 | 用户名/密码错误 | 确认凭据正确性 |
| 连接超时 | 网络问题/防火墙 | 检查网络路由 |

## 注意事项

1. **权限限制**：某些环境可能无法安装 sshpass/paramiko
2. **网络限制**：WSL/容器环境可能有网络隔离
3. **安全优先**：始终推荐使用 SSH 密钥而非密码
4. **令牌轮换**：对话中明文传递的令牌应立即轮换

## 经验总结

- 网络连通性 ≠ SSH 可访问性（防火墙可能阻止特定端口）
- 端口开放 ≠ 认证成功（需要正确凭据）
- 优先使用 SSH 密钥认证，避免密码泄露风险
- 敏感信息应存储到受保护的配置文件，而非对话中传递