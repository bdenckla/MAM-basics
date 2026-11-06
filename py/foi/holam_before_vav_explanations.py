"""Reader-facing labels and display for the ḥolam-before-vav FOI."""

from pathlib import Path

from foi import foiz_wt_holam_before_vav as holam_foi
from mb_misc import mb_html

TITLE = "Ḥolam before vav"
STYLE = Path(__file__).with_suffix(".css").read_text(encoding="utf-8")


def introduction(rows):
    """Describe the corpus and the representative examples."""
    ordinary = [row for row in rows if row["fp"] in holam_foi.OTHER_CATEGORIES]
    verses = {row["bcv_short"] for row in ordinary}
    return [
        mb_html.heading_level_1(TITLE),
        mb_html.para(
            f"Outside the divine name, the tables show all {len(ordinary)} occurrences "
            f"in {len(verses)} verses of the selected MAM body text where a letter other "
            "than vav has a ḥolam dot and the next letter is vav. Combining marks may "
            "intervene. The tables group these occurrences by whether the vav carries "
            "a mark above it."
        ),
        mb_html.para(
            "For the divine name, the tables show the first matching occurrence in "
            "book and verse order for each of two types, with and without an accent "
            "above the vav."
        ),
        mb_html.para(
            "In the selected MAM body text, no vav with HOLAM HASER FOR VAV (U+05BA) "
            "has another vav as its next base letter, allowing intervening combining marks."
        ),
        mb_html.para(
            "The blue text marks the letter carrying the ḥolam dot and the following "
            "vav. Each occurrence appears twice in its row, once with normal letter "
            "spacing and once with expanded letter spacing."
        ),
    ]


def html_target_cells(contents):
    """Render the same pointed atom at two spacings."""
    attrs = {"lang": "hbo", "dir": "rtl"}
    return tuple(
        mb_html.table_datum(mb_html.span_c(contents, spacing), attrs)
        for spacing in ("holam-normal-spacing", "holam-expanded-spacing")
    )
