"""Exports massage_go_book"""

import unicodedata

from pycmn.my_utils import dv_map
from pycmn.my_utils import dv_dispatch
from pycmn import ws_tmpl1 as wtp1


def massage_go_book(go_book):
    """
    Massage a Google book
    into a format suitable for comparison with a Wikisource book.
    """
    return dv_dispatch(_BDISPATCH, go_book)


def _massage_go_verses(go_verses):
    return dv_map(_massage_minirow, go_verses)


def _massage_minirow(minirow):
    """
    This function massages the Google verse, preparing it for
    comparison with a Wikisource verse.
    """
    return {
        "prefix": _massage_wt_tuple(minirow.CP),
        "location": _massage_wt_tuple(minirow.DP),
        "verse-body": _massage_wt_tuple(minirow.EP),
    }


def _massage_wt_list(wt_list):
    """
    This function massages a list of Google Wikitext elements,
    preparing that list for comparison with its Wikisource counterpart.
    """
    # wt list: list of wt els
    # wt el: Wikitext element
    # Wikitext element: one of the following:
    #     a str
    #     a singleton dict with key 'custom_tag' or 'tmpl'
    assert isinstance(wt_list, list)
    return list(map(_massage_wtel, wt_list))


def _massage_wt_tuple(wt_tuple):
    assert isinstance(wt_tuple, tuple)
    return tuple(map(_massage_wtel, wt_tuple))


def _massage_wtel(wtel):
    if isinstance(wtel, str):
        norm = unicodedata.normalize("NFC", wtel)
        if norm == "׆__":  # inverted nun then double underscore
            norm = "׆ "
        return norm
    if wtp1.is_abtag(wtel):
        return wtel
    tels = wtp1.template_elements(wtel)
    assert isinstance(tels, list)
    new_tels = list(_massage_wt_list(tel) for tel in tels)
    return wtp1.mktmpl(new_tels)


_BDISPATCH = {
    "verses_plain": _massage_go_verses,
    "good_ending_plain": lambda x: x,
    "chapter_prefixes": lambda x: x,
    "chapter_suffixes": lambda x: x,
}
