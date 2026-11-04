"""How heavy the shapes are: each region's area at a threshold against its ink.

Written for the concrete-transcription trial, 2026-11-04.  Usage, from the
MAM-basics clone's root:

    ./.venv/Scripts/python.exe py/main_concrete_transcription.py area
        <work-dir> <prefix> [<reach>]

Ben, 2026-11-04: the clean page's strokes look heavier than the image's, the
level-1 boundary lying out in each edge's fade; a dot's apparent area is more
like the sum of its intensity than the area inside that boundary (R19 of
doc/PLAN-ink-regions.md, area preserved); and the fade is likely widened by the
JPEG's ringing.  For each region of the draft named by <prefix>: its pixels (its
owner at each pixel's centre), and its neighbourhood, the pixels within REACH px
of them nearer to them than to any other region's; the vellum level V about it,
the median of the pixels between RING_IN and RING_OUT px from it that lie at least
RING_IN px from all ink; K, the ink level, the median of the pixels at least two
px inside the ink; its deposited ink, the sum over its neighbourhood of
(V - lum) / (V - K), not clamped, so that ringing's light and dark halves cancel;
its area at the level-1 threshold; and the threshold at which its area equals its
deposited ink.  The same in linear light, for comparison.
"""

import json

import numpy as np
from PIL import Image

REACH = 4
RING_IN, RING_OUT = 6, 10


def srgb_to_linear(v):
    c = v / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def neighbours8(a, fill):
    """The eight shifted copies of a, padded with fill."""
    p = np.pad(a, 1, constant_values=fill)
    h, w = a.shape
    return [
        p[1 + dy : 1 + dy + h, 1 + dx : 1 + dx + w]
        for dy in (-1, 0, 1)
        for dx in (-1, 0, 1)
        if dy or dx
    ]


def grow_labels(labels, steps):
    """Each unlabelled pixel within `steps` 8-steps of a label takes the least label
    of its labelled neighbours, step by step; and each pixel's step (0 on a label)."""
    lab = labels.copy()
    dist = np.where(lab > 0, 0, -1)
    big = np.iinfo(np.int32).max
    for k in range(1, steps + 1):
        cand = np.full(lab.shape, big, dtype=np.int64)
        for n in neighbours8(np.where(lab > 0, lab, big), big):
            cand = np.minimum(cand, n)
        take = (lab == 0) & (cand < big)
        lab[take] = cand[take]
        dist[take] = k
    return lab, dist


def distance_steps(mask, steps):
    """Each pixel's 8-step distance from mask, up to steps; steps + 1 beyond."""
    d = np.where(mask, 0, steps + 1)
    cur = mask.copy()
    for k in range(1, steps + 1):
        grown = cur.copy()
        for n in neighbours8(cur, False):
            grown |= n
        d[grown & ~cur] = k
        cur = grown
    return d


def erode(mask, times):
    for _ in range(times):
        out = mask.copy()
        for n in neighbours8(mask, False):
            out &= n
        mask = out
    return mask


def equal_area_threshold(values, deposited):
    """The least integer threshold t at which the count of values below t reaches
    the deposited ink."""
    for t in range(0, 257):
        if (values < t).sum() >= deposited:
            return t
    return 256


def run(work, prefix, reach):
    l1 = json.loads((work / "level1.json").read_text(encoding="utf-8"))
    regions = json.loads((work / f"{prefix}-regions.json").read_text(encoding="utf-8"))
    owner = np.load(work / f"{prefix}-owner.npy")
    with Image.open(work / l1["image"]) as im:
        lum = np.asarray(im.convert("L"), dtype=np.float64)
    t1 = l1["threshold"]
    ink = lum < t1
    order = sorted(regions["regions"], key=lambda rid: int(rid.removeprefix("rg")))
    ids = dict(enumerate(order, 1))
    pix = owner[1::3, 1::3].astype(np.int64) * ink
    hood, _ = grow_labels(pix, reach)
    print(f"neighbourhood reach {reach} px")
    from_ink = distance_steps(ink, RING_OUT)
    core = erode(ink, 2)
    K = float(np.median(lum[core]))
    lin = srgb_to_linear(lum)
    K_lin = float(np.median(lin[core]))
    print(
        f"level-1 threshold {t1}; K, the ink level, {K:.1f} (linear {K_lin:.4f});"
        f" core pixels {int(core.sum())}"
    )
    print(
        f"{'id':5} {'region':28} {'area@t1':>8} {'deposit':>8} {'ratio':>6}"
        f" {'t_eq':>5} {'V':>6} {'t_eq lin':>9}"
    )
    rows = []
    for rank, rid in ids.items():
        own = pix == rank
        if not own.any():
            continue
        dist = distance_steps(own, RING_OUT)
        ring = (dist >= RING_IN) & (dist <= RING_OUT) & (from_ink >= RING_IN)
        if ring.sum() < 20:
            ring = (dist >= RING_IN) & (dist <= RING_OUT) & ~ink
        V = float(np.median(lum[ring]))
        V_lin = float(np.median(lin[ring]))
        hd = hood == rank
        deposit = float(((V - lum[hd]) / (V - K)).sum())
        deposit_lin = float(((V_lin - lin[hd]) / (V_lin - K_lin)).sum())
        area = int((lum[hd] < t1).sum())
        t_eq = equal_area_threshold(lum[hd], deposit)
        # in linear light, the threshold that gives the linear deposit, as a lum value
        t_eq_lin = equal_area_threshold(lum[hd], deposit_lin)
        rows.append((rid, area, deposit, t_eq, V, t_eq_lin))
        print(
            f"{rid:5} {regions['regions'][rid].get('label', ''):28} {area:8d} {deposit:8.1f}"
            f" {deposit / area:6.2f} {t_eq:5d} {V:6.1f} {t_eq_lin:9d}"
        )
    tot_area = sum(r[1] for r in rows)
    tot_dep = sum(r[2] for r in rows)
    print(
        f"all regions: area at t1 {tot_area}, deposited {tot_dep:.0f},"
        f" ratio {tot_dep / tot_area:.2f}"
    )
    allhood = np.isin(
        hood, [rank for rank, rid in ids.items() if rid in {r[0] for r in rows}]
    )
    print(
        "a global threshold with the same total area:",
        equal_area_threshold(lum[allhood], tot_dep),
    )
    dots = [r for r in rows if r[1] < 300]
    print(
        f"dots and small marks ({len(dots)}): area at t1 {sum(r[1] for r in dots)},"
        f" deposited {sum(r[2] for r in dots):.0f}"
    )
    for t in (90, 100, 110, 120, 125, 130, 135):
        print(
            f"  total area below {t}: {int((lum[allhood] < t).sum())}"
            f" ({(lum[allhood] < t).sum() / tot_dep:.2f} of the deposited ink)"
        )
