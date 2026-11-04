"""For Claude: a text map of the ink where the stray stroke meets the letters.

Written for the concrete-transcription trial, 2026-11-03.  Usage, from the
MAM-basics clone's root:

    ./.venv/Scripts/python.exe py/main_concrete_transcription.py measure
        <work-dir> x0 x1 y0 y1 [<prefix>] [--samples]

One character a pixel, from the draft's owner (by default draft 1's, the work
files of prefix "draft"; "draft2" for draft 2's) of the sample at the pixel's
centre: R the resh, N the nun, Z the zayin, S the stroke's draft region, other
ink '#', vellum '.', and ':' where the image's luminance is below the level-1
threshold but the sample is vellum in the ink mask, which is less the draft's
strips of vellum.  With --samples, one character a sample, each in lower case
where a cut of the draft crosses it; the rows and columns are numbered in
pixels at each pixel's first sample.
"""

import json
from types import SimpleNamespace

import numpy as np
from PIL import Image

from pen_stroke import region_derive as rd
from concrete_transcription import ct_drafts
from concrete_transcription import ct_share

S = ct_share.S
LETTER = {"rg7": "Z", "rg10": "R", "rg15": "N", "rg20": "S"}


def run(work, box, prefix, samples):
    x0, x1, y0, y1 = box
    l1 = json.loads((work / "level1.json").read_text(encoding="utf-8"))
    regions = json.loads((work / f"{prefix}-regions.json").read_text(encoding="utf-8"))
    owner = np.load(work / f"{prefix}-owner.npy")
    # region_derive.settle ranks the regions by number, from 1; 0 is no region.
    order = sorted(regions["regions"], key=lambda rid: int(rid.removeprefix("rg")))
    ids = dict(enumerate(order, 1))
    names = [n for n, (_m, p) in ct_drafts.DRAFTS.items() if p == prefix]
    signs = ct_drafts.draft(names[0])[0] if names else None
    ink = ct_share.ink_mask(l1, signs)
    with Image.open(work / l1["image"]) as im:
        lum = np.asarray(im.convert("L"), dtype=np.int32)
    print("owner array", owner.shape, owner.dtype, "regions", len(ids))
    if samples:
        _sample_map(l1, signs, owner, ids, ink, lum, x0, x1, y0, y1)
        return
    head = "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(x0, x1))
    print("     " + head)
    print("     " + "".join(str(x % 10) for x in range(x0, x1)))
    for y in range(y0, y1):
        row = []
        for x in range(x0, x1):
            sy, sx = y * S + S // 2, x * S + S // 2
            o = int(owner[sy, sx])
            if ink[sy, sx]:
                row.append(LETTER.get(ids.get(o), "#"))
            else:
                row.append(":" if lum[y, x] < l1["threshold"] else ".")
        print(f"{y:4} " + "".join(row))


def _sample_map(l1, signs, owner, ids, ink, lum, x0, x1, y0, y1):
    cuts = [
        SimpleNamespace(id=cid, d=d) for cid, d, _note in getattr(signs, "CUTS", [])
    ]
    rf = SimpleNamespace(width=l1["width"], height=l1["height"], cuts=cuts)
    on_cut = np.zeros(ink.shape, dtype=bool)
    for ys, xs in rd.cut_cells(rf).values():
        on_cut[ys, xs] = True
    cols = range(x0 * S, x1 * S)
    print("     " + "".join(str((c // S) % 10) if c % S == 0 else " " for c in cols))
    for sy in range(y0 * S, y1 * S):
        row = []
        for sx in cols:
            if ink[sy, sx]:
                ch = LETTER.get(ids.get(int(owner[sy, sx])), "#")
            else:
                ch = ":" if lum[sy // S, sx // S] < l1["threshold"] else "."
            row.append(ch.lower() if on_cut[sy, sx] else ch)
        label = f"{sy // S:4} " if sy % S == 0 else "     "
        print(label + "".join(row))
