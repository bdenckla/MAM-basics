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
way, so that supplied ink never claims ink the image shows.

Profile 3 takes those eight steps as its draft, and then each glyph's outline,
the library's glyph placed by its fit, at the same samples:

9. each glyph's outline is rasterized by the nonzero rule;
10. a 4-connected piece of the ink inside two glyphs or more is an overlap if
    some sample of it lies deeper than OVERLAP_DEPTH inside each of two of them;
    otherwise the glyphs only touch there, and each of its samples goes to the
    glyph it lies deepest inside, the lower group number and then the earlier
    part on a tie;
11. the rest of the ink inside one glyph is that glyph's;
12. each region keeps the ink the draft gave it that lies inside no glyph: an
    unfitted group's region its ink, and a fitted group's region what its
    glyphs leave of its draft, overfill within NEAR samples of a glyph and
    unexplained ink farther away;
13. each glyph's ink, each overlap of glyphs and each region is traced.

Profile 4 derives as profile 3 does, under the guidelines of the font of the
manuscript's shapes: a mark's glyph is drawn, a letter's outline is moved along
its normal by the distance its fit gives, and a group or a glyph may break a
guideline.

``derive`` recomputes the derived parts and reports what the authored parts
leave unsettled; ``problems`` reports every way a file departs from the profile
and its crop.  ``fit_file`` runs the fit (pen_stroke.glyph_fit), which writes a
crop's glyphs and moves it to profile 4; ``library_derive_file`` and
``library_problems`` derive and check the library of glyphs.
"""

import hashlib
import heapq
import math
from dataclasses import replace
from pathlib import Path

import numpy as np
from PIL import Image

from pen_stroke import derive as dv
from pen_stroke import geometry as geo
from pen_stroke import glyph_fit as gf
from pen_stroke import glyph_library as glib
from pen_stroke import level1
from pen_stroke import level5
from pen_stroke import raster
from pen_stroke import region_svg as rsvg
from pen_stroke import stroke_svg as ssvg

SAMPLES = 3
if gf.SAMPLES != SAMPLES:
    raise ValueError("the fit and the derivation sample the ink alike")
OUTLINE_PLACES = 3
# The judgments that take a residual piece's pixels out of the fills' ink.
NOT_INK = ("paper", "damage")
# How far, in crop pixels, a seed moves to the darkest ink of its piece.
SEED_REACH = 2
# Profile 3: how deep, in crop pixels, ink must lie inside two glyphs for them to
# overlap there rather than touch; set in phase 8 of doc/PLAN-ink-regions.md from
# Ben's readings of page F043A's two crops, between the depth of the geresh's and
# the tav's touch, 0.64, and of line 23's lamed's head in the mem, 4.80, and above
# a qamats's bar's and dot's, 1.04.
OVERLAP_DEPTH = 1.5
# Ink inside no glyph is overfill within this many samples of a glyph, in
# 8-connected steps (about 1.3 crop pixels), and unexplained farther away.
NEAR = 4
# How far, in crop pixels, a strip of vellum or a cut may run inside a glyph.
LINE_CROSSING = 1.0
# Unexplained ink is listed by pieces of at least this many samples (1 pixel).
UNEXPLAINED_PIECE = SAMPLES * SAMPLES


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


def derive(rf, lum, library=None):
    """A copy of rf with every derived part recomputed from the crop's luminance,
    and what its authored parts leave unsettled; and, for a profile-3 file, which
    needs the library of glyphs, the result of its steps 9 to 13."""
    out = dv.derive_level1(rf, lum)
    ink, owner, rank, overlap_masks, problems = region_ink(out, lum)
    fitted = None
    if rf.profile in rsvg.FITTED:
        fitted = glyph_ink(out, ink, owner, rank, overlap_masks, library)
        problems += fitted.problems
    held = set(owner[owner > 0].tolist())
    regions = []
    for r in rf.regions:
        d = ""
        if rank[r.id] in held:
            mask = owner == rank[r.id]
            if fitted is None:
                d = trace_samples(mask, rf.speck_size)
                if not d:
                    problems.append(f"{r.id}: its ink is too small to trace")
            else:
                d = fitted.left_trace(r.id, mask, rf.speck_size, problems)
        regions.append(replace(r, d=d))
    overlaps = []
    for o in rf.overlaps:
        d = ""
        if o.id in overlap_masks and overlap_masks[o.id].any():
            if fitted is None:
                d = trace_samples(overlap_masks[o.id], rf.speck_size)
                if not d:
                    problems.append(f"{o.id}: its ink is too small to trace")
            else:
                d = fitted.left_trace(
                    o.id, overlap_masks[o.id], rf.speck_size, problems
                )
        overlaps.append(replace(o, ink=d))
    if fitted is not None:
        out.glyphs = fitted.glyphs
        out.glyph_overlaps = fitted.glyph_overlaps
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
    return out, problems, fitted


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
    ids += [gl.id for gl in rf.glyphs] + [o.id for o in rf.glyph_overlaps]
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


def library_for(svg_path):
    """The library of glyphs beside a region-SVG."""
    return glib.read(glib.library_path(Path(svg_path).parent))


def check(svg_path):
    """Every way the region-SVG at svg_path departs from the profile and its crop;
    and what the check lists without failing: a fitted file's unexplained ink and
    its groups of a fitted kind that are not fitted, and a profile-4 file's
    breaks of the guidelines."""
    try:
        rf = rsvg.read(svg_path)
    except ValueError as exc:
        return [str(exc)], []
    out = structural_problems(rf)
    png = dv.crop_path(svg_path, rf)
    if not png.exists():
        return out + [f"crop {png.name} does not exist"], []
    lum = raster.load_luminance(png)
    library = None
    if rf.profile in rsvg.FITTED:
        try:
            library = library_for(svg_path)
        except (OSError, ValueError) as exc:
            return out + [f"the library of glyphs: {exc}"], []
        if rf.profile == rsvg.PROFILE_4 and not library.drawn:
            return (
                out
                + [
                    f"a file of profile {rsvg.PROFILE_4!r} needs the library's profile"
                    f" {glib.PROFILE!r}"
                ],
                [],
            )
    try:
        fresh, found, fitted = derive(rf, lum, library)
    except ValueError as exc:
        return out + [str(exc)], []
    out += dv.level1_problems(rf, fresh)
    out += found
    for old, new in zip(rf.regions, fresh.regions):
        if not dv.same_numbers(old.d, new.d):
            out.append(
                f"{old.id}: its outline is not what the seeds, cuts, vellum,"
                " overlaps and glyphs give"
            )
    for old, new in zip(rf.overlaps, fresh.overlaps):
        if not dv.same_numbers(old.ink, new.ink):
            out.append(f"{old.id}: its ink is not the ink inside its outline")
    for old, new in zip(rf.supplied, fresh.supplied):
        if not dv.same_numbers(old.added, new.added):
            out.append(f"{old.id}: its added ink is not its outline less the ink")
    notes = []
    if fitted is not None:
        out += _glyph_problems(rf, fresh)
        notes = fitted.notes
    if rf.profile == rsvg.PROFILE_4:
        found, listed = guideline_problems(rf, library)
        out += found
        notes = listed + notes
    return out, notes


def problems(svg_path):
    """Every way the region-SVG at svg_path departs from the profile and its crop."""
    return check(svg_path)[0]


def guideline_problems(rf, library):
    """A profile-4 file's breaks of the guidelines: what is wrong with each, and
    each listed as a note; and where a glyph departs from a guideline that
    neither it nor its group breaks: a mark's glyph that is not drawn where its
    part has a drawn shape, a glyph of the scribe's that serves only a group that
    breaks preserved, and a letter's distance along its outline's normal beyond
    its limit, or other than 0 where it breaks area."""
    out, notes = [], []
    for g in rf.groups:
        found, wrong = glib.parse_breaks(g.brk)
        out += [f"{g.id}: {p}" for p in wrong]
        notes += [f"{g.id} ({g.kind}) breaks {name}: {why}" for name, why in found]
    groups = {g.id: g for g in rf.groups}
    sources = library.by_id()
    for gl in rf.glyphs:
        found, wrong = glib.parse_breaks(gl.brk)
        out += [f"{gl.id}: {p}" for p in wrong]
        notes += [
            f"{gl.id}, of {gl.group}, breaks {name}: {why}" for name, why in found
        ]
        g, src = groups.get(gl.group), sources.get(gl.glyph)
        if g is None or src is None:
            # place_glyphs already reports the invalid reference.
            continue
        breaks = glyph_breaks(gl, g)
        part = next((p for p in glib.entry_of(g.kind).parts if p.name == gl.part), None)
        if part is not None and part.shape and not src.is_drawn:
            if glib.DRAWN_MARKS not in breaks:
                out.append(
                    f"{gl.id}: its glyph {src.id} is not drawn, and neither it nor"
                    f" {g.id} breaks {glib.DRAWN_MARKS}"
                )
        if src.is_scribes and src.unjudged and glib.PRESERVED not in breaks:
            out.append(
                f"{gl.id}: its glyph {src.id} is not judged well preserved, and"
                f" neither it nor {g.id} breaks {glib.PRESERVED}"
            )
        if level5.pass_of(g.kind) == level5.LETTERS and len(gl.fit) in gf.LETTER_FIT_4:
            offset = gl.fit[-1]
            if abs(offset) > gf.OFFSET_LIMIT:
                out.append(
                    f"{gl.id}: its outline moves {geo.fmt(offset, 4)} pixels along its"
                    f" normal, beyond {geo.fmt(gf.OFFSET_LIMIT, 2)}"
                )
            if glib.AREA in breaks and offset:
                out.append(
                    f"{gl.id}: it breaks {glib.AREA}, but its outline moves along its"
                    " normal"
                )
    return out, notes


def _glyph_problems(rf, fresh):
    """Where a fitted file's derived glyphs and overlaps of glyphs differ from
    what derivation gives."""
    out = []
    for old, new in zip(rf.glyphs, fresh.glyphs):
        if not dv.same_numbers(old.outline, new.outline):
            out.append(
                f"{old.id}: its outline is not what its glyph {old.glyph} and its fit"
                " give: if the library's glyph has changed since the fit, fit this"
                " crop again"
            )
        if not dv.same_numbers(old.ink, new.ink):
            out.append(f"{old.id}: its ink is not what the glyphs give")
    old_o = [(o.id, o.glyphs) for o in rf.glyph_overlaps]
    new_o = [(o.id, o.glyphs) for o in fresh.glyph_overlaps]
    if old_o != new_o:
        out.append("the overlaps of glyphs are not those the glyphs give")
    else:
        for old, new in zip(rf.glyph_overlaps, fresh.glyph_overlaps):
            if not dv.same_numbers(old.d, new.d):
                out.append(f"{old.id}: its ink is not what the glyphs give")
    return out


def derive_file(svg_path):
    """Recompute the region-SVG's derived parts in place.  Whether it changed, and
    what its authored parts leave unsettled.  A profile-3 file whose glyphs'
    outlines would change, since the library's glyphs have changed since its fit,
    is left as it is, to be fitted again."""
    rf = rsvg.read(svg_path)
    lum = raster.load_luminance(dv.crop_path(svg_path, rf))
    library = library_for(svg_path) if rf.profile in rsvg.FITTED else None
    fresh, found, _ = derive(rf, lum, library)
    stale = [
        old.id
        for old, new in zip(rf.glyphs, fresh.glyphs)
        if old.outline and not dv.same_numbers(old.outline, new.outline)
    ]
    if stale:
        return False, found + [
            f"not written: the outlines of {', '.join(stale)} would change, since"
            " the library's glyphs have changed since the fit; fit this crop again"
        ]
    text = rsvg.dumps(fresh)
    changed = text != Path(svg_path).read_text(encoding="utf-8")
    if changed:
        rsvg.write(fresh, svg_path)
    return changed, found


# ---------------------------------------------------------------- profile 3


def draft_masks(rf, lum):
    """The draft, profile 2's derivation of the file as it is: the ink of step 1,
    each region's and each overlap's samples by id, and what the authored parts
    leave unsettled."""
    ink, owner, rank, overlaps, found = region_ink(rf, lum)
    masks = {r.id: owner == rank[r.id] for r in rf.regions}
    masks.update(overlaps)
    return ink, masks, found


def _order_regions(order, regs, masks):
    """A group's regions in the order of its kind's written parts."""
    rows = {r: np.nonzero(masks[r])[0].mean() for r in regs}
    cols = {r: np.nonzero(masks[r])[1].mean() for r in regs}
    if order == glib.TOP_TO_BOTTOM:
        return sorted(regs, key=lambda r: rows[r])
    if order == glib.RIGHT_TO_LEFT:
        return sorted(regs, key=lambda r: -cols[r])
    if order == glib.BAR_AT_LEFT:
        bar = min(regs, key=lambda r: cols[r])
        return [bar] + sorted((r for r in regs if r != bar), key=lambda r: rows[r])
    raise ValueError(f"unknown order {order!r}")


def fitted_parts(rf, masks):
    """The written parts of the fitted groups, in the file's order of groups and
    the table's order of parts, each (group, the table's part, the ids of its draft
    regions); and each group that a group of its owner and kind would be fitted
    as, or that says it is, but is not, with why.  A fitted group is one of the
    crop's subject's, or one that has data-fit="yes", whose kind the table fits,
    under profile 4 as profile 4 fits it and otherwise as profile 3 does, holding
    a region with draft ink for each written part of a sign of several."""
    me = ssvg.subject(rf)
    drawn = rf.profile == rsvg.PROFILE_4
    region_ids = {r.id for r in rf.regions}
    parts, skipped = [], []
    for g in rf.groups:
        entry = glib.entry_of(g.kind)
        asked = g.fit == rsvg.FIT_YES
        if not entry.fitted(drawn):
            if asked:
                skipped.append((g, f"its kind is not fitted: {entry.why_not(drawn)}"))
            continue
        if g.ink_of != me and not asked:
            continue
        regs = [m for m in g.members if m in region_ids and masks[m].any()]
        if not regs:
            skipped.append((g, "it holds no region with ink"))
        elif len(entry.parts) == 1:
            parts.append((g, entry.parts[0], regs))
        elif len(regs) != len(entry.parts):
            skipped.append(
                (
                    g,
                    f"its {len(regs)} regions with ink are not its kind's"
                    f" {len(entry.parts)} written parts",
                )
            )
        else:
            for p, rid in zip(entry.parts, _order_regions(entry.order, regs, masks)):
                parts.append((g, p, [rid]))
    return parts, skipped


def _dilate4(mask):
    out = mask.copy()
    out[1:, :] |= mask[:-1, :]
    out[:-1, :] |= mask[1:, :]
    out[:, 1:] |= mask[:, :-1]
    out[:, :-1] |= mask[:, 1:]
    return out


def _edges(polys):
    """The edges of polygons, as their starts and their ends."""
    a = np.vstack(polys)
    b = np.vstack([np.roll(p, -1, axis=0) for p in polys])
    return a, b


def boundary_distance(points, polys):
    """The distance, in crop pixels, from each point to the nearest edge of the
    polygons."""
    a, b = _edges(polys)
    d = b - a
    len2 = (d * d).sum(1)
    len2 = np.where(len2 > 0, len2, 1.0)
    out = np.empty(len(points))
    for k in range(0, len(points), 256):
        p = points[k : k + 256, None, :]
        t = np.clip(((p - a) * d).sum(2) / len2, 0.0, 1.0)
        e = p - (a + t[..., None] * d)
        out[k : k + 256] = np.sqrt((e * e).sum(2).min(1))
    return out


def inside_polygons(points, polys):
    """Whether each point lies inside the polygons, by the nonzero rule."""
    a, b = _edges(polys)
    ya, yb = a[:, 1], b[:, 1]
    keep = ya != yb
    a, b, ya, yb = a[keep], b[keep], ya[keep], yb[keep]
    out = np.zeros(len(points), dtype=bool)
    for k in range(0, len(points), 256):
        p = points[k : k + 256, None, :]
        up = (ya <= p[..., 1]) & (p[..., 1] < yb)
        down = (yb <= p[..., 1]) & (p[..., 1] < ya)
        x = a[:, 0] + (p[..., 1] - ya) * (b[:, 0] - a[:, 0]) / (yb - ya)
        left = x <= p[..., 0]
        out[k : k + 256] = ((up & left).sum(1) - (down & left).sum(1)) != 0
    return out


def _along(pts, step=0.1):
    """Points along a polyline, no farther apart than step pixels."""
    out = []
    for a, b in zip(pts, pts[1:]):
        n = max(1, math.ceil(math.dist(a, b) / step))
        out += [
            (a[0] + (b[0] - a[0]) * t / n, a[1] + (b[1] - a[1]) * t / n)
            for t in range(n)
        ]
    out.append(pts[-1])
    return np.array(out, dtype=float)


def _crossing_problems(rf, placed):
    """Each glyph that crosses a strip of vellum or a cut by more than
    LINE_CROSSING pixels: some point of the line lies that deep inside it.  In a
    profile-3 file every strip and cut binds the fit."""
    lines = []
    for v in rf.vellum:
        try:
            lines.append((v.id, "strip of vellum", _along(vellum_points(v))))
        except ValueError:
            continue
    for c in rf.cuts:
        try:
            lines.append((c.id, "cut", _along(cut_points(c))))
        except ValueError:
            continue
    out = []
    for gid, polys in placed.items():
        allp = np.vstack(polys)
        lo, hi = allp.min(0), allp.max(0)
        for lid, what, p in lines:
            near = ((p >= lo) & (p <= hi)).all(1)
            if not near.any():
                continue
            q = p[near]
            ins = inside_polygons(q, polys)
            if not ins.any():
                continue
            deep = float(boundary_distance(q[ins], polys).max())
            if deep > LINE_CROSSING:
                out.append(
                    f"{gid}: crosses the {what} {lid}, which lies {deep:.2f} pixels"
                    f" inside it, more than {geo.fmt(LINE_CROSSING, 2)}"
                )
    return out


def outline_text(polys):
    """A placed glyph's outline as the profile writes it."""
    return geo.polygon_path(
        [[(float(x), float(y)) for x, y in p] for p in polys], OUTLINE_PLACES
    )


def glyph_breaks(gl, group):
    """The guidelines that a glyph breaks: its own and its group's."""
    return glib.breaks_named(gl.brk) | glib.breaks_named(group.brk)


def fit_length(rf, letter, breaks):
    """How many numbers a glyph's data-fit holds: a mark's; a letter's under
    profile 3; and under profile 4 a letter's with guideline 3's warp, or with
    phase 8's where it breaks the guideline limbs."""
    if not letter:
        return gf.MARK_FIT
    if rf.profile != rsvg.PROFILE_4:
        return gf.LETTER_FIT_3
    return gf.LETTER_FIT_4[0] if glib.LIMBS in breaks else gf.LETTER_FIT_4[1]


def place_glyphs(rf, library):
    """Each glyph's contours in crop pixels, the library's glyph placed by its fit,
    by id; and what keeps a glyph from being placed."""
    sources = library.by_id()
    groups = {g.id: g for g in rf.groups}
    cache, placed, out = {}, {}, []
    for gl in rf.glyphs:
        src = sources.get(gl.glyph)
        g = groups.get(gl.group)
        if src is None:
            out.append(f"{gl.id}: data-glyph {gl.glyph!r} is not in the library")
            continue
        if g is None:
            out.append(f"{gl.id}: data-group {gl.group!r} is no group of this file")
            continue
        if (src.kind, src.part) != (g.kind, gl.part):
            out.append(
                f"{gl.id}: its glyph {src.id} is for {src.kind!r}, part {src.part!r},"
                f" not {g.kind!r}, part {gl.part!r}"
            )
            continue
        letter = level5.pass_of(g.kind) == level5.LETTERS
        want = fit_length(rf, letter, glyph_breaks(gl, g))
        if len(gl.fit) != want:
            out.append(
                f"{gl.id}: a {'letter' if letter else 'mark'}'s data-fit holds {want}"
                f" numbers here, not {len(gl.fit)}"
            )
            continue
        prm, warp, offset = gf.split_fit(gl.fit)
        if src.id not in cache:
            cache[src.id] = gf.Glyph(glib.contours(src))
        polys = cache[src.id].place(prm, warp)
        if offset:
            polys = gf.offset_polys(polys, offset)
        placed[gl.id] = polys
    return placed, out


class Fitted:
    """A profile-3 file's steps 9 to 13: its glyphs with their outlines and ink, its
    overlaps of glyphs, the samples inside some glyph and near one, and what is
    left of the draft's regions."""

    def __init__(self, rf, ink):
        self.rf = rf
        self.ink = ink
        self.glyphs = []
        self.glyph_overlaps = []
        self.problems = []
        self.notes = []
        self.covered = np.zeros_like(ink)
        self.near = np.zeros_like(ink)
        # Each sample's glyph, k + 1 for the k-th glyph, or -(j + 1) for the j-th
        # overlap of glyphs, and 0 for none.
        self.gown = np.zeros(ink.shape, np.int32)
        self.fitted_groups = set()
        self.region_groups = {}
        # The draft's samples of each region and authored overlap, by id.
        self.masks = {}

    def left_trace(self, rid, mask, speck_size, problems):
        """A region's or overlap's ink inside no glyph, traced; an unfitted group's
        region, or an authored overlap, that glyphs take entirely is a problem."""
        left = mask & ~self.covered
        d = trace_samples(left, speck_size) if left.any() else ""
        fitted = self.region_groups.get(rid, set()) & self.fitted_groups
        if fitted and not rid.startswith("ov"):
            return d
        if not left.any():
            problems.append(f"{rid}: glyphs take all its ink")
        elif not d:
            problems.append(f"{rid}: its ink is too small to trace")
        return d


def _glyph_order(rf, glyphs):
    """The glyphs' indices in the order that settles ties: by group number, then by
    the part's place in the table, then as the file has them."""
    groups = {g.id: g for g in rf.groups}

    def key(k):
        gl = glyphs[k]
        g = groups.get(gl.group)
        if g is None:
            # place_glyphs already reports the invalid reference; it has no ink.
            return (math.inf, math.inf, k)
        names = [p.name for p in glib.entry_of(g.kind).parts]
        n = rsvg.group_number(gl.group)
        part = names.index(gl.part) if gl.part in names else len(names)
        return (n if n is not None else math.inf, part, k)

    return sorted(range(len(glyphs)), key=key)


def glyph_ink(rf, ink, owner, rank, overlap_masks, library):
    """Steps 9 to 13 of a profile-3 file, given its draft: the ink of step 1, each
    sample's region by rank, each region's rank and each overlap's samples."""
    res = Fitted(rf, ink)
    if library is None:
        raise ValueError("a profile-3 file needs the library of glyphs")
    masks = {r.id: owner == rank[r.id] for r in rf.regions}
    masks.update(overlap_masks)
    res.masks = masks
    for g in rf.groups:
        for m in g.members:
            res.region_groups.setdefault(m, set()).add(g.id)
    parts, skipped = fitted_parts(rf, masks)
    res.fitted_groups = {g.id for g, _, _ in parts}
    want = [(g.id, p.name) for g, p, _ in parts]
    have = [(gl.group, gl.part) for gl in rf.glyphs]
    for key in sorted(set(have) - set(want)):
        res.problems.append(
            f"a glyph of {key[0]}"
            + (f", part {key[1]!r}," if key[1] else "")
            + " which is not a fitted group's written part"
        )
    for key in want:
        n = have.count(key)
        if n != 1:
            res.problems.append(
                f"{key[0]}"
                + (f", part {key[1]!r}," if key[1] else "")
                + f" a fitted group's written part, has {n} glyphs"
            )
    for g, why in skipped:
        line = f"{g.id} ({g.kind}): not fitted: {why}"
        if g.fit == rsvg.FIT_YES:
            res.problems.append(line)
        else:
            res.notes.append(line)
    placed, found = place_glyphs(rf, library)
    res.problems += found
    res.problems += _crossing_problems(rf, placed)
    h, w = ink.shape
    grid = gf.Grid(rf.width, rf.height)
    # The crop's samples and NEAR more all round, on the fit's larger grid.
    x0 = gf.PAD * SAMPLES - NEAR
    y0 = gf.PAD * SAMPLES - NEAR
    ext = (x0, y0, x0 + w + 2 * NEAR, y0 + h + 2 * NEAR)
    inner = (slice(NEAR, NEAR + h), slice(NEAR, NEAR + w))
    count_ext = np.zeros((h + 2 * NEAR, w + 2 * NEAR), np.int16)
    glyph_polys, crop_masks = [], []
    for gl in rf.glyphs:
        polys = placed.get(gl.id)
        outline = outline_text(polys) if polys is not None else ""
        res.glyphs.append(replace(gl, outline=outline, ink=""))
        if polys is None:
            glyph_polys.append(None)
            crop_masks.append(np.zeros_like(ink))
            continue
        # The outline as written places the glyph's samples, so that they follow
        # from the file's text alone.
        pts = [np.array(p, dtype=float) for p in geo.flatten(geo.parse_path(outline))]
        glyph_polys.append(pts)
        q = grid.samples(pts)
        win = gf.window_of(q, grid.gw, grid.gh)
        wx0, wy0 = max(win[0], ext[0]), max(win[1], ext[1])
        wx1, wy1 = min(win[2], ext[2]), min(win[3], ext[3])
        full = np.zeros_like(count_ext, dtype=bool)
        if wx0 < wx1 and wy0 < wy1:
            m = gf.rasterize(q, grid.gw, grid.gh, (wx0, wy0, wx1, wy1))
            full[wy0 - ext[1] : wy1 - ext[1], wx0 - ext[0] : wx1 - ext[0]] = m
        count_ext += full
        crop_masks.append(full[inner])
    near = count_ext > 0
    for _ in range(NEAR):
        near = raster.dilate8(near)
    res.near = near[inner]
    count = count_ext[inner]
    res.covered = count > 0
    for k, m in enumerate(crop_masks):
        res.gown[m & ink & (count == 1)] = k + 1
    order = _glyph_order(rf, rf.glyphs)
    multi = ink & (count >= 2)
    label, n = raster.labels(multi, 4)
    for piece in range(1, n + 1):
        ys, xs = np.nonzero(label == piece)
        pts = np.stack([(xs + 0.5) / SAMPLES, (ys + 0.5) / SAMPLES], 1)
        depth = {}
        for k in order:
            inside = crop_masks[k][ys, xs]
            if inside.any():
                dk = np.full(len(ys), -1.0)
                dk[inside] = boundary_distance(pts[inside], glyph_polys[k])
                depth[k] = dk
        deep = set()
        ks = list(depth)
        for i, a in enumerate(ks):
            for b in ks[i + 1 :]:
                both = (depth[a] >= 0) & (depth[b] >= 0)
                if (
                    both.any()
                    and np.minimum(depth[a], depth[b])[both].max() > OVERLAP_DEPTH
                ):
                    deep |= {a, b}
        if deep:
            res.gown[ys, xs] = -(len(res.glyph_overlaps) + 1)
            res.glyph_overlaps.append(
                rsvg.GlyphOverlap(
                    f"go{len(res.glyph_overlaps) + 1}",
                    tuple(rf.glyphs[k].id for k in sorted(deep)),
                )
            )
            continue
        stack = np.stack([depth[k] for k in ks])
        res.gown[ys, xs] = np.array(ks)[np.argmax(stack, axis=0)] + 1
    for k, gl in enumerate(res.glyphs):
        mine = res.gown == k + 1
        in_overlap = any(gl.id in o.glyphs for o in res.glyph_overlaps)
        if not mine.any() and not in_overlap and glyph_polys[k] is not None:
            res.problems.append(f"{gl.id}: a glyph that holds no ink")
        res.glyphs[k] = replace(gl, ink=trace_samples(mine, rf.speck_size))
    for j, o in enumerate(res.glyph_overlaps):
        res.glyph_overlaps[j] = replace(
            o, d=trace_samples(res.gown == -(j + 1), rf.speck_size)
        )
    res.notes += _unexplained_notes(rf, res, masks)
    return res


def _unexplained_notes(rf, res, masks):
    """Each fitted group's unexplained ink: ink its draft regions hold that lies
    inside no glyph and farther than NEAR samples from every glyph, in total and
    by 8-connected pieces of at least UNEXPLAINED_PIECE samples."""
    out = []
    for g in rf.groups:
        if g.id not in res.fitted_groups:
            continue
        left = np.zeros_like(res.ink)
        for m in g.members:
            if m in masks and not m.startswith("ov"):
                left |= masks[m]
        left &= ~res.covered & ~res.near
        if not left.any():
            continue
        line = f"{g.id} ({g.kind}): {_pixels(left.sum())} pixels of unexplained ink"
        label, n = raster.labels(left, 8)
        pieces = []
        for k in range(1, n + 1):
            ys, xs = np.nonzero(label == k)
            if len(ys) >= UNEXPLAINED_PIECE:
                pieces.append(
                    f"{_pixels(len(ys))} at x {_px(xs.min())}-{_px(xs.max() + 1)},"
                    f" y {_px(ys.min())}-{_px(ys.max() + 1)}"
                )
        out.append(line + (": " + "; ".join(pieces) if pieces else ""))
    return out


def _edge_of(own, ink_of):
    """The edge of the crop that another line's or word's ink meets: the bottom for
    the line below, the top for the line above, and for another word the side its
    ink meets, or none."""
    if ink_of == "line-below":
        return "bottom" if own[-1].any() else ""
    if ink_of == "line-above":
        return "top" if own[0].any() else ""
    sides = [s for s, m in (("right", own[:, -1]), ("left", own[:, 0])) if m.any()]
    return sides[0] if len(sides) == 1 else ""


def fit_ink(rf, grid, ink, page_image):
    """The ink the fit scores, on its larger grid: the ink of step 1 inside the crop
    and, beyond it, the page image's samples darker than the crop's threshold;
    which samples are the crop's; and which are known.  The page image must be the
    crop's source, by its SHA-256, and must hold the crop's box and PAD pixels more
    all round."""
    data = Path(page_image).read_bytes()
    want = rf.provenance.get("source-sha256", "").upper()
    if hashlib.sha256(data).hexdigest().upper() != want:
        raise ValueError(f"{page_image}: not the crop's source image, by its SHA-256")
    bx0, by0, bx1, by1 = (int(v) for v in rf.provenance["crop-box"].split())
    if (bx1 - bx0, by1 - by0) != (rf.width, rf.height):
        raise ValueError("the root's data-crop-box is not the crop's size")
    pad = gf.PAD
    box = (bx0 - pad, by0 - pad, bx1 + pad, by1 + pad)
    with Image.open(page_image) as im:
        if box[0] < 0 or box[1] < 0 or box[2] > im.width or box[3] > im.height:
            raise ValueError(
                f"{page_image}: the crop and {pad} pixels round it pass its edge"
            )
        lum = np.asarray(im.convert("RGB").crop(box).convert("L"))
    inside = grid.pad(np.ones_like(ink))
    page_ink = sample_luminance(lum) < rf.threshold * SAMPLES * SAMPLES
    ink_p = np.where(inside, grid.pad(ink), page_ink)
    known = np.ones_like(inside)
    return ink_p, inside, known


def _meets_edge(mask):
    return bool(
        mask[0].any() or mask[-1].any() or mask[:, 0].any() or mask[:, -1].any()
    )


def fit_instances(rf, masks, library, parts):
    """The fit's instances for the fitted parts, each with its glyph of the
    library: the glyph a glyph of the file already names, or the library's first
    for its kind and part; and where each starts.  Under profile 4 the
    guidelines that a glyph and its group do not break: a letter's warp is
    guideline 3's, and a glyph whose draft ink the crop's edge does not cut has
    guideline 2's stage."""
    me = ssvg.subject(rf)
    fourth = rf.profile == rsvg.PROFILE_4
    existing = {(gl.group, gl.part): gl for gl in rf.glyphs}
    sources = library.by_id()
    cache = {}

    def glyph(src):
        if src.id not in cache:
            cache[src.id] = gf.Glyph(glib.contours(src))
        return cache[src.id]

    insts, sizes = [], []
    for g, p, regs in parts:
        old = existing.get((g.id, p.name))
        src = sources[old.glyph] if old and old.glyph in sources else None
        src = src or library.default_for(g.kind, p.name, fourth)
        own = np.zeros_like(next(iter(masks.values())))
        for r in regs:
            own |= masks[r]
        extra = g.ink_of != me
        letter = level5.pass_of(g.kind) == level5.LETTERS
        inst = gf.Instance(
            g.id + (f" {p.name}" if p.name else ""),
            g.id,
            p.name,
            glyph(src),
            own,
            letter,
            extra,
            _edge_of(own, g.ink_of) if extra else "",
        )
        inst.source = src
        inst.brk = old.brk if old else ""
        if fourth:
            breaks = glib.breaks_named(inst.brk) | glib.breaks_named(g.brk)
            inst.follow_limbs(letter and glib.LIMBS not in breaks)
            inst.area = glib.AREA not in breaks and not _meets_edge(own)
        insts.append(inst)
        if letter and not extra:
            # The subject's letters' size, in crop pixels a font unit: the median
            # over them of their draft ink's height over the height of Taamey D's
            # glyph for their kind.
            tad = glyph(sources[glib.taamey_d_id(g.kind, p.name)])
            x0, y0, x1, y1 = gf.box_of(own)
            sizes.append(math.log((y1 - y0) / (2 * tad.half[1] * tad.size_fu)))
    word = float(np.median(sizes)) if sizes else None
    for inst in insts:
        if inst.letter:
            if not inst.source.is_taamey_d:
                inst.ln_px_fu = 0.0
            elif word is None:
                raise ValueError("no letter of the subject's sizes Taamey D's glyphs")
            else:
                inst.ln_px_fu = word
        inst.init = gf.start(inst)
    return insts, word


def fit_file(svg_path, page_image, log=print):
    """Fit the library's glyphs to a region-SVG's crop, writing its glyphs and their
    data-fit and moving it to profile 4: a glyph the file already has keeps its id,
    its glyph of the library and its breaks.  What the derivation then leaves
    unsettled, and what the check lists without failing."""
    svg_path = Path(svg_path)
    rf = rsvg.read(svg_path)
    lum = raster.load_luminance(dv.crop_path(svg_path, rf))
    library = library_for(svg_path)
    if not library.drawn:
        raise ValueError(
            f"the fit moves a crop to profile {rsvg.PROFILE_4!r}, which needs the"
            f" library's profile {glib.PROFILE!r}"
        )
    rf.profile = rsvg.PROFILE_4
    ink, masks, found = draft_masks(rf, lum)
    if found:
        raise ValueError("the draft is unsettled: " + "; ".join(found))
    parts, skipped = fitted_parts(rf, masks)
    for g, why in skipped:
        log(f"{g.id} ({g.kind}): not fitted: {why}")
    insts, word = fit_instances(rf, masks, library, parts)
    if word is not None:
        log(f"the subject's letters: {math.exp(word):.5f} crop pixels a font unit")
    grid = gf.Grid(rf.width, rf.height)
    ink_p, inside, known = fit_ink(rf, grid, ink, page_image)
    fitted = {g.id for g, _, _ in parts}
    unfitted = np.zeros_like(ink)
    for g in rf.groups:
        if g.id not in fitted:
            for m in g.members:
                if m in masks:
                    unfitted |= masks[m]
    gf.run(grid, insts, ink_p, inside, known, grid.pad(unfitted), log)
    existing = {(gl.group, gl.part): gl for gl in rf.glyphs}
    nxt = max((rsvg.glyph_number(gl.id) for gl in rf.glyphs), default=0) + 1
    glyphs = []
    for inst in insts:
        old = existing.get((inst.group, inst.part))
        if old is None:
            gid, nxt = f"gl{nxt}", nxt + 1
        else:
            gid = old.id
        fit = gf.fit_numbers(
            inst.prm,
            inst.warp if inst.letter else None,
            inst.offset if inst.letter else None,
        )
        glyphs.append(
            rsvg.Glyph(
                gid, inst.group, inst.part, inst.source.id, tuple(fit), brk=inst.brk
            )
        )
    rf.glyphs = glyphs
    fresh, found, res = derive(rf, lum, library)
    rsvg.write(fresh, svg_path)
    return found, res.notes


# ---------------------------------------------------------------- the library


def scribe_glyph(src, snips_dir):
    """A glyph of the scribe's derived from its crop: the outline of the ink that
    the crop's draft gives the group's regions, traced as a region is; and what
    keeps it from serving, such as a letter that is not clean: whose ink meets an
    edge of its crop, or touches another group's ink with no data-clean-note to
    say why it serves even so."""
    try:
        crop, gid = src.scribe_source()
    except ValueError as exc:
        return "", [str(exc)]
    svg = Path(snips_dir) / f"{crop}{rsvg.SUFFIX}"
    if not svg.exists():
        return "", [f"{src.id}: no region-SVG {svg.name}"]
    rf = rsvg.read(svg)
    lum = raster.load_luminance(dv.crop_path(svg, rf))
    ink, masks, found = draft_masks(rf, lum)
    out = [f"{src.id}: {crop}: {p}" for p in found]
    g = next((g for g in rf.groups if g.id == gid), None)
    if g is None:
        return "", out + [f"{src.id}: {crop} has no group {gid}"]
    if g.kind != src.kind:
        out.append(f"{src.id}: {gid} of {crop} is a {g.kind}, not a {src.kind}")
    region_ids = {r.id for r in rf.regions}
    mask = np.zeros_like(ink)
    for m in g.members:
        if m in region_ids:
            mask |= masks[m]
    if not mask.any():
        return "", out + [f"{src.id}: {gid} of {crop} holds no ink"]
    touches = any(m not in region_ids for m in g.members)
    if (touches or (_dilate4(mask) & ink & ~mask).any()) and not src.clean_note:
        out.append(
            f"{src.id}: {gid} of {crop} is not clean: its ink touches another"
            " group's, and no data-clean-note says why it serves"
        )
    if mask[0].any() or mask[-1].any() or mask[:, 0].any() or mask[:, -1].any():
        out.append(
            f"{src.id}: {gid} of {crop} is not clean: its ink meets the crop's edge"
        )
    return trace_samples(mask, rf.speck_size), out


def glyph_crop_glyph(src, snips_dir):
    """A glyph of the scribe's from a glyph crop: the outline of the ink inside its
    lasso, its pixels darker than its threshold traced with level 1's tracer and
    its speck size, at SAMPLES samples a pixel, and traced as a region is; and
    what keeps it from serving, such as a missing glyph crop."""
    try:
        png = glib.glyph_crop_path(snips_dir, src)
    except ValueError as exc:
        return "", [str(exc)]
    if not png.exists():
        return "", [f"{src.id}: no glyph crop {glib.GLYPH_CROPS}/{png.name}"]
    lum = raster.load_luminance(png)
    h, w = lum.shape
    out = []
    x0, y0, x1, y1 = src.box
    if (x1 - x0, y1 - y0) != (w, h):
        out.append(
            f"{src.id}: its glyph crop is {w}x{h} pixels, but its box"
            f" {int(x1 - x0)}x{int(y1 - y0)}"
        )
    pts = list(zip(src.lasso[0::2], src.lasso[1::2]))
    if len(pts) < 3:
        return "", out + [f"{src.id}: its lasso has fewer than three points"]
    fills = [
        geo.format_path(comp, level1.FILL_PLACES)
        for comp in level1.trace_fills(lum < src.threshold, src.speck_size)
    ]
    if not fills:
        return "", out + [f"{src.id}: its glyph crop holds no ink"]
    lasso = geo.polygon_path([pts], rsvg.SEED_PLACES)
    mask = scaled_mask(fills, w, h) & scaled_mask([lasso], w, h)
    if not mask.any():
        return "", out + [f"{src.id}: no ink lies inside its lasso"]
    if _meets_edge(mask):
        out.append(f"{src.id}: its letter's ink meets its glyph crop's edge")
    d = trace_samples(mask, src.speck_size)
    if not d:
        out.append(f"{src.id}: its ink is too small to trace")
    return d, out


def _library_fresh(lib, snips_dir, font_path=None):
    """A copy of the library with its glyphs of the scribe's derived from their
    crops and glyph crops, its drawn glyphs made afresh from the table under
    profile 2, and its glyphs of Taamey D's copied afresh from the font when a font
    is given; and what its derivation finds."""
    if font_path is not None:
        lib = glib.copy_taamey_d(lib, font_path)
    if lib.drawn:
        lib = glib.with_drawn(lib)
    out, sources = [], []
    for s in lib.sources:
        if s.is_glyph_crop:
            d, found = glyph_crop_glyph(s, snips_dir)
            out += found
            s = replace(s, outline=d)
        elif s.is_scribes:
            d, found = scribe_glyph(s, snips_dir)
            out += found
            s = replace(s, outline=d)
        sources.append(s)
    return glib.Library(sources, lib.taamey_d_sha256, lib.profile), out


def library_derive(lib, snips_dir, font_path=None):
    """A copy of the library with its derived glyphs made afresh, as
    _library_fresh gives it; and what keeps it from serving."""
    fresh, out = _library_fresh(lib, snips_dir, font_path)
    return fresh, glib.structural_problems(fresh) + out


def library_derive_file(path, font_path=None):
    """Recompute the library's derived parts in place, copying Taamey D's glyphs
    afresh only when the font is given.  Whether it changed, and what keeps it from
    serving."""
    path = Path(path)
    fresh, found = library_derive(glib.read(path), path.parent, font_path)
    text = glib.dumps(fresh)
    changed = text != path.read_text(encoding="utf-8")
    if changed:
        glib.write(fresh, path)
    return changed, found


def library_problems(path):
    """Every way the library departs from its profile and its crops.  The font is
    never read."""
    path = Path(path)
    try:
        lib = glib.read(path)
    except (OSError, ValueError) as exc:
        return [str(exc)]
    fresh, found = _library_fresh(lib, path.parent)
    out = glib.structural_problems(lib) + found
    if [s.id for s in lib.sources] != [s.id for s in fresh.sources]:
        out.append(
            "the drawn glyphs are not those the table gives, in its order, between"
            " the scribe's and Taamey D's; derive the library again"
        )
    made = fresh.by_id()
    for old in lib.sources:
        new = made.get(old.id)
        if old.is_taamey_d or new is None:
            continue
        if not dv.same_numbers(old.outline, new.outline):
            if old.is_drawn:
                what = "its shape gives; derive the library again, and"
            elif old.is_glyph_crop:
                what = "its glyph crop gives;"
            else:
                what = "its crop's draft gives;"
            out.append(
                f"{old.id}: its outline is not what {what} fit again every crop that"
                " uses it"
            )
    return out
