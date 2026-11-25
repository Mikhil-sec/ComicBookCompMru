"""Builds pages 7-8 (ID snaps, signed form) and the final 8-page PDF.

    .venv/Scripts/python tools/final_pdf.py [STUDENT_ID]

The images in private/ are placed by code only. A layout-check copy with grey
boxes instead of the photos goes to renders/check_p7_p8.jpg, so the layout can be
reviewed without exposing the documents.
"""
import sys
from pathlib import Path

import img2pdf
from PIL import Image, ImageDraw, ImageOps

from frontmatter import INK, NAMES, vfont, centered
from layout import BORDER, DPI, PAGE_H, PAGE_W, ROOT

INNER_W, INNER_H = PAGE_W - 2 * BORDER, PAGE_H - 2 * BORDER
PRIV = ROOT / "private"
IDS = [("Mikhil Naika", "id_mikhil.jpeg"), ("Yorvan Rengasamy", "id_yorvan.jpeg"), ("Seeya Awotar", "id_seeya.jpeg")]


def trim_to_page(im):
    """Crop a screenshot to the bright form page (drops status bars, app chrome)."""
    g = ImageOps.grayscale(im)
    w, h = g.size
    px = g.load()
    rows = [y for y in range(h) if sum(px[x, y] for x in range(0, w, 4)) / len(range(0, w, 4)) > 185]
    cols = [x for x in range(w) if sum(px[x, y] for y in range(0, h, 4)) / len(range(0, h, 4)) > 185]
    if not rows or not cols:
        return im
    box = (min(cols), min(rows), max(cols) + 1, max(rows) + 1)
    # only trim if it keeps most of the image (avoid cutting a dark-themed form)
    if (box[2] - box[0]) * (box[3] - box[1]) < 0.5 * w * h:
        return im
    return im.crop(box)


def contain(im, w, h):
    s = min(w / im.width, h / im.height)
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


def page7(check):
    page = Image.new("RGB", (PAGE_W, PAGE_H), "white")
    d = ImageDraw.Draw(page)
    y = centered(d, BORDER + 20, "Participant Identification", vfont("TitleFont.ttf", 80, 800), INK) + 50
    label = vfont("BodyFont.ttf", 44, 600)
    slot_h = (BORDER + INNER_H - y) // 3 - 70
    for name, fn in IDS:
        im = contain(Image.open(PRIV / fn).convert("RGB"), INNER_W - 200, slot_h)
        if check:
            im = Image.new("RGB", im.size, (170, 170, 170))
        x = (PAGE_W - im.width) // 2
        page.paste(im, (x, y))
        d.rectangle([x, y, x + im.width, y + im.height], outline=INK, width=3)
        centered(d, y + im.height + 10, name, label, INK)
        y += slot_h + 70
    return page


def page8(check):
    page = Image.new("RGB", (PAGE_W, PAGE_H), "white")
    form = trim_to_page(Image.open(PRIV / "form.jpeg").convert("RGB"))
    im = contain(form, INNER_W, INNER_H)
    if check:
        im = Image.new("RGB", im.size, (170, 170, 170))
    page.paste(im, ((PAGE_W - im.width) // 2, (PAGE_H - im.height) // 2))
    print(f"form source {form.size} -> placed {im.size} (~{round(DPI * form.width / im.width)} dpi effective)")
    return page


def main():
    sid = sys.argv[1] if len(sys.argv) > 1 else "STUDENTID"
    out = ROOT / "out" / "pages"
    p7, p8 = page7(False), page8(False)
    p7.save(out / "p7_ids.jpg", quality=95, dpi=(DPI, DPI))
    p8.save(out / "p8_form.jpg", quality=95, dpi=(DPI, DPI))

    c7, c8 = page7(True), page8(True)
    check = Image.new("RGB", (PAGE_W * 2 + 40, PAGE_H), "#888")
    check.paste(c7, (0, 0)); check.paste(c8, (PAGE_W + 40, 0))
    check.thumbnail((1600, 1200)); check.save(ROOT / "renders" / "check_p7_p8.jpg", quality=85)

    pages = [out / f for f in ["cover.jpg", "storyline.jpg", "b1.jpg", "b2.jpg", "b3.jpg", "b4.jpg", "p7_ids.jpg", "p8_form.jpg"]]
    a4 = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
    pdf = ROOT / "out" / f"{sid}naika_mikhil.pdf"
    pdf.write_bytes(img2pdf.convert([str(p) for p in pages], layout_fun=img2pdf.get_layout_fun(a4)))
    print(pdf.relative_to(ROOT), f"{pdf.stat().st_size / 1e6:.1f} MB, {len(pages)} pages")


if __name__ == "__main__":
    main()
