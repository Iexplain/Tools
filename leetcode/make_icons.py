# -*- coding: utf-8 -*-
"""生成 LeetTrack App 图标（翠绿渐变圆角方块 + 白色对勾）"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
os.makedirs(OUT, exist_ok=True)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def rounded_gradient(size, radius, c1, c2):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for y in range(size):
        t = y / (size - 1)
        d.line([(0, y), (size, y)], fill=lerp(c1, c2, t))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    img.putalpha(mask)
    return img

def draw_check(base, size, content_scale=1.0):
    """白色对勾 + 底部小括号线，暗示「代码」"""
    d = ImageDraw.Draw(base)
    s = size * content_scale
    ox = (size - s) / 2
    # 对勾
    p1 = (ox + s * 0.26, ox + s * 0.52)
    p2 = (ox + s * 0.44, ox + s * 0.70)
    p3 = (ox + s * 0.76, ox + s * 0.32)
    d.line([p1, p2, p3], fill=(255, 255, 255, 255), width=int(s * 0.11), joint="curve")
    # 底部代码括号线 </> 风格：两条短线
    lw = int(s * 0.045)
    y = ox + s * 0.80
    d.line([(ox + s * 0.30, y), (ox + s * 0.70, y)], fill=(255, 255, 255, 200), width=lw)
    return base

SIZES = {"icon-180.png": 180, "icon-192.png": 192, "icon-512.png": 512, "icon-512-maskable.png": 512}

for name, size in SIZES.items():
    icon = rounded_gradient(size, size * 0.225, (52, 211, 153), (5, 150, 105))
    icon = draw_check(icon, size, content_scale=1.0 if not name.endswith("maskable.png") else 0.8)
    icon.save(os.path.join(OUT, name))
    print("saved", name, size)

print("DONE")
