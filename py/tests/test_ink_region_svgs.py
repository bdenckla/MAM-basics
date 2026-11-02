"""Lint: every region-SVG in doc/pen-stroke-snips/, and the library of glyphs there, agrees
with its crops and the profile.

WHY THIS EXISTS

A region-SVG is part authored (seeds, cuts, strips of supplied vellum, overlaps' outlines,
supplied outlines, groups, judgments, and under profile 3 each glyph's group, part, glyph
and fit) and part derived (fills, image residual, each region's outline, each overlap's
ink, each supplied outline's added ink, and under profile 3 each glyph's outline and ink
and each overlap of glyphs), and the derived parts are true only of the crop and the
authored parts they came from.  This lint derives them again and fails on any difference,
so a seed or a cut edited without a following ``py/main_pen_stroke.py regions-derive``
cannot stand.  The library's glyphs of the scribe's are derived from their crops in the
same way.  It is a mechanical lint over the tree.

WHAT IT CHECKS, for each region-SVG (``pen_stroke.region_derive.problems``)

1. The profile's structure: its closed sets of elements, classes, attributes, group kinds,
   ink owners, supplied values and judgments, and each region's id, rg and a number.
2. Ids are unique; every group holds regions, overlaps or supplied ink of the same file;
   every region is in one group, every overlap in two or more, and every supplied ink in
   one or more; each group's ink owner suits the crop's subject, and ink of the line above
   or below has that line's text on the root; a group whose kind has several written parts
   holds as many members, or says why not; every cut and strip of vellum is one path of
   straight segments; every overlap's and supplied outline is closed, and every supplied
   outline has a reason; every residual piece is judged.
3. The crop is beside the file, and its pixel size is the viewBox.
4. Level 1 is what the crop gives, as a stroke-SVG's is.
5. Every strip of vellum takes out ink and every cut crosses it; every seed lies in the ink,
   off the cuts and out of the vellum, and no two regions' seeds move to one sample; every
   piece of ink the cuts leave holds a seed; the ink under the cuts goes back to a region;
   and every overlap takes ink that no other overlap takes.
6. Each region's outline is what the watershed from its seeds, the cuts, the vellum and the
   overlaps give; each overlap's ink is the ink inside its outline; and each supplied
   outline's added ink is the outline less the ink, and is not empty.
7. Under profiles 3 and 4: every fitted group's written part has one glyph and no other
   group has one; every glyph's glyph is in the library, of its group's kind and part, and
   its fit has a letter's or a mark's numbers; every glyph holds ink, crosses no strip of
   vellum or cut by more than a pixel, and has the outline its glyph and fit give; and
   each glyph's ink, each overlap of glyphs and each region's ink inside no glyph are
   what the glyphs give.
8. Under profile 4: the library is of profile 2; every break of a group or a glyph names
   a guideline and gives a reason with whose word it is and when; and a glyph that breaks
   no guideline follows them: a mark's glyph is drawn where its part has a drawn shape, a
   glyph of the scribe's that is not judged serves only a group that breaks preserved,
   and a letter's outline moves along its normal at most its limit, and not at all where
   it breaks area.
9. The library: its closed table agrees with the parts rule; every glyph is of a fitted
   kind and one of its written parts; Taamey D's glyphs cover every such part, under the
   font's SHA-256; each glyph of the scribe's is the outline its crop's draft gives its
   group, a letter that meets no edge of its crop and touches no other group's ink, or
   says why it serves even so; and under profile 2, each glyph crop's outline is the ink
   inside its lasso that its PNG gives, each drawn glyph is its shape's outline, the drawn
   glyphs cover every part with a shape, and each glyph of the scribe's is judged, with
   whose judgment it is and when, or breaks preserved.

A missing input fails: the directory must hold a region-SVG and the library.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_ink_region_svgs.py
"""

import pytest

from mb_cmn import paths
from pen_stroke import glyph_library
from pen_stroke import region_derive
from pen_stroke import region_svg
from pen_stroke import tools

_SNIPS = paths.repo_root() / tools.SNIPS_DIR
_SVGS = region_svg.all_svgs(_SNIPS)
_LIBRARY = glyph_library.library_path(_SNIPS)


def test_the_directory_holds_region_svgs() -> None:
    assert _SVGS, f"no region-SVGs in {_SNIPS}"


def test_the_library_agrees_with_its_crops() -> None:
    assert _LIBRARY.exists(), f"no library of glyphs at {_LIBRARY}"
    found = region_derive.library_problems(_LIBRARY)
    assert not found, f"{_LIBRARY.name}:\n  " + "\n  ".join(found)


@pytest.mark.parametrize("svg", _SVGS, ids=[p.name for p in _SVGS])
def test_region_svg_agrees_with_its_crop(svg) -> None:
    found = region_derive.problems(svg)
    assert not found, f"{svg.name}:\n  " + "\n  ".join(found)
