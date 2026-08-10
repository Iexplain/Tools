# -*- coding: utf-8 -*-
"""生成入口页「我的小工具」App 图标（深色渐变圆角方块 + 白色清单条目）"""
from PIL import Image, ImageDraw
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
os.makedirs(OUT, exist_ok=True)


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


def draw_list_icon(base, size, content_scale=1.0):
    """在渐变背景上画三条白色清单行，每行前面一个彩色圆点（对应各个子应用）"""
    d = ImageDraw.Draw(base)
    s = size * content_scale
    ox = (size - s) / 2
    oy = (size - s) / 2

    dot_colors = [(0, 200, 150), (255, 107, 107), (148, 163, 184)]  # 求职录绿 / 记账本红 / 预留灰
    line_h = s * 0.075
    gap = s * 0.135
    top = oy + s * 0.30
    dot_r = s * 0.055
    dot_cx = ox + s * 0.26
    bar_x0 = ox + s * 0.38
    bar_widths = [0.36, 0.30, 0.22]

    for i in range(3):
        cy = top + i * (line_h + gap)
        d.ellipse([dot_cx - dot_r, cy - dot_r, dot_cx + dot_r, cy + dot_r], fill=dot_colors[i] + (255,))
        x1 = bar_x0 + s * bar_widths[i]
        d.rounded_rectangle(
            [bar_x0, cy - line_h / 2, x1, cy + line_h / 2],
            radius=line_h / 2,
            fill=(255, 255, 255, 255),
        )
    return base


SIZES = {"icon-180.png": 180, "icon-192.png": 192, "icon-512.png": 512, "icon-512-maskable.png": 512}

for name, size in SIZES.items():
    icon = rounded_gradient(size, size * 0.225, (31, 41, 55), (55, 65, 81))
    icon = draw_list_icon(icon, size, content_scale=1.0 if not name.endswith("maskable.png") else 0.8)
    icon.save(os.path.join(OUT, name))
    print("saved", name, size)

print("DONE")
