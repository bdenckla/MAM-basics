"""Survey Wikisource template usage patterns in MAM-parsed plain data."""

import json
import collections

from tmpl_survey import column_d_0_process_all_mpasuq_calls as cdp
from tmpl_survey import column_d_0_store_the_mpasuq_call as cds
from tmpl_survey import nesting_normal_form
from mb_cmn import bib_locales as tbn
from mb_misc import my_utils_for_mainish as my_utils_fm
from mb_cmn import ws_tmpl1 as wtp1
from mb_cmn import kq_special_templates as kqst

_MINIROW = collections.namedtuple("_MINIROW", "CP, DP, EP")
_PSV_PSN_CATEGORIES = {"0": "0 (pre-chapter)", str("תתת"): "2 (post-chapter)"}
_DOCNOTE_ARG2_CONTEXT = ("נוסח", "2")
_DOCNOTE_SLOTS = {"1", "2"}
_DOCNOTE_TEMPLATE_SYMBOL = "נוסח"
_DOCNOTE_SYMBOL_BY_SLOT = {
    "1": "נוסח@1",
    "2": "נוסח@2",
}


def _psv_category(bscv):
    psv_psn = bscv["psv_psn"]
    return _PSV_PSN_CATEGORIES.get(psv_psn) or "1 (normal verse)"


def _wtel_type_and_subtype(wtel):
    if wtp1.is_template(wtel):
        # template_name() intentionally normalizes ASCII quote shorthand to
        # gershayim, and this applies to both stmpl and tmpl template forms.
        tmpl_name = wtp1.template_name(wtel)
        return "tmpl", _survey_tmpl_subtype(tmpl_name, wtel)
    if wtp1.is_abtag(wtel):
        return "custom_tag", wtel["custom_tag"]
    assert False, wtel


def _survey_tmpl_subtype(tmpl_name, tmpl1):
    if not kqst.is_special_kq_template_name(tmpl_name):
        return tmpl_name
    assert kqst.is_unified_special_kq_template_name(tmpl_name), tmpl_name
    # For survey outputs, reflect the actual template node in the data.
    return tmpl_name


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
    stack_top = wtel_subtype
    stack_rest = _stack_rest_from_stack(stack)
    _my_plus_equals(accum["stack_counts"], stack_top, stack_rest)
    argc = wtp1.template_len(wtel) - 1
    _check_argc(wtel_subtype, argc)
    _my_plus_equals(accum["arg_counts"], wtel_subtype, argc)
    for arg_idx, arg in enumerate(wtp1.template_arguments(wtel), start=1):
        new_stack = *stack, *_child_stack_symbols(wtel_subtype, arg_idx)
        # e.g. for a, b, c in {{f|a|b|c}}
        for arg_wtel in arg:
            if _record_parent_context(accum, wtel_subtype, arg_idx, arg_wtel):
                accum["tmpl_has_tmpl_children"][wtel_subtype] = True
            arg_wtel_rec = bscv, new_stack, arg_wtel
            _record_wtel(accum, arg_wtel_rec)


def _child_stack_symbols(parent_subtype, arg_key):
    if parent_subtype != _DOCNOTE_TEMPLATE_SYMBOL:
        return (parent_subtype,)
    return (_DOCNOTE_TEMPLATE_SYMBOL, _child_stack_symbol(parent_subtype, arg_key))


def _child_stack_symbol(parent_subtype, arg_key):
    if parent_subtype != _DOCNOTE_TEMPLATE_SYMBOL:
        return parent_subtype
    slot = str(arg_key)
    assert (
        slot in _DOCNOTE_SLOTS
    ), f"Unexpected נוסח arg slot {slot!r}; expected one of {sorted(_DOCNOTE_SLOTS)}"
    return _DOCNOTE_SYMBOL_BY_SLOT[slot]


def _record_parent_context(accum, parent_subtype, arg_key, arg_wtel):
    if isinstance(arg_wtel, str):
        return False
    assert isinstance(arg_wtel, dict)
    wtel_type, child_subtype = _wtel_type_and_subtype(arg_wtel)
    if wtel_type != "tmpl":
        return False
    accum["tmpl_parent_contexts"][child_subtype].add((parent_subtype, str(arg_key)))
    return True


def _stack_rest_from_stack(stack):
    return "/".join(stack)


def _my_plus_equals(accum_x, *key_parts):
    accum_x[key_parts] += 1


_EXPECTED_ARGC = {
    str("כו״ק"): 2,
    str("מ:אות מנוקדת"): 1,
    kqst.UNIFIED_SPECIAL_KQ_TEMPLATE_NAME: tuple((2, 3, 4, 5, 6)),
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
    grouped = {}
    for key, count in dic.items():
        wtel_type, wtel_subtype, pseudoverse_category, column_letter = key
        group_key = (wtel_type, wtel_subtype, pseudoverse_category)
        if group_key not in grouped:
            grouped[group_key] = {
                "wtel_type": wtel_type,
                "wtel_subtype": wtel_subtype,
                "pseudoverse_category": pseudoverse_category,
                "count_C": 0,
                "count_D": 0,
                "count_E": 0,
            }
        grouped[group_key][f"count_{column_letter}"] = count
    return _sort_dics_by_values(list(grouped.values()))


def _sort_dics_by_values(dics):
    return sorted(dics, key=_keyfn)


def _keyfn(dic):
    return tuple(dic.values())


def _flatten_stack_counts(accum):
    stacks_to_counts = accum["stack_counts"]
    stack_count_dics = map(_stack_count_dic, stacks_to_counts.items())
    return _sort_dics_by_values(list(stack_count_dics))


def _stack_count_dic(stack_and_count):
    stack_top, stack_rest = stack_and_count[0]
    count = stack_and_count[1]
    return {
        "stack": f"{stack_rest}/{stack_top}",
        "count": count,
    }


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


def survey(case_rank_maps):
    """Survey the use of templates in MAM plain.

    Returns (result_dict, raw_stack_counts, docnote_arg2_only_leaf_templates).
    """
    accum = {
        "mpasuq": [],
        "naked_sam2_pe2_pe3": [],
        "empty_col_c": [],
        "column_counts": collections.defaultdict(int),
        "stack_counts": collections.defaultdict(int),
        "arg_counts": collections.defaultdict(int),
        "tmpl_parent_contexts": collections.defaultdict(set),
        "tmpl_has_tmpl_children": collections.defaultdict(bool),
    }
    for bk24id in tbn.ALL_BK24_IDS:
        _do_a_book24(bk24id, accum)
    nesting_normal_form.assert_stack_counts_in_normal_form_by_case(
        accum["stack_counts"],
        dataset_key="plain",
        case_rank_maps=case_rank_maps,
    )
    result = {
        "mpasuq": cdp.process_all_mpasuq_calls(accum["mpasuq"]),
        "naked_sam2_pe2_pe3": accum["naked_sam2_pe2_pe3"],
        "empty_col_c": accum["empty_col_c"],
        "column_counts": _flatten_col_counts(accum),
        "stack_counts": _flatten_stack_counts(accum),
        "arg_counts": _flatten_arg_counts(accum),
    }
    return result, accum["stack_counts"]
