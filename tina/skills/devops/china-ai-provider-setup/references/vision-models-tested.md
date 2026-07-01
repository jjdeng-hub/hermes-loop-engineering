# 视觉模型测试记录 (2026-07-01)

## 环境
- Hermes Agent, profile: default
- Providers: opencode-go, sn-sensenova (custom), apikey-fun (custom)
- 网络: 中国直接连接（无科学上网）

## 测试方法
发送图片 `Lenna.png` / base64 蓝像素图 到每个候选模型的 `/v1/chat/completions` 端点，要求描述图片内容。

## 结果

| Provider | 模型 | 视觉支持 | 备注 |
|----------|------|---------|------|
| opencode-go | deepseek-v4-flash | ❓公网 API 404，需通过 Hermes 内部路由测试 | 主模型 |
| opencode-go | glm-5.2 | ❓同下 | |
| opencode-go | kimi-k2.7-code | ❓同下 | |
| opencode-go | qwen3.7-max | ❓同下 | |
| sn-sensenova | sensenova-6.7-flash-lite | ❌ 超时 | 纯文本模型 |
| sn-sensenova | nova-vl | ❌ 模型名不存在 | |
| sn-sensenova | sensenova-vl | ❌ 模型名不存在 | |
| sn-sensenova | sensenova-6.7-vl | ❌ 模型名不存在 | |
| sn-sensenova | glm-5v-turbo | ❌ 模型名不存在 | 此模型在 Z.AI 平台不在 sensenova |
| **apikey-fun** | **gpt-5.4** | **✅ 确认可用** | base64 图片识别正确 |

## 结论

- **apikey-fun/gpt-5.4**: 当前已验证可用的视觉模型。通过 `custom:apikey-fun` 配置。
- **opencode-go**: 公网 API 返回 404，但 Hermes 内部有独立路由。需通过 `auto` 模式测试或设置 `model.supports_vision: true` 后验证。
- **sn-sensenova**: 暂无可用视觉模型。现有模型（6.7-flash-lite）为纯文本。
