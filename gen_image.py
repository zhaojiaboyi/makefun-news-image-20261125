"""Draw the 25 November 2026 world-news image (1024x1024 PNG).

Run: python3 gen_image.py  -> writes entry.png beside this file.
Only Pillow + DejaVu fonts (present on this machine) are used; the entry
program itself (main.py) is stdlib-only and just copies entry.png.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
CREAM = (247, 243, 234)
NAVY = (20, 33, 61)
WHITE = (255, 255, 255)
INK = (25, 25, 25)
GREY = (90, 90, 90)
GOLD = (212, 175, 55)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 62)
F_SUB = font("DejaVuSans.ttf", 24)
F_KICK = font("DejaVuSans-Bold.ttf", 17)
F_HEAD = font("DejaVuSans-Bold.ttf", 28)
F_BODY = font("DejaVuSans.ttf", 21)
F_FOOT = font("DejaVuSans.ttf", 17)

STORIES = [
    ("HORMUZ  •  ENERGY", "Tankers hit mines in Hormuz",
     "Iran's IRGC says two oil tankers struck naval mines, exploded and caught fire in the strait.",
     (179, 32, 44), "ship"),
    ("SPACE  •  CHINA", "Pakistan's first astronaut in orbit",
     "Muhammad Zeeshan Ali launched on Shenzhou-24 and docked with the Tiangong station on Wednesday.",
     (31, 78, 121), "sat"),
    ("USA  •  TRADE", "Trump unveils new tariffs",
     "Washington proposes 20-40% tariffs on 14 partners including China and the EU; hearing set for January.",
     (29, 122, 61), "chip"),
    ("PACIFIC  •  DEFENCE", "Australia-Solomons treaty signed",
     "Canberra and Honiara sign a pact barring any foreign military base in the Solomon Islands.",
     (91, 45, 142), "radar"),
    ("UKRAINE  •  WAR", "Drones torch Russian refineries",
     "Ukrainian drones hit the Syzran and Kuibyshev refineries in Samara overnight; one person killed.",
     (140, 30, 30), "blast"),
    ("MARKETS  •  ASIA", "Asian stocks plunge on AI selloff",
     "Korea's KOSPI fell 6.2%, Japan's Nikkei 2.8% and Taiwan about 5% as chip shares tumbled.",
     (122, 74, 18), "chart"),
]


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def icon_ship(d, x, y, s, c):
    d.polygon([(x, y + 52), (x + s, y + 52), (x + s - 14, y + 78), (x + 14, y + 78)], fill=c)
    d.rectangle([x + s // 2 - 4, y + 12, x + s // 2 + 4, y + 52], fill=c)
    d.polygon([(x + s // 2 + 4, y + 12), (x + s // 2 + 34, y + 30), (x + s // 2 + 4, y + 34)], fill=c)
    for i, wy in enumerate((y + 88, y + 96)):
        d.line([(x + i * 6, wy), (x + s - i * 6, wy)], fill=c, width=4)


def icon_chip(d, x, y, s, c):
    d.rounded_rectangle([x + 14, y + 14, x + s - 14, y + s - 14], radius=8, outline=c, width=6)
    d.rectangle([x + s // 2 - 12, y + s // 2 - 12, x + s // 2 + 12, y + s // 2 + 12], fill=c)
    for i in range(3):
        px = x + 24 + i * 22
        d.line([(px, y + 4), (px, y + 14)], fill=c, width=4)
        d.line([(px, y + s - 14), (px, y + s - 4)], fill=c, width=4)
        py = y + 24 + i * 22
        d.line([(x + 4, py), (x + 14, py)], fill=c, width=4)
        d.line([(x + s - 14, py), (x + s - 4, py)], fill=c, width=4)


def icon_blast(d, x, y, s, c):
    cx, cy = x + s // 2, y + s // 2
    pts = []
    import math
    for i in range(16):
        r = 38 if i % 2 == 0 else 16
        a = math.pi * i / 8
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=c)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=WHITE)


def icon_radar(d, x, y, s, c):
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([x + 10, y + 10, x + s - 10, y + s - 10], outline=c, width=5)
    d.ellipse([x + 26, y + 26, x + s - 26, y + s - 26], outline=c, width=3)
    d.line([(cx, y + 10), (cx, y + s - 10)], fill=c, width=3)
    d.line([(x + 10, cy), (x + s - 10, cy)], fill=c, width=3)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=c)


def icon_sat(d, x, y, s, c):
    d.rectangle([x + 38, y + 38, x + s - 38, y + s - 38], fill=c)
    d.rectangle([x + 4, y + 44, x + 34, y + 60], outline=c, width=4)
    d.rectangle([x + s - 34, y + 44, x + s - 4, y + 60], outline=c, width=4)
    d.line([(x + s // 2, y + 38), (x + s - 14, y + 14)], fill=c, width=4)
    d.ellipse([x + s - 22, y + 6, x + s - 6, y + 22], outline=c, width=4)


def icon_chart(d, x, y, s, c):
    # Downward-trending bars with a falling line.
    base = y + s - 12
    heights = [62, 48, 34, 20]
    for i, h in enumerate(heights):
        bx = x + 12 + i * 22
        d.rectangle([bx, base - h, bx + 14, base], fill=c)
    pts = [(x + 12, y + 18), (x + 34, y + 34), (x + 56, y + 52), (x + 82, y + 72)]
    d.line(pts, fill=c, width=5)
    d.polygon([(x + 82, y + 72), (x + 68, y + 70), (x + 76, y + 58)], fill=c)


ICONS = {"ship": icon_ship, "chip": icon_chip, "blast": icon_blast,
         "radar": icon_radar, "sat": icon_sat, "chart": icon_chart}


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # Header band.
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.text((32, 22), "WEDNESDAY  •  THE WORLD IN ONE DAY", font=F_SUB, fill=GOLD)
    d.text((32, 58), "25 NOVEMBER 2026", font=F_TITLE, fill=WHITE)
    d.text((32, 128), "Six stories that defined the day, from Hormuz to Tiangong.",
           font=F_SUB, fill=(200, 205, 220))

    # Story grid: 2 columns x 3 rows.
    top, footer_h = 168, 48
    cell_w, cell_h = W // 2, (H - top - footer_h) // 3
    for i, (kicker, head, body, color, kind) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0, y0 = col * cell_w, top + row * cell_h
        d.rectangle([x0, y0, x0 + cell_w - 1, y0 + cell_h - 1], fill=WHITE,
                    outline=(210, 205, 195), width=2)
        d.rectangle([x0, y0, x0 + cell_w - 1, y0 + 8], fill=color)
        ix, iy = x0 + 20, y0 + 42
        d.rounded_rectangle([ix - 6, iy - 6, ix + 106, iy + 106], radius=12,
                            fill=(242, 240, 235))
        ICONS[kind](d, ix, iy, 100, color)
        tx = x0 + 146
        d.text((tx, y0 + 26), kicker, font=F_KICK, fill=color)
        y = y0 + 54
        for line in wrap(d, head, F_HEAD, cell_w - 166)[:2]:
            d.text((tx, y), line, font=F_HEAD, fill=INK)
            y += 33
        y += 6
        for line in wrap(d, body, F_BODY, cell_w - 166)[:4]:
            d.text((tx, y), line, font=F_BODY, fill=GREY)
            y += 26

    # Footer band.
    d.rectangle([0, H - footer_h, W, H], fill=NAVY)
    d.text((32, H - 35), "Drawn by code — no photographs.  Sources: Reuters, AP, Just Security Early Edition, UN News.",
           font=F_FOOT, fill=(200, 205, 220))

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
