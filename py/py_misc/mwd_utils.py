"""Exports helpers for "MAM with doc" """

from dataclasses import dataclass
import enum
import re

from pycmn import hebrew_verse_numerals as hvn
from pyrender import render_element as renel
from py_misc import verse_and_friends as vaf
from pycmn import bib_locales as tbn
from py_misc import ren_html_for_renel as hfr
from py_misc import my_html
from pycmn import shrink
from pycmn import my_utils


@dataclass
class VerseNdd:
    """Holds a cvt, a nondoc veraf & a doc veraf."""

    bcvt: tuple
    nondoc_veraf: vaf.VerseAndFriends
    doc_veraf: vaf.VerseAndFriends


def mk_table(rows):
    """Make a 3-column table for cv, verse, & doc."""
    style_statements = (
        # 'max-width: 40em',
        "table-layout: fixed",
        "text-align: justify",
    )
    attr = {
        "class": "border-collapse",
        "style": "; ".join(style_statements),
        "lang": "hbo",
        "dir": "rtl",
    }
    cols = (
        my_html.col({"span": "1", "style": "width: 8%;"}),
        my_html.col({"span": "1", "style": "width: 46%;"}),
        my_html.col({"span": "1", "style": "width: 46%;"}),
    )
    colgroup = my_html.colgroup(cols)
    return my_html.table((colgroup, *rows), attr)


def mk_chapter_heading_level_2(chnu):
    """Make a heading of level 2 containing the Hebrew chapter number."""
    he_ch_str = hvn.INT_TO_STR_DIC[chnu]
    return my_html.heading_level_2("פרק " + he_ch_str, _h2_attr)


_h2_style_statements = (
    "position: sticky",
    "top: 0",
    "text-align: left",
)
_h2_attr = {
    "class": "border-collapse",
    "style": "; ".join(_h2_style_statements),
    "lang": "hbo",
    "dir": "rtl",
}


def mgketer_dot_org(bk39id, chnu):
    """Make a paragraph containing an mgketer.org anchor."""
    bknu = tbn.get_bknu(bk39id)
    href = f"https://www.mgketer.org/mikra/{bknu}/{chnu}/1/mg/106"
    attr = {"href": href, "target": "_blank"}
    anchor = my_html.anchor(f"mgketer.org {bknu} {chnu}", attr)
    return my_html.para(anchor)


@dataclass
class HtmlForVerse:
    """Holds a main HTML row, and maybe a "big doc" HTML div."""

    rows_for_main_page: dict
    div_for_bido_page: dict = None  # bido: big doc


@dataclass
class _DocCtx:
    bkid: str
    hfr_ctx: hfr.HfrCtx
    ver_ndd: VerseNdd


class _DocType(enum.Enum):
    """Types of documentation for a verse."""

    SELF_CONTAINED = enum.auto()
    A_T_BIDO = enum.auto()
    BIDO = enum.auto()


def html_for_ver_ndd(bkid, hfr_ctx: hfr.HfrCtx, ver_ndd: VerseNdd) -> HtmlForVerse:
    """Return an HtmlForVerse."""
    doc_ctx = _DocCtx(bkid, hfr_ctx, ver_ndd)
    bcvt = ver_ndd.bcvt
    html_for_nondoc = _html_for_nondoc(hfr_ctx, ver_ndd)
    length_of_docs = _length_of_docs_in_doc_veraf(ver_ndd.doc_veraf)
    if not length_of_docs > 400:
        html_for_docs = _html_for_docs(doc_ctx, _DocType.SELF_CONTAINED)
        rows_sc = _rows_for_main_page(bcvt, html_for_nondoc, html_for_docs)
        return HtmlForVerse(rows_sc)  # sc: self-contained (no atb)
    # atb: anchor [with link] to bido
    htd_atb = _html_for_docs(doc_ctx, _DocType.A_T_BIDO)
    htd_bido = _html_for_docs(doc_ctx, _DocType.BIDO)
    rows_atb = _rows_for_main_page(bcvt, html_for_nondoc, htd_atb)
    div_for_bido = _div_for_bido_page(bcvt, html_for_nondoc, htd_bido)
    return HtmlForVerse(rows_atb, div_for_bido)


def _rows_for_main_page(
    bcvt, html_for_nondoc: vaf.VerseAndFriends, html_for_docs: vaf.VerseAndFriends
):
    rows = [_row_for_verse(bcvt, html_for_nondoc.verse, html_for_docs.verse)]
    if html_for_nondoc.vaf_next_cp:
        rows.append(
            _row_for_next_cp(html_for_nondoc.vaf_next_cp, html_for_docs.vaf_next_cp)
        )
    if html_for_nondoc.good_ending:
        rows.append(
            _row_for_good_ending(html_for_nondoc.good_ending, html_for_docs.good_ending)
        )
    return rows


def _div_for_bido_page(
    bcvt, html_for_nondoc: vaf.VerseAndFriends, html_for_docs: vaf.VerseAndFriends
):
    """Make a div for cv & doc notes."""
    div_attr = {"style": "max-width: 40em", "lang": "hbo", "dir": "rtl"}
    cv_str = _hebrew_cv_str_verbose(bcvt)
    div_contents_1 = [my_html.para(cv_str), my_html.para(html_for_nondoc.verse)]
    div_contents_2 = []
    if html_for_docs.verse:
        div_contents_2.append(my_html.para(html_for_docs.verse))
    if html_for_docs.vaf_next_cp:
        div_contents_1.append(my_html.para(html_for_nondoc.vaf_next_cp))
        div_contents_2.append(my_html.para(html_for_docs.vaf_next_cp))
    if html_for_docs.good_ending:
        div_contents_1.append(my_html.para(html_for_nondoc.good_ending))
        div_contents_2.append(my_html.para(html_for_docs.good_ending))
    div_contents = div_contents_1 + div_contents_2
    return my_html.div(div_contents, div_attr)


def _row_for_verse(bcvt, html_for_verse, html_for_docs):
    cv_attr = {
        "id": mk_chapnver_id_from_bcvt(bcvt),
        "title": _hebrew_cv_str_verbose_and_wa(bcvt),
        "class": "top-n-bot-bordered end-aligned",
    }
    docs_attr = {"class": "top-n-bot-bordered"} if html_for_docs else {}
    return my_html.table_row(
        (
            my_html.table_datum(_hebrew_c_or_v_str(bcvt), cv_attr),
            my_html.table_datum(html_for_verse),
            my_html.table_datum(html_for_docs, docs_attr),
        )
    )


def _row_for_next_cp(html_for_next_cp, html_for_docs):
    attr_for_next_cp = {"class": "top-n-bot-bordered small"}
    docs_attr = {"class": "top-n-bot-bordered"} if html_for_docs else {}
    return my_html.table_row(
        (
            my_html.table_datum(html_for_next_cp, attr_for_next_cp),
            my_html.table_datum(tuple()),
            my_html.table_datum(html_for_docs, docs_attr),
        )
    )


def _row_for_good_ending(html_for_good_ending, html_for_docs):
    attr_for_cell_1 = {"class": "top-n-bot-bordered small"}
    docs_attr = {"class": "top-n-bot-bordered"} if html_for_docs else {}
    return my_html.table_row(
        (
            my_html.table_datum("סיום בטוב", attr_for_cell_1),
            my_html.table_datum(html_for_good_ending),
            my_html.table_datum(html_for_docs, docs_attr),
        )
    )


def mk_anchor_with_link_to_book(bkid):
    """Return the anchor for a book."""
    filename = filename_for_bkid(bkid)
    return my_html.anchor_h(bkid, filename)


def mk_anchor_with_link_to_chapter(chnu):
    """Return the anchor for a chapter."""
    cv_id = _mk_chapnver_id(chnu, 1)
    return my_html.anchor_h(str(chnu), "#" + cv_id)


def _mk_anchor_with_link_to_bido(bkid, cvt, doc_index):
    filename = filename_for_bkid_for_bido(bkid)
    doc_id = _mk_doc_id(cvt, doc_index)
    return my_html.anchor_h("...", filename + "#" + doc_id)


def filename_for_bkid(bkid):
    """Return filename for the main file for a book."""
    osdf = tbn.ordered_short_dash_full_39(bkid)
    return f"{osdf}.html"


def filename_for_bkid_for_bido(bkid):
    """Return filename for the "big doc" file for a book."""
    osdf = tbn.ordered_short_dash_full_39(bkid)
    return f"{osdf}-big-doc.html"


def _html_for_nondoc(hfr_ctx: hfr.HfrCtx, ver_ndd: VerseNdd):
    nondoc_veraf = ver_ndd.nondoc_veraf
    return nondoc_veraf.map_over((hfr.html_for_ren_el, hfr_ctx))


def _html_for_docs(doc_ctx: _DocCtx, doc_type):
    doc_veraf = doc_ctx.ver_ndd.doc_veraf
    return doc_veraf.map_over((_html_for_docs2, doc_ctx, doc_type))


def _html_for_docs2(doc_ctx: _DocCtx, doc_type, doc_renels):
    hfd = my_utils.st_map(
        (_html_for_single_doc_ren_el, doc_ctx, doc_type), enumerate(doc_renels)
    )
    line_break_seq = (my_html.line_break(),)
    return _shrink_join(line_break_seq, hfd)


def _mk_chapnver_id(chnu, vrnu):
    """Make a chapter & verse ID like c7v8"""
    return f"c{str(chnu)}v{str(vrnu)}"


def mk_chapnver_id_from_bcvt(bcvt):
    """Make a chapter & verse ID like c7v8"""
    return _mk_chapnver_id(*tbn.bcvt_get_chnu_vrnu(bcvt))


def _mk_doc_id(cvt, doc_index):
    """Make a doc ID like c7v8doc3"""
    return mk_chapnver_id_from_bcvt(cvt) + "doc" + str(1 + doc_index)


def _hebrew_c_or_v_str(bcvt):
    int_chnu, int_vrnu = tbn.bcvt_get_chnu_vrnu(bcvt)
    if int_vrnu == 1:
        # trailing colon allows chapter numbers to be distinguished from verse
        # numbers, for example in doing a search
        return hvn.INT_TO_STR_DIC[int_chnu] + ":"
    return hvn.INT_TO_STR_DIC[int_vrnu]


def _hebrew_cv_str_verbose(bcvt):
    int_chnu, int_vrnu = tbn.bcvt_get_chnu_vrnu(bcvt)
    ch_str = hvn.INT_TO_STR_DIC[int_chnu]
    vr_str = hvn.INT_TO_STR_DIC[int_vrnu]
    return "פרק " + ch_str + " פסוק " + vr_str


def _hebrew_cv_str_verbose_and_wa(bcvt):  # wa: Western Arabic
    int_chnu, int_vrnu = tbn.bcvt_get_chnu_vrnu(bcvt)
    ch_str, vr_str = map(str, (int_chnu, int_vrnu))
    hcsv = _hebrew_cv_str_verbose(bcvt)
    wac = f"{ch_str}:{vr_str}"  # Western Arabic concise
    wacp = f"({wac})"  # Western Arabic concise, [in] parens
    return hcsv + " " + wacp


def _html_for_single_doc_ren_el(doc_ctx: _DocCtx, doc_type, enum_pair):
    doc_index, doc = enum_pair
    lemma_ht = hfr.html_for_ren_el(doc_ctx.hfr_ctx, doc["doc_lemma"])
    lemma = my_html.span_c(lemma_ht, "mam-doc-lemma")
    if doc_type == _DocType.A_T_BIDO:
        anchor_to_bido = _mk_anchor_with_link_to_bido(
            doc_ctx.bkid, doc_ctx.ver_ndd.bcvt, doc_index
        )
        return lemma, " ", anchor_to_bido
    return _bido_or_self_contained(doc_ctx, doc_type, enum_pair, lemma)


def _bido_or_self_contained(doc_ctx: _DocCtx, doc_type, enum_pair, lemma):
    doc_index, doc = enum_pair
    part0_ht = hfr.html_for_ren_el(doc_ctx.hfr_ctx, doc["doc_parts"][0])
    part0_attr = {"class": "mam-doc-part-0"}
    if doc_type == _DocType.BIDO:
        part0_attr["id"] = _mk_doc_id(doc_ctx.ver_ndd.bcvt, doc_index)
    else:
        assert doc_type == _DocType.SELF_CONTAINED
    part0 = my_html.span(part0_ht, part0_attr)
    lemma_sp_part0 = lemma, " ", part0
    parts1c = my_utils.st_map(
        (hfr.html_for_ren_el, doc_ctx.hfr_ctx), doc["doc_parts"][1:]
    )
    if parts1c:
        uo_list = my_html.unordered_list(parts1c, {"class": "mam-doc-parts"})
        return *lemma_sp_part0, uo_list
    return lemma_sp_part0


def _length_of_docs_in_doc_veraf(doc_veraf: vaf.VerseAndFriends):
    return (
        _length_of_docs(doc_veraf.verse)
        + _length_of_docs(doc_veraf.vaf_next_cp)
        + _length_of_docs(doc_veraf.good_ending)
    )


def _length_of_docs(docs):
    return sum(map(_length_of_doc, docs), 0)


def _length_of_doc(doc_ren_el):
    return _length_of_renel(doc_ren_el["doc_lemma"]) + _length_of_renel(
        doc_ren_el["doc_parts"]
    )


_DOC_LENGTH = {
    "ren-tag-thin-space": 1,  # 0 would also be reasonable
    "ren-tag-no-break-space": 1,
    "mam-kq-k-velo-q-maq": 1,
}


def _length_of_renel(obj):
    if isinstance(obj, (tuple, list)):
        return sum(map(_length_of_renel, obj), 0)
    if renel.obj_is_ren_el(obj):
        if contents := renel.get_ren_el_contents(obj):
            return _length_of_renel(contents)
        return _DOC_LENGTH[renel.get_ren_el_tag(obj)]
    if isinstance(obj, str):
        patt_for_vowacc = r"[\u0590-\u05cf]*"  # vowel or accent
        stripped = re.sub(patt_for_vowacc, "", obj)
        return len(stripped)
    assert False, obj


def _shrink_join(joiner, tup):
    if not tup:
        return tup
    if len(tup) == 1:
        return tup[0]
    return shrink.shrink(tup[0] + joiner + _shrink_join(joiner, tup[1:]))
