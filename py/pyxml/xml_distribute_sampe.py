""" Exports
    distribute_sampe
    versam_type
    versam_bcvt
    versam_body
    chasam_body
"""

from py_misc import my_html
from py_misc import get_cvm_rec_from_bcvt as gcrfb
from py_misc import verse_and_friends as vaf
from pycmn import bib_locales as tbn
from pycmn import my_utils


def distribute_sampe(verses):
    """
    Distribute sampes liberally,
    i.e., put them in all places we think they might be convenient to have
    """
    versams = _make_versams(verses)
    books = _split_into_chaptered_books(versams)
    bksams = _make_bksams(books)
    return bksams


def versam_type(versam):
    """Get the type part of a versam"""
    return versam[0]


def versam_bcvt(versam):
    """Get the bcvt part of a versam"""
    return versam[1]


def versam_body(versam):
    """Get the body part of a versam"""
    return versam[2]


def chasam_body(chasam):
    """Get the body part of a chasam"""
    return chasam[1]


def _mk_versam_ver2(bcvt, html_els, attr):
    cvm_rec = gcrfb.get_cvm_rec_from_bcvt(bcvt)
    body = html_els, attr, None, cvm_rec
    return "versam_ver", bcvt, body


def _mk_versam_sam(bcvt, html_el_for_sampe):
    body = html_el_for_sampe
    return "versam_sam", bcvt, body


def _make_versams(verses):
    versams = []
    sampe = None
    for bcvt, veraf in verses:
        versam = _mk_versam_ver(bcvt, veraf, sampe)
        versams.append(versam)
        if sampe := _get_sampe_from_next_cp(veraf.vaf_next_cp):
            versam = _mk_versam_sam(bcvt, sampe)
            versams.append(versam)
    return versams


def _split_into_chaptered_books(versams):
    books = {}
    for versam in versams:
        bcvt = versam_bcvt(versam)
        bkid = tbn.bcvt_get_bk39id(bcvt)
        chnu = tbn.bcvt_get_chnu(bcvt)
        if bkid not in books:
            books[bkid] = {}
        if chnu not in books[bkid]:
            books[bkid][chnu] = []
        books[bkid][chnu].append(versam)
    return books


def _make_bksams(books):
    bksams = []
    for chapters in books.values():
        chasams = []
        for chapter in chapters.values():
            versams = chapter
            chasam_cha = "chasam_cha", versams
            chasams.append(chasam_cha)
            if _is_versam_sam(versams[-1]):
                versam_sam = versams.pop()
                chasam_sam = "chasam_sam", versam_sam
                chasams.append(chasam_sam)
        bksam_bk = "bksam_bk", chasams
        bksams.append(bksam_bk)
        if _is_chasam_sam(chasams[-1]):
            chasam_sam = chasams.pop()
            bksam_sam = "bksam_sam", chasam_sam
            bksams.append(bksam_sam)
    return bksams


def _mk_versam_ver(bcvt, veraf, last_sampe):
    new_html_els, trailing_sampe = _strip_trailing_sampe(veraf)
    attr = {}
    if last_sampe:
        attr["starts-with-sampe"] = _sampe_attr_val(last_sampe)
    if trailing_sampe:
        attr["ends-with-sampe"] = _sampe_attr_val(trailing_sampe)
    return _mk_versam_ver2(bcvt, new_html_els, attr)


def _strip_trailing_sampe(veraf: vaf.VerseAndFriends):
    if sampe := _get_sampe_from_next_cp(veraf.vaf_next_cp):
        verse_and_ge = veraf.verse + veraf.good_ending
        return verse_and_ge, sampe
    all_3 = veraf.verse + veraf.good_ending + veraf.vaf_next_cp
    return all_3, None


def _sampe_attr_val(sampe):
    htel_tag = my_html.htel_get_tag(sampe)
    return _SAMPE_MAP[htel_tag]


def _get_sampe_from_next_cp(vaf_next_cp):
    if not vaf_next_cp:
        return None
    fao = my_utils.first_and_only(vaf_next_cp)
    htel_tag = my_html.htel_get_tag(fao)
    return fao if htel_tag in _SAMPE_MAP else None


def _is_versam_sam(versam):
    return versam_type(versam) == "versam_sam"


def _is_chasam_sam(chasam):
    versam = chasam_body(chasam)
    return versam_type(versam) == "versam_sam"


_SAMPE_MAP = {
    "spi-samekh2": "samekh2",
    "spi-samekh3": "samekh3",
    "spi-pe2": "pe2",
    "spi-pe3": "pe3",
}
