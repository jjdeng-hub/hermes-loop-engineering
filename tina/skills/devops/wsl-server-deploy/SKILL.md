---
name: wsl-server-deploy
description: WSL 环境下服务器部署指南 - 解决 SSH 认证、网络限制等常见问题
category: devops
version: 1.0
created: 2026-05-06
---

# WSL 服务器部署技能

## 概述

在 WSL (Windows Subsystem for Linux) 环境下部署代码到远程服务器时，常遇到 SSH 认证、网络限制等问题。本技能提供经过验证的解决方案。

## 核心问题与解决方案

### 1. SSH 认证问题

**症状：**
```
Permission denied (publickey,gssapi-keyex,gssapi-with-mic,password)
```

**原因分析：**
| 认证方式 | WSL 支持 | 常见问题 |
|---------|---------|---------|
| 密码认证 | ⚠️ 有限 | 需要 sshpass，WSL 默认无权限安装 |
| SSH 密钥 | ✅ 支持 | 需要服务器配置公钥 |
| GSSAPI | ❌ 不支持 | 企业环境专用 |

**解决方案：**

#### 方案 A：SSH 密钥认证（推荐）

```bash
# 1. 查看 WSL SSH 公钥
cat ~/.ssh/id_ed25519.pub
# 或
cat ~/.ssh/id_rsa.pub

# 2. 通过云控制台 VNC 登录服务器，添加公钥
echo "ssh-ed25519 AAAA... 你的公钥" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# 3. 测试连接
ssh -o StrictHostKeyChecking=no root@服务器IP
```

#### 方案 B：临时启用密码认证

```bash
# 通过云控制台 VNC 登录服务器
vi /etc/ssh/sshd_config

# 修改或添加
PasswordAuthentication yes
PermitRootLogin yes

# 重启 SSH
systemctl restart sshd
```

#### 方案 C：云厂商云助手（无需 SSH）

- **腾讯云轻量**：控制台 → 云助手 → 创建命令
- **阿里云轻量**：控制台 → 云助手 → 创建命令
- **华为云**：控制台 → 云助手 → 远程命令

### 2. 网络限制问题

**症状：**
- git clone 超时
- npm install 超时
- pip install 超时

**解决方案：**

```bash
# npm 使用淘宝镜像
npm config set registry https://registry.npmmirror.com

# pip 使用清华镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple

# git 增加超时时间
git config --global http.lowSpeedLimit 0
git config --global http.postBuffer 524288000
```

### 3. WSL 权限问题

**症状：**
- apt install 权限被拒绝
- 无法安装系统级工具

**解决方案：**

```bash
# WSL 中无法使用 apt 安装系统工具
# 替代方案：使用用户级工具

# npm 全局安装（无需 sudo）
npm install -g pm2

# uv 安装 Python 包（推荐）
uv pip install --user paramiko

# 或使用 conda/mamba
conda install paramiko
```

## 部署流程检查清单

### 部署前检查

```bash
# 1. 确认 SSH 认证方式
ssh -v root@服务器IP 2>&1 | grep "Authentications"

# 2. 测试网络连通性
ping -c 2 服务器IP
nc -z -w 5 服务器IP 22

# 3. 确认本地代码已 push
git log origin/develop..HEAD  # 应为空
```

### 标准部署命令

```bash
# 1. SSH 连接
ssh root@服务器IP

# 2. 拉取代码
cd /root/项目名
git pull origin develop

# 3. 前端构建
cd frontend
npm install
npm run build

# 4. PM2 启动
pm2 stop my-web 2>/dev/null || true
pm2 delete my-web 2>/dev/null || true
pm2 start npm --name my-web -- start
pm2 save

# 5. 验证
pm2 status
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
nginx -t && systemctl restart nginx
```

### 故障排查

| 问题 | 检查命令 | 解决方案 |
|------|---------|---------|
| npm install 失败 | `npm cache clean --force` | 删除 node_modules 重装 |
| 构建报错 | `node --version` | Node.js 需 ≥ 20 |
| PM2 启动失败 | `pm2 logs my-web` | 查看错误日志 |
| Nginx 502 | `systemctl status nginx` | 检查 upstream 配置 |
| 外部无法访问 | 云控制台检查安全组 | 开放 80/443 端口 |

## 安全建议

1. **优先使用 SSH 密钥认证**，禁用密码登录
2. **定期轮换 SSH 密钥**
3. **使用 fail2ban 防暴力破解**：`apt install fail2ban`
4. **只开放必要端口**：22, 80, 443
5. **敏感信息使用环境变量**，不要硬编码在代码中

## 工具推荐

| 工具 | 用途 | WSL 安装方式 |
|------|------|-------------|
| sshpass | 密码认证 | ❌ 无法安装（需 sudo） |
| paramiko | Python SSH | `uv pip install paramiko` |
| expect | 交互式自动化 | ❌ 无法安装（需 sudo） |
| uv | Python 包管理 | ✅ 推荐 |
| nvm | Node 版本管理 | ✅ 推荐 |

## 经验教训

1. **部署前先确认 SSH 认证方式**，不要假设密码可用
2. **WSL 中避免依赖 sudo 的工具**，选择用户级替代方案
3. **云控制台 VNC 是最后的救命稻草**，确保知道如何使用
4. **本地测试构建成功后再部署**，避免服务器构建失败
5. **保留回滚方案**，部署前备份当前版本
6. **Windows 文件系统权限问题** — NTFS 与 Linux 权限模型不同，可能导致 SSH 私钥被拒绝

---

## Windows SSH 权限问题（重要！）

### 问题症状

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0777 for '/mnt/c/Users/.../id_ed25519' are too open.
Load key "/mnt/c/.../id_ed25519": bad permissions
Permission denied (publickey)
```

### 根本原因

Windows NTFS 文件系统权限模型与 Linux 不同：
- Windows 上私钥文件权限通常显示为 `0777`（所有人可读写）
- SSH 要求私钥权限必须是 `0600`（只有所有者可读写）
- SSH 检测到权限不安全，直接拒绝使用该密钥

### 解决方案 A：修复 Windows 文件权限（推荐）

**在 Windows PowerShell（管理员）中执行：**

```powershell
# 1. 移除所有继承权限，只给当前用户读取权限
icacls "C:\Users\用户名\.ssh\id_ed25519" /inheritance:r /grant:r "$($env:USERNAME):(R)"

# 2. 验证权限
icacls "C:\Users\用户名\.ssh\id_ed25519"
# 应该只显示你的用户名有权限

# 3. 测试连接
ssh -i "C:\Users\用户名\.ssh\id_ed25519" root@服务器IP "echo OK"
```

### 解决方案 B：复制密钥到 WSL 本地（备选）

如果方案 A 不起作用，将密钥复制到 WSL 本地文件系统：

```bash
# 1. 复制密钥到 WSL 本地
cp /mnt/c/Users/用户名/.ssh/id_ed25519 ~/.ssh/
cp /mnt/c/Users/用户名/.ssh/id_ed25519.pub ~/.ssh/

# 2. 设置正确权限
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub

# 3. 更新 SSH Config 使用本地路径
cat > ~/.ssh/config << 'EOF'
Host 服务器别名
  HostName 服务器IP
  User root
  IdentityFile ~/.ssh/id_ed25519
EOF
chmod 600 ~/.ssh/config

# 4. 测试连接
ssh 服务器别名 "echo OK"
```

### Windows SSH Config 配置

编辑 `C:\Users\用户名\.ssh\config`：

```
Host 服务器别名
  HostName 122.51.91.167
  User root
  IdentityFile C:/Users/用户名/.ssh/id_ed25519
  ServerAliveInterval 60
  ServerAliveCountMax 3
  IdentitiesOnly yes
```

**注意**：Windows SSH Config 中使用正斜杠 `/`

### 一键修复脚本（管理员 PowerShell）

```powershell
# 修复 SSH 密钥权限并测试连接
$KEY_PATH = "C:\Users\$env:USERNAME\.ssh\id_ed25519_trae"

# 修复权限
icacls $KEY_PATH /inheritance:r /grant:r "$($env:USERNAME):(R)"

# 启动 SSH Agent
Start-Service ssh-agent

# 添加密钥
ssh-add $KEY_PATH

# 测试连接
ssh -i $KEY_PATH root@122.51.91.167 "echo '连接成功!'"
```

### 验证步骤

```powershell
# 检查密钥权限
icacls "C:\Users\用户名\.ssh\id_ed25519"

# 检查 SSH Agent 中的密钥
ssh-add -l

# 详细调试连接
ssh -v -i "C:\Users\用户名\.ssh\id_ed25519" root@服务器IP "echo OK"
```

### 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `Permissions too open` | 文件权限 0777 | 用 icacls 修复权限 |
| `Could not open SSH key` | 路径错误或格式问题 | 确认路径，检查密钥格式 |
| `Connection timed out` | 防火墙/网络问题 | `Test-NetConnection IP -Port 22` |
| 密钥不在 Agent 中 | SSH Agent 未启动 | `Start-Service ssh-agent` |

---

## 相关技能

- `project-deploy-guide` - 通用项目部署指南
- `github-content-download` - GitHub 内容下载（处理网络限制）

## 宝塔面板服务器部署（补充）

### 适用场景
- Next.js + FastAPI 项目
- 宝塔面板 (Baota Panel) 服务器
- 使用 PM2 管理 Node.js 进程

### 关键发现

#### 1. 端口冲突问题
**症状**: PM2 启动失败，错误 `errno: -98, Address already in use`

**原因**: 旧进程未完全清理，端口 3000 仍被占用

**解决方案**:
```bash
# 完全清理旧进程
pm2 stop all
pm2 delete all
pm2 save

# 确认端口释放
ss -tlnp | grep 3000 || echo "PORT_FREE"

# 重新启动
cd /root/tool-seeker/frontend
pm2 start npm --name toolseeker-web -- start
```

#### 2. 宝塔 Nginx 路径
**发现**: 宝塔面板的 Nginx 二进制在 `/usr/sbin/nginx`，而非 `/www/server/nginx/sbin/nginx`

**验证**:
```bash
which nginx
# 输出: /usr/sbin/nginx

# 测试配置
/usr/sbin/nginx -t

# 重启
/usr/sbin/nginx -s reload
```

#### 3. 手动创建 Nginx 配置
宝塔面板可能没有自动创建站点配置，需要手动创建：

```bash
cat > /etc/nginx/conf.d/toolseeker.conf << 'EOF'
server {
    listen 80;
    server_name your-domain.com www.your-domain.com your-ip;
    
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:8002/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF

/usr/sbin/nginx -t && /usr/sbin/nginx -s reload
```

#### 4. 宝塔面板工具脚本问题
**症状**: `/www/server/panel/tools.py` 报错 `ModuleNotFoundError: No module named 'psutil'`

**原因**: 宝塔面板 Python 环境缺少依赖

**解决方案**: 直接使用系统 Nginx，绕过宝塔面板工具

### 部署检查清单

```bash
# 1. SSH 连接测试
ssh -o StrictHostKeyChecking=no root@服务器IP "echo OK"

# 2. 代码拉取
cd /root/tool-seeker && git pull origin develop

# 3. 前端构建
cd frontend && npm install && npm run build

# 4. 清理旧进程
pm2 stop all && pm2 delete all

# 5. 启动服务
cd /root/tool-seeker/frontend
pm2 start npm --name toolseeker-web -- start
cd ../api && pm2 start "python3 main.py" --name toolseeker-api
pm2 save

# 6. 配置 Nginx
# 创建 /etc/nginx/conf.d/toolseeker.conf
/usr/sbin/nginx -t && /usr/sbin/nginx -s reload

# 7. 验证
pm2 status
ss -tlnp | grep -E ":(80|3000|8002)"
curl -s -o /dev/null -w "HTTP: %{http_code}\n" http://服务器IP
```

### 端口规划

| 服务 | 端口 | 监听地址 | 说明 |
|------|------|----------|------|
| Nginx | 80/8080 | 0.0.0.0 | 对外服务 |
| Next.js | 3000 | 127.0.0.1 | 前端（内网） |
| FastAPI | 8002 | 127.0.0.1 | 后端 API（内网） |

## 相关技能

- `project-deploy-guide` - 通用项目部署指南
- `github-content-download` - GitHub 内容下载（处理网络限制）