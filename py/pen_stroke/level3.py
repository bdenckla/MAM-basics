"""Level 3: a stroke's shape class, from its median and nib alone.

The classes need no frame of reference: a bar is straight, not horizontal.
"""

import math

SHAPES = ("dot", "bar", "corner", "curve")

# A turn at one vertex of at least this many degrees makes a corner.
_CORNER_DEGREES = 60.0


def shape_class(points, nib):
    """The stroke's class: "dot", "bar", "corner" (one sharp turn) or "curve"."""
    pts = [p for k, p in enumerate(points) if k == 0 or p != points[k - 1]]
    length = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    if length <= max(2.0, 0.5 * nib.width):
        return "dot"
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    chord = math.dist(pts[0], pts[-1])
    if chord > 0:
        dev = max(
            abs((x1 - x0) * (y0 - py) - (x0 - px) * (y1 - y0)) / chord for px, py in pts
        )
        if dev <= max(1.0, 0.1 * length):
            return "bar"
    turns = []
    for a, b, c in zip(pts, pts[1:], pts[2:]):
        h1 = math.atan2(b[1] - a[1], b[0] - a[0])
        h2 = math.atan2(c[1] - b[1], c[0] - b[0])
        turns.append(abs(math.degrees((h2 - h1 + math.pi) % (2 * math.pi) - math.pi)))
    if sum(t >= _CORNER_DEGREES for t in turns) == 1:
        return "corner"
    return "curve"
