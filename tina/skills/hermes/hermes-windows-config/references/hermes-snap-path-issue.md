# Hermes-Snap Temp Script Path Issue in WSL2

## 问题现象

每次 `terminal()` 调用返回值的末尾都附加以下噪音（无论命令成功与否）：

```
/bin/bash: line 5: C:/Users/jjdeng/.hermes/cache/terminal/hermes-snap-xxx.sh: No such file or directory
/bin/bash: line 6: C:/Users/jjdeng/.hermes/cache/terminal/hermes-cwd-xxx.txt: No such file or directory
```

`exit_code` 始终为 0，正常输出不受影响。**纯外观噪音，不影响功能。**

## 根因

Hermes Desktop（Windows）在执行 `terminal()` 时生成一个临时 bash 脚本来运行用户命令。脚本末尾包含 Hermes 内部后处理行：

```bash
# ≈line 5: source snapshot script
source C:/Users/jjdeng/.hermes/cache/terminal/hermes-snap-xxx.sh
# ≈line 6: read CWD
echo "---CWD---" > C:/Users/jjdeng/.hermes/cache/terminal/hermes-cwd-xxx.txt
```

Hermes 将临时脚本写入 Windows 文件系统路径 `C:\Users\jjdeng\.hermes\cache\terminal\`，但脚本内的 `C:/Users/...` 路径在原生 **WSL2 bash**（非 MSYS2）中无法解析：

| Shell 环境 | `C:/Users/...` 行为 |
|-----------|-------------------|
| MSYS2/git-bash | ✅ 自动翻译为 `/c/Users/...` |
| WSL2 bash | ❌ 当作相对路径查找 `C:` 目录，不存在则报错 |

Hermes 有两个独立的 `.hermes` 家目录：
- **Windows 端**：`C:\Users\jjdeng\.hermes\`（Hermes Desktop 运行处，文件被正确写入）
- **WSL2 端**：`/home/jjdeng/.hermes/`（bash 运行处，看不到 Windows 路径下的临时文件）

## 为什么 `exit_code` 总是 0

Hermes 的 terminal 工具包装器捕获 bash 的最终退出码。后处理行（lines 5-6）的 `source` 失败不会阻止包装器脚本主体成功返回。所以即使 Python 的 `1/0` 错误也显示 `exit_code=0`。

## 修复尝试

### 方案 A（尝试过，遇到 sudo 密码锁死）

在 WSL2 根目录创建 `C:` 符号链接指向 `/mnt/c`：

```bash
sudo ln -s /mnt/c "/C:"
```

这样 `C:/Users/...` 会被解析为 `/C:/Users/...` → `/mnt/c/Users/...`。失败原因：WSL2 未配置 sudo 免密码，命令卡在密码输入，60s 超时。

### 方案 B（未尝试，更彻底）

修改 Hermes 的临时脚本路径生成逻辑，使其在 WSL 环境下输出 `/mnt/c/Users/...` 而非 `C:/Users/...`。需要访问 Hermes 源码。

### 方案 C（未尝试，绕路）

把 WSL2 的 `/home/jjdeng/.hermes` 绑定挂载到 Windows 的 `C:\Users\jjdeng\.hermes`（或反过来），让两个 Hermes 共用同一个家目录。风险：两个实例的状态文件（state.db、锁文件）可能冲突。

## 实际影响评估

| 维度 | 影响 |
|------|------|
| 命令输出 | ✅ 正确，不受影响 |
| exit_code | ⚠️ 总是 0，不能依赖它判断子命令失败 |
| 速度 | ✅ 无影响 |
| 可读性 | ⛔ 输出被噪音污染，群聊/调试时分散注意力 |
| 功能阻塞 | ❌ 无 |

## 当前建议

- 接受这组噪音为 WSL2 + Hermes Desktop 已知限制
- 判断命令是否成功时，检查 `output` 内容而非 `exit_code`（因为 exit_code 总是 0）
- 如果需要干净的 exit_code，用 `execute_code` 的 Python `subprocess.run()` + `check=True`

## 关键时间线

- 首次发现：本 session 中排查 Alex PM "回复有问题"时
- 确认范围：所有 profile（alex-pm、justin-coder、eli-rag、默认 profile）都受影响
- 突破口：对比 `echo 'hello world'`（成功命令、无噪音）和 `echo 'real output' && nonexistent_cmd`（错误命令、有噪音）的原始输出——发现噪音始终存在
- 确切根因：用 `xxd` 确认 `api.py` 未被损坏，转向排查环境问题
