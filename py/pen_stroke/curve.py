"""Level 2's strokes: a smooth median swept with a width that varies along it.

A median is one or a few cubic Bézier segments, end to end.  A width goes with
each of its points, so that each segment has four, like its four points, and the
stroke's width at the segment's parameter t is the cubic Bernstein polynomial of
those four.  The width is therefore smooth along each segment, continuous where
two segments meet, and never outside the range of the widths given.

The ink is a band of that width centred on the median, cut square to the median
at its ends.  A stroke whose ends are "round" adds a disc of the end's width at
each end and at each corner, as a round brush would; one whose ends are "flat"
leaves its ends cut and fills each corner's outer side to a mitre.  The ink is a
list of convex polygons, every one running clockwise on a y-down screen, so that
their union is the stroke under either fill rule.
"""

import math

from pen_stroke import geometry as geo

ENDS = ("round", "flat")

# Samples per pixel of the segment's control polygon, along t.
_SAMPLES_PER_PX = 2
# Square pixels by which a merged piece of the band may exceed the band it covers.
_MERGE_SLACK = 0.1
# A disc's polygon has a side of about this many pixels, and 12 to 48 sides.
_DISC_SIDE = 1.0
# A turn of less than this many degrees where two segments meet is no corner.
_SMOOTH_JOIN_DEGREES = 1.0
# A mitre longer than this many half-widths is cut off square.
_MITRE_LIMIT = 4.0


def segments(subpaths):
    """The median's cubic segments, each (p0, p1, p2, p3).

    A median is one open subpath of C segments.  Anything else raises, so that
    a vector editor's straight segment cannot pass as a curve unnoticed.
    """
    if len(subpaths) != 1:
        raise ValueError(f"a median has one subpath, not {len(subpaths)}")
    start, segs, closed = subpaths[0]
    if closed:
        raise ValueError("a median is open, not closed")
    if not segs:
        raise ValueError("a median has at least one C segment")
    out = []
    pos = start
    for seg in segs:
        if seg[0] != "C":
            raise ValueError(f"a median's segments are C segments, not {seg[0]}")
        out.append((pos, seg[1], seg[2], seg[3]))
        pos = seg[3]
    return out


def point(seg, t):
    p0, p1, p2, p3 = seg
    a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t**3
    return (
        a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
        a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1],
    )


def width(ws, t):
    """The width at t of a segment whose four widths are ws."""
    w0, w1, w2, w3 = ws
    return (
        (1 - t) ** 3 * w0
        + 3 * (1 - t) ** 2 * t * w1
        + 3 * (1 - t) * t * t * w2
        + t**3 * w3
    )


def tangent(seg, t):
    """The unit direction of travel at t.

    Where the derivative vanishes, as at an end whose control point coincides
    with it, the direction is that of a nearby chord, and failing that the
    segment's chord.  A segment of four equal points has no direction and
    raises.
    """
    p0, p1, p2, p3 = seg
    u = 1 - t
    dx = 3 * (
        u * u * (p1[0] - p0[0]) + 2 * u * t * (p2[0] - p1[0]) + t * t * (p3[0] - p2[0])
    )
    dy = 3 * (
        u * u * (p1[1] - p0[1]) + 2 * u * t * (p2[1] - p1[1]) + t * t * (p3[1] - p2[1])
    )
    n = math.hypot(dx, dy)
    if n > 1e-9:
        return (dx / n, dy / n)
    a, b = point(seg, max(0.0, t - 0.01)), point(seg, min(1.0, t + 0.01))
    for q0, q1 in ((a, b), (p0, p3)):
        dx, dy = q1[0] - q0[0], q1[1] - q0[1]
        n = math.hypot(dx, dy)
        if n > 1e-9:
            return (dx / n, dy / n)
    raise ValueError("a segment whose four points coincide has no direction")


def _sample_count(seg):
    p0, p1, p2, p3 = seg
    hull = math.dist(p0, p1) + math.dist(p1, p2) + math.dist(p2, p3)
    return max(2, math.ceil(hull * _SAMPLES_PER_PX))


def samples(seg, ws):
    """(point, unit tangent, width) at evenly spaced t, both ends included."""
    n = _sample_count(seg)
    return [
        (point(seg, k / n), tangent(seg, k / n), width(ws, k / n)) for k in range(n + 1)
    ]


def segment_widths(widths, nseg):
    """Each segment's four widths, from the median's 1 + 3 * nseg widths."""
    if len(widths) != 1 + 3 * nseg:
        raise ValueError(
            f"{len(widths)} widths where a median of {nseg} segments needs {1 + 3 * nseg}"
        )
    return [tuple(widths[3 * k : 3 * k + 4]) for k in range(nseg)]


def length(segs):
    """The median's length along its curve."""
    total = 0.0
    for seg in segs:
        pts = [point(seg, k / 64) for k in range(65)]
        total += sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    return total


def join_turns(segs):
    """The turn, in degrees, where each segment meets the next."""
    out = []
    for a, b in zip(segs, segs[1:]):
        ta, tb = tangent(a, 1.0), tangent(b, 0.0)
        dot = max(-1.0, min(1.0, ta[0] * tb[0] + ta[1] * tb[1]))
        out.append(math.degrees(math.acos(dot)))
    return out


def _side_points(s):
    (x, y), (tx, ty), w = s
    h = w / 2
    return (x - ty * h, y + tx * h), (x + ty * h, y - tx * h)


def _band_pieces(smp):
    """Convex pieces covering the band along one segment's samples.

    Neighbouring quadrilaterals are merged while the convex hull of the run
    exceeds the band it covers by no more than _MERGE_SLACK square pixels.
    """
    sides = [_side_points(s) for s in smp]
    pieces = []
    i = 0
    j = i + 1
    while j < len(sides):
        k = j + 1
        while k < len(sides):
            left = [sides[m][0] for m in range(i, k + 1)]
            right = [sides[m][1] for m in range(i, k + 1)]
            hull = geo.convex_hull(left + right)
            band = left + right[::-1]
            if abs(geo.signed_area(hull)) - abs(geo.signed_area(band)) > _MERGE_SLACK:
                break
            k += 1
        j = k - 1
        left = [sides[m][0] for m in range(i, j + 1)]
        right = [sides[m][1] for m in range(i, j + 1)]
        pieces.append(geo.convex_hull(left + right))
        i = j
        j = i + 1
    return pieces


def disc(centre, w):
    """A convex polygon approximating the disc of diameter w about centre."""
    r = w / 2
    n = max(12, min(48, math.ceil(2 * math.pi * r / _DISC_SIDE)))
    cx, cy = centre
    return geo.convex_hull(
        [
            (
                cx + r * math.cos(2 * math.pi * k / n),
                cy + r * math.sin(2 * math.pi * k / n),
            )
            for k in range(n)
        ]
    )


def _mitre(join, ta, tb, w):
    """The convex piece that fills a corner's outer side to a mitre."""
    na, nb = (-ta[1], ta[0]), (-tb[1], tb[0])
    side = -1.0 if na[0] * tb[0] + na[1] * tb[1] > 0 else 1.0
    h = w / 2
    jx, jy = join
    a = (jx + side * h * na[0], jy + side * h * na[1])
    b = (jx + side * h * nb[0], jy + side * h * nb[1])
    sx, sy = na[0] + nb[0], na[1] + nb[1]
    s2 = sx * sx + sy * sy
    if s2 < 1e-12 or w / math.sqrt(s2) > _MITRE_LIMIT * h:
        return geo.convex_hull([join, a, b])
    m = (jx + side * w * sx / s2, jy + side * w * sy / s2)
    return geo.convex_hull([join, a, m, b])


def ink_pieces(segs, widths, ends):
    """The stroke's ink: convex polygons whose union is the swept band."""
    if ends not in ENDS:
        raise ValueError(f"unknown ends {ends!r}")
    sws = segment_widths(widths, len(segs))
    pieces = []
    for seg, ws in zip(segs, sws):
        pieces.extend(_band_pieces(samples(seg, ws)))
    for (a, wa), (b, _wb) in zip(zip(segs, sws), zip(segs[1:], sws[1:])):
        ta, tb = tangent(a, 1.0), tangent(b, 0.0)
        dot = max(-1.0, min(1.0, ta[0] * tb[0] + ta[1] * tb[1]))
        if math.degrees(math.acos(dot)) < _SMOOTH_JOIN_DEGREES:
            continue
        w = wa[3]
        if ends == "round":
            pieces.append(disc(a[3], w))
        else:
            pieces.append(_mitre(a[3], ta, tb, w))
    if ends == "round":
        pieces.append(disc(segs[0][0], sws[0][0]))
        pieces.append(disc(segs[-1][3], sws[-1][3]))
    return [p for p in pieces if len(p) >= 3]
