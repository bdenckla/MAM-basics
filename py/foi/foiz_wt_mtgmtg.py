from pycmn import hebrew_points as hpo
from pycmn import hebrew_punctuation as hpu
from py_misc import wt_qere
from pycmn.my_utils import sum_of_map
from pycmn.my_utils import first_and_only_and_str


def find_fois_wt(mroge):
    verse = wt_qere.get_verse_as_wordstrs(_HANDLERS, mroge)
    return sum_of_map(_get_features, verse)


_HANDLERS = {
    **wt_qere.HANDLERS,
    "מ:דחי": wt_qere.hnd_recurse_on_arg_0,
    "מ:צינור": wt_qere.hnd_recurse_on_arg_0,
    "מ:קמץ": wt_qere.hnd_recurse_on_param_dalet,
    "מ:כפול": wt_qere.hnd_recurse_on_param_vals_and_ca,
    #
    "מ:פסק": wt_qere.hnd_return_plain_space,
}

######################################################################
######################################################################


def _get_features(word: str):
    cnt_of_mtgoslq = word.count(hpo.MTGOSLQ)
    if cnt_of_mtgoslq < 2:
        return []
    foi_path = "mtgmtg", *_get_qualifiers(word, cnt_of_mtgoslq)
    foi_target = word
    return [(foi_path, foi_target)]


def _get_qualifiers(word: str, cnt_of_mtgoslq: int):
    has_sopa = word[-1] == hpu.SOPA
    assert has_sopa or hpu.SOPA not in word
    cnt_of_mtg = cnt_of_mtgoslq - 1 if has_sopa else cnt_of_mtgoslq
    sopa = "sopa-y" if has_sopa else "sopa-n"
    maq = "maq-y" if hpu.MAQ in word else "maq-n"
    return str(cnt_of_mtg), sopa, maq
