#!/usr/bin/env python3
"""
WCAG 2.1 对比度分析工具

计算颜色对比度并评估是否符合 WCAG AA/AAA 标准。
用于网站设计审查时验证 CSS 变量颜色值。

用法:
    python wcag_contrast.py
"""

def relative_luminance(r: int, g: int, b: int) -> float:
    """
    计算颜色的相对亮度 (WCAG 2.1 公式)
    
    Args:
        r, g, b: 0-255 的 RGB 值
    
    Returns:
        相对亮度值 (0.0 - 1.0)
    """
    def adjust(c: int) -> float:
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)


def contrast_ratio(hex1: str, hex2: str) -> float:
    """
    计算两个颜色的对比度
    
    Args:
        hex1, hex2: 十六进制颜色值 (如 "#3B82F6")
    
    Returns:
        对比度比值 (1:1 - 21:1)
    """
    def hex_to_rgb(h: str) -> tuple[int, int, int]:
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    l1 = relative_luminance(*hex_to_rgb(hex1))
    l2 = relative_luminance(*hex_to_rgb(hex2))
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


def wcag_rating(ratio: float) -> str:
    """
    WCAG 评级
    
    Args:
        ratio: 对比度比值
    
    Returns:
        评级字符串
    """
    if ratio >= 7:
        return "AAA ✅"
    elif ratio >= 4.5:
        return "AA ✅"
    elif ratio >= 3:
        return "AA Large ⚠️"
    else:
        return "Fail ❌"


def find_compliant_color(base_hex: str, target_ratio: float = 4.5, 
                         bg: str = "#FFFFFF") -> tuple[str, float]:
    """
    找到符合目标对比度的颜色（通过调整亮度）
    
    Args:
        base_hex: 原始颜色
        target_ratio: 目标对比度
        bg: 背景色
    
    Returns:
        (符合标准的颜色, 实际对比度)
    """
    def hex_to_rgb(h: str) -> list[int]:
        h = h.lstrip('#')
        return [int(h[i:i+2], 16) for i in (0, 2, 4)]
    
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        return f"#{r:02x}{g:02x}{b:02x}"
    
    r, g, b = hex_to_rgb(base_hex)
    
    # 尝试变暗（增加对比度）
    for i in range(100):
        factor = 1 - (i * 0.01)
        new_r = min(255, max(0, int(r * factor)))
        new_g = min(255, max(0, int(g * factor)))
        new_b = min(255, max(0, int(b * factor)))
        
        ratio = contrast_ratio(rgb_to_hex(new_r, new_g, new_b), bg)
        if ratio >= target_ratio:
            return rgb_to_hex(new_r, new_g, new_b), ratio
    
    return base_hex, contrast_ratio(base_hex, bg)


def analyze_colors(colors: dict[str, str], bg: str = "#FFFFFF") -> None:
    """
    分析一组颜色的对比度
    
    Args:
        colors: {颜色名: 十六进制值}
        bg: 背景色
    """
    print(f"\n=== 对比度分析 (背景: {bg}) ===\n")
    print(f"{'颜色名':<20} {'值':<12} {'对比度':<12} {'评级'}")
    print("-" * 60)
    
    for name, hex_val in colors.items():
        ratio = contrast_ratio(hex_val, bg)
        rating = wcag_rating(ratio)
        print(f"{name:<20} {hex_val:<12} {ratio:.2f}:1      {rating}")


def main():
    """主函数：分析 ToolSeeker 设计系统的颜色"""
    
    # 亮色主题颜色
    light_colors = {
        "--heading": "#111827",
        "--body": "#374151",
        "--muted": "#6B7280",
        "--blue": "#3B82F6",
        "--accent-purple": "#8B5CF6",
        "--accent-cyan": "#06B6D4",
        "--accent-orange": "#F97316",
        "--accent-green": "#10B981",
        "--accent-red": "#EF4444",
    }
    
    # 暗色主题颜色
    dark_colors = {
        "--heading": "#F1F5F9",
        "--body": "#CBD5E1",
        "--muted": "#94A3B8",
        "--blue": "#60A5FA",
        "--accent-purple": "#A78BFA",
        "--accent-cyan": "#22D3EE",
        "--accent-orange": "#FB923C",
        "--accent-green": "#34D399",
        "--accent-red": "#F87171",
    }
    
    # 分析亮色主题
    analyze_colors(light_colors, "#FFFFFF")
    
    # 分析暗色主题
    analyze_colors(dark_colors, "#1E293B")
    
    # 检查需要修复的颜色
    print("\n=== 修复建议 ===\n")
    
    problematic = [
        ("--accent-green", "#10B981"),  # 2.54:1 ❌
        ("--blue", "#3B82F6"),           # 3.68:1 ⚠️
        ("--accent-purple", "#8B5CF6"),  # 4.23:1 ⚠️
        ("--accent-red", "#EF4444"),     # 3.76:1 ⚠️
    ]
    
    for name, original in problematic:
        fixed, ratio = find_compliant_color(original, 4.5)
        original_ratio = contrast_ratio(original, "#FFFFFF")
        print(f"{name}:")
        print(f"  原值: {original} → {original_ratio:.2f}:1 → {wcag_rating(original_ratio)}")
        print(f"  建议: {fixed} → {ratio:.2f}:1 → {wcag_rating(ratio)}\n")


if __name__ == "__main__":
    main()
