"""Exports get_tanach_dot_us_url, get_uxlc_bkid."""

import py_uxlc.my_uxlc_book_abbreviations as u_bk_abbr
from wlc_cmn.wlc_book_codes import bk39id_to_wlc_bb
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id


def make_wbs_from_std_bcv_triple(std_bcv_triple):
    std_bkid = std_bcv_triple[0]
    wlc_bkid = bk39id_to_wlc_bb(std_bkid)
    chnu, vrnu = std_bcv_triple[1], std_bcv_triple[2]
    return f"{wlc_bkid}{chnu}:{vrnu}"


def get_std_bcv_triple(wlc_bcv_str):
    """
    Return a bcv triple like ('Genesis', 1, 1) for a WLC bcv string like 'gn1:1'.
    The returned book ID is a standard book ID.
    (bcv: book, chapter, & verse).
    """
    std_bkid = _get_std_bkid(wlc_bcv_str)
    cv_pair = get_cv_pair(wlc_bcv_str)
    return std_bkid, *cv_pair


def get_uxlc_bkid(wlc_bcv_str):
    """Return UXLC book ID for WLC bcv string (bcv: book, chapter, & verse)"""
    wlc_bkid = wlc_bcv_str[:2]
    std_bkid = wlc_bb_to_bk39id(wlc_bkid)
    uxlc_bkid = u_bk_abbr.BKNA_MAP_STD_TO_UXLC[std_bkid]
    return uxlc_bkid


def get_cv_pair(wlc_bcv_str):
    """Return chapter & verse integer pair for WLC bcv string (bcv: book, chapter, & verse)"""
    wlc_cv_str = _get_cv_str(wlc_bcv_str)
    c_str, v_str = wlc_cv_str.split(":")
    return int(c_str), int(v_str)


def get_tanach_dot_us_url(wlc_bcv_str):
    """Return tanach.us URL for WLC bcv string (bcv: book, chapter, & verse)"""
    uxlc_bkid = get_uxlc_bkid(wlc_bcv_str)
    wlc_cv_str = _get_cv_str(wlc_bcv_str)
    uxlc_bcv_str = uxlc_bkid + wlc_cv_str
    return f"https://tanach.us/Tanach.xml?{uxlc_bcv_str}"


def _get_std_bkid(wlc_bcv_str):
    """Return the standard book ID for WLC bcv string (bcv: book, chapter, & verse)"""
    wlc_bkid = wlc_bcv_str[:2]
    return wlc_bb_to_bk39id(wlc_bkid)


def _get_cv_str(wlc_bcv_str):
    wlc_cv_str = wlc_bcv_str[2:]
    return wlc_cv_str
