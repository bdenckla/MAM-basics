"""Exports evaluate"""

from mb_cmn import shrink
from mb_cmn import ws_tmpl2 as wtp
from mb_cmn import template_names as tmpln
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_accents as ha
from mb_cmn import str_defs as sd


def evaluate(wtel):
    """Evaluate boring templates in every branch of a recognized container.

    "Boring" templates are ones that all editions treat the same.
    So there's no point in preserving them.

    This is a structure-preserving edition transformation, not a Scripture
    survey: a preserved template deliberately retains and transforms every one
    of its parameters, including documentation and alternative branches.  The
    preserved-name roster is closed so a new template cannot become a
    transparent recursive container by default.
    """
    if isinstance(wtel, str):
        return wtel
    if isinstance(wtel, (tuple, list)):
        return _flatten_then_shrink(list(map(evaluate, wtel)))
    name = wtp.template_name(wtel)
    handler = _HANDLERS.get(name)
    if handler is None:
        if name not in PRESERVED_TEMPLATE_NAMES:
            raise ValueError(f"unclassified template in boring-template pass: {name!r}")
        return wtp.mktmpl_mp(evaluate, wtel)
    validate_current_handler_input_template(wtel)
    if isinstance(handler, str):
        return handler
    return handler(wtel)


def _flatten_then_shrink(wtels):
    accum = []
    for wtel in wtels:
        if isinstance(wtel, (tuple, list)):
            accum.extend(wtel)
        else:
            accum.append(wtel)
    return shrink.shrink(accum)


def _handle_yerushalayim(tmpl):  # 635 cases
    return _yerushalax_subhandler(tmpl, hpo.XIRIQ)


def _handle_yerushalayemah(tmpl):  # 4 cases
    return _yerushalax_subhandler(tmpl, hpo.SHEVA)


def _handle_qupo(tmpl):  # 4 cases
    assert wtp.template_len(tmpl) == 2
    el10 = wtp.template_i0(tmpl, 1)
    above_accent = evaluate(el10)
    assert isinstance(above_accent, str)
    # The above-accent is the O in QUPO (O for "over").
    return sd.CGJ + hpo.PATAX + above_accent  # cPO of QUcPO


def _handle_accent(tmpl):
    assert wtp.template_len(tmpl) == 2
    el10 = wtp.template_i0(tmpl, 1)
    # Below, we strip off the 1st code point.
    # The 1st code point is presumably a dummy letter whose only role is to
    # "hold" the accent.
    return el10[1:]


def _handle_word_with_puncta_extraordinaria(tmpl):
    assert wtp.template_len(tmpl) == 2
    return evaluate(wtp.template_i0(tmpl, 1))


def _handle_pseudo_title(tmpl):
    assert wtp.template_len(tmpl) == 2
    el1_proper = wtp.template_param_val(tmpl, "כותרת")
    return evaluate(el1_proper)


def _handle_bold(tmpl):
    assert wtp.template_len(tmpl) == 2
    ei0 = evaluate(wtp.template_i0(tmpl, 1))
    if ei0 == "":
        # There's a bold of קק that we want to turn into
        # nothing instead of bold of nothing.
        return ""
    return tmpl


def _just_take_arg_1(tmpl):
    assert wtp.template_len(tmpl) == 2
    return evaluate(wtp.template_element(tmpl, 1))


def _yerushalax_subhandler(tmpl, vowel_for_implicit_yod):
    assert wtp.template_len(tmpl) in (2, 3)
    # Below, accent is a "maybe" since sometimes there is no
    # accent. E.g. accent on the word is dexi, a prepositive
    # without a helper.
    vowel = wtp.template_i0(tmpl, 1)
    assert isinstance(vowel, str)
    accent = _tmpl_i0_maybe(tmpl, 2, "")
    assert isinstance(accent, str)
    return vowel + accent + sd.CGJ + vowel_for_implicit_yod


def _tmpl_i0_maybe(tmpl, idx, default=None):
    """
    Acts like template_i0 if element i exists and is nonempty.
    Otherwise returns default.
    """
    if wtp.template_len(tmpl) <= idx:
        return default
    eli = wtp.template_element(tmpl, idx)
    return default if len(eli) == 0 else wtp.first_and_only(eli)


_HANDLERS = {
    "מודגש": _handle_bold,
    "מ:ירושלם": _handle_yerushalayim,
    "מ:ירושלמה": _handle_yerushalayemah,
    tmpln.TWO_ACCENTS_OF_QUPO: _handle_qupo,
    "מ:טעם": _handle_accent,
    "מ:אות מנוקדת": _handle_word_with_puncta_extraordinaria,
    "פרשה-מרכז": _handle_pseudo_title,  # Job and Proverbs
    "גלגל-2": _just_take_arg_1,
    "ירח בן יומו-2": _just_take_arg_1,
    #
    "מ:טעם ומתג באות אחת": sd.CGJ + hpo.MTGOSLQ,
    "מ:כל קמץ קטן מרכא": "כׇּ֥ל",
    "מ:גרש ותלישא גדולה": ha.G1_TG,
    "מ:גרשיים ותלישא גדולה": ha.G2_TG,
    #
    "רווח בסוף שורה": "",
    "קק": "",
    "עוגן בשורה": "",
    # Other candidates for "pre-evaluation"
    # 'מ:נו"ן הפוכה': {_MASK_EL: _handle_inverted_nun},
}

_CURRENT_HANDLER_INPUT_PARAM_POLICY = {
    "מודגש": (frozenset({"1"}), frozenset({"1"})),
    "מ:ירושלם": (frozenset({"1"}), frozenset({"1", "2"})),
    "מ:ירושלמה": (frozenset({"1", "2"}), frozenset({"1", "2"})),
    tmpln.TWO_ACCENTS_OF_QUPO: (frozenset({"1"}), frozenset({"1"})),
    "מ:טעם": (frozenset({"1"}), frozenset({"1"})),
    "מ:אות מנוקדת": (frozenset({"1"}), frozenset({"1"})),
    "פרשה-מרכז": (frozenset({"כותרת"}), frozenset({"כותרת"})),
    "גלגל-2": (frozenset({"1"}), frozenset({"1"})),
    "ירח בן יומו-2": (frozenset({"1"}), frozenset({"1"})),
    "מ:טעם ומתג באות אחת": (frozenset(), frozenset()),
    "מ:כל קמץ קטן מרכא": (frozenset(), frozenset()),
    "מ:גרש ותלישא גדולה": (frozenset(), frozenset()),
    "מ:גרשיים ותלישא גדולה": (frozenset(), frozenset()),
    "רווח בסוף שורה": (frozenset(), frozenset()),
    "קק": (frozenset({"1", "2"}), frozenset({"1", "2"})),
    "עוגן בשורה": (frozenset({"1"}), frozenset({"1"})),
}
assert frozenset(_CURRENT_HANDLER_INPUT_PARAM_POLICY) == frozenset(_HANDLERS)


def validate_current_handler_input_template(tmpl):
    """Validate a current plain-only template after conversion to tmpl2 form."""
    if not isinstance(tmpl, dict) or not isinstance(tmpl.get("tmpl_name"), str):
        raise TypeError(f"not a converted current template: {tmpl!r}")
    name = tmpl["tmpl_name"]
    policy = _CURRENT_HANDLER_INPUT_PARAM_POLICY.get(name)
    if policy is None:
        raise ValueError(f"not a current boring-template input: {name!r}")
    extra_object_keys = set(tmpl) - {"tmpl_name", "tmpl_params"}
    if extra_object_keys:
        raise ValueError(
            f"unexpected object keys for current boring-template input {name!r}: "
            f"{sorted(extra_object_keys)!r}"
        )
    params = tmpl.get("tmpl_params", {})
    if not isinstance(params, dict):
        raise TypeError(
            f"non-mapping params for current boring-template input {name!r}: {params!r}"
        )
    required, allowed = policy
    actual = frozenset(params)
    if not required <= actual or not actual <= allowed:
        raise ValueError(
            f"unexpected parameters for current boring-template input {name!r}: "
            f"required {sorted(required)!r}, allowed {sorted(allowed)!r}, "
            f"got {sorted(actual)!r}"
        )
    return params


PRESERVED_TEMPLATE_NAMES = (
    tmpln.CURRENT_PLUS_TMPL_NAMES | {tmpln.SCRDFF_NO_TAR, "מ:לגרמיה", "קו״כ-אם"}
) - set(_HANDLERS)
RECOGNIZED_TEMPLATE_NAMES = PRESERVED_TEMPLATE_NAMES | set(_HANDLERS)
