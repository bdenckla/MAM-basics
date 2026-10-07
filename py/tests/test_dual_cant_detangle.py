"""Stage-2 of issue wlc-utils#36: the dual-cantillation detangler.

Drives all three loci (Gen 35:22 + the two Decalogues) through the detangler and the
*existing* prose grammar.  The corpus-backed assertions FAIL, rather than skipping, when the
WLC 4.22 kq-u corpus or MAM-simple is missing: the corpus is committed in this repo's ``out/``,
so its absence means a tracked file was deleted, and MAM-simple's absence is a
misconfiguration ``paths.require_mam_simple_dir`` answers with both env overrides.  See
``paths.require_sibling`` for the argument.

What the detangler finds is recorded in tracked outputs, whose diffs show any change to it:
``run-dual-cant`` writes each reading's chanted-verse trees, the supplied marks and the
anomalies to ``out/accgram/dual-cant/_dual_cant.json``; ``generate-html`` renders the supplied
marks as ``gh-pages/wlc/accgram/supplied-marks.html``; and ``run-prose`` folds the ungrammatical
chanted verses into ``out/accgram/prose/wlc_422_ps_<bb>_ag.json``, which the ungrammatical-verse
page ``gh-pages/wlc/accgram/goerwitz.html`` renders.  The tests below check the rules those
outputs rest on:

  * each strand has one chanted verse per sof pasuq of MAM's text of that strand;
  * every supplied mark is a case the supplied-marks page has an image for, each case once;
  * supplied-mark words parse clean (the charity is what lets them parse);
  * every chanted verse is clean or an attributed error, and the dt 5:8 elyon anomaly surfaces
    as an attributed ungrammatical verse, not a crash;
  * the supplied-marks page's links into another page resolve there, and its anchors include
    every one that CLC's long notes link to.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_dual_cant_detangle.py -v
"""

from __future__ import annotations

import re

import pytest

from accgram import accent_marks as am
from accgram import dual_cant_detangle as dcd
from accgram import prose_filter
from accgram import rtms_data
from accgram import supplied_marks
from accgram.mam_simple_verse import load_mam_simple_for_refs
from accgram.prose_ply_grammar import build_parser
from clc import clc_render

from mb_cmn import paths

_ID = re.compile(r'\bid="([^"]+)"')
# A link to a fragment of another page in the same tree: no scheme, so no colon.
_PAGE_FRAGMENT_LINK = re.compile(r'href="([^":#]+\.html)#([^"]+)"')


def _mam_with_strands() -> dict[str, dict]:
    return load_mam_simple_for_refs(
        paths.require_mam_simple_dir(),
        dcd.all_refs_by_book(),
        include_strands=True,
    )


def _detangle() -> list[dcd.PassageResult]:
    kq_u_dir = rtms_data.default_wlc422_kq_u_dir(paths.repo_root())
    wlc_index = rtms_data.load_wlc422_index(kq_u_dir)
    return dcd.detangle_all(wlc_index, _mam_with_strands(), build_parser())


def _all_chanted_verses(
    results: list[dcd.PassageResult],
) -> list[dcd.ChantedVerseResult]:
    return [cv for pr in results for tr in pr.strands for cv in tr.chanted_verses]


def test_gen3522_strands_are_pashut_and_midrashit_and_parse() -> None:
    results = _detangle()
    gen = next(pr for pr in results if pr.passage.bb == "gn")
    alef, bet = gen.strands
    assert alef.strand_label == "pashut" and bet.strand_label == "midrashit"
    assert all(cv.status == "clean" for cv in alef.chanted_verses + bet.chanted_verses)


def test_each_strand_has_one_chanted_verse_per_sof_pasuq() -> None:
    """In all three passages, as many chanted verses as MAM's text of the strand has sof pasuqs."""
    mam = _mam_with_strands()
    for pr in _detangle():
        for tr in pr.strands:
            where = (pr.passage.name, tr.strand_label)
            sof_pasuqs = sum(
                word.count(am.SOF_PASUQ)
                for chnu, vrnu in pr.passage.refs
                for word in mam[f"{pr.passage.bb}{chnu}:{vrnu}"]["mam_simple_verse"][
                    f"vels_cant_{tr.strand}"
                ]
            )
            assert sof_pasuqs, where
            assert len(tr.chanted_verses) == sof_pasuqs, where


def test_supplied_marks_are_the_cases_the_page_has_an_image_for() -> None:
    results = _detangle()
    supplies = [s for pr in results for s in pr.supplied_marks]
    keyed = {(s.bcv, s.strand, s.accent) for s in supplies}  # one row per supply
    assert keyed == set(supplied_marks._CASE_IMAGE)
    assert len(keyed) == len(supplies)
    # The dt 5:8 qadma is the one supply with manuscript (LC) support; the rest are MAM-only.
    dt58 = next(s for s in supplies if (s.bcv, s.accent) == ("dt5:8", am.QADMA))
    assert dt58.source == "lc"
    assert all(s.source == "mam" for s in supplies if s is not dt58)


def test_supplied_mark_words_parse_clean() -> None:
    # The supply is precisely what lets the chanted verse parse: a supplied-mark word's
    # chanted verse must be clean and NOT an ungrammatical verse (the issue's reporting requirement).
    results = _detangle()
    supply_bcvs = {(s.bcv, s.strand) for pr in results for s in pr.supplied_marks}
    for pr in results:
        for tr in pr.strands:
            for cv in tr.chanted_verses:
                for bcv in {b for b in cv.bcv_span}:
                    if (bcv, tr.strand) in supply_bcvs:
                        assert cv.status == "clean", f"{cv.ref} -> {cv.status}"


def test_dt58_anomaly_surfaces_as_attributed_error_not_crash() -> None:
    results = _detangle()
    dt = next(pr for pr in results if pr.passage.bb == "dt")
    elyon = next(
        tr for tr in dt.strands if tr.strand == "bet"
    )  # the merkha breaks the elyon
    dt58 = [cv for cv in elyon.chanted_verses if "dt5:8" in cv.word_bcvs]
    assert dt58 and dt58[0].status == "error"
    assert dt58[0].tree is not None  # a real (ERROR-bearing) tree, not a None crash
    # The taxton's dt 5:8 chanted verse is now clean -- its omitted qadma is supplied.
    taxton = next(tr for tr in dt.strands if tr.strand == "alef")
    tax58 = [cv for cv in taxton.chanted_verses if cv.bcv_span[0] == "dt5:8"]
    assert tax58 and tax58[0].status == "clean"


def test_every_chanted_verse_parses_or_is_attributed() -> None:
    # A chanted verse is clean or an attributed error; none fails to parse outright or is
    # located but unparsed.
    cvs = _all_chanted_verses(_detangle())
    bad = [cv.ref for cv in cvs if cv.status not in ("clean", "error")]
    assert not bad, f"unexpected no_parse/location_only: {bad}"


# --------------------------------------------------------------------------- #
# Stage 3: routing (prose_filter) and fold-in / supplied-marks surfaces.
# --------------------------------------------------------------------------- #
def _range_verses() -> list[tuple[str, int, int]]:
    out: list[tuple[str, int, int]] = []
    for bb, chnu, start, end in prose_filter._BHS_RANGE_EXCLUSIONS:
        out.extend((bb, chnu, vr) for vr in range(start, end + 1))
    return out


def test_prose_filter_single_cant_exceptions_match_mam_and_routing() -> None:
    # The hardcoded "un-exclude these 9" set must equal exactly the in-range verses MAM
    # marks single-cantillation (no cant-all-three) -- so it can't silently drift.
    mam = _mam_with_strands()
    derived_single_cant = set()
    for bb, chnu, vrnu in _range_verses():
        verse = mam[f"{bb}{chnu}:{vrnu}"]["mam_simple_verse"]
        if verse["vels_cant_alef"] == verse["vels_cant_bet"]:
            derived_single_cant.add((bb, chnu, vrnu))
    assert derived_single_cant == set(prose_filter._BHS_SINGLE_CANT_IN_RANGE)

    # Routing: the 9 single-cant verses go to the normal prose path; the 24 dual
    # verses (gn 35:22 + the rest of the ranges) stay excluded.
    for bb, chnu, vrnu in prose_filter._BHS_SINGLE_CANT_IN_RANGE:
        assert prose_filter.should_keep_line(bb, chnu, vrnu) is True
    dual_in_range = [v for v in _range_verses() if v not in derived_single_cant]
    for bb, chnu, vrnu in dual_in_range:
        assert prose_filter.should_keep_line(bb, chnu, vrnu) is False
    assert prose_filter.should_keep_line("gn", 35, 22) is False


def test_supplied_marks_page_links_resolve_in_their_target_pages() -> None:
    """Every ``href="<page>.html#<fragment>"`` on the supplied-marks page names an id of <page>.

    Both pages are the tracked ones.  The links lead into the ungrammatical-verse page, whose
    ids come from the chanted verses ``run-prose`` folds in, so a link whose record moved or
    vanished fails here.
    """
    page = supplied_marks.default_html_out_path(paths.repo_root())
    links = _PAGE_FRAGMENT_LINK.findall(page.read_text(encoding="utf-8"))
    assert links, f"{page}: no link into another page"
    for target, fragment in links:
        ids = set(_ID.findall((page.parent / target).read_text(encoding="utf-8")))
        assert fragment in ids, (target, fragment)


def test_supplied_marks_page_renders_every_case_and_the_punctuation_inventory() -> None:
    results = _detangle()
    supplies = [s for pr in results for s in pr.supplied_marks]
    punctuation_changes = [d for pr in results for d in pr.punctuation_changes]
    body = supplied_marks.render_body_contents(supplies, punctuation_changes)
    from py_html import wlc_utils_html as H

    html = H.el_to_str_no_wbr(body[0])
    # Each supplied accent is its own case, with a heading and an image.
    assert html.count("goerwitz-tms-reading-label") == len(supplies)
    assert html.count("<img") == len(supplies)
    # Each case's heading carries a stable anchor id (supplied_marks._anchor_id).  CLC's
    # long notes deep-link to some of them through clc_render._SUPPLIED_MARKS_ANCHOR, so
    # every anchor that table names must be on the page.
    assert set(clc_render._SUPPLIED_MARKS_ANCHOR.values()) <= set(_ID.findall(html))
    # The lone punctuation-change table: a header row + one row per supply/suppress change.
    assert html.count("<tr") == 1 + len(punctuation_changes)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-v"]))
