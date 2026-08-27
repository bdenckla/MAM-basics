"""Bot edit: replace the manuscript sigil ב2 with ת451, per MAM-basics#260.

MAM's sigil ב2 and its sigil ת451 name the SAME manuscript. The MAM editor
(skadish1) chose ב2 first, for its proximity to ב1, then abandoned it -- ב2 is
used in the literature for other things, and the manuscript is not in the
British Library -- and switched to the number the manuscript had when Meir
Benayahu held it. Many uses of ב2 were already written by then and were never
updated. He asked for the replacement on 2026-04-10 and restated it 2026-08-27.

The sigil stands in exactly one book, over six of Daniel's twelve chapters, 32
times in all. Every one of the 32 is preceded by a comma (the sigil is never the
first member of an authority list) and none is followed by a digit, so a plain
string replacement is exact -- there is no ב20 or ב21 to guard against.

TWO GUARDS, because the same two characters occur many hundreds of times
elsewhere in this tree and not one of those occurrences is a sigil -- 216 in the
five Torah books of in/mam-ws/ alone, measured 2026-08-27:

  1. The per-chapter expected-count table below. A (bk39id, he_chnu) pair the
     table does not name is returned UNCHANGED, so the transform cannot touch a
     page it was not measured against; a pair the table does name must hold
     exactly the counted number of occurrences.
  2. The aliyah-parameter assertion. The Torah's {{מ:עלייה}} calls carry a named
     parameter spelled with the same two characters -- 216 of them across the
     five Torah books -- always preceded by "|" and followed by "=", where the
     sigil is always preceded by ",". A page carrying one is not a page this
     transform may touch, so finding one is an error rather than a skip.

THIS TRANSFORM IS ONE-SHOT BY DESIGN, and that is a consequence of guard 1
rather than an oversight. The count table describes one corpus state: the state
in/mam-ws/F1-Daniel.json was in when the counts were measured. Once the live
edit of Phase 3 has landed and its re-download has refreshed that file, a table
chapter holds zero occurrences, so re-running the bot over the refreshed corpus
raises on the count assertion instead of quietly doing nothing. That is the
right failure -- a bot era is run once -- but it is worth knowing before
re-running a proto rehearsal after Phase 3.

doc/PLAN-replace-sigil-b2-with-t451.md is the fuller statement, including the
four classes of non-sigil ב2 and the chain that carries the replacement from
Wikisource through the Google Sheet into MAM-parsed.
"""

from mb_cmn import bib_locales as tbn
from mb_cmn import hebrew_verse_numerals as hvn

_warnings = []

_B2 = "\N{HEBREW LETTER BET}2"
_T451 = "\N{HEBREW LETTER TAV}451"

# The aliyah template's named parameter, which is NOT the sigil. Spelled with
# both of its delimiters, since it is the delimiters that tell the two apart.
_ALIYAH_PARAM = f"|{_B2}="

# Chapter numbers are integers here and Hebrew numerals in the table built from
# them, so that no Hebrew numeral is typed by hand: a mistyped key would drop
# its whole chapter silently, the table being a skip list as well as a count.
_EXPECTED_BY_INT_CHAPTER = {
    tbn.BK_DANIEL: {7: 17, 8: 2, 9: 3, 10: 3, 11: 6, 12: 1},
}

_EXPECTED = {
    bk39id: {hvn.INT_TO_STR_DIC[chnu]: count for chnu, count in by_chnu.items()}
    for bk39id, by_chnu in _EXPECTED_BY_INT_CHAPTER.items()
}


def get_warnings():
    return list(_warnings)


def expected_counts(bk39id):
    """One book's Hebrew-chapter-to-count table, empty for a book not named."""
    return dict(_EXPECTED.get(bk39id, {}))


def expected_total():
    """The total this transform expects to replace, across every chapter."""
    return sum(sum(by_chnu.values()) for by_chnu in _EXPECTED.values())


def edit_page_text(bk39id, he_chnu, page_text):
    expected = _EXPECTED.get(bk39id, {}).get(he_chnu)
    if expected is None:
        return page_text
    assert _ALIYAH_PARAM not in page_text, (
        f"{bk39id} chapter {he_chnu} carries the aliyah parameter"
        f" {_ALIYAH_PARAM!r}, so it is not a page this transform may touch"
    )
    count = page_text.count(_B2)
    assert count == expected, (
        f"Expected {expected} occurrence(s) of {_B2!r} in {bk39id} chapter"
        f" {he_chnu}, found {count}"
    )
    _warnings.append(
        {
            "bk39id": bk39id,
            "he_chnu": he_chnu,
            "chapter": hvn.STR_TO_INT_DIC[he_chnu],
            "reason": "sigil-replaced",
            "count": count,
        }
    )
    return page_text.replace(_B2, _T451)
