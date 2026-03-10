""" Exports massage """

from pycmn import hebrew_letters as hl
from pycmn import hebrew_points as hpo
from pycmn import hebrew_accents as ha
from pycmn import ws_tmpl1 as wtp1
from pycmn import template_names as tmpln
from pycmn import shrink
from pycmn import my_utils


def massage(minirow_dic):
    """
    Given a dict from cvt to minirow,
    Return a dict from cvt to massaged cell E values.
    By massaged I mean doc stripped & other changes to aid "GoGo" comparison
    """
    return my_utils.dv_map(_massage_minirow, minirow_dic)


def _massage_minirow(minirow):
    return tuple(_massage_wt_list(list(minirow.EP)))


def _massage_wt_list(wtseq):
    # wt list: list of wt els
    # wt el: Wikitext element
    # Wikitext element: one of the following:
    #     a str
    #     a singleton dict with key 'custom_tag' or 'tmpl'
    assert isinstance(wtseq, list)
    new_wtseqs = tuple(_massage_wtel(wtel) for wtel in wtseq)
    return shrink.shrink(sum(new_wtseqs, []))


# פסקא באמצע פסוק
# Take only elements 0 and 1 of the template, i.e.,
# drop the 2nd arg to this template, if present.
# The 2nd arg is a reiteration of the book, chapter, & verse.
# Differences in this arg (e.g., corrections to it) are not interesting.
#
# קרי ולא כתיב
# Take only elements 0 and 1 of this template, i.e.,
# any elements beyond those are documentation.
# (These inline documentation elements are only present in older MAM
# sources.)


def _massage_wtel(wtel):
    # returns a wt list since the process of stripping doc
    # can turn a wt el into a wt list
    handlers = {
        "נוסח": _take_el1,
        "מ:קמץ": _strip_space_after_sameq_from_el2,
        "שני טעמים באות אחת": _sheni_teamim_beot_exat,
        "פסקא באמצע פסוק": _discard_els_2_and_beyond,
        "קרי ולא כתיב": _discard_els_2_and_beyond,
        'קו"כ-אם': _discard_els_2_and_beyond,
        "ר0": _discard_els_2_and_beyond,
    }
    if isinstance(wtel, str):
        if wtel == "מִתַָּ֑֜חַת":
            return ["מִתָּ֑", _make_qupo_call(hl.TAV, ha.GER), "חַת"]
        no_double_slash = wtel.replace("//", "")
        return [no_double_slash]
    if tuple(wtel.keys()) == ("custom_tag",):
        return []
    if handler := handlers.get(wtp1.template_name(wtel)):
        return handler(wtel)
    return _massage_tmpl_elements(wtel)


def _massage_tmpl_elements(wtel):
    tels = wtp1.template_elements(wtel)
    new_tels = list(_massage_wt_list(tel) for tel in tels)
    return [wtp1.mktmpl(new_tels)]


def _sheni_teamim_beot_exat(tmpl):
    """Modernize calls to שני טעמים באות אחת by using the following templates
    where appropriate:
        מ:טעם ומתג באות אחת
        שני טעמים באות אחת קמץ-תחתון-פתח-עליון
    """
    irange = range(1, wtp1.template_len(tmpl))
    args = tuple(wtp1.template_i0(tmpl, i) for i in irange)
    if len(args) == 2 and args[1] == hpo.MTGOSLQ:
        wt_list = [args[0], wtp1.mktmpl([["מ:טעם ומתג באות אחת"]])]
        return wt_list
    if len(args) == 3 and args[1] == hpo.PATAX:
        wt_list = [args[0], _make_qupo_call(hl.NUN, args[2])]
        return wt_list
    return list(args)


def _make_qupo_call(base_letter, upper_accent):
    taam_call = wtp1.mktmpl([["מ:טעם"], [base_letter + upper_accent]])
    return wtp1.mktmpl([[tmpln.TWO_ACCENTS_OF_QUPO], [taam_call]])


def _discard_els_2_and_beyond(wtel):
    return [wtp1.mktmpl(wtp1.template_elements(wtel)[0:2])]


def _take_el1(wtel):
    wt_list = wtp1.template_element(wtel, 1)
    return _massage_wt_list(wt_list)


def _strip_space_after_sameq_from_el2(wtel):
    assert wtp1.template_len(wtel) == 3
    el2 = wtp1.template_element(wtel, 2)
    assert isinstance(my_utils.first_and_only(el2), str)
    el2_new = [el2[0].replace("ס= ", "ס=")]
    tel0_and_tel1 = wtp1.template_elements(wtel)[0:2]
    wtel_new = wtp1.mktmpl([*tel0_and_tel1, el2_new])
    return _massage_tmpl_elements(wtel_new)
