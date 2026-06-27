# WSL UNC Access — Session Reference

## Discovery Context

**Session**: Windows Hermes + WSL Ubuntu Hermes merge request
**Problem**: User had two separate Hermes instances (Windows + WSL Ubuntu-24.04) and wanted to merge/transfer skills, plugins, and config.

## The Tool Limitation

- `read_file` tool — **cannot** handle UNC paths (`\\wsl.localhost\Ubuntu-24.04\...`)
  - Returns `File not found` or `用户名或密码不正确` (WinError 1326)
- `search_files` tool — **cannot** access UNC paths
- `terminal` tool — **cannot** run any command when session working directory (`C:\Program Files\Hermes Studio`) doesn't exist in MSYS/bash
  - All commands fail with exit code 126: `/bin/bash: line 2: cd: C:\\Program Files\\Hermes Studio: No such file or directory`
- **`execute_code` tool — WORKS with UNC paths**
  - Python's `os.listdir()`, `os.path.exists()`, and built-in `open()` all work with raw UNC strings like `r"\\wsl.localhost\Ubuntu-24.04\home\jjdeng\.hermes"`

## Concrete Commands That Worked

```python
import os

# Reading WSL directory
unc_path = r"\\wsl.localhost\Ubuntu-24.04\home\jjdeng\.hermes"
items = os.listdir(unc_path)  # Returns full directory listing

# Reading WSL config
with open(os.path.join(unc_path, 'config.yaml'), 'r') as f:
    content = f.read()  # Full file content

# Copying files — use shutil
import shutil
shutil.copytree(
    os.path.join(unc_path, 'skills'),
    r"C:\Users\jjdeng\.hermes\skills",
    dirs_exist_ok=True
)
```

## WSL Distro Name Pitfall

**What user said**: "Ubuntu"
**Actual name**: `Ubuntu-24.04`

The user corrected me. Always run `wsl --list --verbose` or ask the user to check the exact distro name. The UNC path is:
```
\\wsl.localhost\<EXACT-DISTRO-NAME>\home\<username>\.hermes\
```

## What Was Found on Each Instance

### Windows Hermes (this session)
- Model: Claude Opus 4.8 (custom provider `fun-claude`)
- Skills: 10 (mostly WebUI-managed: apikey-image-gen, grok-image-to-video, hyperframes, markdown-viewer, remotion + hermes)
- Plugins: 0
- Profiles: 0
- Personalities: none configured
- Config: ~40 lines, clean minimal setup

### WSL Hermes (Ubuntu-24.04)
- Model: DeepSeek V4 Pro
- Skills: 48 (rich: devops, research, mlops, data-science, github, frontend, content-creation, gaming, etc.)
- Plugins: 1 (hermes-achievements)
- Profiles: 0
- Personalities: 15+ configured (cute characters: catgirl, pirate, shakespeare, surfer, noir, uwu, philosopher, hype, kawaii, etc.)

## Recommended Merge Strategy

1. Copy all WSL skills → Windows (no conflicts — Windows has WebUI skills, WSL has generic ones)
2. Copy `hermes-achievements` plugin
3. Merge WSL `agent.personalities` into Windows config.yaml
4. Keep Windows config.yaml as-is for model/provider settings (already has Opus 4.8)

## Config Security Guard (Hard Constraint)

The agent **cannot** modify `~/.hermes/config.yaml` via `patch` or `write_file` — both are blocked with:
```
Refusing to write to Hermes config file: ...
Agent cannot modify security-sensitive configuration.
Edit ~/.hermes/config.yaml directly or use 'hermes config' instead.
```

**Workaround for config edits**: Use `execute_code` to write a helper file to the user's Desktop, then tell the user to manually paste the relevant section into their config.yaml:
```python
path = r"C:\Users\<username>\Desktop\helper-content.txt"
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
```
Then instruct: "打开 C:\Users\<username>\.hermes\config.yaml，找到 agent: 段落，把以下内容粘贴进去"
