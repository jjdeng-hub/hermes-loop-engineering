# Dual Path Spaces on Windows Hermes Desktop

## TL;DR

On Windows Hermes Desktop, `execute_code` (Python) and `terminal` can resolve `~` and file paths **differently** depending on which bash the terminal tool uses.

## The Three Path Namespaces

| Layer | `~` resolves to | Uses |
|-------|----------------|------|
| **Python (execute_code)** | `C:\Users\<username>` | Windows native paths |
| **WSL2 bash** (no `HERMES_GIT_BASH_PATH`) | `/home/<username>` | WSL Linux filesystem |
| **Git for Windows bash** (with `HERMES_GIT_BASH_PATH`) | `C:\Users\<username>` (via MSYS2 `/c/Users/...`) | Windows native, MSYS2-translated |

## Why This Matters

A file written via `execute_code` Python to `~/data.txt` lands at `C:\Users\jjdeng\data.txt`.
A file written via `terminal` (WSL bash) to `~/data.txt` lands at `/home/jjdeng/data.txt`.
These are **different physical files** on different filesystems.

## How to Check Which You're Running

In terminal output, look at the first line:
- `Linux ... WSL2` → WSL bash (no fix applied)
- `MSYS_NT-10.0-...` → Git for Windows bash (with `HERMES_GIT_BASH_PATH`)

Python always uses the Windows namespace regardless.

## When Does This Matter?

- Reading/writing `~/.hermes/` files via terminal vs execute_code
- When `execute_code` writes a file and `terminal` needs to read it (or vice versa)
- When debugging "file not found" errors across tools

## Root Cause

Hermes terminal tool runs bash via `_find_bash()` in `tools/environments/local.py`. On Windows, it searches for `bash.exe` in this order: `$HERMES_GIT_BASH_PATH` → bundled portable Git → `shutil.which("bash")` → Git for Windows. With WSL installed, `shutil.which("bash")` finds WSL's `bash.exe` first (see the main SKILL.md "Terminal Path Pitfall" section for details).
