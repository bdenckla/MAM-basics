"""The trial's shapes as path data: the same construction as the page's script.

Written for the concrete-transcription trial, 2026-11-03.  An outline is
closed contours of control points (x, y, corner): a closed uniform Catmull-Rom
curve through them, as cubic Bezier segments, each control point's handles a
sixth of the chord between its neighbours, and a corner's handles of length 0.
A stroke is a centerline of points, an open Catmull-Rom curve through them,
swept by one width, each end flat or round.  The page's script, in the template,
does exactly this; keep the two alike.
"""

import math

STROKE_SAMPLES = 12  # samples of the centerline per segment
CAP_SAMPLES = 10  # samples of a round cap's half circle


def fmt(v):
    """A coordinate to 3 decimals, without trailing zeros."""
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _tangents_closed(pts):
    n = len(pts)
    out = []
    for i, p in enumerate(pts):
        if p[2]:
            out.append((0.0, 0.0))
            continue
        a, b = pts[(i - 1) % n], pts[(i + 1) % n]
        out.append(((b[0] - a[0]) / 2, (b[1] - a[1]) / 2))
    return out


def outline_d(contours):
    """Path data for an outline's closed contours."""
    parts = []
    for pts in contours:
        n = len(pts)
        if n < 2:
            continue
        tan = _tangents_closed(pts)
        d = [f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"]
        for i in range(n):
            p, q = pts[i], pts[(i + 1) % n]
            tp, tq = tan[i], tan[(i + 1) % n]
            c1 = (p[0] + tp[0] / 3, p[1] + tp[1] / 3)
            c2 = (q[0] - tq[0] / 3, q[1] - tq[1] / 3)
            d.append(
                f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])}"
                f" {fmt(q[0])} {fmt(q[1])}"
            )
        d.append("Z")
        parts.append("".join(d))
    return "".join(parts)


def _bez(p, c1, c2, q, t):
    u = 1 - t
    return (
        u * u * u * p[0]
        + 3 * u * u * t * c1[0]
        + 3 * u * t * t * c2[0]
        + t * t * t * q[0],
        u * u * u * p[1]
        + 3 * u * u * t * c1[1]
        + 3 * u * t * t * c2[1]
        + t * t * t * q[1],
    )


def centerline_samples(pts):
    """Points along an open Catmull-Rom curve through pts, end tangents along the
    first and last chords."""
    n = len(pts)
    tan = []
    for i in range(n):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        k = 1.0 if i in (0, n - 1) else 0.5
        tan.append(((b[0] - a[0]) * k, (b[1] - a[1]) * k))
    out = []
    for i in range(n - 1):
        p, q = pts[i], pts[i + 1]
        c1 = (p[0] + tan[i][0] / 3, p[1] + tan[i][1] / 3)
        c2 = (q[0] - tan[i + 1][0] / 3, q[1] - tan[i + 1][1] / 3)
        for s in range(STROKE_SAMPLES):
            out.append(_bez(p, c1, c2, q, s / STROKE_SAMPLES))
    out.append((pts[-1][0], pts[-1][1]))
    return out


def stroke_polygon(centerline, width, caps):
    """The outline of a stroke, as one polygon."""
    s = centerline_samples(centerline)
    m = len(s)
    r = width / 2
    units = []
    for k in range(m):
        a, b = s[max(k - 1, 0)], s[min(k + 1, m - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        units.append((dx / length, dy / length))
    normals = [(-uy, ux) for ux, uy in units]
    left = [(p[0] + n[0] * r, p[1] + n[1] * r) for p, n in zip(s, normals)]
    right = [(p[0] - n[0] * r, p[1] - n[1] * r) for p, n in zip(s, normals)]
    poly = list(left)
    if caps[1] == "round":
        poly += _half_circle(s[-1], units[-1], normals[-1], r, forward=True)
    poly += list(reversed(right))
    if caps[0] == "round":
        poly += _half_circle(s[0], units[0], normals[0], r, forward=False)
    return poly


def _half_circle(c, u, n, r, forward):
    """Inner points of the half circle round c from +n to -n through +u (forward),
    or from -n to +n through -u."""
    out = []
    for j in range(1, CAP_SAMPLES):
        th = math.pi * j / CAP_SAMPLES
        if forward:
            vx = n[0] * math.cos(th) + u[0] * math.sin(th)
            vy = n[1] * math.cos(th) + u[1] * math.sin(th)
        else:
            vx = -n[0] * math.cos(th) - u[0] * math.sin(th)
            vy = -n[1] * math.cos(th) - u[1] * math.sin(th)
        out.append((c[0] + vx * r, c[1] + vy * r))
    return out


def stroke_d(centerline, width, caps):
    """Path data for a stroke's outline."""
    poly = stroke_polygon(centerline, width, caps)
    head = f"M{fmt(poly[0][0])} {fmt(poly[0][1])}"
    return head + "".join(f"L{fmt(x)} {fmt(y)}" for x, y in poly[1:]) + "Z"


def shape_d(shape):
    """Path data for a shape of either type."""
    if shape["type"] == "outline":
        return outline_d(shape["contours"])
    if shape["type"] == "stroke":
        return stroke_d(shape["centerline"], shape["width"], shape["caps"])
    raise ValueError(f"unknown shape type {shape['type']!r}")
