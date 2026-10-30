"""Lint: every stroke-SVG in doc/pen-stroke-snips/ agrees with its crop and the profile.

WHY THIS EXISTS

A stroke-SVG is part authored (medians, nibs, groups, frame, judgments) and part derived
(fills, image residual, each stroke's ink and shape, pen residual), and the derived parts
are true only of the crop and the authored parts they came from.  This lint derives them
again and fails on any difference, so a median edited without a following
``py/main_pen_stroke.py derive`` cannot stand.  It is a mechanical lint over the tree.

WHAT IT CHECKS, for each stroke-SVG (``pen_stroke.derive.problems``)

1. The profile's structure: its closed sets of elements, classes, attributes, nibs,
   stroke-group kinds, judgments and shapes.
2. Ids are unique; every group holds strokes of the same file; every stroke is in a
   group; each stroke's nib is the nib of its groups' kinds; every residual piece is
   judged; the frame is there.
3. The crop is beside the file, and its pixel size is the viewBox.
4. The fills are the tracer's outlines of the crop's ink at the stated threshold and
   speck size.
5. The residual pieces, smoothing slivers, halo and pen residual are what the crop gives.
6. Each stroke's ink is its median swept by its nib, and its shape is its median's.

A missing input fails: the directory must hold a stroke-SVG.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_pen_stroke_svgs.py
"""

import pytest

from mb_cmn import paths
from pen_stroke import derive
from pen_stroke import tools

_SNIPS = paths.repo_root() / tools.SNIPS_DIR
_SVGS = tools.all_svgs(_SNIPS)


def test_the_directory_holds_stroke_svgs() -> None:
    assert _SVGS, f"no stroke-SVGs in {_SNIPS}"


@pytest.mark.parametrize("svg", _SVGS, ids=[p.name for p in _SVGS])
def test_stroke_svg_agrees_with_its_crop(svg) -> None:
    found = derive.problems(svg)
    assert not found, f"{svg.name}:\n  " + "\n  ".join(found)
