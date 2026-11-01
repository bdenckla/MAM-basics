"""Lint: every region-SVG in doc/pen-stroke-snips/ agrees with its crop and the profile.

WHY THIS EXISTS

A region-SVG is part authored (cuts, seeds, supplied outlines, groups, judgments) and part
derived (fills, image residual, each region's outline, each supplied outline's added ink),
and the derived parts are true only of the crop and the authored parts they came from.  This
lint derives them again and fails on any difference, so a cut or a seed edited without a
following ``py/main_pen_stroke.py regions-derive`` cannot stand.  It is a mechanical lint over
the tree.

WHAT IT CHECKS, for each region-SVG (``pen_stroke.region_derive.problems``)

1. The profile's structure: its closed sets of elements, classes, attributes, group kinds,
   ink owners, supplied values and judgments, and each region's id, rg and a number.
2. Ids are unique; every group holds regions or supplied ink of the same file, and every
   region and supplied ink is in a group; each group's ink owner suits the crop's subject,
   and ink of the line above or below has that line's text on the root; every cut is one
   path of straight segments; every supplied outline is closed and has a reason; every
   residual piece is judged.
3. The crop is beside the file, and its pixel size is the viewBox.
4. Level 1 is what the crop gives, as a stroke-SVG's is.
5. Every cut crosses ink; every seed lies in the ink and off the cuts; every piece of ink
   the cuts leave holds exactly one seed; and the ink under the cuts goes back to a region.
6. Each region's outline is what its seed and the cuts give, and each supplied outline's
   added ink is the outline less the ink, and is not empty.

A missing input fails: the directory must hold a region-SVG.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_ink_region_svgs.py
"""

import pytest

from mb_cmn import paths
from pen_stroke import region_derive
from pen_stroke import region_svg
from pen_stroke import tools

_SNIPS = paths.repo_root() / tools.SNIPS_DIR
_SVGS = region_svg.all_svgs(_SNIPS)


def test_the_directory_holds_region_svgs() -> None:
    assert _SVGS, f"no region-SVGs in {_SNIPS}"


@pytest.mark.parametrize("svg", _SVGS, ids=[p.name for p in _SVGS])
def test_region_svg_agrees_with_its_crop(svg) -> None:
    found = region_derive.problems(svg)
    assert not found, f"{svg.name}:\n  " + "\n  ".join(found)
