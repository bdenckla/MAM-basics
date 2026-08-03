"""Test for clc_versification (the §7.8 vtrad-MAM Decalogue verse map).

Run from the repo root:
    .venv/Scripts/python.exe py/main_test.py py/tests/clc_versification_test.py

Two things are checked:

  * the hand-encoded BHS↔MAM map (``clc_to_mam`` / ``mam_merge_group`` / boundaries) on
    the known Decalogue anchors and its structural invariants (monotonic, identity outside
    the two chapters); and
  * the **validation** that gives #45 its content: the boundaries MAM runs through (this
    module's merge groups) coincide **1:1** with the atoms where the §7.7 ``_ORACLE`` shows
    the elyon strand ending a verse the taḥton strand reads through — i.e. MAM's
    versification *is* the taḥton strand, so §7.7 already renders the overlay.

The full 53-verse agreement with MAM-basics' own converter was established once against a
``.novc/`` versemap dump (produced by a throwaway harvest script, since retired); that dump is
gitignored, so this test pins the map by hardcoded known facts instead of reading it.
"""

import clc.clc_versification as cv
import clc.clc_dual_cant as dc
import mb_cmn.hebrew_punctuation as hpu

_SOF_PASUQ = hpu.SOPA


def test_clc_to_mam_known_anchors():
    # The anchors recorded for #38 (MAM-with-doc merged-elyon numbering runs ~1 behind
    # vtrad-BHS): BHS Ex 20:3 -> MAM 20:2; BHS Dt 5:6 & 5:7 both -> MAM 5:6; BHS Dt 5:17
    # (תרצח) -> MAM 5:16.
    assert cv.clc_to_mam("Exodus", 20, 3) == (20, 2)
    assert cv.clc_to_mam("Deuter", 5, 6) == (5, 6)
    assert cv.clc_to_mam("Deuter", 5, 7) == (5, 6)
    assert cv.clc_to_mam("Deuter", 5, 17) == (5, 16)

    # The two early-split anchors and their post-split −1 shift.
    assert cv.clc_to_mam("Exodus", 20, 2) == (20, 2)  # first member keeps the number
    assert cv.clc_to_mam("Exodus", 20, 4) == (20, 3)  # −1 after the early split
    assert cv.clc_to_mam("Exodus", 20, 12) == (20, 11)

    # The late 4-way split collapses to one MAM verse, then −4 for the rest of the chapter.
    for v in (13, 14, 15, 16):
        assert cv.clc_to_mam("Exodus", 20, v) == (20, 12), v
    assert cv.clc_to_mam("Exodus", 20, 17) == (20, 13)  # −4 (1 early + 3 late)
    assert cv.clc_to_mam("Exodus", 20, 26) == (20, 22)  # last verse of the chapter

    for v in (17, 18, 19, 20):
        assert cv.clc_to_mam("Deuter", 5, v) == (5, 16), v
    assert cv.clc_to_mam("Deuter", 5, 21) == (5, 17)
    assert cv.clc_to_mam("Deuter", 5, 33) == (5, 29)  # last verse of Deut 5


def test_identity_outside_decalogue():
    # Before the first split, and in every non-Decalogue locus, BHS and MAM agree exactly.
    assert cv.clc_to_mam("Exodus", 20, 1) == (20, 1)
    for v in range(1, 6):
        assert cv.clc_to_mam("Deuter", 5, v) == (5, v)
    assert cv.clc_to_mam("Exodus", 21, 5) == (21, 5)
    assert cv.clc_to_mam("Genesis", 35, 22) == (
        35,
        22,
    )  # dual-cant, but same versification
    assert cv.clc_to_mam("Psalms", 23, 1) == (23, 1)
    assert not cv.mam_differs_from_bhs("Exodus", 20, 1)
    assert not cv.mam_differs_from_bhs("Genesis", 35, 22)


def test_map_is_monotone_and_onto():
    # Within each Decalogue chapter, clc_to_mam is non-decreasing in v, never skips a MAM
    # number, and is surjective onto a contiguous 1..max range — a sanity net against a
    # typo in _MERGE_GROUPS producing a gap or a non-monotone jump.
    for book_id, ch in cv.decalogue_chapters():
        prev = 0
        produced = set()
        for v in range(1, 40):  # covers both chapters (Ex 20: 26 vv, Dt 5: 33 vv)
            _, mam_v = cv.clc_to_mam(book_id, ch, v)
            assert mam_v in (prev, prev + 1), (book_id, ch, v, prev, mam_v)
            prev = max(prev, mam_v)
            produced.add(mam_v)
        assert produced == set(range(1, max(produced) + 1)), (book_id, ch)


def test_merge_group_and_boundaries():
    # A merged verse reports its whole BHS run; an unmerged one reports just itself.
    assert cv.mam_merge_group("Exodus", 20, 2) == (2, 3)
    assert cv.mam_merge_group("Exodus", 20, 3) == (2, 3)
    assert cv.mam_merge_group("Exodus", 20, 14) == (13, 14, 15, 16)
    assert cv.mam_merge_group("Deuter", 5, 20) == (17, 18, 19, 20)
    assert cv.mam_merge_group("Exodus", 20, 4) == (4,)
    assert cv.mam_merge_group("Exodus", 20, 1) == (1,)

    # MAM draws NO boundary after a non-final member of a merge run; it agrees with BHS
    # everywhere else. These False points are the §7.8 overlay.
    assert not cv.mam_boundary_after("Exodus", 20, 2)  # reads on into 20:3
    assert cv.mam_boundary_after("Exodus", 20, 3)  # then MAM does end here
    for v in (13, 14, 15):
        assert not cv.mam_boundary_after("Exodus", 20, v)
    assert cv.mam_boundary_after("Exodus", 20, 16)  # end of the merged coveting verse
    assert cv.mam_boundary_after("Exodus", 20, 1)  # agrees with BHS pre-split


def test_differs_flag():
    # mam_differs_from_bhs is True for a merged verse (boundary difference) AND for a merely
    # shifted verse (numbering difference), False otherwise.
    assert cv.mam_differs_from_bhs(
        "Exodus", 20, 2
    )  # merged (20:2+3), same number but a
    assert cv.mam_differs_from_bhs("Exodus", 20, 3)  # boundary/number difference
    assert cv.mam_differs_from_bhs("Exodus", 20, 4)  # shifted −1
    assert cv.mam_differs_from_bhs("Deuter", 5, 33)  # shifted −4


def test_overlay_matches_dual_cant_oracle():
    # THE validation of #45 (§7.8): the boundaries MAM runs through (this module's merge
    # groups) are exactly the atoms where clc_dual_cant._ORACLE shows the elyon (bet) strand
    # ending a verse (silluq/sof-pasuq) while the taxton (alef) strand reads on. That 1:1
    # match is the proof that MAM's versification == the taxton strand, so §7.7 already
    # renders the vtrad-MAM overlay and #45 needs no new rendered surface.
    reads_through = set()
    for book_id, ch in cv.decalogue_chapters():
        for v in range(1, 40):
            if not cv.mam_boundary_after(book_id, ch, v):
                reads_through.add((book_id, ch, v))

    elyon_ends = set()
    for book_id in ("Exodus", "Deuter"):
        for (ch, v), entry_map in dc._ORACLE[book_id].items():
            for entry in entry_map.values():
                add = entry.get("add", {})
                alef_has = _SOF_PASUQ in entry.get("alef", "") or _SOF_PASUQ in add.get(
                    "alef", []
                )
                bet_has = _SOF_PASUQ in entry.get("bet", "") or _SOF_PASUQ in add.get(
                    "bet", []
                )
                if (
                    bet_has and not alef_has
                ):  # elyon ends here, taxton (= MAM) reads through
                    elyon_ends.add((book_id, ch, v))

    assert reads_through == elyon_ends, (
        "overlay/oracle disagree",
        reads_through ^ elyon_ends,
    )
    assert len(reads_through) == 8  # Ex 20:2,13,14,15 + Dt 5:6,17,18,19
