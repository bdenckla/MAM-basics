"""
Find the forms in MAM's documentation notes that use plus notation or double
guillemets.

POPULATION.  A documentation note is a נוסח template, and the population is its
body, parameter 2.  Notes are found in all three verse cells, columns C, D and
E, and in a book's good ending, whose wikitext element is itself a נוסח
template.  A MinirowExt's next_CP repeats the next verse's column C, so it is
not scanned.  A body is read at any depth: inside מ:כפול, inside qamats and
stress-helper alternatives, and inside templates within the body.  Every
template stays recognized by name, through all_branch_foilers.  MAM's
scroll-difference notes, the מ:הערה-2 template, are outside the population
unless one sits inside a documentation note's body.

FORMS.  In a note body, a form is one of the maximal runs that
foi_wikitext_helpers.forms finds: a run of Hebrew letters, Hebrew marks and
joiners, square brackets, plus signs and the two double guillemets, which that
function's docstring and constants define exactly.  The Unicode FOI reads note
bodies by the same forms.  Both read their strings as
foi_wikitext_helpers.with_attached_marks returns them, so a form keeps a
legarmeh, sof pasuq or maqaf that MAM-parsed-plus writes apart from it.  A form is
recorded under "plus" when one of its plus signs has a Hebrew letter, Hebrew
mark or joiner on each side.  It is recorded under "double-guillemets" when it
contains a LEFT-POINTING or RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK.  Each
form is one row, and a form with both notations appears in both categories.  No
classification of plus forms is inferred.

LIMITATION.  A template inside a note body splits the text around it into
separate strings, and each string is read alone.  So a form that a template
interrupts would be missed, or shown only in part.  None is today.
"""

import re

from foi import foi_gray_marks as gray_marks
from foi import foi_wikitext_helpers as fwh

FOI_PATHS = (
    ("doc-note-notation", "double-guillemets"),
    ("doc-note-notation", "plus"),
)
_FP_DOUBLE_GUILLEMETS, _FP_PLUS = FOI_PATHS


def find_fois_wt(mroge):
    """Find doc-note forms that use plus notation or double guillemets."""
    # mroge: minirow or good ending
    if minirow := mroge.get("mroge-minirow"):
        # Not minirow.next_CP, which repeats the next verse's column C.
        cells = minirow.CP, minirow.DP, minirow.EP
        wtseq = [wtel for cell in cells for wtel in fwh.with_attached_marks(cell)]
        return fwh.find_fois_in_wtseq(_FOILERS, wtseq)
    gewe = mroge["mroge-good-ending"]["wikitext_element"]
    return fwh.find_fois_in_wtseq(_FOILERS, fwh.with_attached_marks([gewe]))


def _find_fois_in_string(stack, string):
    if "doc-part-n" not in stack:
        return []
    fois = []
    for form in fwh.forms(string):
        # A form's notation is found in its text, and its row shows its gray marks.
        text, target = gray_marks.text(form), gray_marks.target(form)
        if _PLUS_BETWEEN.search(text):
            fois.append((_FP_PLUS, target))
        if _DOUBLE_GUILLEMET.search(text):
            fois.append((_FP_DOUBLE_GUILLEMETS, target))
    return fois


_FOILERS = fwh.all_branch_foilers(
    {
        str: _find_fois_in_string,
        "נוסח": fwh.label_args_of_doc,
    }
)

_PLUS_BETWEEN = re.compile(
    "[" + fwh.LETTERS_MARKS_JOINERS + r"]\+[" + fwh.LETTERS_MARKS_JOINERS + "]"
)
_DOUBLE_GUILLEMET = re.compile("[" + fwh.DOUBLE_GUILLEMETS + "]")
