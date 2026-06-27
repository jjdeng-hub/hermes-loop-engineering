# 封面生成系统 v5

基于桌面实拍照片 + PIL 合成标题的封面生成方案。

## 设计参数（2026-05-25 确定）

| 参数 | 值 |
|------|-----|
| 背景 | `bg.jpg`（桌面实拍，3024×4032） |
| 字体 | **微软雅黑 Bold**（msyhbd.ttc） |
| 模糊度 | **blur=15** |
| 标题宽度比 | **0.92**（填满画面 92%） |
| 标题位置 | 画面 32% 高度处，水平居中 |
| 标签 | **不放标签，纯标题** |
| 署名 | @Jerry在想什么（右下角，150 透明度） |

## 脚本位置

```
/mnt/c/Users/jjdeng/Desktop/xiaohongshu-content/covers/generate_cover.py
```

## 用法

```bash
python generate_cover.py "标题文本"
```

不带标签参数即为纯标题封面。

## 输出

`output/<md5hash>.png`
