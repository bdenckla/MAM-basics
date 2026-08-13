"""Stage-2 of issue wlc-utils#36: the dual-cantillation detangler.

Drives all three loci (Gen 35:22 + the two Decalogues) through the detangler and the
*existing* prose grammar.  The corpus-backed assertions FAIL, rather than skipping, when the
WLC 4.22 kq-u corpus or MAM-simple is missing: the corpus is committed in this repo's ``out/``,
so its absence means a tracked file was deleted, and MAM-simple's absence is a
misconfiguration ``paths.require_mam_simple_dir`` answers with both env overrides.  See
``paths.require_sibling`` for the argument.

The fixed expectations were originally derived from a one-off corpus survey run in gitignored
scratch, which no longer exists; this test is now their record, and the assertions below are
what re-derives them.  They are:

  * exactly 5 supplied marks (clean charities; dt 5:8's taxton qadma has non-definitive
    LC support) and 1 anomaly -- WLC's dt 5:8 merkha, a stray in the elyon (a real accent
    where only a meteg is due) while the taxton's omitted qadma is supplied;
  * Gen 35:22 detangles into pashut = 2 chanted verses, midrashit = 1, all parsing;
  * supplied-mark words parse clean (the charity is what lets them parse);
  * the dt 5:8 elyon anomaly surfaces as an attributed ungrammatical verse, not a crash.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_dual_cant_detangle.py -v
"""

from __future__ import annotations

import pytest

from accgram import accent_marks as am
from accgram import dual_cant_detangle as dcd
from accgram import prose_filter
from accgram import rtms_data
from accgram import supplied_marks
from accgram.mam_simple_verse import load_mam_simple_for_refs
from accgram.prose_ply_grammar import build_parser

from mb_cmn import paths


def _detangle() -> list[dcd.PassageResult]:
    kq_u_dir = rtms_data.default_wlc422_kq_u_dir(paths.repo_root())
    wlc_index = rtms_data.load_wlc422_index(kq_u_dir)
    mam = load_mam_simple_for_refs(
        paths.require_mam_simple_dir(),
        dcd.all_refs_by_book(),
        include_strands=True,
    )
    return dcd.detangle_all(wlc_index, mam, build_parser())


def _all_chanted_verses(
    results: list[dcd.PassageResult],
) -> list[dcd.ChantedVerseResult]:
    return [cv for pr in results for tr in pr.strands for cv in tr.chanted_verses]


def test_gen3522_splits_into_two_and_one_chanted_verse_all_parsing() -> None:
    results = _detangle()
    gen = next(pr for pr in results if pr.passage.bb == "gn")
    alef, bet = gen.strands
    assert alef.strand_label == "pashut" and bet.strand_label == "midrashit"
    assert len(alef.chanted_verses) == 2
    assert len(bet.chanted_verses) == 1
    assert all(cv.status == "clean" for cv in alef.chanted_verses + bet.chanted_verses)


def test_supplied_marks_are_exactly_the_five_clean_supplies() -> None:
    results = _detangle()
    supplies = [s for pr in results for s in pr.supplied_marks]
    keyed = {(s.bcv, s.strand, s.accent) for s in supplies}  # one row per supply
    assert len(supplies) == 5
    assert keyed == {
        ("ex20:3", "alef", am.MERKHA),
        (
            "dt5:8",
            "alef",
            am.QADMA,
        ),  # the taxton's omitted qadma, supplied (LC-supported)
        ("dt5:17", "alef", am.TIPEXA),
        ("dt5:6", "bet", am.TIPEXA),
        ("dt5:6", "bet", am.ATNAX),
    }
    # The dt 5:8 qadma is the one supply with manuscript (LC) support; the rest are MAM-only.
    dt58 = next(s for s in supplies if (s.bcv, s.accent) == ("dt5:8", am.QADMA))
    assert dt58.source == "lc"
    assert all(s.source == "mam" for s in supplies if s is not dt58)


def test_dt58_merkha_is_a_stray_anomaly_in_the_elyon() -> None:
    # WLC's single tangled merkha belongs to the elyon's meteg slot, where a real accent
    # is not due: it is emitted as a stray and flagged (a no-accent-due anomaly).  The
    # taxton's omitted qadma is supplied instead (no taxton anomaly).  This is the only
    # anomaly across the three loci.
    results = _detangle()
    anomalies = [a for pr in results for a in pr.anomalies]
    assert len(anomalies) == 1
    anomaly = anomalies[0]
    assert (anomaly.bcv, anomaly.strand) == ("dt5:8", "bet")  # the elyon
    assert anomaly.expected == ""  # the elyon is due no accent (only a meteg)
    assert anomaly.found == am.MERKHA  # yet WLC has a merkha here


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


def test_every_chanted_verse_parses_or_is_attributed_only_dt58_is_an_oddity() -> None:
    # The lone dt 5:8 merkha spoils only the elyon's 5:7-10 chanted verse (which contains
    # 5:8); the taxton's 5:8 is rescued by supplying its qadma.  Nothing else is non-clean.
    results = _detangle()
    cvs = _all_chanted_verses(results)
    bad = [cv.ref for cv in cvs if cv.status not in ("clean", "error")]
    assert not bad, f"unexpected no_parse/location_only: {bad}"
    ungrammatical_spans = {
        (cv.strand, cv.bcv_span) for cv in cvs if cv.status == "error"
    }
    assert ungrammatical_spans == {("bet", ("dt5:7", "dt5:10"))}


# --------------------------------------------------------------------------- #
# Stage 3: routing (prose_filter) and fold-in / supplied-marks surfaces.
# --------------------------------------------------------------------------- #
def _mam_with_strands() -> dict[str, dict]:
    return load_mam_simple_for_refs(
        paths.require_mam_simple_dir(),
        dcd.all_refs_by_book(),
        include_strands=True,
    )


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


def test_fold_in_yields_one_dt58_ungrammatical_record() -> None:
    kq_u_dir = rtms_data.default_wlc422_kq_u_dir(paths.repo_root())
    wlc_index = rtms_data.load_wlc422_index(kq_u_dir)
    mam = _mam_with_strands()
    parser = build_parser()

    # Genesis 35:22 and the Exodus Decalogue fold in nothing (no oddities).
    assert dcd.folded_ungrammatical_records("gn", wlc_index, mam, parser) == []
    assert dcd.folded_ungrammatical_records("ex", wlc_index, mam, parser) == []
    # Deuteronomy folds in exactly the dt 5:8 elyon oddity, keyed at the verse where the
    # rogue merkha lives (dt 5:8), though the elyon reading itself spans dt 5:7-10.
    dt = dcd.folded_ungrammatical_records("dt", wlc_index, mam, parser)
    assert len(dt) == 1
    assert dt[0]["bcv"] == "dt5:8"
    assert (
        dt[0]["dual_cant_strand"] == "bet"
    )  # the elyon is the ungrammatical reading now
    assert dt[0]["status"] == "error"
    assert dt[0]["dual_cant"] is True
    assert dt[0]["ref"].endswith("5:8")  # so the ungrammatical collector reads (5, 8)


def test_supplied_marks_page_renders_all_five_cases_and_punctuation_inventory() -> None:
    results = _detangle()
    supplies = [s for pr in results for s in pr.supplied_marks]
    punctuation_changes = [d for pr in results for d in pr.punctuation_changes]
    body = supplied_marks.render_body_contents(supplies, punctuation_changes)
    from py_html import wlc_utils_html as H

    html = H.el_to_str_no_wbr(body[0])
    # Each of the five supplied accents is its own case, with a heading and an image.
    assert html.count("goerwitz-tms-reading-label") == len(supplies) == 5
    assert html.count("<img") == 5
    # Each case's heading carries a stable anchor id (supplied_marks._anchor_id) that
    # UXLC-utils's CLC long-notes deep-links to -- keep these in sync with that repo's
    # clc_render._SUPPLIED_MARKS_ANCHOR if the id scheme ever changes.
    for anchor in (
        'id="supplied-ex20v3-alef-merkha"',
        'id="supplied-dt5v6-bet-tipexa"',
        'id="supplied-dt5v6-bet-atnax"',
        'id="supplied-dt5v8-alef-qadma"',
        'id="supplied-dt5v17-alef-tipexa"',
    ):
        assert anchor in html, anchor
    # The lone punctuation-change table: a header row + one row per supply/suppress change.
    assert html.count("<tr") == 1 + len(punctuation_changes)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-v"]))
