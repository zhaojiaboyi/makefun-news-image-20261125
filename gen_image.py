# Builds entry.png for the 25 November 2026 news-image bounty.
# A 1024x1024 poster: navy masthead, six story cards in two columns,
# navy footer. Everything is drawn with Pillow shapes and DejaVu text;
# there are no photographs. Run: python3 gen_image.py

import math
import os

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
PAPER = (250, 246, 238)
CARD = (255, 255, 255)
DEEP = (18, 30, 58)
INK = (28, 28, 30)
SOFT = (96, 96, 100)
ACCENT = (214, 176, 58)
EDGE = (216, 210, 198)
TILE = (244, 241, 234)

FONTS = "/usr/share/fonts/truetype/dejavu"


def fnt(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONTS, name), size)


DATE_F = fnt(True, 60)
STRAP_F = fnt(False, 23)
TAG_F = fnt(True, 16)
HEAD_F = fnt(True, 27)
BODY_F = fnt(False, 20)
FOOT_F = fnt(False, 16)

# tag, headline, summary, colour, glyph name
ITEMS = [
    ("HORMUZ / ENERGY", "Tankers hit mines in Hormuz",
     "Iran's IRGC says two oil tankers struck naval mines, exploded and caught fire in the strait.",
     (176, 34, 46), "boat"),
    ("SPACE / CHINA", "Pakistan's first astronaut in orbit",
     "Muhammad Zeeshan Ali launched on Shenzhou-24 and docked with the Tiangong station on Wednesday.",
     (30, 80, 124), "orbit"),
    ("USA / TRADE", "Trump unveils new tariffs",
     "Washington proposes 20-40% tariffs on 14 partners including China and the EU; hearing set for January.",
     (28, 124, 62), "scale"),
    ("PACIFIC / DEFENCE", "Australia-Solomons treaty signed",
     "Canberra and Honiara sign a pact barring any foreign military base in the Solomon Islands.",
     (94, 48, 144), "shield"),
    ("UKRAINE / WAR", "Drones torch Russian refineries",
     "Ukrainian drones hit the Syzran and Kuibyshev refineries in Samara overnight; one person killed.",
     (144, 32, 32), "flame"),
    ("MARKETS / ASIA", "Asian stocks plunge on AI selloff",
     "Korea's KOSPI fell 6.2%, Japan's Nikkei 2.8% and Taiwan about 5% as chip shares tumbled.",
     (124, 76, 20), "fall"),
]


def lines_for(draw, text, font, limit):
    out, row = [], ""
    for word in text.split():
        cand = (row + " " + word).strip()
        if draw.textlength(cand, font=font) <= limit:
            row = cand
        else:
            if row:
                out.append(row)
            row = word
    if row:
        out.append(row)
    return out


def glyph_boat(d, x, y, s, c):
    hull = [(x + 4, y + 56), (x + s - 4, y + 56), (x + s - 18, y + 82), (x + 18, y + 82)]
    d.polygon(hull, fill=c)
    d.rectangle([x + 30, y + 36, x + 66, y + 56], fill=c)
    d.line([(x + 48, y + 36), (x + 48, y + 10)], fill=c, width=5)
    d.polygon([(x + 48, y + 10), (x + 76, y + 22), (x + 48, y + 26)], fill=c)
    d.arc([x + 6, y + 84, x + 42, y + 100], 0, 180, fill=c, width=4)
    d.arc([x + 54, y + 84, x + 90, y + 100], 0, 180, fill=c, width=4)


def glyph_orbit(d, x, y, s, c):
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=c)
    d.ellipse([x + 4, y + 26, x + s - 4, y + s - 26], outline=c, width=4)
    d.ellipse([x + s - 18, y + 34, x + s - 4, y + 48], fill=c)
    d.ellipse([cx - 6, cy - 6, cx + 2, cy + 2], fill=CARD)


def glyph_scale(d, x, y, s, c):
    cx = x + s // 2
    d.line([(cx, y + 14), (cx, y + 76)], fill=c, width=5)
    d.line([(x + 16, y + 24), (x + s - 16, y + 24)], fill=c, width=5)
    d.line([(x + 16, y + 24), (x + 6, y + 46)], fill=c, width=3)
    d.line([(x + 16, y + 24), (x + 26, y + 46)], fill=c, width=3)
    d.line([(x + s - 16, y + 24), (x + s - 26, y + 46)], fill=c, width=3)
    d.line([(x + s - 16, y + 24), (x + s - 6, y + 46)], fill=c, width=3)
    d.arc([x + 4, y + 38, x + 28, y + 56], 0, 180, fill=c, width=4)
    d.arc([x + s - 28, y + 38, x + s - 4, y + 56], 0, 180, fill=c, width=4)
    d.rectangle([cx - 16, y + 78, cx + 16, y + 86], fill=c)


def glyph_shield(d, x, y, s, c):
    cx = x + s // 2
    pts = [(cx, y + 6), (x + s - 14, y + 18), (x + s - 14, y + 50),
           (cx, y + 92), (x + 14, y + 50), (x + 14, y + 18)]
    d.polygon(pts, outline=c, width=6)
    d.line([(cx - 14, y + 46), (cx - 4, y + 58), (cx + 16, y + 32)], fill=c, width=6)


def glyph_flame(d, x, y, s, c):
    cx = x + s // 2
    d.polygon([(cx, y + 6), (cx + 26, y + 44), (cx + 30, y + 66),
               (cx + 14, y + 88), (cx - 14, y + 88), (cx - 30, y + 66),
               (cx - 26, y + 44)], fill=c)
    d.polygon([(cx, y + 40), (cx + 12, y + 62), (cx + 6, y + 80),
               (cx - 6, y + 80), (cx - 12, y + 62)], fill=CARD)


def glyph_fall(d, x, y, s, c):
    pts = [(x + 8, y + 16), (x + 36, y + 30), (x + 58, y + 52), (x + 84, y + 74)]
    d.line(pts, fill=c, width=6)
    d.polygon([(x + 84, y + 74), (x + 66, y + 72), (x + 76, y + 56)], fill=c)
    for i, h in enumerate((44, 34, 24)):
        bx = x + 14 + i * 26
        d.rectangle([bx, y + s - 8 - h, bx + 16, y + s - 8], outline=c, width=4)


GLYPHS = {"boat": glyph_boat, "orbit": glyph_orbit, "scale": glyph_scale,
          "shield": glyph_shield, "flame": glyph_flame, "fall": glyph_fall}


def poster():
    img = Image.new("RGB", (SIDE, SIDE), PAPER)
    d = ImageDraw.Draw(img)
    mast_h, foot_h = 164, 46
    d.rectangle([0, 0, SIDE, mast_h], fill=DEEP)
    d.text((34, 20), "WEDNESDAY  ·  THE WORLD IN ONE DAY", font=STRAP_F, fill=ACCENT)
    d.text((34, 54), "25 NOVEMBER 2026", font=DATE_F, fill=CARD)
    d.text((34, 124), "Six stories that defined the day, from Hormuz to Tiangong.",
           font=STRAP_F, fill=(198, 204, 218))
    col_w = SIDE // 2
    row_h = (SIDE - mast_h - foot_h) // 3
    for idx, (tag, head, body, colour, glyph) in enumerate(ITEMS):
        gx = (idx % 2) * col_w
        gy = mast_h + (idx // 2) * row_h
        d.rectangle([gx, gy, gx + col_w - 1, gy + row_h - 1], fill=CARD,
                    outline=EDGE, width=2)
        d.rectangle([gx, gy, gx + col_w - 1, gy + 7], fill=colour)
        tx, ty = gx + 18, gy + 40
        d.rounded_rectangle([tx - 6, ty - 6, tx + 104, ty + 104], radius=12, fill=TILE)
        GLYPHS[glyph](d, tx, ty, 98, colour)
        hx = gx + 144
        d.text((hx, gy + 24), tag, font=TAG_F, fill=colour)
        yy = gy + 50
        for ln in lines_for(d, head, HEAD_F, col_w - 162)[:2]:
            d.text((hx, yy), ln, font=HEAD_F, fill=INK)
            yy += 32
        yy += 5
        for ln in lines_for(d, body, BODY_F, col_w - 162)[:4]:
            d.text((hx, yy), ln, font=BODY_F, fill=SOFT)
            yy += 25
    d.rectangle([0, SIDE - foot_h, SIDE, SIDE], fill=DEEP)
    d.text((34, SIDE - 33),
           "Drawn by code, no photographs.  Sources: Reuters, AP, Just Security Early Edition, UN News.",
           font=FOOT_F, fill=(198, 204, 218))
    return img


if __name__ == "__main__":
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    poster().save(out_path, "PNG", optimize=True)
    print("entry.png bytes:", os.path.getsize(out_path))
