"""Deriving a region-SVG's computed parts from its crop, and checking them.

Authored: the root's provenance and parameters; the judgments of level 1's
residual pieces and of fills that are not ink; the cuts; each region's id and
seed; each outline of supplied ink, with whether and why it is supplied; and the
groups, with whose ink each is.  Derived: level 1's fills and image residual,
exactly as a stroke-SVG's are (pen_stroke.derive.derive_level1); each region's
outline; and each supplied outline's added ink.

The ink is level 1's as judged: the fills judged ink, less every residual piece
judged paper or damage, which is a hole the tracer filled, and then with every
piece judged ink, a speck the tracer dropped or faint ink; a piece judged
anything else, such as noise, leaves the fills as they are.  The regions come
from it in five
steps, at SAMPLES samples a pixel each way, so that they keep level 1's smooth
outlines:

1. the ink is rasterized, a sample being inside when its centre is;
2. every sample that a cut's segments cross is removed, each segment drawn as an
   8-connected line of samples, so that no 4-connected path crosses it;
3. of the 4-connected pieces of ink that remain, each must hold exactly one
   region's seed, and every seed must lie in one, except that a crumb, a piece
   that holds no seed and no more samples than the speck size, so that the
   tracer would drop it, is removed as the cuts' samples are;
4. each removed sample of ink goes back to the 4-adjacent region of lowest
   number, round after round, until none is left that touches a region;
5. each region's samples are traced with level 1's tracer and speck size, and
   the outline is scaled to crop pixels.

A supplied outline's added ink is its samples less the ink's, traced the same
way, so that supplied ink never claims ink the image shows.  ``derive``
recomputes the derived parts and reports what the cuts and seeds leave
unsettled; ``problems`` reports every way a file departs from the profile and
its crop.
"""

import math
from dataclasses import replace
from pathlib import Path

import numpy as np

from pen_stroke import derive as dv
from pen_stroke import geometry as geo
from pen_stroke import level1
from pen_stroke import raster
from pen_stroke import region_svg as rsvg
from pen_stroke import stroke_svg as ssvg

SAMPLES = 3
OUTLINE_PLACES = 3
# The judgments that take a residual piece's pixels out of the fills' ink.
NOT_INK = ("paper", "damage")


def scaled_mask(ds, width, height):
    """The samples, SAMPLES a pixel each way, whose centres lie inside the paths."""
    polys = [
        [(x * SAMPLES, y * SAMPLES) for x, y in p]
        for d in ds
        for p in geo.flatten(geo.parse_path(d))
    ]
    return geo.rasterize(polys, width * SAMPLES, height * SAMPLES, "nonzero")


def ink_samples(rf):
    """The ink as level 1 judges it, at SAMPLES samples a pixel: the fills judged
    ink, less the residual pieces judged paper or damage, with those judged ink."""
    w, h = rf.width, rf.height
    ink = scaled_mask(dv.ink_fill_ds(rf), w, h)
    not_ink = [p.d for p in rf.pieces if p.judged in NOT_INK]
    if not_ink:
        ink &= ~scaled_mask(not_ink, w, h)
    judged_ink = [p.d for p in rf.pieces if p.judged == "ink"]
    if judged_ink:
        ink |= scaled_mask(judged_ink, w, h)
    return ink


def cut_points(cut):
    """A cut's points in crop pixels, its first point again at the end of a closed
    cut.  A cut that is not one path of straight segments raises."""
    subpaths = geo.parse_path(cut.d)
    if len(subpaths) != 1:
        raise ValueError("a cut is one path of straight segments")
    start, segs, closed = subpaths[0]
    if not segs or any(s[0] != "L" for s in segs):
        raise ValueError("a cut is one path of straight segments")
    pts = [start] + [s[1] for s in segs]
    return pts + [start] if closed else pts


def sample_of(pt):
    """The sample, (column, row), whose square holds a point given in crop pixels."""
    return (math.floor(pt[0] * SAMPLES), math.floor(pt[1] * SAMPLES))


def _line(a, b):
    """The samples, (column, row), of the 8-connected digital line from a to b."""
    (x0, y0), (x1, y1) = a, b
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    out = [(x0, y0)]
    while (x0, y0) != (x1, y1):
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
        out.append((x0, y0))
    return out


def cut_cells(rf):
    """Each well-formed cut's samples within the crop, as (rows, columns), by id."""
    cols, rows = rf.width * SAMPLES, rf.height * SAMPLES
    out = {}
    for c in rf.cuts:
        try:
            cells = [sample_of(p) for p in cut_points(c)]
        except ValueError:
            continue
        line = {cells[0]}
        for a, b in zip(cells, cells[1:]):
            line.update(_line(a, b))
        inside = sorted((y, x) for x, y in line if 0 <= x < cols and 0 <= y < rows)
        out[c.id] = (
            np.array([y for y, _ in inside], dtype=np.intp),
            np.array([x for _, x in inside], dtype=np.intp),
        )
    return out


def settle(rf, ink):
    """Which region each sample of ink belongs to, as an array of region numbers
    by rank (0 for none), each region's rank by id, and what the cuts and seeds
    leave unsettled: steps 2 to 4 of this module's derivation."""
    problems = []
    rows, cols = ink.shape
    cut = np.zeros_like(ink)
    for cid, (ys, xs) in cut_cells(rf).items():
        if not ink[ys, xs].any():
            problems.append(f"{cid}: crosses no ink")
        cut[ys, xs] = True
    label, n = raster.labels(ink & ~cut, 4)
    order = sorted(rf.regions, key=lambda r: rsvg.region_number(r.id))
    rank = {r.id: k for k, r in enumerate(order, 1)}
    owner_of = np.zeros(n + 1, dtype=np.int32)
    seeded = {}
    for r in rf.regions:
        x, y = sample_of(r.seed)
        if not (0 <= x < cols and 0 <= y < rows) or not ink[y, x]:
            problems.append(f"{r.id}: its seed lies outside the ink")
            continue
        k = int(label[y, x])
        if cut[y, x]:
            problems.append(f"{r.id}: its seed lies on a cut")
        elif k in seeded:
            problems.append(
                f"{r.id}: its seed lies in the same piece of ink as {seeded[k]}'s"
            )
        else:
            seeded[k] = r.id
            owner_of[k] = rank[r.id]
    flat = label.ravel()
    sizes = np.bincount(flat, minlength=n + 1)
    pieces, first = np.unique(flat, return_index=True)
    crumbs = []
    for k, i in zip(pieces.tolist(), first.tolist()):
        if not k or k in seeded:
            continue
        if sizes[k] <= rf.speck_size:
            crumbs.append(k)
            continue
        y, x = divmod(i, cols)
        problems.append(
            f"{_pixels(sizes[k])} pixels of ink from ({_px(x)}, {_px(y)}) hold no"
            " region's seed"
        )
    owner = owner_of[label]
    pending = (ink & cut) | np.isin(label, crumbs)
    none = len(order) + 1
    while pending.any():
        held = np.where(owner > 0, owner, none)
        near = np.full(ink.shape, none, dtype=np.int32)
        near[1:, :] = np.minimum(near[1:, :], held[:-1, :])
        near[:-1, :] = np.minimum(near[:-1, :], held[1:, :])
        near[:, 1:] = np.minimum(near[:, 1:], held[:, :-1])
        near[:, :-1] = np.minimum(near[:, :-1], held[:, 1:])
        take = pending & (near < none)
        if not take.any():
            break
        owner[take] = near[take]
        pending &= ~take
    if pending.any():
        problems.append(
            f"{_pixels(pending.sum())} pixels of ink lie under cuts and touch no region"
        )
    return owner, rank, problems


def _px(sample):
    return geo.fmt(sample / SAMPLES, 1)


def _pixels(samples):
    return geo.fmt(samples / SAMPLES**2, 1)


def trace_samples(mask, speck_size):
    """Path data, in crop pixels, for samples that level 1's tracer traces."""
    ys, xs = np.nonzero(mask)
    if not len(ys):
        return ""
    y0, x0 = int(ys.min()), int(xs.min())
    sub = np.zeros((int(ys.max()) - y0 + 3, int(xs.max()) - x0 + 3), dtype=bool)
    sub[ys - y0 + 1, xs - x0 + 1] = True
    subpaths = [
        _to_crop(sp, x0 - 1, y0 - 1)
        for comp in level1.trace_fills(sub, speck_size)
        for sp in comp
    ]
    return geo.format_path(subpaths, OUTLINE_PLACES)


def _to_crop(subpath, dx, dy):
    def f(p):
        return ((p[0] + dx) / SAMPLES, (p[1] + dy) / SAMPLES)

    start, segs, closed = subpath
    return (f(start), [(s[0],) + tuple(f(p) for p in s[1:]) for s in segs], closed)


def derive(rf, lum):
    """A copy of rf with every derived part recomputed from the crop's luminance,
    and what its cuts and seeds leave unsettled."""
    out = dv.derive_level1(rf, lum)
    ink = ink_samples(out)
    owner, rank, problems = settle(out, ink)
    seeded = set(owner[owner > 0].tolist())
    regions = []
    for r in rf.regions:
        d = ""
        if rank[r.id] in seeded:
            d = trace_samples(owner == rank[r.id], rf.speck_size)
            if not d:
                problems.append(f"{r.id}: its ink is too small to trace")
        regions.append(replace(r, d=d))
    supplied = []
    for s in rf.supplied:
        added = scaled_mask([s.outline], rf.width, rf.height) & ~ink
        d = trace_samples(added, rf.speck_size)
        if not d:
            problems.append(f"{s.id}: adds no ink: its outline holds only ink")
        supplied.append(replace(s, added=d))
    out.regions = regions
    out.supplied = supplied
    return out, problems


def structural_problems(rf):
    """What the authored parts get wrong, whatever the crop."""
    out = []
    ids = [f.id for f in rf.fills] + [p.id for p in rf.pieces]
    ids += [c.id for c in rf.cuts] + [r.id for r in rf.regions]
    ids += [s.id for s in rf.supplied] + [g.id for g in rf.groups]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        out.append(f"ids used more than once: {dupes}")
    members = {r.id for r in rf.regions} | {s.id for s in rf.supplied}
    grouped = set()
    for g in rf.groups:
        if not g.members:
            out.append(f"{g.id}: a group that holds nothing")
        for m in g.members:
            if m in members:
                grouped.add(m)
            else:
                out.append(
                    f"{g.id}: refers to {m!r}, which is no region or supplied ink"
                    " of this file"
                )
    for i in [r.id for r in rf.regions] + [s.id for s in rf.supplied]:
        if i not in grouped:
            out.append(f"{i}: in no group")
    out += _ink_owner_problems(rf)
    for c in rf.cuts:
        try:
            cut_points(c)
        except ValueError as exc:
            out.append(f"{c.id}: {exc}")
    for s in rf.supplied:
        if not all(closed for _, _, closed in geo.parse_path(s.outline)):
            out.append(f"{s.id}: its outline is not closed")
    for p in rf.pieces:
        if p.judged == "unjudged":
            out.append(f"{p.id}: residual piece not yet judged")
    return out


def _ink_owner_problems(rf):
    """What the groups' ink-of values get wrong (decision 17).  Unlike a stroke's,
    a region's groups may disagree on whose ink it is: ink that two lines share
    is how a collision between them is proposed."""
    out = []
    me = ssvg.subject(rf)
    allowed = {me, "line-above", "line-below"}
    if me == ssvg.THIS_WORD:
        allowed.add("other-word")
    for g in rf.groups:
        if g.ink_of not in allowed:
            out.append(f"{g.id}: ink of {g.ink_of!r} in a crop whose subject is {me!r}")
    used = {g.ink_of for g in rf.groups}
    for side in ("line-above", "line-below"):
        if side in used and side not in rf.provenance:
            out.append(f"ink of the {side.replace('-', ' ')} but no data-{side} text")
    return out


def problems(svg_path):
    """Every way the region-SVG at svg_path departs from the profile and its crop."""
    try:
        rf = rsvg.read(svg_path)
    except ValueError as exc:
        return [str(exc)]
    out = structural_problems(rf)
    png = dv.crop_path(svg_path, rf)
    if not png.exists():
        return out + [f"crop {png.name} does not exist"]
    lum = raster.load_luminance(png)
    try:
        fresh, found = derive(rf, lum)
    except ValueError as exc:
        return out + [str(exc)]
    out += dv.level1_problems(rf, fresh)
    out += found
    for old, new in zip(rf.regions, fresh.regions):
        if not dv.same_numbers(old.d, new.d):
            out.append(f"{old.id}: its outline is not what its seed and the cuts give")
    for old, new in zip(rf.supplied, fresh.supplied):
        if not dv.same_numbers(old.added, new.added):
            out.append(f"{old.id}: its added ink is not its outline less the ink")
    return out


def derive_file(svg_path):
    """Recompute the region-SVG's derived parts in place.  Whether it changed, and
    what its cuts and seeds leave unsettled."""
    rf = rsvg.read(svg_path)
    lum = raster.load_luminance(dv.crop_path(svg_path, rf))
    fresh, found = derive(rf, lum)
    text = rsvg.dumps(fresh)
    changed = text != Path(svg_path).read_text(encoding="utf-8")
    if changed:
        rsvg.write(fresh, svg_path)
    return changed, found
