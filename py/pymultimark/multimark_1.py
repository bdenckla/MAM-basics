from pymultimark import multimark_uni as splhu
from pymultimark import multimark_char as splhc
from pycmn import hebrew_punctuation as hpu
from pycmn import bib_locales as tbn
from pycmn import ws_tmpl2 as wtp
from py_misc import wt_qere
from py_misc.my_utils_for_mainish import show_progress_g
from pycmn.my_utils import sum_of_map
from pycmn.my_utils import sum_of_seqs
from py_misc.split import my_re_split


def get_raw_data_wt(books_mpp):
    return sum_of_map(_do_one_book, books_mpp.items())


def _do_one_book(bk39id_and_book_mpp):
    bk39id, book_mpp = bk39id_and_book_mpp
    show_progress_g(__file__, bk39id)
    return sum_of_map(_do_one_verse, book_mpp["verses_plus"].items())


def _do_one_verse(bcvt_and_minirow):
    bcvt, minirow = bcvt_and_minirow
    qere = wt_qere.do_one_wtseq(wt_qere.HANDLERS, minirow.EP)
    list_of_chars_with_multimarks = _do_one_wtseq(qere)
    if list_of_chars_with_multimarks:
        out_pair = list_of_chars_with_multimarks, tbn.short_bcv_of_bcvt(bcvt)
        return [out_pair]
    return []


def _do_one_wtseq(wtseq):
    return sum_of_map(_do_one_wtel, wtseq)


def _do_one_wtel(wtel):
    if isinstance(wtel, str):
        return _do_one_string(wtel)
    tmpl_name = wtp.template_name(wtel)
    return _HANDLERS[tmpl_name](wtel)


def _hnd_return_empty_list(_1):
    return []


def _hnd_recurse_on_param_vals(tmpl):
    return sum_of_seqs(wtp.map_params(_do_one_wtseq, tmpl))


def _do_one_string(string):
    lis_word_as_str = my_re_split(_PATT_FOR_SPLIT, string)
    sh_words = splhu.convert_uw_to_splh(lis_word_as_str)
    if chars_with_multimarks := _cwm_in_words(sh_words):
        return chars_with_multimarks
    return []


def _cwm_in_words(words):  # cwm: chars with multimarks
    return sum(map(_cwm_in_word, words), tuple())


def _cwm_in_word(word):  # cwm: chars with multimarks
    chars = word["chars"]
    return tuple(
        _this_n_nxt_n_pre(chars, i) for i, char in enumerate(chars) if splhc.mmcat(char)
    )


def _this_n_nxt_n_pre(seq, i):
    return seq[i], _nxt(seq, i), _pre(seq, i)


def _nxt(seq, i):
    return None if i + 1 == len(seq) else seq[i + 1]


def _pre(seq, i):
    return None if i == 0 else seq[i - 1]


_HANDLERS = {
    "מ:דחי": _hnd_recurse_on_param_vals,
    "מ:צינור": _hnd_recurse_on_param_vals,
    "מ:קמץ": _hnd_recurse_on_param_vals,
    "מ:כפול": _hnd_recurse_on_param_vals,
    #
    "מ:פסק": _hnd_return_empty_list,
}
_PATT_FOR_SPLIT = (
    r"[ xyz]+".replace("x", hpu.SOPA).replace("y", hpu.MAQ).replace("z", hpu.PASOLEG)
)
