---
name: china-ai-provider-setup
description: 在中国网络环境下为 Hermes 配置 AI 模型提供商 — 连接性测试、提供商选择、视觉/辅助模型配置。国内直连可用 vs 被墙提供商的对照指南。
triggers:
  - "配个视觉模型"
  - "看图功能用不了"
  - "多模态模型国内哪个能用"
  - "换个能直连的 API"
  - "Gemini 连不上"
  - "vision_analyze 失败"
allowed-tools: Bash(curl:*), Read, Write, Edit
---

# 中国网络环境 AI 提供商配置

> 核心原则：**先测连接，再配配置**。国内网络环境下，Google/OpenAI 等西方 API 大概率不通，但国内大厂（智谱、阿里、百度）的兼容 API 直连可用且延迟更低。

---

## 1. 连接性测试

在改任何配置之前，先对候选提供商做连通性测试：

```bash
# 智谱 GLM-4V（推荐首选）
curl -s -o /dev/null -w "%{http_code} %{time_total}s" --connect-timeout 5 \
  https://open.bigmodel.cn/api/paas/v4/chat/completions

# 阿里百炼（通义千问 VL）
curl -s -o /dev/null -w "%{http_code} %{time_total}s" --connect-timeout 5 \
  https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions

# Google Gemini（大概率超时）
curl -s -o /dev/null -w "%{http_code} %{time_total}s" --connect-timeout 5 \
  https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=test
```

**判断标准**：
- `HTTP 400/401` + 低延迟 → ✅ 通了（只是缺少认证参数）
- `000` + 5s 超时 → ❌ 被墙，换下一个
- `000` + 快速返回 → ❌ DNS/路由问题

---

## 2. 国内可用模型速查

| 提供商 | API 地址 | 视觉模型 | 延迟 | 免费额度 |
|--------|----------|---------|------|---------|
| **智谱** | `open.bigmodel.cn/api/paas/v4` | `glm-4v` | ~160ms | ✅ 新用户送 |
| 阿里百炼 | `dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-vl-plus` | ~120ms | ✅ 新用户送 |
| 百度文心 | `aip.baidubce.com` | `ernie-4.0-turbo` | ~200ms | ✅ 有 |
| **OpenCode Go** | 聚合代理，内部路由⁺ | `deepseek-v4-flash`, `glm-5.2`, `kimi-k2.7-code`, `qwen3.7-max` | ~150ms | ✅ Go套餐 $5-10/月含13模型 |
| **apikey.fun** | `api.apikey.fun/v1` | `gpt-5.4` (支持视觉) | ~200ms | ✅ 付费按量 |
| **DeepSeek** | `api.deepseek.com` | — | ✅ | ❌ 不支持多模态 |
| **Google Gemini** | `generativelanguage.googleapis.com` | `gemini-2.0-flash` | ❌ | 被墙 |

⁺ OpenCode Go 是一个国内可用的模型聚合代理，通过环境变量 `OPENCODE_GO_API_KEY` 配置。它将多个国产模型（DeepSeek、GLM、Kimi、Qwen 等）暴露为统一 OpenAI 兼容 API。Hermes 内置支持（built-in provider），无需在 custom_providers 中注册。

> **推荐首选智谱 GLM-4V**：OpenAI 兼容格式，Hermes 配置改动最少，API Key 一个就够。

---

## 3. 注册与获取 Key

1. 打开 https://open.bigmodel.cn → 注册/登录
2. 控制台 → API Keys → 创建新 Key
3. 复制 Key（只显示一次）

---

## 4. 配置 Hermes

需要改两处：`custom_providers` 注册提供商，`auxiliary.vision` 指定使用它。

### 4.1 注册智谱为自定义提供商

在 `config.yaml` 的 `custom_providers` 列表末尾添加：

```yaml
- name: zhipu-vision
  base_url: https://open.bigmodel.cn/api/paas/v4
  api_key: <你的Key>
  model: glm-4v
```

### 4.2 指定视觉引擎

修改 `auxiliary.vision` 块：

```yaml
auxiliary:
  vision:
    provider: custom:zhipu-vision
    model: glm-4v
    base_url: https://open.bigmodel.cn/api/paas/v4
    api_key: <你的Key>
    timeout: 120
    extra_body: {}
    download_timeout: 30
```

### 4.3 文本模型不变

`model.default` 保持原样（如 DeepSeek V4）。视觉和文本是两个独立通道，互不影响。

---

## 5. 验证

配置后重启 Hermes，发任意图片测试：

```
「看看这张图」+ 发送图片
```

或直接调用 vision_analyze：

```bash
vision_analyze(image_url="https://picsum.photos/400/300", question="描述这张图")
```

成功返回图片描述 = 配置完成。

---

## 6. Fallback 链设计（模型架构优化）

除了设置单个主模型，还可以通过 `fallback_providers` 配置一整个模型兜底链。Hermes 在主模型不可用时自动按序尝试。

### 6.1 设计原则

- **Provider 多样性 > 模型多样性** — 同一个 provider 挂了，再强的模型也调不通
- **去重** — 同一个 `provider/model` 在链中出现多次等于浪费槽位
- **Premium 兜底** — 把最贵的模型放最后，日常用便宜模型

### 6.2 推荐模式 (3+3+1)

```
主模型:   provider-A/flash-model         ← 日常主力，便宜+快
FB 1~3:   provider-A (其他模型)           ← 同 provider，模型多样性
FB 4~6:   provider-B/C (同模型/不同模型)   ← 不同 provider，provider 容灾
FB 7:     provider-D/premium-model       ← Premium 最终兜底
```

### 6.3 实际操作

通过 Python YAML 直接编辑（`hermes config set` 传 JSON 数组会被存为字符串，导致故障）：

```bash
# ❌ 不工作 — JSON 数组被存为字符串
hermes config set fallback_providers '["m1", "m2", "m3"]'

# ✅ 正确 — 直接写 config.yaml
python3 -c "
import yaml
c = yaml.safe_load(open('/root/.hermes/config.yaml'))
c['fallback_providers'] = ['m1', 'm2', 'm3']
yaml.dump(c, open('/root/.hermes/config.yaml', 'w'), default_flow_style=False, sort_keys=False)
"
```

### 6.4 验证

```bash
python3 -c "
import yaml
c = yaml.safe_load(open('/root/.hermes/config.yaml'))
print('主:', c['model']['default'])
for i, p in enumerate(c.get('fallback_providers', []), 1):
    print(f'  FB{i}: {p}')
"
```

---

## 7. 视觉模型备选方案

如果推荐的智谱 GLM-4V 不可用，以下替代方案已验证可用：

### 7.1 apikey.fun / gpt-5.4（通用型）

通过 `apikey.fun` 代理调用 GPT-5.4 的视觉能力，无需科学上网：

```yaml
auxiliary:
  vision:
    provider: custom:apikey-fun
    model: gpt-5.4
```

无需额外配置 base_url 和 api_key（已在 custom_providers 中定义）。

### 7.2 已知不工作的模型

| 模型 | 原因 |
|------|------|
| `sensenova-6.7-flash-lite` | 纯文本模型，不支持图片输入 |
| `sensenova/vl`, `sensenova-vl` | 模型名不存在 |

验证新模型的方法见 `references/vision-models-tested.md`。

---

## 8. 故障排除

| 症状 | 原因 | 解决 |
|------|------|------|
| vision_analyze 返回错误 | `auto` 落到纯文本模型 | 显式指定 `custom:zhipu-vision` 或 `custom:apikey-fun` 加 `model: gpt-5.4` |
| 401 Unauthorized | Key 错误或过期 | 去智谱控制台重新生成 |
| 000 超时 | 被墙 | 换国内提供商 |
| 文本模型变了 | 误改了 `model.default` | 只改 `auxiliary.vision`，不动顶层 model |
| fallback_providers 不生效 | `hermes config set` 把 JSON 数组存成了字符串 | 用 Python YAML 直接写配置文件（见第 6.3 节） |

---

## 9. 扩展到其他辅助能力

同理可配其他 auxiliary 能力（web_extract、compression 等），只需把 `auxiliary.<能力>.provider` 改为 `custom:zhipu-vision`，或创建新的 custom_providers 条目指向不同模型。

---

## 10. 本地模型部署（Ollama）

国内安装 Ollama 和导入本地模型：见 [references/ollama-china-install.md](references/ollama-china-install.md)
