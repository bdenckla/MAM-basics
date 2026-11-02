"""The fit of a fitted word: the library's glyphs placed on a crop's ink.

Under the ink-region profile's profile 3 (doc/ink-region-representation.md), each
written part of each fitted group of a region-SVG has a glyph of the library
(pen_stroke.glyph_library), placed at its ink and fitted to it.  This module
holds the fit's arithmetic, which pen_stroke.region_derive's ``fit`` runs and
whose placement every derivation uses.  It ports the untracked trial of
2026-11-01, its script tt_fit.py, version 3, with its constants, so that the same
start and the same ink give the trial's parameters exactly:

1. a glyph's frame: its outline centred on its box, y down, its larger side 1,
   its edges cut into pieces no longer than DENSIFY; placed by a move, two
   scales, a turn and a shear, and a letter also warped by a thin-plate spline
   through 9 control points on a 3-by-3 grid over its box;
2. the ink, at SAMPLES samples a pixel, on a grid PAD pixels larger than the crop
   all round, where a placed glyph's samples are those whose centres lie inside
   its outline by the nonzero rule, as pen_stroke.geometry.rasterize decides,
   counted in a window round the glyph rather than over the whole grid;
3. CMA-ES, a seeded evolution strategy, which moves, scales, turns and shears
   each glyph, in stage A, toward its group's draft ink, and again, in stage B,
   toward the ink nearest it after stage A, a letter also warped.

Every random draw is seeded, so a fit run twice on one machine gives the same
parameters; on another machine the last digits may differ.
"""

import math

import numpy as np

from pen_stroke import raster

SAMPLES = 3
# Crop pixels round the crop where a glyph may reach, and where the page image's
# ink is known when a fit is given it.
PAD = 60
# A glyph's edges are cut into pieces no longer than this, in its frame.
DENSIFY = 1 / 60
# How far a glyph may depart from where it starts, as logarithms of its scales,
# radians of its turn and its shear: a letter, and a mark.
LETTER_LIMIT = 0.15
MARK_LIMIT = 0.35
# How far a glyph may move: this fraction of its size, but at least MIN_MOVE
# pixels; another line's or word's letter, OTHER_MOVE pixels.
MOVE_FRACTION = 0.3
MIN_MOVE = 3.0
OTHER_MOVE = 40.0
# The score of a sample, in stage A: its group's draft ink +1, other ink in the
# crop OTHER_INK, vellum -1; in stage B: its own ink +1, ink that other glyphs or
# unfitted groups hold FOREIGN_INK, vellum -1.
OTHER_INK = -0.5
FOREIGN_INK = -0.25
# Stage B: how far, in samples, a glyph's own ink reaches (10 crop pixels).
NEAREST_REACH = 30
# A control point's largest move, in glyph sizes, and what a move costs: this
# many square pixels of score for each square pixel of movement.
WARP_LIMIT = 0.12
WARP_COST = 0.5
# Beyond its limits a glyph's score falls by this much for each squared excess.
LIMIT_COST = 1e4
GENERATIONS_A = 100
GENERATIONS_B_LETTER = 200
GENERATIONS_B_MARK = 100
SEED_A = 1000
SEED_B = 2000
# The steps CMA-ES first takes in each parameter: the move in pixels, the
# logarithms of the scales, the turn in radians, the shear; and each of a warp's
# 18 numbers, in glyph sizes.
AFFINE_STEPS = (1.0, 1.0, 0.05, 0.05, 0.04, 0.05)
WARP_STEP = 0.02
WARP_SIZE = 18
FIT_PLACES = 4
# The top or bottom band of a glyph, in its frame, that places another line's
# letter by its part inside the crop.
EDGE_BAND = 0.12


def rasterize(polys, width, height, window=None):
    """The samples of a width-by-height grid whose centres lie inside the polygons,
    each an array of points, by the nonzero rule, as pen_stroke.geometry.rasterize
    decides: within the window (x0, y0, x1, y1) of the grid only, if one is given,
    and then exactly what the whole grid has there."""
    x0, y0, x1, y1 = window or (0, 0, width, height)
    w, h = x1 - x0, y1 - y0
    acc = np.zeros((h, w + 1), np.int32)
    for p in polys:
        q = np.roll(p, -1, axis=0)
        ya, yb = p[:, 1], q[:, 1]
        keep = ya != yb
        a, b, ya, yb = p[keep], q[keep], ya[keep], yb[keep]
        wind = np.where(yb > ya, 1, -1)
        lo, hi = np.minimum(ya, yb), np.maximum(ya, yb)
        j0 = np.clip(np.ceil(lo - 0.5).astype(np.int64), y0, y1)
        j1 = np.clip(np.ceil(hi - 0.5).astype(np.int64), y0, y1)
        n = j1 - j0
        sel = n > 0
        if not sel.any():
            continue
        n, j0 = n[sel], j0[sel]
        a, b, wind = a[sel], b[sel], wind[sel]
        idx = np.repeat(np.arange(len(n)), n)
        offs = np.arange(n.sum()) - np.repeat(np.cumsum(n) - n, n)
        jj = j0[idx] + offs
        yc = jj + 0.5
        ax, ay, bx, by = a[idx, 0], a[idx, 1], b[idx, 0], b[idx, 1]
        xs = ax + (yc - ay) * (bx - ax) / (by - ay)
        ii = np.clip(np.ceil(xs - 0.5).astype(np.int64), x0, x1) - x0
        np.add.at(acc, (jj - y0, ii), wind[idx])
    return np.cumsum(acc[:, :w], axis=1) != 0


def window_of(polys, width, height, grow=0):
    """A window of the grid that holds every sample inside the polygons, grown by
    grow samples each way, within the grid."""
    pts = np.vstack(polys)
    lo, hi = pts.min(0), pts.max(0)
    return (
        max(0, int(math.floor(lo[0])) - grow),
        max(0, int(math.floor(lo[1])) - grow),
        min(width, int(math.ceil(hi[0])) + 1 + grow),
        min(height, int(math.ceil(hi[1])) + 1 + grow),
    )


class Grid:
    """A crop's samples, SAMPLES a pixel each way, on a grid PAD pixels larger than
    the crop all round."""

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.gw = (width + 2 * PAD) * SAMPLES
        self.gh = (height + 2 * PAD) * SAMPLES
        self.inner = (
            slice(PAD * SAMPLES, (PAD + height) * SAMPLES),
            slice(PAD * SAMPLES, (PAD + width) * SAMPLES),
        )

    def pad(self, m):
        """A mask of the crop's samples on the larger grid, False beyond the crop."""
        out = np.zeros((self.gh, self.gw), m.dtype)
        out[self.inner] = m
        return out

    def samples(self, polys):
        """Polygons in crop pixels as polygons in the larger grid's samples."""
        return [(p + PAD) * SAMPLES for p in polys]

    def placed(self, polys):
        """A placed glyph's window of the larger grid, and its samples there."""
        q = self.samples(polys)
        win = window_of(q, self.gw, self.gh)
        return win, rasterize(q, self.gw, self.gh, win)

    def full(self, polys):
        """A placed glyph's samples on the whole larger grid."""
        win, m = self.placed(polys)
        out = np.zeros((self.gh, self.gw), dtype=bool)
        out[win[1] : win[3], win[0] : win[2]] = m
        return out


def _densify(c, step):
    out = []
    n = len(c)
    for k in range(n):
        a, b = c[k], c[(k + 1) % n]
        m = max(1, int(math.ceil(np.hypot(*(b - a)) / step)))
        for t in range(m):
            out.append(a + (b - a) * t / m)
    return np.array(out)


def _moments(polys):
    """Area, centroid and covariance of polygons, signed areas summed."""
    A = cx = cy = ixx = iyy = ixy = 0.0
    for p in polys:
        x, y = p[:, 0], p[:, 1]
        x1, y1 = np.roll(x, -1), np.roll(y, -1)
        c = x * y1 - x1 * y
        A += c.sum() / 2
        cx += ((x + x1) * c).sum() / 6
        cy += ((y + y1) * c).sum() / 6
        ixx += ((x * x + x * x1 + x1 * x1) * c).sum() / 12
        iyy += ((y * y + y * y1 + y1 * y1) * c).sum() / 12
        ixy += ((x * y1 + 2 * x * y + 2 * x1 * y1 + x1 * y) * c).sum() / 24
    cx, cy = cx / A, cy / A
    cov = np.array([[ixx / A - cx * cx, ixy / A - cx * cy], [0, iyy / A - cy * cy]])
    cov[1, 0] = cov[0, 1]
    return abs(A), np.array([cx, cy]), cov


def _sqrtm(s, inverse=False):
    vals, vecs = np.linalg.eigh(s)
    vals = np.maximum(vals, 1e-12) ** (-0.5 if inverse else 0.5)
    return (vecs * vals) @ vecs.T


def _tps_matrix(ctrl, pts):
    """The linear map from the control points' moves to the points' moves by the
    thin-plate spline through them."""

    def kern(d):
        with np.errstate(divide="ignore", invalid="ignore"):
            v = d * d * np.log(d)
        return np.nan_to_num(v)

    n = len(ctrl)
    dc = np.linalg.norm(ctrl[:, None] - ctrl[None], axis=2)
    m = np.zeros((n + 3, n + 3))
    m[:n, :n] = kern(dc)
    m[:n, n] = 1
    m[:n, n + 1 :] = ctrl
    m[n, :n] = 1
    m[n + 1 :, :n] = ctrl.T
    minv = np.linalg.inv(m)[:, :n]
    dp = np.linalg.norm(pts[:, None] - ctrl[None], axis=2)
    basis = np.hstack([kern(dp), np.ones((len(pts), 1)), pts])
    return basis @ minv


class Glyph:
    """A glyph in its frame: centred on its box, y down, its larger side 1; with the
    thin-plate spline's map from control points' moves to its points' moves.  Its
    contours are given y up, as a font's are (glyph_library.contours)."""

    def __init__(self, contours):
        allp = np.vstack(contours)
        lo, hi = allp.min(0), allp.max(0)
        # Its size, in its own units: font units, or the scribe's crop pixels.
        self.size_fu = float((hi - lo).max())
        centre = (lo + hi) / 2
        polys = []
        for c in contours:
            q = (c - centre) / self.size_fu
            q[:, 1] = -q[:, 1]
            polys.append(_densify(q, DENSIFY))
        self.polys = polys
        self.lens = [len(p) for p in polys]
        self.pts = np.vstack(polys)
        self.half = (hi - lo) / self.size_fu / 2
        hx, hy = self.half
        self.ctrl = np.array(
            [(sx * hx, sy * hy) for sy in (-1, 0, 1) for sx in (-1, 0, 1)]
        )
        self.tps = _tps_matrix(self.ctrl, self.pts)
        self.area, self.centroid, self.cov = _moments(polys)

    def place(self, prm, warp=None):
        """The glyph's contours in crop pixels for the parameters prm = (move x,
        move y, ln scale x, ln scale y, turn, shear) and the control points'
        moves warp."""
        tx, ty, lsx, lsy, th, sh = prm
        u = self.pts if warp is None else self.pts + self.tps @ warp.reshape(9, 2)
        a = np.array([[math.exp(lsx), sh * math.exp(lsy)], [0.0, math.exp(lsy)]])
        r = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        p = u @ (r @ a).T + (tx, ty)
        return np.split(p, np.cumsum(self.lens)[:-1])


def cmaes(f, x0, scale, gens, seed):
    """Minimize f near x0 by CMA-ES in the coordinates x0 + scale * z: the best
    point found and its value."""
    rng = np.random.default_rng(seed)
    n = len(x0)
    lam = 4 + int(3 * math.log(n))
    mu = lam // 2
    w = math.log(mu + 0.5) - np.log(np.arange(1, mu + 1))
    w /= w.sum()
    mueff = 1 / (w * w).sum()
    cc = (4 + mueff / n) / (n + 4 + 2 * mueff / n)
    cs = (mueff + 2) / (n + mueff + 5)
    c1 = 2 / ((n + 1.3) ** 2 + mueff)
    cmu = min(1 - c1, 2 * (mueff - 2 + 1 / mueff) / ((n + 2) ** 2 + mueff))
    damps = 1 + 2 * max(0, math.sqrt((mueff - 1) / (n + 1)) - 1) + cs
    chin = math.sqrt(n) * (1 - 1 / (4 * n) + 1 / (21 * n * n))
    m = np.zeros(n)
    sigma = 1.0
    c = np.eye(n)
    b, d = np.eye(n), np.ones(n)
    pc, ps = np.zeros(n), np.zeros(n)
    best = (f(x0), m.copy())
    for g in range(gens):
        z = rng.standard_normal((lam, n))
        y = (z * d) @ b.T
        xs = m + sigma * y
        fx = np.array([f(x0 + scale * x) for x in xs])
        order = np.argsort(fx, kind="stable")
        if fx[order[0]] < best[0]:
            best = (fx[order[0]], xs[order[0]].copy())
        ysel = y[order[:mu]]
        yw = w @ ysel
        m = m + sigma * yw
        ps = (1 - cs) * ps + math.sqrt(cs * (2 - cs) * mueff) * (b @ ((b.T @ yw) / d))
        hsig = np.linalg.norm(ps) / math.sqrt(1 - (1 - cs) ** (2 * (g + 1))) / chin
        hsig = hsig < 1.4 + 2 / (n + 1)
        pc = (1 - cc) * pc + hsig * math.sqrt(cc * (2 - cc) * mueff) * yw
        c = (
            (1 - c1 - cmu) * c
            + c1 * (np.outer(pc, pc) + (1 - hsig) * cc * (2 - cc) * c)
            + cmu * (ysel.T * w) @ ysel
        )
        sigma *= math.exp((cs / damps) * (np.linalg.norm(ps) / chin - 1))
        c = np.triu(c) + np.triu(c, 1).T
        d2, b = np.linalg.eigh(c)
        d = np.sqrt(np.maximum(d2, 1e-20))
        if sigma * d.max() < 1e-3:
            break
    return x0 + scale * best[1], best[0]


class Instance:
    """One glyph to fit: a written part of a fitted group, with its glyph, its
    group's or part's draft ink, and where it starts."""

    def __init__(self, name, group, part, glyph, own, letter, extra, edge=""):
        self.name = name
        self.group = group
        self.part = part
        self.glyph = glyph
        # Its draft ink, on the crop's samples.
        self.own = own
        self.letter = letter
        # Whether it is another line's or word's letter or mark, and which edge of
        # the crop its ink meets: "top", "bottom", "left" or "right".
        self.extra = extra
        self.edge = edge
        self.ln_px_fu = 0.0
        self.init = None
        self.prm = None
        self.warp = np.zeros(WARP_SIZE)


def _target_moments(mask):
    ys, xs = np.nonzero(mask)
    pts = np.stack([(xs + 0.5) / SAMPLES, (ys + 0.5) / SAMPLES], 1)
    c = pts.mean(0)
    return c, np.cov((pts - c).T, bias=True)


def _largest_piece(mask):
    lab, n = raster.labels(mask, 4)
    if n <= 1:
        return mask
    sizes = np.bincount(lab.ravel())[1:]
    return lab == (1 + int(np.argmax(sizes)))


def start_mark(g, mask):
    """A mark's start: the largest piece of its ink's centroid and second moments."""
    ct, st = _target_moments(_largest_piece(mask))
    a = _sqrtm(st) @ _sqrtm(g.cov, inverse=True)
    t = ct - a @ g.centroid
    q, r = np.linalg.qr(a)
    for k in range(2):
        if r[k, k] < 0:
            q[:, k] *= -1
            r[k, :] *= -1
    th = math.atan2(q[1, 0], q[0, 0])
    return np.array(
        [t[0], t[1], math.log(r[0, 0]), math.log(r[1, 1]), th, r[0, 1] / r[1, 1]]
    )


def box_of(mask):
    """The box of a mask's samples, in crop pixels."""
    ys, xs = np.nonzero(mask)
    return (
        xs.min() / SAMPLES,
        ys.min() / SAMPLES,
        (xs.max() + 1) / SAMPLES,
        (ys.max() + 1) / SAMPLES,
    )


def start_letter(g, mask, ln_px_fu):
    """A letter's start: ln_px_fu crop pixels a unit of its glyph, its glyph's box's
    top and right edge on its ink's, since Hebrew letters hang from the line and
    begin at the right."""
    x0, y0, x1, y1 = box_of(mask)
    s = math.exp(ln_px_fu) * g.size_fu
    hx, hy = g.half
    return np.array([x1 - s * hx, y0 + s * hy, math.log(s), math.log(s), 0.0, 0.0])


def start_partial(g, own, ln_px_fu, edge):
    """Another line's or word's letter, of which the crop shows only the part that
    meets one of its edges: that part of its glyph over its ink.  At the crop's
    bottom edge, the glyph's top at the ink's top and the middle of its top band
    over the ink's; at its top edge, likewise its bottom; at its right edge, its
    left side at the ink's left and the middle of its left band level with the
    ink's; at its left edge, likewise its right side."""
    pts = g.pts
    s = math.exp(ln_px_fu) * g.size_fu
    ys, xs = np.nonzero(own)
    if edge == "bottom":
        top = pts[:, 1].min()
        band = pts[pts[:, 1] < top + EDGE_BAND]
        tx = xs.mean() / SAMPLES - s * band[:, 0].mean()
        ty = ys.min() / SAMPLES - s * top
    elif edge == "top":
        bottom = pts[:, 1].max()
        band = pts[pts[:, 1] > bottom - EDGE_BAND]
        tx = xs.mean() / SAMPLES - s * band[:, 0].mean()
        ty = (ys.max() + 1) / SAMPLES - s * bottom
    elif edge == "right":
        left = pts[:, 0].min()
        band = pts[pts[:, 0] < left + EDGE_BAND]
        tx = xs.min() / SAMPLES - s * left
        ty = ys.mean() / SAMPLES - s * band[:, 1].mean()
    elif edge == "left":
        right = pts[:, 0].max()
        band = pts[pts[:, 0] > right - EDGE_BAND]
        tx = (xs.max() + 1) / SAMPLES - s * right
        ty = ys.mean() / SAMPLES - s * band[:, 1].mean()
    else:
        raise ValueError(f"unknown edge {edge!r}")
    return np.array([tx, ty, math.log(s), math.log(s), 0.0, 0.0])


def start(inst):
    """Where an instance starts, from its glyph, its draft ink and ln_px_fu."""
    if not inst.letter:
        return start_mark(inst.glyph, inst.own)
    if inst.extra:
        return start_partial(inst.glyph, inst.own, inst.ln_px_fu, inst.edge)
    return start_letter(inst.glyph, inst.own, inst.ln_px_fu)


def penalty(inst, prm):
    """The bounds: a letter keeps its starting size, give or take LETTER_LIMIT, and
    little shear or turn; a mark keeps near its starting place and shape."""
    init = inst.init
    size = math.exp(max(init[2], init[3]))
    move = OTHER_MOVE if inst.extra else max(MIN_MOVE, MOVE_FRACTION * size)
    lim = LETTER_LIMIT if inst.letter else MARK_LIMIT
    centre = init.copy()
    if inst.letter:
        ln_s = inst.ln_px_fu + math.log(inst.glyph.size_fu)
        centre[2] = centre[3] = ln_s
    lims = np.array([move, move, lim, lim, lim, lim])
    excess = np.maximum(np.abs(prm - centre) - lims, 0) / lims
    return LIMIT_COST * (excess**2).sum()


def objective(grid, inst, weights, warp):
    """The function CMA-ES minimizes for an instance: its penalties less its score,
    the sum of the weights of the samples inside it, in square crop pixels."""
    g = inst.glyph
    size = math.exp(max(inst.init[2], inst.init[3]))

    def f(v):
        prm = v[:6]
        wv = v[6:] if warp else None
        pen = penalty(inst, prm)
        if warp:
            ex = np.maximum(np.abs(wv) - WARP_LIMIT, 0)
            pen += LIMIT_COST * (ex**2).sum() + WARP_COST * ((wv * size) ** 2).sum()
        (x0, y0, x1, y1), m = grid.placed(g.place(prm, wv))
        return pen - weights[y0:y1, x0:x1][m].sum() / SAMPLES**2

    return f


def fit_one(grid, inst, weights, warp, seed, gens):
    """An instance fitted from its parameters: its new parameters, its warp and
    its score."""
    f = objective(grid, inst, weights, warp)
    sc_aff = np.array(AFFINE_STEPS)
    base = np.concatenate([inst.prm, inst.warp]) if warp else inst.prm
    scale = np.concatenate([sc_aff, np.full(WARP_SIZE, WARP_STEP)]) if warp else sc_aff
    best, val = cmaes(f, base, scale, gens, seed)
    return best[:6], (best[6:] if warp else np.zeros(WARP_SIZE)), -val


def nearest(grid, masks, reach):
    """Each glyph's share of the grid: the samples no farther from it, in
    8-connected steps, than from any other glyph, and at most reach steps; each
    as its window and its samples there."""
    best = np.full((grid.gh, grid.gw), reach + 1, np.int16)
    dists = []
    for win, m in masks:
        x0, y0, x1, y1 = (
            max(0, win[0] - reach - 1),
            max(0, win[1] - reach - 1),
            min(grid.gw, win[2] + reach + 1),
            min(grid.gh, win[3] + reach + 1),
        )
        cur = np.zeros((y1 - y0, x1 - x0), dtype=bool)
        cur[win[1] - y0 : win[3] - y0, win[0] - x0 : win[2] - x0] = m
        dist = np.full(cur.shape, reach + 1, np.int16)
        dist[cur] = 0
        for r in range(1, reach + 1):
            cur = raster.dilate8(cur)
            dist[cur & (dist > r)] = r
        np.minimum(best[y0:y1, x0:x1], dist, out=best[y0:y1, x0:x1])
        dists.append(((x0, y0, x1, y1), dist))
    shares = []
    for (x0, y0, x1, y1), dist in dists:
        here = best[y0:y1, x0:x1]
        shares.append(((x0, y0, x1, y1), (dist == here) & (here <= reach)))
    return shares, best <= reach


def _window_mask(shape, win, m):
    out = np.zeros(shape, dtype=bool)
    out[win[1] : win[3], win[0] : win[2]] = m
    return out


def run(grid, insts, ink, inside, known, unfitted, log=None):
    """Fit every instance in place, in two stages, given the ink on the larger
    grid, which of its samples are the crop's, which are known, and the ink that
    unfitted groups hold."""
    # Stage A: each glyph toward its own draft ink.
    for k, inst in enumerate(insts):
        own = grid.pad(inst.own)
        if inst.extra:
            own |= ink & ~inside  # its part beyond the crop is its own
        other = ink & ~own & inside
        wts = np.where(own, 1.0, np.where(other, OTHER_INK, np.where(ink, 0.0, -1.0)))
        wts = wts * known
        inst.prm, inst.warp = inst.init.copy(), np.zeros(WARP_SIZE)
        inst.prm, _, sc = fit_one(grid, inst, wts, False, SEED_A + k, GENERATIONS_A)
        if log:
            log(f"A {inst.name:12s} score {sc:7.1f}")
    # Stage B: the ink each glyph of stage A is nearest is its own; each glyph, a
    # letter warped too, toward its own ink, other glyphs' ink and unfitted groups'
    # counting a little against it.
    masks = [grid.placed(i.glyph.place(i.prm)) for i in insts]
    shares, any_share = nearest(grid, masks, NEAREST_REACH)
    for k, inst in enumerate(insts):
        share = _window_mask(ink.shape, *shares[k])
        mine = ink & share & ~unfitted
        if not inst.extra:
            mine &= inside  # beyond the crop, only another line's letter's own
        theirs = ink & inside & ~mine & (unfitted | any_share)
        wts = np.where(
            mine, 1.0, np.where(theirs, FOREIGN_INK, np.where(ink, 0.0, -1.0))
        )
        wts = wts * known
        warp = inst.letter
        gens = GENERATIONS_B_LETTER if warp else GENERATIONS_B_MARK
        prm, wv, sc = fit_one(grid, inst, wts, warp, SEED_B + k, gens)
        inst.prm, inst.warp = prm, wv
        if log:
            log(f"B {inst.name:12s} score {sc:7.1f} warp {np.abs(wv).max():.3f}")


def fit_numbers(prm, warp):
    """A glyph's data-fit: its 6 parameters, and for a letter its warp's 18
    numbers, each to FIT_PLACES decimals."""
    vals = list(prm) + ([] if warp is None else list(warp))
    return [round(float(v), FIT_PLACES) for v in vals]


def split_fit(numbers):
    """A data-fit's numbers as parameters and a warp, or None for a mark's."""
    if len(numbers) not in (6, 6 + WARP_SIZE):
        raise ValueError(f"a data-fit holds 6 or {6 + WARP_SIZE} numbers")
    prm = np.array(numbers[:6], dtype=float)
    warp = np.array(numbers[6:], dtype=float) if len(numbers) > 6 else None
    return prm, warp
