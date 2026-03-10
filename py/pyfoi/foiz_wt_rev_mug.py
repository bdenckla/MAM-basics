from pycmn import bib_locales as tbn
from pycmn import hebrew_accents as ha
from py_misc import wt_qere
from pycmn.my_utils import sum_of_map


def find_fois_wt(mroge):
    if not tbn.is_poetcant(mroge["mroge-bcvt"]):
        return []
    verse = wt_qere.get_verse_as_wordstrs(_HANDLERS, mroge)
    return sum_of_map(_get_features, verse)


_HANDLERS = {
    **wt_qere.HANDLERS,
    "מ:דחי": wt_qere.hnd_recurse_on_arg_0,
    "מ:צינור": wt_qere.hnd_recurse_on_arg_0,
    "מ:קמץ": wt_qere.hnd_recurse_on_param_dalet,
    #
    "מ:פסק": wt_qere.hnd_return_plain_space,
}

######################################################################
######################################################################


def _get_features(word: str):
    gmci = word.find(ha.GER_M)
    if gmci != -1:
        if word[gmci + 1] == ha.REV:
            foi_path = ("revia-mugrash",)
            foi_target = word
            return [(foi_path, foi_target)]
    return []
