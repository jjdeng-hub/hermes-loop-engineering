#!/usr/bin/env python3
"""
获取搜狗加密链接的真实 URL
"""

import requests
import sys

def decode_sogou_link(encoded_link: str) -> str:
    """
    解码搜狗微信搜索的加密链接
    
    搜狗的链接格式：
    /link?url=<编码URL>&type=2&query=...&token=...
    
    访问该链接会重定向到真实的微信公众号文章 URL
    """
    if not encoded_link.startswith("http"):
        encoded_link = f"https://weixin.sogou.com{encoded_link}"
    
    try:
        # 访问搜狗链接，跟随重定向
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        
        response = requests.get(
            encoded_link,
            headers=headers,
            timeout=15,
            allow_redirects=True
        )
        
        # 获取最终 URL
        final_url = response.url
        
        # 检查是否是微信公众号文章
        if "mp.weixin.qq.com" in final_url or "weixin.qq.com" in final_url:
            return final_url
        else:
            return f"重定向到：{final_url}"
            
    except Exception as e:
        return f"解码失败：{str(e)}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 decode_sogou_link.py <搜狗链接>")
        print("\n示例：")
        print("  python3 decode_sogou_link.py 'https://weixin.sogou.com/link?url=...'")
        sys.exit(1)
    
    link = sys.argv[1]
    print(f"🔗 原始链接：{link[:80]}...")
    print("\n🔄 正在解码...")
    
    result = decode_sogou_link(link)
    print(f"\n✅ 真实 URL：{result}")
