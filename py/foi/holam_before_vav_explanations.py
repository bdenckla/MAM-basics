"""Reader-facing labels and display for the holam-before-vav FOI."""

from collections import Counter
from pathlib import Path

from accgram import printed_decalogue_strands as names
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hp
from mb_cmn import str_defs as sd
from mb_cmn import unicode_data
from mb_misc import mb_html
from py_html.my_html_span_romanized import rmn

TITLE = "Holam before vav"
STYLE = Path(__file__).with_suffix(".css").read_text(encoding="utf-8")
_NAMES = {
    ha.ZAQ_Q: names.ROM_ZAQEF_QATAN + " qatan",
    ha.REV: names.ROM_REVIA,
    ha.MAH: names.ROM_MAHAPAKH,
    ha.MER: names.ROM_MERKHA,
    ha.MUN: names.ROM_MUNAX,
    ha.TIP: names.ROM_TIPEHA,
    hp.MTGOSLQ: names.ROM_METEG,
}
_VOWEL_NAMES = {
    hp.SEGOL_V: "segol vowel",
    hp.QAMATS: names.ROM_QAMATS,
    hp.TSERE: "tsere",
}


def _name(mark):
    return _NAMES.get(mark) or _VOWEL_NAMES.get(mark) or unicode_data.name(mark)


def qualifier_for_html(qualifier):
    """Name every mark on the matched vav, preserving the source order."""
    parts = []
    for mark in qualifier["vav_marks"]:
        if parts:
            parts.append(", ")
        if mark == sd.CGJ:
            parts.append("combining grapheme joiner")
        else:
            parts.append(rmn(_name(mark)))
    bhl = qualifier["bhl"]
    if bhl:
        page = mb_html.span(
            f"BHL p. {bhl['printed_page']}",
            {
                "title": f"Scan {bhl['scan_filename']}; inventory position {bhl['inventory_index_1based']}"
            },
        )
    else:
        page = "BHL page not located"
    return {"Vav marks": parts or ["None"], "BHL page": page}


def introduction(rows):
    """Derive every displayed count from the newly generated FOI rows."""
    above = Counter(
        mark for row in rows for mark in row["vav_marks"] if mark in ha.UNI_OVER_ACCENTS
    )
    mark_counts = []
    for mark, count in above.items():
        if mark_counts:
            mark_counts.append("; ")
        mark_counts.extend((rmn(_name(mark)), f": {count}"))
    return [
        mb_html.heading_level_1(TITLE),
        mb_html.para(
            f"All {len(rows)} occurrences in {len({r['bcv_short'] for r in rows})} verses "
            "of MAM. A non-vav letter has a holam dot, and the next letter is vav; "
            "combining marks may intervene. The divine name, including prefixed "
            "occurrences, is excluded. Holam haser for vav is also excluded."
        ),
        mb_html.para(
            "The blue text marks the holam-bearing letter and following vav. "
            "The original marks remain on their original letters. Hebrew is enlarged "
            "and spaced to make the mark placement easier to inspect."
        ),
        mb_html.para(
            ["Above-marks on the matched vav: ", *mark_counts, "."]
            if mark_counts
            else "No matched vav has an above-accent."
        ),
        mb_html.para(
            "The marks column names all marks on the matched vav. "
            "An accent on another letter does not put an occurrence in the first group."
        ),
        mb_html.para(
            "BHL page numbers are the printed page numbers, checked against the "
            "verse text. Hover over a page number for its scan filename and inventory "
            "position. These locations do not imply agreement with MAM's pointing. "
            "In Nehemiah 6:6, the target is on page 1113 although that page's header "
            "begins at 6:7."
        ),
    ]
