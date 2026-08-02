"""Issue wlc-utils#52: the printed-Decalogue grammaticality page (printed-decalogue.html).

Covers the page-1-specific machinery the Simanim test does not: that the whole body builds
(exercising the ``printed_decalogue_strands`` drift assertions AND the four-strands table's
per-cell check that a word's sof pasuq agrees with whether its strand ends a chanted verse
there), that the two signal words identify the strands, and that ``_strip_pointing`` keeps the
cantillation signal (accents + sof pasuq) while dropping vowels, MAM-simple style.

The vendored source JSON is committed here, so these FAIL rather than skip if it is absent --
see ``test_printed_decalogue``'s docstring and ``wlc_paths.require_sibling``.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_printed_decalogue_page.py -v
"""

from __future__ import annotations


from accgram import printed_decalogue as pd
from accgram import printed_decalogue_page as page
from accgram import printed_decalogue_strands as pds
from accgram import transcription_parse as tp

# Marks referenced below, spelled with \N{} escapes rather than bare (orphan) combining marks
# in a literal (CLAUDE.md). U+05BD is the meteg/silluq glyph -- kept by _strip_pointing only
# when the word is verse-final (there it is silluq, an accent); U+05C3 is sof pasuq.
_SILLUQ = (
    "\N{HEBREW POINT METEG}"  # U+05BD, functioning as silluq on the verse-final word
)
_SOF_PASUQ = "\N{HEBREW PUNCTUATION SOF PASUQ}"  # U+05C3
_QAMATS = "\N{HEBREW POINT QAMATS}"  # U+05B8, a vowel -- must be dropped
_HATAF_PATAH = "\N{HEBREW POINT HATAF PATAH}"  # U+05B2, a vowel -- must be dropped


def _source() -> dict:
    return pd.load_source()


def test_body_renders() -> None:
    """The full page body builds and is non-empty. Building it runs pds.resolve_readings (whose
    per-strand drift assertions, Ex/Dt signal-pair agreement check, and pairwise-distinctness
    check all fire here) and _four_strands_table (whose per-cell assert pins each word's sof pasuq
    against whether its strand ends a chanted verse there), so a data drift fails this test loudly.

    It also runs the transcription paragraph's own guard (issue wlc-utils#52): the editions said to print
    the p-trad elyon's ungrammatical opening verse must really be the ones following it.
    """
    source = _source()
    results = pd.check_all(source)
    body = page.render_body_contents(results, source, tp.check_all(results))
    assert isinstance(body, tuple) and len(body) > 0


def test_strip_pointing_keeps_accent_and_sof_pasuq_drops_vowels() -> None:
    """On a verse-final עבדים (silluq + sof pasuq): letters and the two signal marks survive,
    the vowels do not."""
    results = pd.check_all(_source())
    readings = {r.name: r for r in pds.resolve_readings(results)}
    # m-trad elyon gives אנכי…עבדים its own verse, so its עבדים is verse-final (silluq + sof pasuq).
    avadim = readings["m-trad elyon"].avadim_word
    stripped = page._strip_pointing(avadim)
    assert pds.base_skeleton(stripped) == pds.AVADIM  # all letters kept
    assert _SOF_PASUQ in stripped  # accent-coupled punctuation kept
    assert _SILLUQ in stripped  # the verse-final U+05BD is silluq (an accent), kept
    assert _QAMATS not in stripped and _HATAF_PATAH not in stripped  # vowels dropped


def test_me_pt_identical_through_avadim() -> None:
    """m-trad elyon and p-trad taḥton read אנכי…עבדים identically once stripped (their full forms
    differ only by an immaterial meteg) -- the "but only through עבדים" identity the page's third
    bullet claims. The two part at the span's OTHER signal word, על־פני, which is why each now has
    its own table row; that parting is pinned by test_signal_pairs_identify_strands below.
    """
    results = pd.check_all(_source())
    readings = {r.name: r for r in pds.resolve_readings(results)}
    me, pt = readings["m-trad elyon"], readings["p-trad taḥton"]
    assert page._strip_pointing(me.first_verse_words[0]) == page._strip_pointing(
        pt.first_verse_words[0]
    )
    assert page._strip_pointing(me.first_verse_words[-1]) == page._strip_pointing(
        pt.first_verse_words[-1]
    )


def test_signal_pairs_identify_strands() -> None:
    """The page's headline claim: the (עבדים, על־פני) accent pair is different in each of the four
    strands, so the pair alone places a text among them. ``pds.resolve_readings`` checks the
    pairwise distinctness itself; this pins the actual four pairs from outside, so a data change
    that merely permuted them (still distinct, but no longer these) also fails."""
    readings = pds.resolve_readings(pd.check_all(_source()))
    pairs = {r.name: (r.avadim_accent, r.penei_accent) for r in readings}
    assert pairs == {
        "m-trad taḥton": (pds.ROM_ETNAHTA, pds.ROM_SILLUQ),
        "m-trad elyon": (pds.ROM_SILLUQ, pds.ROM_REVIA),
        "p-trad taḥton": (pds.ROM_SILLUQ, pds.ROM_SILLUQ),
        "p-trad elyon": (pds.ROM_REVIA, pds.ROM_REVIA),
    }
    assert len(set(pairs.values())) == len(pairs)  # pairwise distinct
