# Hermes Studio Desktop 排查参考

## 安装路径

```
C:\Program Files\HermesStudio\
├── Hermes Studio.exe          # 主程序
├── resources/
│   ├── app-update.yml         # 更新配置
│   ├── app.asar               # Electron 打包
│   ├── build/                 # 构建产物
│   └── webui/                 # 内嵌 Vue3 Web UI
│       ├── package.json       # Web UI 版本 (当前 0.6.15)
│       └── dist/              # 编译后的前端
├── chrome_100_percent.pak
├── ffmpeg.dll
└── ...
```

## 版本架构（重要）

Hermes Studio 桌面版有三个独立的版本号，问"版本"时要区分清楚：

| 组件 | 版本号 | 位置 |
|------|--------|------|
| **Hermes Studio 桌面版** | 如 `0.6.15` | `latest.yml` 的 `version` 字段 |
| **内嵌 Hermes Agent 核心** | 如 `0.16.0` | `resources/build/runtime-release.json` 的 `hermesAgentVersion` |
| **内嵌 Web UI** | 如 `0.6.15` | `resources/webui/package.json` 的 `version` |

三个版本号各自独立，不通用。上游 NousResearch/hermes-agent 使用日期版本号（如 `v2026.6.5`），与 Hermes Studio 版本号体系不同。

## 更新配置 (app-update.yml)

路径：`C:\Program Files\HermesStudio\resources\app-update.yml`

```yaml
provider: generic
url: https://download.ekkolearnai.com
updaterCacheDirName: hermes-studio-updater
```

使用 electron-updater 的 generic provider，从 `download.ekkolearnai.com` 拉取更新。

## 检查最新版本

从 WSL2 可以通过 curl 查询下载服务器：

```bash
curl -s https://download.ekkolearnai.com/latest.yml
```

返回结构：
```yaml
version: 0.6.15
files:
  - url: Hermes.Studio-0.6.15-x64.exe
    sha512: ...
    size: 136147548
path: Hermes.Studio-0.6.15-x64.exe
sha512: ...
releaseDate: '2026-06-15T01:48:06.413Z'
```

## 读取运行时版本信息

**Hermes Agent 核心版本：** `resources/build/runtime-release.json`

```json
{
  "tag": "hermes-0.16.0-runtime",
  "hermesAgentVersion": "0.16.0"
}
```

**Web UI 版本：** `resources/webui/package.json`

```json
{
  "name": "hermes-web-ui",
  "version": "0.6.15",
  "repository": "https://github.com/EKKOLearnAI/hermes-studio.git",
  "homepage": "https://hermes-studio.ai"
}
```

**完整读取示例：** 用 terminal 直接 cat 即可（WSL2 路径 `/mnt/c/Program Files/HermesStudio/...`）。无需 Python 或特殊工具。

## 更新方式

桌面版的更新**不能**通过 `hermes update` CLI 命令完成。只能通过：

1. 桌面应用内菜单 → Help → Check for Updates
2. 设置/关于页面 → 检查更新
3. 应用启动时自动检查（electron-updater 后台查询）

## Tom 的能力边界

| 操作 | 能否执行 | 说明 |
|------|---------|------|
| 读取 app-update.yml | ✅ | 通过 `/mnt/c/Program Files/HermesStudio/resources/` |
| 读取 package.json | ✅ | 同上 |
| 触发桌面版更新 | ❌ | 需要桌面应用 UI 操作 |
| 运行 hermes CLI | ❌ | CLI 未安装到 WSL2 |
| 启动 Dashboard (9119) | ❌ | 需要桌面应用内启动 |

## 排查清单

当用户问 Hermes 更新或版本问题时：

1. 确认用户用的是**桌面版**还是 **CLI 版**
2. 桌面版：检查 `C:\Program Files\HermesStudio\resources\app-update.yml` 和 `webui\package.json`
3. CLI 版：运行 `hermes --version` 和 `hermes update`
4. 不要假设 `hermes` 命令在 WSL2 中可用——桌面版的 CLI 不会自动安装到 WSL2
