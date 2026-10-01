from itertools import starmap
import yeivin_itm.content.my_yeivin_amisc_tocsec_metadata as tsm
import yeivin_itm.content.my_yeivin_amisc_helpers_for_bibrefs as bibrefs
import yeivin_itm.content.my_yeivin_amisc_helpers_for_locales as loc
import yeivin_itm.content.my_yeivin_amisc_helpers_private as pri
import mb_cmn.str_defs as sd
import mb_cmn.hebrew_punctuation as hpu
import mb_cmn.my_utils as my_utils
import py_html.legacy_html as aht_html


def ftntjoin(pre, ftnt):
    if isinstance(pre, str):
        pre_n1 = pre[-1]
        the_map = ":.,acdnrst"
        assert pre_n1 in the_map
        return pre + " ", paren(ftnt)
    assert aht_html.is_htel(pre)
    assert pre["attr"]["class"] == "romanized"
    return pre, " ", paren(ftnt)


def ftntjoin2(pre, ftnt1, ftnt2):
    return ftntjoin(pre, [ftnt1, ", ", ftnt2])


def ftnt_contents_for_pointer_to_huge(huge_ftnt_rec):
    return [
        "See ",
        aht_html.anchor(
            huge_ftnt_rec["huge-ftnt-rec-h1-contents"],
            {"href": huge_ftnt_rec["huge-ftnt-rec-path-rel-web-publish-topdir"]},
        ),
        ".",
    ]


def mwrom(string: str, mwcap, as_str=False):
    return pri.mwrom(string, mwcap, as_str)


def hbo(contents, attr=None):
    nn_attr = {} if attr is None else attr  # nn: non-None
    return aht_html.bdi(contents, {"lang": "hbo", **nn_attr})


def make_ftnt_struct(secnum, ftnt_index, body):
    return pri.make_ftnt_struct(secnum, ftnt_index, body)


def make_html_for_ftnt_callout(ftnt_struct):
    return pri.make_html_for_ftnt_callout(ftnt_struct)


def make_html_for_ftnt_bodies(ftnt_structs):
    if not ftnt_structs:
        return []
    html_for_bodies = list(map(pri.make_html_for_one_ftnt_body, ftnt_structs))
    the_hr = aht_html.horizontal_rule()
    foot_or_foots = "Footnotes" if len(ftnt_structs) > 1 else "Footnote"
    intro = aht_html.para(f"{foot_or_foots} for this section:")
    return the_hr, intro, *html_for_bodies


def emphasis(contents):
    return aht_html.emphasis(contents)


def line_break(part1, part2):
    return part1, aht_html.line_break(), part2


def line_break_seq(parts):
    flat_parts = list(map(aht_html.flatten, parts))
    rough = my_utils.intersperse([aht_html.line_break()], flat_parts)
    return my_utils.sum_of_seqs(rough)


def some_hi(norm_star_loc):
    # Like hboloc, but with some highlighting
    normal_word, starred_word, xloc = norm_star_loc
    parts_with_hi = pri.parts_with_hi((normal_word, starred_word))
    dual_contents = {
        "hboloc-contents-for-here": parts_with_hi,
        "hboloc-contents-for-list-of-bibrefs": normal_word,
    }
    return hboloc(dual_contents, xloc)


def some_hi_no_loc(norm_star):
    return hbo(pri.parts_with_hi(norm_star))


def hbo_varacc(contents):
    va1 = "book, chapter, and verse not given"
    va2 = "this word appears with various accents in various locales"
    return hbo(contents, {"title": f"{va1}: {va2}"})


def norm_and_syl_inline(norm_dash_loc):
    normal_word, dash_sep_word, sloc = norm_dash_loc
    assert normal_word == pri.strip_syl_stuff(dash_sep_word)
    return hboloc(normal_word, sloc), syl_inline(dash_sep_word)


def norm_and_syl_sep(word, dash_sep_word, xloc=None):
    hbo_element = hboloc(word, xloc) if xloc else hbo(word)
    return hbo_element, *syl_sep(word, dash_sep_word)


def syl_sep(word, dash_sep_word):
    assert word == pri.strip_syl_stuff(dash_sep_word)
    accum = pri.syllables_generic(dash_sep_word)
    return list(map(hbo, accum))


def lns(xloc, word, dash_sep_word):
    return norm_and_syl_sep(word, dash_sep_word, xloc)


def lhbo(xloc, contents, attr=None):
    return hboloc(contents, xloc, attr)


def make_dloc(sloc1, sloc2):
    return loc.make_dloc(sloc1, sloc2)


def make_aeloc(sloc):
    return loc.make_aeloc(sloc)


def isolated_slocale(sloc):
    return bibrefs.strip_at_sign_prefix(sloc)


def compare_with(ms_or_mss, hbo_contents):
    return "cf. ", ms_or_mss, " ", hbo(hbo_contents)


def sy3(dash_sep_word):
    return pri.syn(3, dash_sep_word)


def sy4(dash_sep_word):
    return pri.syn(4, dash_sep_word)


def sy5(dash_sep_word):
    return pri.syn(5, dash_sep_word)


def sy6(dash_sep_word):
    return pri.syn(6, dash_sep_word)


#
def sy4ps(dash_sep_word):
    return pri.syn(4, dash_sep_word, "-")


def sy5ps(dash_sep_word):
    return pri.syn(5, dash_sep_word, "-")


def sy6ps(dash_sep_word):
    return pri.syn(6, dash_sep_word, "-")


#
def sy4pe(dash_sep_word):
    return pri.syn(4, dash_sep_word, "", "-")


def sy5pe(dash_sep_word):
    return pri.syn(5, dash_sep_word, "", "-")


def sy6pe(dash_sep_word):
    return pri.syn(6, dash_sep_word, "", "-")


#
def sy4pspe(dash_sep_word):
    return pri.syn(4, dash_sep_word, "-", "-")


def sy5pspe(dash_sep_word):
    return pri.syn(5, dash_sep_word, "-", "-")


def sy6pspe(dash_sep_word):
    return pri.syn(6, dash_sep_word, "-", "-")


# def sy6ps2pe(dash_sep_word): return pri.syn(6, dash_sep_word, '--', '-')


def hbo_attr_for_els():
    return {"class": "extra-letter-spacing"}


def hbo_els(contents):
    return hbo(contents, hbo_attr_for_els())


def comma_list_of_bdis(*list_items):
    bdis = list(map(aht_html.bdi, list_items))
    return my_utils.intersperse(", ", bdis)


def rom(string: str, cap=False, as_str=False):
    assert isinstance(string, str)
    if cap:
        words = string.split(" ")
        string = " ".join(word.capitalize() for word in words)
    if as_str:
        return string
    return aht_html.span_c(string, "romanized")


def table_std(
    args_to_trod,
    attr=None,
    coldirs=None,
    tdattrs=None,
    arg_to_troh=None,
    arg_to_caption=None,
):
    if coldirs:
        assert not tdattrs
        tdattrs = [{"dir": coldir} for coldir in coldirs]
    args_to_table = [
        aht_html.table_row_of_data(tdconts, tdattrs) for tdconts in args_to_trod
    ]
    if arg_to_troh:
        header_row = aht_html.table_row_of_headers(arg_to_troh)
        args_to_table = [header_row, *args_to_table]
    if arg_to_caption:
        if isinstance(arg_to_caption, dict):
            atc_cont = arg_to_caption["atc-contents"]
            atc_attr = arg_to_caption["atc-attr"]
            caption = aht_html.caption(atc_cont, atc_attr)
        else:
            caption = aht_html.caption(arg_to_caption)
        args_to_table = [caption, *args_to_table]
    return aht_html.table(args_to_table, pri.add_center(attr))


def table_std_rtl(args_to_trod, coldirs=None, arg_to_caption=None):
    return table_std(
        args_to_trod,
        attr={"dir": "rtl"},
        coldirs=coldirs,
        arg_to_caption=arg_to_caption,
    )


def alpha_beta(hbo_str: str, xloc):
    parts = hbo_str.split(" ")
    if len(parts) == 1:
        pre, mid, post = hbo_str.partition(hpu.MAQ)
        assert pre and post
        assert mid == hpu.MAQ
        parts = pre + mid, post
    assert len(parts) == 2
    return hboloc(parts[0], xloc), hbo(parts[1])


def table_std_alpha_beta_3col(args_to_trod, arg_to_troh=("", "α", "β")):
    new_args_to_trod = [[cell[2], cell[0], cell[1]] for cell in args_to_trod]
    return table_std(
        new_args_to_trod,
        {"dir": "rtl"},
        tdattrs=({"dir": "ltr"}, {"align": "left"}, {}),
        arg_to_troh=arg_to_troh,
    )


def table_std_alpha_beta_2col(args_to_trod, arg_to_troh=("α", "β")):
    return table_std(
        args_to_trod,
        {"dir": "rtl"},
        tdattrs=({"align": "left"}, {}),
        arg_to_troh=arg_to_troh,
    )


def table_std_alpha_beta_2col_std(args_to_alpha_beta, arg_to_troh=("α", "β")):
    args_to_trod = list(starmap(alpha_beta, args_to_alpha_beta))
    return table_std_alpha_beta_2col(args_to_trod, arg_to_troh)


def table_std_alpha_beta_3col_std(list_of_abc, arg_to_troh=("", "α", "β")):
    args_to_trod = [(*alpha_beta(a, b), c) for a, b, c in list_of_abc]
    return table_std_alpha_beta_3col(args_to_trod, arg_to_troh)


def span_ltr(contents):
    return aht_html.span(contents, {"dir": "ltr"})


def table_row_std(list_of_cell_data):
    return aht_html.table_row_of_data(list_of_cell_data)


def abbr_tit(abbr_contents, title_value):
    return aht_html.abbr(abbr_contents, {"title": title_value})


def abbr_tit_sc(abbr_contents, title_value):
    return aht_html.abbr(abbr_contents, {"title": title_value, "class": "small-caps"})


def rtn(num_of_sec):
    """Reference to a numbered section."""
    id_of_sec = pri.id_of_numsec(num_of_sec)
    filename = tsm.filename_for_secnum(num_of_sec)
    attr = {"href": f"{filename}#{id_of_sec}", "data-num-of-sec": str(num_of_sec)}
    return aht_html.anchor(f"#{num_of_sec}", attr)


def rtn_p(num_of_sec, pre=None, post=None):
    """Reference to a numbered section, in parentheses."""
    return paren([rtn(num_of_sec)], pre=pre, post=post)


def rtn_p2(num_of_sec1, num_of_sec2, pre=None, post=None):
    """Reference to two numbered sections, in a single set of parentheses."""
    inner = rtn(num_of_sec1), ", ", rtn(num_of_sec2)
    return paren(inner, pre=pre, post=post)


def paren(inner, pre=None, post=None):
    inner = aht_html.flatten_nn(inner)
    pre = pre or []
    post = post or []
    return "(", *pre, *inner, *post, ")"


def nowrap(inner):
    return aht_html.span(inner, {"style": "white-space: nowrap"})


def single_angle_quotes_hh(inner):
    return nowrap(["‹" + sd.HAIRSP, inner, sd.HAIRSP + "›"])


def para_paren(inner):
    return aht_html.para(paren(inner))


def paren_xt(inner, pre=None):  # xt: something, then thin space
    return paren(inner, pre, post=[sd.THSP])  # nowrap needed?


def paren_tt(inner):
    """tt: with thin space inside both parentheses"""
    return paren(inner, pre=[sd.THSP], post=[sd.THSP])  # nowrap needed?


def paren_th(inner):
    return paren(inner, pre=[sd.THSP], post=[sd.HAIRSP])  # nowrap needed?


def dquotes(inner):
    return "“", *aht_html.flatten_nn(inner), "”"


def trvhnd_make_html_for_tose_h(contents):
    """tose_h: tocsec heading"""
    # ITM uses centered all-caps italic for this heading level.
    # ITM resorts to single quotes for romanized words
    # within these headings.
    return [aht_html.heading_level_1(contents)]


def trvhnd_make_html_for_tise_h(contents):
    """tise_h: titsec heading"""
    # ITM uses left-aligned italic for this heading level.
    # We just call it a level 2 heading and accept
    # whatever styling that implies.
    # We assume that the styling of h2 is not
    # italic since there are romanized words within these headings that
    # will be in italic and these words are supposed to be style-distinguished
    # from normal words in the heading.
    # ITM uses italic styling for these headings
    # so it resorts to single quotes for romanized words
    # within these headings.
    return [aht_html.heading_level_2(contents)]


def trvhnd_make_html_for_nsi(numsec_item):
    num_of_sec, contents_of_sec = numsec_item
    return [
        pri.numbered_section_heading(num_of_sec),
        *pri.insert_numsec_selflink(num_of_sec, contents_of_sec),
        *bibrefs.make_html_for_bibrefs(contents_of_sec),
    ]


def syl_inline(dash_sep_word):
    accum = pri.syllables_generic(dash_sep_word)
    accum2 = my_utils.intersperse([sd.NBSP], accum)
    accum3 = my_utils.sum_of_seqs(accum2)
    return hbo(accum3)


def hboloc(contents, xloc, attr=None):
    nn_attr = {} if attr is None else attr  # nn: non-None
    hboloc_attr = pri.hboloc_attr(xloc)
    for_here, for_lob = pri.hboloc_get_contents(contents)
    if for_lob:
        hboloc_attr["data-contents-for-list-of-bibrefs"] = for_lob
    return hbo(for_here, {**hboloc_attr, **nn_attr})


def hbo_loc_ms(hbo_contents, xloc, ms_or_mss):
    return hboloc(hbo_contents, xloc), " ", paren(ms_or_mss)
