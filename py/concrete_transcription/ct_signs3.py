"""Draft 3 of the trial: draft 2 changed as Ben asked on 2026-11-04.

Data of the concrete-transcription trial, 2026-11-04.  Ben wrote of
draft 2: "Please destroy the "bridge" between zayin and resh"; that the resh and
the stray mark "don't seem to intersect, they just seem to abut", and that the
stray mark's tail should be guessed and "extend into the resh", the resh's shape
under it guessed "(rounded, not straight as it is now!)"; and "Nun appears to
have some sharp edges at 3 of the 4 corners where the stray mark intercepts.
Smooth those out please."  The handoff concrete-transcription-handoff-2026-11-04.md
in the commander's shared notes folder planned this draft; its coordinates are
the image's pixels, measured at the level-1 threshold, 135.

1. A strip of vellum (VELLUM) takes the light ridge that joins the zayin's head
   to the resh's roof out of the ink, so that the two letters do not touch.
2. The stray stroke is draft 2's, Ben's centerline and his width fitted to the
   ink, with its start made round, so that its tail reaches about half its width
   into the resh: Ben's first choice, the two overlapping.
3. Three cuts give the letters their edges under the stroke, each a cubic Bezier
   curve sampled into straight segments, from vellum to vellum: the resh's lower
   left corner, rounded; and the nun's two edges, each tangent to the nun's
   visible edge above the stroke and below it.  Draft 2's cut along the stroke's
   outline is gone, so the nun's ink under the stroke joins its head and stem,
   and draft 1's seeds hold it.
4. The ink outside the letters' edges is the stray stroke's region; what of it
   the stroke does not cover is given an outline of its own in the stray
   stroke's group (STROKE_REST), so that hiding the stray stroke leaves the
   letters with none of it, and showing it holds all the image's ink.
5. The tracer's corners on the nun's and the resh's outlines where their hidden
   edges meet their visible ones are made smooth (SMOOTH).
"""

from concrete_transcription import ct_geometry as ctg
from concrete_transcription.ct_signs import GROUPS as _GROUPS_1
from concrete_transcription.ct_signs import (
    CLUSTERS,
    JUDGMENTS,
    PART_NAMES,
    SHORT,
    STROKE_REGION,
)  # noqa: F401
from concrete_transcription.ct_signs2 import STROKE as _STROKE_2

# Ben's stroke as draft 2 fitted it, its start round.
STROKE = dict(_STROKE_2, caps=["round", _STROKE_2["caps"][1]])

# The seeds that draft 3 changes, by region: the stroke's ink that shows,
# between the resh and the nun, and left of the nun, as draft 2 seeded it.
_SEEDS = {"rg20": [(168, 96.5), (126.5, 107)]}
GROUPS = [
    (gid, kind, owner, label, [(rid, _SEEDS.get(rid, seeds)) for rid, seeds in regs])
    for gid, kind, owner, label, regs in _GROUPS_1
]

# Strips of vellum: (id, line, width in pixels, why).  The zayin's head and the
# resh's roof meet at x 240 to 244, y 83 to 89, where a light ridge, luminance
# 107 to 130 against the threshold 135, the letters' cores 40 to 100, joins them.
VELLUM = [
    (
        "v1",
        "M 239.4 81.2 L 240.5 84.0 L 242.0 85.5 L 244.0 86.8 L 245.3 88.3 L 246.4 90.2",
        1.5,
        "the light ridge between the zayin's head and the resh's roof",
    ),
]

BEZIER_SEGMENTS = 16  # straight segments per sampled curve


def _curve(p0, c1, c2, p3):
    """A cubic Bezier curve as BEZIER_SEGMENTS straight segments, after its start."""
    pts = [
        ctg._bez(p0, c1, c2, p3, k / BEZIER_SEGMENTS)
        for k in range(1, BEZIER_SEGMENTS + 1)
    ]
    return "".join(f" L {ctg.fmt(x)} {ctg.fmt(y)}" for x, y in pts)


# The letters' edges under the stroke.  The resh: its left edge is x 171 at y 75
# to 82 and 170 at y 83 to 84; its roof's underside sags from y 95 at x 200 to
# 211 to y 101 at x 180 to 181, where the stroke's lower edge meets it.  The
# nun's right edge: x 162.0 for y 76 to 85, x 164.0 for y 115 to 125.  The nun's
# left edge: x 128 to 129 for y 89 to 93; below the stroke, the stem's edge, 139
# at y 121 to 122, 140 at 123 to 124, 141 at 125 to 126, a slope of one in two.
CUTS = [
    (
        "c1",
        "M 169 83.4 L 170.5 85"
        + _curve((170.5, 85), (170.5, 92), (176.9, 102.8), (180.5, 101))
        + " L 181.2 101.6",
        "the resh's lower left corner under the stroke's start, rounded",
    ),
    (
        "c2",
        "M 162.4 84.6 L 162 85.5"
        + _curve((162, 85.5), (162, 95.5), (164, 105), (164, 115))
        + " L 164.6 116",
        "the nun's right edge under the stroke",
    ),
    (
        "c3",
        "M 127.6 91.6 L 128.6 92"
        + _curve((128.6, 92), (128.6, 102), (134.5, 112.6), (139, 121.5))
        + " L 138.4 122.4",
        "the nun's left edge under the stroke",
    ),
]

# The stray stroke's ink that the stroke does not cover: the region STROKE_REGION
# less the stroke's samples, those of its pieces that reach farther than
# `reach` pixels from the stroke, each grown `overlap` pixels into the stroke so
# that the two meet without a seam.  ct_draft.py traces it; ct_shapes.py makes it
# an outline in the stroke's group.
STROKE_REST = {
    "id": "rg20",
    "part": "where it meets the letters",
    "reach": 1.3,
    "overlap": 0.7,
}

# Boxes (x0, y0, x1, y1), by region, within which the outline's control points are
# smooth, not corners.
SMOOTH = {}

DRAFT_VERSION = "draft 3, Claude, 2026-11-04"
MADE = "2026-11-04"
DRAFT_NOTE = (
    " <strong>This is the third draft</strong>, made from your comments on the second."
    " The zayin and the resh no longer touch: a strip of vellum takes the faint bridge"
    " between them out of the ink. The stray stroke's right end is now round and runs"
    " into the resh, over the resh's lower left corner, which Claude has drawn rounded"
    " under it. The nun's two edges under the stroke now curve from its edges above the"
    " stroke to its edges below it, with no corners. The stray stroke's ink beside the"
    " stroke, where it meets the letters, has an outline of its own, which the stray"
    " stroke's checkbox hides with the stroke."
)
DOWNLOAD_NAME = "concrete-transcription-2026-11-03-draft-3-edits.json"
QUESTIONS = [
    {"letter": "A", "ring": [176, 92, 8], "text": [186, 108]},
    {"letter": "B", "ring": [163, 100, 6], "text": [172, 115]},
    {"letter": "B", "ring": [133.5, 106, 6], "text": [116, 98]},
]
QUESTION_ITEMS = [
    (
        "A",
        "Under the stray stroke's right end, the resh's lower left corner cannot be"
        " seen. Claude has drawn it rounded, and the stroke's round end runs over it into"
        " the resh. Drag the resh's outline, or the stroke's right end, where you infer"
        " them.",
    ),
    (
        "B",
        "Under the stroke, the nun's two edges cannot be seen. Each now curves from"
        " where it shows above the stroke to where it shows below it. Drag the nun's"
        " outline where you infer them.",
    ),
]
QUESTION_LETTERS = "A and B"
