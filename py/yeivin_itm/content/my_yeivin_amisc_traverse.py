import mb_cmn.my_utils as my_utils
import py_html.legacy_html as aht_html


def find_refs_to_numsecs(tocsec):
    return traverse_tocsec(_HANDLERS_FOR_FIND_REFS_TO_NUMSECS, tocsec)


def find_nums_of_numsecs(tocsec):
    return traverse_tocsec(_HANDLERS_FOR_FIND_NUMS_OF_NUMSECS, tocsec)


def traverse_tocsec(handlers, tocsec):
    handler_for_tose_h = handlers["trav-handler-for-tocsec-heading"]
    tose_h = tocsec["tocsec-heading"]
    numsecs_before_titsecs = tocsec["tocsec-numsecs-before-titsecs"]
    numsecs_after_titsecs = tocsec.get("tocsec-numsecs-after-titsecs") or {}
    titsecs = tocsec["tocsec-titsecs"]
    return [
        *handler_for_tose_h(tose_h),
        *_traverse_numsecs(handlers, numsecs_before_titsecs),
        *_traverse_titsecs(handlers, titsecs),
        *_traverse_numsecs(handlers, numsecs_after_titsecs),
    ]


def ptraverse_tocsec(handlers, tocsec):
    true_handlers = dict(handlers)
    true_handlers["tocsec-numsecs-before-titsecs"] = _ptraverse_numsecs
    true_handlers["tocsec-titsecs"] = _ptraverse_titsecs
    true_handlers["titsec-numsecs"] = _ptraverse_numsecs
    return {kv[0]: _call_handler(true_handlers, kv) for kv in tocsec.items()}


def _call_handler(handlers, key_and_val):
    key, val = key_and_val
    handler = handlers.get(key)
    if handler:
        return handler(handlers, val)
    return val


def traverse_html(tag_handlers, obj):
    if isinstance(obj, (list, tuple)):
        recursion_results = my_utils.sl_map((traverse_html, tag_handlers), obj)
        return my_utils.sum_of_seqs(recursion_results)
    if aht_html.is_htel(obj):
        tag = aht_html.htel_deref_tag(obj)
        if handler := tag_handlers.get(tag):
            return handler(obj)
        if contents := obj.get("contents"):
            return traverse_html(tag_handlers, contents)
        return []
    if isinstance(obj, str):
        return []
    assert False, obj


############################################################


def _traverse_numsecs(handlers, numsecs):
    handler_for_nsi = handlers["trav-handler-for-numsec-item"]
    list_of_lists = list(map(handler_for_nsi, numsecs.items()))
    return my_utils.sum_of_seqs(list_of_lists)


def _ptraverse_numsecs(handlers, numsecs):
    handler_for_nsi = handlers["ptrav-handler-for-numsec-item"]
    new_numsec_values = list(map(handler_for_nsi, numsecs.items()))
    return dict(zip(numsecs.keys(), new_numsec_values))


def _traverse_titsecs(handlers, titsecs):
    list_of_lists = my_utils.sl_map((_traverse_titsec, handlers), titsecs)
    return my_utils.sum_of_seqs(list_of_lists)


def _ptraverse_titsecs(handlers, titsecs):
    return my_utils.sl_map((_ptraverse_titsec, handlers), titsecs)


def _traverse_titsec(handlers, titsec):
    handler_for_tise_h = handlers["trav-handler-for-titsec-heading"]
    tise_h = titsec["titsec-heading"]
    numsecs = titsec["titsec-numsecs"]
    return [
        *handler_for_tise_h(tise_h),
        *_traverse_numsecs(handlers, numsecs),
    ]


def _ptraverse_titsec(handlers, titsec):
    return {kv[0]: _call_handler(handlers, kv) for kv in titsec.items()}


############################################################


def _trvhnd_find_nums_of_numsecs_in_nsi(numsec_item):
    num_of_sec = numsec_item[0]
    return [num_of_sec]


def _trvhnd_find_refs_to_numsecs_in_nsi(numsec_item):
    html_contents_of_sec = numsec_item[1]
    return traverse_html(_TAG_HANDLERS_FOR_FIND_RTN, html_contents_of_sec)


############################################################


def _find_rtn_in_anchor(htel):
    # rtn: references to numsecs
    if dnos_str := htel["attr"].get("data-num-of-sec"):
        return [int(dnos_str)]
    return []


_HANDLERS_FOR_FIND_NUMS_OF_NUMSECS = {
    "trav-handler-for-tocsec-heading": lambda x: [],
    "trav-handler-for-titsec-heading": lambda x: [],
    "trav-handler-for-numsec-item": _trvhnd_find_nums_of_numsecs_in_nsi,
}
_HANDLERS_FOR_FIND_REFS_TO_NUMSECS = {
    "trav-handler-for-tocsec-heading": lambda x: [],
    "trav-handler-for-titsec-heading": lambda x: [],
    "trav-handler-for-numsec-item": _trvhnd_find_refs_to_numsecs_in_nsi,
}
_TAG_HANDLERS_FOR_FIND_RTN = {
    "a": _find_rtn_in_anchor,
}
