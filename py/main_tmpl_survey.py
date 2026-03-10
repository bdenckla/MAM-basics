"""Survey Wikisource template usage patterns across the MAM corpus and write analytics to JSON."""

import json
import collections
from itertools import starmap

from pytmpl_survey import column_d_0_process_all_mpasuq_calls as cdp
from pytmpl_survey import column_d_0_store_the_mpasuq_call as cds
from pycmn import bib_locales as tbn
from pycmn import my_utils
from pycmn import file_io
from py_misc import my_utils_for_mainish as my_utils_fm
from pycmn import ws_tmpl1 as wtp1
from pycmn import template_names as tmpln

_MINIROW = collections.namedtuple("_MINIROW", "CP, DP, EP")
_PSV_PSN_CATEGORIES = {"0": "0 (pre-chapter)", str("תתת"): "2 (post-chapter)"}


def _psv_category(bscv):
    psv_psn = bscv["psv_psn"]
    return _PSV_PSN_CATEGORIES.get(psv_psn) or "1 (normal verse)"


def _wtel_type_and_subtype(wtel):
    if wtp1.is_template(wtel):
        return "tmpl", wtp1.template_name(wtel)
    if wtp1.is_abtag(wtel):
        return "custom_tag", wtel["custom_tag"]
    assert False, wtel


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
        _psv_category(bscv),
        column_letter,
    )
    if wtel_type == "tmpl":
        _record_naked_sam2_pe2_pe3(accum, wtel_rec, wtel_subtype)
        _record_tmpl(accum, wtel_rec, wtel_subtype)


def _record_naked_sam2_pe2_pe3(accum, wtel_rec, wtel_subtype):
    bscv, stack, wtel = wtel_rec
    # Currently there are only 12 סס in col E
    # and none of them are "naked", i.e. none
    # of them are at the bottom of the stack.
    # They are all inside מ:כפול, i.e. they are all
    # on top of מ:כפול on the stack.
    if wtel_subtype in _SAM2_PE2_PE3 and stack == ("E",):
        if wtp1.template_len(wtel) == 2:
            assert wtp1.template_element(wtel, 1) == ["פסקא באמצע פסוק"]
        else:
            accum["naked_sam2_pe2_pe3"].append(bscv)


_SAM2_PE2_PE3 = {"סס", "פפ", "פפפ"}


def _record_tmpl(accum, wtel_rec, wtel_subtype):
    bscv, stack, wtel = wtel_rec
    _my_plus_equals(accum["stack_counts"], wtel_subtype, _string_from_stack(stack))
    argc = wtp1.template_len(wtel) - 1
    _check_argc(wtel_subtype, argc)
    _my_plus_equals(accum["arg_counts"], wtel_subtype, argc)
    new_stack = *stack, wtel_subtype
    for arg in wtp1.template_arguments(wtel):
        # e.g. for a, b, c in {{f|a|b|c}}
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
        return (argc_expectation,)  # tuple of length 1
    return argc_expectation


def _check_argc(wtel_subtype, argc):
    exp = _EXPECTED_ARGC.get(wtel_subtype)
    assert exp is None or argc in _handle_int(exp)


def _record_pseudo_verse(accum, bscv, minirow):
    bscv_dic = _make_bscv_dic(bscv)
    colpairs = (
        (minirow.CP, "C"),
        (minirow.DP, "D"),
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


def _flatten_stack_counts(accum):
    dic = accum["stack_counts"]
    records = list(starmap(_flatten_stack_counts_item, dic.items()))
    return _sort_dics_by_values(records)


def _flatten_col_counts_item(key, count):
    rec = {
        "wtel_type": key[0],
        "wtel_subtype": key[1],
        "pseudoverse_category": key[2],
        "column_letter": key[3],
        "count": count,
    }
    return rec


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


# psv docs
# key = psv_psn = pseudo-verse's pseudo-number (0, 1..N, תתת)
# val = psv_contents = pseudo-verse contents = 3-element list,
#       with the elements being cells C, D, & E, in parsed form.


def _do_a_book39(book39, accum):
    bk24na, sub_bkna = book39["book24_name"], book39["sub_book_name"]
    for chapter in book39["chapters"].items():
        chnu, ch_contents = chapter
        for pseudo_verse in ch_contents.items():
            psv_psn, psv_contents = pseudo_verse  # See "psv docs"
            minirow = _MINIROW(*psv_contents)
            bscv = bk24na, sub_bkna, chnu, psv_psn
            _record_pseudo_verse(accum, bscv, minirow)
            _record_empty_col_c(accum["empty_col_c"], bscv, minirow.CP)
            cds.store_the_mpasuq_call(accum["mpasuq"], bscv, minirow.DP)


def _record_empty_col_c(accum_ecc, bscv, minirow_cp):
    bscv_dic = _make_bscv_dic(bscv)
    if not minirow_cp:
        accum_ecc.append(bscv_dic)


def _make_bscv_dic(bscv_tuple):
    bk24na, sub_bkna, chnu, psv_psn = bscv_tuple
    return {"bk24na": bk24na, "sub_bkna": sub_bkna, "chnu": chnu, "psv_psn": psv_psn}


def _do_a_book24(bk24id, accum):
    my_utils_fm.show_progress_g(__file__, bk24id)
    folder = "../MAM-parsed/plain"
    osdf24 = tbn.ordered_short_dash_full_24(bk24id)
    in_path = f"{folder}/{osdf24}.json"
    with open(in_path, encoding="utf-8") as json_in_fp:
        bk24_contents = json.load(json_in_fp)
    # book39: a book in the "1 of 39" division of books
    # bk24na: a book name in the "1 of 24" division of books
    for book39 in bk24_contents["book39s"]:
        _do_a_book39(book39, accum)


def almost_main():
    """Survey the use of templates in MAM."""
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
    rflat = {
        "mpasuq": cdp.process_all_mpasuq_calls(accum["mpasuq"]),
        "naked_sam2_pe2_pe3": accum["naked_sam2_pe2_pe3"],
        "empty_col_c": accum["empty_col_c"],
        "column_counts": _flatten_col_counts(accum),
        "stack_counts": _flatten_stack_counts(accum),
        "arg_counts": _flatten_arg_counts(accum),
    }
    out_path = "out/MAM-tmpl-survey.json"
    file_io.json_dump_to_file_path(rflat, out_path)


def main():
    """Survey the use of templates in MAM."""
    almost_main()


if __name__ == "__main__":
    main()
