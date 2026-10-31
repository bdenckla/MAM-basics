"""Level 3: a stroke's shape class, from its median and widths alone.

The classes need no frame of reference: a bar is straight, not horizontal.
"""

import math

from pen_stroke import curve

SHAPES = ("dot", "bar", "corner", "curve")

# A turn of at least this many degrees where two segments meet makes a corner.
_CORNER_DEGREES = 60.0


def shape_class(segs, widths):
    """The stroke's class: "dot", "bar", "corner" (one sharp turn) or "curve"."""
    length = curve.length(segs)
    sws = curve.segment_widths(widths, len(segs))
    widest = max(curve.width(ws, k / 16) for ws in sws for k in range(17))
    if length <= max(2.0, 0.5 * widest):
        return "dot"
    pts = [curve.point(seg, k / 32) for seg in segs for k in range(33)]
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    chord = math.dist(pts[0], pts[-1])
    if chord > 0:
        dev = max(
            abs((x1 - x0) * (y0 - py) - (x0 - px) * (y1 - y0)) / chord for px, py in pts
        )
        if dev <= max(1.0, 0.1 * length):
            return "bar"
    if sum(t >= _CORNER_DEGREES for t in curve.join_turns(segs)) == 1:
        return "corner"
    return "curve"
