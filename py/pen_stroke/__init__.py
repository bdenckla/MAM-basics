"""The pen-stroke representation of a manuscript crop.

One crop of a manuscript page is described by a stroke-SVG beside it, under the
profile in doc/pen-stroke-representation.md: level 1, the ink as filled Bezier
outlines with an image residual; level 2, pen strokes, smooth medians swept with a
width that varies along them or by the crop's nib, with a pen residual; level 3,
each stroke's shape class; level 4, the writing frame; level 5, stroke groups
labelled with a kind congruent to a code point and with whose ink they are.
Medians, widths, ends, nibs, groups, the frame and the residual judgments are
authored; everything else is
derived by this package, and py/tests/test_pen_stroke_svgs.py checks every
stroke-SVG in doc/pen-stroke-snips/ against its crop.

The stroke-SVGs are a frozen record since 2026-11-01, when regions of ink
replaced the strokes.  A region-SVG beside each crop, under the profile in
doc/ink-region-representation.md, holds the same level 1, cuts across the ink,
regions with authored seeds and derived outlines, supplied ink, and the groups,
which hold regions in place of strokes; py/tests/test_ink_region_svgs.py checks
every region-SVG against its crop.
"""
