#!/usr/bin/env python3
"""
GitHub API Content Downloader
当 git clone / curl 下载 GitHub 内容失败时，使用 GitHub API 获取内容
"""

import sys
import json
import base64
import urllib.request
import urllib.error

def download_file(owner, repo, path, output_file=None, max_time=30):
    """
    通过 GitHub API 下载单个文件
    
    Args:
        owner: 仓库所有者
        repo: 仓库名称
        path: 文件路径
        output_file: 输出文件路径（可选）
        max_time: 超时时间（秒）
    
    Returns:
        文件内容字符串
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        
        with urllib.request.urlopen(req, timeout=max_time) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if 'content' not in data:
                print(f"错误: API 返回格式异常", file=sys.stderr)
                return None
            
            # base64 解码
            content = base64.b64decode(data['content']).decode('utf-8')
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"已保存: {output_file} ({len(content)} 字符)")
            
            return content
            
    except urllib.error.HTTPError as e:
        print(f"HTTP 错误 {e.code}: {e.reason}", file=sys.stderr)
        if e.code == 403:
            print("提示: GitHub API 速率限制，请等待或配置认证", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"URL 错误: {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return None


def list_tree(owner, repo, branch='main', recursive=True):
    """
    获取仓库文件树
    
    Args:
        owner: 仓库所有者
        repo: 仓库名称
        branch: 分支名
        recursive: 是否递归获取所有文件
    
    Returns:
        文件列表
    """
    recursive_param = '?recursive=1' if recursive else ''
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}{recursive_param}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            files = []
            for item in data.get('tree', []):
                files.append({
                    'type': item['type'],
                    'path': item['path'],
                    'sha': item.get('sha')
                })
            
            return files
            
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return None


def main():
    if len(sys.argv) < 4:
        print("用法: python github_download.py <owner> <repo> <path> [output_file]")
        print("示例: python github_download.py jnMetaCode agency-agents-zh README.md")
        sys.exit(1)
    
    owner = sys.argv[1]
    repo = sys.argv[2]
    path = sys.argv[3]
    output_file = sys.argv[4] if len(sys.argv) > 4 else None
    
    content = download_file(owner, repo, path, output_file)
    
    if content and not output_file:
        print(content)


if __name__ == '__main__':
    main()
