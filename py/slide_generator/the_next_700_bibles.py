"""Slide definitions for the 'The Next 700 Bibles' deck.

Slides
------
title-card      "The Next 700 Bibles" with a nod to P. J. Landin (1966)
"""

import pathlib

from PIL import ImageFont

from slide_generator import slide_render

DECK_NAME = "the-next-700-bibles"
IMAGES_DIR = pathlib.Path("misc/the-next-700-bibles/img")

# Teal gradient shared across all slides in this deck
_TOP_RGB = (13, 94, 87)
_BOT_RGB = (8, 61, 56)


def _gradient():
    return slide_render.make_gradient(_TOP_RGB, _BOT_RGB)


def render_title_card(**kwargs):
    """Render slide-title-card.png."""
    font_bold = ImageFont.truetype(str(slide_render.FONT_DIR / "arialbd.ttf"), size=180)
    font_reg = ImageFont.truetype(str(slide_render.FONT_DIR / "arial.ttf"), size=96)
    lines = [
        ("The Next 700 Bibles", font_bold, (255, 255, 255)),
        ("after P. J. Landin (1966)", font_reg, (200, 232, 228)),
    ]
    img = _gradient()
    slide_render.draw_centered_lines(img, lines, gap_after=[80, 0])
    dest = IMAGES_DIR / "slide-title-card.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest)
    slide_render.write_provenance(dest, DECK_NAME, "title-card")
    print(f"Saved {dest} {img.size}")


ALL_SLIDES = {
    "title-card": render_title_card,
}
