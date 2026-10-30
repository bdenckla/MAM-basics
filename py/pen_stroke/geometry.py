"""Path data, exact rasterization at pixel centres, and exact pixel contours.

A path is a list of subpaths; a subpath is a start point and a list of
segments, each ("L", end) or ("C", control1, control2, end), and every subpath
of a filled path is closed.  Coordinates are crop pixels, x right and y down,
with pixel (i, j) covering [i, i+1) x [j, j+1); a pixel is inside a shape when
its centre (i + 0.5, j + 0.5) is.
"""

import math
import re

import numpy as np

_TOKEN = re.compile(r"[MmLlHhVvCcZz]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")
_ARG_COUNTS = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "Z": 0}


def parse_path(d):
    """Parse SVG path data with commands M, L, H, V, C and Z, absolute or relative.

    Other commands raise: the profile's paths use these alone, and a vector
    editor's arcs or quadratic curves must be converted before the file is read.
    """
    tokens = _TOKEN.findall(d)
    if "".join(tokens).replace(" ", "") != re.sub(r"[\s,]+", "", d):
        raise ValueError(f"unsupported path data: {d[:80]!r}")
    subpaths = []
    cur = None
    pos = (0.0, 0.0)
    i = 0
    cmd = None
    while i < len(tokens):
        tok = tokens[i]
        if tok.isalpha():
            cmd = tok
            i += 1
            if cmd in "Zz":
                if cur is None:
                    raise ValueError("Z without a subpath")
                cur[2] = True
                pos = cur[0]
                cur = None
                continue
        elif cmd is None:
            raise ValueError("path data does not start with a command")
        upper = cmd.upper()
        n = _ARG_COUNTS[upper]
        args = [float(t) for t in tokens[i : i + n]]
        if len(args) != n:
            raise ValueError(f"truncated {cmd} in path data")
        i += n
        rel = cmd.islower()
        if upper == "M":
            pt = _rel(pos, args[0], args[1], rel)
            cur = [pt, [], False]
            subpaths.append(cur)
            pos = pt
            cmd = "l" if rel else "L"
            continue
        if cur is None:
            cur = [pos, [], False]
            subpaths.append(cur)
        if upper == "L":
            pt = _rel(pos, args[0], args[1], rel)
            cur[1].append(("L", pt))
        elif upper == "H":
            pt = (pos[0] + args[0] if rel else args[0], pos[1])
            cur[1].append(("L", pt))
        elif upper == "V":
            pt = (pos[0], pos[1] + args[0] if rel else args[0])
            cur[1].append(("L", pt))
        else:
            c1 = _rel(pos, args[0], args[1], rel)
            c2 = _rel(pos, args[2], args[3], rel)
            pt = _rel(pos, args[4], args[5], rel)
            cur[1].append(("C", c1, c2, pt))
        pos = pt
    return [(sp[0], sp[1], sp[2]) for sp in subpaths]


def _rel(pos, x, y, rel):
    return (pos[0] + x, pos[1] + y) if rel else (x, y)


def fmt(v, places):
    """A number with at most ``places`` decimals, trailing zeros dropped."""
    s = f"{v:.{places}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def format_path(subpaths, places):
    """SVG path data for subpaths, absolute commands only."""
    out = []
    for start, segs, closed in subpaths:
        parts = [f"M{fmt(start[0], places)} {fmt(start[1], places)}"]
        for seg in segs:
            pts = seg[1:]
            nums = " ".join(f"{fmt(p[0], places)} {fmt(p[1], places)}" for p in pts)
            parts.append(f"{seg[0]}{nums}")
        if closed:
            parts.append("Z")
        out.append(" ".join(parts))
    return " ".join(out)


def polygon_path(polygons, places):
    """SVG path data for closed polygons given as vertex lists."""
    subpaths = [(p[0], [("L", q) for q in p[1:]], True) for p in polygons]
    return format_path(subpaths, places)


def flatten(subpaths, tolerance=0.25):
    """Each subpath as a polyline: a list of vertices, curves subdivided evenly
    into pieces no longer than about ``tolerance`` pixels."""
    polys = []
    for start, segs, _closed in subpaths:
        pts = [start]
        pos = start
        for seg in segs:
            if seg[0] == "L":
                pts.append(seg[1])
            else:
                c1, c2, end = seg[1], seg[2], seg[3]
                hull = math.dist(pos, c1) + math.dist(c1, c2) + math.dist(c2, end)
                n = min(64, max(4, math.ceil(hull / tolerance)))
                for k in range(1, n + 1):
                    t = k / n
                    a = (1 - t) ** 3
                    b = 3 * (1 - t) ** 2 * t
                    c = 3 * (1 - t) * t * t
                    e = t**3
                    pts.append(
                        (
                            a * pos[0] + b * c1[0] + c * c2[0] + e * end[0],
                            a * pos[1] + b * c1[1] + c * c2[1] + e * end[1],
                        )
                    )
            pos = seg[-1]
        polys.append(pts)
    return polys


def polyline_points(subpaths):
    """The vertices of an open or closed path of straight segments, in order.

    A median is authored as one subpath of straight segments; a curve in it is
    flattened first, so a vector editor's smoothing does not change its meaning.
    """
    if len(subpaths) != 1:
        raise ValueError(f"a median has one subpath, not {len(subpaths)}")
    return flatten(subpaths)[0]


def signed_area(poly):
    """Twice-halved shoelace area; positive when clockwise on a y-down screen."""
    s = 0.0
    n = len(poly)
    for k in range(n):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % n]
        s += x0 * y1 - x1 * y0
    return s / 2


def rasterize(polygons, width, height, rule="nonzero"):
    """The pixels whose centres lie inside the polygons, by the given fill rule."""
    if rule not in ("nonzero", "evenodd"):
        raise ValueError(f"unknown fill rule {rule!r}")
    x0s, y0s, x1s, y1s = [], [], [], []
    for poly in polygons:
        n = len(poly)
        for k in range(n):
            a, b = poly[k], poly[(k + 1) % n]
            if a[1] != b[1]:
                x0s.append(a[0])
                y0s.append(a[1])
                x1s.append(b[0])
                y1s.append(b[1])
    mask = np.zeros((height, width), dtype=bool)
    if not x0s:
        return mask
    X0, Y0, X1, Y1 = (np.array(v, dtype=np.float64) for v in (x0s, y0s, x1s, y1s))
    up = Y1 > Y0
    lo = np.where(up, Y0, Y1)
    hi = np.where(up, Y1, Y0)
    wind = np.where(up, 1, -1)
    for j in range(height):
        yc = j + 0.5
        hit = (lo <= yc) & (yc < hi)
        if not hit.any():
            continue
        xs = X0[hit] + (yc - Y0[hit]) * (X1[hit] - X0[hit]) / (Y1[hit] - Y0[hit])
        ws = wind[hit]
        order = np.argsort(xs, kind="stable")
        xs, ws = xs[order], ws[order]
        acc = np.cumsum(ws)
        inside = acc != 0 if rule == "nonzero" else (np.arange(1, len(xs) + 1) % 2 == 1)
        for k in range(len(xs) - 1):
            if inside[k]:
                i0 = max(0, math.ceil(xs[k] - 0.5))
                i1 = min(width, math.ceil(xs[k + 1] - 0.5))
                if i1 > i0:
                    mask[j, i0:i1] = True
    return mask


def path_mask(d, width, height, rule="nonzero"):
    """The pixels inside SVG path data."""
    return rasterize(flatten(parse_path(d)), width, height, rule)


def mask_contours(mask):
    """Closed rectilinear loops along the pixel edges of a mask.

    Every loop runs clockwise around set pixels on a y-down screen, so holes run
    the other way, and either fill rule reproduces the mask exactly.  Where two
    set pixels touch only at a corner, the loop turns so as to keep them apart.
    """
    h, w = mask.shape
    m = np.zeros((h + 2, w + 2), dtype=bool)
    m[1:-1, 1:-1] = mask
    out = {}
    ys, xs = np.nonzero(mask)
    for y, x in zip(ys.tolist(), xs.tolist()):
        my, mx = y + 1, x + 1
        if not m[my - 1, mx]:
            out.setdefault((x, y), []).append((x + 1, y))
        if not m[my, mx + 1]:
            out.setdefault((x + 1, y), []).append((x + 1, y + 1))
        if not m[my + 1, mx]:
            out.setdefault((x + 1, y + 1), []).append((x, y + 1))
        if not m[my, mx - 1]:
            out.setdefault((x, y + 1), []).append((x, y))
    loops = []
    for start in sorted(out):
        while out.get(start):
            loop = [start]
            prev = start
            cur = out[start].pop(0)
            while cur != start:
                loop.append(cur)
                cands = out[cur]
                if len(cands) == 1:
                    nxt = cands.pop()
                else:
                    nxt = _right_turn(prev, cur, cands)
                    cands.remove(nxt)
                prev, cur = cur, nxt
            loops.append(_merge_collinear(loop))
        out.pop(start, None)
    return loops


def _right_turn(prev, cur, cands):
    dx, dy = cur[0] - prev[0], cur[1] - prev[1]
    right = (cur[0] - dy, cur[1] + dx)
    return right if right in cands else sorted(cands)[0]


def _merge_collinear(loop):
    n = len(loop)
    keep = []
    for k in range(n):
        a, b, c = loop[k - 1], loop[k], loop[(k + 1) % n]
        if (b[0] - a[0]) * (c[1] - b[1]) != (b[1] - a[1]) * (c[0] - b[0]):
            keep.append(b)
    return keep


def contour_path(loops):
    """Compact path data for rectilinear loops, using H and V."""
    out = []
    for loop in loops:
        parts = [f"M{loop[0][0]} {loop[0][1]}"]
        for a, b in zip(loop, loop[1:] + loop[:1]):
            if b == loop[0] and a == loop[-1]:
                break
            parts.append(f"H{b[0]}" if a[1] == b[1] else f"V{b[1]}")
        parts.append("Z")
        out.append("".join(parts))
    return " ".join(out)


def mask_path(mask):
    """Path data that reproduces a mask exactly; empty for an empty mask."""
    return contour_path(mask_contours(mask))


def convex_hull(points):
    """The convex hull of points, clockwise on a y-down screen."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    if signed_area(hull) < 0:
        hull.reverse()
    return hull
