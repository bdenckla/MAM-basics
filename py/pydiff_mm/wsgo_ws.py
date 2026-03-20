"""Exports massage_ws_book"""

from pycmn import ws_tmpl1 as wtp1
from pycmn import hebrew_accents as ha
from pycmn.my_utils import dv_dispatch
from pycmn.my_utils import dv_map
from pycmn.my_utils import sl_map
from pycmn.my_utils import first_and_only
from pycmn.shrink import shrink


def massage_ws_book(wsf2_book):
    """
    Massage a format-2 book from Wikisource, preparing it for
    comparison with a book from Google.
    """
    return dv_map(_massage_ws_chapter, wsf2_book)


def _massage_ws_chapter(ws_chapter):
    ws_chap_1 = dv_dispatch(_CDISPATCH, ws_chapter)
    ws_chap_1["golike_chapter_prefix"] = _golike_cp(ws_chap_1)
    ws_chap_1["golike_chapter_suffix"] = _golike_cs(ws_chap_1)
    return ws_chap_1


def _golike_cp(ws_chap):
    return _golike_wninc(ws_chap["ws-chap-noinclude-header"])


def _golike_cs(ws_chap):
    wide_ninc = _golike_wninc(ws_chap["ws-chap-noinclude-footer"])
    wide_gden = _golike_wgden(ws_chap.get("ws-chap-good-ending"))
    return wide_gden + wide_ninc


_ASB_NINC = {"custom_tag": "noinclude"}
_ASE_NINC = {"custom_tag": "/noinclude"}
_ASB_GDEN = {"custom_tag": "קטע התחלה=סיום בטוב/"}  # ASB: abtag section begin
_ASE_GDEN = {"custom_tag": "קטע סוף=סיום בטוב/"}  # ASE: abtag section end


def _golike_wninc(narrow_ninc):
    return [_ASB_NINC, narrow_ninc, _ASE_NINC]


def _golike_wgden(narrow_gden):
    return ["////", _ASB_GDEN, narrow_gden, _ASE_GDEN] if narrow_gden else []


def _massage_ws_chapter_body(ws_chapter_body):
    return dv_map(_massage_plb_verse, ws_chapter_body)


def _massage_plb_verse(plb_verse):
    """
    Massage a "plb verse" from Wikisource, preparing it for
    comparison with a verse from Google.
    A "plb verse" is a dict with keys "prefix", "location", and "body".
    """
    return dv_dispatch(_VDISPATCH, plb_verse)


def _massage_ws_wt_list(wt_list):
    return _cmass_ws_wt_list("mctx-generic", wt_list)


def _cmass_ws_wt_list(mctx, wt_list):
    """
    Massage a list of Wikitext elements from Wikisource, preparing it for
    comparison with a list of Wikitext elements from Google.
    The prefix "cmass" means massage with mctx.
    """
    assert isinstance(wt_list, list)
    out = sl_map((_cmass_ws_wtel, mctx), wt_list)
    return shrink(out)  # E.g. ["//", "==xxx=="] becomes "//==xxx=="


def _massage_prefix(prefix):
    generic = _cmass_ws_wt_list("mctx-prefix", prefix)
    # We use "generic" to mean generically massaged, i.e.
    # not yet massaged in a prefix specific way, only massaged
    # in generic ways.
    assert isinstance(generic, list)
    if _has_double_slash(generic) and not _has_spacing_tmpl(generic):
        return list(map(_ds_to_du, generic))
    return generic


def _ds_to_du(wtel):
    return "__" if wtel == "//" else wtel


def _is_double_slash(obj):
    return obj == "//"


def _has_double_slash(wtseq):
    return any(map(_is_double_slash, wtseq))


def _has_spacing_tmpl(wtseq):
    return any(map(_is_spacing_tmpl, wtseq))


def _is_spacing_tmpl(wtel):
    if not wtp1.is_template(wtel):
        return False
    if wtp1.is_doc_template(wtel):
        tel1 = wtp1.template_element(wtel, 1)
        return _has_spacing_tmpl(tel1) or tel1 in ([" "], ["__"])
    tel00 = wtp1.template_name(wtel)
    return _IS_SPACING_TMPL[tel00]


_IS_SPACING_TMPL = {
    "קק": False,
    "עוגן בשורה": False,
    ##########
    "סס": True,
    "ססס": True,
    "פפ": True,
    "פפפ": True,
    "מ:ששש": True,
    "ר4": True,
    "ר1": True,
}


def _massage_ws_wtel(ws_wtel):
    return _cmass_ws_wtel("mctx-generic", ws_wtel)


_THIRTY_TWO = {
    "mctx-prefix": "__",
    "mctx-generic": " ",
}


def _cmass_ws_wtel(mctx, wtel):  # cmass: massage with mctx
    """
    Massage a Wikitext element from Wikisource, preparing it for
    comparison with a Wikitext element from Google.
    """
    if wtel == "&#32;":
        return _THIRTY_TWO[mctx]
    if wtel == "¶":
        return "//"
    if isinstance(wtel, str):
        return _germuq_revia(wtel)
    if isinstance(wtel, list):
        return _cmass_ws_wt_list(mctx, wtel)
    assert isinstance(wtel, dict)
    if wtp1.is_abtag(wtel):
        return wtel
    return _cmass_tmpl(mctx, wtel)


def _germuq_revia(in_str):
    """Standardize on germuq-then-revia order"""
    return in_str.replace(ha.REV + ha.GER_M, ha.GER_M + ha.REV)


def _cmass_tmpl(mctx, tmpl):  # cmass: massage with mctx
    tels_in = wtp1.template_elements(tmpl)
    assert isinstance(tels_in, list)
    tels_out = sl_map((_cmass_ws_wt_list, mctx), tels_in)
    return wtp1.mktmpl(tels_out)


_CDISPATCH = {
    "ws-chap-noinclude-header": _massage_ws_wt_list,
    "ws-chap-body": _massage_ws_chapter_body,
    "ws-chap-good-ending": _massage_ws_wt_list,
    "ws-chap-noinclude-footer": _massage_ws_wt_list,
    "ws-chap-category": lambda x: x,
}
_VDISPATCH = {
    "prefix": _massage_prefix,
    "location": _massage_ws_wtel,
    "verse-body": _massage_ws_wt_list,
}
