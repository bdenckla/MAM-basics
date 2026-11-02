"""Differential: the fit's rasterizer against pen_stroke.geometry.rasterize.

WHY THIS EXISTS

The fit of a fitted word (pen_stroke.glyph_fit) scores thousands of placements of each
glyph, so it rasterizes them with a vectorized rasterizer of its own, counted in a window
round the glyph rather than over the whole grid.  The ink-region profile requires that it
decide every sample exactly as geometry.rasterize, the rasterizer of every other derived
part, decides it.  This test compares the two on independent terms: geometry.rasterize,
which sorts each row's crossings, is the oracle.

WHAT IT CHECKS

For every glyph of the library doc/pen-stroke-snips/glyphs.svg, placed by a turn, a shear,
two scales and, for a letter, a warp; and for every glyph of every profile-3 region-SVG,
by its outline as written: the fit's rasterizer, over the whole grid and in the glyph's
window, gives exactly the samples that geometry.rasterize gives.  It fails if it finds no
glyph to compare.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_glyph_raster.py
"""

import math

import numpy as np
import pytest

from mb_cmn import paths
from pen_stroke import geometry as geo
from pen_stroke import glyph_fit as gf
from pen_stroke import glyph_library as glib
from pen_stroke import level5
from pen_stroke import region_svg as rsvg
from pen_stroke import tools

_SNIPS = paths.repo_root() / tools.SNIPS_DIR
_LIBRARY = glib.library_path(_SNIPS)
# The grid, in crop pixels, on which a library glyph is placed.
_SIDE = 40


def _library_cases():
    if not _LIBRARY.exists():
        return []
    lib = glib.read(_LIBRARY)
    out = []
    for k, src in enumerate(lib.sources):
        glyph = gf.Glyph(glib.contours(src))
        prm = np.array([20.0, 20.0, math.log(14.0), math.log(12.5), 0.2, 0.1])
        warp = None
        if level5.pass_of(src.kind) == level5.LETTERS:
            warp = 0.04 * np.sin(np.arange(gf.WARP_SIZE) + k)
        out.append((src.id, _SIDE, _SIDE, glyph.place(prm, warp)))
    return out


def _region_cases():
    out = []
    for svg in rsvg.all_svgs(_SNIPS):
        rf = rsvg.read(svg)
        for gl in rf.glyphs:
            polys = [
                np.array(p, dtype=float)
                for p in geo.flatten(geo.parse_path(gl.outline))
            ]
            out.append((f"{svg.name} {gl.id}", rf.width, rf.height, polys))
    return out


_CASES = _library_cases() + _region_cases()


def test_there_are_glyphs_to_compare() -> None:
    assert _CASES, f"no glyphs in {_LIBRARY} or in the region-SVGs of {_SNIPS}"


@pytest.mark.parametrize("case", _CASES, ids=[c[0] for c in _CASES])
def test_the_fits_rasterizer_is_geometrys(case) -> None:
    _, width, height, polys = case
    grid = gf.Grid(width, height)
    q = grid.samples(polys)
    oracle = geo.rasterize([[tuple(p) for p in poly] for poly in q], grid.gw, grid.gh)
    assert oracle.any(), "the placed glyph holds no sample"
    assert np.array_equal(gf.rasterize(q, grid.gw, grid.gh), oracle)
    win, m = grid.placed(polys)
    assert np.array_equal(grid.full(polys), oracle)
    assert m.sum() == oracle.sum(), f"the window {win} leaves out samples"


@pytest.mark.parametrize("offset", [(-500, 0), (500, 0), (0, -500), (0, 500)])
def test_an_off_grid_glyph_has_no_samples(offset) -> None:
    """A fit can place a glyph outside the padded grid; its window must be empty."""
    poly = np.array([(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)]) + offset
    grid = gf.Grid(20, 20)
    oracle = geo.rasterize(
        [[tuple(p) for p in q] for q in grid.samples([poly])], grid.gw, grid.gh
    )
    assert not oracle.any()
    assert np.array_equal(grid.full([poly]), oracle)
