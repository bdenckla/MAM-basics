"""For Claude: two sets of the trial's shapes over a close-up of the image.

Written for the concrete-transcription trial, 2026-11-03.  Usage, from the
MAM-basics clone's root:

    ./.venv/Scripts/python.exe py/main_concrete_transcription.py look3
        <work-dir> <before.json> <after.json>
        <out.png> <scale> x0 y0 x1 y1 [<id> ...] [--draft=<draft>]

Each json holds {"shapes": [...]}.  Draws the image's pixels x0..x1, y0..y1 at
<scale> times, the ink that the after-shapes leave farther than 1.3 px from every shape
red, the ink in two of them magenta, and the outlines of the given shapes (all,
when none is given): the before-shapes thin grey, the after-shapes blue, the
stroke green.  With --draft, the ink is less that draft's strips of vellum.
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from pen_stroke import geometry as geo
from concrete_transcription import ct_drafts
from concrete_transcription import ct_share

S = ct_share.S


def run(work, before_path, after_path, png, scale, box, ids, draft_name):
    signs = ct_drafts.draft(draft_name)[0] if draft_name else None
    before = json.loads(Path(before_path).read_text(encoding="utf-8"))["shapes"]
    after = json.loads(Path(after_path).read_text(encoding="utf-8"))["shapes"]
    x0, y0, x1, y1 = box
    ids = set(ids) or {s["id"] for s in after}
    l1 = json.loads((work / "level1.json").read_text(encoding="utf-8"))
    w, h = l1["width"], l1["height"]
    ink = ct_share.ink_mask(l1, signs)
    masks = {s["id"]: ct_share.shape_mask(s, w, h) for s in after}
    out, count, near_any = ct_share.share_out(ink, masks)
    ct_share.print_share(after_path, out)
    with Image.open(work / l1["image"]) as im:
        base = im.convert("RGB").crop((x0, y0, x1, y1))
    size = ((x1 - x0) * scale, (y1 - y0) * scale)
    base = base.resize(size, Image.Resampling.BICUBIC)
    over = np.zeros((h * S, w * S, 4), dtype=np.uint8)
    over[ink & ~near_any] = (255, 0, 0, 230)
    over[ink & (count >= 2)] = (255, 0, 255, 120)
    over_im = Image.fromarray(over, "RGBA").crop((x0 * S, y0 * S, x1 * S, y1 * S))
    pic = Image.alpha_composite(
        base.convert("RGBA"), over_im.resize(size, Image.Resampling.NEAREST)
    )
    draw = ImageDraw.Draw(pic)

    def outline(shape, colour, width):
        for poly in geo.flatten(geo.parse_path(ct_share.shape_d(shape))):
            pts = [((x - x0) * scale, (y - y0) * scale) for x, y in poly]
            draw.line(pts + [pts[0]], fill=colour, width=width)

    for s in before:
        if s["id"] in ids:
            outline(s, (150, 150, 150, 255), 1)
    for s in after:
        if s["id"] in ids:
            outline(
                s, (0, 160, 0, 255) if s["type"] == "stroke" else (0, 90, 255, 255), 2
            )
    pic.convert("RGB").save(png)
    print(png)
