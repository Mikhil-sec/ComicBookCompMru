"""Builds the cover (page 1) and storyline page (page 2).

    .venv/Scripts/python tools/frontmatter.py   -> out/pages/cover.jpg, out/pages/storyline.jpg
"""
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from layout import BORDER, DPI, FONT_DIR, PAGE_H, PAGE_W, ROOT, fit, greedy

TITLE = "55 Spring Festivals"
TITLE_ZH = "五十五个春节"
THEME = "Touching Stories of the Ordinary People of China and Mauritius in the Journey of 55 Years"
NAMES = ["Mikhil Naika", "Yorvan Rengasamy", "Seeya Awotar"]
INK = (34, 26, 22)
PAPER = (250, 245, 234)
INNER_W, INNER_H = PAGE_W - 2 * BORDER, PAGE_H - 2 * BORDER


def vfont(name, size, weight=None):
    f = ImageFont.truetype(str(FONT_DIR / name), size)
    if weight:
        f.set_variation_by_axes([weight])
    return f


def centered(draw, y, text, fnt, fill, shadow=None):
    w = draw.textlength(text, font=fnt)
    x = (PAGE_W - w) / 2
    if shadow:
        draw.text((x, y), text, font=fnt, fill=shadow, stroke_width=6, stroke_fill=shadow)
    draw.text((x, y), text, font=fnt, fill=fill)
    return y + fnt.size


def cover():
    band = 470
    page = Image.new("RGB", (PAGE_W, PAGE_H), "white")
    art_h = INNER_H - band
    art = fit(Image.open(ROOT / "assets/cover/cover_art.png").convert("RGB"), INNER_W, art_h, 0.5, 0.35)

    # soft light veil behind the title
    veil = Image.new("L", art.size, 0)
    vd = ImageDraw.Draw(veil)
    for i in range(700):
        vd.line([(0, i), (INNER_W, i)], fill=int(150 * (1 - i / 700) ** 1.6))
    art = Image.composite(Image.new("RGB", art.size, (252, 246, 232)), art, veil)
    page.paste(art, (BORDER, BORDER))

    d = ImageDraw.Draw(page)
    band_top = BORDER + art_h
    d.rectangle([BORDER, band_top, BORDER + INNER_W, BORDER + INNER_H], fill=(28, 22, 26))
    d.line([(BORDER, band_top), (BORDER + INNER_W, band_top)], fill=(200, 160, 90), width=6)
    d.rectangle([BORDER, BORDER, BORDER + INNER_W - 1, BORDER + INNER_H - 1], outline=INK, width=5)

    title = vfont("TitleFont.ttf", 200, 800)
    y = centered(d, BORDER + 110, TITLE, title, INK)
    centered(d, y + 50, TITLE_ZH, vfont("ChineseFont.ttf", 96, 600), (150, 30, 30))

    y = band_top + 60
    y = centered(d, y, "THEME", vfont("BodyFont.ttf", 38, 700), (225, 185, 115)) + 22
    body = vfont("CaptionFont.ttf", 54, 500)
    for line in greedy(d, THEME, body, INNER_W - 300):
        y = centered(d, y, line, body, (250, 244, 230)) + 16
    y += 60
    centered(d, y, "  ·  ".join(NAMES), vfont("BodyFont.ttf", 58, 600), (250, 244, 230))
    save(page, "cover")


def thumb_strip(paths, w, h, labels, label_font):
    gap = 18
    tw = (w - gap * (len(paths) - 1)) // len(paths)
    strip = Image.new("RGB", (w, h + 56), PAPER)
    d = ImageDraw.Draw(strip)
    for i, (p, crop) in enumerate(paths):
        im = Image.open(ROOT / p).convert("RGB")
        if crop:
            W, H = im.size
            im = im.crop((int(crop[0] * W), int(crop[1] * H), int(crop[2] * W), int(crop[3] * H)))
        x = i * (tw + gap)
        strip.paste(fit(im, tw, h), (x, 0))
        d.rectangle([x, 0, x + tw - 1, h - 1], outline=INK, width=3)
        lw = d.textlength(labels[i], font=label_font)
        d.text((x + (tw - lw) / 2, h + 10), labels[i], font=label_font, fill=INK)
    return strip


def storyline():
    page = Image.new("RGB", (PAGE_W, PAGE_H), "white")
    d = ImageDraw.Draw(page)
    d.rectangle([BORDER, BORDER, BORDER + INNER_W, BORDER + INNER_H], fill=PAPER, outline=INK, width=4)
    pad = 70
    x0, w = BORDER + pad, INNER_W - 2 * pad
    y = BORDER + 60

    y = centered(d, y, "Storyline", vfont("TitleFont.ttf", 96, 800), INK) + 26
    theme_f = vfont("CaptionFont.ttf", 34, 500)
    for line in greedy(d, f"Theme: {THEME}", theme_f, w - 200):
        y = centered(d, y, line, theme_f, (110, 60, 40)) + 8
    y += 34

    md = (ROOT / "story/storyline.md").read_text(encoding="utf-8")
    paras = [p.strip() for p in md.split("\n\n") if p.strip() and not p.startswith("#")]
    words = sum(len(re.findall(r"\S+", p)) for p in paras)

    body = vfont("BodyFont.ttf", 38, 400)
    bold = vfont("BodyFont.ttf", 38, 700)
    lh = 54
    label_f = vfont("CaptionFont.ttf", 28, 500)

    for i, p in enumerate(paras):
        if p.startswith("**AI and other tools used.**"):
            # the AI workflow, shown before the tools paragraph
            strip = thumb_strip(
                [("assets/plates/shop_1972.png", None), ("assets/plates/shop_1984.png", None),
                 ("assets/plates/shop_2008.png", None), ("assets/plates/shop_2027.png", None)],
                w, 190, ["Shop 1972", "1984", "2008", "2027"], label_f)
            page.paste(strip, (x0, y + 6)); y += strip.height + 22
            sheets = ["wei_14", "wei_21", "wei_26", "wei_32", "wei_50", "wei_69"]
            strip = thumb_strip([(f"assets/sheets/{s}.png", (0.0, 0.62, 0.25, 1.0)) for s in sheets],
                                w, 190, ["Wei 14", "21", "26", "32", "50", "69"], label_f)
            page.paste(strip, (x0, y)); y += strip.height + 26
            lead, p = "AI and other tools used.", p.replace("**AI and other tools used.**", "").strip()
            d.text((x0, y), lead, font=bold, fill=INK)
            first_indent = d.textlength(lead + " ", font=bold)
        else:
            first_indent = 0
        lines = greedy(d, " " * 0 + p, body, w - first_indent)
        # re-wrap after the first line at full width
        if first_indent and len(lines) > 1:
            rest = p[len(lines[0]):].strip()
            lines = [lines[0]] + greedy(d, rest, body, w)
        for j, line in enumerate(lines):
            d.text((x0 + (first_indent if j == 0 else 0), y), line, font=body, fill=INK)
            y += lh
        y += 22
    save(page, "storyline")
    print(f"storyline words: {words}; text bottom at y={y} (page inner bottom {BORDER + INNER_H})")


def save(img, name):
    out = ROOT / "out" / "pages" / f"{name}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, quality=95, dpi=(DPI, DPI))
    prev = img.copy(); prev.thumbnail((1400, 1980))
    prev.save(ROOT / "renders" / f"preview_{name}.jpg", quality=85)
    print(out.relative_to(ROOT))


if __name__ == "__main__":
    cover()
    storyline()
