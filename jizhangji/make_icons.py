# -*- coding: utf-8 -*-
"""生成记账本 App 图标（渐变圆角方块 + 钱包 + ¥ 符号）"""
from PIL import Image, ImageDraw, ImageFont
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

def draw_wallet_icon(base, size, content_scale=1.0):
    """在渐变背景上画白色钱包 + ¥ 符号"""
    d = ImageDraw.Draw(base)
    s = size * content_scale
    ox = (size - s) / 2
    # 钱包主体（圆角矩形）
    w = [ox + s * 0.16, ox + s * 0.34, ox + s * 0.84, ox + s * 0.74]
    d.rounded_rectangle(w, radius=s * 0.08, fill=(255, 255, 255, 255))
    # 钱包顶部翻盖（小一些的圆角矩形）
    flap = [w[0] + s * 0.02, w[1] - s * 0.06, w[2] - s * 0.02, w[1] + s * 0.06]
    d.rounded_rectangle(flap, radius=s * 0.04, fill=(255, 255, 255, 255))
    # 钱包中间的圆点（按扣）
    cx = (w[0] + w[2]) / 2
    cy = (w[1] + w[3]) / 2 + s * 0.04
    r = s * 0.045
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 107, 107, 255))
    # ¥ 符号
    try:
        font = ImageFont.truetype("arial.ttf", int(s * 0.18))
    except OSError:
        font = ImageFont.load_default()
    text = "¥"
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), text, font=font, fill=(255, 255, 255, 255))
    return base

SIZES = {"icon-180.png": 180, "icon-192.png": 192, "icon-512.png": 512, "icon-512-maskable.png": 512}

for name, size in SIZES.items():
    icon = rounded_gradient(size, size * 0.225, (255, 107, 107), (255, 138, 92))
    icon = draw_wallet_icon(icon, size, content_scale=1.0 if not name.endswith("maskable.png") else 0.8)
    icon.save(os.path.join(OUT, name))
    print("saved", name, size)

print("DONE")