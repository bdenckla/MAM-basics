"""Find a ḥolam dot on a letter other than vav before a vav in MAM.

Select the nontrivial qere, the pointed ketiv for a trivial ketiv/qere,
the first stress-helper form, the dalet qamats alternative, and combined
cantillation. The renderer lists every match outside the divine name and
selects a representative of each category for the divine name.
"""

from foi import foi_struct as fct
from hkq_cmn.qere_projection import QereProjectionPolicy, project_qere_atoms
from mb_cmn import bib_locales as tbn
from mb_cmn import stress_helper_forms as shf
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_letters as hl
from mb_cmn import hebrew_points as hp
from mb_cmn import hebrew_punctuation as hpu
from mb_misc import mb_html
from py_html.hebrew_letter_spacing import iter_atoms

STEM = "holam-before-vav"
_DIVINE_WITH = (STEM, "The divine name with an accent above vav")
_DIVINE_WITHOUT = (STEM, "The divine name without an accent above vav")
DIVINE_NAME_PATHS = frozenset((_DIVINE_WITH, _DIVINE_WITHOUT))
_OTHER_WITH = (STEM, "Other forms with a mark above vav")
_OTHER_WITHOUT = (STEM, "Other forms without a mark above vav")
OTHER_CATEGORIES = frozenset((_OTHER_WITH[1], _OTHER_WITHOUT[1]))
_POLICY = QereProjectionPolicy(
    name="holam-before-vav-foi",
    trivial_qere_argument_key="1",
    stress_helper_forms=(shf.PARAMETER_1,),
    qamats_argument_keys=("ד",),
    dual_cantillation_argument_keys=("כפול",),
)
_ABOVE_MARKS = ha.UNI_OVER_ACCENTS | {
    hp.XOLAM,
    hp.XOLAM_XFV,
    hp.RAFE,
    hp.SHIND,
    hp.SIND,
    hp.VARIKA,
    hpu.UPDOT,
    hpu.MCIRC,
}


def find_fois_wt(mroge):
    """Return one FOI row per matching pair."""
    minirow = mroge.get("mroge-minirow")
    if minirow is None:
        return []  # A repeated good ending is a second display of the same verse.
    text = "".join(
        item["text"]
        for item in project_qere_atoms(minirow.EP, source=None, policy=_POLICY)
    )
    return [
        feature
        for _, _, atom in iter_atoms(text)
        for feature in _features_in_atom(atom, mroge["mroge-bcvt"])
    ]


def _features_in_atom(atom, bcvt):
    starts = [i for i, char in enumerate(atom) if hl.ALEF <= char <= hl.TAV]
    clusters = list(zip(starts, starts[1:] + [len(atom)]))
    consonants = "".join(atom[i] for i in starts)
    for (start, stop), (next_start, next_stop) in zip(clusters, clusters[1:]):
        if atom[next_start] != hl.VAV:
            continue
        marks = atom[start + 1 : stop]
        if atom[start] == hl.VAV:
            if hp.XOLAM_XFV in marks:
                raise ValueError(
                    "Expected no vav with HOLAM HASER FOR VAV (U+05BA) followed "
                    f"by vav at {tbn.short_bcv_of_bcvt(bcvt)}: {atom!r}"
                )
        elif hp.XOLAM in marks:
            vav_marks = atom[next_start + 1 : next_stop]
            is_divine_name = consonants.endswith("יהוה") and start == starts[-3]
            yield _feature(atom, start, next_stop, vav_marks, is_divine_name)


def _feature(atom, start, stop, marks, is_divine_name):
    if is_divine_name:
        path = (
            _DIVINE_WITH if ha.UNI_OVER_ACCENTS.intersection(marks) else _DIVINE_WITHOUT
        )
    else:
        path = _OTHER_WITH if _ABOVE_MARKS.intersection(marks) else _OTHER_WITHOUT
    target = (
        atom[:start],
        mb_html.span_c(atom[start:stop], "mam-doc-target-without-callout"),
        atom[stop:],
    )
    return path, fct.make_qtarget(target, {"vav_marks": marks})
