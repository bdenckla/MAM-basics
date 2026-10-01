"""Render the selected adaptation and Ben's validated, data-backed footnotes."""

import py_html.legacy_html as aht_html
import mb_cmn.my_utils as my_utils
from mb_cmn.my_utils import append_at_key
from yeivin_itm import paths, claims, claim_schema, claim_text
from py_html import forbidden_phonetic_marks as fpmg
import yeivin_itm.content.my_yeivin_amisc_tocsec_metadata as tsm
import yeivin_itm.content.my_yeivin_amisc_traverse as tra
import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

import yeivin_itm.content.my_yeivin_tocsec_131_to_135 as tocsec_131
import yeivin_itm.content.my_yeivin_tocsec_192_to_206 as tocsec_192
import yeivin_itm.content.my_yeivin_tocsec_207_to_285 as tocsec_207
import yeivin_itm.content.my_yeivin_tocsec_307_to_310 as tocsec_307
import yeivin_itm.content.my_yeivin_tocsec_311_to_317 as tocsec_311
import yeivin_itm.content.my_yeivin_tocsec_318_to_344 as tocsec_318
import yeivin_itm.content.my_yeivin_tocsec_345_to_357 as tocsec_345
import yeivin_itm.content.my_yeivin_tocsec_358_to_374 as tocsec_358
import yeivin_itm.content.my_yeivin_tocsec_375_to_375 as tocsec_375
import yeivin_itm.content.my_yeivin_tocsec_376_to_393 as tocsec_376
import yeivin_itm.content.my_yeivin_tocsec_394_to_416 as tocsec_394

import yeivin_itm.content.my_yeivin_amisc_sec_320_footnotes as ftnts_320
import yeivin_itm.content.my_yeivin_amisc_sec_322_footnotes as ftnts_322
import yeivin_itm.content.my_yeivin_amisc_sec_385_footnotes as ftnts_385

# a tocsec contains 0 or more numsecs ("numsecs-before-titsecs") and then 0 or more titsecs
# a titsec contains 1 or more numsecs
#
# tocsec: TOC section, i.e. a section listed in the Table of Contents
# titsec: a titled section NOT listed in the Table of Contents (because it is too fine-grained)
# numsec: a numbered section


def page_texts(claim_data=None):
    """Return complete unwritten pages, using only the tracked approved claims."""
    claim_data = claims.read() if claim_data is None else claim_data
    claim_schema.validate(claim_data)
    tocsec_dic_1 = {
        "tocsec-id-131": tocsec_131.TOCSEC,
        "tocsec-id-192": tocsec_192.TOCSEC,
        "tocsec-id-207": tocsec_207.TOCSEC,
        "tocsec-id-307": tocsec_307.TOCSEC,
        "tocsec-id-311": tocsec_311.TOCSEC,
        "tocsec-id-318": tocsec_318.TOCSEC,
        "tocsec-id-345": tocsec_345.TOCSEC,
        "tocsec-id-358": tocsec_358.TOCSEC,
        "tocsec-id-375": tocsec_375.TOCSEC,
        "tocsec-id-376": tocsec_376.TOCSEC,
        "tocsec-id-394": tocsec_394.TOCSEC,
    }
    tocsec_dic_2 = _fill_in_ftnt_callouts(tocsec_dic_1)
    _check_secnums(tocsec_dic_2)
    pages = {}
    _render_pages(tocsec_dic_2, pages)
    resolved = {}
    for name, (contents, write_ctx) in pages.items():
        text = aht_html.html_text(_resolve_contents(contents, claim_data), write_ctx)
        fpmg.refuse_forbidden_phonetic_marks(text, name)
        resolved[name] = text
    return resolved


def _resolve_contents(contents, claim_data):
    """Resolve declared HTML text before the historical serializer wraps lines."""
    if isinstance(contents, str):
        return claim_text.resolve(contents, claim_data)
    if isinstance(contents, (list, tuple)):
        return [_resolve_contents(item, claim_data) for item in contents]
    if aht_html.is_htel(contents):
        if "contents" not in contents:
            return contents
        return aht_html.htel_set_contents(
            contents, _resolve_contents(contents["contents"], claim_data)
        )
    raise ValueError(f"Unknown Yeivin HTML content shape: {type(contents).__name__}")


def _fill_in_ftnt_callouts(ts_dic):
    new_values = list(map(_fifc_in_one_tocsec, ts_dic.values()))
    return dict(zip(ts_dic.keys(), new_values))


def _fifc_in_one_tocsec(tocsec):  # fifc: fill in ftnt callouts
    handlers = {
        "ptrav-handler-for-numsec-item": _fill_in_ftnt_callouts_in_one_numsec,
    }
    return tra.ptraverse_tocsec(handlers, tocsec)


def _fill_in_ftnt_callouts_in_one_numsec(numsec_item):
    secnum, sec_contents = numsec_item
    main_outs, ftnts = _deal_with_ftnts(secnum, sec_contents, 0)
    return [*main_outs, *hlp.make_html_for_ftnt_bodies(ftnts)]


def _deal_with_ftnts(secnum, htobj_seq, start_idx_for_ftnt_callouts):
    main_outs = []
    ftnts = []
    for htobj in htobj_seq:
        if aht_html.is_htel(htobj):
            if aht_html.htel_deref_tag(htobj) == "footnote":
                ftnt_idx = start_idx_for_ftnt_callouts + len(ftnts)
                ftnt_struct = hlp.make_ftnt_struct(secnum, ftnt_idx, htobj["contents"])
                new_htel = hlp.make_html_for_ftnt_callout(ftnt_struct)
                main_outs.append(new_htel)
                ftnts.append(ftnt_struct)
            elif contents := htobj.get("contents"):
                ftnt_idx = start_idx_for_ftnt_callouts + len(ftnts)
                main_outs_fth, ftnts_fth = _deal_with_ftnts(secnum, contents, ftnt_idx)
                # fth: For This Htobj
                new_htel = aht_html.htel_set_contents(htobj, main_outs_fth)
                main_outs.append(new_htel)
                ftnts.extend(ftnts_fth)
            else:
                main_outs.append(htobj)
        else:
            assert isinstance(htobj, str)
            main_outs.append(htobj)
    return main_outs, ftnts


def _render_pages(ts_dic, pages):
    anchor_dic = _render_html_files_for_tocsec(ts_dic, pages)
    _render_yeivin_top_page(anchor_dic, pages)
    _render_huge_ftnt_pages(pages)


def _render_huge_ftnt_pages(pages):
    _render_huge_ftnt_page(ftnts_320.HUGE_FTNT_REC_FOR_FEW_DOZEN, pages)
    _render_huge_ftnt_page(ftnts_322.HUGE_FTNT_REC_FOR_SLIGHTLY, pages)
    _render_huge_ftnt_page(ftnts_385.HUGE_FTNT_REC_FOR_THE_SIX, pages)
    _render_huge_ftnt_page(ftnts_385.HUGE_FTNT_REC_FOR_D1_RARELY, pages)
    _render_huge_ftnt_page(ftnts_385.HUGE_FTNT_REC_FOR_D1_OFTEN, pages)


def _render_html_files_for_tocsec(ts_dic, pages):
    bookpart_anchor_pairs = [
        _render_html_file_for_tocsec_1(item, pages) for item in ts_dic.items()
    ]
    bookpart_anchor_pairs = my_utils.sum_of_seqs(bookpart_anchor_pairs)
    anchor_dic = {}
    for bookpart, anchor in bookpart_anchor_pairs:
        append_at_key(anchor_dic, bookpart, anchor)
    return anchor_dic


def _render_html_file_for_tocsec_1(ts_dic_item, pages):
    tsid, tocsec = ts_dic_item
    anchor = _render_html_file_for_tocsec_2(tsid, tocsec, pages)
    if tocsec.get("tocsec-include-in-top-page"):
        bookpart = tocsec["tocsec-part"]
        return [(bookpart, anchor)]
    return []


def _check_secnums(ts_dic):
    refs_to_numsecs = []
    nums_of_numsecs = []
    for tsid, tocsec in ts_dic.items():
        nums_in_this_sec = tra.find_nums_of_numsecs(tocsec)
        assert tsm.all_in_range(tsid, nums_in_this_sec)
        nums_of_numsecs.extend(nums_in_this_sec)
        refs_to_numsecs.extend(tra.find_refs_to_numsecs(tocsec))
    refs_to_nowhere = set(refs_to_numsecs) - set(nums_of_numsecs)
    assert not refs_to_nowhere, refs_to_nowhere


def _render_html_file_for_tocsec_2(tsid, tocsec, pages):
    # tsid: TOC section ID, e.g. 'tocsec-id-318'
    # tocsec: TOC section title, heading, numsecs, & titsecs
    filename = tsm.filename_for_tsid(tsid)
    short_title = tocsec["tocsec-title"]
    bookpart = tocsec["tocsec-part"]
    full_title = f"{short_title} (a section in Yeivin ITM {bookpart})"
    anchor_contents = tocsec["tocsec-heading"]
    tocsec_html = tra.traverse_tocsec(_HANDLERS_FOR_MAKE_HTML, tocsec)
    contents = [_COPYRIGHT, _CAVEAT, *tocsec_html]
    path = paths.pages_dir() / filename
    write_ctx = aht_html.WriteCtx(full_title, path, path_to_style="./")
    # This generator is guarded like the two phonetic ones, and it is the one where the
    # guard could someday be wrong. Yeivin's book is about the masorah, so its adaptation
    # could legitimately come to want a masora circle as a masora circle, or an upper dot
    # as an extraordinary point, in a way Phonetic MAM's pages never can. The adaptation has zero
    # of either mark today, measured 2026-09-09, so nothing is being suppressed. IF THAT
    # CHANGES, NARROW THE GUARD HERE RATHER THAN DELETING IT: pass the common collector
    # a `forbidden` holding only the marks that remain forbidden, and the rest
    # of the site stays guarded as before.
    _collect_page(pages, filename, contents, write_ctx)
    return aht_html.anchor(anchor_contents, {"href": filename})


def _bookpart_list_item(anchor_dic_item):
    bookpart, anchors = anchor_dic_item
    return bookpart, aht_html.unordered_list(anchors)


def _render_yeivin_top_page(anchor_dic, pages):
    bookpart_list_items = map(_bookpart_list_item, anchor_dic.items())
    itm = aht_html.span_c(sub.ITM_TITLE, "book-title")
    h1_contents = "Excerpts from ", itm, " by Israel Yeivin"
    body_contents = [
        aht_html.heading_level_1(h1_contents),
        aht_html.unordered_list(bookpart_list_items),
        aht_html.para(
            aht_html.anchor("Font license and source", {"href": "woff2/SOURCE.txt"})
        ),
    ]
    title = "Excerpts from ITM by Yeivin"
    path = paths.pages_dir() / paths.LANDING_FILENAME
    write_ctx = aht_html.WriteCtx(title, path, path_to_style="./")
    _collect_page(pages, paths.LANDING_FILENAME, body_contents, write_ctx)


def _render_huge_ftnt_page(huge_ftnt_rec, pages):
    prwp = huge_ftnt_rec["huge-ftnt-rec-path-rel-web-publish-topdir"]
    titl = huge_ftnt_rec["huge-ftnt-rec-title"]
    h1co = huge_ftnt_rec["huge-ftnt-rec-h1-contents"]
    # h1co is like like title but can have formatting
    main = huge_ftnt_rec["huge-ftnt-rec-main"]
    body_contents = [aht_html.heading_level_1(h1co), main]
    path = paths.pages_dir() / prwp
    write_ctx = aht_html.WriteCtx(titl, path, path_to_style="./")
    _collect_page(pages, prwp, body_contents, write_ctx)


def _collect_page(pages, filename, body_contents, write_ctx):
    if filename in pages:
        raise ValueError(f"Duplicate Yeivin page: {filename}")
    pages[filename] = (body_contents, write_ctx)


_COPYRIGHT = aht_html.para(
    [
        "Adapted, by permission, from Israel Yeivin, ",
        aht_html.span_c(sub.ITM_TITLE, "book-title"),
        ", "
        "translated and edited by E. J. Revell."
        " "
        "Copyright © 1980 by the Society of Biblical Literature.",
    ]
)
_CAVEAT = aht_html.para(
    [
        "Note that this is a loose adaptation of the work of Yeivin and Revell:",
        " while some sections are faithfully rendered,",
        " I’ve taken great liberties with others. "
        #
        " I’ve tried to relegate actual ideas of my own to footnotes,"
        " but I may not have observed that discipline fully.",
    ]
)
_HANDLERS_FOR_MAKE_HTML = {
    "trav-handler-for-tocsec-heading": hlp.trvhnd_make_html_for_tose_h,
    "trav-handler-for-titsec-heading": hlp.trvhnd_make_html_for_tise_h,
    "trav-handler-for-numsec-item": hlp.trvhnd_make_html_for_nsi,
}
