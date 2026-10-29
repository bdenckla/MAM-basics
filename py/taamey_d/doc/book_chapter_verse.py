from taamey_d.doc.html_helpers import to_str, xanchor2, sup
from taamey_d.doc.book_properties import BOOK_PROPERTIES


def bcv_ref(book_code, chap_colon_ver, bcvi):
    single = book_code, chap_colon_ver
    return bcv_ref_multi("", (single,), bcvi)


def bcv_ref_multi(join_str, multi, bcvi):
    multi_out = tuple(_bcv_ref_core(*m, bcvi) for m in multi)
    inside = join_str.join(multi_out)
    return "[" + inside + "]"


def bcv(book_code, chap_colon_ver):
    return _bcv_str_html(book_code, chap_colon_ver)


def cv_str_html(chap_colon_ver):
    if isinstance(chap_colon_ver, str):
        return chap_colon_ver
    ccv_mam = chap_colon_ver["MAM"]
    ccv_uxlc = chap_colon_ver["UXLC"]
    chap_mam, _ver_mam = ccv_mam.split(":")
    chap_uxlc, ver_uxlc = ccv_uxlc.split(":")
    if chap_mam == chap_uxlc:
        return divergent_versification(ccv_mam, ver_uxlc)
    return divergent_versification(ccv_mam, ccv_uxlc)


def divergent_versification(mam, uxlc):
    return str(mam) + sup("M") + str(uxlc) + sup("U")


def _bcv_ref_core(book_code, chap_colon_ver, bcvi):
    bcv_core_dict = _bcv_ref_core2(book_code, chap_colon_ver, bcvi)
    ref_num_str = str(bcv_core_dict["ref_num"])
    href = "#ref_" + ref_num_str  # e.g. #ref_17
    id = "callout_" + ref_num_str  # e.g. callout_17
    hover_str = _bcv_str_hover(book_code, chap_colon_ver)
    attrs = {"href": href, "id": id, "title": hover_str}
    return to_str(xanchor2(ref_num_str, attrs))


def _bcv_ref_core2(book_code, chap_colon_ver, bcvi):
    accum, sec_or_subsec = bcvi
    sec_title_abbrev = sec_or_subsec.get("sec_title_abbrev")
    subsec_title_abbrev = sec_or_subsec.get("subsec_title_abbrev") or ""
    accum_entry = dict(
        ref_num=1 + len(accum),
        book_code=book_code,
        chap_colon_ver=chap_colon_ver,
        sec_title_abbrev=sec_title_abbrev,
        subsec_title_abbrev=subsec_title_abbrev,
    )
    accum.append(accum_entry)
    ref_num = len(accum)
    return dict(ref_num=ref_num)


def _book_short2(book_code):
    short = BOOK_PROPERTIES[book_code][0]
    remaps = {"Psalms": "Psalm"}
    return remaps.get(short) or short


def _bcv_str_hover(book_code, chap_colon_ver):
    return _book_short2(book_code) + " " + _cv_str_hover(chap_colon_ver)


def _bcv_str_html(book_code, chap_colon_ver):
    return _book_short2(book_code) + " " + cv_str_html(chap_colon_ver)


def _cv_str_hover(chap_colon_ver):
    if isinstance(chap_colon_ver, str):
        return chap_colon_ver
    mamstr = chap_colon_ver["MAM"]
    uxlcstr = chap_colon_ver["UXLC"]
    mam_suffix = "\N{MODIFIER LETTER CAPITAL M}"
    uxlc_suffix = "\N{MODIFIER LETTER CAPITAL U}"
    return mamstr + mam_suffix + uxlcstr + uxlc_suffix
