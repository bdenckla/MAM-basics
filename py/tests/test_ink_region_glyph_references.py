"""A malformed profile-3 glyph gets a diagnostic rather than a check traceback."""

import math

import numpy as np

from pen_stroke import glyph_library as glib
from pen_stroke import region_derive as rd
from pen_stroke import region_svg as rs
from pen_stroke import stroke_svg as ss


def test_a_glyph_of_a_missing_group_is_reported() -> None:
    rf = rs.RegionFile(20, 20, "synthetic.png", {}, 142, 0, 24, profile=rs.PROFILE_3)
    rf.regions = [rs.Region("rg1", ((3, 3),))]
    rf.groups = [ss.Group("g1", "pataḥ vowel", ["rg1"], ss.THIS_WORD)]
    rf.glyphs = [
        rs.Glyph("gl1", "g999", "", "square", (10, 10, math.log(8), math.log(8), 0, 0))
    ]
    source = glib.GlyphSource(
        "square",
        "pataḥ vowel",
        "",
        "Taamey D HEBREW POINT PATAH",
        "M-1 -1 L1 -1 L1 1 L-1 1 Z",
    )
    ink = np.ones((60, 60), dtype=bool)
    result = rd.glyph_ink(
        rf, ink, np.ones_like(ink, dtype=int), {"rg1": 1}, {}, glib.Library([source])
    )
    assert any(
        "data-group 'g999' is no group" in message for message in result.problems
    )
    assert not result.covered.any()
