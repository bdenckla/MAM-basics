"""Pin CTR's two Decalogues against the reference strands (issue wlc-utils#73).

CTR (The Complete Tanach with Rashi, chabad.org) is a VENDORED STRAND, not a hand
transcription: digital, accent-exact Hebrew, compared at the GLYPH level because its encoding
cannot distinguish the lookalike accent pairs a reader resolves by grammar (see
``accgram/ctr_decalogue.py``).  These tests pin the surprise the comparison found and guard it
against a re-fetch or a re-vendoring that would quietly change it:

* CTR's Exodus 20 has the ta'am ELYON accents (not the taxton expected of a running text) under
  a punctuation that is neither strand's: sixteen sof pasuqs, the union of the two strands'
  boundaries.  Only nine of the sixteen spans have a silluq, so only nine are chanted verses --
  say SOF PASUQ SPAN for the rest, which is what makes the finding statable at all (a real
  re-division would have moved the silluqs, and silluq is an accent).
* CTR's Deuteronomy 5 is the taxton, division and all: thirteen spans, all with a silluq.

Every residual difference from the followed strand is CONJUNCTIVE -- the disjunctive skeleton,
which is what wlc-utils#69 claims survives, is intact in both books.

Both vendored JSONs are committed here under ``in/accgram``, so these FAIL rather than skip if
one is absent: the fetch scripts are how the file is regenerated, not a dependency a runner may
be missing, and a tracked file having been deleted is the last moment to go quiet.  ``load_ctr``
and ``load_source`` already raise naming the file, which is the whole of what a guard could say.
See ``wlc_paths.require_sibling`` for the argument.

ONE BLESSED EXAMPLE-BASED TEST (issue wlc-utils#88): ``clean_verse`` against a hand-built HTML string,
the shape ``doc/agent-planning-principles.md`` otherwise forbids.  Kept, because the vendored
JSON is already cleaned, so every differential check above runs downstream of the stripper and
none of them would notice it regressing on markup that a re-fetch reintroduced -- the raw HTML
is exactly the input no committed artifact holds.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_ctr_decalogue.py -v
"""

from __future__ import annotations

import pytest

from accgram import ctr_decalogue as cd
from accgram import ctr_decalogue_fetch as cdf
from accgram import printed_decalogue as pd
from accgram import printed_decalogue_strands as pds

# (glyph-agreeing words, total words) established against the followed strand, and the exact
# set of residual chanted-word skeletons -- every one conjunctive-only.  Pinned so a re-fetch
# that moved an accent, or a fold that stopped hiding a lookalike pair, fails here.
_EXPECTED = {
    "ex": {
        "primary": "elyon",
        "agree": 139,
        "total": 142,
        # CTR has a munax on the non-final atom of two maqaf compounds (יהיה־לך, ובנך־ובתך)
        # and swaps a munax for the reference's merkha on one ואשר.  All conjunctive.
        "residuals": {"יהיהלך", "ואשר", "ובנךובתך"},
        "ctr_spans": 16,
        "ctr_chanted_verses": 9,
        # The seven spans that close on no silluq, each with the elyon's own mid-verse
        # disjunctive still standing where a silluq would have to be.
        "silluqless": {
            "עבדים": ("rev",),
            "עלפני": ("rev",),
            "לארץ": ("rev",),
            "לשנאי": ("etn",),
            "לקדשו": ("rev",),
            "כלמלאכתך": ("seg",),
            "בשעריך": ("zaq",),
        },
    },
    "dt": {
        "primary": "taxton",
        "agree": 163,
        "total": 164,
        # A single munax/merkha swap on ולא.
        "residuals": {"ולא"},
        "ctr_spans": 13,
        "ctr_chanted_verses": 13,
        "silluqless": {},
    },
}


def _ctr() -> dict:
    return cd.load_ctr()


def _source() -> dict:
    return pd.load_source()


def test_vendored_ctr_has_both_decalogue_spans() -> None:
    """The snapshot holds Exodus 20:2-14 and Deuteronomy 5:6-18, 13 verses each."""
    ctr = _ctr()
    assert set(ctr["chapters"]) == {"ex", "dt"}
    assert list(ctr["chapters"]["ex"]["decalogue_verses"]) == [
        f"20:{v}" for v in range(2, 15)
    ]
    assert list(ctr["chapters"]["dt"]["decalogue_verses"]) == [
        f"5:{v}" for v in range(6, 19)
    ]


@pytest.mark.parametrize("book", ["ex", "dt"])
def test_ctr_follows_its_strand_at_the_glyph_level(book: str) -> None:
    """CTR agrees with its followed strand at exactly the pinned word count."""
    ctr, source = _ctr(), _source()
    exp = _EXPECTED[book]
    cmp = cd.compare(ctr, source, book, exp["primary"])
    assert cmp.agree == exp["agree"]
    assert cmp.agree + len(cmp.diffs) == exp["total"]


@pytest.mark.parametrize("book", ["ex", "dt"])
def test_residual_differences_are_exactly_these_and_all_conjunctive(book: str) -> None:
    """The residuals are the pinned words, and every one leaves the disjunctive skeleton intact."""
    ctr, source = _ctr(), _source()
    exp = _EXPECTED[book]
    cmp = cd.compare(ctr, source, book, exp["primary"])
    assert {d.skeleton for d in cmp.diffs} == exp["residuals"]
    assert cmp.disjunctive_skeleton_intact
    for d in cmp.diffs:
        assert (
            d.conjunctive_only
        ), f"{d.skeleton}: {d.ctr} vs {d.strand} touches a disjunctive"


@pytest.mark.parametrize("book", ["ex", "dt"])
def test_the_cross_strand_agreement_collapses(book: str) -> None:
    """Against the OTHER tradition, agreement collapses -- the evidence the match is real.

    A clean match against the followed strand could in principle be an artifact of the glyph
    fold; that the SAME comparison against the other tradition falls apart is what rules that
    out.  Pinned loosely (a wide margin) rather than to an exact count, since the cross diff is
    not the finding and its exact difflib alignment is not worth freezing.
    """
    ctr, source = _ctr(), _source()
    exp = _EXPECTED[book]
    primary = cd.compare(ctr, source, book, exp["primary"])
    cross = cd.compare(ctr, source, book, cd.CROSS[book])
    assert cross.agree < primary.agree - 40


@pytest.mark.parametrize("book", ["ex", "dt"])
def test_ctr_sof_pasuq_span_structure(book: str) -> None:
    """Deuteronomy shares the taxton's 13-verse division; Exodus has its own 16 sof pasuqs, the
    elyon accents notwithstanding -- it does not group the commandments the elyon way.
    """
    ctr, source = _ctr(), _source()
    exp = _EXPECTED[book]
    n_spans = len(cd.sof_pasuq_spans(ctr, book))
    assert n_spans == exp["ctr_spans"]
    strand_cv = cd.strand_chanted_verse_count(source, book, exp["primary"])
    if book == "dt":
        assert n_spans == strand_cv  # taxton division IS the numbered verses
    else:
        assert n_spans != strand_cv  # elyon groups into 9; CTR does not


@pytest.mark.parametrize("book", ["ex", "dt"])
def test_only_spans_with_a_silluq_are_chanted_verses(book: str) -> None:
    """The silluq check the glyph comparison cannot do -- and the page's claim rests on it.

    ``word_glyphs`` drops U+05BD, so 139/142 is silluq-BLIND: it would report the same score if
    CTR had re-silluqed its sixteen boundaries, which is exactly the reading that would make
    "the accents are the elyon's" false.  Pin what is actually there instead: nine of Exodus's
    sixteen spans have a silluq, and the other seven still have the elyon's mid-verse
    disjunctive where a silluq would have to be.  Deuteronomy's thirteen all have one.
    """
    ctr = _ctr()
    exp = _EXPECTED[book]
    spans = cd.span_silluq_status(ctr, book)
    assert len(spans) == exp["ctr_spans"]
    assert sum(s.is_chanted_verse for s in spans) == exp["ctr_chanted_verses"]
    assert {s.skeleton: s.final_glyphs for s in spans if not s.is_chanted_verse} == exp[
        "silluqless"
    ]


def test_the_sixteen_exodus_marks_are_the_union_of_both_strands_boundaries() -> None:
    """CTR's Exodus punctuation is not a third division: it is elyon's 9 ∪ taxton's 13.

    The two strands share six boundaries, so the union is 16 -- the count CTR has.  This is
    what "belongs to neither strand" means here, and it is a stronger claim than the count
    alone: every one of CTR's marks is some strand's, and no strand's mark is missing.
    """
    ctr, source = _ctr(), _source()
    ctr_ends = {s.skeleton for s in cd.span_silluq_status(ctr, "ex")}
    strand_ends = {}
    for reading in ("elyon", "taxton"):
        version = next(
            v
            for v in source["versions"]
            if v["book"] == "ex"
            and v["reading"] == reading
            and v["tradition"] == "printed"
        )
        strand_ends[reading] = {
            pds.base_skeleton(cv.split()[-1]) for cv in version["chanted_verses"]
        }
    assert len(strand_ends["elyon"]) == 9
    assert len(strand_ends["taxton"]) == 13
    assert ctr_ends == strand_ends["elyon"] | strand_ends["taxton"]
    # The nine chanted verses are exactly the elyon's, and the seven silluq-less spans are
    # exactly the boundaries only the taxton has.
    chanted = {
        s.skeleton for s in cd.span_silluq_status(ctr, "ex") if s.is_chanted_verse
    }
    assert chanted == strand_ends["elyon"]
    assert ctr_ends - chanted == strand_ends["taxton"] - strand_ends["elyon"]


def test_clean_verse_drops_rendering_cruft_but_keeps_the_qere() -> None:
    """clean_verse strips the ketiv note and section markers, keeps the accented qere text."""
    raw = (
        'foo <co:instructional ksiv="מצותו">'
        "מִצְוֺתָֽי</co:instructional>"
        '<span class="instructional ksiv"> (כתיב מצותו) </span>'
        ": ס bar:"
    )
    cleaned = cdf.clean_verse(raw)
    assert "<" not in cleaned and ">" not in cleaned
    assert "ס" not in cleaned.split()  # bare samekh section marker dropped
    assert "(" not in cleaned  # the ketiv parenthetical note is gone
    assert "מִצְוֺתָֽי" in cleaned  # the accented qere survives
