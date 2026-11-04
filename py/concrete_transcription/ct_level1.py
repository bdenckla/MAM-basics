"""Level 1 of the trial's image: threshold, the fills, the residual pieces.

Written for the concrete-transcription trial, 2026-11-03.  Usage, from the
MAM-basics clone's root:

    ./.venv/Scripts/python.exe py/main_concrete_transcription.py level1
        <image.jpg> <work-dir>

Writes <work-dir>/112-Detail.png, the decoded pixels, lossless; level1.json, the
threshold, speck size, halo band, the fills' path data and the residual pieces'
paths; and level1-pieces.png, each 8-connected piece of thresholded ink numbered
at its first pixel, for placing seeds.  Uses the tracked level 1 code unchanged.
"""

import json

import numpy as np
from PIL import Image, ImageDraw

from pen_stroke import geometry as geo
from pen_stroke import level1
from pen_stroke import raster

# The snips' word crops used speck size 8 and halo band 24 at Sefaria's scale.
# This image is about 2.7 times Sefaria's scale each way, so a speck's area is
# about 7 times as many pixels.
SPECK_SIZE = 50
HALO_BAND = 24


def run(src, work):
    work.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        rgb = im.convert("RGB")
    png = work / "112-Detail.png"
    rgb.save(png)
    lum = raster.load_luminance(png)
    h, w = lum.shape
    threshold = raster.otsu_threshold(lum)
    ink = lum < threshold
    comps = level1.trace_fills(ink, SPECK_SIZE)
    fill_ds = [geo.format_path(c, level1.FILL_PLACES) for c in comps]
    fills_px = level1.fill_mask(fill_ds, w, h)
    pieces, smoothing, halo = level1.image_residual(
        lum, threshold, HALO_BAND, SPECK_SIZE, fills_px
    )
    out = {
        "image": png.name,
        "width": w,
        "height": h,
        "threshold": threshold,
        "speck_size": SPECK_SIZE,
        "halo_band": HALO_BAND,
        "tracer": level1.TRACER,
        "fills": [],
        "pieces": [],
    }
    for k, d in enumerate(fill_ds, 1):
        mask = level1.fill_mask([d], w, h)
        ys, xs = np.nonzero(mask)
        out["fills"].append(
            {
                "id": f"f{k}",
                "d": d,
                "area": int(mask.sum()),
                "box": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
            }
        )
    for k, (source, mask) in enumerate(pieces, 1):
        ys, xs = np.nonzero(mask)
        out["pieces"].append(
            {
                "id": f"r{k}",
                "source": source,
                "d": geo.mask_path(mask),
                "area": int(mask.sum()),
                "box": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                "mean_lum": round(float(lum[mask].mean()), 1),
            }
        )
    with open(work / "level1.json", "w", encoding="utf-8", newline="\n") as fp:
        json.dump(out, fp, ensure_ascii=False, indent=1)
        fp.write("\n")
    print(
        "size",
        w,
        h,
        "threshold",
        threshold,
        "lum min/median/max",
        int(lum.min()),
        int(np.median(lum)),
        int(lum.max()),
    )
    print("ink pixels", int(ink.sum()), "fill pixels", int(fills_px.sum()))
    for f in out["fills"]:
        print(f["id"], "area", f["area"], "box", f["box"])
    for p in out["pieces"]:
        print(
            p["id"],
            p["source"],
            "area",
            p["area"],
            "box",
            p["box"],
            "mean lum",
            p["mean_lum"],
        )
    _pieces_image(rgb, out["fills"], work / "level1-pieces.png", w, h)


def _pieces_image(rgb, fills, out_path, w, h):
    scale = 3
    big = rgb.resize((w * scale, h * scale), Image.Resampling.BICUBIC)
    draw = ImageDraw.Draw(big)
    for f in fills:
        for poly in geo.flatten(geo.parse_path(f["d"])):
            pts = [(x * scale, y * scale) for x, y in poly]
            draw.line(pts + [pts[0]], fill=(255, 0, 0), width=1)
        x0, y0 = f["box"][0], f["box"][1]
        draw.text((x0 * scale, max(0, y0 * scale - 12)), f["id"], fill=(0, 0, 255))
    big.save(out_path)
