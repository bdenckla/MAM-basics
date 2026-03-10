from dataclasses import dataclass

from pycmn import bib_locales as tbn
from pycmn import my_utils

from py_misc import my_html
from py_misc import my_utils_for_mainish as my_utils_fm
from py_misc import ren_tag_survey as rts
from py_misc import mwd_utils as mwdu
from py_misc import ren_html_for_renel as hfr
from py_misc import ren_html_from_ren_el_mapping as hfrm
from py_misc import mam_doc_utils as doc_utils
from pyrender import render_wikitext as rwt


@dataclass
class _ExtendedWriteCtx:
    bkid: str
    wc_for_main: my_html.WriteCtx
    wc_for_bido: my_html.WriteCtx
    hfr_ctx: hfr.HfrCtx
    para_for_chap_ancs: dict


def _pair_of_write_ctxs(ecb, out_paths):
    edition, css_hrefs, bkid = ecb
    path_for_main, path_for_bido = out_paths
    title_for_main = f"{edition}: {bkid}"
    title_for_bido = f"{title_for_main}: big docs"
    tp_for_main = title_for_main, path_for_main
    tp_for_bido = title_for_bido, path_for_bido
    wr_for_main = my_html.WriteCtx(*tp_for_main, css_hrefs=css_hrefs, add_wbr=True)
    wr_for_bido = my_html.WriteCtx(*tp_for_bido, css_hrefs=css_hrefs, add_wbr=True)
    return wr_for_main, wr_for_bido


def _para_for_chap_ancs(bkid, books_mpp):
    """Render chapter anchors (for MAM with doc)"""
    verses = books_mpp[bkid]["verses_plus"]
    bcvts = verses.keys()
    chnus_dic = {tbn.bcvt_get_chnu(bcvt): True for bcvt in bcvts}
    chnus = tuple(chnus_dic.keys())
    anchors = tuple(map(mwdu.mk_anchor_with_link_to_chapter, chnus))
    return my_html.para(my_utils.intersperse(" ", anchors))


def _extended_write_ctx(ecb, books_mpp, out_paths):
    bkid = ecb[2]
    powc = _pair_of_write_ctxs(ecb, out_paths)
    return _ExtendedWriteCtx(
        bkid,
        powc[0],
        powc[1],
        hfr.HfrCtx(hfrm.HT_TAC_FOR_RT_FOR_MAM_WITH_DOC),
        _para_for_chap_ancs(bkid, books_mpp),
    )


def _break_into_chapters(ver_ndds: list[mwdu.VerseNdd]):
    chapters = {}
    for ver_ndd in ver_ndds:
        chnu = tbn.bcvt_get_chnu(ver_ndd.bcvt)
        if chnu not in chapters:
            chapters[chnu] = []
        chapters[chnu].append(ver_ndd)
    return list(chapters.values())


def _html_for_chapter(bkid, hfr_ctx: hfr.HfrCtx, ver_ndds: list[mwdu.VerseNdd]):
    hfv_objs = my_utils.sl_map((mwdu.html_for_ver_ndd, bkid, hfr_ctx), ver_ndds)
    row_lists_for_main = [hfv.rows_for_main_page for hfv in hfv_objs]
    rows_for_main = my_utils.sum_of_seqs(row_lists_for_main)
    table_for_main = mwdu.mk_table(rows_for_main)
    chnu = tbn.bcvt_get_chnu(ver_ndds[0].bcvt)
    heading_level_2 = mwdu.mk_chapter_heading_level_2(chnu)
    para_for_mgketer = mwdu.mgketer_dot_org(bkid, chnu)
    div_for_main = my_html.div(
        (
            heading_level_2,
            table_for_main,
            para_for_mgketer,
        )
    )
    divs_for_bido = [hfv.div_for_bido_page for hfv in hfv_objs if hfv.div_for_bido_page]
    return {"div_for_main": div_for_main, "divs_for_bido": divs_for_bido}


def _html_for_book(wrae: _ExtendedWriteCtx, ver_ndds):
    chapters = _break_into_chapters(ver_ndds)
    survey = rts.make()
    hfr_ctx = hfr.HfrCtx(wrae.hfr_ctx.ht_tag_and_class_for_ren_tag, survey)
    divs_for_main = []
    divs_for_bido = []
    for chapter in chapters:
        chapter = _html_for_chapter(wrae.bkid, hfr_ctx, chapter)
        divs_for_main.append(chapter["div_for_main"])
        divs_for_bido.extend(chapter["divs_for_bido"])
    return {
        "survey": survey,
        "body_for_main": divs_for_main,
        "body_for_bido": divs_for_bido,
    }


def _write_three_col_html(wrae: _ExtendedWriteCtx, ver_ndds):
    """Write 3-column HTML main file and maybe a "big docs" file"""
    html_for_book = _html_for_book(wrae, ver_ndds)
    body_for_main = wrae.para_for_chap_ancs, *html_for_book["body_for_main"]
    my_html.write_html_to_file(body_for_main, wrae.wc_for_main)
    body_for_bido = html_for_book["body_for_bido"]
    if body_for_bido:
        my_html.write_html_to_file(body_for_bido, wrae.wc_for_bido)
    return html_for_book["survey"]


def write_book(ecb, books_mpp, out_paths):
    bkid = ecb[2]
    my_utils_fm.show_progress_g(__file__, "book", bkid)
    io_renlog = {}
    bcvt_to_veraf = rwt.render(bkid, books_mpp, _RENOPTS_MAM_WITH_DOC, io_renlog)
    bcvts = tuple(bcvt_to_veraf.keys())
    verafs = bcvt_to_veraf.values()
    nondoc = rwt.map_over_verafs(doc_utils.mark_doc_targets, verafs)
    doc = rwt.map_over_verafs(doc_utils.extract_docs, verafs)
    ver_ndd_part_triples = tuple(my_utils.szip(bcvts, nondoc, doc))
    ver_ndds = tuple(mwdu.VerseNdd(*triple) for triple in ver_ndd_part_triples)
    ewc = _extended_write_ctx(ecb, books_mpp, out_paths)
    survey = _write_three_col_html(ewc, ver_ndds)
    return survey


_RENOPTS_MAM_WITH_DOC = {
    "ro_no_slh_word": True,
    "ro_trivial_qere_to_doc": True,
    "ro_scrdfftar_to_doc": True,
}
