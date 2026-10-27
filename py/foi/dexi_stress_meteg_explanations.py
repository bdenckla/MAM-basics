"""The dexi-stress-meteg FOI page's introduction, table cells and script.

The introduction's figures are the numbers of calls that foiz_wt_dexi_stress_meteg
records under its CENSUS_FOI_PATHS, and its two examples are the first calls, in the
order of the books, of two of those kinds; both are read when the page is generated.
"""

import json

from foi import dexi_stress_meteg_translations as translations
from foi import foiz_wt_dexi_stress_meteg as dsm
from mb_misc import mb_html

COUNTED_FOI_PATHS = frozenset(dsm.CENSUS_FOI_PATHS.values())
_HEBREW = {"lang": "hbo", "dir": "rtl"}
# An example is a paragraph of its own, centered.
_EXAMPLE = {**_HEBREW, "style": "text-align: center"}
# A table cell's lines above and below, as MAM-with-doc's verse rows have them.
_BORDERED = {"class": "top-n-bot-bordered"}
# The button above each note, labelled with what a click on it shows.
_TOGGLE_CLASS = "translation-toggle"
_TO_ENGLISH = "click to show English translation"
_TO_HEBREW = "click to show original Hebrew"
_HIDDEN = {"hidden": ""}
# The page's script, after its table. A note's cell holds its button, then the
# Hebrew note, then the note's English translation, hidden. A click on the button
# shows whichever of the two is hidden in place of the other, and relabels the button.
SCRIPT = f"""
for (const button of document.querySelectorAll({json.dumps(f"button.{_TOGGLE_CLASS}")})) {{
  button.addEventListener("click", () => {{
    const [hebrew, english] = button.parentElement.querySelectorAll(":scope > div");
    hebrew.hidden = !hebrew.hidden;
    english.hidden = !hebrew.hidden;
    button.textContent = hebrew.hidden
      ? {json.dumps(_TO_HEBREW)}
      : {json.dumps(_TO_ENGLISH)};
  }});
}}
"""


def overall_explanation(census):
    """Return the introduction's HTML; census gives, for each census foi_path, the
    rows of the מ:דחי calls of its kind, in the order of the books."""
    if set(census) != COUNTED_FOI_PATHS:
        raise ValueError(f"census rows for other foi_paths: {sorted(census)}")
    calls = {kind: census[foi_path] for kind, foi_path in dsm.CENSUS_FOI_PATHS.items()}
    kinds = {kind: len(kind_calls) for kind, kind_calls in calls.items()}
    earlier_atom = calls[dsm.METEG_ON_EARLIER_ATOM]
    earlier_in_atom = calls[dsm.METEG_EARLIER_IN_STRESSED_ATOM]
    if not (earlier_atom and earlier_in_atom):
        raise ValueError(f"no example of a meteg before the stress: {kinds}")
    before = len(earlier_atom) + len(earlier_in_atom)
    rows = kinds[dsm.METEG_ON_HELPER_LETTER]
    if before <= rows:
        raise ValueError(f"no longer usually before the stressed syllable: {kinds}")
    paragraphs = (
        " ".join(
            (
                "Deḥi is prepositive, so its position does not necessarily show",
                "which syllable of its chanted word has the stress. A stress helper",
                "shows it: a second deḥi on the first letter of the stressed",
                "syllable. MAM's template מ:דחי gives a chanted word in two forms,",
                "parameter 1 without the helper and parameter 2 with it, and since",
                "2026-10-26 MAM-with-doc has shown parameter 2. Taamey D, the font",
                "of these pages, draws the helper as a top meteg, a vertical bar",
                "above its letter.",
            )
        ),
        " ".join(
            (
                "Below are the chanted words whose parameter 1 has a meteg on the",
                "letter where parameter 2 has the helper, the two parameters being",
                "otherwise the same. MAM's parameter 2 lacks that meteg, but with the",
                "helper drawn above the letter and the meteg below it, MAM-with-doc",
                "keeps the meteg: since 2026-10-27 it has shown each of these",
                "chanted words as parameter 2 with parameter 1's meteg. In each row,",
                "parameter 1 is above the chanted word as MAM-with-doc shows it, with",
                "both the meteg and the helper, and to their left is MAM's",
                "documentation note on the word, as MAM-with-doc shows it too. Each",
                f"of those notes describes the meteg as “{dsm.NOTE_WORDS}”, a ga'ya",
                "stroke to show where the stress is.",
            )
        ),
        " ".join(
            (
                "A button above each note shows an English translation of the note",
                "in its place. These are AI-generated translations, not yet reviewed",
                "by a human: Claude, an AI model, translated the notes into English",
                "on 2026-10-27.",
            )
        ),
    )
    return (
        *map(mb_html.para, paragraphs),
        _lead_in(
            (
                "A meteg in parameter 1 is usually before the stressed syllable.",
                f"Of MAM's {sum(kinds.values()):,} uses of מ:דחי, parameter 1 has",
                f"no meteg in {kinds[dsm.NO_METEG]:,}. In {before:,}, it has meteg",
                "marks only before the stressed syllable. In",
                f"{len(earlier_atom):,} of those, a meteg is on an earlier atom of",
                "a maqaf compound, as in this chanted word from",
            ),
            earlier_atom[0],
            ", shown with parameter 1 above parameter 2:",
        ),
        _example(earlier_atom[0]),
        _lead_in(
            (
                f"In the other {len(earlier_in_atom):,}, the meteg marks are only",
                "earlier in the atom with the stress, as in this chanted word from",
            ),
            earlier_in_atom[0],
            ":",
        ),
        _example(earlier_in_atom[0]),
        mb_html.para(_rows_sentence(rows)),
    )


def _rows_sentence(rows):
    if not rows:
        return "In none is a meteg on the letter where parameter 2 has the helper."
    return (
        f"Only in the {rows:,} below is a meteg on the letter where parameter 2 has"
        " the helper."
    )


def _lead_in(words, call, after):
    """A paragraph of the words, the verse of the call, and after."""
    return mb_html.para((" ".join(words), " ", *call["bcv_anchor"], after))


def _example(call):
    """The call's parameter 1 above its parameter 2, as a paragraph of its own."""
    if set(call) != {"bcv_anchor", "parameter_2", "html_contents"}:
        raise ValueError(f"unexpected census row keys: {sorted(call)}")
    return mb_html.para(_above(call["html_contents"], call["parameter_2"]), _EXAMPLE)


def _above(upper, lower):
    return upper, mb_html.line_break(), lower


def html_row_cells(row_dic):
    """The note, below a button that shows the note's English translation in its
    place; then parameter 1 above the chanted word as MAM-with-doc shows it, which
    keeps parameter 1's meteg; then the verse. Each cell is lined above and below, so
    that the lines divide the table's rows.

    The note's cell holds a Hebrew block and an English one, so the Hebrew block, not
    the cell, has the Hebrew language and direction: a Hebrew cell would set the
    English in the Hebrew font at its larger size, and enlarge the Hebrew words
    quoted in the English a second time."""
    keys = {"bcv_anchor", "parameter_2", "mam_with_doc", "note", "html_contents"}
    if set(row_dic) != keys:
        raise ValueError(f"unexpected row keys: {sorted(row_dic)}")
    hebrew = {**_BORDERED, **_HEBREW}
    forms = _above(row_dic["html_contents"], row_dic["mam_with_doc"])
    toggle = mb_html.button(_TO_ENGLISH, {"type": "button", "class": _TOGGLE_CLASS})
    note = (
        toggle,
        mb_html.div(row_dic["note"], _HEBREW),
        mb_html.div(translations.english_note(row_dic["note"]), _HIDDEN),
    )
    return (
        mb_html.table_datum(note, _BORDERED),
        mb_html.table_datum(forms, hebrew),
        mb_html.table_datum(row_dic["bcv_anchor"], _BORDERED),
    )
