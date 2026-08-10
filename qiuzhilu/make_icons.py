# -*- coding: utf-8 -*-
"""生成面试进度记录本 App 图标（渐变圆角方块 + 对话气泡 + 对勾）"""
from PIL import Image, ImageDraw

OUT = r"C:\Users\liuyalu\WorkBuddy\2026-08-10-16-28-55\interview-tracker\icons"

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def rounded_gradient(size, radius, c1, c2):
    """斜向渐变 + 圆角透明蒙版"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for y in range(size):
        t = y / (size - 1)
        d.line([(0, y), (size, y)], fill=lerp(c1, c2, t))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    img.putalpha(mask)
    return img

def draw_bubble_icon(base, size, content_scale=1.0):
    """在渐变背景上画白色对话气泡 + 对勾，content_scale 用于 maskable 安全区"""
    d = ImageDraw.Draw(base)
    s = size * content_scale
    ox = (size - s) / 2
    # 气泡圆角矩形
    b = [ox + s * 0.18, ox + s * 0.26, ox + s * 0.82, ox + s * 0.74]
    d.rounded_rectangle(b, radius=s * 0.09, fill=(255, 255, 255, 255))
    # 气泡小尾巴
    tail = [
        (b[0] + s * 0.20, b[3] - s * 0.02),
        (b[0] + s * 0.34, b[3] - s * 0.02),
        (b[0] + s * 0.30, b[3] + s * 0.12),
    ]
    d.polygon(tail, fill=(255, 255, 255, 255))
    # 气泡内的两行文本线条
    line_c = (150, 156, 164, 255)
    lw = max(2, int(s * 0.035))
    d.line([(b[0] + s * 0.09, b[1] + s * 0.16), (b[2] - s * 0.09, b[1] + s * 0.16)], fill=line_c, width=lw)
    d.line([(b[0] + s * 0.09, b[1] + s * 0.30), (b[2] - s * 0.24, b[1] + s * 0.30)], fill=line_c, width=lw)
    # 绿色对勾
    green = (0, 169, 127, 255)
    gw = max(3, int(s * 0.05))
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2 + s * 0.04
    d.line([(cx - s * 0.13, cy), (cx - s * 0.035, cy + s * 0.11), (cx + s * 0.15, cy - s * 0.12)], fill=green, width=gw, joint="curve")
    return base

SIZES = {"icon-180.png": 180, "icon-192.png": 192, "icon-512.png": 512, "icon-512-maskable.png": 512}

for name, size in SIZES.items():
    icon = rounded_gradient(size, size * 0.225, (0, 200, 150), (76, 125, 255))
    icon = draw_bubble_icon(icon, size, content_scale=1.0 if not name.endswith("maskable.png") else 0.8)
    icon.save(f"{OUT}\\{name}")
    print("saved", name, size)

print("DONE")
