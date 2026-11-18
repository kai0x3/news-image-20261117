#!/usr/bin/env python3
"""Build the 17 Nov 2026 world-news front page (1024x1024 PNG) for the
make.fun news-image-20261117 bounty. Headlines verified against
Just Security Early Edition, Level Headlines daily brief and NPR 5am ET,
all 17 Nov 2026 (checked 2026-11-18 00:45 UTC)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 234)      # newsprint cream
INK = (24, 24, 28)
NAVY = (18, 38, 66)
RED = (178, 34, 34)
GOLD = (198, 148, 44)
GREY = (90, 90, 92)
RULE = (180, 172, 158)

F = "/usr/share/fonts/truetype/dejavu/"
serif_b = lambda s: ImageFont.truetype(F + "DejaVuSerif-Bold.ttf", s)
serif = lambda s: ImageFont.truetype(F + "DejaVuSerif.ttf", s)
sans_b = lambda s: ImageFont.truetype(F + "DejaVuSans-Bold.ttf", s)
sans = lambda s: ImageFont.truetype(F + "DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def wrap(draw, s, font, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# ---- masthead ----
d.rectangle([0, 0, W, 118], fill=NAVY)
text(512, 14, "TUESDAY  •  17 NOVEMBER 2026", sans_b(30), fill=(232, 222, 190), anchor="ma")
text(512, 52, "THE WORLD IN ONE IMAGE", serif_b(52), fill=(255, 255, 255), anchor="ma")
d.rectangle([0, 118, W, 124], fill=GOLD)

# ---- lead story: Kerch Bridge ----
text(48, 146, "UKRAINE STRIKES KERCH BRIDGE", serif_b(44), fill=RED)
for i, ln in enumerate(wrap(d, "Road span to Crimea collapses; Zelenskyy hails an \u201cunprecedented operation\u201d \u2014 as Russia hits Kyiv bridges in reply.", serif(25), 928)):
    text(48, 210 + i * 32, ln, serif(25))

# bridge illustration: deck with a broken gap, two towers, smoke
bx0, by0, bx1, by1 = 48, 300, 976, 470
d.rectangle([bx0, by0, bx1, by1], fill=(214, 226, 232))
d.rectangle([bx0, by0, bx1, by0 + 4], fill=NAVY)
# deck
d.rectangle([bx0 + 20, 420, 470, 436], fill=INK)
d.rectangle([554, 420, bx1 - 20, 436], fill=INK)
# broken span falling
d.polygon([(478, 420), (546, 420), (530, 452), (492, 452)], fill=RED)
# towers
for tx in (180, 830):
    d.rectangle([tx, 330, tx + 14, 424], fill=INK)
    d.line([tx + 7, 330, 470, 420], fill=INK, width=3)
    d.line([tx + 7, 330, 554, 420], fill=INK, width=3)
# smoke puffs over the gap
for cx, cy, r in [(512, 372, 26), (488, 352, 20), (538, 350, 18), (512, 330, 14)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 122))
# water
for wy in (452, 462):
    d.line([bx0 + 20, wy, bx1 - 20, wy], fill=(90, 130, 160), width=3)
text(48, 478, "The Kerch Strait bridge, Russia's link to occupied Crimea.", sans(20), fill=GREY)

# ---- rule ----
d.line([48, 516, 976, 516], fill=RULE, width=2)

# ---- four stories in a 2x2 grid ----
stories = [
    ("MIDDLE EAST ON EDGE", RED,
     ["Iran fires drones at a U.S.",
      "radar base in Bahrain;",
      "tankers hit by mines in",
      "the Strait of Hormuz as a",
      "third U.S. carrier arrives."]),
    ("TRUMP IN ASIA", NAVY,
     ["President Trump lands in",
      "Manila for the ASEAN",
      "summit, signs a trade deal",
      "with Thailand, then heads",
      "to China for Xi\u2013Putin talks."]),
    ("ROCKET FAILURE", NAVY,
     ["A ULA Vulcan rocket fails",
      "in flight, destroying 40",
      "Amazon Leo internet",
      "satellites bound for orbit."]),
    ("MARKETS & TECH", NAVY,
     ["JPMorgan blames a software",
      "bug for a banking outage;",
      "UK sanctions Israeli",
      "settlement builders; Nvidia",
      "reports earnings."]),
]
gx, gy = 48, 540
cw, ch = 452, 210
for i, (head, col, lines) in enumerate(stories):
    x = gx + (i % 2) * (cw + 24)
    y = gy + (i // 2) * (ch + 16)
    d.rectangle([x, y, x + cw, y + ch], outline=RULE, width=2)
    d.rectangle([x, y, x + cw, y + 44], fill=col)
    text(x + 14, y + 8, head, sans_b(24), fill=(255, 255, 255))
    for j, ln in enumerate(lines):
        text(x + 14, y + 56 + j * 28, ln, sans(22))

# ---- footer ----
d.line([48, 992, 976, 992], fill=RULE, width=2)
text(512, 998, "Also: Estonia to shut Russia border crossings  •  GTA VI launches Thursday",
     sans(19), fill=GREY, anchor="ma")

img.save("/home/hatch/workspace/makefun/news-image-20261117/entry.png", "PNG", optimize=True)
print("saved")
