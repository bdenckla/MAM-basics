"""The dexi-stress-meteg FOI page's introduction and table cells.

The introduction's figures are the counts that foiz_wt_dexi_stress_meteg records
under its CENSUS_FOI_PATHS, read when the page is generated.
"""

from foi import foiz_wt_dexi_stress_meteg as dsm
from mb_misc import mb_html

COUNTED_FOI_PATHS = frozenset(dsm.CENSUS_FOI_PATHS.values())


def overall_explanation(counts):
    """Return the introduction's paragraphs; counts gives the number of מ:דחי calls
    of each kind by its census foi_path."""
    if set(counts) != COUNTED_FOI_PATHS:
        raise ValueError(f"census counts for other foi_paths: {sorted(counts)}")
    kinds = {kind: counts[foi_path] for kind, foi_path in dsm.CENSUS_FOI_PATHS.items()}
    earlier_atom = kinds[dsm.METEG_ON_EARLIER_ATOM]
    earlier_in_atom = kinds[dsm.METEG_EARLIER_IN_STRESSED_ATOM]
    before = earlier_atom + earlier_in_atom
    rows = kinds[dsm.METEG_ON_HELPER_LETTER]
    if before <= rows:
        raise ValueError(f"no longer usually before the stressed syllable: {kinds}")
    return (
        " ".join(
            (
                "Deḥi is prepositive, so its position does not show which syllable of",
                "its chanted word has the stress. A stress helper shows it: a second",
                "deḥi on the first letter of the stressed syllable. MAM's template",
                "מ:דחי gives a chanted word in two forms, parameter 1 without the",
                "helper and parameter 2 with it, and since 2026-10-26 MAM-with-doc",
                "has shown parameter 2.",
            )
        ),
        " ".join(
            (
                "Below are the chanted words whose parameter 1 has a meteg on the",
                "letter where parameter 2 has the helper, the two parameters being",
                "otherwise the same. In each row, parameter 1 is above parameter 2,",
                "and to their left is MAM's documentation note on the word, as",
                "MAM-with-doc shows it. Each of those notes describes the meteg as",
                f"“{dsm.NOTE_WORDS}”, a ga'ya stroke to show where the stress is.",
            )
        ),
        " ".join(
            filter(
                None,
                (
                    "A meteg in parameter 1 is usually before the stressed syllable.",
                    f"Of MAM's {sum(kinds.values()):,} uses of מ:דחי, parameter 1 has",
                    f"no meteg in {kinds[dsm.NO_METEG]:,}. In {before:,}, it has meteg",
                    "marks only before the stressed syllable: on an earlier atom of a",
                    f"maqaf compound in {earlier_atom:,}, and only earlier in the atom",
                    f"with the stress in {earlier_in_atom:,}.",
                    _rows_sentence(rows),
                    _unclassified_sentence(kinds[dsm.TEMPLATE_IN_PARAMETER]),
                ),
            )
        ),
    )


def _rows_sentence(rows):
    if not rows:
        return "In none is a meteg on the letter where parameter 2 has the helper."
    return (
        f"Only in the {rows:,} below is a meteg on the letter where parameter 2 has"
        " the helper."
    )


def _unclassified_sentence(count):
    if not count:
        return ""
    if count == 1:
        return (
            "The remaining one has a template inside a parameter and is not"
            " classified here."
        )
    return (
        f"The remaining {count:,} have a template inside a parameter and are not"
        " classified here."
    )


def html_row_cells(row_dic):
    """The note, then parameters 1 and 2 one above the other, then the verse."""
    if set(row_dic) != {"bcv_anchor", "parameter_2", "note", "html_contents"}:
        raise ValueError(f"unexpected row keys: {sorted(row_dic)}")
    hebrew = {"lang": "hbo", "dir": "rtl"}
    forms = row_dic["html_contents"], mb_html.line_break(), row_dic["parameter_2"]
    return (
        mb_html.table_datum(row_dic["note"], hebrew),
        mb_html.table_datum(forms, hebrew),
        mb_html.table_datum(row_dic["bcv_anchor"]),
    )
