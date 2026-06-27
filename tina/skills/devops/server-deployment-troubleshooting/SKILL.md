---
name: server-deployment-troubleshooting
description: 远程服务器部署常见问题排查与解决方案
category: devops
trigger: 当部署到远程服务器遇到 SSH、Git、Python 环境等问题时
---

# server-deployment-troubleshooting

## 常见问题与解决方案

### 1. SSH 连接问题

#### Host key verification failed
```bash
# 添加主机密钥到 known_hosts
ssh-keyscan -H <服务器 IP> >> ~/.ssh/known_hosts

# 或者临时跳过验证（不推荐生产环境）
ssh -o StrictHostKeyChecking=no root@<服务器 IP>
```

#### Permission denied (publickey)
```bash
# 检查本地密钥
ls -la ~/.ssh/id_ed25519*

# 复制密钥到服务器
scp ~/.ssh/id_ed25519 root@<服务器 IP>:/root/.ssh/
scp ~/.ssh/id_ed25519.pub root@<服务器 IP>:/root/.ssh/

# 配置权限
ssh root@<服务器 IP> "chmod 600 /root/.ssh/id_ed25519 && cat /root/.ssh/id_ed25519.pub >> /root/.ssh/authorized_keys"

# 配置 SSH config（可选）
cat >> ~/.ssh/config << 'EOF'
Host <服务器 IP>
    HostName <服务器 IP>
    User root
    IdentityFile ~/.ssh/id_ed25519
EOF
```

### 2. Git 问题

#### detected dubious ownership
```bash
git config --global --add safe.directory /root/tool-seeker
```

#### Your local changes would be overwritten
```bash
# 先 stash 本地修改
git stash
git pull origin develop
# 如有需要再恢复
git stash pop
```

#### 服务器 Git SSH 配置
```bash
# 在服务器上配置 Gitee SSH
cat > /root/.ssh/config << 'EOF'
Host gitee.com
    HostName gitee.com
    User git
    IdentityFile /root/.ssh/id_ed25519_gitee
    IdentitiesOnly yes
EOF
chmod 600 /root/.ssh/config
```

### 3. Python 环境问题

#### venv 不存在
```bash
# 检查是否存在
ls -la /root/tool-seeker/backend/.venv/bin/python

# 如不存在，创建虚拟环境
cd /root/tool-seeker/backend
python3 -m venv .venv

# 安装依赖
source .venv/bin/activate
pip install -r requirements.txt
```

#### ModuleNotFoundError
```bash
# 确保使用正确的 Python
cd /root/tool-seeker/backend
source .venv/bin/activate
python -c "import sqlalchemy; print('OK')"

# 如模块缺失
pip install <module-name>
```

### 4. PM2 问题

#### 服务重启
```bash
pm2 restart toolseeker-web toolseeker-api --update-env
pm2 status
pm2 logs toolseeker-api --lines 50
```

#### 服务未启动
```bash
# 检查是否已存在
pm2 list

# 如不存在，启动
pm2 start npm --name toolseeker-web -- start --prefix frontend
pm2 start python --name toolseeker-api -- main.py --prefix backend
```

### 5. 部署流程标准化

```bash
# 完整的部署流程
ssh root@<服务器 IP>

# 1. 拉取代码
cd /root/tool-seeker
git stash && git pull origin develop

# 2. 部署前端
cd frontend
npm install
npm run build

# 3. 部署后端（如有新依赖）
cd ../backend
source .venv/bin/activate
pip install -r requirements.txt

# 4. 初始化数据（如有新脚本）
python init_tutorials.py

# 5. 重启服务
pm2 restart toolseeker-web toolseeker-api --update-env

# 6. 验证
curl -s -o /dev/null -w "%{http_code}" http://localhost/
curl -s -o /dev/null -w "%{http_code}" http://localhost/api/tutorials
pm2 status
```

## 快速诊断命令

```bash
# SSH 连通性
ssh root@<服务器 IP> "echo OK"

# Git 仓库状态
ssh root@<服务器 IP> "cd /root/tool-seeker && git status"

# 前端构建状态
ssh root@<服务器 IP> "ls -la /root/tool-seeker/frontend/.next/"

# 后端 API 状态
ssh root@<服务器 IP> "curl -s http://localhost:8002/api/tools | head -c 200"

# PM2 状态
ssh root@<服务器 IP> "pm2 status"

# 端口占用
ssh root@<服务器 IP> "netstat -tlnp | grep 8002"
```

## 排查顺序

1. **SSH 能连上吗？** → `ssh root@IP "echo OK"`
2. **Git 能拉取吗？** → `cd /root/tool-seeker && git pull`
3. **前端能构建吗？** → `cd frontend && npm run build`
4. **后端能启动吗？** → `cd backend && python main.py`
5. **API 能访问吗？** → `curl http://localhost:8002/api/tools`
6. **PM2 在运行吗？** → `pm2 status`

## 6. Nginx 反向代理问题（2026-05-08 新增）

### 6.1 Nginx 服务未启动

**现象**：网站本地访问正常（localhost:3000 返回 200），但公网 IP 无法访问。

**原因**：
- Nginx 未运行或配置错误
- 云服务器使用 NAT/负载均衡，公网 IP 需要反向代理到内网服务

**排查步骤**：
```bash
# 1. 检查 Nginx 进程
ssh root@<IP> "pgrep -a nginx"

# 2. 检查 Nginx 是否安装
ssh root@<IP> "which nginx; rpm -qa | grep nginx"

# 3. 检查配置文件
ssh root@<IP> "nginx -t"
ssh root@<IP> "cat /etc/nginx/conf.d/*.conf"

# 4. 检查端口监听
ssh root@<IP> "ss -tlnp | grep -E ':80|:3000|:8002'"

# 5. 启动 Nginx（注意：OpenCloudOS/CentOS 可能使用直接命令而非 systemd）
ssh root@<IP> "nginx"  # 直接启动
# 或
ssh root@<IP> "systemctl start nginx"  # 如果使用 systemd

# 6. 验证
curl -s -o /dev/null -w "%{http_code}" http://<公网 IP>/
```

**⚠️ 重要提示**：
- OpenCloudOS 9/CentOS 9 可能未将 Nginx 注册为 systemd 服务
- 使用 `nginx` 命令直接启动，进程会常驻后台
- 重启服务器后需要手动重启 Nginx（或配置开机自启）

### 6.2 Nginx 配置覆盖 Next.js API 路由

**问题**：Nginx 配置将 `/api/*` 全部代理到后端，导致 Next.js 的 API 路由无法生效。

**解决方案**：
```nginx
# ❌ 错误：覆盖所有 /api/*
location /api/ {
    proxy_pass http://127.0.0.1:8002;
}

# ✅ 正确：只对后端 API 代理
location /api/backend/ {
    proxy_pass http://127.0.0.1:8002;
}
# 其他 /api/* 由 Next.js 自身处理
```

### 6.3 服务器文件同步问题

**现象**：本地构建成功，服务器构建失败，提示找不到文件。

**原因**：服务器存在旧的目录结构（如 `frontend/components/`），与新的 `frontend/src/components/` 冲突。

**解决方案**：
```bash
# 1. 检查服务器文件结构
ssh root@<IP> "find /root/tool-seeker/frontend -name 'spotlight.tsx'"

# 2. 清理旧文件
ssh root@<IP> "rm -rf /root/tool-seeker/frontend/components"

# 3. 重新构建
ssh root@<IP> "cd /root/tool-seeker/frontend && npm run build"
```

**预防措施**：
- 部署前清理可能冲突的旧目录
- 使用 `git clean -fdx` 清理未跟踪文件（谨慎使用）
- 保持本地和服务器目录结构一致