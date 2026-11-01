"""Deriving a region-SVG's computed parts from its crop, and checking them.

Authored: the root's provenance and parameters; the judgments of level 1's
residual pieces and of fills that are not ink; the strips of supplied vellum;
the cuts; each region's id and seeds; each overlap's outline; each outline of
supplied ink, with whether and why it is supplied; and the groups, with whose
ink each is.  Derived: level 1's fills and image residual, exactly as a
stroke-SVG's are (pen_stroke.derive.derive_level1); each region's outline; each
overlap's ink; and each supplied outline's added ink.

The ink is level 1's as judged: the fills judged ink, less every residual piece
judged paper or damage, which is a hole the tracer filled, and then with every
piece judged ink, a speck the tracer dropped or faint ink; a piece judged
anything else, such as noise, leaves the fills as they are.  The regions come
from it in eight steps, at SAMPLES samples a pixel each way, so that they keep
level 1's smooth outlines:

1. the ink is rasterized, a sample being inside when its centre is, and every
   sample whose centre lies within half a strip of vellum's width of its line
   leaves it;
2. every sample that a cut's segments cross is set aside, each segment drawn as
   an 8-connected line of samples, so that no 4-connected path crosses it;
3. of the 4-connected pieces of ink that remain, each must hold a seed, and
   every seed must lie in one, except that a crumb, a piece that holds no seed
   and no more samples than the speck size, so that the tracer would drop it, is
   set aside as the cuts' samples are;
4. each seed moves to the darkest sample of its piece within SEED_REACH pixels,
   the first in row order on a tie;
5. the watershed: from all the seeds at once, the floods take the samples of
   each piece in order of the photograph's luminance, darkest first, a tie
   going to the sample reached first, each sample going to the seed whose flood
   reaches it first; the luminance at a sample is interpolated bilinearly
   between the centres of the crop's pixels;
6. each sample set aside goes back to the 4-adjacent region of lowest number,
   round after round, until none is left that touches a region;
7. each overlap takes the ink of step 1 inside its outline out of the regions,
   as one region of its own;
8. each region's and each overlap's samples are traced with level 1's tracer
   and speck size, and the outline is scaled to crop pixels.

A supplied outline's added ink is its samples less the ink's, traced the same
way, so that supplied ink never claims ink the image shows.  ``derive``
recomputes the derived parts and reports what the authored parts leave
unsettled; ``problems`` reports every way a file departs from the profile and
its crop.
"""

import heapq
import math
from dataclasses import replace
from pathlib import Path

import numpy as np

from pen_stroke import derive as dv
from pen_stroke import geometry as geo
from pen_stroke import level1
from pen_stroke import level5
from pen_stroke import raster
from pen_stroke import region_svg as rsvg
from pen_stroke import stroke_svg as ssvg

SAMPLES = 3
OUTLINE_PLACES = 3
# The judgments that take a residual piece's pixels out of the fills' ink.
NOT_INK = ("paper", "damage")
# How far, in crop pixels, a seed moves to the darkest ink of its piece.
SEED_REACH = 2


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


def sample_luminance(lum):
    """The photograph's luminance at each sample's centre, interpolated bilinearly
    between the centres of the crop's pixels, beyond which it is the edge pixel's,
    and multiplied by SAMPLES squared: whole numbers, exact on every machine."""
    lum = lum.astype(np.int64)

    def axis(n):
        # Sample i's centre lies (i + 0.5) / SAMPLES pixels from the edge, which is
        # (i - (SAMPLES - 1) / 2) / SAMPLES past the centre of pixel 0.
        off = np.arange(n * SAMPLES) - (SAMPLES - 1) // 2
        k = off // SAMPLES
        f = off - k * SAMPLES
        return np.clip(k, 0, n - 1), np.clip(k + 1, 0, n - 1), f

    y0, y1, fy = axis(lum.shape[0])
    x0, x1, fx = axis(lum.shape[1])
    fy, fx = fy[:, None], fx[None, :]
    top = (SAMPLES - fx) * lum[np.ix_(y0, x0)] + fx * lum[np.ix_(y0, x1)]
    bottom = (SAMPLES - fx) * lum[np.ix_(y1, x0)] + fx * lum[np.ix_(y1, x1)]
    return (SAMPLES - fy) * top + fy * bottom


def line_points(d, what):
    """The points, in crop pixels, of one path of straight segments, its first
    point again at the end if it is closed.  Anything else raises."""
    subpaths = geo.parse_path(d)
    if len(subpaths) != 1:
        raise ValueError(f"a {what} is one path of straight segments")
    start, segs, closed = subpaths[0]
    if not segs or any(s[0] != "L" for s in segs):
        raise ValueError(f"a {what} is one path of straight segments")
    pts = [start] + [s[1] for s in segs]
    return pts + [start] if closed else pts


def cut_points(cut):
    """A cut's points in crop pixels, its first point again at the end of a closed
    cut.  A cut that is not one path of straight segments raises."""
    return line_points(cut.d, "cut")


def vellum_points(v):
    """A strip of vellum's line in crop pixels.  A line that is not one open path of
    straight segments raises."""
    if any(closed for _, _, closed in geo.parse_path(v.d)):
        raise ValueError("a strip of vellum's line is open")
    return line_points(v.d, "strip of vellum's line")


def vellum_mask(v, width, height):
    """The samples whose centres lie within half the strip's width of its line."""
    cols, rows = width * SAMPLES, height * SAMPLES
    out = np.zeros((rows, cols), dtype=bool)
    half = v.width / 2
    pts = vellum_points(v)
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        lo_x = max(0, math.floor((min(ax, bx) - half) * SAMPLES))
        hi_x = min(cols, math.ceil((max(ax, bx) + half) * SAMPLES) + 1)
        lo_y = max(0, math.floor((min(ay, by) - half) * SAMPLES))
        hi_y = min(rows, math.ceil((max(ay, by) + half) * SAMPLES) + 1)
        if lo_x >= hi_x or lo_y >= hi_y:
            continue
        cx = (np.arange(lo_x, hi_x) + 0.5) / SAMPLES
        cy = (np.arange(lo_y, hi_y) + 0.5) / SAMPLES
        px, py = np.meshgrid(cx, cy)
        dx, dy = bx - ax, by - ay
        length2 = dx * dx + dy * dy
        if length2:
            t = np.clip(((px - ax) * dx + (py - ay) * dy) / length2, 0, 1)
        else:
            t = np.zeros_like(px)
        ex, ey = px - (ax + t * dx), py - (ay + t * dy)
        out[lo_y:hi_y, lo_x:hi_x] |= ex * ex + ey * ey <= half * half
    return out


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


def vellum_masks(rf):
    """Each well-formed strip of vellum's samples, by id."""
    out = {}
    for v in rf.vellum:
        try:
            out[v.id] = vellum_mask(v, rf.width, rf.height)
        except ValueError:
            continue
    return out


def _within_reach(seed, piece_label, label, slum):
    """The darkest sample of the piece within SEED_REACH pixels of the seed, the
    first in row order on a tie, as (row, column).  The test is exact: the seed is
    taken to its written hundredths of a pixel, and distances are whole numbers of
    600ths of a pixel."""
    sx, sy = (round(v * 100) for v in seed)
    reach = SEED_REACH * SAMPLES
    x, y = sample_of(seed)
    rows, cols = label.shape
    best = None
    for j in range(max(0, y - reach - 1), min(rows, y + reach + 2)):
        for i in range(max(0, x - reach - 1), min(cols, x + reach + 2)):
            if label[j, i] != piece_label:
                continue
            ex = 100 * (2 * i + 1) - 2 * SAMPLES * sx
            ey = 100 * (2 * j + 1) - 2 * SAMPLES * sy
            if ex * ex + ey * ey > (200 * SAMPLES * SEED_REACH) ** 2:
                continue
            key = (int(slum[j, i]), j, i)
            if best is None or key < best:
                best = key
    return best[1], best[2]


def flood(remaining, slum, starts):
    """The watershed: each sample of the remaining ink goes to the start whose
    flood reaches it first.  The starts, (rank, row, column), are taken first, in
    order, then the samples in order of luminance, darkest first, a tie going to
    the sample reached first; a sample is given its rank when it is reached."""
    rows, cols = remaining.shape
    free = remaining.ravel().tolist()
    lum = slum.ravel().tolist()
    rank = [0] * (rows * cols)
    heap = []
    n = 0
    for r, y, x in starts:
        i = y * cols + x
        rank[i] = r
        free[i] = False
        heap.append((-1, n, i))
        n += 1
    while heap:
        _, _, i = heapq.heappop(heap)
        r = rank[i]
        y, x = divmod(i, cols)
        for j in (
            i - cols if y else -1,
            i - 1 if x else -1,
            i + 1 if x + 1 < cols else -1,
            i + cols if y + 1 < rows else -1,
        ):
            if j >= 0 and free[j]:
                free[j] = False
                rank[j] = r
                heapq.heappush(heap, (lum[j], n, j))
                n += 1
    return np.array(rank, dtype=np.int32).reshape(rows, cols)


def settle(rf, level1_ink, ink, slum):
    """Which region each sample of ink belongs to, as an array of region ranks (0
    for none), each region's rank by id, and what the authored parts leave
    unsettled: steps 2 to 6 of this module's derivation, given the ink as level 1
    judges it and the ink of step 1."""
    problems = []
    rows, cols = ink.shape
    cut = np.zeros_like(ink)
    for cid, (ys, xs) in cut_cells(rf).items():
        if not ink[ys, xs].any():
            problems.append(f"{cid}: crosses no ink")
        cut[ys, xs] = True
    remaining = ink & ~cut
    label, n = raster.labels(remaining, 4)
    order = sorted(rf.regions, key=lambda r: rsvg.region_number(r.id))
    rank = {r.id: k for k, r in enumerate(order, 1)}
    starts = []
    taken = {}
    seeded = set()
    for r in order:
        for seed in r.seeds:
            x, y = sample_of(seed)
            where = f"{r.id}: its seed at {rsvg.seeds_text([seed])}"
            if not (0 <= x < cols and 0 <= y < rows) or not level1_ink[y, x]:
                problems.append(f"{where} lies outside the ink")
                continue
            if not ink[y, x]:
                problems.append(f"{where} lies in a strip of vellum")
                continue
            if cut[y, x]:
                problems.append(f"{where} lies on a cut")
                continue
            k = int(label[y, x])
            y, x = _within_reach(seed, k, label, slum)
            if (y, x) in taken:
                if taken[(y, x)] != r.id:
                    problems.append(
                        f"{where} moves to the sample that a seed of"
                        f" {taken[(y, x)]} moves to"
                    )
                continue
            taken[(y, x)] = r.id
            seeded.add(k)
            starts.append((rank[r.id], y, x))
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
    owner = flood(remaining, slum, starts)
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
            f"{_pixels(pending.sum())} pixels of ink under cuts or in crumbs touch no"
            " region"
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


def region_ink(rf, lum):
    """The ink of step 1, each sample's region by rank, each region's rank by id,
    each overlap's samples by id, and what the authored parts leave unsettled."""
    level1_ink = ink_samples(rf)
    ink = level1_ink.copy()
    problems = []
    for vid, mask in vellum_masks(rf).items():
        if not (mask & level1_ink).any():
            problems.append(f"{vid}: takes out no ink")
        ink &= ~mask
    owner, rank, found = settle(rf, level1_ink, ink, sample_luminance(lum))
    problems += found
    flooded = set(owner[owner > 0].tolist())
    overlaps = {}
    claimed = np.zeros_like(ink)
    for o in rf.overlaps:
        if not all(closed for _, _, closed in geo.parse_path(o.outline)):
            continue
        mask = scaled_mask([o.outline], rf.width, rf.height) & ink
        if not mask.any():
            problems.append(f"{o.id}: takes no ink")
        if (mask & claimed).any():
            problems.append(f"{o.id}: shares ink with another overlap")
        claimed |= mask
        owner[mask] = 0
        overlaps[o.id] = mask
    held = set(owner[owner > 0].tolist())
    for r in rf.regions:
        if rank[r.id] in flooded and rank[r.id] not in held:
            problems.append(f"{r.id}: overlaps take all its ink")
    return ink, owner, rank, overlaps, problems


def derive(rf, lum):
    """A copy of rf with every derived part recomputed from the crop's luminance,
    and what its authored parts leave unsettled."""
    out = dv.derive_level1(rf, lum)
    ink, owner, rank, overlap_masks, problems = region_ink(out, lum)
    held = set(owner[owner > 0].tolist())
    regions = []
    for r in rf.regions:
        d = ""
        if rank[r.id] in held:
            d = trace_samples(owner == rank[r.id], rf.speck_size)
            if not d:
                problems.append(f"{r.id}: its ink is too small to trace")
        regions.append(replace(r, d=d))
    overlaps = []
    for o in rf.overlaps:
        d = ""
        if o.id in overlap_masks and overlap_masks[o.id].any():
            d = trace_samples(overlap_masks[o.id], rf.speck_size)
            if not d:
                problems.append(f"{o.id}: its ink is too small to trace")
        overlaps.append(replace(o, ink=d))
    supplied = []
    for s in rf.supplied:
        added = scaled_mask([s.outline], rf.width, rf.height) & ~ink
        d = trace_samples(added, rf.speck_size)
        if not d:
            problems.append(f"{s.id}: adds no ink: its outline holds only ink")
        supplied.append(replace(s, added=d))
    out.regions = regions
    out.overlaps = overlaps
    out.supplied = supplied
    return out, problems


def vellum_ink(rf):
    """Each strip of vellum's ink, the ink as level 1 judges it that the strip
    takes out, as path data in crop pixels, by id: what the region page draws."""
    ink = ink_samples(rf)
    return {vid: trace_samples(m & ink, 0) for vid, m in vellum_masks(rf).items()}


def structural_problems(rf):
    """What the authored parts get wrong, whatever the crop."""
    out = []
    ids = [f.id for f in rf.fills] + [p.id for p in rf.pieces]
    ids += [v.id for v in rf.vellum] + [c.id for c in rf.cuts]
    ids += [r.id for r in rf.regions] + [o.id for o in rf.overlaps]
    ids += [s.id for s in rf.supplied] + [g.id for g in rf.groups]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        out.append(f"ids used more than once: {dupes}")
    regions = {r.id for r in rf.regions}
    overlaps = {o.id for o in rf.overlaps}
    members = regions | overlaps | {s.id for s in rf.supplied}
    held = {}
    for g in rf.groups:
        if not g.members:
            out.append(f"{g.id}: a group that holds nothing")
        for m in g.members:
            if m in members:
                held.setdefault(m, []).append(g.id)
            else:
                out.append(
                    f"{g.id}: refers to {m!r}, which is no region, overlap or supplied"
                    " ink of this file"
                )
        out += _parts_problems(g)
    ordered = [r.id for r in rf.regions] + [o.id for o in rf.overlaps]
    for i in ordered + [s.id for s in rf.supplied]:
        if i not in held:
            out.append(f"{i}: in no group")
        elif i in regions and len(held[i]) > 1:
            out.append(
                f"{i}: a region in {len(held[i])} groups, {' '.join(held[i])}; ink"
                " that signs share is an overlap"
            )
        elif i in overlaps and len(held[i]) < 2:
            out.append(f"{i}: an overlap that only {held[i][0]} holds")
    out += _ink_owner_problems(rf)
    for v in rf.vellum:
        try:
            vellum_points(v)
        except ValueError as exc:
            out.append(f"{v.id}: {exc}")
    for c in rf.cuts:
        try:
            cut_points(c)
        except ValueError as exc:
            out.append(f"{c.id}: {exc}")
    for o in rf.overlaps:
        if not all(closed for _, _, closed in geo.parse_path(o.outline)):
            out.append(f"{o.id}: its outline is not closed")
    for s in rf.supplied:
        if not all(closed for _, _, closed in geo.parse_path(s.outline)):
            out.append(f"{s.id}: its outline is not closed")
    for p in rf.pieces:
        if p.judged == "unjudged":
            out.append(f"{p.id}: residual piece not yet judged")
    return out


def _parts_problems(g):
    """The parts rule: a group whose kind has several written parts holds at least
    as many regions, overlaps and supplied inks, unless its data-parts-note says
    why it does not."""
    parts = level5.parts_of(g.kind)
    if parts is None or len(g.members) >= parts or g.parts_note:
        return []
    return [
        f"{g.id}: a {g.kind} has {parts} written parts, but the group holds"
        f" {len(g.members)} and no data-parts-note says why"
    ]


def _ink_owner_problems(rf):
    """What the groups' ink-of values get wrong (decision 17).  Unlike a stroke's,
    an overlap's groups may disagree on whose ink it is: ink that two lines share
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
            out.append(
                f"{old.id}: its outline is not what the seeds, cuts, vellum and"
                " overlaps give"
            )
    for old, new in zip(rf.overlaps, fresh.overlaps):
        if not dv.same_numbers(old.ink, new.ink):
            out.append(f"{old.id}: its ink is not the ink inside its outline")
    for old, new in zip(rf.supplied, fresh.supplied):
        if not dv.same_numbers(old.added, new.added):
            out.append(f"{old.id}: its added ink is not its outline less the ink")
    return out


def derive_file(svg_path):
    """Recompute the region-SVG's derived parts in place.  Whether it changed, and
    what its authored parts leave unsettled."""
    rf = rsvg.read(svg_path)
    lum = raster.load_luminance(dv.crop_path(svg_path, rf))
    fresh, found = derive(rf, lum)
    text = rsvg.dumps(fresh)
    changed = text != Path(svg_path).read_text(encoding="utf-8")
    if changed:
        rsvg.write(fresh, svg_path)
    return changed, found
