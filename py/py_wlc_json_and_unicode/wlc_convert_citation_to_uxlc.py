"""Exports get_tanach_dot_us_url, get_uxlc_bkid."""

from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id


def get_std_bcv(wlc_bcv_str):
    """
    Return a bcv triple like ('Genesis', 1, 1) for a WLC bcv string like 'gn1:1'.
    The returned book ID is a standard book ID.
    (bcv: book, chapter, & verse).
    """
    std_bkid = get_std_bkid(wlc_bcv_str)
    cv_pair = get_cv_pair(wlc_bcv_str)
    return std_bkid, *cv_pair


def get_std_bkid(wlc_bcv_str):
    """Return the standard book ID for WLC bcv string (bcv: book, chapter, & verse)"""
    wlc_bkid = wlc_bcv_str[:2]
    return wlc_bb_to_bk39id(wlc_bkid)


def get_cv_pair(wlc_bcv_str):
    """Return chapter & verse integer pair for WLC bcv string (bcv: book, chapter, & verse)"""
    wlc_cv_str = _get_cv_str(wlc_bcv_str)
    c_str, v_str = wlc_cv_str.split(":")
    return int(c_str), int(v_str)


def _get_cv_str(wlc_bcv_str):
    wlc_cv_str = wlc_bcv_str[2:]
    return wlc_cv_str
