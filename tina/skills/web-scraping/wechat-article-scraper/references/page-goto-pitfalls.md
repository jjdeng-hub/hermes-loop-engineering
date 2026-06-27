# page.goto() 反模式与正确用法

## 反模式：`wait_until="networkidle"`

```python
# ❌ 国内站点（搜狗、微信等）会无限挂起
page.goto(url, wait_until="networkidle", timeout=30000)
```

**原因**：`networkidle` 等待页面 500ms 内无任何网络请求。中国网站加载大量第三方 trackers/广告脚本（部分被墙超时），永远达不到 idle 状态。

## 正确用法

```python
# ✅ 通用：domcontentloaded + 固定等待
page.goto(url, wait_until="domcontentloaded", timeout=20000)
page.wait_for_timeout(3000)

# ✅ 需要特定元素时：wait_for_selector
page.goto(url, wait_until="domcontentloaded", timeout=20000)
page.wait_for_selector('//div[@id="js_content"]', timeout=10000)
```

## 适用场景判断

| `wait_until` 值 | 适用 | 不适用 |
|---|---|---|
| `domcontentloaded` | 搜狗、微信公众号、百度等中文站 | 重度 SPA（React 动态渲染） |
| `networkidle` | 纯静态站、Google 搜索结果 | **任何中国网站** |
| `load` | 一般网站 | 图片懒加载页面 |

## WSL Chromium 启动参数

```python
# WSL 环境下必须加 --no-sandbox
browser = p.chromium.launch(
    headless=True,
    args=["--no-sandbox"]
)
```
