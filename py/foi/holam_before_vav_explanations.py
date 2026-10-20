"""Reader-facing labels and display for the holam-before-vav FOI."""

from collections import Counter
from pathlib import Path

from accgram import printed_decalogue_strands as names
from mb_cmn import hebrew_accents as ha
from mb_misc import mb_html
from py_html.my_html_span_romanized import rmn

TITLE = "Holam before vav"
STYLE = Path(__file__).with_suffix(".css").read_text(encoding="utf-8")
_NAMES = {
    ha.ZAQ_Q: names.ROM_ZAQEF_QATAN + " qatan",
    ha.REV: names.ROM_REVIA,
}


def introduction(rows):
    """Derive every displayed count from the newly generated FOI rows."""
    above = Counter(
        mark for row in rows for mark in row["vav_marks"] if mark in ha.UNI_OVER_ACCENTS
    )
    mark_counts = []
    for mark, count in above.items():
        if mark_counts:
            mark_counts.append("; ")
        mark_counts.extend((rmn(_NAMES[mark]), f": {count}"))
    return [
        mb_html.heading_level_1(TITLE),
        mb_html.para(
            f"The two groups show all {len(rows)} occurrences in "
            f"{len({r['bcv_short'] for r in rows})} verses of MAM where a non-vav "
            "letter has a holam dot and the next letter is vav; combining marks may "
            "intervene. These groups exclude the divine name, including prefixed occurrences."
        ),
        mb_html.para(
            "In the selected MAM body text, no vav with HOLAM HASER FOR VAV "
            "(U+05BA) has another vav as its next base letter, allowing "
            "intervening combining marks."
        ),
        mb_html.para(
            "The blue text marks the holam-bearing letter and following vav. "
            "Each occurrence appears twice in its row: once with normal letter "
            "spacing and once with expanded letter spacing."
        ),
        mb_html.para(
            ['In "With an above-mark on vav": ', *mark_counts, "."]
            if mark_counts
            else "No matched vav has an above-accent."
        ),
    ]
