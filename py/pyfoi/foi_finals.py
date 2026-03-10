""" Exports write """

from pycmn import bib_locales as tbn
from pycmn import file_io

from py_misc import mwd_utils as mwdu
from py_misc import my_html
from py_misc import two_col_css_styles as tcstyles

from pyfoi import foiz_wt_pasoleg_1 as foi_pasoleg_1
from pyfoi import foi_struct as fct
from pyfoi import tsinnorit_explanations as tsinnorit_e
from pyfoi import ole_yored_explanations as ole_yored_e
from pyfoi import sec_yyy_explanations as sec_merk_e

# XXX TODO show a "table of contents"
# XXX TODO show friendlier descriptions of the FOIs
# XXX TODO show broader category counts, not just fine-grained
# XXX TODO show upper or lower (cantillation) where applicable
# XXX TODO show underlying Unicode where applicable (e.g. CGJ)


def write(args_foi, all_fois):
    """
    This is phase 2 of the foi (features of interest) process.
    It turns the all_fois structure into the final output files.
    """
    auto_outspecs = _auto_outspecs(all_fois)
    jacobson_outspec = "jacobson-pasoleg-1", foi_pasoleg_1.jacobson_features()
    all_outspecs = [*auto_outspecs, jacobson_outspec]
    tcstyles.make_css_file_for_mwd(f"{_OUT_DIR_PATH}/{_CSS_HREF}")
    if not args_foi:
        _write_index_dot_html(all_outspecs)
    for outspec in all_outspecs:
        _write_finals3(args_foi, all_fois, outspec)


_OUT_DIR_PATH = "../MAM-with-doc/docs/foi"
_CSS_HREF = "two_col_style.css"


def _slash_str_from_path_parts(path_parts):
    assert not any(("/" in x for x in path_parts))
    return "/".join(path_parts)


def _rm_html(contents):
    return "".join(map(_rm_html_single, contents))


def _rm_html_single(html_el):
    if isinstance(html_el, str):
        return html_el
    return _rm_html(html_el.get("contents", ""))


def _licont_for_outspec(outspec):
    outfile_stem, _foi_paths = outspec
    outfilename_for_html = _outfilename_for_html(outfile_stem)
    return my_html.anchor_h(outfile_stem, outfilename_for_html)


def _unordered_list_of_links_to_html(outspecs):
    liconts_for_outspecs = tuple(map(_licont_for_outspec, outspecs))
    return my_html.unordered_list(liconts_for_outspecs)


def _write_index_dot_html(outspecs):
    outspecs = sorted(outspecs)
    body_contents = _unordered_list_of_links_to_html(outspecs)
    write_ctx = my_html.WriteCtx(
        "MAM features of interest",
        f"{_OUT_DIR_PATH}/index.html",
        css_hrefs=(_CSS_HREF,),
    )
    my_html.write_html_to_file(body_contents, write_ctx)


def _write_finals3(args_foi, all_fois, outspec):
    outfile_stem, foi_paths = outspec
    outs = {"rowdics": [], "html_tables": {}}
    for foi_path in sorted(foi_paths):
        for foi_struct in all_fois[foi_path]:
            fpfs = foi_path, foi_struct
            _make_final_for_foi_struct(fpfs, outs)
    _write_json(args_foi, outfile_stem, outs["rowdics"])
    _write_html(args_foi, outfile_stem, outs["html_tables"])


def _make_final_for_foi_struct(fpfs, outs):
    foi_path, foi_struct = fpfs
    row_dic_for_json, row_dic_for_html = _get_rows(foi_path, foi_struct)
    outs["rowdics"].append(row_dic_for_json)
    _append_table_row(outs["html_tables"], foi_path, row_dic_for_html)


def _auto_outspecs(all_fois):
    dic = {}
    for foi_path in all_fois:
        outfile_stem = foi_path[0]
        if outfile_stem not in dic:
            dic[outfile_stem] = []
        dic[outfile_stem].append(foi_path)
    return list(map(tuple, dic.items()))


def _get_rows(foi_path, foi_struct):
    bcvt = fct.get_bcvt(foi_struct)
    bcv_short = tbn.short_bcv_of_bcvt(bcvt)
    bcv_anchor = my_html.anchor_h(bcv_short, _href_for_bcvt(bcvt))
    foi_target_type, foi_target = fct.get_target(foi_struct)
    qualifier = {}
    if foi_target_type == "foi-target-type-htseq":
        html_contents = foi_target
    elif foi_target_type == "foi-target-type-htseq-qual":
        html_contents = fct.qtar_proper(foi_target)
        qualifier = fct.qtar_qual(foi_target)
    else:
        assert False, foi_target_type
    row_dic_for_json = _row_dic_for_json(foi_path, bcv_short, qualifier, html_contents)
    row_dic_for_html = _row_dic_for_html(bcv_anchor, qualifier, html_contents)
    return row_dic_for_json, row_dic_for_html


def _href_for_bcvt(bcvt):
    bkid = tbn.bcvt_get_bk39id(bcvt)
    book_filename = mwdu.filename_for_bkid(bkid)
    chapnver_id = mwdu.mk_chapnver_id_from_bcvt(bcvt)
    href = f"../{book_filename}#{chapnver_id}"
    return href


def _row_dic_for_html(bcv_anchor, qualifier, html_contents):
    return {
        "bcv_anchor": [bcv_anchor],
        **qualifier,
        "html_contents": html_contents,
    }


def _row_dic_for_json(foi_path, bcv_short, qualifier, html_contents):
    return {
        "bcv_short": bcv_short,
        **qualifier,
        "fp": _slash_str_from_path_parts(foi_path[1:]),
        "r": _rm_html(html_contents),
    }


def _append_table_row(io_html_tables, foi_path, row_dic):
    table_row = _make_table_row(row_dic)
    tfp = tuple(foi_path)
    if tfp not in io_html_tables:
        io_html_tables[tfp] = []
    io_html_tables[tfp].append(table_row)


def _make_table_row(row_dic):
    td_attrs = {"lang": "hbo", "dir": "rtl"}
    # if ropts.get("bordered"):
    #     td_attrs["class"] = "bordered"
    hc_td = my_html.table_datum(row_dic["html_contents"], td_attrs)
    other_tds = tuple(_my_td(v) for k, v in row_dic.items() if k != "html_contents")
    return my_html.table_row((hc_td, *other_tds))


def _my_td(htseq_or_str_or_none):
    return my_html.table_datum(htseq_or_str_or_none)


def _write_json(args_foi, outfile_stem, rowdics):
    if not rowdics:
        assert args_foi
        return
    out_path = _out_path_for_json(outfile_stem)
    file_io.json_dump_to_file_path(rowdics, out_path)


def _out_path_for_html(outfile_stem):
    filename = _outfilename_for_html(outfile_stem)
    return f"{_OUT_DIR_PATH}/{filename}"


def _out_path_for_json(outfile_stem):
    filename = _outfilename_for_json(outfile_stem)
    return f"{_OUT_DIR_PATH}/{filename}"


def _outfilename_for_html(outfile_stem):
    return f"foi-{outfile_stem}.html"


def _outfilename_for_json(outfile_stem):
    return f"foi-{outfile_stem}.json"


def _write_html(args_foi, outfile_stem, html_tables):
    body1, body2 = _get_html_body1_and_2(outfile_stem, html_tables)
    if not body1:
        assert args_foi
        return
    body_contents = body1 + body2
    title = f"{outfile_stem} (MAM features of interest)"
    write_ctx = my_html.WriteCtx(
        title, _out_path_for_html(outfile_stem), css_hrefs=(_CSS_HREF,)
    )
    my_html.write_html_to_file(body_contents, write_ctx)


def _get_html_body1_and_2(outfile_stem, html_tables):
    body1 = []
    body2 = []
    for tfp, cases in html_tables.items():
        count1, head1, head2 = _section_heads(outfile_stem, tfp, len(cases))
        body1.extend(_html_for_section(head1, cases[:count1]))
        if head2:
            body2.extend(_html_for_section(head2, cases[count1:]))
    return body1, body2


def _html_for_section(head, trs):
    return head + [my_html.table(trs, {"class": "border-collapse"})]


def _section_head_parts_1b_and_2(outfile_stem, len_trs, rem_thresholds, tup2):
    if len_trs > rem_thresholds[2]:
        part2 = None
        outfilename_for_json = _outfilename_for_json(outfile_stem)
        part1b = [
            " No more are shown. See ",
            my_html.anchor_h("JSON output", outfilename_for_json),
            " for full list.",
        ]
    else:
        part2 = f"the remaining {tup2[0]} of {tup2[1]} are shown."
        part1b = [f" Further below, {part2}"]
    return part1b, part2


def _intro(tuple_foi_path, part_n, rest_idq=""):
    # idq: ID qualifier
    # sfp: string foi path (slash-separated)
    sfp = _slash_str_from_path_parts(tuple_foi_path[1:])
    the_id = _intro_id(sfp, rest_idq)
    contents = _intro_contents(sfp, part_n, the_id)
    return my_html.para(contents, {"id": the_id})


def _intro_id(sfp, rest_idq):
    d_sfp_q = f"-{sfp}" if sfp else ""  # d: dash; q: maybe
    out = "intro" + d_sfp_q + rest_idq
    return _escape_space(out)


def _escape_space(id_str):
    # (An HTML id must not contain any kind of ASCII whitespace.)
    g_space_g = "«space»"
    assert g_space_g not in id_str, id_str
    out = id_str.replace(" ", g_space_g)
    for char in out:
        assert not char.isspace(), out
    return out


def _intro_contents(sfp, part_n, the_id):
    anc = my_html.anchor_h("#", f"#{the_id}")  # self-anchor
    sfp_cs_q = f"{sfp}: " if sfp else ""  # cs: colon space; q: maybe
    return [anc, " ", f"{sfp_cs_q}Immediately below, ", *part_n]


def _head1b(tuple_foi_path):
    explanation_dic = _EXPLANATIONS.get(tuple_foi_path[0])
    if explanation_dic is None:
        return []
    explanation = explanation_dic.get(tuple_foi_path[1:])
    if explanation is None:
        # print(f"Warning: no explanation for {tuple_foi_path}")
        return []
    sfp = _slash_str_from_path_parts(tuple_foi_path[1:])
    full_exp = f"(The label «{sfp}» means {explanation}.)"
    return [my_html.para(full_exp)]


_EXPLANATIONS = {
    "tsinnorit": tsinnorit_e.EXPLANATIONS,
    "oleh-yored": ole_yored_e.EXPLANATIONS,
    "sec-merk": sec_merk_e.EXPLANATIONS,
}


def _section_heads(outfile_stem, tuple_foi_path, len_trs):
    rem_thresholds = 5, 20, 80
    if len_trs > rem_thresholds[1]:
        count1 = rem_thresholds[0]
        tup1 = count1, len_trs
        tup2 = len_trs - count1, len_trs
        part1b, part2 = _section_head_parts_1b_and_2(
            outfile_stem, len_trs, rem_thresholds, tup2
        )
        the_1st = f"the first {tup1[0]} of {tup1[1]} are shown."
        part1 = [the_1st, *part1b]
    else:
        count1 = len_trs
        part1 = [f"all {len_trs} are shown."]
        part2 = None
    head1a = [_intro(tuple_foi_path, part1)]
    head1b = _head1b(tuple_foi_path)
    head2 = [_intro(tuple_foi_path, part2, "-rest")] if part2 else None
    return count1, head1a + head1b, head2
