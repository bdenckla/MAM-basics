"""Reader-facing labels and display for the holam-before-vav FOI."""

from collections import Counter
from pathlib import Path

from accgram import printed_decalogue_strands as names
from foi.foiz_wt_holam_before_vav import HASER_CATEGORY
from mb_cmn import hebrew_accents as ha
from mb_misc import mb_html
from py_html.my_html_span_romanized import rmn

TITLE = "Holam before vav and holam haser for vav"
STYLE = Path(__file__).with_suffix(".css").read_text(encoding="utf-8")
_NAMES = {
    ha.ZAQ_Q: names.ROM_ZAQEF_QATAN + " qatan",
    ha.REV: names.ROM_REVIA,
}


def section_sort_key(path):
    """Keep the two original sections first, then the separate encoding."""
    return path[-1] == HASER_CATEGORY, path


def spaced_examples(contents):
    """Show the same unmodified Hebrew nodes with two spacing presentations."""
    result = []
    for label, css_class in (
        ("Normal spacing", "holam-normal-spacing"),
        ("Expanded spacing", "holam-expanded-spacing"),
    ):
        result.extend(
            (
                mb_html.div(
                    label,
                    {"class": "holam-spacing-label", "dir": "ltr", "lang": "en"},
                ),
                mb_html.div(contents, {"class": css_class}),
            )
        )
    return result


def introduction(rows):
    """Derive every displayed count from the newly generated FOI rows."""
    pairs = [row for row in rows if row["fp"] != HASER_CATEGORY]
    haser = [row for row in rows if row["fp"] == HASER_CATEGORY]
    above = Counter(
        mark
        for row in pairs
        for mark in row["vav_marks"]
        if mark in ha.UNI_OVER_ACCENTS
    )
    mark_counts = []
    for mark, count in above.items():
        if mark_counts:
            mark_counts.append("; ")
        mark_counts.extend((rmn(_NAMES[mark]), f": {count}"))
    return [
        mb_html.heading_level_1(TITLE),
        mb_html.para(
            f"The first two groups show all {len(pairs)} occurrences in "
            f"{len({r['bcv_short'] for r in pairs})} verses of MAM where a non-vav "
            "letter has a holam dot and the next letter is vav; combining marks may "
            "intervene. These groups exclude the divine name, including prefixed occurrences."
        ),
        mb_html.para(
            f'The third group, "{HASER_CATEGORY}", shows all {len(haser)} occurrences '
            f"in {len({r['bcv_short'] for r in haser})} verses of the separate Unicode "
            "character HOLAM HASER FOR VAV (U+05BA). Each is on vav; another following "
            "vav is not required."
        ),
        mb_html.para(
            "In the first two groups, the blue text marks the holam-bearing letter "
            "and following vav. In the third group, it marks the vav with holam haser. "
            "The original marks remain on their original letters. Each occurrence "
            'is enlarged and shown with "Normal spacing" and "Expanded spacing"; '
            "only the letter spacing differs."
        ),
        mb_html.para(
            ['In "With an above-mark on vav": ', *mark_counts, "."]
            if mark_counts
            else "No matched vav has an above-accent."
        ),
    ]
