"""Draft 2 of the trial: Claude's reading re-seeded from Ben's edits of draft 1.

Data of the concrete-transcription trial, 2026-11-03.  Ben exported his edits of
draft 1's page, doc/concrete-transcription-2026-11-03/edits/ben-edits-1.json,
and then wrote: "BTW there's
nothing sacred about my edits... if you want to use them as guidelines
re-seeding your own analysis/shapes, that's fine!"

Draft 2 takes the stray stroke as Ben drew it, which starts at the resh's lower
left corner, its width fitted to the ink (WIDEN, below), and makes a cut of the
outline of the same stroke made
wider by BLUR on each side, its start where Ben put it: the letters take all the
ink outside that, the resh by draft 1's seeds, and ink within BLUR of the stroke
is the stroke's blur, as the page counts blur.  (A cut along the stroke's own
outline gave the resh a hairline of the stroke's blur along its whole lower
edge.)  Inside the cut, two more cuts give the nun the ink between its edges,
which continue its edges above and below the stroke in straight lines; the rest
is the stroke's ink that shows.  Ben's own outline of the resh is not used: the
resh is traced again.  Everything else is draft 1's, from ct_signs.
"""

import json

from mb_cmn import paths
from concrete_transcription import ct_geometry as ctg
from concrete_transcription.ct_signs import GROUPS as _GROUPS_1
from concrete_transcription.ct_signs import (
    CLUSTERS,
    JUDGMENTS,
    PART_NAMES,
    SHORT,
    STROKE_REGION,
)  # noqa: F401

_EDITS = (
    paths.repo_root() / "doc/concrete-transcription-2026-11-03/edits/ben-edits-1.json"
)
_BEN = {s["id"]: s for s in json.loads(_EDITS.read_text(encoding="utf-8"))["changed"]}

# Ben's stroke, its width fitted to the ink: Ben's centerline and caps, and his
# width made wider by WIDEN, the least, in tenths of a pixel, that leaves none of
# the ink about the stroke farther than 1.3 px from every shape, as the page
# counts.  At Ben's width a hairline of the ink's lower edge, under the stroke
# from the resh to the nun and under its round end, lay just beyond that; at this
# width the stroke reaches beyond the ink by a third of a pixel's area in all.
WIDEN = 0.5
STROKE = {
    "id": "st1",
    "group": "g14",
    "centerline": [tuple(p) for p in _BEN["st1"]["centerline"]],
    "width": round(_BEN["st1"]["width"] + WIDEN, 2),
    "caps": list(_BEN["st1"]["caps"]),
}

# The seeds that draft 2 changes, by region.
_SEEDS = {
    # The stroke's ink that shows: between the resh and the nun, and left of the nun.
    "rg20": [(168, 96.5), (126.5, 107)],
    # The nun: draft 1's seeds, and one for its ink under the stroke, which the
    # stroke's outline cuts off from the rest of the nun.
    "rg15": [(140, 62), (152, 140), (110, 180), (147, 106)],
}
GROUPS = [
    (gid, kind, owner, label, [(rid, _SEEDS.get(rid, seeds)) for rid, seeds in regs])
    for gid, kind, owner, label, regs in _GROUPS_1
]

BLUR = 1.3  # pixels, as ct_share.NEAR and the page's NEAR count blur

# The nun's edges under the stroke: each runs straight from the nun's edge where
# it shows just above the stroke to where it shows just below it, and each cut a
# little beyond c1, so that it meets it.  The right edge: x 162 at y 85, x 164 at
# y 115.  The left edge: x 128.5 at y 93, the inner corner of the head, x 139 at
# y 121.5, the stem's edge below the stroke's lower fillet.
CUTS = [
    (
        "c1",
        ctg.stroke_d(STROKE["centerline"], STROKE["width"] + 2 * BLUR, STROKE["caps"]),
        "the stray stroke as Ben drew it, with its blur",
    ),
    ("c2", "M 162.16 87.4 L 163.87 113", "the nun's right edge under the stroke"),
    ("c3", "M 129.42 95.5 L 137.92 118.6", "the nun's left edge under the stroke"),
]

DRAFT_VERSION = "draft 2, Claude, 2026-11-03"
DRAFT_NOTE = (
    " <strong>This is the second draft.</strong> Its stray stroke is the one you drew on"
    " the first draft's page, which begins at the resh's lower left corner, made a hair"
    " wider so that it reaches the edge of its ink; Claude then traced the letters again"
    " so that they hold all the ink outside the stroke."
)
DOWNLOAD_NAME = "concrete-transcription-2026-11-03-draft-2-edits.json"
QUESTIONS = [
    {"letter": "A", "ring": [163, 100, 6], "text": [172, 115]},
    {"letter": "A", "ring": [133.5, 106, 6], "text": [116, 98]},
]
QUESTION_ITEMS = [
    (
        "A",
        "Under the stroke, the nun's two edges, which cannot be seen, run straight from"
        " where they show above the stroke to where they show below it. Drag the nun's"
        " outline where you infer them.",
    ),
]
QUESTION_LETTERS = "A"
