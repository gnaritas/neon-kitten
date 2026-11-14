#!/usr/bin/env python3
"""Generate public/og.png (1200x630) — Neon Kitten share-card art.
Ransom-note blocks on jet black + halftone + paw motif. Shop identity only
(no builder names per lane ruling); claims limited to sourced facts."""
import random
from PIL import Image, ImageDraw, ImageFont

SUP = "/System/Library/Fonts/Supplemental/"
COAL = (11, 11, 14); PAPER = (246, 241, 229); PINK = (255, 47, 142)
ACID = (212, 255, 63); SMOKE = (167, 167, 179)

W, H = 1200, 630
img = Image.new("RGB", (W, H), COAL)
d = ImageDraw.Draw(img)

def F(name, size):
    return ImageFont.truetype(SUP + name, size)

disp, mono = F("Impact.ttf", 168), F("Courier New Bold.ttf", 24)
small = F("Courier New.ttf", 22)
tag_f = F("Impact.ttf", 54)

# frame
d.rectangle([10, 10, W - 11, H - 11], outline=PINK, width=3)

# halftone field, upper right (deterministic randomness)
rnd = random.Random(42)
for gy in range(30, 300, 18):
    for gx in range(760, W - 24, 18):
        if rnd.random() < 0.62:
            r = 2.2 + rnd.random() * 3.4
            col = PINK if rnd.random() < 0.8 else ACID
            d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=col)

# paw print motif, upper right over the dots
def paw(cx, cy, s, col):
    d.ellipse([cx - 34*s, cy - 10*s, cx + 34*s, cy + 44*s], fill=col)
    for i, (dx, dy) in enumerate([(-40, -34), (-13, -48), (15, -48), (41, -32)]):
        d.ellipse([cx + dx*s - 13*s, cy + dy*s - 13*s, cx + dx*s + 13*s, cy + dy*s + 13*s], fill=col)
paw(1010, 210, 1.15, COAL)

# kicker
d.text((48, 42), "NEW  ·  DOWNTOWN VANCOUVER, WA", font=mono, fill=ACID)

def ransom(text, x, y, bg, angle, size=168):
    fnt = F("Impact.ttf", size)
    tb = ImageDraw.Draw(Image.new("RGB", (10, 10))).textbbox((0, 0), text, font=fnt)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    pad_x, pad_y = 26, 10
    bw, bh = tw + pad_x * 2, th + pad_y * 2 + 14
    blk = Image.new("RGBA", (bw + 40, bh + 40), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blk)
    bd.rectangle([20, 20, 20 + bw, 20 + bh], fill=bg)
    bd.text((20 + pad_x - tb[0], 20 + pad_y - tb[1] + 4), text, font=fnt, fill=COAL)
    blk = blk.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(blk, (x, y), blk)

ransom("NEON", 44, 118, PINK, -3)
ransom("KITTEN", 96, 300, ACID, 2)

# tagline
d.text((48, 470), "CATS. PUNK. THINGS.", font=tag_f, fill=PAPER)
tb = d.textbbox((48, 470), "CATS. PUNK. THINGS.", font=tag_f)
d.rectangle([48, tb[3] + 12, tb[2], tb[3] + 17], fill=PINK)

# footer NAP line (sourced facts only)
d.text((48, H - 58), "621 Broadway St · Vancouver, WA 98660 · neonkittenpdx@gmail.com", font=small, fill=SMOKE)

img.save("/Users/rleon/sites/neon-kitten/public/og.png", "PNG", optimize=True)
print("og.png written", img.size)
