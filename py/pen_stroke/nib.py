"""Level 2's pen: a flat nib swept along a median, and its fit to a crop's ink.

A nib is a rectangle ``width`` long and ``edge`` thick, its long side at
``angle`` degrees counterclockwise from the crop's x axis as seen on the page.
Moved in a direction at angle phi, it leaves a band of ink
width * |sin(phi - angle)| + edge * |cos(phi - angle)| thick.  The nib is
stiff: nothing modulates its width but direction.
"""

import math
from dataclasses import dataclass

import numpy as np

from pen_stroke import geometry as geo


@dataclass(frozen=True)
class Nib:
    width: float
    angle: float
    edge: float

    def thickness(self, phi):
        """The band of ink the nib leaves moving at angle phi, in degrees."""
        a = math.radians(phi - self.angle)
        return self.width * abs(math.sin(a)) + self.edge * abs(math.cos(a))


def corners(nib):
    """The nib's corners relative to its centre, in crop coordinates (y down)."""
    t = math.radians(nib.angle)
    ux, uy = math.cos(t), -math.sin(t)
    vx, vy = -uy, ux
    a, b = nib.width / 2, nib.edge / 2
    return [
        (a * ux + b * vx, a * uy + b * vy),
        (a * ux - b * vx, a * uy - b * vy),
        (-a * ux - b * vx, -a * uy - b * vy),
        (-a * ux + b * vx, -a * uy + b * vy),
    ]


def sweep(points, nib):
    """The ink of the nib swept along a polyline: one convex polygon per
    segment, whose union is the stroke.  A single point is a dab of the nib."""
    cs = corners(nib)
    pts = [p for k, p in enumerate(points) if k == 0 or p != points[k - 1]]
    if len(pts) == 1:
        x, y = pts[0]
        return [geo.convex_hull([(x + cx, y + cy) for cx, cy in cs])]
    polys = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        hull = [(x0 + cx, y0 + cy) for cx, cy in cs] + [
            (x1 + cx, y1 + cy) for cx, cy in cs
        ]
        polys.append(geo.convex_hull(hull))
    return polys


def _blur(a):
    k = np.array([1.0, 4.0, 6.0, 4.0, 1.0]) / 16.0
    p = np.pad(a, 2, mode="edge")
    rows = sum(k[i] * p[:, i : i + a.shape[1]] for i in range(5))
    return sum(k[i] * rows[i : i + a.shape[0], :] for i in range(5))


def _sobel(a):
    p = np.pad(a, 1, mode="edge")
    gx = (
        (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:])
        - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    ) / 8.0
    gy = (
        (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:])
        - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    ) / 8.0
    return gx, gy


def width_samples(lum, ink, select=None, max_width=60.0, step=0.25, max_skew=30.0):
    """Stroke-width samples (phi, width), one per edge pixel whose ray crosses
    the ink to a roughly parallel far edge.

    From the centre of each ink pixel on the ink's edge, a ray runs along the
    luminance gradient into the ink until it leaves it.  The run is the ink's
    width across the stroke there; phi is the stroke's direction, the edge's
    tangent, in degrees on the page, from 0 up to 180.  A ray whose far edge
    is skewed by more than ``max_skew`` degrees crossed a junction or a curve
    end, not a stroke, and is dropped.  ``select`` limits the starting pixels.
    """
    h, w = ink.shape
    gx, gy = _sobel(_blur(lum.astype(np.float64)))
    p = np.zeros((h + 2, w + 2), dtype=bool)
    p[1:-1, 1:-1] = ink
    inner = p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    edge = ink & ~inner
    if select is not None:
        edge &= select
    cos_skew = math.cos(math.radians(max_skew))
    out = []
    ys, xs = np.nonzero(edge)
    for y, x in zip(ys.tolist(), xs.tolist()):
        g = math.hypot(gx[y, x], gy[y, x])
        if g < 1.0:
            continue
        dx, dy = -gx[y, x] / g, -gy[y, x] / g
        cx, cy = x + 0.5, y + 0.5
        n = 1
        exit_at = None
        while n * step <= max_width:
            qx, qy = cx + n * step * dx, cy + n * step * dy
            ix, iy = math.floor(qx), math.floor(qy)
            if not (0 <= ix < w and 0 <= iy < h):
                break
            if not ink[iy, ix]:
                exit_at = (iy, ix)
                break
            n += 1
        if exit_at is None:
            continue
        ey, ex = exit_at
        ge = math.hypot(gx[ey, ex], gy[ey, ex])
        if ge < 1.0 or (gx[ey, ex] * dx + gy[ey, ex] * dy) / ge < cos_skew:
            continue
        width = (n - 0.5) * step + 0.5
        phi = math.degrees(math.atan2(dx, dy)) % 180.0
        out.append((phi, width))
    return out


def fit(samples, bin_degrees=10, min_count=5):
    """The stiff nib that best explains the samples' median width per direction.

    Returns the nib, the root-mean-square misfit of the bin medians in pixels,
    and the bins as (centre, count, median width).
    """
    nb = round(180 / bin_degrees)
    bins = [[] for _ in range(nb)]
    for phi, wd in samples:
        bins[min(nb - 1, int(phi // bin_degrees))].append(wd)
    rows = [
        ((k + 0.5) * bin_degrees, len(b), float(np.median(b)))
        for k, b in enumerate(bins)
        if len(b) >= min_count
    ]
    if len(rows) < 3:
        return None, None, rows
    phis = np.array([r[0] for r in rows])
    counts = np.array([r[1] for r in rows], dtype=np.float64)
    meds = np.array([r[2] for r in rows])
    wts = np.sqrt(counts)
    best = None
    for k in range(360):
        theta = k * 0.5
        a = np.radians(phis - theta)
        A = np.stack([np.abs(np.sin(a)), np.abs(np.cos(a))], axis=1)
        coef = _nonneg_lstsq(A * wts[:, None], meds * wts)
        resid = A @ coef - meds
        sse = float(np.sum(counts * resid**2))
        if best is None or sse < best[0]:
            best = (sse, theta, coef)
    sse, theta, coef = best
    rms = math.sqrt(sse / counts.sum())
    width, edge = float(coef[0]), float(coef[1])
    # A nib w wide at angle a with edge e leaves the same widths as one e wide at
    # a + 90 with edge w; the nib is the reading whose width is the larger.
    if edge > width:
        width, edge, theta = edge, width, (theta + 90.0) % 180.0
    return Nib(width=width, angle=theta, edge=edge), rms, rows


def _nonneg_lstsq(A, b):
    coef, *_ = np.linalg.lstsq(A, b, rcond=None)
    if (coef >= 0).all():
        return coef
    best = None
    for j in range(A.shape[1]):
        col = A[:, j]
        c = max(0.0, float(col @ b) / float(col @ col))
        trial = np.zeros(A.shape[1])
        trial[j] = c
        err = float(np.sum((A @ trial - b) ** 2))
        if best is None or err < best[0]:
            best = (err, trial)
    return best[1]
