"""
Find the מ:דחי calls whose parameter 1 has a meteg on the letter where parameter 2
has the dexi's stress helper, and count every מ:דחי call by where its parameter 1
has a meteg.

POPULATION.  Every מ:דחי call in MAM-parsed-plus: in the three verse cells,
columns C, D and E, and in a book's good ending, at any depth.  A MinirowExt's
next_CP repeats the next verse's column C, so it is not scanned.  Every template
stays recognized by name, through all_branch_foilers.

KINDS.  Each parameter is compared as the text of its chanted word.  A parameter
is that text, or one מ:אות-מיוחדת-במילה, a word with a special letter, whose
parameter 2 is the word's text uninterrupted; any other parameter raises.  The two
texts must have the same letters, and their marks must differ on exactly one
letter, the helper's letter, where parameter 2 has one dexi more than parameter 1.
If, apart from that dexi, parameter 2 lacks only a meteg that parameter 1 has on
that letter, the call is one of the page's rows, and both of its parameters must
be text.  A row shows parameter 1 above the chanted word as MAM-with-doc renders
it, with its render options: parameter 2 with parameter 1's meteg kept.  If
nothing else differs, parameter 1 has no
meteg, or has meteg marks only before the helper's letter, at least one on an
earlier atom of a maqaf compound or all of them in the helper's atom.  Any other
call raises, so that the page's introduction, which states these kinds, is
revised rather than made false.

NOTES.  A row's note is the innermost נוסח whose target holds the call, rendered
as MAM-with-doc renders a note, with its render options.  A row outside every
note's target, or whose note lacks the words that the page's introduction quotes,
raises, for the same reason.

Every call is also recorded, with its two texts, under the CENSUS_FOI_PATHS of its
kind.  foi_finals gives those to the page's introduction, which counts them and
takes its examples from them, rather than listing them.
"""

import functools
from collections import Counter
import unicodedata

from foi import foi_struct as fct
from foi import foi_wikitext_helpers as fwh
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import template_names as tmpln
from mb_cmn import ws_tmpl2 as wtp
from mwd import mwd_write_book as mwdwb
from py_misc import mam_doc_utils as doc_utils
from py_misc import mwd_utils as mwdu
from py_misc import ren_html_for_renel as hfr
from py_misc import ren_html_from_ren_el_mapping as hfrm
from render_wt import render_wikitext_handlers as handlers
from render_wt import render_wikitext_helpers as wt_help

STEM = "dexi-stress-meteg"
ROWS_FOI_PATH = (STEM,)
NO_METEG = "no-meteg"
METEG_ON_EARLIER_ATOM = "meteg-on-earlier-atom"
METEG_EARLIER_IN_STRESSED_ATOM = "meteg-earlier-in-stressed-atom"
METEG_ON_HELPER_LETTER = "meteg-on-helper-letter"
CENSUS_FOI_PATHS = {
    kind: (STEM, "census", kind)
    for kind in (
        NO_METEG,
        METEG_ON_EARLIER_ATOM,
        METEG_EARLIER_IN_STRESSED_ATOM,
        METEG_ON_HELPER_LETTER,
    )
}
FOI_PATHS = (ROWS_FOI_PATH, *CENSUS_FOI_PATHS.values())
# The words of the notes that the page's introduction quotes.
NOTE_WORDS = "קו של געיה להורות על מקום הטעם"
# For each template that a parameter can be, its parameter that holds the chanted
# word's text uninterrupted, as render_wikitext_handlers also has it.
_UNINTERRUPTED_WORD_PARAMETERS = {tmpln.SLH_WORD: "2"}


def find_fois_wt(mroge):
    """Find the rows and count the kinds of מ:דחי call."""
    # mroge: minirow or good ending
    bcvt = mroge["mroge-bcvt"]
    foilers = fwh.all_branch_foilers(
        {
            "מ:דחי": functools.partial(_handle_dexi, bcvt),
            "נוסח": functools.partial(_handle_doc, bcvt),
        }
    )
    if minirow := mroge.get("mroge-minirow"):
        # Not minirow.next_CP, which repeats the next verse's column C.
        wtseq = (*minirow.CP, *minirow.DP, *minirow.EP)
    else:
        wtseq = [mroge["mroge-good-ending"]["wikitext_element"]]
    fois = fwh.find_fois_in_wtseq(foilers, wtseq)
    for foi_path, target in fois:
        if foi_path == ROWS_FOI_PATH and fct.qtar_qual(target)["note"] is None:
            raise ValueError(f"{bcvt}: a row's call is in no note's target: {target}")
    return fois


def _handle_dexi(bcvt, foilers, _stack, tmpl):
    text_1, text_2 = (_text(bcvt, tmpl, val) for val in _params(tmpl))
    kind = _kind(bcvt, tmpl, text_1, text_2)
    census_target = fct.make_qtarget(text_1, {"parameter_2": text_2})
    fois = [(CENSUS_FOI_PATHS[kind], census_target)]
    if kind == METEG_ON_HELPER_LETTER:
        if _params(tmpl) != [[text_1], [text_2]]:
            raise ValueError(f"{bcvt}: a row with a special-letter word: {tmpl!r}")
        qualifier = {
            "parameter_2": text_2,
            "mam_with_doc": _mam_with_doc_form(bcvt, tmpl),
            "note": None,
        }
        fois.append((ROWS_FOI_PATH, fct.make_qtarget(text_1, qualifier)))
    for key in ("1", "2"):
        fois += fwh.find_fois_in_wtseq(foilers, wtp.template_param_val(tmpl, key))
    return fois


def _handle_doc(bcvt, foilers, _stack, tmpl):
    # A note's target is walked before its body, and an inner note gives its rows
    # their note before this one is reached, so a row gets the innermost note.
    target_fois = fwh.find_fois_in_wtseq(foilers, wtp.template_param_val(tmpl, "1"))
    body_fois = fwh.find_fois_in_wtseq(foilers, wtp.template_param_val(tmpl, "2"))
    return [_with_note(bcvt, tmpl, foi) for foi in target_fois] + body_fois


def _with_note(bcvt, note, foi):
    foi_path, target = foi
    if foi_path != ROWS_FOI_PATH or fct.qtar_qual(target)["note"] is not None:
        return foi
    body = wtp.template_param_val(note, "2")
    if not any(isinstance(wtel, str) and NOTE_WORDS in wtel for wtel in body):
        raise ValueError(f"{bcvt}: a row's note lacks {NOTE_WORDS}: {note!r}")
    qualifier = {**fct.qtar_qual(target), "note": _note_html(bcvt, note)}
    return foi_path, fct.make_qtarget(fct.qtar_proper(target), qualifier)


def _mam_with_doc_form(bcvt, tmpl):
    """The chanted word as MAM-with-doc's verse column has it."""
    hctx = handlers.default_hctx(bcvt, mwdwb.RENOPTS_MAM_WITH_DOC)
    form = wt_help.render_wtseq(hctx, [tmpl])
    if not (len(form) == 1 and isinstance(form[0], str)):
        raise ValueError(f"{bcvt}: MAM-with-doc's form is not text: {form!r}")
    return form[0]


def _note_html(bcvt, note):
    """The note as MAM-with-doc's note column has it."""
    hctx = handlers.default_hctx(bcvt, mwdwb.RENOPTS_MAM_WITH_DOC)
    (doc,) = doc_utils.extract_docs(wt_help.render_wtseq(hctx, [note]))
    hfr_ctx = hfr.HfrCtx(hfrm.HT_TAC_FOR_RT_FOR_MAM_WITH_DOC)
    return mwdu.html_for_self_contained_note(hfr_ctx, doc)


def _params(tmpl):
    return [wtp.template_param_val(tmpl, key) for key in ("1", "2")]


def _text(bcvt, tmpl, val):
    """The text of the chanted word that the parameter val holds."""
    if len(val) != 1:
        raise ValueError(f"{bcvt}: a parameter of {len(val)} elements: {tmpl!r}")
    (wtel,) = val
    if isinstance(wtel, str):
        return wtel
    name = wtp.template_name_if_is_template(wtel)
    if name not in _UNINTERRUPTED_WORD_PARAMETERS:
        raise ValueError(f"{bcvt}: a parameter that is not a word: {tmpl!r}")
    word = wtp.template_param_val(wtel, _UNINTERRUPTED_WORD_PARAMETERS[name])
    if not (len(word) == 1 and isinstance(word[0], str)):
        raise ValueError(f"{bcvt}: a special-letter word that is not text: {tmpl!r}")
    return word[0]


def _kind(bcvt, tmpl, text_1, text_2):
    clusters_1, clusters_2 = _clusters(text_1), _clusters(text_2)
    if [cluster[:2] for cluster in clusters_1] != [
        cluster[:2] for cluster in clusters_2
    ]:
        raise ValueError(f"{bcvt}: parameters with different letters: {tmpl!r}")
    differing = [
        index
        for index, (cluster_1, cluster_2) in enumerate(zip(clusters_1, clusters_2))
        if cluster_1[2] != cluster_2[2]
    ]
    if len(differing) != 1:
        raise ValueError(f"{bcvt}: marks differ on {len(differing)} letters: {tmpl!r}")
    (helper,) = differing
    marks_1, marks_2 = clusters_1[helper][2], clusters_2[helper][2]
    if marks_2 - marks_1 != Counter({ha.DEX: 1}):
        raise ValueError(f"{bcvt}: parameter 2 adds no dexi alone: {tmpl!r}")
    removed = marks_1 - marks_2
    if removed == Counter({hpo.MTGOSLQ: 1}):
        return METEG_ON_HELPER_LETTER
    if removed:
        raise ValueError(f"{bcvt}: parameter 2 lacks marks of parameter 1: {tmpl!r}")
    metegs = [
        index for index, cluster in enumerate(clusters_1) if cluster[2][hpo.MTGOSLQ]
    ]
    if not metegs:
        return NO_METEG
    if max(metegs) >= helper:
        raise ValueError(f"{bcvt}: a meteg on or after the helper's letter: {tmpl!r}")
    helper_atom = clusters_1[helper][0]
    if any(clusters_1[index][0] < helper_atom for index in metegs):
        return METEG_ON_EARLIER_ATOM
    return METEG_EARLIER_IN_STRESSED_ATOM


def _clusters(text):
    """(atom index, letter, marks) for each character of text that is not a mark,
    with the marks after it; the atom index counts the maqaf marks and spaces up
    to and including that character."""
    clusters = []
    atom = 0
    for char in text:
        if unicodedata.category(char) == "Mn":
            if not clusters:
                raise ValueError(f"a mark with no letter before it: {text!r}")
            clusters[-1][2][char] += 1
            continue
        if char in (hpu.MAQ, " "):
            atom += 1
        clusters.append((atom, char, Counter()))
    return clusters
