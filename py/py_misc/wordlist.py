from py_misc import wt_qere
from py_misc import hebrew_letter_words as hlw
from pycmn import hebrew_punctuation as hpu
from pycmn import ws_tmpl2 as wtp
from pycmn import template_names as tmpln
from pycmn.my_utils import sum_of_map
from pycmn.my_utils import sum_of_seqs
from pycmn.my_utils import sl_map
from pycmn.my_utils import first_and_only_and_str
from py_misc.split import my_re_split


def get_sorted_words_wt(books_mpp):
    som = sum_of_map(_do_one_book, books_mpp.values())
    return sorted(set(som), key=_keyfn)


def _keyfn(word):
    if isinstance(word, str):
        word_and_slhyn = word, "slh no"
    else:
        slh_quad = word
        word_and_slhyn = slh_quad[0], "slh yes"
    word_str = word_and_slhyn[0]
    out_triple = hlw.letters_and_maqafs(word_str), *word_and_slhyn
    return out_triple  # E.g. (str('יקרא'), str('יִקְרָ֗א'), 'slh no')


def _do_one_book(book_mpp):
    return sum_of_map(_do_one_verse, book_mpp["verses_plus"].values())


def _do_one_verse(minirow):
    qere = wt_qere.do_one_wtseq(_HANDLERS_FOR_STAGE_1, minirow.EP)
    return _do_one_wtseq(qere)


def _do_one_wtseq(wtseq):
    return sum_of_map(_do_one_wtel, wtseq)


def _do_one_wtel(wtel):
    if isinstance(wtel, str):
        return my_re_split(_PATT_FOR_SPLIT, wtel)
    tmpl_name = wtp.template_name(wtel)
    return _HANDLERS_FOR_STAGE_2[tmpl_name](wtel)


def _hnd_return_empty_list(_1):
    return []


def _hnd_slh_word(tmpl):
    quad1 = [wtp.template_param_val(tmpl, key) for key in ("2", "3", "4", "5")]
    quad2 = sl_map(first_and_only_and_str, quad1)
    return [tuple(quad2)]


def _hnd_recurse_on_param_vals(tmpl):
    return sum_of_seqs(wtp.map_params(_do_one_wtseq, tmpl))


_HANDLERS_FOR_STAGE_2 = {
    "מ:דחי": _hnd_recurse_on_param_vals,
    "מ:צינור": _hnd_recurse_on_param_vals,
    "מ:קמץ": _hnd_recurse_on_param_vals,
    "מ:כפול": _hnd_recurse_on_param_vals,
    tmpln.SLH_WORD: _hnd_slh_word,
    "מ:פסק": _hnd_return_empty_list,
}
_HANDLERS_FOR_STAGE_1 = {
    **wt_qere.HANDLERS,
    tmpln.SLH_WORD: wt_qere.hnd_identity,
}
_PATT_FOR_SPLIT = (
    r"[ xyz]+".replace("x", hpu.SOPA).replace("y", hpu.MAQ).replace("z", hpu.PASOLEG)
)
