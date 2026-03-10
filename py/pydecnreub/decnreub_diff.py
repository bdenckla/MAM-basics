from pycmn import my_diffs
from pycmn import str_defs as sd
from pycmn import uni_heb as uh
from pycmn.my_utils import sl_map


def add_diffs(dualcant_recs):
    return sl_map(_add_diffs_to_one, dualcant_recs)


def _add_diffs_to_one(one_dualcant_rec):
    wlo = one_dualcant_rec["wlo"]
    wup = one_dualcant_rec["wup"]
    wco = one_dualcant_rec["wco"]
    return {
        **one_dualcant_rec,
        "dup": _get_diff(wco, wup),
        "dlo": _get_diff(wco, wlo),
    }


def _get_diff(co_word, te_word):  # co_word: combined (elyon + taxton) word
    if isinstance(co_word, str) and isinstance(te_word, str):
        co_seq, te_seq = _seq_for_diff(co_word), _seq_for_diff(te_word)
    else:
        co_word_h = _make_hashable(co_word)
        te_word_h = _make_hashable(te_word)
        co_seq, te_seq = (co_word_h,), (te_word_h,)
    diffs = my_diffs.get(co_seq, te_seq)
    diffs_favoring_deletes = list(map(_favor_delete, diffs))
    return diffs_favoring_deletes


def _seq_for_diff(word):
    wchars_no_cgj = word.replace(sd.CGJ, "")
    char_names = tuple(uh.t_shunnas(wchars_no_cgj))
    return char_names


def _make_hashable(obj):
    if isinstance(obj, dict):
        new_keys = map(_make_hashable, obj.keys())
        new_vals = map(_make_hashable, obj.values())
        new_dic = dict(zip(new_keys, new_vals))
        new_items = tuple(new_dic.items())
        return new_items
    if isinstance(obj, list):
        return tuple(map(_make_hashable, obj))
    return obj


def _favor_delete(diff):
    # We don't label a delete, i.e. we don't label
    # it with 'del' or similar, because
    # deletes are the most common opcode.
    if diff[1] is None:
        return diff[0]
    if diff[0] is None:
        return "ins", diff[1]
    return "rep", diff[0], diff[1]
