"""The forms that a stress-helper template gives a chanted word.

MAM's two stress-helper templates, template_names.STRESS_HELPER_TMPL_NAMES, each
have two parameters: parameter 1 is the chanted word with its accent alone, and
parameter 2 is the same chanted word with the accent's stress helper as well.  A
third form is parameter 2 keeping a meteg that parameter 1 has where parameter 2
lacks it.  The renderer's ro_stress_helper option
(render_wt/render_wikitext_handlers.py) and the policies of
hkq_cmn/qere_projection.py each choose among the three by name; this module,
which the renderer held until 2026-11-12, checks the parameters and derives the
third form for both.
"""

import unicodedata
from collections import Counter

from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hpo
from mb_cmn import template_names as tmpln
from mb_cmn import ws_tmpl2 as wtp
from mb_cmn.my_utils import first_and_only
from mb_cmn.my_utils import first_and_only_and_str

PARAMETER_1 = "parameter 1"
PARAMETER_2 = "parameter 2"
PARAMETER_2_KEEPING_METEG = "parameter 2 keeping meteg"
FORM_NAMES = frozenset((PARAMETER_1, PARAMETER_2, PARAMETER_2_KEEPING_METEG))

# The accent of which each template's parameter 2 has one more: its stress helper.
_STRESS_HELPER_ACCENTS = {"מ:דחי": ha.DEX, "מ:צינור": ha.Z_OR_TSOR}
# For each template that a stress-helper parameter can be, its parameter holding
# the uninterrupted chanted word as text.
_UNINTERRUPTED_WORD_PARAMETERS = {tmpln.SLH_WORD: "2"}


def forms(tmpl, where):
    """Return the three forms of a stress-helper template, keyed by FORM_NAMES.

    They are parameter 1, parameter 2, and parameter 2 keeping parameter 1's meteg.
    Each is a parameter value, a list of strings and templates.  ``where`` begins
    each error message; the renderer passes its verse.

    Raises unless parameter 2 is parameter 1 with one more of the template's accent,
    its stress helper, on one letter, where parameter 2 may also lack a meteg that
    parameter 1 has, as a few calls of מ:דחי in MAM do (the FOI page
    foi-dexi-stress-meteg lists them). The third form keeps that meteg.
    A parameter that is a special-letter word is compared through its uninterrupted
    word, and may not lack such a meteg, since nothing here keeps one inside it.
    """
    if set(wtp.template_param_keys(tmpl)) != {"1", "2"}:
        raise ValueError(f"{where}: unexpected stress-helper parameters: {tmpl!r}")
    helper = _STRESS_HELPER_ACCENTS[wtp.template_name(tmpl)]
    val1, val2 = (wtp.template_param_val(tmpl, name) for name in ("1", "2"))
    for name, val in (("1", val1), ("2", val2)):
        if all(wtel == "" for wtel in val):
            raise ValueError(f"{where}: empty stress-helper parameter {name}: {tmpl!r}")
    found = {PARAMETER_1: val1, PARAMETER_2: val2}
    if all(isinstance(wtel, str) for wtel in (*val1, *val2)):
        kept = _with_kept_meteg(where, "".join(val1), "".join(val2), helper)
        return {**found, PARAMETER_2_KEEPING_METEG: val2 if kept is None else [kept]}
    word1, word2 = (_uninterrupted_word(where, val) for val in (val1, val2))
    if _with_kept_meteg(where, word1, word2, helper) is not None:
        raise ValueError(f"{where}: a meteg to keep in a special-letter word: {tmpl!r}")
    return {**found, PARAMETER_2_KEEPING_METEG: val2}


def _uninterrupted_word(where, val):
    """Return the text of a stress-helper parameter that is one special-letter word."""
    wtel = first_and_only(val)
    name = wtp.template_name_if_is_template(wtel)
    if name not in _UNINTERRUPTED_WORD_PARAMETERS:
        raise ValueError(f"{where}: unexpected stress-helper parameter: {val!r}")
    param_val = wtp.template_param_val(wtel, _UNINTERRUPTED_WORD_PARAMETERS[name])
    return first_and_only_and_str(param_val)


def _with_kept_meteg(where, text1, text2, helper):
    """Return text2 with the meteg that text1 has where text2 has the helper.

    Returns None if text1 has no meteg there. Raises unless the two texts have the
    same letters and marks, except that on one letter text2 has one more helper and
    may lack a meteg that text1 has.
    """
    clusters1, clusters2 = _mark_clusters(text1), _mark_clusters(text2)
    differing = [
        i
        for i, (cl1, cl2) in enumerate(zip(clusters1, clusters2))
        if cl1[0] != cl2[0] or Counter(cl1[1]) != Counter(cl2[1])
    ]
    if len(clusters1) != len(clusters2) or len(differing) != 1:
        raise ValueError(f"{where}: unexpected stress-helper forms: {text1} {text2}")
    (i,) = differing
    (base, marks1), (base2, marks2) = clusters1[i], clusters2[i]
    added = Counter(marks2) - Counter(marks1)
    removed = Counter(marks1) - Counter(marks2)
    expected_removals = Counter(), Counter({hpo.MTGOSLQ: 1})
    if (
        base != base2
        or added != Counter({helper: 1})
        or removed not in expected_removals
    ):
        raise ValueError(f"{where}: unexpected stress-helper forms: {text1} {text2}")
    if not removed:
        return None
    kept = [char + "".join(marks) for char, marks in clusters2]
    kept[i] = base + "".join(marks1) + helper
    return "".join(kept)


def _mark_clusters(text):
    """Return each character that is not a combining mark, with the marks after it."""
    clusters = []
    for char in text:
        if unicodedata.category(char) != "Mn":
            clusters.append((char, []))
        elif clusters:
            clusters[-1][1].append(char)
        else:
            raise ValueError(f"a combining mark with no letter before it: {text!r}")
    return clusters
