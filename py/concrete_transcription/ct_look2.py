"""Write a contrast-stretched, gridded enlargement of part of an image, for viewing.

Written for the concrete-transcription trial, 2026-11-03.  Usage, from the
MAM-basics clone's root:

    ./.venv/Scripts/python.exe py/main_concrete_transcription.py look2
        <image> <out.png> <scale> x0 y0 x1 y1 [grid]

Luminance is stretched so that its 2nd and 98th percentiles in the box span 0 to 255;
nearest-neighbour enlargement, so each source pixel shows as a square.  A grid line
every <grid> source pixels (default 10), labelled with the source coordinate.
"""

import numpy as np
from PIL import Image, ImageDraw


def run(src, out, scale, box, grid):
    x0, y0, x1, y1 = box
    image = Image.open(src).convert("RGB").crop((x0, y0, x1, y1))
    rgb = np.asarray(image, dtype=np.float64)
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    lo, hi = np.percentile(lum, [2, 98])
    stretched = np.clip((lum - lo) / (hi - lo) * 255.0, 0, 255).astype(np.uint8)
    big = Image.fromarray(stretched, "L").resize(
        (stretched.shape[1] * scale, stretched.shape[0] * scale),
        Image.Resampling.NEAREST,
    )
    big = big.convert("RGB")
    draw = ImageDraw.Draw(big)
    for gx in range((x0 // grid + 1) * grid, x1, grid):
        px = (gx - x0) * scale
        draw.line([(px, 0), (px, big.height)], fill=(255, 0, 0), width=1)
        draw.text((px + 2, 2), str(gx), fill=(255, 0, 0))
    for gy in range((y0 // grid + 1) * grid, y1, grid):
        py = (gy - y0) * scale
        draw.line([(0, py), (big.width, py)], fill=(0, 140, 255), width=1)
        draw.text((2, py + 2), str(gy), fill=(0, 140, 255))
    big.save(out)
    print(out, big.size, "lum p2 p98", round(lo, 1), round(hi, 1))
