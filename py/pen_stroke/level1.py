"""Level 1: the ink as filled Bezier outlines, and the image residual.

The ink is the pixels whose luminance is below the crop's threshold.  Potrace,
in its pure-Python port, traces them as filled outlines and drops every path
whose area is no more than the speck size.  The image residual is everything the
fills and the threshold leave unsettled, for a human to judge: specks the tracer
dropped, holes it filled, faint ink the threshold lost, the slivers where its
smoothing departs from the pixels, and the halo of pixels within a band of the
threshold on either side.
"""

import numpy as np
import potrace

from pen_stroke import geometry as geo
from pen_stroke import raster

TRACER = "potracer 0.0.4, turnpolicy minority, alphamax 1, opttolerance 0.2"
_TRACE_ARGS = {
    "turnpolicy": potrace.POTRACE_TURNPOLICY_MINORITY,
    "alphamax": 1.0,
    "opticurve": True,
    "opttolerance": 0.2,
}
FILL_PLACES = 3

# What a human may judge a residual piece, or a fill that is not ink, to be.
JUDGMENTS = (
    "unjudged",
    "ink",
    "speck",
    "stain",
    "bleed-through",
    "damage",
    "noise",
    "paper",
)
# The kinds of residual piece this level derives.
PIECE_SOURCES = ("speck", "hole", "faint")


def trace_fills(ink, speck_size):
    """The fill components, each a list of subpaths: an outer outline, then the
    holes inside it.  Components and holes keep the tracer's order."""
    curves = potrace.Bitmap(~ink).trace(turdsize=speck_size, **_TRACE_ARGS)
    subpaths = [_subpath(c) for c in curves]
    polys = [geo.flatten([sp])[0] for sp in subpaths]
    areas = [geo.signed_area(p) for p in polys]
    outers = [k for k, a in enumerate(areas) if a > 0]
    members = {k: [k] for k in outers}
    for k, a in enumerate(areas):
        if a >= 0:
            continue
        probe = polys[k][0]
        around = [o for o in outers if _inside(polys[o], probe)]
        if not around:
            raise ValueError(f"a traced hole at {probe} lies in no outline")
        members[min(around, key=lambda o: areas[o])].append(k)
    return [[subpaths[k] for k in members[o]] for o in outers]


def _subpath(curve):
    start = (curve.start_point.x, curve.start_point.y)
    segs = []
    for s in curve.segments:
        if s.is_corner:
            segs.append(("L", (s.c.x, s.c.y)))
            segs.append(("L", (s.end_point.x, s.end_point.y)))
        else:
            segs.append(
                (
                    "C",
                    (s.c1.x, s.c1.y),
                    (s.c2.x, s.c2.y),
                    (s.end_point.x, s.end_point.y),
                )
            )
    return (start, segs, True)


def _inside(poly, pt):
    x, y = pt
    inside = False
    n = len(poly)
    for k in range(n):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % n]
        if (y0 > y) != (y1 > y):
            if x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
                inside = not inside
    return inside


def fill_mask(fill_ds, width, height):
    """The pixels inside the given fill paths."""
    polys = []
    for d in fill_ds:
        polys.extend(geo.flatten(geo.parse_path(d)))
    return geo.rasterize(polys, width, height, "nonzero")


def image_residual(lum, threshold, band, speck_size, fills_px):
    """The residual pieces as (source, mask) pairs, the smoothing slivers, and
    the halo, all as boolean masks."""
    ink = lum < threshold
    specks = [c for c in raster.components(ink, 8) if not (c & fills_px).any()]
    holes = [c for c in raster.components(~ink, 4) if not (c & ~fills_px).any()]
    near_ink = raster.dilate8(ink)
    faint_zone = (lum >= threshold) & (lum < threshold + band)
    faint = [
        c
        for c in raster.components(faint_zone, 8)
        if c.sum() > speck_size and not (c & near_ink).any()
    ]
    pieces = (
        [("speck", c) for c in specks]
        + [("hole", c) for c in holes]
        + [("faint", c) for c in faint]
    )
    pieces.sort(key=lambda p: _first_pixel(p[1]))
    settled = np.zeros_like(ink)
    for source, c in pieces:
        if source != "faint":
            settled |= c
    smoothing = (ink ^ fills_px) & ~settled
    halo = (lum >= threshold - band) & (lum < threshold + band)
    return pieces, smoothing, halo


def _first_pixel(mask):
    ys, xs = np.nonzero(mask)
    return (int(ys[0]), int(xs[0]))
