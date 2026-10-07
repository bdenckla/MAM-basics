"""Issue wlc-utils#68: the m-trad Decalogue strands agree between the repo's two copies of them.

The printed-Decalogue page trio (``printed_decalogue_page`` and its Koren and Simanim
satellites, via ``printed_decalogue_strands``) takes MAM's manuscript tradition as its
authoritative baseline and states facts about it as ground truth.  Those pages read the
mirrored ``in/mam-ws-special/decalogue-base.mediawiki``; MAM's own parse of the same text
lives one repo over in MAM-parsed's ``plus`` tree.  Nothing tied the two together, so a
refresh of the mirror or an upstream Wikisource edit could have moved a word or a stroke and left
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

import re
import unicodedata

import pytest

from accgram import decalogue_m_trad as dmt
from accgram import printed_decalogue as pd

# NOTHING HERE SKIPS ON A MISSING SOURCE, deliberately.  Both sides of the comparison are
# supposed to be on disk -- the mirrored one is committed in this repo, and the MAM-parsed
# clone is a hard dependency of the check, not an optional enrichment -- so an absent one is
# a misconfiguration.  Skipping would report green having compared nothing, in the very
# channel this suite reserves for SEMANTIC skips (see test_edition_transcriptions' "diverges
# from its Wikisource strand; the control needs an agreeing page").  ``paths.require_sibling``
# turns the sibling's absence into a failure that names the two overrides that fix it.

STRAND_KEYS = tuple((b, r) for b in dmt.BOOKS for r in dmt.READINGS)

# The two templates whose calls the readers resolve to one of their forms, as the mirrored
# page's faithful text writes them: a ketiv/qere and a qamats variant.
_KETIV_QERE_OPEN = '{{כו"ק|'
_KETIV_QERE = re.compile(r'\{\{כו"ק\|([^|{}]*)\|([^|{}]*)\}\}')
_QAMATS_VARIANT_OPEN = "{{מ:קמץ|"
_QAMATS_VARIANT = re.compile(r"\{\{מ:קמץ\|ד=([^|{}]*)\|ס=([^|{}]*)\}\}")


def _letters(word: str) -> str:
    return "".join(c for c in word if "א" <= c <= "ת")


@pytest.fixture(scope="module")
def source() -> dict:
    """The mirrored side of the comparison -- committed in this repo, so simply read it."""
    return pd.load_source(pd.default_source_path())


@pytest.fixture(scope="module")
def strands(source) -> dict[tuple[str, str], tuple[dmt.Strand, dmt.Strand]]:
    return {
        key: (dmt.from_mam_plus(*key), dmt.from_mirrored(source, *key))
        for key in STRAND_KEYS
    }


@pytest.mark.parametrize("key", STRAND_KEYS)
def test_no_differences(strands, key) -> None:
    plus, mirrored = strands[key]
    diffs = dmt.compare(plus, mirrored)
    assert not diffs, "\n".join(d.describe() for d in diffs)


def test_no_differences_anywhere(source) -> None:
    # The same claim made once over all four strands, so a strand vanishing from either
    # source cannot make the per-strand tests pass by not running.
    diffs = dmt.compare_all(source)
    assert not diffs, "\n".join(d.describe() for d in diffs)


@pytest.mark.parametrize("key", STRAND_KEYS)
def test_words_differ_only_by_mark_order(strands, key) -> None:
    """Every raw word difference moves marks about; none adds, drops or changes one."""
    plus, mirrored = strands[key]
    for index, plus_word, mirrored_word in dmt.mark_order_differences(plus, mirrored):
        where = f"{plus.label} word {index}"
        # Same marks, just placed differently within their letter's own run.  Checked
        # both ways round: as a multiset (nothing gained or lost) and canonically (the
        # reordering is the canonical one, not some third order).
        assert sorted(plus_word) == sorted(mirrored_word), where
        assert unicodedata.normalize("NFC", plus_word) == unicodedata.normalize(
            "NFC", mirrored_word
        ), where


@pytest.mark.parametrize("key", STRAND_KEYS)
def test_mirrored_side_is_canonically_ordered(strands, key) -> None:
    # The asymmetry is one-sided: it is the mirrored side that is already canonical, so
    # the canonical reading changes only how MAM-parsed-plus is read.
    _, mirrored = strands[key]
    for word in mirrored.words:
        assert word == unicodedata.normalize("NFC", word), f"{mirrored.label}: {word}"


def _calls(source, key) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """``(K, Q)`` for each ``{{כו"ק|K|Q}}`` and ``(X, Y)`` for each ``{{מ:קמץ|ד=X|ס=Y}}``.

    Read from the strand's faithful text on the mirrored page.  Every call of either template
    must match its pattern, so a call of another shape fails here rather than going unchecked.
    """
    version = next(
        v
        for v in source["versions"]
        if (v["book"], v["reading"], v["tradition"]) == (*key, dmt.TRADITION)
    )
    text = "\n".join(version["faithful_chanted_verses"])
    ketiv_qere = _KETIV_QERE.findall(text)
    qamats_variants = _QAMATS_VARIANT.findall(text)
    assert len(ketiv_qere) == text.count(_KETIV_QERE_OPEN), key
    assert len(qamats_variants) == text.count(_QAMATS_VARIANT_OPEN), key
    return ketiv_qere, qamats_variants


@pytest.mark.parametrize("key", STRAND_KEYS)
def test_both_readers_take_the_qere_and_the_dalet_form(source, strands, key) -> None:
    """Every ``{{כו"ק|K|Q}}`` reads as Q, and every ``{{מ:קמץ|ד=X|ס=Y}}`` as X, in both readers.

    The first two normalizations ``decalogue_m_trad``'s docstring lists, checked call by call
    against the forms the mirrored page writes out, in the canonical order ``compare`` reads:
    Q and X are in the strand, Y is not, and no chanted word has K's letters.
    """
    ketiv_qere, qamats_variants = _calls(source, key)
    assert ketiv_qere or qamats_variants, f"{key}: neither template is called"
    for strand in strands[key]:
        where = f"{strand.source} {strand.label}"
        words = [w for verse in strand.canonical_verses for w in verse]
        skeletons = {_letters(w) for w in words}
        for ketiv, qere in ketiv_qere:
            assert any(qere in w for w in words), (where, qere)
            assert _letters(ketiv) not in skeletons, (where, ketiv)
        for dalet, samekh in qamats_variants:
            assert any(dalet in w for w in words), (where, dalet)
            assert not any(samekh in w for w in words), (where, samekh)
