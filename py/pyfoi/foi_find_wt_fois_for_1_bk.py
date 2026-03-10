from py_misc import my_utils_for_mainish as my_utils_fm


def _mk_mroge_mr(bcvt, minirow):
    return {
        "mroge-bcvt": bcvt,
        "mroge-minirow": minirow,
    }


def _mk_mroge_ge(bcvt, good_ending):
    return {
        "mroge-bcvt": bcvt,
        "mroge-good-ending": good_ending,
    }


def _find_wikitext_fois(fois_funs, mroge):
    # mroge: minirow or good ending
    out = []
    for fff in fois_funs:
        out.extend(fff(mroge))
    return out


def find_wt_fois_for_1_bk(the_arg_triple):
    fois_funs, book_mpp, bkid = the_arg_triple
    my_utils_fm.show_progress_g(__file__, "Wikitext", bkid)
    verses = book_mpp["verses_plus"]
    good_ending = book_mpp["good_ending_with_bcvt"]
    out = {}
    for bcvt, minirow in verses.items():
        fois_for_this_verse = _find_wikitext_fois(
            fois_funs, _mk_mroge_mr(bcvt, minirow)
        )
        if fois_for_this_verse:
            out[bcvt] = fois_for_this_verse
    if good_ending:
        bcvt = good_ending["last_bcvt"]
        fois_for_ge = _find_wikitext_fois(fois_funs, _mk_mroge_ge(bcvt, good_ending))
        if fois_for_ge:
            if bcvt in out:
                out[bcvt] += fois_for_ge
            else:
                out[bcvt] = fois_for_ge
    return bkid, out
