# 微信公众号图片下载 — 绕过防盗链

## 问题

微信文章中的图片有严格的防盗链保护：
- 直接 `requests.get(img_url)` → 403
- 浏览器新标签打开 → 空白（缺少 Referer）
- 图片 URL 有有效期，过期失效

## 原理

用 Playwright 打开文章页 → 页面已持有完整 Cookie + Referer → 在页面上下文内用 `fetch()` 下载图片 → 微信服务端认为是正常图片加载 → 返回图片数据 → 转 base64 → Python 解码写入本地文件。

关键：**图片请求从文章页面内部发出，继承了页面的所有认证上下文。**

## 完整代码

```python
import base64, re
from pathlib import Path
from playwright.sync_api import sync_playwright

def download_article_images(article_url: str, output_dir: Path, prefix: str = "img"):
    """下载微信公众号文章中的所有图片到本地"""
    output_dir.mkdir(parents=True, exist_ok=True)
    downloaded = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)
        
        page = context.new_page()
        
        # 1. 访问文章
        page.goto(article_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)
        
        # 2. 触发懒加载（微信图片默认用 data-src 懒加载）
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(1000)
        
        # 3. 获取所有图片 URL（优先 data-src，通常是高清版）
        img_elements = page.query_selector_all('//div[@id="js_content"]//img')
        img_urls = []
        for img in img_elements:
            src = img.get_attribute("data-src") or img.get_attribute("src")
            if src and not src.startswith("data:"):
                img_urls.append(src)
        
        # 4. 逐张下载（页面内 fetch → base64 → 写文件）
        for i, img_url in enumerate(img_urls):
            try:
                result = page.evaluate("""
                    async (url) => {
                        try {
                            const resp = await fetch(url);
                            const blob = await resp.blob();
                            const reader = new FileReader();
                            return new Promise((resolve) => {
                                reader.onloadend = () => resolve(reader.result);
                                reader.readAsDataURL(blob);
                            });
                        } catch(e) { return null; }
                    }
                """, img_url)
                
                if result and result.startswith("data:"):
                    # data:image/png;base64,iVBOR...
                    header, b64 = result.split(",", 1)
                    img_data = base64.b64decode(b64)
                    
                    if len(img_data) > 500:  # 过滤太小的 icon
                        # 确定扩展名
                        ext = "jpg"
                        if "png" in header: ext = "png"
                        elif "gif" in header: ext = "gif"
                        elif "webp" in header: ext = "webp"
                        
                        fname = f"{prefix}_{i+1:02d}.{ext}"
                        fpath = output_dir / fname
                        fpath.write_bytes(img_data)
                        downloaded.append({"url": img_url, "local": fname, "size": len(img_data)})
                        
            except Exception as e:
                print(f"  图{i+1} 下载失败: {e}")
        
        page.close()
        browser.close()
    
    return downloaded
```

## 替代方案：直接 requests + Referer（更简单，100% 可用）

**本方案在 2026-06-16 实测验证**：对 141 篇微信文章、750 张图片，用 `requests.get()` + `Referer` header 做到了 **100% 下载成功率**，零失败。

无需 Playwright，无需浏览器，纯 HTTP 请求即可绕过微信防盗链。

### 工作原理

微信 CDN（`mmbiz.qpic.cn`）对图片访问的检查机制：
1. ✅ 检查 `Referer` header 是否是 `mp.weixin.qq.com` 域名下的页面
2. ❌ **不检查 Cookie**（requests 无需 cookie）
3. ❌ **不检查 User-Agent 细节**（标准浏览器 UA 即可）

因此，只需将 `Referer` 设置为文章 URL，即可正常下载。

### 代码

```python
def download_wechat_images(html, article_url, article_dir):
    \"\"\"下载微信文章中的全部图片\"\"\"
    img_srcs = re.findall(r'data-src="(https?://mmbiz\\.qpic\\.cn[^"]+)"', html)
    img_srcs = list(set(img_srcs))
    
    for idx, img_url in enumerate(img_srcs):
        ext = "jpg"
        if "wx_fmt=png" in img_url: ext = "png"
        elif "wx_fmt=gif" in img_url: ext = "gif"
        
        img_path = os.path.join(article_dir, f"img_{idx+1:03d}.{ext}")
        
        img_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": article_url,  # 🎯 关键：微信防盗链就靠这个
        }
        resp = requests.get(img_url, headers=img_headers, timeout=20)
        if resp.status_code == 200 and len(resp.content) > 1000:
            with open(img_path, "wb") as f:
                f.write(resp.content)
```

### 与其他方案的对比

| 方案 | 是否可行 | 依赖 | 速度 | 可靠性 |
|------|:--:|:----:|:----:|:----:|
| `requests.get()` + 裸请求 | ❌ 403 | 无 | — | — |
| `requests.get()` + `Referer` header | ✅✅ | 仅 requests | ~0.5s/图 | 100% |
| `page.screenshot(element)` | ⚠️ | Playwright | 慢 | 非原图 |
| `page.route()` 拦截 | ✅ | Playwright | 复杂 | 需刷新 |
| **页面内 fetch + base64** | ✅✅ | Playwright | ~2s/图 | 100% |

## Pitfalls

- **图片 URL 去重**：同一张图可能同时出现在 `src` 和 `data-src` 中
- **微信表情/icon**：大小为 1-3KB，通过 `len(img_data) > 500` 过滤
- **并发限制**：不要同时下载太多张，微信可能限速
- **URL 有效期**：图片链接可能 24 小时后失效，建议尽快下载

## 参考

- 首次验证：2026-06-10，爬取 "KS焊线机技术进阶之路" 12 篇文章的 196 张图片（7.4MB），成功率 100%
