"""The pen-stroke representation of a manuscript crop.

One crop of a manuscript page is described by a stroke-SVG beside it, under the
profile in doc/pen-stroke-representation.md: level 1, the ink as filled Bezier
outlines with an image residual; level 2, pen strokes swept by a flat nib with a
pen residual; level 3, each stroke's shape class; level 4, the writing frame;
level 5, stroke groups labelled with a kind congruent to a code point.  Medians,
groups, the frame and the residual judgments are authored; everything else is
derived by this package, and py/tests/test_pen_stroke_svgs.py checks every
stroke-SVG in doc/pen-stroke-snips/ against its crop.
"""
