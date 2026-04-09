import re


def explanation_for_path(path_parts):
    if len(path_parts) != 3:
        return None
    cantsys, fp_lvl_3, acc_str = path_parts
    return _EXPLANATION_OVERRIDES.get(path_parts) or _generic_explanation(
        cantsys, fp_lvl_3, acc_str
    )


def explanation_for_shewa_path(path_parts):
    if len(path_parts) not in {2, 3}:
        return None
    cantsys, shewa_pattern, *rest = path_parts
    out = (
        f"that the cantillation system is {cantsys} and that the relevant "
        f"shewa pattern is shown as {shewa_pattern}"
    )
    if rest:
        out += f", and that {_shewa_followup_clause(rest[0])}"
    return out


def explanation_for_ref_path(path_parts):
    if len(path_parts) != 1:
        return None
    ref = path_parts[0]
    return f"that the examples below all cite Breuer/CoS reference {ref}"


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
    parts = _PROFILE_OPERATOR_SPLIT.split(acc_str)
    if len(parts) == 1:
        return _clean_profile_token(acc_str)
    tokens = parts[::2]
    operators = parts[1::2]
    rendered = []
    first_token = tokens[0] if tokens else ""
    rendered.append(_clean_profile_token(first_token) if first_token else "nothing")
    for operator_group, token in zip(operators, tokens[1:]):
        rendered.append(_operator_group_phrase(operator_group))
        rendered.append(_clean_profile_token(token))
    out = " ".join(rendered)
    if acc_str.startswith("-"):
        out += f"; {_NOTHING}"
    return out


def _clean_profile_token(token):
    return token.replace("(", "").replace(")", "")


def _operator_group_phrase(operator_group):
    if operator_group == "+":
        return "sharing a letter with"
    if len(operator_group) == 1:
        return f"followed, across {_single_operator_span(operator_group)}, by"
    if len(set(operator_group)) == 1 and operator_group[0] in _COUNTABLE_OPERATORS:
        repeated_span = _countable_operator_span(operator_group[0], len(operator_group))
        return f"followed, across {repeated_span}, by"
    return f"followed, across {_sequential_operator_chain(operator_group)}, by"


def _single_operator_span(operator):
    return _SINGLE_OPERATOR_SPANS.get(operator, operator)


def _joined_spans(spans):
    if len(spans) == 1:
        return spans[0]
    if len(spans) == 2:
        return f"{spans[0]} and {spans[1]}"
    return ", ".join(spans[:-1]) + f", and {spans[-1]}"


def _sequential_operator_chain(operator_group):
    spans = [_sequential_operator_span(operator) for operator in operator_group]
    return " followed by ".join(spans)


def _sequential_operator_span(operator):
    return _SEQUENTIAL_OPERATOR_SPANS.get(operator, _single_operator_span(operator))


def _countable_operator_span(operator, count):
    count_word = _COUNT_WORDS.get(count, str(count))
    singular, plural = _COUNTABLE_OPERATORS[operator]
    noun = singular if count == 1 else plural
    return f"{count_word} {noun}"


def _shewa_followup_clause(extra_part):
    return _SHEWA_FOLLOWUP_CLAUSES.get(
        extra_part, f"the following context is tagged as {extra_part}"
    )


_A_SBR_RAW = """
The “profile” is the accent/maqaf/meteg profile.
Comma means one or more letters (but no maqaf marks) intervene;
dash means exactly one maqaf intervenes.
Tilde means exactly one gray maqaf (implicit maqaf) intervenes;
plus means the accents on either side share a letter.
Repeated operator strings are read left to right.
Breuer references (if any) are listed alongside examples"""
_A_SBR = _A_SBR_RAW.replace("\n", " ").strip()
_NOTHING = "where “nothing” means an atom with no marks of note"
_PROFILE_OPERATOR_SPLIT = re.compile(r"([,~+\-]+)")
_COUNT_WORDS = {2: "two", 3: "three", 4: "four"}

_SINGLE_OPERATOR_SPANS = {
    ",": "one or more letters without maqaf",
    "-": "one maqaf",
    "~": "one gray maqaf (implicit maqaf)",
    "+": "the same letter",
}

_SEQUENTIAL_OPERATOR_SPANS = {
    ",": "one or more letters without maqaf",
    "-": "a maqaf",
    "~": "a gray maqaf (implicit maqaf)",
    "+": "the same letter",
}

_COUNTABLE_OPERATORS = {
    "-": ("maqaf mark", "maqaf marks"),
    "~": ("gray maqaf mark", "gray maqaf marks"),
}

_ENDING_CLAUSES = {
    "a-misc": "the profile falls in the miscellaneous ending category",
    "psg-before-paseq": "the profile falls in the psg-before-paseq category",
    "psg-closed-after-tsere": "the profile falls in the psg-closed-after-tsere category",
    "psg-closed-by-guttural": "the profile falls in the psg-closed-by-guttural category",
    "psg-misc": "the profile falls in the miscellaneous psg category",
    "psg-open": "the profile falls in the psg-open category",
}

_SHEWA_FOLLOWUP_CLAUSES = {
    "bgdkft-dagesh": "the following consonant is a bgdkft letter with dagesh",
    "double shewa": "the following consonant also carries shewa",
}

_EXPLANATION_OVERRIDES = {
    ("poetic", "(atn)", "(mer),(atn)"): _wrap(
        "poetic", "the profile ends in atn", _detail_for_profile("(mer),(atn)")
    ),
    ("poetic", "(atn)", "(mer)-(atn)"): _wrap(
        "poetic", "the profile ends in atn", _detail_for_profile("(mer)-(atn)")
    ),
    ("poetic", "(atn)", "-(mer),(ümtg),(atn)"): _wrap(
        "poetic",
        "the profile ends in atn",
        _detail_for_profile("-(mer),(ümtg),(atn)"),
    ),
}
