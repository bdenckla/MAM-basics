"""Issue wlc-utils#68: the m-trad Decalogue strands agree between the repo's two copies of them.

The printed-Decalogue page trio (``printed_decalogue_page`` and its Koren and Simanim
satellites, via ``printed_decalogue_strands``) takes MAM's manuscript tradition as its
authoritative baseline and states facts about it as ground truth.  Those pages read the
vendored ``in/accgram/printed_decalogue_teamim.json``; MAM's own parse of the same text
lives one repo over in MAM-parsed's ``plus`` tree.  Nothing tied the two together, so a
re-vendoring or an upstream Wikisource edit could have moved a word or a stroke and left
the pages asserting something MAM does not say.

The answer is that they agree exactly -- all four (book, reading) strands, every chanted
verse, every word, every vertical stroke, with no exceptions to enumerate.  The single
respect in which the two sources are not byte-identical is the ORDER of a letter's own
marks (see ``decalogue_m_trad``'s docstring): MAM-parsed-plus keeps MAM's order, the
Wikisource base page is canonically ordered.  ``test_words_differ_only_by_mark_order``
pins that down independently of the canonical reading ``compare`` does, so the day the two
sources really do diverge, that is not where it hides.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_decalogue_m_trad.py -v
"""

from __future__ import annotations

import unicodedata

import pytest

from accgram import decalogue_m_trad as dmt
from accgram import printed_decalogue as pd

# NOTHING HERE SKIPS ON A MISSING SOURCE, deliberately.  Both sides of the comparison are
# supposed to be on disk -- the vendored one is committed in this repo, and the MAM-parsed
# clone is a hard dependency of the check, not an optional enrichment -- so an absent one is
# a misconfiguration.  Skipping would report green having compared nothing, in the very
# channel this suite reserves for SEMANTIC skips (see test_edition_transcriptions' "diverges
# from its Wikisource strand; the control needs an agreeing page").  ``wlc_paths.require_sibling``
# turns the sibling's absence into a failure that names the two overrides that fix it.

# Per strand: chanted verses, chanted words, and the kind of every vertical stroke in
# reading order.  Derived from MAM-parsed-plus and equally true of the vendored side --
# pinned here so a change that moved both in step still has to be looked at.  The verse
# counts are the same ones printed_decalogue_strands.STRUCTURE pins for Exodus.
EXPECTED: dict[tuple[str, str], tuple[int, int, tuple[str, ...]]] = {
    ("ex", "taxton"): (12, 142, ("legarmeh",)),
    ("ex", "elyon"): (10, 142, ("paseq", "paseq", "legarmeh", "legarmeh")),
    ("dt", "taxton"): (12, 165, ("legarmeh",)),
    ("dt", "elyon"): (
        10,
        164,
        ("paseq", "paseq") + ("legarmeh",) * 5,
    ),
}

STRAND_KEYS = tuple(EXPECTED)

QAMATS = "\N{HEBREW POINT QAMATS}"
QAMATS_QATAN = "\N{HEBREW POINT QAMATS QATAN}"


def _letters(word: str) -> str:
    return "".join(c for c in word if "א" <= c <= "ת")


@pytest.fixture(scope="module")
def source() -> dict:
    """The vendored side of the comparison -- committed in this repo, so simply read it."""
    return pd.load_source(pd.default_source_path())


@pytest.fixture(scope="module")
def strands(source) -> dict[tuple[str, str], tuple[dmt.Strand, dmt.Strand]]:
    return {
        key: (dmt.from_mam_plus(*key), dmt.from_vendored(source, *key))
        for key in STRAND_KEYS
    }


@pytest.mark.parametrize("key", STRAND_KEYS)
def test_no_differences(strands, key) -> None:
    plus, vendored = strands[key]
    diffs = dmt.compare(plus, vendored)
    assert not diffs, "\n".join(d.describe() for d in diffs)


def test_no_differences_anywhere(source) -> None:
    # The same claim made once over all four strands, so a strand vanishing from either
    # source cannot make the per-strand tests pass by not running.
    diffs = dmt.compare_all(source)
    assert not diffs, "\n".join(d.describe() for d in diffs)


@pytest.mark.parametrize("key", STRAND_KEYS)
def test_shapes_are_as_pinned(strands, key) -> None:
    n_verses, n_words, stroke_kinds = EXPECTED[key]
    for strand in strands[key]:
        where = f"{strand.source} {strand.label}"
        assert len(strand.verses) == n_verses, where
        assert len(strand.words) == n_words, where
        assert strand.stroke_kinds == stroke_kinds, where


@pytest.mark.parametrize("key", STRAND_KEYS)
def test_words_differ_only_by_mark_order(strands, key) -> None:
    """Every raw word difference moves marks about; none adds, drops or changes one."""
    plus, vendored = strands[key]
    for index, plus_word, vendored_word in dmt.mark_order_differences(plus, vendored):
        where = f"{plus.label} word {index}"
        # Same marks, just placed differently within their letter's own run.  Checked
        # both ways round: as a multiset (nothing gained or lost) and canonically (the
        # reordering is the canonical one, not some third order).
        assert sorted(plus_word) == sorted(vendored_word), where
        assert unicodedata.normalize("NFC", plus_word) == unicodedata.normalize(
            "NFC", vendored_word
        ), where


@pytest.mark.parametrize("key", STRAND_KEYS)
def test_vendored_side_is_canonically_ordered(strands, key) -> None:
    # The asymmetry is one-sided: it is the vendored side that is already canonical, so
    # the canonical reading changes only how MAM-parsed-plus is read.
    _, vendored = strands[key]
    for word in vendored.words:
        assert word == unicodedata.normalize("NFC", word), f"{vendored.label}: {word}"


@pytest.mark.parametrize("key", (("dt", "taxton"), ("dt", "elyon")))
def test_ketiv_qere_resolves_to_the_qere(strands, key) -> None:
    """Deut 5:9's מצותי is a ketiv/qere; both sources are read for the qere."""
    for strand in strands[key]:
        skeletons = {_letters(w) for w in strand.words}
        assert "מצותי" in skeletons, strand.source
        assert "מצותו" not in skeletons, strand.source


@pytest.mark.parametrize("key", STRAND_KEYS)
def test_qamats_variant_resolves_to_the_dalet_form(strands, key) -> None:
    """תעבדם is a ``מ:קמץ``; both sources are read for its ``ד`` spelling.

    Which is the one that writes both qamatsim as qamats qatan -- the ``ס`` spelling
    leaves the first as a plain qamats, so the absence of that tells the two apart.
    """
    for strand in strands[key]:
        taavdem = [w for w in strand.words if _letters(w) == "תעבדם"]
        assert len(taavdem) == 1, f"{strand.source} {strand.label}: {taavdem}"
        assert taavdem[0].count(QAMATS_QATAN) == 2, strand.source
        assert QAMATS not in taavdem[0], strand.source


def test_deuteronomy_shared_legarmeh_is_the_same_stroke(strands) -> None:
    """Deut 5:15's לְמַעַן is the one stroke either Decalogue shares between its strands.

    In MAM-parsed-plus it sits outside any ``מ:כפול``, which is what "shared" means there;
    both strands must therefore carry it, and it is the taxton's only stroke.
    """
    lemaan = "לְמַ֣עַן" + dmt.PASOLEG
    taxton_plus, taxton_vendored = strands[("dt", "taxton")]
    elyon_plus, elyon_vendored = strands[("dt", "elyon")]
    for strand in (taxton_plus, taxton_vendored):
        assert lemaan in strand.words, strand.source
        assert strand.stroke_kinds == ("legarmeh",), strand.source
    for strand in (elyon_plus, elyon_vendored):
        assert lemaan in strand.words, strand.source
