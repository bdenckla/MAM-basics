def explanation_for_path(path_parts):
    if len(path_parts) != 3:
        return None
    cantsys, fp_lvl_3, acc_str = path_parts
    return _EXPLANATION_OVERRIDES.get(path_parts) or _generic_explanation(
        cantsys, fp_lvl_3, acc_str
    )


def _generic_explanation(cantsys, fp_lvl_3, acc_str):
    ending_clause = _ending_clause(fp_lvl_3)
    detail = _detail_for_profile(acc_str)
    return _wrap(cantsys, ending_clause, detail)


def _wrap(cantsys, ending_clause, inner):
    return (
        f"that the cantillation system is {cantsys}, that {ending_clause}, "
        f"and that the profile is, in detail, {inner}. {_A_SBR}"
    )


def _ending_clause(fp_lvl_3):
    if fp_lvl_3.startswith("(") and fp_lvl_3.endswith(")"):
        return f"the profile ends in {fp_lvl_3[1:-1]}"
    return _ENDING_CLAUSES.get(
        fp_lvl_3, f"the profile falls in the {fp_lvl_3} category"
    )


def _detail_for_profile(acc_str):
    if acc_str.startswith("-"):
        return f"nothing{acc_str}; {_NOTHING}"
    return acc_str


_A_SBR_RAW = """
The “profile” is the accent/maqaf/meteg profile.
Comma means one or more letters (but no maqaf marks) intervene;
dash means exactly one maqaf intervenes.
Other separators, if present, are left in their compact profile notation.
Breuer references (if any) are listed alongside examples"""
_A_SBR = _A_SBR_RAW.replace("\n", " ").strip()
_NOTHING = "where “nothing” means an atom with no marks of note"

_ENDING_CLAUSES = {
    "a-misc": "the profile falls in the miscellaneous ending category",
    "psg-before-paseq": "the profile falls in the psg-before-paseq category",
    "psg-closed-after-tsere": "the profile falls in the psg-closed-after-tsere category",
    "psg-closed-by-guttural": "the profile falls in the psg-closed-by-guttural category",
    "psg-misc": "the profile falls in the miscellaneous psg category",
    "psg-open": "the profile falls in the psg-open category",
}

_EXPLANATION_OVERRIDES = {
    ("poetic", "(atn)", "(mer),(atn)"): _wrap(
        "poetic", "the profile ends in atn", "mer,atn"
    ),
    ("poetic", "(atn)", "(mer)-(atn)"): _wrap(
        "poetic", "the profile ends in atn", "mer-atn"
    ),
    ("poetic", "(atn)", "-(mer),(ümtg),(atn)"): _wrap(
        "poetic",
        "the profile ends in atn",
        "nothing-(mer,mtg,atn); " + _NOTHING,
    ),
}
