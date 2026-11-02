"""A newly bootstrapped ink-region glyph library must satisfy its own profile.

WHY THIS EXISTS

The no-library branch of regions-derive --copy-taamey-d creates a profile-2 library.
It needs drawn mark glyphs as well as the copied font outlines before it is written.

WHAT IT CHECKS

The real command handler, with committed font outlines supplied by a read-only stub,
writes a structurally valid new library without changing those copied outlines.
"""

from dataclasses import replace
from types import SimpleNamespace

import main_pen_stroke
from pen_stroke import glyph_library as glib


def test_a_new_library_contains_its_drawn_glyphs(tmp_path, monkeypatch) -> None:
    original = glib.read(glib.library_path(main_pen_stroke.tools.SNIPS_DIR))
    printed = [s for s in original.sources if s.is_taamey_d]
    expected = {s.id: s.outline for s in printed}

    def copy_committed_outlines(lib, _font_path):
        return replace(lib, sources=printed, taamey_d_sha256=original.taamey_d_sha256)

    monkeypatch.setattr(main_pen_stroke.tools, "SNIPS_DIR", tmp_path)
    monkeypatch.setattr(glib, "copy_taamey_d", copy_committed_outlines)
    main_pen_stroke._run_regions_derive(SimpleNamespace(copy_taamey_d=True, svgs=[]))

    made = glib.read(glib.library_path(tmp_path))
    assert made.profile == glib.PROFILE
    assert not glib.structural_problems(made)
    assert {s.id: s.outline for s in made.sources if s.is_taamey_d} == expected
