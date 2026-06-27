---
name: hermes-windows-config
description: Configure Hermes Agent on Windows — models, providers, SOUL/persona, and troubleshoot terminal/path issues in the WSL2/bash environment.
tags: [hermes, windows, configuration, setup, terminal]
triggers:
  - user asks to configure Hermes model, provider, or SOUL on Windows
  - terminal commands fail due to Windows path issues (WSL2 can't cd to C:\...)
  - user needs help with config.yaml on Windows
  - hermes setup or hermes config commands needed
  - terminal executes in WSL when it should run on Windows natively ($HERMES_GIT_BASH_PATH fix)
  - user has WSL Hermes and wants to sync/merge with Windows Hermes
  - cross-instance Hermes migration or file access via UNC paths
---

# Hermes Windows Configuration

## Terminal Path Pitfall (critical)

On Windows with Hermes Desktop, the terminal tool ALWAYS runs commands through **bash** — not cmd.exe, not PowerShell. The `shell: powershell.exe` key in `config.yaml` is **dead config**: the code in `tools/environments/local.py` calls `_find_bash()` which searches for a bash executable and uses it unconditionally.

### Root cause: why terminal runs in WSL

`_find_bash()` on Windows searches in this order:

```
1. $HERMES_GIT_BASH_PATH     ← explicit override, skips everything
2. %LOCALAPPDATA%\hermes\git\bin\bash.exe  ← Hermes-bundled portable Git
3. shutil.which("bash")      ← finds first "bash.exe" on %PATH%
4. C:\Program Files\Git\bin\bash.exe       ← Git for Windows
5. C:\Program Files (x86)\Git\bin\bash.exe
6. RuntimeError: "Git Bash not found"
```

On Windows 11 with WSL installed, `C:\Windows\System32\bash.exe` exists (it's the WSL launcher). Since `System32` is always first on `%PATH%`, `shutil.which("bash")` hits WSL's bash at step 3 **before** Git for Windows at steps 4-5. This is why terminal commands run inside WSL — **not by design, but by accidental PATH resolution.**

### Fix: force Git for Windows bash

Add this to `C:\Users\jjdeng\.hermes\.env`:

```
HERMES_GIT_BASH_PATH=C:\Program Files\Git\bin\bash.exe
```

Then restart Hermes Agent (close Hermes Studio and reopen, or restart the gateway via Settings). This makes `_find_bash()` hit step 1 immediately, skipping `shutil.which()` entirely. The terminal will use Git for Windows' MSYS2 bash — it runs as a native Windows process and does NOT touch WSL.

Verify: after restart, `terminal(command="uname -a")` returns `MSYS_NT-10.0-...` instead of `Linux ... WSL2`.

If Git for Windows is not installed, install from https://git-scm.com/download/win or check for bundled portable Git at `%LOCALAPPDATA%\hermes\git\bin\bash.exe`.

### Consequences of NOT fixing

If left as-is (terminal in WSL):
- WSL was meant for the Tom2 profile; Tom1 shouldn't be there
- Every command produces noise: `No such file or directory` errors from hermes-snap/cwd scripts writing `C:/...` paths inside WSL
- If WSL is ever uninstalled, terminal permanently breaks (no bash found)

### Default working directory

Even after fixing the bash (to Git for Windows), the default working directory is often a Windows path. Always use `workdir="/home/jjdeng"` for terminal commands. Verify with:
```
terminal(command="echo ok", workdir="/home/jjdeng")
```

### Primary Workaround: `execute_code` (Python) as a full replacement

When terminal is broken, `execute_code` is the **reliable fallback** for ALL operations. The Python process in Hermes Desktop inherits a working environment that is not affected by the bash `cd` issue.

**File operations:**
```python
from hermes_tools import execute_code  # already available in execute_code context

# Writing files — use Python open() directly, NOT write_file tool
path = r"C:\Users\username\file.txt"
with open(path, "w", encoding="utf-8") as f:
    f.write(content)

# Reading files — use Python open() directly, NOT read_file tool
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Listing directories — use os.listdir() / os.walk()
import os
items = os.listdir(r"C:\Users\username")
for root, dirs, files in os.walk(r"C:\Users\username"):
    ...
```

**System commands — use subprocess.run() with cmd.exe:**
```python
import subprocess
result = subprocess.run(
    ["cmd.exe", "/c", "echo %USERPROFILE%"],
    capture_output=True, text=True, timeout=10
)
print(result.stdout)
# Works for: mkdir, pip install, python scripts, git clone, etc.
```

**Network requests — use urllib / requests:**
```python
import urllib.request, json
req = urllib.request.Request("https://api.example.com/data",
    headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode())
```

**Pip installs via cmd.exe:**
```python
subprocess.run(
    ["cmd.exe", "/c", r"C:\Users\username\AppData\Local\Programs\Python\Python312\python.exe",
     "-m", "pip", "install", "requests"],
    capture_output=True, text=True, timeout=60
)
```

**When the terminal IS fixable** (not blocked by WSL2 path issue), try these `workdir` values:
- `workdir: "/home/jjdeng"` (WSL2 home — always works, recommended)
- `workdir: "/mnt/c/Users/jjdeng"` (Windows C: via WSL2 mount — works too)

### Dual Path Space Warning

On Windows Hermes Desktop, `execute_code` (Python) and `terminal` (WSL bash, unless `HERMES_GIT_BASH_PATH` is set) resolve `~` differently:
- **Python** → `C:\\Users\\<username>` (Windows native)
- **WSL2 bash** (without `HERMES_GIT_BASH_PATH`) → `/home/<username>` (WSL2 Linux)
- **Git for Windows bash** (with `HERMES_GIT_BASH_PATH` set) → `C:\\Users\\<username>` (MSYS2 translates `/c/Users/...`)

These are different directories. Writing to one does NOT affect the other.

**Rule**: Verify file writes from the same environment that wrote them. Use WSL2 paths for any file that needs to be visible to Hermes at runtime, UNLESS you've fixed the bash via `HERMES_GIT_BASH_PATH` — in which case terminal and execute_code share the same Windows filesystem namespace.

See `references/dual-path-spaces.md` for full details.

## Config File Locations (Windows)

- Primary: `C:\Users\<username>\.hermes\config.yaml`
- Alternative: `%APPDATA%\hermes\config.yaml`
- Profile-specific: `C:\Users\<username>\.hermes\profiles\<profile>\config.yaml`

If the config file doesn't exist yet, the user may need to run initial setup first.

## Setup Commands

1. **Quickest path** (Nous Portal — one OAuth for model + tools):
   ```
   hermes setup --portal
   ```

2. **Manual model configuration**:
   ```
   hermes config set provider <provider-name>
   hermes config set model <model-name>
   ```

3. **Show current config**:
   ```
   hermes config show
   ```

## Common Provider Configurations

In `config.yaml`:
```yaml
provider: openai        # or: anthropic, nous, custom, ollama
model: gpt-4o          # model identifier for chosen provider
api_key: sk-...        # or use environment variable
```

For custom/self-hosted:
```yaml
provider: custom
model: <model-name>
api_base: http://localhost:8080/v1
```

## SOUL / Persona Configuration

"SOUL" refers to Hermes's system prompt / persona layer. It's configured via:
- The `soul` or `system_prompt` field in config.yaml
- Or a dedicated soul file referenced in config

Ask the user what persona/style they want and write it into the appropriate config field.

## WSL Integration (Cross-Instance Hermes)

When the user has Hermes installed on both Windows and WSL and wants to merge/sync, I need dedicated techniques because standard tools have limitations with UNC paths.

### Accessing WSL Files from Windows Hermes

The critical discovery: `read_file` and `search_files` tools **cannot** handle UNC paths (`\\wsl.localhost\<distro>\...`). But **`execute_code` Python environment CAN access UNC paths** via `os.listdir()` and `open()` with raw strings.

**Workflow:**
1. Determine the exact WSL distro name — it may NOT be just `Ubuntu`. Check with `wsl --list --verbose` or ask the user. Common values: `Ubuntu`, `Ubuntu-24.04`, `Ubuntu-22.04`, `Debian`, etc.
2. Construct the UNC path: `r"\\wsl.localhost\<distro>\home\<username>\.hermes"`
3. Use `execute_code` (NOT `read_file`) to read/list/copy files:
   ```python
   import os, shutil
   unc = r"\\wsl.localhost\Ubuntu-24.04\home\jjdeng\.hermes"
   items = os.listdir(unc)  # works!
   with open(os.path.join(unc, 'config.yaml'), 'r') as f:
       content = f.read()
   ```
4. To copy files from WSL to Windows, use `shutil.copy2()` or `shutil.copytree()` with the UNC source and a Windows-local target.

**When terminal blocks you:** The terminal tool fails when the default working directory is a Windows path (WSL2 can't `cd` to `C:\...`). Use `workdir="/home/jjdeng"` or fall back to `execute_code` — it inherits a working Python process that can reach UNC shares regardless of WSL2 directory issues.

### Syncing/Merging Instances

When comparing two Hermes instances (Windows vs WSL):

1. **Read both configs** via `execute_code` — compare model provider, skills config, personalities
2. **List skills dirs** — note which skills exist on one but not the other. WSL often accumulates many more skills (devops, research, mlops, etc.)
3. **Copy assets selectively**:
   - **Skills**: `shutil.copytree(wsl_skills_src, win_skills_dst, dirs_exist_ok=True)` — this merges without overwriting
   - **Plugins**: Copy the plugin directory
   - **Personalities**: Cherry-pick from WSL config.yaml's `agent.personalities` block and merge into Windows config
   - **Config**: Keep Windows config as-is (it likely has the user's preferred model already configured); only merge specific sections

**Never blindly overwrite config.yaml** — always compare and merge specific sections.

### Distro Name Discovery

When the user says they use "Ubuntu" on WSL, the actual distro name visible to Windows may be version-qualified:
- User says "Ubuntu" → real name may be `Ubuntu-24.04`, `Ubuntu-22.04`, `Ubuntu-20.04`
- Correct this early: `wsl --list --verbose` in PowerShell/CMD shows the exact names

**Pitfall**: Guessing the WSL distro name wrong wastes time. Get the exact name from `wsl --list` output up front.

## Hermes Studio Desktop (Electron App)

Hermes Studio 桌面版 (`C:\Program Files\HermesStudio\`) 是 EKKOLearnAI 基于 Electron 打包的桌面应用，**不是** NousResearch 的 CLI 版 `hermes`。两者是独立的：

| | Hermes Studio Desktop | Hermes Agent CLI |
|---|---|---|
| 来源 | EKKOLearnAI (hermes-studio) | NousResearch (hermes-agent) |
| 形式 | Electron 打包，含内置 Web UI | Python CLI + 可选 Dashboard |
| 更新 | app-update.yml → download.ekkolearnai.com | `hermes update` 命令 |
| CLI | `hermes` 不在 WSL2 PATH 中 | `hermes` 命令可用 |
| Web UI | 内嵌 Vue3 前端 (端口由应用管理) | 可选 Dashboard 端口 9119 |

### 更新桌面版

**Tom 无法从 WSL2 更新桌面版。** 桌面版是 Windows 原生应用，更新必须通过应用自身：

1. 菜单栏 → Help → Check for Updates
2. 设置页 → About → 检查更新
3. 启动时自动检查（electron-updater 后台查询 `download.ekkolearnai.com`）

更新配置文件：`C:\Program Files\HermesStudio\resources\app-update.yml`（内容：`provider: generic` + `url: https://download.ekkolearnai.com`）

当前 Web UI 版本可从 `C:\Program Files\HermesStudio\resources\webui\package.json` 的 `version` 字段读取。

### 关键限制

- `hermes update` CLI 命令**不适用于桌面版**
- 桌面版的 hermes CLI 未安装到 WSL2，WSL2 终端中无法调用 `hermes` 命令
- 桌面版 Dashboard（带"一键更新 Hermes"按钮）需要应用内启动，不能从 WSL2 单独启动
- 要排查桌面版问题，检查 `C:\Program Files\HermesStudio\resources\` 下的配置文件和日志
- 详细排查参考：`references/hermes-studio-desktop.md`

## Image / Vision Workaround

When `vision_analyze` tool is unavailable or vision provider is unconfigured, use the direct Claude Messages API via `execute_code`. Full pattern in `references/vision-workaround.md`.

## Hermes-Snap Temp Script Path Issue (WSL Only)

**现象**：每次 `terminal()` 返回值的末尾都出现：
```
/bin/bash: line 5: C:/Users/jjdeng/.hermes/cache/terminal/hermes-snap-xxx.sh: No such file or directory
/bin/bash: line 6: C:/Users/jjdeng/.hermes/cache/terminal/hermes-cwd-xxx.txt: No such file or directory
```

**根因**：Hermes Desktop 生成临时 bash 脚本时将 `C:/Users/...` 路径硬编码进脚本，但 WSL2 bash 无法解析 `C:` 前缀（这需要 MSYS2 翻译，原生 WSL bash 没有）。Hermes 有两个独立的 `.hermes` 家目录——`C:\Users\jjdeng\.hermes\`（Windows，文件被正确写入）和 `/home/jjdeng/.hermes/`（WSL，bash 找不到临时文件）。

**影响**：纯外观噪音。`exit_code` 始终为 0，命令输出不受影响。

**不能依赖 `exit_code` 判断命令成功与否**——因为后处理行失败时包装器脚本主体已返回成功。改为检查 `output` 内容，或用 `execute_code` + Python `subprocess.run(check=True)` 获得真实的退出码。

**修复方法**：设置 `HERMES_GIT_BASH_PATH` 让终端使用 Git for Windows 的 MSYS2 bash 而非 WSL bash。MSYS2 能正确解析 `C:/Users/...` 路径，`hermes-snap` 临时脚本可以正常工作。详见上方 "Terminal Path Pitfall" 节。

详见 `references/hermes-snap-path-issue.md`。

## Diagnostic Steps When Stuck

1. Use `read_file` to check if config.yaml exists and what's in it
2. Try terminal with explicit `workdir` set to user's home directory
3. If terminal runs in WSL (check `uname -a` output), suspect `_find_bash()` is picking WSL's bash.exe. Check `C:\Windows\System32\bash.exe` existence (WSL launcher) vs `C:\Program Files\Git\bin\bash.exe` (Git for Windows). Fix with `HERMES_GIT_BASH_PATH` env var.
4. Check Hermes docs at https://hermes-agent.nousresearch.com/docs (sidebar → Getting Started → Configuration)
5. If docs URL 404s, try searching from the docs homepage — structure may have changed

## Pitfalls

- The docs site URL structure changes; don't hardcode deep links without verification
- On Windows, `hermes` CLI may only be available in PowerShell/cmd, not in the WSL2 bash — if bash can't find `hermes`, suggest the user run config commands in PowerShell directly
- Config file may not exist until first `hermes setup` is run
- WSL distro name in UNC paths is version-qualified (e.g. `Ubuntu-24.04` not `Ubuntu`) — always verify with `wsl --list --verbose`
- `read_file` and `search_files` cannot handle UNC paths; use `execute_code` with Python raw strings instead
- Terminal tool fails when the default working directory is a Windows path that WSL2 can't cd into — always use `workdir="/home/jjdeng"` for terminal commands, or fix the root cause via `HERMES_GIT_BASH_PATH` (see Terminal Path Pitfall section)
- **Do NOT use `/c/Users/...` paths** in terminal — this is MSYS2 convention and doesn't exist in WSL2. Use `/mnt/c/Users/...` for Windows files
- **Config.yaml is off-limits**: `patch` and `write_file` on `.hermes/config.yaml` are blocked by a security guard. Never try to edit it directly — write a helper file to Desktop and guide the user to paste the relevant section manually.
- When merging WSL config.yaml into Windows config.yaml, only `agent.personalities` is safe to recommend merging. Do not overwrite the Windows config's model/provider section.
