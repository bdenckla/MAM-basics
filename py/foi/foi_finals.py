"""Exports write"""

from mb_cmn import bib_locales as tbn
from mb_cmn import file_io
from mb_cmn import paths
from mb_cmn import provenance

from py_misc import mwd_utils as mwdu
from mb_author import author
from mb_misc import mb_html

from foi import pasoleg_1_labels
from foi import foi_gray_marks as gray_marks
from foi import foi_struct as fct
from foi import tsinnorit_explanations as tsinnorit_e
from foi import ole_yored_explanations as ole_yored_e
from foi import sec_yyy_explanations as sec_merk_e
from foi import dml_an_explanations as dml_e
from foi import dexi_stress_meteg_explanations as dexi_stress_meteg_e
from foi import doc_note_notation_explanations as doc_note_notation_e
from foi import foiz_wt_holam_before_vav as holam_foi
from foi import holam_before_vav_explanations as holam_e
from foi import kq_simple_explanations as kq_simple_e
from foi import kq_complex_explanations as kq_complex_e
from foi import mtgmtg_explanations as mtgmtg_e
from foi import qamats_var_explanations as qamats_var_e
from foi import quick_brown_explanations as quick_brown_e
from foi import rare_tmpls_explanations as rare_tmpls_e
from foi import slh_word_explanations as slh_word_e
from foi import unicode_explanations as unicode_e

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
    provenance.write_directory_provenance(
        _OUT_DIR_PATH,
        __file__,
        "FOI JSON and HTML outputs. Structural inventories that opt into "
        "all_branch_foilers inspect every validated parameter of every recognized "
        "template. Other FOIs select or separately label the Scripture branches "
        "required by their own question.",
    )
    if not args_foi:
        _write_index_dot_html(auto_outspecs)
    for outspec in auto_outspecs:
        _write_finals3(args_foi, all_fois, outspec)


_OUT_DIR_PATH = str(paths.repo_root() / "gh-pages" / "MAM-with-doc" / "foi")
_CSS_HREF = "../two_col_style.css"


def _slash_str_from_path_parts(path_parts):
    assert not any(("/" in x for x in path_parts))
    return "/".join(path_parts)


def _rm_html(contents):
    return "".join(map(_rm_html_single, contents))


def _rm_html_single(html_el):
    if isinstance(html_el, str):
        return html_el
    if gray_marks.is_left_out_of_json_text(html_el):
        return ""
    return _rm_html(html_el.get("contents", ()))


def _licont_for_outspec(outspec):
    outfile_stem, _foi_paths = outspec
    outfilename_for_html = _outfilename_for_html(outfile_stem)
    return mb_html.anchor_h(outfile_stem, outfilename_for_html)


def _unordered_list_of_links_to_html(outspecs):
    liconts_for_outspecs = tuple(map(_licont_for_outspec, outspecs))
    return mb_html.unordered_list(liconts_for_outspecs)


def _write_index_dot_html(outspecs):
    outspecs = sorted(outspecs)
    body_contents = _foi_body_wrapper(_unordered_list_of_links_to_html(outspecs))
    write_ctx = mb_html.WriteCtx(
        "MAM features of interest",
        f"{_OUT_DIR_PATH}/index.html",
        css_hrefs=(_CSS_HREF,),
        html_comment=provenance.generated_html_comment(__file__),
    )
    mb_html.write_html_to_file(body_contents, write_ctx)


def _write_finals3(args_foi, all_fois, outspec):
    outfile_stem, foi_paths = outspec
    # A counted path's rows go to the page's introduction, which counts them and may
    # show some of them, rather than to a table.
    counted = _COUNTED_FOI_PATHS.get(outfile_stem, frozenset())
    census = {
        foi_path: [_get_rows(foi_path, fs)[1] for fs in all_fois[foi_path]]
        for foi_path in counted
    }
    listed = sorted(foi_path for foi_path in foi_paths if foi_path not in counted)
    # Every listed path gets a table, in sorted order, so that a declared category
    # with no rows keeps its section.
    html_tables = {tuple(foi_path): [] for foi_path in listed}
    outs = {"rowdics": [], "html_tables": html_tables}
    for foi_path in listed:
        cases = all_fois[foi_path]
        if foi_path in holam_foi.DIVINE_NAME_PATHS:
            cases = cases[:1]
        for foi_struct in cases:
            fpfs = foi_path, foi_struct
            _make_final_for_foi_struct(fpfs, outs)
    if outfile_stem == "mtgmtg":
        mtgmtg_e.validate_quoted_mam_atoms(outs["rowdics"])
    _write_json(outfile_stem, outs["rowdics"])
    overall_head = (
        holam_e.introduction(outs["rowdics"])
        if outfile_stem == holam_foi.STEM
        else _overall_head(outfile_stem, census)
    )
    _write_html(args_foi, outfile_stem, outs["html_tables"], overall_head)


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
    bcv_anchor = mb_html.anchor_h(bcv_short, _href_for_bcvt(bcvt))
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
    html_qualifier = {} if foi_path[0] == holam_foi.STEM else qualifier
    row_dic_for_html = _row_dic_for_html(bcv_anchor, html_qualifier, html_contents)
    return row_dic_for_json, row_dic_for_html


def _href_for_bcvt(bcvt):
    bkid = tbn.bcvt_get_bk39id(bcvt)
    book_href = mwdu.href_for_bkid(bkid)
    chapnver_id = mwdu.mk_chapnver_id_from_bcvt(bcvt)
    href = f"../{book_href}#{chapnver_id}"
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
        **{key: _json_value(value) for key, value in qualifier.items()},
        "fp": _slash_str_from_path_parts(foi_path[1:]),
        "r": _rm_html(html_contents),
        **gray_marks.json_flags(html_contents, *qualifier.values()),
    }


def _json_value(value):
    # A qualifier that shows a gray mark goes to the JSON without the gray marks that
    # the JSON leaves out: as its text if it holds only text and gray marks, like
    # foi-kq-simple's pqere, and otherwise as the HTML it is, like foi-slh-word's
    # html, which keeps its markup.
    if not gray_marks.labels(value):
        return value
    assert isinstance(value, (tuple, list)), value
    if all(isinstance(el, str) or gray_marks.is_gray_mark(el) for el in value):
        return _rm_html(value)
    return tuple(el for el in value if not gray_marks.is_left_out_of_json_text(el))


def _append_table_row(io_html_tables, foi_path, row_dic):
    # A row is its cells and the labels of the gray marks it shows, from which its
    # table's columns of gray marks are made.
    cells = _make_table_cells(foi_path, row_dic)
    labels = gray_marks.labels(*row_dic.values())
    tfp = tuple(foi_path)
    if tfp not in io_html_tables:
        io_html_tables[tfp] = []
    io_html_tables[tfp].append((cells, labels))


def _make_table_cells(foi_path, row_dic):
    if foi_path[0] == "dexi-stress-meteg":
        return tuple(dexi_stress_meteg_e.html_row_cells(row_dic))
    if foi_path[0] == "slh-word":
        target_tds = slh_word_e.html_target_cells(row_dic["html_contents"])
    elif foi_path[0] == holam_foi.STEM:
        target_tds = holam_e.html_target_cells(row_dic["html_contents"])
    else:
        target_tds = (_target_td(tuple(foi_path), row_dic["html_contents"]),)
    other_tds = tuple(_my_td(k, v) for k, v in row_dic.items() if k != "html_contents")
    return (*target_tds, *other_tds)


def _target_td(foi_path, html_contents):
    """Return the cell of a row's target, in the pointed-Hebrew font unless a label.

    lang="hbo" sets Taamey D at 140%, which is for pointed Hebrew: by the
    hebrew-prose skill's rule "Unpointed Hebrew keeps the surrounding font", a
    label, which names a template or the parameters around one, keeps the
    surrounding font. Any other target is MAM's text, lifted whole and shown with
    the other rows' forms, so it keeps their font even where it has no point or
    accent; a path whose targets may be wholly unpointed is declared in
    _LIFTED_UNPOINTED_PATHS, and any other unpointed target raises.
    """
    if foi_path in _LABEL_PATHS:
        assert author.is_unpointed_hebrew(html_contents), (foi_path, html_contents)
        return mb_html.table_datum(html_contents, {"dir": "rtl"})
    if author.is_unpointed_hebrew(html_contents):
        if foi_path not in _LIFTED_UNPOINTED_PATHS:
            raise ValueError(f"unpointed target in {foi_path}: {html_contents!r}")
    return mb_html.table_datum(html_contents, {"lang": "hbo", "dir": "rtl"})


# The paths whose targets are labels: the template stack around a dexi stress
# helper, or a template inside its arguments, as a tuple or a name, and the name
# of a column E divider template, whose letters are the divider's.
_LABEL_PATHS = frozenset(
    {
        ("poetic-stress-helpers", "dexi-with-tmpl-above"),
        ("poetic-stress-helpers", "dexi-with-tmpl-below"),
        ("rare-tmpls", "col-e-sampe"),
    }
)
# The paths whose lifted targets may have no point or accent: a ketiv velo qere,
# which has none in MAM, and which MAM-for-Sefaria's examples keep in the
# pointed-Hebrew font (Ben, 2026-10-26); and a scroll-difference note's
# arguments, whose target may be a parashah sign or __, the placeholder for none,
# beside a note with no pointing, which Ben kept in that font on 2026-11-09.
_LIFTED_UNPOINTED_PATHS = frozenset(
    {
        ("kq-simple", "x-velo-y-k-velo-q"),
        ("rare-tmpls", "na-note"),
    }
)


def _my_td(key, htseq_or_str_or_none):
    td_attrs = None
    if key == "pqere":
        # A pointed qere: pointed Hebrew, in the pointed-Hebrew font.
        assert not author.is_unpointed_hebrew(
            htseq_or_str_or_none
        ), htseq_or_str_or_none
        td_attrs = {"lang": "hbo", "dir": "rtl"}
    return mb_html.table_datum(htseq_or_str_or_none, td_attrs)


def _write_json(outfile_stem, rowdics):
    # Only a declared stem reaches here with no rows; its JSON is then [].
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


def _write_html(args_foi, outfile_stem, html_tables, overall_head):
    body1, body2 = _get_html_body1_and_2(outfile_stem, html_tables)
    if not body1:
        assert args_foi
        return
    body_contents = _foi_body_wrapper(overall_head + body1 + body2)
    script = _SCRIPTS.get(outfile_stem)
    if script is not None:  # After the tables, so that it finds their elements.
        body_contents.append(mb_html.script(script))
    title_stem = holam_e.TITLE if outfile_stem == holam_foi.STEM else outfile_stem
    title = f"{title_stem} (MAM features of interest)"
    write_ctx = mb_html.WriteCtx(
        title,
        _out_path_for_html(outfile_stem),
        head_style=holam_e.STYLE if outfile_stem == holam_foi.STEM else None,
        css_hrefs=(_CSS_HREF,),
        html_comment=provenance.generated_html_comment(__file__),
    )
    mb_html.write_html_to_file(body_contents, write_ctx)


def _foi_body_wrapper(contents):
    style = "max-width: 40rem; margin-left: auto; margin-right: auto"
    return [mb_html.div(contents, {"style": style})]


def _overall_head(outfile_stem, census):
    explanation = _OVERALL_EXPLANATIONS.get(outfile_stem)
    if explanation is None:
        return []
    if callable(explanation):  # It makes its HTML from the counted paths' rows.
        return list(explanation(census))
    if isinstance(explanation, str):
        return [mb_html.para(explanation)]
    return [mb_html.para(paragraph) for paragraph in explanation]


def _get_html_body1_and_2(outfile_stem, html_tables):
    body1 = []
    body2 = []
    for tfp, cases in html_tables.items():
        count1, head1, head2 = _section_heads(outfile_stem, tfp, len(cases))
        body1.extend(_html_for_section(head1, cases[:count1]))
        if head2:
            body2.extend(_html_for_section(head2, cases[count1:]))
    return body1, body2


def _html_for_section(head, rows):
    if not rows:  # A declared category with no rows has no table.
        return head
    # A table has a column for each kind of gray mark that one of its rows shows.
    table_labels = gray_marks.labels_of_table(labels for _cells, labels in rows)
    trs = [
        mb_html.table_row((*cells, *gray_marks.cells(labels, table_labels)))
        for cells, labels in rows
    ]
    return head + [mb_html.table(trs, {"class": "border-collapse"})]


def _section_head_parts_1b_and_2(
    outfile_stem, len_trs, rem_thresholds, tup2, tuple_foi_path
):
    if len_trs > rem_thresholds[2]:
        part2 = None
        outfilename_for_json = _outfilename_for_json(outfile_stem)
        part1b = [
            " No more are shown. See ",
            mb_html.anchor_h("JSON output", outfilename_for_json),
            " for full list.",
        ]
    else:
        part2 = f"the remaining {tup2[0]} of {tup2[1]} are shown."
        sfp = _slash_str_from_path_parts(tuple_foi_path[1:])
        rest_id = _intro_id(sfp, "-rest")
        further_below = mb_html.anchor_h("Further below", f"#{rest_id}")
        part1b = [" ", further_below, f", {part2}"]
    return part1b, part2


def _intro(tuple_foi_path, part_n, rest_idq=""):
    # idq: ID qualifier
    # sfp: string foi path (slash-separated)
    sfp = _slash_str_from_path_parts(tuple_foi_path[1:])
    the_id = _intro_id(sfp, rest_idq)
    contents = _intro_contents(sfp, part_n, the_id)
    return mb_html.para(contents, {"id": the_id})


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
    anc = mb_html.anchor_h("#", f"#{the_id}")  # self-anchor
    sfp_cs_q = f"{sfp}: " if sfp else ""  # cs: colon space; q: maybe
    if part_n is None:  # A declared category with no rows
        return [anc, " ", f"{sfp_cs_q}None are found."]
    return [anc, " ", f"{sfp_cs_q}Immediately below, ", *part_n]


def _head1b(tuple_foi_path):
    explanation = _explanation_for_foi_path(tuple_foi_path)
    if explanation is None:
        return []
    if isinstance(explanation, str):
        return [_label_explanation_para(tuple_foi_path, explanation)]
    assert isinstance(explanation, dict), explanation
    label = explanation.get("label")
    paras = []
    if label is not None:
        paras.append(_label_explanation_para(tuple_foi_path, label))
    paras.extend(mb_html.para(paragraph) for paragraph in explanation.get("paras", ()))
    return paras


def _explanation_for_foi_path(tuple_foi_path):
    explanation_source = _EXPLANATIONS.get(tuple_foi_path[0])
    if explanation_source is None:
        return None
    if callable(explanation_source):
        return explanation_source(tuple_foi_path[1:])
    return explanation_source.get(tuple_foi_path[1:])


def _label_explanation_para(tuple_foi_path, explanation):
    sfp = _slash_str_from_path_parts(tuple_foi_path[1:])
    if not sfp:
        return mb_html.para(explanation[0].upper() + explanation[1:] + ".")
    if "«" in sfp or "»" in sfp:
        full_exp = f"(The label {sfp} means {explanation}.)"
    else:
        full_exp = f"(The label «{sfp}» means {explanation}.)"
    return mb_html.para(full_exp)


_EXPLANATIONS = {
    "alef-dual-ml-alef-first": dml_e.EXPLANATIONS_DML_A1,
    "alef-dual-ml-alef-second": dml_e.EXPLANATIONS_DML_A2,
    "kq-simple": kq_simple_e.explanation_for_path,
    "kq-complex": kq_complex_e.explanation_for_path,
    "mtgmtg": mtgmtg_e.explanation_for_path,
    "oleh-yored": ole_yored_e.EXPLANATIONS,
    "pasoleg-1": pasoleg_1_labels.explanation_for_path,
    "quick-brown-fox": quick_brown_e.explanation_for_path,
    "qamats-variants": qamats_var_e.explanation_for_path,
    "rare-tmpls": rare_tmpls_e.explanation_for_path,
    "sec-misc": sec_merk_e.explanation_for_path,
    "sec-merk": sec_merk_e.explanation_for_path,
    "sec-misc-shewa": sec_merk_e.explanation_for_shewa_path,
    "sec-merk-shewa": sec_merk_e.explanation_for_shewa_path,
    "sec-star-breuer-cos": sec_merk_e.explanation_for_ref_path,
    "slh-word": slh_word_e.explanation_for_path,
    "tsinnorit": tsinnorit_e.EXPLANATIONS,
    "unicode": unicode_e.explanation_for_path,
}


_OVERALL_EXPLANATIONS = {
    "alef-dual-ml-alef-first": dml_e.OVERALL_EXPLANATION_DML_A1,
    "alef-dual-ml-alef-second": dml_e.OVERALL_EXPLANATION_DML_A2,
    "dexi-stress-meteg": dexi_stress_meteg_e.overall_explanation,
    "doc-note-notation": doc_note_notation_e.OVERALL_EXPLANATION,
    "kq-simple": kq_simple_e.OVERALL_EXPLANATION,
    "kq-complex": kq_complex_e.OVERALL_EXPLANATION,
    "mtgmtg": mtgmtg_e.OVERALL_EXPLANATION,
    "oleh-yored": ole_yored_e.OVERALL_EXPLANATION,
    "pasoleg-1": pasoleg_1_labels.OVERALL_EXPLANATION,
    "quick-brown-fox": quick_brown_e.OVERALL_EXPLANATION,
    "qamats-variants": qamats_var_e.OVERALL_EXPLANATION,
    "rare-tmpls": rare_tmpls_e.OVERALL_EXPLANATION,
    "sec-merk": sec_merk_e.OVERALL_EXPLANATION,
    "sec-misc": sec_merk_e.OVERALL_EXPLANATION,
    "sec-merk-shewa": sec_merk_e.OVERALL_EXPLANATION_SHEWA,
    "sec-misc-shewa": sec_merk_e.OVERALL_EXPLANATION_SHEWA,
    "sec-star-breuer-cos": sec_merk_e.OVERALL_EXPLANATION_REF,
    "slh-word": slh_word_e.OVERALL_EXPLANATION,
    "tsinnorit": tsinnorit_e.OVERALL_EXPLANATION,
    "unicode": unicode_e.OVERALL_EXPLANATION,
}


# The foi_paths of a stem whose rows go to its page's introduction rather than to a
# table; its explanation then takes those rows and returns the introduction's HTML.
_COUNTED_FOI_PATHS = {
    "dexi-stress-meteg": dexi_stress_meteg_e.COUNTED_FOI_PATHS,
}


# The JavaScript of a stem whose page has a script, which follows the page's tables.
_SCRIPTS = {
    "dexi-stress-meteg": dexi_stress_meteg_e.SCRIPT,
}


def _section_heads(outfile_stem, tuple_foi_path, len_trs):
    rem_thresholds = 5, 20, 80
    if len_trs > rem_thresholds[1]:
        count1 = rem_thresholds[0]
        tup1 = count1, len_trs
        tup2 = len_trs - count1, len_trs
        part1b, part2 = _section_head_parts_1b_and_2(
            outfile_stem, len_trs, rem_thresholds, tup2, tuple_foi_path
        )
        the_1st = f"the first {tup1[0]} of {tup1[1]} are shown."
        part1 = [the_1st, *part1b]
    elif len_trs:
        count1 = len_trs
        part1 = [
            (
                "one example is shown."
                if tuple_foi_path in holam_foi.DIVINE_NAME_PATHS
                else f"all {len_trs} are shown."
            )
        ]
        part2 = None
    else:  # A declared category with no rows
        count1 = 0
        part1 = None
        part2 = None
    head1a = [_intro(tuple_foi_path, part1)]
    head1b = _head1b(tuple_foi_path)
    head2 = [_intro(tuple_foi_path, part2, "-rest")] if part2 else None
    return count1, head1a + head1b, head2
