"""Tests for the per-line transcription editor's crop diagnostics.

``crop_warnings`` exists because both ways of misplacing a vertical crop are SILENT: the debug
overlay draws a plausible band for a clipped line and for a merged one alike.  The numbers
below are the real ones from Koren A5-D-281, where both mistakes were made in one sitting.

BLESSED EXAMPLE-BASED FILE (issue wlc-utils#88).  The hand-picked band geometries, the synthesized row
profiles and the drawn pages are all the shape ``doc/agent-planning-principles.md`` otherwise
forbids.  Kept, because these diagnostics have no oracle to differ against and produce no
tracked output to diff: the input is a scan, the failure is silent by construction, and the only
statable check is that a page shaped like the one that broke yields the warning it should.  The
synthetic profiles are scaled versions of that real page precisely so the numbers stay readable
as the page, not as magic constants.
"""

from PIL import Image, ImageDraw

from accgram.transcription_editor import (
    DETECT_MARGIN_FALLBACK,
    SMOOTH_RADIUS,
    band_context,
    band_rows,
    crop_and_resize,
    crop_warnings,
    detect_margin,
    find_bands,
    median_pitch,
    rendered_region,
    row_profile,
    smooth,
)

MEDIAN = 64  # a printed line on that page, in rendered pixels


def _levels(warnings):
    return [level for level, _ in warnings]


def test_a_crop_clear_of_its_neighbours_says_nothing():
    """The quiet case: every band a full line, none touching an edge."""
    bands = [(10, 74), (100, 164), (190, 254)]
    assert crop_warnings(bands, height=300) == []


def test_a_band_that_absorbed_a_clipped_sliver_warns():
    """Koren p. 281 at bottom 0.614: band 17 came out 117px against a median of 64.

    ``_absorb_slivers`` folds a sub-half-line fragment into its neighbour, which is right for
    a fragment shaved off by a split and wrong for a genuine next line the crop cut through.
    """
    bands = [(10, 74), (100, 217), (240, 304)]
    warnings = crop_warnings(bands, height=400)
    assert _levels(warnings) == ["WARNING"]
    assert "117px" in warnings[0][1] and "64px" in warnings[0][1]


def test_a_band_touching_the_crop_edge_is_a_note_not_a_warning():
    """Ambiguous by construction, so it must not cry wolf.

    On a CORRECT crop the outermost band is the half-line of context the Hebrew cropping rule
    asks for, and it necessarily touches the edge; on a wrong one it is a transcribed line cut
    short.  Both are simply short, so the geometry cannot separate them and the message states
    both readings instead of asserting one.
    """
    for bands, height in (([(0, 64), (100, 164)], 200), ([(10, 74), (100, 164)], 164)):
        warnings = crop_warnings(bands, height)
        assert _levels(warnings) == ["note"], bands
        assert "clipped if it is a line you mean to transcribe" in warnings[0][1]


def test_the_merge_trap_reports_both_at_once():
    """The 0.614 crop really did trip both: an over-tall band that also touched the edge."""
    bands = [(10, 74), (100, 164), (190, 307)]
    assert _levels(crop_warnings(bands, height=307)) == ["WARNING", "note"]


def test_no_bands_is_not_an_error():
    assert crop_warnings([], height=100) == []


# ---------------------------------------------------------------------------
# Trailing-line recovery.  Koren hangs a Decalogue's closing word on a line of its own; being
# horizontally short it clears the ink cutoff only faintly and only in fragments, so the
# min-height filter drops it as speckle -- a silent hole.  ``find_bands`` recovers it as a final
# band, but only from BELOW the last kept band, so the recovery cannot renumber a line already
# found: it is purely additive at the tail.  The numbers below are scaled so the cutoff lands at
# 0.04 (baseline 0 + INK_CUTOFF * a busy row of 0.5), a full line's ink is 60 * 0.5 = 30, and a
# single line stands 60px tall -- the same shape as the real Koren page, in round figures.

FULL_VALUE = 0.5  # a full line's per-row ink fraction; the cutoff falls at 0.04
# Five full printed lines: height 60, gaps 40 (wider than any within-line accent gap).
LINES = [(40, 100), (140, 200), (240, 300), (340, 400), (440, 500)]
BASE = [(a, b, FULL_VALUE) for a, b in LINES]


def _profile(length, blocks):
    """A row profile ``length`` rows long, blank but for ``blocks`` of ``(top, bottom, value)``."""
    prof = [0.0] * length
    for top, bottom, value in blocks:
        for i in range(top, bottom):
            prof[i] = value
    return prof


def test_a_hung_closing_word_is_recovered_as_a_final_band():
    """The bug: a short final line, split by sub-cutoff gaps into fragments each too short to
    keep and too far apart to merge, vanished entirely.

    Three faint clusters (0.06, just over the 0.04 cutoff) at 25px spacing stand in for the word;
    individually they are specks, together they are a line half again as tall as the threshold.
    """
    word = BASE + [
        (540, 548, 0.06),
        (548, 573, 0.02),  # sub-cutoff gap between letter cores
        (573, 580, 0.06),
        (580, 605, 0.02),
        (605, 609, 0.06),
    ]
    bands = find_bands(_profile(730, word))
    assert len(bands) == 6
    # Additive at the tail: the five full lines are untouched, the recovered word is appended.
    assert bands[:5] == [(40, 100), (140, 200), (240, 300), (340, 400), (440, 500)]
    assert bands[5] == (540, 609)  # bracketed from its first to its last inked row


def test_a_blank_bottom_margin_is_not_recovered_as_a_line():
    """The ordinary correct case: nothing hangs below the last line, so nothing is invented."""
    assert find_bands(_profile(730, BASE)) == [
        (40, 100),
        (140, 200),
        (240, 300),
        (340, 400),
        (440, 500),
    ]


def test_a_thin_decorative_rule_is_not_recovered():
    """A decorative rule is dense enough to clear the cutoff but only a few rows tall.  It fails
    the height gate -- a real line stands half a line tall even when it is horizontally short.
    """
    rule = BASE + [(540, 543, 0.7)]  # 3px, near-full width: high ink, no height
    assert len(find_bands(_profile(730, rule))) == 5


def test_a_faint_smudge_spanning_half_a_line_is_not_recovered():
    """The height gate alone would pass this: two faint marks 30px apart span half a line.  The
    ink gate is what rejects it -- there is too little ink between and within them to be a word.
    """
    smudge = BASE + [(540, 544, 0.045), (544, 574, 0.015), (574, 578, 0.045)]
    assert len(find_bands(_profile(730, smudge))) == 5


def test_a_line_clipped_to_a_stub_at_the_crop_bottom_is_not_recovered():
    """Word-like ink, but jammed against the image bottom with no margin below.  That is the
    signature of a next line the crop cut through, which ``crop_warnings`` should flag -- not a
    whole hung line to recover.  The bottom-clearance gate leaves it alone."""
    clipped = BASE + [
        (540, 548, 0.06),
        (548, 573, 0.02),
        (573, 580, 0.06),
        (580, 605, 0.02),
        (605, 611, 0.06),  # runs to the image bottom at 612
    ]
    assert len(find_bands(_profile(612, clipped))) == 5


# ---------------------------------------------------------------------------
# Crop split (issue wlc-utils#71).  --crop's top/bottom name the lines to transcribe; detection runs over
# a region grown about a line past them, and the neighbours it pulls in are classified as context
# by where their centres fall.  So the reader crops to just the wanted lines and the old dead zone
# -- a vertical bound between the two good placements that clipped a line or absorbed a sliver --
# is unreachable, since the region detected over is no longer theirs to choose.


def test_median_pitch_is_the_line_to_line_spacing():
    assert median_pitch([(0, 50), (100, 150), (200, 250)]) == 100  # tops 0,100,200


def test_median_pitch_needs_two_bands():
    assert median_pitch([(0, 50)]) is None
    assert median_pitch([]) is None


def test_detect_margin_is_one_pitch_in_source_fractions():
    """Two-plus bands: a whole pitch, converted from rendered to source px and to a page fraction.
    100px pitch * scale 2.0 = 200 source px, over a 1000px page = 0.2."""
    assert (
        detect_margin([(0, 40), (100, 140)], probe_scale=2.0, source_height=1000) == 0.2
    )


def test_detect_margin_falls_back_to_a_lone_lines_own_height():
    """One requested line has no pitch, so its own height stands in: the line is kept off the edge
    even though its neighbours are not pulled into view.  50px * 2.0 / 1000 = 0.1."""
    assert detect_margin([(10, 60)], probe_scale=2.0, source_height=1000) == 0.1


def test_detect_margin_falls_back_to_a_page_fraction_when_nothing_detected():
    assert (
        detect_margin([], probe_scale=2.0, source_height=1000) == DETECT_MARGIN_FALLBACK
    )


def test_band_context_is_by_centre_against_the_requested_range():
    """crop [_, 0.2, _, 0.6] over a 1000px page asks for source rows 200..600.  With origin 100
    and scale 1.0 (source = 100 + rendered), the outer two bands centre outside it and are
    context; the inner two centre inside and are lines to transcribe."""
    bands = [
        (40, 60),
        (140, 160),
        (440, 460),
        (540, 560),
    ]  # centres 50,150,450,550 rendered
    flags = band_context(
        bands, [0.0, 0.2, 1.0, 0.6], origin=100, scale=1.0, source_height=1000
    )
    assert flags == [True, False, False, True]  # source centres 150,250,550,650


def test_band_rows_numbers_transcribable_lines_and_sets_context_aside():
    bands = [(40, 60), (140, 160), (440, 460), (540, 560)]
    flags = [True, False, False, True]
    rows, context_rows = band_rows(bands, flags, height=800, origin=100, scale=1.0)
    assert [r["n"] for r in rows] == [
        1,
        2,
    ]  # numbered 1..k over the transcribable bands alone
    assert [r["px"] for r in rows] == [[140, 160], [440, 460]]
    assert rows[0]["px_source"] == [240, 260]  # origin 100 + rendered, scale 1.0
    assert [c["px"] for c in context_rows] == [[40, 60], [540, 560]]
    assert all("n" not in c for c in context_rows)  # context has no line number


def _page(width, height, pitch, band_h, top0, n_lines):
    """A plain synthetic page: ``n_lines`` full-width ink bars, evenly spaced, on white."""
    img = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(img)
    lines = []
    for i in range(n_lines):
        top = top0 + i * pitch
        draw.rectangle([width // 8, top, width - width // 8, top + band_h], fill=0)
        lines.append((top, top + band_h))
    return img, lines


def _grow_and_classify(img, lines, lo_idx, hi_idx, width=1200):
    """Run the editor's grow-then-classify pipeline exactly as ``run`` composes it, over a crop
    set tight to lines ``lo_idx..hi_idx`` -- the new 'the lines I want' meaning."""
    height = img.height
    crop = [0.05, lines[lo_idx][0] / height, 0.95, lines[hi_idx][1] / height]
    probe, _, probe_scale = crop_and_resize(img, crop, width)
    probe_bands = find_bands(smooth(row_profile(probe), SMOOTH_RADIUS))
    margin = detect_margin(probe_bands, probe_scale, height)
    detect_crop = [
        crop[0],
        max(0.0, crop[1] - margin),
        crop[2],
        min(1.0, crop[3] + margin),
    ]
    rendered, origin, scale = crop_and_resize(img, detect_crop, width)
    bands = find_bands(smooth(row_profile(rendered), SMOOTH_RADIUS))
    flags = band_context(bands, crop, origin, scale, height)
    return band_rows(bands, flags, rendered.height, origin, scale)


def test_a_tight_crop_of_a_middle_run_transcribes_exactly_those_lines():
    """The whole point: crop to just the wanted lines and get exactly them, their neighbours held
    aside as context rather than clipped into the boundary bands or merged with them."""
    img, lines = _page(400, 1600, pitch=130, band_h=40, top0=150, n_lines=10)
    rows, context_rows = _grow_and_classify(img, lines, 3, 6)

    assert len(rows) == 4  # exactly the four requested lines
    assert len(context_rows) >= 1  # at least one neighbour pulled in as context
    centres = [sum(r["px_source"]) / 2 for r in rows]
    matched = {
        min(range(len(lines)), key=lambda i: abs(sum(lines[i]) / 2 - c))
        for c in centres
    }
    assert matched == {
        3,
        4,
        5,
        6,
    }  # each transcribable row sits on a requested source line


def test_a_crop_at_the_top_grows_only_downward():
    """The grow clamps at the page edge, so a top-of-page run has context only below it -- and
    still transcribes exactly its own lines, none clipped by sitting against the top."""
    img, lines = _page(400, 1600, pitch=130, band_h=40, top0=150, n_lines=10)
    rows, _ = _grow_and_classify(img, lines, 0, 2)
    centres = [sum(r["px_source"]) / 2 for r in rows]
    matched = {
        min(range(len(lines)), key=lambda i: abs(sum(lines[i]) / 2 - c))
        for c in centres
    }
    assert len(rows) == 3 and matched == {0, 1, 2}


# --------------------------------------------------------------------------- #
# The export-format rule wlc-utils#71 introduced (see ``rendered_region``)
# --------------------------------------------------------------------------- #
def test_rendered_region_reads_a_post_71_export_off_detect_crop():
    """With a grow, ``crop`` is the lines requested and ``detect_crop`` the region rendered."""
    render = {
        "crop": [0.05, 0.30, 0.95, 0.50],
        "detect_crop": [0.05, 0.26, 0.95, 0.54],
        "width": 1200,
    }
    assert rendered_region(render) == [0.05, 0.26, 0.95, 0.54]


def test_rendered_region_reads_a_pre_71_export_off_crop():
    """No ``detect_crop`` is the OLD format, whose ``crop`` already meant the region rendered --
    every transcription committed so far is this shape, and none will be rewritten."""
    render = {"crop": [0.05, 0.26, 0.95, 0.54], "width": 1200}
    assert rendered_region(render) == [0.05, 0.26, 0.95, 0.54]


def test_rendered_region_is_none_for_a_whole_page_export():
    """A whole-page render grows nothing and writes ``crop: null``; the region is the page."""
    assert rendered_region({"crop": None, "width": 1200}) is None


def test_rendered_region_agrees_with_crop_horizontally_on_every_committed_export():
    """The two formats never differed left-to-right, which is what lets ``zoom_line`` keep
    reading ``crop`` for its column bounds.  Asserted over the real exports, not a fixture.
    """
    import json

    from accgram import edition_transcription as et

    exports = sorted(et.transcriptions_dir().glob("*.json"))
    assert exports, "no editor exports committed"
    for path in exports:
        record = json.loads(path.read_text(encoding="utf-8"))
        for page in record.get("pages", [record]):
            render = page["render"]
            region, crop = rendered_region(render), render["crop"]
            if crop is None:
                assert region is None
            else:
                assert (region[0], region[2]) == (crop[0], crop[2]), path.name
