"""Survey Wikisource template usage patterns in MAM-parsed plus data."""

import json
import collections
from itertools import starmap

from pytmpl_survey import column_d_0_process_all_mpasuq_calls as cdp
from pytmpl_survey import column_d_0_store_the_mpasuq_call_plus as cds_plus
from pycmn import bib_locales as tbn
from py_misc import my_utils_for_mainish as my_utils_fm
from pycmn import ws_tmpl2 as wtp2
from pycmn import template_names as tmpln

_MINIROW = collections.namedtuple("_MINIROW", "DP, CP, EP")


def _wtel_type_and_subtype(wtel):
    assert wtp2.is_template(wtel), wtel
    return "tmpl", wtp2.template_name(wtel)


def _record_wtel(accum, wtel_rec):
    bscv, stack, wtel = wtel_rec
    if isinstance(wtel, str):
        return
    assert isinstance(wtel, dict)
    wtel_type, wtel_subtype = _wtel_type_and_subtype(wtel)
    column_letter = stack[0]
    _my_plus_equals(
        accum["column_counts"],
        wtel_type,
        wtel_subtype,
        column_letter,
    )
    _record_naked_sam2_pe2_pe3(accum, wtel_rec, wtel_subtype)
    _record_tmpl(accum, wtel_rec, wtel_subtype)


def _record_naked_sam2_pe2_pe3(accum, wtel_rec, wtel_subtype):
    bscv, stack, wtel = wtel_rec
    if wtel_subtype in _SAM2_PE2_PE3 and stack == ("E",):
        if wtp2.template_len(wtel) == 2:
            assert wtp2.template_element(wtel, 1) == ["פסקא באמצע פסוק"]
        else:
            accum["naked_sam2_pe2_pe3"].append(bscv)


_SAM2_PE2_PE3 = {"סס", "פפ", "פפפ"}


def _record_tmpl(accum, wtel_rec, wtel_subtype):
    bscv, stack, wtel = wtel_rec
    _my_plus_equals(accum["stack_counts"], wtel_subtype, _string_from_stack(stack))
    argc = wtp2.template_len(wtel) - 1
    _check_argc(wtel_subtype, argc)
    _my_plus_equals(accum["arg_counts"], wtel_subtype, argc)
    new_stack = *stack, wtel_subtype
    for arg in wtp2.template_param_vals(wtel):
        for arg_wtel in arg:
            arg_wtel_rec = bscv, new_stack, arg_wtel
            _record_wtel(accum, arg_wtel_rec)


def _string_from_stack(stack):
    return "/".join(stack)


def _my_plus_equals(accum_x, *key_parts):
    accum_x[key_parts] += 1


_EXPECTED_ARGC = {
    str('כו"ק'): 2,
    str("מ:אות מנוקדת"): 1,
    tmpln.K1Q2_SR_KQQ: tuple((2, 3)),
    tmpln.K2Q1: 2,
    tmpln.K2Q2: 2,
    tmpln.K3Q3: 2,
}


def _handle_int(argc_expectation):
    if isinstance(argc_expectation, int):
        return (argc_expectation,)
    return argc_expectation


def _check_argc(wtel_subtype, argc):
    exp = _EXPECTED_ARGC.get(wtel_subtype)
    assert exp is None or argc in _handle_int(exp)


def _record_pseudo_verse(accum, bscv, minirow):
    bscv_dic = _make_bscv_dic(bscv)
    colpairs = (
        (minirow.DP, "D"),
        (minirow.CP, "C"),
        (minirow.EP, "E"),
    )
    for wtseq, column_letter in colpairs:
        for wtel in wtseq:
            stack = (column_letter,)
            wtel_rec = bscv_dic, stack, wtel
            _record_wtel(accum, wtel_rec)


def _flatten_col_counts(accum):
    dic = accum["column_counts"]
    records = list(starmap(_flatten_col_counts_item, dic.items()))
    return _sort_dics_by_values(records)


def _sort_dics_by_values(dics):
    return sorted(dics, key=_keyfn)


def _keyfn(dic):
    return tuple(dic.values())


def _flatten_col_counts_item(key, count):
    rec = {
        "wtel_type": key[0],
        "wtel_subtype": key[1],
        "column_letter": key[2],
        "count": count,
    }
    return rec


def _flatten_stack_counts(accum):
    dic = accum["stack_counts"]
    records = list(starmap(_flatten_stack_counts_item, dic.items()))
    return _sort_dics_by_values(records)


def _flatten_stack_counts_item(key, count):
    rec = {"wtel_subtype": key[0], "stack": key[1], "count": count}
    return rec


def _flatten_arg_counts(accum):
    dic = accum["arg_counts"]
    variations = {}
    for key, count in dic.items():
        wtel_subtype = key[0]
        if wtel_subtype in variations:
            variations[wtel_subtype] += 1
        else:
            variations[wtel_subtype] = 1
    records = []
    for key, count in dic.items():
        wtel_subtype = key[0]
        rec = {
            "wtel_subtype": wtel_subtype,
            "arg_count": key[1],
            "count": count,
            "variations": variations[wtel_subtype],
        }
        records.append(rec)
    return _sort_dics_by_values(records)


def _do_a_book39(book39, accum):
    bk24na, sub_bkna = book39["book24_name"], book39["sub_book_name"]
    for chapter in book39["chapters"].items():
        chnu, ch_contents = chapter
        for pseudo_verse in ch_contents.items():
            psv_psn, psv_contents = pseudo_verse
            minirow = _MINIROW(*psv_contents)
            bscv = bk24na, sub_bkna, chnu, psv_psn
            _record_pseudo_verse(accum, bscv, minirow)
            _record_empty_col_c(accum["empty_col_c"], bscv, minirow.CP)
            cds_plus.store_the_mpasuq_call(accum["mpasuq"], bscv, minirow.CP)


def _record_empty_col_c(accum_ecc, bscv, minirow_cp):
    bscv_dic = _make_bscv_dic(bscv)
    if not minirow_cp:
        accum_ecc.append(bscv_dic)


def _make_bscv_dic(bscv_tuple):
    bk24na, sub_bkna, chnu, psv_psn = bscv_tuple
    return {"bk24na": bk24na, "sub_bkna": sub_bkna, "chnu": chnu, "psv_psn": psv_psn}


def _do_a_book24(bk24id, accum):
    my_utils_fm.show_progress_g(__file__, bk24id)
    folder = "../MAM-parsed/plus"
    osdf24 = tbn.ordered_short_dash_full_24(bk24id)
    in_path = f"{folder}/{osdf24}.json"
    with open(in_path, encoding="utf-8") as json_in_fp:
        bk24_contents = json.load(json_in_fp)
    for book39 in bk24_contents["book39s"]:
        _do_a_book39(book39, accum)


def survey():
    """Survey the use of templates in MAM plus. Return the result dict."""
    accum = {
        "mpasuq": [],
        "naked_sam2_pe2_pe3": [],
        "empty_col_c": [],
        "column_counts": collections.defaultdict(int),
        "stack_counts": collections.defaultdict(int),
        "arg_counts": collections.defaultdict(int),
    }
    for bk24id in tbn.ALL_BK24_IDS:
        _do_a_book24(bk24id, accum)
    return {
        "mpasuq": cdp.process_all_mpasuq_calls(accum["mpasuq"]),
        "naked_sam2_pe2_pe3": accum["naked_sam2_pe2_pe3"],
        "empty_col_c": accum["empty_col_c"],
        "column_counts": _flatten_col_counts(accum),
        "stack_counts": _flatten_stack_counts(accum),
        "arg_counts": _flatten_arg_counts(accum),
    }
