# 封面生成工具

## 位置
`<项目>/covers/generate_cover.py`

## 依赖
- Python 3 + PIL/Pillow
- 桌面背景照片：`covers/bg.jpg`（3024×4032，手机直拍桌面）

## 用法
```bash
# 带标签
python generate_cover.py "AI 要有身体了" "#AI" "#具身智能" "#未来已来"

# 不带标签
python generate_cover.py "AI 要有身体了"
```

## 设计要点
- 背景高斯模糊（radius=12）+ 暗色遮罩
- 标题自适应字号（不超出画面 85%），多层阴影
- 标签纯文字居中横排，`#` 前缀，字号 5.5% 画面宽
- 署名 `@Jerry在想什么` 右下角

## 迭代历史
| 版本 | 改动 |
|------|------|
| v1 | HTML + Playwright 截图 |
| v2 | PIL 合成，原图分辨率，CSS 阴影模拟 |
| v3 | 标签胶囊，标题加大到 140px |
| v4 | 背景高斯模糊，标题自适应 |
| v5 | 标签去胶囊改纯文字，字号再加大 +40% |
