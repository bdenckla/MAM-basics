"""The trial's draft regions: a seeded watershed on the image's luminance, by the
tracked profile-2 derivation (py/pen_stroke/region_derive.py), unchanged.

Written for the concrete-transcription trial, 2026-11-03.  Usage, from the
MAM-basics clone's root:

    ./.venv/Scripts/python.exe py/main_concrete_transcription.py draft
        <work-dir> [<draft>]

Reads <work-dir>/level1.json and 112-Detail.png; writes, for draft 1 (the
default), draft-regions.json, each region's traced outline, draft-owner.npy and
draft-regions.png, the regions over the image; for draft 2, draft2-regions.json
and so on (ct_drafts.py).  A draft's strips of vellum (VELLUM) take their samples
out of the ink before the watershed, as region_derive.region_ink does; a draft
with STROKE_REST also gets the stray stroke's region less the stroke, traced, as
the regions file's "rest".
"""

import json
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw

from pen_stroke import geometry as geo
from pen_stroke import raster
from pen_stroke import region_derive as rd
from concrete_transcription import ct_drafts
from concrete_transcription import ct_share

PALETTE = [
    (230, 25, 75),
    (60, 180, 75),
    (255, 180, 0),
    (0, 130, 200),
    (245, 130, 48),
    (145, 30, 180),
    (70, 200, 200),
    (240, 50, 230),
    (160, 200, 40),
    (250, 140, 160),
    (0, 128, 128),
    (170, 110, 40),
    (128, 0, 0),
    (120, 220, 150),
    (128, 128, 0),
    (0, 0, 128),
    (110, 110, 110),
]


def run(work, draft_name):
    signs, prefix = ct_drafts.draft(draft_name)
    l1 = json.loads((work / "level1.json").read_text(encoding="utf-8"))
    w, h = l1["width"], l1["height"]
    lum = raster.load_luminance(work / l1["image"])
    ink = rd.scaled_mask([f["d"] for f in l1["fills"]], w, h)
    pieces = {p["id"]: p for p in l1["pieces"]}
    for pid, (judged, _why) in signs.JUDGMENTS.items():
        if judged == "ink":
            ink |= rd.scaled_mask([pieces[pid]["d"]], w, h)
        elif judged in rd.NOT_INK:
            ink &= ~rd.scaled_mask([pieces[pid]["d"]], w, h)
    if set(signs.JUDGMENTS) != set(pieces):
        raise SystemExit(f"unjudged pieces: {set(pieces) - set(signs.JUDGMENTS)}")
    level1_ink = ink
    strips = ct_share.vellum_strips(signs)
    if strips:
        ink = level1_ink.copy()
        for v in strips:
            mask = rd.vellum_mask(v, w, h)
            if not (mask & level1_ink).any():
                print("PROBLEM:", f"{v.id}: takes out no ink")
            print(
                v.id,
                "takes out",
                round((mask & level1_ink).sum() / rd.SAMPLES**2, 1),
                "px of ink",
            )
            ink &= ~mask
    regions = [
        SimpleNamespace(id=rid, seeds=[(float(x), float(y)) for x, y in seeds])
        for _g, _k, _o, _l, regs in signs.GROUPS
        for rid, seeds in regs
    ]
    cuts = [SimpleNamespace(id=cid, d=d) for cid, d, _note in signs.CUTS]
    for c in cuts:
        rd.cut_points(c)  # a cut that is not one path of straight segments raises
    rf = SimpleNamespace(
        width=w, height=h, cuts=cuts, regions=regions, speck_size=l1["speck_size"]
    )
    owner, rank, problems = rd.settle(rf, level1_ink, ink, rd.sample_luminance(lum))
    for p in problems:
        print("PROBLEM:", p)
    out = {"ink_samples": int(ink.sum()), "regions": {}}
    for r in regions:
        mask = owner == rank[r.id]
        out["regions"][r.id] = {
            "d": rd.trace_samples(mask, l1["speck_size"]),
            "area": round(mask.sum() / rd.SAMPLES**2, 1),
        }
        print(r.id, "area", out["regions"][r.id]["area"])
    rest = getattr(signs, "STROKE_REST", None)
    if rest:
        region = owner == rank[signs.STROKE_REGION]
        out["rest"] = _stroke_rest(signs.STROKE, rest, region, w, h, l1["speck_size"])
    np.save(work / f"{prefix}-owner.npy", owner)
    with open(
        work / f"{prefix}-regions.json", "w", encoding="utf-8", newline="\n"
    ) as fp:
        json.dump(out, fp, ensure_ascii=False, indent=1)
        fp.write("\n")
    _picture(work, l1, out, w, h, prefix)


def _stroke_rest(stroke, rest, region, w, h, speck_size):
    """The stray stroke's region less the stroke, traced: those of its 4-connected
    pieces that reach farther than rest["reach"] pixels from the stroke, each grown
    rest["overlap"] pixels into the stroke, so that the two meet without a seam."""
    st = ct_share.shape_mask(dict(stroke, type="stroke"), w, h)
    left = region & ~st
    far = left & ~ct_share.near(st, rest["reach"])
    label, _n = raster.labels(left, 4)
    kept = np.isin(label, np.unique(label[far])) & (label > 0)
    grown = ct_share.near(kept, rest["overlap"]) & (kept | st)
    px = rd.SAMPLES**2
    sizes = np.bincount(label[left].ravel())
    print(
        "rest:",
        int((sizes > 0).sum()),
        "pieces outside the stroke;",
        "kept",
        [round(int(sizes[k]) / px, 1) for k in np.unique(label[far]).tolist()],
        "px",
    )
    return {
        "id": rest["id"],
        "d": rd.trace_samples(grown, speck_size),
        "area": round(grown.sum() / px, 1),
    }


def _picture(work, l1, out, w, h, prefix):
    scale = 3
    with Image.open(work / l1["image"]) as im:
        base = im.convert("RGB").resize(
            (w * scale, h * scale), Image.Resampling.BICUBIC
        )
    over = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(over)
    labels = []
    for k, (rid, reg) in enumerate(out["regions"].items()):
        colour = PALETTE[k % len(PALETTE)]
        for poly in geo.flatten(geo.parse_path(reg["d"])):
            pts = [(x * scale, y * scale) for x, y in poly]
            if len(pts) >= 3:
                draw.polygon(pts, fill=colour + (110,), outline=colour + (255,))
        polys = geo.flatten(geo.parse_path(reg["d"]))
        if polys:
            xs = [x for p in polys for x, _ in p]
            ys = [y for p in polys for _, y in p]
            labels.append((rid, min(xs) * scale, min(ys) * scale))
    pic = Image.alpha_composite(base.convert("RGBA"), over)
    draw = ImageDraw.Draw(pic)
    for rid, x, y in labels:
        draw.text((x, max(0, y - 11)), rid, fill=(0, 0, 0, 255))
    pic.convert("RGB").save(work / f"{prefix}-regions.png")
