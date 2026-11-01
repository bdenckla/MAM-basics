"""Level 2's strokes: a smooth median swept with a width that varies along it.

A median is one or a few cubic Bézier segments, end to end.  A width goes with
each of its points, so that each segment has four, like its four points, and the
stroke's width at the segment's parameter t is the cubic Bernstein polynomial of
those four.  The width is therefore smooth along each segment, continuous where
two segments meet, and never outside the range of the widths given.

The ink is a band of that width centred on the median.  A stroke whose ends are
"round" is cut square at each end and adds a disc of the end's width there and at
each corner, as a round brush would.  One whose ends are "cut" ends along a
straight cut at each end, as a broad pen's edge ends a stroke, at an angle given
for each end, and fills each corner's outer side to a mitre.  A cut passes
through the median's end; where the band's two edges meet it are its corners,
one beyond the band's square end and one short of it.  An angle is in degrees,
counterclockwise on the page from the crop's x axis, from 0 up to but not
including 180, so that 90 is upright.  The ink is a list of convex polygons,
every one running clockwise on a y-down screen, so that their union is the
stroke under either fill rule.

A swept stroke (profile 5) has no widths of its own: its ink is the crop's
stiff nib, a rectangle, swept along the median without turning, so that its
thickness comes from its direction alone and each end is the nib's own edges.
"""

import math

from pen_stroke import geometry as geo

ENDS = ("round", "cut")
# A cut makes at least this many degrees with the median where it ends; nearer
# the median's direction, its corner would run far beyond the band.
MIN_CUT_DEGREES = 15.0

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
# A merged piece of a swept stroke turns by no more than this many degrees, so
# that the area the nib sweeps along it is the sum of its steps' areas.
_SWEEP_MERGE_TURN = 30.0


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


def end_frame(segs, which):
    """The median's start (which=0) or end (which=1) and its unit tangent pointing
    out of the stroke there."""
    if which == 0:
        tx, ty = tangent(segs[0], 0.0)
        return segs[0][0], (-tx, -ty)
    return segs[-1][3], tangent(segs[-1], 1.0)


def angle_of(direction):
    """A direction's angle as a cut's is given: degrees counterclockwise on the
    page from the x axis, from 0 up to but not including 180."""
    return math.degrees(math.atan2(-direction[1], direction[0])) % 180.0


def square_cut(segs, which):
    """The angle of the cut square to the median at its start (0) or end (1)."""
    _p, (ox, oy) = end_frame(segs, which)
    return angle_of((-oy, ox))


class Cut:
    """One cut end: the half-plane the band keeps, and the triangle it adds.

    The band keeps the points q with m . q <= c, the cut's inner side, and gains
    the triangle between the band's square end, its edge on the side whose
    corner lies beyond that end, and the cut.  ``reach`` is how far the corners
    lie from the square end, along the median.
    """

    def __init__(self, point, out, w, angle):
        ux, uy = math.cos(math.radians(angle)), -math.sin(math.radians(angle))
        ox, oy = out
        nx, ny = -oy, ox
        un = ux * nx + uy * ny
        if abs(un) < math.sin(math.radians(MIN_CUT_DEGREES)):
            raise ValueError(
                f"a cut at {angle:g} degrees makes less than {MIN_CUT_DEGREES:g}"
                " degrees with the median where it ends"
            )
        mx, my = -uy, ux
        if mx * ox + my * oy < 0:
            mx, my = -mx, -my
        self.m = (mx, my)
        self.c = mx * point[0] + my * point[1]
        h = w / 2
        lam = h * (ux * ox + uy * oy) / un
        side = 1.0 if lam >= 0 else -1.0
        edge = (point[0] + side * h * nx, point[1] + side * h * ny)
        corner = (edge[0] + abs(lam) * ox, edge[1] + abs(lam) * oy)
        self.triangle = geo.convex_hull([point, edge, corner])
        self.reach = abs(lam)

    def clip(self, poly):
        """The convex polygon poly cut to the band's side of the cut."""
        (mx, my), c = self.m, self.c
        out = []
        n = len(poly)
        for k in range(n):
            a, b = poly[k], poly[(k + 1) % n]
            da = mx * a[0] + my * a[1] - c
            db = mx * b[0] + my * b[1] - c
            if da <= 0:
                out.append(a)
            if (da < 0 < db) or (db < 0 < da):
                t = da / (da - db)
                out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
        return out


def cut_ends(segs, widths, cuts):
    """The two Cut ends of a stroke whose ends are cut at the angles in cuts."""
    if len(cuts) != 2:
        raise ValueError(f"a cut stroke has two cut angles, not {len(cuts)}")
    for a in cuts:
        if not 0 <= a < 180:
            raise ValueError(f"a cut angle is from 0 up to 180 degrees, not {a:g}")
    sws = segment_widths(widths, len(segs))
    out = []
    for which, w in ((0, sws[0][0]), (1, sws[-1][3])):
        point, direction = end_frame(segs, which)
        try:
            out.append(Cut(point, direction, w, cuts[which]))
        except ValueError as exc:
            raise ValueError(f"at its {('start', 'end')[which]}: {exc}") from exc
    return out


def _cut_band_pieces(segs, sws, cuts):
    """Convex pieces covering a cut stroke's band, segment by segment.

    Within a cut's reach of its end, plus the end's width, along the median,
    each quadrilateral between two samples is kept apart and clipped to the
    cut's inner side; the rest are merged as ``_band_pieces`` merges them.
    """
    per_seg = [samples(seg, ws) for seg, ws in zip(segs, sws)]
    arcs = []
    start = 0.0
    for smp in per_seg:
        arc = [start]
        for a, b in zip(smp, smp[1:]):
            arc.append(arc[-1] + math.dist(a[0], b[0]))
        arcs.append(arc)
        start = arc[-1]
    total = start
    near_start = cuts[0].reach + sws[0][0]
    near_end = total - (cuts[1].reach + sws[-1][3])
    pieces = []
    for smp, arc in zip(per_seg, arcs):
        run = [0]
        for i in range(len(smp) - 1):
            clipping = []
            if arc[i] <= near_start:
                clipping.append(cuts[0])
            if arc[i + 1] >= near_end:
                clipping.append(cuts[1])
            if not clipping:
                run.append(i + 1)
                continue
            if len(run) > 1:
                pieces.extend(_band_pieces([smp[k] for k in run]))
            run = [i + 1]
            a, b = _side_points(smp[i]), _side_points(smp[i + 1])
            quad = geo.convex_hull([a[0], a[1], b[0], b[1]])
            for c in clipping:
                if len(quad) < 3:
                    break
                quad = c.clip(quad)
            if len(quad) >= 3:
                pieces.append(quad)
        if len(run) > 1:
            pieces.extend(_band_pieces([smp[k] for k in run]))
    return pieces


def ink_pieces(segs, widths, ends, cuts=()):
    """The stroke's ink: convex polygons whose union is the swept band."""
    if ends not in ENDS:
        raise ValueError(f"unknown ends {ends!r}")
    sws = segment_widths(widths, len(segs))
    pieces = []
    if ends == "cut":
        ce = cut_ends(segs, widths, cuts)
        pieces.extend(_cut_band_pieces(segs, sws, ce))
        pieces.extend(c.triangle for c in ce if abs(geo.signed_area(c.triangle)) > 1e-6)
    else:
        if cuts:
            raise ValueError("only a stroke whose ends are cut has cut angles")
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


def flattened(segs):
    """The median's points, spaced along each segment as ``samples`` spaces them,
    with no point repeated."""
    pts = []
    for seg in segs:
        n = _sample_count(seg)
        for k in range(n + 1):
            p = point(seg, k / n)
            if not pts or math.dist(p, pts[-1]) > 1e-9:
                pts.append(p)
    return pts


def swept_pieces(segs, nib):
    """A swept stroke's ink: convex polygons whose union is the nib swept along
    the median.

    Moved from one of the median's flattened points to the next, the nib covers
    the convex hull of its rectangle at the two.  Neighbouring steps are merged
    while the run turns by no more than _SWEEP_MERGE_TURN degrees and the convex
    hull of the run exceeds the area the nib sweeps along it, the rectangle's
    area and each step's length times the nib's thickness in its direction, by
    no more than _MERGE_SLACK square pixels.
    """
    corners = nib.corners()

    def placed(p):
        return [(p[0] + cx, p[1] + cy) for cx, cy in corners]

    pts = flattened(segs)
    if len(pts) == 1:
        return [geo.convex_hull(placed(pts[0]))]
    areas, headings = [], []
    for a, b in zip(pts, pts[1:]):
        d = (b[0] - a[0], b[1] - a[1])
        areas.append(math.hypot(*d) * nib.thickness(angle_of(d)))
        headings.append(math.degrees(math.atan2(d[1], d[0])))
    rect = nib.width * nib.edge
    pieces = []
    i = 0
    while i < len(areas):
        hull = geo.convex_hull(placed(pts[i]) + placed(pts[i + 1]))
        band = rect + areas[i]
        turned = 0.0
        k = i + 1
        while k < len(areas):
            turn = abs((headings[k] - headings[k - 1] + 180.0) % 360.0 - 180.0)
            if turned + turn > _SWEEP_MERGE_TURN:
                break
            grown = geo.convex_hull(hull + placed(pts[k + 1]))
            if abs(geo.signed_area(grown)) - (band + areas[k]) > _MERGE_SLACK:
                break
            hull, band, turned = grown, band + areas[k], turned + turn
            k += 1
        pieces.append(hull)
        i = k
    return pieces


def swept_widths(segs, nib, n=16):
    """The thickness of the nib's sweep at n + 1 evenly spaced t along each segment."""
    return [
        nib.thickness(angle_of(tangent(seg, k / n)))
        for seg in segs
        for k in range(n + 1)
    ]
