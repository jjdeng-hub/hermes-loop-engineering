"""封面自动生成脚本 v5 — 背景模糊 + 自适应大字 + 纯文字#标签
用法:
  python generate_cover.py "AI 要有身体了" "#AI" "#具身智能" "#未来已来"
  python generate_cover.py "AI 要有身体了"           # 不传标签 = 无标签
输出: covers/output/<slug>.png — 原图分辨率 PNG
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

COVER_DIR = Path(__file__).parent
BG_PATH = COVER_DIR / "bg.jpg"
OUTPUT_DIR = COVER_DIR / "output"
FONT_DIR = Path("/usr/share/fonts")

BLUR_RADIUS = 12
TITLE_MAX_WIDTH_RATIO = 0.85


def find_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        FONT_DIR / "truetype/noto/NotoSansCJK-Bold.ttc",
        FONT_DIR / "opentype/noto/NotoSansCJK-Bold.ttc",
        FONT_DIR / "truetype/noto/NotoSansSC-Bold.otf",
        FONT_DIR / "truetype/wqy/wqy-zenhei.ttc",
        Path("/mnt/c/Windows/Fonts/msyhbd.ttc"),
        Path("/mnt/c/Windows/Fonts/simhei.ttf"),
    ]
    for p in candidates:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                continue
    return ImageFont.load_default()


def fit_title_font(draw: ImageDraw.Draw, text: str, W: int) -> tuple:
    """二分查找能放进画面的最大字号"""
    max_w = int(W * TITLE_MAX_WIDTH_RATIO)
    lo, hi = 80, int(W * 0.22)
    best = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        font = find_font(mid)
        bbox = draw.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_w:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best, find_font(best)


def generate(title: str, tags: list = None) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)

    img = Image.open(BG_PATH).convert("RGBA")
    W, H = img.size

    # 背景虚化
    blurred = img.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))

    # 暗色遮罩
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(H):
        alpha = int(55 + 20 * (y / H))
        od.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    blurred = Image.alpha_composite(blurred, overlay).convert("RGBA")

    draw = ImageDraw.Draw(blurred)

    # 标题 — 自适应
    title_size, title_font = fit_title_font(draw, title, W)
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (W - tw) // 2
    ty = int(H * 0.32)

    for dx, dy, alpha in [(8, 8, 40), (4, 4, 60), (1, 1, 100)]:
        shadow = (0, 0, 0, alpha)
        for sx in range(-dx, dx + 1, max(1, dx)):
            for sy in range(-dy, dy + 1, max(1, dy)):
                draw.text((tx + sx, ty + sy), title, font=title_font, fill=shadow)
    draw.text((tx, ty), title, font=title_font, fill=(255, 255, 255, 255))

    # 标签 — 纯文字 #前缀
    if tags:
        tag_font_size = max(36, int(W * 0.055))
        tag_font = find_font(tag_font_size)
        gap = int(W * 0.06)
        tag_y = int(H * 0.72)

        tag_texts = [t if t.startswith("#") else f"#{t}" for t in tags]
        total_w = sum(draw.textbbox((0, 0), t, font=tag_font)[2] for t in tag_texts) + gap * (len(tag_texts) - 1)
        x = (W - total_w) // 2
        for t in tag_texts:
            draw.text((x, tag_y), t, font=tag_font, fill=(255, 255, 255, 200))
            x += draw.textbbox((0, 0), t, font=tag_font)[2] + gap

    # 署名
    credit = "@Jerry在想什么"
    credit_size = max(20, int(W * 0.03))
    credit_font = find_font(credit_size)
    cb = draw.textbbox((0, 0), credit, font=credit_font)
    cx = W - (cb[2] - cb[0]) - int(W * 0.07)
    cy = H - int(H * 0.06)
    draw.text((cx, cy), credit, font=credit_font, fill=(255, 255, 255, 150))

    slug = __import__("hashlib").md5(title.encode()).hexdigest()[:8]
    out_path = OUTPUT_DIR / f"{slug}.png"
    blurred = blurred.convert("RGB")
    blurred.save(out_path, "PNG")

    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python generate_cover.py <标题> [#标签1] [#标签2] ...")
        sys.exit(1)
    title = sys.argv[1]
    tags = [a for a in sys.argv[2:] if a.startswith("#")] or None
    path = generate(title, tags)
    print(f"✅ {path}")
