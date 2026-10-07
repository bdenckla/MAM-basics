"""Parameters and templates added by the near-Aleppo dataset.

MAM's input does not contain these names. A renamed note keeps MAM's original
target in MAM_TARGET. Parameter 2 is the reviewed near-Aleppo clause; MAM_NOTE
contains the remaining source clauses with their original MAM subject.
POINTED_KETIV carries the pointed ketiv shown alongside MAM's pointed qere.
FLAGS identify the edition's evidence clauses. MARKS_WITHOUT_LETTER explicitly
identifies artificial carriers used for marks without a written consonant.

The near-Aleppo edition checks these shared declarations against its build.
"""

from mb_cmn import ws_tmpl2 as wtp
from py_misc import orphan_marks as orphan_marks  # re-exported for the shared renderer

MAM_TARGET = "מקרא על פי המסורה"
MAM_NOTE = "הערת מקרא על פי המסורה"
APPLIED_AND_FLAGGED = "applied-and-flagged"
FLAGGED_NOT_APPLIED = "flagged-not-applied"
FLAGS = (APPLIED_AND_FLAGGED, FLAGGED_NOT_APPLIED)
POINTED_KETIV = "כתיב מנוקד"
RENAMED_DOC = "נוסח עם הקשר מקרא על פי המסורה"
RENAMED_SCRDFFTAR = "הערה-2 עם הקשר מקרא על פי המסורה"
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
    name. RENAMED_DOC additionally requires both MAM_TARGET and MAM_NOTE.
    """
    name = wtp.template_name(tmpl)
    keys = list(wtp.template_param_keys(tmpl))
    numbered = [key for key in keys if key.isdigit()]
    if numbered != [str(index) for index in range(1, 1 + len(numbered))]:
        raise ValueError(f"{name}: numbered parameters {numbered}")
    if name not in _DOC_NAMES:
        raise ValueError(f"Unknown note template {name}")
    added_keys = FLAGS + ((MAM_TARGET, MAM_NOTE) if name == RENAMED_DOC else ())
    mam, added = split_params(tmpl, numbered, added_keys)
    if name == RENAMED_DOC:
        validate_baked_note(tmpl)
    return mam, added


def validate_baked_note(tmpl):
    """Validate the complete explicit parameter contract of either baked note."""
    name = wtp.template_name(tmpl)
    if name not in (RENAMED_DOC, RENAMED_SCRDFFTAR):
        raise ValueError(f"Unknown baked note {name}")
    keys = set(wtp.template_param_keys(tmpl))
    numbered = {"1", "2", "3"} if name == RENAMED_SCRDFFTAR else {"1", "2"}
    required = numbered | {MAM_TARGET, MAM_NOTE}
    if (
        not required <= keys
        or keys - required - set(FLAGS)
        or len(keys & set(FLAGS)) > 1
    ):
        raise ValueError(f"{name}: invalid parameters {sorted(keys)}")
    params = tmpl["tmpl_params"]
    if not (isinstance(params["2"], str) or params["2"] == []):
        raise ValueError(f"{name}: near-Aleppo clause must be text or an empty array")
    if name == RENAMED_SCRDFFTAR and params["3"] not in ("*אאא", "אאא*"):
        raise ValueError(f"{name}: invalid scroll-note marker position")
    for key in required | (keys & set(FLAGS)):
        if not isinstance(params[key], (str, list, dict)):
            raise ValueError(f"{name}: invalid content for {key}")


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
