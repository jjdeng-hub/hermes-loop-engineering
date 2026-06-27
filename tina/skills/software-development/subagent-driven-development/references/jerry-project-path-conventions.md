# Jerry's Project Path Conventions

> Environment: Hermes Desktop on Windows 11, terminal runs via WSL2 (bash).
> Default session workdir maps from `C:\Program Files\HermesStudio` which does not exist in WSL — always set workdir explicitly.

## Path Translation Table

| Windows Path | WSL Access Path | Notes |
|-------------|----------------|-------|
| `C:\Users\jjdeng\Desktop\rag-agent` | `/mnt/c/Users/jjdeng/Desktop/rag-agent` | Current demo project |
| `C:\Users\jjdeng\Desktop\myBrain` | `/mnt/c/Users/jjdeng/Desktop/myBrain` | Obsidian vault |
| `C:\Users\jjdeng\Desktop\rag-data` | `/mnt/c/Users/jjdeng/Desktop/rag-data` | Knowledge base data |
| `C:\Users\jjdeng\.hermes` | `/mnt/c/Users/jjdeng/.hermes/` | Hermes config (NOT `/home/jjdeng/.hermes/`) |
| `C:\Users\jjdeng\.hermes-web-ui` | `/mnt/c/Users/jjdeng/.hermes-web-ui/` | Upload directory |

--- wait, this should actually be confirmed...

## Rules for `read_file` tool

The `read_file` tool does NOT support Windows paths like `C:\Users\...` directly.
It expects WSL paths (starting with `/mnt/c/...`).

When reading files from the user's project:
```python
# WRONG — will fail
read_file("C:/Users/jjdeng/Desktop/rag-agent/rag_agent.py")

# CORRECT — use WSL path
read_file("/mnt/c/Users/jjdeng/Desktop/rag-agent/rag_agent.py")
```

## Setting workdir for terminal commands

When using `terminal()` to access user files, always set workdir:
```python
terminal("ls", workdir="/mnt/c/Users/jjdeng/Desktop/rag-agent")
```

Otherwise the default working directory is `C:\Program Files\HermesStudio` which doesn't exist in WSL, producing `No such file or directory` errors.

## Pre-Flight Path Verification Sequence

Before dispatching review subagents for a user project:

```python
from hermes_tools import terminal

# 1. Confirm the path
user_said_path = "C:\\Users\\jjdeng\\Desktop\\rag-agent"

# 2. Translate to WSL for terminal
wsl_path = "/mnt/c/" + user_said_path.replace("\\", "/").split(":/")[1]

# 3. Verify it exists
r = terminal(f"ls {wsl_path}/ | head -20", workdir="/home/jjdeng")
print(r['output'])

# 4. Read key files to confirm content matches
r2 = terminal(f"wc -l {wsl_path}/*.py", workdir="/home/jjdeng")
print(r2['output'])
```
