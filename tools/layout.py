"""Assemble a comic page: A4 portrait, 300 dpi, 2 cm borders, 6 panels.

    .venv/Scripts/python tools/layout.py b1        -> out/pages/board1.jpg

Layout (rows): wide / two medium / two medium / wide.
Panels are centre-cropped to their slot (optionally shifted with "crop": [fx, fy]
in story/pages.json, 0..1 for where the crop window sits), then lettered from
the same file. Lettering is drawn by code, never by the image model, so text is
exact and editable.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
DPI = 300
PAGE_W, PAGE_H = 2480, 3508          # A4 at 300 dpi
BORDER = 236                         # 2 cm
GUTTER = 36
WIDE_H = 780
INNER_W, INNER_H = PAGE_W - 2 * BORDER, PAGE_H - 2 * BORDER
MID_W = (INNER_W - GUTTER) // 2
MID_H = (INNER_H - 2 * WIDE_H - 3 * GUTTER) // 2
FONT_DIR = ROOT / "assets" / "fonts"


def slots():
    x0, y = BORDER, BORDER
    s = [(x0, y, INNER_W, WIDE_H)]
    y += WIDE_H + GUTTER
    for _ in range(2):
        s += [(x0, y, MID_W, MID_H), (x0 + MID_W + GUTTER, y, MID_W, MID_H)]
        y += MID_H + GUTTER
    s.append((x0, y, INNER_W, WIDE_H))
    return s


def fit(img, w, h, fx=0.5, fy=0.5):
    """Scale to cover w x h, then crop; fx/fy pick the crop window position."""
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left = round((img.width - w) * fx)
    top = round((img.height - h) * fy)
    return img.crop((left, top, left + w, top + h))


def font(name, size):
    path = FONT_DIR / name
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default(size)


def wrap(draw, text, fnt, max_w):
    """Greedy wrap, then narrow the width while the line count holds, so lines
    come out balanced instead of leaving a single word on the last line."""
    lines = greedy(draw, text, fnt, max_w)
    while len(lines) > 1:
        narrower = greedy(draw, text, fnt, max_w - 8)
        if len(narrower) != len(lines):
            break
        max_w -= 8
        lines = narrower
    return lines


def greedy(draw, text, fnt, max_w):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def text_block(draw, lines, fnt, pad):
    lh = fnt.size * 1.18
    w = max(draw.textlength(l, font=fnt) for l in lines) + 2 * pad
    h = lh * len(lines) + 2 * pad - (lh - fnt.size)
    return w, h, lh


def caption(draw, panel_xy, item):
    """Rectangular narration box; item: {text, at: [fx, fy] inside panel}."""
    (px, py, pw, ph) = panel_xy
    fnt = font("CaptionFont.ttf", item.get("size", 34))
    lines = wrap(draw, item["text"], fnt, item.get("max_w", 0.42) * pw)
    w, h, lh = text_block(draw, lines, fnt, 22)
    fx, fy = item.get("at", [0.03, 0.05])
    x, y = px + fx * pw, py + fy * ph
    x, y = min(x, px + pw - w - 12), min(y, py + ph - h - 12)
    draw.rectangle([x, y, x + w, y + h], fill=(250, 244, 228), outline=(40, 32, 28), width=3)
    for i, l in enumerate(lines):
        draw.text((x + 22, y + 22 + i * lh), l, font=fnt, fill=(30, 24, 20))


def bubble(draw, panel_xy, item):
    """Speech bubble; item: {text, at: [fx, fy] centre, tail: [fx, fy] tip}."""
    (px, py, pw, ph) = panel_xy
    fnt = font("DialogueFont.ttf", item.get("size", 36))
    lines = wrap(draw, item["text"], fnt, item.get("max_w", 0.34) * pw)
    w, h, lh = text_block(draw, lines, fnt, 30)
    w, h = w * 1.12, h * 1.18
    cx, cy = px + item["at"][0] * pw, py + item["at"][1] * ph
    cx = min(max(cx, px + w / 2 + 10), px + pw - w / 2 - 10)
    cy = min(max(cy, py + h / 2 + 10), py + ph - h / 2 - 10)
    box = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
    if "tail" in item:
        tx, ty = px + item["tail"][0] * pw, py + item["tail"][1] * ph
        base = 0.16 * min(w, h)
        dx = 1 if abs(tx - cx) < abs(ty - cy) else 0
        p1 = (cx - base * dx, cy - base * (1 - dx))
        p2 = (cx + base * dx, cy + base * (1 - dx))
        draw.polygon([p1, p2, (tx, ty)], fill="white", outline=(20, 20, 20))
        draw.line([p1, (tx, ty), p2], fill=(20, 20, 20), width=4)
    draw.ellipse(box, fill="white", outline=(20, 20, 20), width=4)
    if "tail" in item:  # hide the tail's base line inside the bubble
        draw.polygon([p1, p2, (cx + (tx - cx) * 0.25, cy + (ty - cy) * 0.25)], fill="white")
    ty0 = cy - (lh * (len(lines) - 1) + fnt.size) / 2
    for i, l in enumerate(lines):
        draw.text((cx - draw.textlength(l, font=fnt) / 2, ty0 + i * lh), l, font=fnt, fill=(15, 15, 15))


def build(board, letter=True):
    spec = json.loads((ROOT / "story" / "pages.json").read_text(encoding="utf-8"))[board]
    page = Image.new("RGB", (PAGE_W, PAGE_H), "white")
    draw = ImageDraw.Draw(page)
    for slot, p in zip(slots(), spec["panels"]):
        x, y, w, h = slot
        img = Image.open(ROOT / p["image"]).convert("RGB")
        page.paste(fit(img, w, h, *p.get("crop", [0.5, 0.5])), (x, y))
        draw.rectangle([x, y, x + w - 1, y + h - 1], outline=(20, 20, 20), width=5)
        if letter:
            for item in p.get("text", []):
                (caption if item["type"] == "caption" else bubble)(draw, slot, item)
    out = ROOT / "out" / "pages" / f"{board}{'' if letter else '_clean'}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    page.save(out, quality=95, dpi=(DPI, DPI))
    print(out.relative_to(ROOT))


if __name__ == "__main__":
    for b in [a for a in sys.argv[1:] if not a.startswith("--")]:
        build(b, letter="--clean" not in sys.argv)
