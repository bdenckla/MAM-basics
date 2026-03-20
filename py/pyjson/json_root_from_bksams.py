"""Exports root"""

from pycmn import bib_locales as tbn
from py_misc import my_html
from py_misc import get_cvm_rec_from_bcvt as gcrfb
from py_misc import vtrad_helpers
from py_misc import osis_book_abbrevs as osisba
from py_misc import yeivin_book_abbrevs as yeivinba
from pyxml import xml_distribute_sampe as xml_sampe


def root(bksams, vtrad, variant):
    """Get JSON root dict from bksams (mix of books & sampes)."""
    contents = []
    _add_subelements(contents, bksams, variant)
    return {"versification-tradition": vtrad, "contents": contents}


def _add_subelements(contents, bksams, variant):
    for bksam_type, bksam_body in bksams:
        if bksam_type == "bksam_bk":
            chasams = bksam_body
            versams = xml_sampe.chasam_body(chasams[0])
            bcvt = xml_sampe.versam_bcvt(versams[0])
            bkid = tbn.bcvt_get_bk39id(bcvt)
            osis_bkid = osisba.BOOK_ABBREVS[bkid]
            book_contents = []
            _add_subelements2(book_contents, chasams, variant)
            contents.append(
                {"type": "book39", "osisID": osis_bkid, "contents": book_contents}
            )
        else:
            assert bksam_type == "bksam_sam"
            versam_sam = xml_sampe.chasam_body(bksam_body)
            contents.append(_versam_sam_to_json(xml_sampe.versam_body(versam_sam)))


def _add_subelements2(book_contents, chasams, variant):
    for chasam_type, the_chasam_body in chasams:
        if chasam_type == "chasam_cha":
            versams = the_chasam_body
            bcvt = xml_sampe.versam_bcvt(versams[0])
            bkid = tbn.bcvt_get_bk39id(bcvt)
            chnu = tbn.bcvt_get_chnu(bcvt)
            osis_bkid = osisba.BOOK_ABBREVS[bkid]
            osis_chid = _osis_id(osis_bkid, chnu)
            chapter_contents = []
            for versam in versams:
                if xml_sampe.versam_type(versam) == "versam_ver":
                    chapter_contents.append(_versam_ver_to_json(versam, variant))
                else:
                    assert xml_sampe.versam_type(versam) == "versam_sam"
                    chapter_contents.append(
                        _versam_sam_to_json(xml_sampe.versam_body(versam))
                    )
            book_contents.append(
                {"type": "chapter", "osisID": osis_chid, "contents": chapter_contents}
            )
        else:
            assert chasam_type == "chasam_sam"
            book_contents.append(
                _versam_sam_to_json(xml_sampe.versam_body(the_chasam_body))
            )


def _versam_ver_to_json(versam_ver, variant):
    bcvt = xml_sampe.versam_bcvt(versam_ver)
    html_els, versam_attr, _alt, cvm_rec = xml_sampe.versam_body(versam_ver)
    id_attr = _id_attr(bcvt, variant)
    cvm_attr = _cvm_attr(bcvt, cvm_rec)
    result = {**id_attr, **versam_attr, **cvm_attr}
    if html_els and len(html_els) == 1 and isinstance(html_els[0], str):
        result["text"] = html_els[0]
    elif html_els:
        result["contents"] = [_htel_to_json(el) for el in html_els]
    return result


def _versam_sam_to_json(html_el_for_sampe):
    tag = my_html.htel_get_tag(html_el_for_sampe)
    return {"type": tag}


def _htel_to_json(htel):
    if isinstance(htel, str):
        return {"type": "text", "text": htel}
    tag = my_html.htel_get_tag(htel)
    attr = htel.get("attr") or {}
    contents = htel.get("contents")
    result = {"type": tag, **attr}
    if contents is not None:
        if len(contents) == 1 and isinstance(contents[0], str):
            result["text"] = contents[0]
        else:
            result["contents"] = [_htel_to_json(c) for c in contents]
    return result


def _id_attr(bcvt, variant):
    out = {"osisID": _osis_id_from_bcvt(bcvt)}
    if alt_id := variant.get("variant-alt-id"):
        assert alt_id == "variant-alt-id-value-yeivin"
        out["yeivinID"] = _yeivin_id_from_bcvt(bcvt)
    return out


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


def _yeivin_id_from_bcvt(bcvt):
    bkid, chnu, vrnu = tbn.bcvt_get_bcv_triple(bcvt)
    yba = yeivinba.BOOK_ABBREV_FROM_BK39ID[bkid]
    return f"{yba} {str(chnu)}:{str(vrnu)}"


def _osis_id_from_cvm(bcvt, cvm):
    bkid = tbn.bcvt_get_bk39id(bcvt)
    return _osis_id_from_bcvt(tbn.mk_bcvt(bkid, cvm))


def _osis_id(osis_bkid, chnu=None, vrnu=None):
    maybe_chnu_part = (str(chnu),) if chnu else tuple()
    maybe_vrnu_part = (str(vrnu),) if vrnu else tuple()
    osis_id_parts = osis_bkid, *maybe_chnu_part, *maybe_vrnu_part
    return ".".join(osis_id_parts)
