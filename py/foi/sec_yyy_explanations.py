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
    out = " ".join(
        (
            f"that the cantillation system is {cantsys} and that",
            f"{_shewa_pattern_clause(shewa_pattern)}",
        )
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
    return " ".join(
        (
            f"that the cantillation system is {cantsys}, that {ending_clause},",
            f"and that the profile is, in detail, {inner}",
        )
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
    for index, (operator_group, token) in enumerate(zip(operators, tokens[1:])):
        rendered.append(_operator_group_phrase(operator_group, is_first=index == 0))
        rendered.append(_clean_profile_token(token))
    out = "".join(rendered)
    if acc_str.startswith("-"):
        out += f"; {_NOTHING}"
    return out


def _clean_profile_token(token):
    return token.replace("(", "").replace(")", "")


def _operator_group_phrase(operator_group, is_first):
    if operator_group == "+":
        return (
            " sharing a letter with " if is_first else ", then sharing a letter with "
        )
    prefix = " followed, across " if is_first else ", then across "
    return f"{prefix}{_operator_group_span(operator_group)}, by "


def _operator_group_span(operator_group):
    if len(operator_group) == 1:
        return _single_operator_span(operator_group)
    if len(set(operator_group)) == 1 and operator_group[0] in _COUNTABLE_OPERATORS:
        return _countable_operator_span(operator_group[0], len(operator_group))
    return _sequential_operator_chain(operator_group)


def _single_operator_span(operator) -> str:
    return _SINGLE_OPERATOR_SPANS.get(operator, operator)


def _sequential_operator_chain(operator_group):
    spans = [_sequential_operator_span(operator) for operator in operator_group]
    return " followed by ".join(spans)


def _sequential_operator_span(operator) -> str:
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


def _shewa_pattern_clause(shewa_pattern):
    inner = _strip_guillemets(shewa_pattern)
    if inner == "gutt-:":
        return "the marked consonant is a guttural carrying simple shewa"
    parts = tuple(filter(None, inner.split(",")))
    rendered = tuple(_describe_shewa_part(part) for part in parts)
    if not rendered:
        return f"the shewa shorthand is {shewa_pattern}"
    if len(rendered) == 1:
        return f"the marked consonant carries {rendered[0]}"
    if len(rendered) == 2:
        return " ".join(
            (
                f"the marked consonant carries {rendered[0]} together with",
                f"{rendered[1]}",
            )
        )
    joined = ", ".join(rendered[:-1]) + f", and {rendered[-1]}"
    return f"the marked consonant carries {joined}"


def _strip_guillemets(text):
    if text.startswith("«") and text.endswith("»"):
        return text[1:-1]
    return text


def _describe_shewa_part(part) -> str:
    return _SHEWA_PATTERN_PARTS.get(part, part)


_NOTHING = "where “nothing” means an atom with no marks of note"
_PROFILE_OPERATOR_SPLIT = re.compile(r"([,~+\-]+)")
_COUNT_WORDS = {2: "two", 3: "three", 4: "four"}

_SINGLE_OPERATOR_SPANS = {
    ",": "one or more letters without maqaf",
    "-": "one maqaf",
    "~": "one gray maqaf",
    "+": "the same letter",
}

_SEQUENTIAL_OPERATOR_SPANS = {
    ",": "one or more letters without maqaf",
    "-": "a maqaf",
    "~": "a gray maqaf",
    "+": "the same letter",
}

_COUNTABLE_OPERATORS = {
    "-": ("maqaf mark", "maqaf marks"),
    "~": ("gray maqaf mark", "gray maqaf marks"),
}

_ENDING_CLAUSES = {
    "a-misc": "the profile falls in the miscellaneous ending category",
    "psg-before-paseq": "the profile falls in the psg-before-paseq category",
    "psg-closed-after-tsere": (
        "the profile falls in the psg-closed-after-tsere category"
    ),
    "psg-closed-by-guttural": (
        "the profile falls in the psg-closed-by-guttural category"
    ),
    "psg-misc": "the profile falls in the miscellaneous psg category",
    "psg-open": "the profile falls in the psg-open category",
}

_SHEWA_FOLLOWUP_CLAUSES = {
    "bgdkft-dagesh": "the following consonant is a bgdkft letter with dagesh",
    "double shewa": "the following consonant also carries shewa",
}

_SHEWA_PATTERN_PARTS = {
    ":": "simple shewa",
    ":∵": "ḥataf segol",
    ":_": "ḥataf pataḥ",
    ":a": "ḥataf qamats",
    "(mos)": "meteg",
    "varika": "varika",
}

OVERALL_EXPLANATION = (
    " ".join(
        (
            "These pages group examples by compact accent/maqaf/meteg profiles.",
            "The labels are not separate manuscript readings; they are profile",
            "summaries of how accents, maqaf, and meteg are arranged in the cited",
            "examples.",
        )
    ),
    " ".join(
        (
            "In these sec-profile pages, gray maqaf and implicit maqaf are",
            "equivalent terms. In the detailed profile labels, comma means one or",
            "more letters intervene without maqaf, dash means one maqaf, tilde",
            "means one gray maqaf, plus means the accents on either side share a",
            "letter, and repeated operator strings are read left to right.",
        )
    ),
    " ".join(
        (
            "Breuer references, when present, are listed alongside the examples",
            "rather than encoded in the profile itself.",
        )
    ),
)

OVERALL_EXPLANATION_SHEWA = (
    " ".join(
        (
            "These pages group sec-merk and sec-misc examples by the vocalization",
            "of the consonant that carries the relevant shewa or ḥataf sign.",
        )
    ),
    " ".join(
        (
            "In the shorthand labels, : means simple shewa, :∵ means ḥataf segol,",
            ":_ means ḥataf pataḥ, :a means ḥataf qamats, (mos) means meteg on",
            "that same consonant, varika means varika on that same consonant, and",
            "gutt-: means a guttural with simple shewa. Commas join marks that",
            "occur on the same consonant.",
        )
    ),
    " ".join(
        (
            "Any extra suffix such as double shewa or bgdkft-dagesh describes the",
            "following consonant, not the marked one.",
        )
    ),
)

OVERALL_EXPLANATION_REF = (
    " ".join(
        (
            "This page regroups sec-merk and sec-misc examples by the Breuer/CoS",
            "references cited for them.",
        )
    ),
    " ".join(
        (
            "Each section label such as 09.23 or 09.23.fn21 is a Breuer/CoS",
            "reference key rather than an accent-profile label. The rows below are",
            "the MAM examples whose qualifier data cites that reference.",
        )
    ),
    " ".join(
        (
            "The Breuer and CoS columns preserve the more specific citation strings",
            "and notes for each example.",
        )
    ),
)

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
