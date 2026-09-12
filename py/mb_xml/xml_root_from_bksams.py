"""Exports root"""

import xml.etree.ElementTree as ET
from mb_cmn import bib_locales as tbn
from mb_misc import mb_html
from py_misc import get_cvm_rec_from_bcvt as gcrfb
from py_misc import vtrad_helpers
from mb_misc import osis_book_abbrevs as osisba
from mb_xml import xml_distribute_sampe as xml_sampe


def root(bksams, vtrads, variant):
    """Get XML root element from bksams (mix of books & sampes).

    ``vtrads`` is the comma-separated set of versification traditions whose cv-labels
    this book group's file carries, which for a vtmam file is more than one wherever the
    other traditions agree with MAM.  See main_mam_simple._vtrads_served.
    """
    the_root = ET.Element("book24")
    _add_subelements(the_root, bksams, variant)
    the_root.set("versification-tradition", vtrads)
    return the_root


def _add_subelements(the_root, bksams, variant):
    for bksam_type, bksam_body in bksams:
        if bksam_type == "bksam_bk":
            chasams = bksam_body
            versams = xml_sampe.chasam_body(chasams[0])
            bcvt = xml_sampe.versam_bcvt(versams[0])
            bkid = tbn.bcvt_get_bk39id(bcvt)
            osis_bkid = osisba.BOOK_ABBREVS[bkid]
            book_et_el = _sub_el(the_root, "book39", osis_bkid)
            _add_subelements2(book_et_el, bksam_body, variant)
        else:
            assert bksam_type == "bksam_sam"
            _sub_el_fun_versam_sam(the_root, xml_sampe.chasam_body(bksam_body), variant)


def _add_subelements2(the_root, chasams, variant):
    for chasam_type, the_chasam_body in chasams:
        if chasam_type == "chasam_cha":
            versams = the_chasam_body
            bcvt = xml_sampe.versam_bcvt(versams[0])
            bkid = tbn.bcvt_get_bk39id(bcvt)
            chnu = tbn.bcvt_get_chnu(bcvt)
            osis_bkid = osisba.BOOK_ABBREVS[bkid]
            chap_et_el = _sub_el(the_root, "chapter", osis_bkid, chnu)
            for versam in the_chasam_body:
                sub_el_fn = _sub_el_fun(xml_sampe.versam_type(versam))
                sub_el_fn(chap_et_el, versam, variant)
        else:
            assert chasam_type == "chasam_sam"
            _sub_el_fun_versam_sam(the_root, the_chasam_body, variant)


def _sub_el_fun(in_versam_type):
    sub_el_fns = {
        "versam_ver": _sub_el_fun_versam_ver,
        "versam_sam": _sub_el_fun_versam_sam,
    }
    return sub_el_fns[in_versam_type]


def _sub_el_fun_versam_ver(chap_et_el, versam_ver, variant):
    bcvt = xml_sampe.versam_bcvt(versam_ver)
    html_els, versam_attr, _alt, cvm_rec = xml_sampe.versam_body(versam_ver)
    id_attr = _id_attr(bcvt, variant)
    cvm_attr = _cvm_attr(bcvt, cvm_rec)
    attr = {**id_attr, **versam_attr, **cvm_attr}
    verse_html_el = mb_html.htel_mk("verse", attr, html_els)
    mb_html.add_htel_to_etxml(chap_et_el, verse_html_el)


def _id_attr(bcvt, _variant):
    # A "yeivinID" attribute sat beside this one, on every verse of the vtmam
    # variant alone, until 2026-09-12.  It was Yeivin's spelling of the very same
    # chapter and verse -- "Rut 1:1" beside osisID "Ruth.1.1" -- differing from the
    # osisID in the book abbreviation and the separators and in nothing else, as
    # all 23,202 of them were checked to be that day.  Ben had it written so that he
    # could search the corpus for references in the form his Yeivin ITM adaptation
    # uses, and retired it on the grounds that he has no plans to resume that work
    # and that an agent doing it would convert reference styles itself.  The book
    # map remains at py/py_misc/yeivin_book_abbrevs.py, so the attribute can be
    # recomputed from the osisID; nothing in this repository ever read it.
    return {"osisID": _osis_id_from_bcvt(bcvt)}


def _cvm_attr(bcvt, cvm_rec):
    if cvm_rec is None:
        return {}
    cvve_type, cvm = gcrfb.cvm_rec_get_parts(cvm_rec)
    if cvve_type == vtrad_helpers.CVVE_TYPE_NO_CONTENTS:
        return {"contents-corresponds-to": "no verse in MAM"}
    if cvve_type == vtrad_helpers.CVVE_TYPE_PARTIAL_CONTENTS:
        return {
            "contents-corresponds-to": "less than a full verse in MAM",
            "osisID-of-MAM-src": _osis_id_from_cvm(bcvt, cvm),
        }
    assert cvve_type == vtrad_helpers.CVVE_TYPE_SAME_CONTENTS
    return {
        "contents-corresponds-to": "a full verse in MAM",
        "osisID-of-MAM-src": _osis_id_from_cvm(bcvt, cvm),
    }


def _osis_id_from_bcvt(bcvt):
    bkid, chnu, vrnu = tbn.bcvt_get_bcv_triple(bcvt)
    osis_bkid = osisba.BOOK_ABBREVS[bkid]
    return _osis_id(osis_bkid, chnu, vrnu)


def _osis_id_from_cvm(bcvt, cvm):
    bkid = tbn.bcvt_get_bk39id(bcvt)
    return _osis_id_from_bcvt(tbn.mk_bcvt(bkid, cvm))


def _sub_el_fun_versam_sam(et_el, versam_sam, _variant):
    html_el_for_sampe_mid = xml_sampe.versam_body(versam_sam)
    mb_html.add_htel_to_etxml(et_el, html_el_for_sampe_mid)


def _sub_el(parent, tag, osis_bkid, chnu=None, vrnu=None):
    sub_el = ET.SubElement(parent, tag)
    osis_id = _osis_id(osis_bkid, chnu, vrnu)
    sub_el.set("osisID", osis_id)
    return sub_el


def _osis_id(osis_bkid, chnu, vrnu):
    maybe_chnu_part = (str(chnu),) if chnu else tuple()
    maybe_vrnu_part = (str(vrnu),) if vrnu else tuple()
    osis_id_parts = osis_bkid, *maybe_chnu_part, *maybe_vrnu_part
    osis_id = ".".join(osis_id_parts)
    return osis_id
