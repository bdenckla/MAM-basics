""" Exports massage """

from pycmn import ws_tmpl1 as wtp1
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
        "פסקא באמצע פסוק": _discard_els_2_and_beyond,
        'קו"כ-אם': _discard_els_2_and_beyond,
        "קרי ולא כתיב": _discard_els_2_and_beyond,
    }
    if isinstance(wtel, str):
        no_double_slash = wtel.replace("//", "")
        return [no_double_slash]
    if tuple(wtel.keys()) == ("custom_tag",):
        return []
    if handler := handlers.get(wtp1.template_name(wtel)):
        return handler(wtel)
    if wtp1.template_name(wtel) == "מ:כפול":
        wt_list = wtp1.named_template_element(wtel, 1, "כפול")
        return _massage_wt_list(wt_list)
    tels = wtp1.template_elements(wtel)
    new_tels = list(_massage_wt_list(tel) for tel in tels)
    return [wtp1.mktmpl(new_tels)]


def _discard_els_2_and_beyond(wtel):
    return [wtp1.mktmpl(wtp1.template_elements(wtel)[0:2])]


def _take_el1(wtel):
    wt_list = wtp1.template_element(wtel, 1)
    return _massage_wt_list(wt_list)
