"""Exports evaluate"""

from pycmn import shrink
from pycmn import ws_tmpl2 as wtp
from pycmn import template_names as tmpln
from pycmn import hebrew_points as hpo
from pycmn import hebrew_accents as ha
from pycmn import str_defs as sd


def evaluate(wtel):
    """
    Evaluate boring templates.
    "Boring" templates are ones that all editions treat the same.
    So there's no point in preserving them.
    """
    if isinstance(wtel, str):
        return wtel
    if isinstance(wtel, (tuple, list)):
        return _flatten_then_shrink(list(map(evaluate, wtel)))
    handler = _HANDLERS.get(wtp.template_name(wtel))
    if handler is None:
        return wtp.mktmpl_mp(evaluate, wtel)
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
    # accent. E.g. accent on the word is dehi, a prepositive
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
