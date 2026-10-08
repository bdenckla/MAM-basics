"""Check structural invariants after the last pointed-ketiv import.

Written consonants must remain the ketiv's, with artificial carriers excluded.
Raw combining marks need a written-letter owner; explicit orphan templates use
the existing GA/GV contract. These checks neither choose ownership nor assess
letter-local or whole-atom grammar, and never rewrite a pointing.
"""

import unicodedata

from mb_cmn import hebrew_letters
from mb_cmn import hebrew_points
from near_aleppo import phase2_templates as phase2
from py_misc import orphan_marks


def check_e_cell(value, verse):
    """Inspect Scripture targets before note copying, renaming and output writing."""
    if isinstance(value, str):
        return
    if isinstance(value, list):
        for item in value:
            check_e_cell(item, verse)
        return
    name = value["tmpl_name"]
    rule = phase2._RULES[name]
    params = value.get("tmpl_params", {})
    if rule.action == phase2._KEEP_NOTE:
        for key in phase2.selected_keys(value, verse):
            check_e_cell(params[key], verse)
    elif name in phase2.POINTED_KETIV_FAMILIES:
        if phase2.POINTED_KETIV_PARAMETER in params:
            _check_value(params[phase2.POINTED_KETIV_PARAMETER], params["1"], verse)
    elif name == "מ:קו״כ-אם-2":
        _check_value(params["1"], params["2"], verse)


def _check_value(value, ketiv, verse):
    parts = value if isinstance(value, list) else [value]
    written = []
    owner = False
    for part in parts:
        if isinstance(part, str):
            written.append(part)
            for char in part:
                if unicodedata.category(char).startswith("M") or char in (
                    hebrew_points.SHEVA_NA,
                    hebrew_points.DAGESH_XAZAQ,
                ):
                    if not owner:
                        raise AssertionError(
                            f"{verse}: raw mark {char!r} without a ketiv letter; "
                            "an orphan requires its explicit carrier template"
                        )
                elif char != "\N{ZERO WIDTH NON-JOINER}":
                    owner = "א" <= char <= "ת"
        else:
            orphan_marks.carriers(part, verse)
            owner = False
    if hebrew_letters.letters("".join(written)) != hebrew_letters.letters(ketiv):
        raise AssertionError(
            f"{verse}: pointed ketiv changes the written ketiv consonants "
            "(artificial carriers are not written letters)"
        )
