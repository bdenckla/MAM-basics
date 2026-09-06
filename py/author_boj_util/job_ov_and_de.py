"""Overview and details generation for quirkrecs."""

from boj_render import boj_html
from author_boj_util.is_lop import is_lop
from mb_cmn import my_utils
from mb_cmn.my_utils import intersperse, sl_map
from author_boj_util.common_titles_etc import d1d_detail_href
from author_boj_util import author
from author_boj_util.qr_relations import ACCENT_INFO
from author_boj_util.proposed import key_for_proposed
from author_boj_util.says import says
from author_boj_util.short_id_etc import short_id
from author_boj_util.job1_highlight import highlight, color
from author_boj_util.job1_lcloc import lcloc
from uxlc_misc import my_uxlc_location
from mb_cmn import bib_locales as bib_locales

__all__ = ["make_ov_and_de", "make_example_row", "row_id"]


def make_ov_and_de(quirkrecs):
    """Build overview-row and detail-HTML for every quirkrec.

    Args:
        quirkrecs: list of enriched quirkrec dicts.

    Returns:
        Dict mapping row IDs to {"od-overview": ..., "od-details": ...}
        sub-dicts.
    """
    ids = sl_map(row_id, quirkrecs)
    dups = _duplicates(ids)
    assert not dups, f"Duplicate row IDs found: {dups}"
    # No paths passed: uxlc_misc/uxlc_lci address their own inputs, and book-of-job's
    # private copies of both were proved equal to them before this call lost them --
    # all 39 UXLC XML one blob, and lci_recs.json differing in one header line whose
    # body unflatten_many never reads.  See boj_paths' module docstring.
    uxlc, pbi = my_uxlc_location.prep()
    ovdes = sl_map((_make_one_ov_and_de, uxlc, pbi), quirkrecs)
    return dict(zip(ids, ovdes))


def make_example_row():
    hlcp = color("proposed", "qr-lc-proposed")
    hcon = color("consensus", "qr-consensus")
    lcp_and_con = [hlcp, boj_html.line_break(), hcon]
    return boj_html.table_row(
        [
            boj_html.table_datum(lcp_and_con),
            boj_html.table_datum("# c:v"),
            boj_html.table_datum("how proposed differs from consensus"),
        ]
    )


def row_id(quirkrec):
    return f"row-{short_id(quirkrec)}"


def _duplicates(seq):
    seen = set()
    dups = set()
    for item in seq:
        if item in seen:
            dups.add(item)
        else:
            seen.add(item)
    return dups


def _make_one_ov_and_de(uxlc, pbi, quirkrec):
    std_bcvp_quad = _std_bcvp_quad(quirkrec)
    pg_dict = my_uxlc_location.page_and_guesses(uxlc, pbi, std_bcvp_quad)
    pg_diff = _pg_diff(pg_dict, quirkrec["qr-lc-loc"])
    if pg_diff is not None:
        ri = row_id(quirkrec)
        print(ri, pg_diff)
        print(ri, pg_dict)
        print(ri, quirkrec["qr-lc-loc"])
    return {
        "od-overview": _make_overview_row(quirkrec),
        "od-details": _make_details_html(quirkrec, "../jobn/img"),
        "od-quirkrec": quirkrec,
    }


def _pg_diff(pg_dict, lc_loc):
    if pg_dict["page"] != lc_loc["page"]:
        return f"Page mismatch: pg_dict page {pg_dict['page']} vs lc_loc page {lc_loc['page']}"
    lcl = lc_loc["line"]
    if lcl < 1:
        assert lcl != 0
        pline = 27 + (lcl + 1)
    else:
        pline = lcl
    fline = pline + 27 * (lc_loc["column"] - 1)
    flg = float(pg_dict["fline-guess"])
    balm = 2  # biggest acceptable line mismatch
    if abs(flg - fline) > balm:
        return (
            "fline mismatch: pg_dict fline-guess"
            + f" {pg_dict['fline-guess']} vs lc_loc fline {fline}"
        )
    return None


def _std_bcvp_quad(quirkrec):
    cn_colon_vn = quirkrec["qr-cv"]
    upwv = quirkrec.get("qr-uxlc-position-within-verse")
    pwv = upwv or 1  # use the position within verse if available, else 1
    bkid = bib_locales.BK_JOB
    chnu_str, vrnu_str = cn_colon_vn.split(":")
    chnu = int(chnu_str)
    vrnu = int(vrnu_str)
    atnu = pwv  # atom number within verse
    return bkid, chnu, vrnu, atnu


_KEY_FOR_QUESTION_MARK = {
    "qr-lc-proposed": "qr-lc-q",
    "qr-ac-proposed": "qr-ac-q",
}


def _key_for_question_mark(quirkrec):
    return _KEY_FOR_QUESTION_MARK[key_for_proposed(quirkrec)]


def _lcp_and_con(quirkrec):
    hl_pro = highlight(quirkrec, key_for_proposed(quirkrec))
    hl_con = highlight(quirkrec, "qr-consensus")
    if qm := quirkrec.get(_key_for_question_mark(quirkrec)):
        assert qm == "(?)"
        hl_pro_and_qm = [hl_pro, " (?)"]
    else:
        hl_pro_and_qm = [hl_pro]
    pro_lb_con = [*hl_pro_and_qm, boj_html.line_break(), hl_con]
    return pro_lb_con


def _make_overview_row(quirkrec, *, include_hash_link=True):
    hbo_rtl = {"lang": "hbo", "dir": "rtl"}
    nowrap = {"style": "text-wrap: nowrap"}
    td1_attrs = {**hbo_rtl, **nowrap, **_els(quirkrec)}
    the_row_id = row_id(quirkrec)
    sid = short_id(quirkrec)
    if include_hash_link:
        anc = boj_html.anchor_h("#", d1d_detail_href(sid))
        cv_contents = [anc, " ", quirkrec["qr-cv"]]
    else:
        cv_contents = quirkrec["qr-cv"]
    tr_contents = [
        boj_html.table_datum(_lcp_and_con(quirkrec), td1_attrs),
        boj_html.table_datum(cv_contents),
        author.table_datum(_what_is_weird(quirkrec)),
    ]
    tr_attrs = {"id": the_row_id}
    return boj_html.table_row(tr_contents, tr_attrs)


_IN_MY_YYY = {
    "qr-lc-proposed": "in μL",
    "qr-ac-proposed": author.span_color("in μA", "red"),
}


def _in_mu_yyy(quirkrec):
    return _IN_MY_YYY[key_for_proposed(quirkrec)]


def _maybe_maybe(quirkrec):
    qm_key = _key_for_question_mark(quirkrec)
    if qm_key in quirkrec:
        return [" maybe,"]
    return []


def _what_is_weird(quirkrec):
    in_my_yyy = _in_mu_yyy(quirkrec)
    wiw_in_mu_ell = [
        quirkrec["qr-what-is-weird"],
        *[" ", in_my_yyy, ","],
        _maybe_maybe(quirkrec),
    ]
    parts = [wiw_in_mu_ell, *says(quirkrec)]
    wiw_and_says = intersperse(boj_html.line_break(), parts)
    return wiw_and_says


def _els(quirkrec):
    if quirkrec.get("qr-extra-letter-spacing"):
        return {"class": "extra-letter-spacing"}
    return {}


def _img(img, img_prefix="img", scale=None):
    return author.para_for_img(img, "maxwidth50pc", img_prefix=img_prefix, scale=scale)


_MI_ARGS = {
    "mi-args-aleppo": [
        "μA (Aleppo)",
        "qr-ac-loc",
        "qr-aleppo-img",
    ],
    "mi-args-cam1753": [
        "μY (Cambridge 1753)",
        "qr-cam1753-loc",
        "qr-cam1753-img",
    ],
    "mi-args-jc": [
        "Jerusalem Crown",
        "qr-jc-img-intro",
        "qr-jc-img",
    ],
}


# Note: despite the parallel structure here, these location dicts have
# different origins. qr-ac-loc is hand-authored in each qr_*.py file;
# qr-cam1753-loc is computed during enrichment from cam1753-crops.json.
def _ac_loc_intro(ac_loc):
    """Format qr-ac-loc dict as a location string."""
    return (
        f"page {ac_loc['page']}, col {ac_loc['column']}, "
        f"line {ac_loc['line']}, word {ac_loc['word']}"
    )


def _cam1753_loc_intro(loc):
    """Format qr-cam1753-loc dict as a location string."""
    page = loc["page"].lstrip("0")
    text = f"page {page}, col {loc['column']}, " f"line {loc['line']}"
    if "line2" in loc:
        text += f" and line {loc['line2']}"
    if "word" in loc:
        text += f", word {loc['word']}"
    return text


def _maybe_one_img(quirkrec, mi_args_key, img_prefix="img"):
    ms_name, iikey, ipkey = _MI_ARGS[mi_args_key]
    maybe_img_path = quirkrec.get(ipkey)
    if maybe_img_path is None:
        return []
    maybe_img_intro = quirkrec.get(iikey)
    if iikey == "qr-ac-loc" and maybe_img_intro is not None:
        maybe_img_intro = _ac_loc_intro(maybe_img_intro)
    elif iikey == "qr-cam1753-loc" and maybe_img_intro is not None:
        maybe_img_intro = _cam1753_loc_intro(maybe_img_intro)
    if maybe_img_intro:
        intro = [" (", maybe_img_intro, ")"]
    else:
        intro = []
    cpara = [ms_name, *intro, ":"]
    return [author.para(cpara), _img(maybe_img_path, img_prefix)]


def _maybe_imgs(quirkrec, img_prefix="img"):
    result = []
    for mi_args_key in _MI_ARGS:
        result.extend(_maybe_one_img(quirkrec, mi_args_key, img_prefix))
    return result


def _maybe_bhq(bhq):
    if bhq is None:
        return []
    cont_p = ["$BHQ: ", author.hbo(bhq)]
    return [author.para_cc(cont_p)]


_SEP = " \N{EM DASH} "


def _maybe_inline(yyycom):
    return [] if yyycom is None else [yyycom]


def _maybe_para(yyycom):
    return [] if yyycom is None else [_ensure_lop(yyycom)]


def _ensure_lop(yyycom):
    """lop: list of paras"""
    return yyycom if is_lop(yyycom) else [author.para(yyycom)]


def _ancs(quirkrec):
    cv = quirkrec["qr-cv"]
    uxlc_href = f"https://tanach.us/Tanach.xml?Job{cv}"
    uxlc_anc = boj_html.anchor_h("U", uxlc_href)
    cn_v_vn = "c" + cv.replace(":", "v")
    mwd_href = (
        f"https://bdenckla.github.io/MAM-basics/MAM-with-doc/D3-Job.html#{cn_v_vn}"
    )
    mwd_anc = boj_html.anchor_h("M", mwd_href)
    return uxlc_anc, mwd_anc


def _dpe(quirkrec):
    fn = _dpe_stretched if _use_stretched_format(quirkrec) else _dpe_inline
    return fn(quirkrec)


def _use_stretched_format(quirkrec):
    gencom = quirkrec.get("qr-generic-comment")
    bhqcom = quirkrec.get("qr-bhq-comment")
    return is_lop(gencom) or is_lop(bhqcom)


def _dpe_inline(quirkrec):
    dpe1 = [
        *_maybe_inline(quirkrec.get("qr-generic-comment")),
        *_maybe_inline(quirkrec.get("qr-bhq-comment")),
        *_non_comment_dpe_parts(quirkrec),
    ]
    return _parasperse(dpe1)


def _dpe_stretched(quirkrec):
    return [
        *_maybe_para(quirkrec.get("qr-generic-comment")),
        *_maybe_para(quirkrec.get("qr-bhq-comment")),
        _parasperse(_non_comment_dpe_parts(quirkrec)),
    ]


def _parasperse(items):
    return author.para(my_utils.intersperse(_SEP, items))


def _non_comment_dpe_parts(quirkrec):
    uxlc_anc, mwd_anc = _ancs(quirkrec)
    return [
        *_maybe_g3yh_dontcare_message(quirkrec),
        uxlc_anc,
        mwd_anc,
        lcloc(quirkrec.get("qr-lc-loc")),
    ]


def _maybe_g3yh_dontcare_message(quirkrec):
    for ig_key in ("qr-ignore-g3yh-diff", "qr-ignore-g3yh-diff-in-consensus"):
        if quirkrec.get(ig_key):
            return ["The געיה difference is not important to us here."]
    return []


def _make_details_html(quirkrec, img_prefix="img"):
    lc_scale = quirkrec.get("qr-lc-img-scale")
    return [
        author.table_c(_make_overview_row(quirkrec, include_hash_link=False)),
        *_maybe_bhq(quirkrec.get("qr-bhq")),
        _dpe(quirkrec),
        *_maybe_rel_paras(quirkrec),
        _img(quirkrec["qr-lc-img"], img_prefix, scale=lc_scale),
        *_maybe_imgs(quirkrec, img_prefix),
    ]


def _maybe_rel_paras(quirkrec):
    """Render each qr-rel edge as its own dedicated paragraph.

    This is the cross-record accent relationship (e.g. a relocated אתנח), kept
    visually distinct from any same-word mention in the generic comment.
    """
    return [author.para(_rel_line(edge)) for edge in quirkrec.get("qr-rel", [])]


def _rel_line(edge):
    assert edge["kind"] == "move", f"Unsupported qr-rel kind: {edge['kind']}"
    accent_he = ACCENT_INFO[edge["accent"]]["he"]
    other = _rel_other_link(edge)
    if edge["role"] == "from":
        return [
            "In the consensus reading, this ",
            accent_he,
            " is relocated to ",
            other,
            ".",
        ]
    assert edge["role"] == "to", f"Unsupported qr-rel role: {edge['role']}"
    return [
        "This ",
        accent_he,
        " belongs here only in the consensus reading;",
        " in μL it is on ",
        other,
        " instead.",
    ]


def _rel_other_link(edge):
    """A link to the sibling record's detail page, labeled by its bare word."""
    word = boj_html.span_c(edge["other-word"], "unpointed-tanakh")
    return boj_html.anchor_h(word, d1d_detail_href(edge["other"]))
