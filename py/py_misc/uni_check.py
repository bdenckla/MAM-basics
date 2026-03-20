"""Exports check"""

import itertools

from pycmn import uni_denorm as ud
from pycmn import uni_heb as uh
from pycmn import uni_norm_fragile as unf


def check(obj):
    """Check that the Unicode has standard mark order and is not fragile."""
    if isinstance(obj, str):
        _check_unicode_in_str(obj)
        return
    if isinstance(obj, (tuple, list)):
        for elem in obj:
            check(elem)
        return
    if isinstance(obj, dict):
        for elem in obj.values():
            check(elem)
        return
    assert False


def _check_unicode_in_str(string):
    if not ud.has_std_mark_order(string):
        _print_non_std_mark_order(string)
        assert False
    assert not unf.is_fragile(string), f"{string} is fragile!"


def _print_non_std_mark_order(string):
    parts = string.split(" ")
    parts_ns = tuple(itertools.filterfalse(ud.has_std_mark_order, parts))
    parts_nsf = tuple(map(_ns_and_fixed, parts_ns))
    parts_nsfs = tuple(map(_pair_with_shunna, parts_nsf))
    msg = f"The following {len(parts_nsfs)} have nonstandard mark order:"
    print(msg, flush=True)
    for part_nsfs in parts_nsfs:
        _print_dic(part_nsfs)


def _print_dic(dic):
    for key, value in dic.items():
        print(f"{key}: {value}", flush=True)


def _pair_with_shunna(dic):
    return {k: (v, uh.join_shunnas(v)) for k, v in dic.items()}


def _ns_and_fixed(nonstd):
    return {"nonstd": nonstd, "fixed": ud.give_std_mark_order(nonstd)}
