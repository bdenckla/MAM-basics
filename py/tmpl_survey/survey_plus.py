"""Survey Wikisource template usage patterns in MAM-parsed-plus data."""

import json
import collections

from tmpl_survey import column_d_0_process_all_mpasuq_calls as cdp
from tmpl_survey import column_d_0_store_the_mpasuq_call_plus as cds_plus
from tmpl_survey import nesting_normal_form
from mb_cmn import bib_locales as tbn
from mb_misc import my_utils_for_mainish as my_utils_fm
from mb_cmn import ws_tmpl2 as wtp2
from mb_cmn import kq_special_templates as kqst

_MINIROW = collections.namedtuple("_MINIROW", "CP, DP, EP")
_NUSACH_ARG2_CONTEXT = ("נוסח", "2")
_NON_TARGETED_SCROLL_DIFF_NOTE_TMPL = "מ:הערה"
_NUSACH_SLOTS = {"1", "2"}
_NUSACH_TEMPLATE_SYMBOL = "נוסח"
_NUSACH_SYMBOL_BY_SLOT = {
    "1": "נוסח@1",
    "2": "נוסח@2",
}


def _wtel_type_and_subtype(wtel):
    assert wtp2.is_template(wtel), wtel
    tmpl_name = wtp2.template_name(wtel)
    return "tmpl", _survey_tmpl_subtype(tmpl_name, wtel)


def _survey_tmpl_subtype(tmpl_name, tmpl):
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
    stack_top = wtel_subtype
    stack_rest = _stack_rest_from_stack(stack)
    _my_plus_equals(accum["stack_counts"], stack_top, stack_rest)
    argc = wtp2.template_len(wtel) - 1
    _check_argc(wtel_subtype, argc)
    _my_plus_equals(accum["arg_counts"], wtel_subtype, argc)
    for param_key in wtp2.template_param_keys(wtel):
        new_stack = *stack, *_child_stack_symbols(wtel_subtype, param_key)
        arg = wtp2.template_param_val(wtel, param_key)
        for arg_wtel in arg:
            if _record_parent_context(accum, wtel_subtype, param_key, arg_wtel):
                accum["tmpl_has_tmpl_children"][wtel_subtype] = True
            arg_wtel_rec = bscv, new_stack, arg_wtel
            _record_wtel(accum, arg_wtel_rec)


def _child_stack_symbols(parent_subtype, arg_key):
    if parent_subtype != _NUSACH_TEMPLATE_SYMBOL:
        return (parent_subtype,)
    return (_NUSACH_TEMPLATE_SYMBOL, _child_stack_symbol(parent_subtype, arg_key))


def _child_stack_symbol(parent_subtype, arg_key):
    if parent_subtype != _NUSACH_TEMPLATE_SYMBOL:
        return parent_subtype
    slot = str(arg_key)
    assert slot in _NUSACH_SLOTS, (
        f"Unexpected נוסח arg slot {slot!r}; expected one of {sorted(_NUSACH_SLOTS)}"
    )
    return _NUSACH_SYMBOL_BY_SLOT[slot]


def _record_parent_context(accum, parent_subtype, param_key, arg_wtel):
    if isinstance(arg_wtel, str):
        return False
    assert isinstance(arg_wtel, dict)
    wtel_type, child_subtype = _wtel_type_and_subtype(arg_wtel)
    if wtel_type != "tmpl":
        return False
    accum["tmpl_parent_contexts"][child_subtype].add((parent_subtype, str(param_key)))
    return True


def _nusach_arg2_only_leaf_templates(accum):
    return {
        tmpl
        for tmpl, contexts in accum["tmpl_parent_contexts"].items()
        if contexts == {_NUSACH_ARG2_CONTEXT}
        and not accum["tmpl_has_tmpl_children"][tmpl]
    }


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
        return (argc_expectation,)
    return argc_expectation


def _check_argc(wtel_subtype, argc):
    exp = _EXPECTED_ARGC.get(wtel_subtype)
    assert exp is None or argc in _handle_int(exp)


def _assert_plus_excludes_non_targeted_scroll_diff_notes(stack_counts):
    for stack_top, stack_rest in stack_counts:
        # We assert this invariant because deep discard was removed from
        # survey_dot, where it was previously needed to suppress מ:הערה chains.
        assert (
            stack_top != _NON_TARGETED_SCROLL_DIFF_NOTE_TMPL
        ), f"Unexpected {_NON_TARGETED_SCROLL_DIFF_NOTE_TMPL} as plus subtype"
        assert _NON_TARGETED_SCROLL_DIFF_NOTE_TMPL not in stack_rest.split("/"), (
            "Unexpected "
            f"{_NON_TARGETED_SCROLL_DIFF_NOTE_TMPL} in plus stack: {stack_rest}"
        )


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
        wtel_type, wtel_subtype, column_letter = key
        group_key = (wtel_type, wtel_subtype)
        if group_key not in grouped:
            grouped[group_key] = {
                "wtel_type": wtel_type,
                "wtel_subtype": wtel_subtype,
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


def _do_a_book39(book39, accum):
    bk24na, sub_bkna = book39["book24_name"], book39["sub_book_name"]
    for chapter in book39["chapters"].items():
        chnu, ch_contents = chapter
        for pseudo_verse in ch_contents.items():
            psv_psn, psv_contents = pseudo_verse
            minirow = _MINIROW(*psv_contents)
            bscv = bk24na, sub_bkna, chnu, psv_psn
            _record_pseudo_verse(accum, bscv, minirow)
            cds_plus.store_the_mpasuq_call(accum["mpasuq"], bscv, minirow.DP)


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


def survey(plain_mpasuq, case_rank_maps):
    """Survey the use of templates in MAM plus.

    Returns (result_dict, raw_stack_counts, nusach_arg2_only_leaf_templates).
    """
    accum = {
        "mpasuq": [],
        "naked_sam2_pe2_pe3": [],
        "column_counts": collections.defaultdict(int),
        "stack_counts": collections.defaultdict(int),
        "arg_counts": collections.defaultdict(int),
        "tmpl_parent_contexts": collections.defaultdict(set),
        "tmpl_has_tmpl_children": collections.defaultdict(bool),
    }
    for bk24id in tbn.ALL_BK24_IDS:
        _do_a_book24(bk24id, accum)
    _assert_plus_excludes_non_targeted_scroll_diff_notes(accum["stack_counts"])
    nesting_normal_form.assert_stack_counts_in_normal_form_by_case(
        accum["stack_counts"],
        dataset_key="plus",
        case_rank_maps=case_rank_maps,
    )
    plus_mpasuq = cdp.process_all_mpasuq_calls(accum["mpasuq"])
    result = {
        "mpasuq": _mpasuq_dedup(plus_mpasuq, plain_mpasuq),
        "naked_sam2_pe2_pe3": accum["naked_sam2_pe2_pe3"],
        "column_counts": _flatten_col_counts(accum),
        "stack_counts": _flatten_stack_counts(accum),
        "arg_counts": _flatten_arg_counts(accum),
    }
    return result, accum["stack_counts"], _nusach_arg2_only_leaf_templates(accum)


def _mpasuq_dedup(plus_mpasuq, plain_mpasuq):
    if plus_mpasuq == plain_mpasuq:
        return "same as plain"
    return plus_mpasuq
