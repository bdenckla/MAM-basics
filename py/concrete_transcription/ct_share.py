"""How a set of the trial's shapes shares out the ink: masks and counts.

Written for the concrete-transcription trial, 2026-11-03.  Every shape is
rasterized at rd.SAMPLES samples a pixel, from its path data `d` when it has one
(an edited shape, exactly as the page drew it), else from ct_geometry.shape_d.
Nearness is measured as the page measures it, by distance: ink whose sample's
centre lies within NEAR pixels of a shape's sample is that shape's blur.  (The
eight-neighbour dilation of ct_shapes.py reaches farther along the diagonals,
and missed a hairline of red that the page shows.)
"""

import math
from types import SimpleNamespace

import numpy as np

from pen_stroke import geometry as geo
from pen_stroke import region_derive as rd
from concrete_transcription import ct_geometry as ctg
from concrete_transcription import ct_signs

S = rd.SAMPLES
NEAR = 1.3  # pixels: ink this near a shape is the shape's blur, as the page counts


def vellum_strips(signs):
    """A draft's strips of vellum (its VELLUM, if any), as region_derive takes them."""
    return [
        SimpleNamespace(id=vid, d=d, width=width)
        for vid, d, width, _why in getattr(signs, "VELLUM", [])
    ]


def strips_mask(signs, w, h):
    """The samples that a draft's strips of vellum take out of the ink, or None."""
    strips = vellum_strips(signs)
    if not strips:
        return None
    out = np.zeros((h * S, w * S), dtype=bool)
    for v in strips:
        out |= rd.vellum_mask(v, w, h)
    return out


def ink_mask(l1, signs=None):
    """Level 1's fills and the residual pieces judged ink, at S samples a pixel,
    less the samples of the draft's strips of vellum."""
    w, h = l1["width"], l1["height"]
    ink = rd.scaled_mask([f["d"] for f in l1["fills"]], w, h)
    pieces = {p["id"]: p for p in l1["pieces"]}
    for pid, (judged, _why) in ct_signs.JUDGMENTS.items():
        if judged == "ink":
            ink |= rd.scaled_mask([pieces[pid]["d"]], w, h)
    strips = strips_mask(signs, w, h)
    if strips is not None:
        ink &= ~strips
    return ink


def shape_d(shape):
    return shape.get("d") or ctg.shape_d(shape)


def shape_mask(shape, w, h):
    polys = [
        [(x * S, y * S) for x, y in p]
        for p in geo.flatten(geo.parse_path(shape_d(shape)))
    ]
    rule = "evenodd" if shape["type"] == "outline" else "nonzero"
    return geo.rasterize(polys, w * S, h * S, rule)


def near(mask, pixels=NEAR):
    """Every sample whose centre lies within `pixels` of a sample of mask."""
    radius = pixels * S
    r = math.floor(radius)
    rows, cols = mask.shape
    out = mask.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if (dx or dy) and dx * dx + dy * dy <= radius * radius:
                out[
                    max(dy, 0) : rows + min(dy, 0), max(dx, 0) : cols + min(dx, 0)
                ] |= mask[
                    max(-dy, 0) : rows + min(-dy, 0), max(-dx, 0) : cols + min(-dx, 0)
                ]
    return out


def share_out(ink, masks):
    """How the shapes' masks share out the ink, in pixels; and the per-sample
    count of shapes, and the samples within NEAR of a shape."""
    px = S * S
    count = np.zeros(ink.shape, dtype=np.int32)
    for m in masks.values():
        count += m
    near_any = near(count > 0)
    ink_near = near(ink)
    out = {
        "ink": ink.sum() / px,
        "in_no_shape": (ink & (count == 0)).sum() / px,
        "unexplained": (ink & ~near_any).sum() / px,
        "in_two_or_more": (ink & (count >= 2)).sum() / px,
        "overlaps": {},
        "beyond_ink": {},
    }
    ids = list(masks)
    for i, a in enumerate(ids):
        for b in ids[i + 1 :]:
            both = (ink & masks[a] & masks[b]).sum()
            if both:
                out["overlaps"][f"{a} & {b}"] = both / px
    for sid, m in masks.items():
        beyond = (m & ~ink_near).sum()
        if beyond > px:
            out["beyond_ink"][sid] = beyond / px
    return out, count, near_any


def print_share(title, out):
    r = lambda v: round(v, 1)  # noqa: E731
    print(title)
    print(
        "  ink",
        r(out["ink"]),
        "px; in no shape",
        r(out["in_no_shape"]),
        "of which farther than 1.3 px from every shape",
        r(out["unexplained"]),
        "; in two shapes or more",
        r(out["in_two_or_more"]),
    )
    for pair, v in out["overlaps"].items():
        print(f"  overlap {pair}: {r(v)} px of ink")
    for sid, v in out["beyond_ink"].items():
        print(f"  {sid} reaches more than 1.3 px beyond the ink: {r(v)} px")
