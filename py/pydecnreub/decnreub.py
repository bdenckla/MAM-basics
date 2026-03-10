from itertools import zip_longest
from pydecnreub import decnreub_diff as dr_diff
from pydecnreub import decnreub_for_one_cant as dr_for_one_cant
from pycmn import hebrew_punctuation as hpu
from pycmn import bib_locales as tbn
from pycmn import ws_tmpl2 as wtp
from pycmn.my_utils import sl_map
from pycmn.my_utils import sum_of_map
from pycmn.shrink import shrink
from py_misc.split import my_re_split


def do_one_book(book_mpp):
    return sum_of_map(_do_one_verse, book_mpp["verses_plus"].items())


def flatrow_for_jsondump(row):
    additions = {
        "dup": _maybe_simplify(row["dup"]),
        "dlo": _maybe_simplify(row["dlo"]),
    }
    return {**row, **additions}


def _do_one_verse(bcvt_and_minirow):
    bcvt, minirow = bcvt_and_minirow
    if tbn.has_dualcant(bcvt):
        out_1 = _do_one_wtseq(minirow.EP)
        out_2 = dr_diff.add_diffs(out_1)
        out_3 = _add_bcv(bcvt, out_2)
        return out_3
    return []


def _do_one_wtseq(wtseq):
    return sum_of_map(_do_one_wtel, wtseq)


def _do_one_wtel(wtel):
    if isinstance(wtel, str):
        return _HANDLERS_FOR_TOP["string"](wtel)
    if tmpl_name := wtp.template_name(wtel):
        return _HANDLERS_FOR_TOP[tmpl_name](wtel)
    assert False, wtel


def _hnd_top_dualcant(tmpl):
    triple = wtp.map_params(_do_one_wtseq_for_one_cant, tmpl)
    assert len(triple) == 3
    b_xx = zip_longest(*triple)
    b_xx_neq = filter(_bxx_item_neq, b_xx)
    return sl_map(_mk_rec, b_xx_neq)


def _hnd_top_return_empty_list(_1):
    return []


def _mk_rec(b_xx_item):
    b_co_item, b_lo_item, b_up_item = b_xx_item
    return {
        "wlo": b_lo_item,
        "wup": b_up_item,
        "wco": b_co_item,
    }


def _bxx_item_neq(b_xx_item):
    assert len(b_xx_item) == 3
    return not (b_xx_item[0] == b_xx_item[1] == b_xx_item[2])


def _do_one_wtseq_for_one_cant(wtseq):
    wtseq_1 = dr_for_one_cant.do_one_wtseq(wtseq)
    wtseq_2 = shrink(wtseq_1)
    wtseq_3 = sum_of_map(_my_split_wtel, wtseq_2)
    return wtseq_3


def _my_split_wtel(wtel):
    if not isinstance(wtel, str):
        return [wtel]
    return my_re_split(_PATT_FOR_SPLIT, wtel)


def _add_bcv(bcvt, dualcant_recs):
    return sl_map((_add_bcv_to_one, bcvt), dualcant_recs)


def _add_bcv_to_one(bcvt, one_dualcant_rec):
    return {
        "bcv": tbn.short_bcv_of_bcvt(bcvt),
        **one_dualcant_rec,
    }


def _maybe_simplify(dxx):  # dxx: dup or dlo
    if isinstance(dxx, (list, tuple)) and len(dxx) == 1:
        if isinstance(dxx[0], str):
            return dxx[0]
        return _maybe_simplify(dxx[0])
    return dxx


_HANDLERS_FOR_TOP = {
    "מ:כפול": _hnd_top_dualcant,
    #
    "string": _hnd_top_return_empty_list,
    "נוסח": _hnd_top_return_empty_list,
    'כו"ק': _hnd_top_return_empty_list,
    "מ:לגרמיה-2": _hnd_top_return_empty_list,
    "ססס": _hnd_top_return_empty_list,
}
_PATT_FOR_SPLIT = r"([^ y]+)".replace("y", hpu.MAQ)
