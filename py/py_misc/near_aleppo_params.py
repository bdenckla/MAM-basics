"""Parameters and templates added by the near-Aleppo dataset.

MAM's input does not contain these names. A renamed note keeps MAM's original
target in MAM_TARGET, while its numbered parameters preserve the note's clauses.
POINTED_KETIV carries the pointed ketiv shown alongside MAM's pointed qere.
FLAGS identify the edition's evidence clauses. MARKS_WITHOUT_LETTER explicitly
identifies artificial carriers used for marks without a written consonant.

The near-Aleppo edition checks these shared declarations against its build.
"""

from mb_cmn import ws_tmpl2 as wtp
from py_misc import orphan_marks

MAM_TARGET = "מקרא על פי המסורה"
APPLIED_AND_FLAGGED = "applied-and-flagged"
FLAGGED_NOT_APPLIED = "flagged-not-applied"
FLAGS = (APPLIED_AND_FLAGGED, FLAGGED_NOT_APPLIED)
POINTED_KETIV = "כתיב מנוקד"
RENAMED_DOC = "נוסח למקרא על פי המסורה"
RENAMED_SCRDFFTAR = "הערה-2 למקרא על פי המסורה"
MARKS_WITHOUT_LETTER = "ניקוד בלי אות"

# The render tags of the lines the edition adds to a note: a parameter's name, and a
# fixed English sentence that is a flag's value.
LABEL_TAG = "near-aleppo-label"
ENGLISH_TAG = "near-aleppo-english"

_DOC_NAMES = ("נוסח", RENAMED_DOC)


def is_doc_template(wtel):
    """Whether ``wtel`` is a note: MAM's נוסח, or the dataset's RENAMED_DOC."""
    return wtp.is_template_with_name_in(wtel, _DOC_NAMES)


def split_params(tmpl, mam_keys, added_keys):
    """The keys of ``tmpl``'s parameters that are MAM's and the keys the dataset adds.

    Each list is in the template's order. A key in neither ``mam_keys`` nor
    ``added_keys`` raises, so that a parameter no one has decided how to show is
    never dropped or shown silently.
    """
    mam, added = [], []
    for key in wtp.template_param_keys(tmpl):
        if key in added_keys:
            added.append(key)
        elif key in mam_keys:
            mam.append(key)
        else:
            raise ValueError(
                f"{wtp.template_name(tmpl)}: parameter {key!r} is neither MAM's "
                f"{sorted(mam_keys)} nor one the near-aleppo dataset adds here, "
                f"{sorted(added_keys)}"
            )
    return mam, added


def split_doc_params(tmpl):
    """``split_params`` for a note: MAM's are its numbered parameters, 1 and up.

    A note of MAM's text has two, its target and its body, and a note that
    MAM-with-doc's conversions make has more. The dataset adds the flags to either
    name, and MAM_TARGET, which RENAMED_DOC always has and נוסח never does.
    """
    name = wtp.template_name(tmpl)
    keys = list(wtp.template_param_keys(tmpl))
    numbered = [key for key in keys if key.isdigit()]
    if numbered != [str(index) for index in range(1, 1 + len(numbered))]:
        raise ValueError(f"{name}: numbered parameters {numbered}")
    added_keys = FLAGS + ((MAM_TARGET,) if name == RENAMED_DOC else ())
    mam, added = split_params(tmpl, numbered, added_keys)
    if name == RENAMED_DOC and MAM_TARGET not in added:
        raise ValueError(f"{name} without {MAM_TARGET}")
    return mam, added


def raw_params(tmpl, keys):
    """``tmpl``'s parameters named by ``keys``, as the JSON stores them, in order."""
    return {key: tmpl["tmpl_params"][key] for key in keys}


def with_params(tmpl, params):
    """``tmpl`` with ``params`` after its own; a key it already has raises."""
    if not params:
        return tmpl
    own = tmpl.get("tmpl_params", {})
    clash = set(own) & set(params)
    if clash:
        raise ValueError(f"{wtp.template_name(tmpl)} already has {sorted(clash)}")
    return {**tmpl, "tmpl_params": {**own, **params}}
