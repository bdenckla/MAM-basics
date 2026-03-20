"""Exports make_comparable"""

import re
from pycmn import hebrew_punctuation as hpu
from pycmn import ws_tmpl1 as wtp1
from py_misc import hebrew_letter_words as hlw
from pydiff_mm import diff_mm_separators as seps
from pycmn.my_utils import sum_of_map
from pycmn.my_utils import sl_map


def make_comparable(obj):
    """Turn a Wikitext sequence into something more comparable"""
    return _make_comparable(None, obj)


def _make_comparable(stack_ctx, obj):
    if isinstance(obj, (tuple, list)):
        flattened = sum_of_map((_make_comparable, stack_ctx), obj)
        return _qualify_separators(flattened)
    if isinstance(obj, str):
        return _make_comparable_str(obj, stack_ctx)
    if wtp1.is_template(obj):
        return _make_comparable_tmpl(obj, stack_ctx)
    if wtp1.is_abtag(obj):
        return _make_comparable_abtag(obj, stack_ctx)
    assert False, obj


def _make_comparable_tmpl(tmpl, stack_ctx):
    tmpl_el0 = wtp1.template_element(tmpl, 0)
    tmpl_args = wtp1.template_arguments(tmpl)
    stack_label = _stack_label(tmpl_el0)
    if len(tmpl_args) == 0:
        tel0_with_sc = _give_stack_ctx(stack_ctx, stack_label)
        return [tel0_with_sc]
    stct = stack_ctx or tuple()  # sct: stack ctx, guaranteed to be a tuple (never None)
    assert isinstance(stct, tuple)
    eargs = enumerate(tmpl_args)
    return sum_of_map((_make_comparable_arg, stct, stack_label), eargs)


def _stack_label(tmpl_el0):
    if len(tmpl_el0) == 1:
        assert isinstance(tmpl_el0[0], str)
        return tmpl_el0[0]
    return str(tmpl_el0)  # ['#בלי קטע:', {'stmpl': 'שם הדף המלא'}]


def _make_comparable_arg(stack_ctx, stack_label, earg):
    arg_idx, arg = earg
    ctx1 = *stack_ctx, stack_label
    ctx2 = _label_with_argnum(ctx1, arg_idx)
    return _make_comparable(ctx2, arg)


def _label_with_argnum(stack_ctx, argidx):
    argnum = argidx + 1
    new_last = stack_ctx[-1] + ":" + str(argnum)
    return *stack_ctx[:-1], new_last


def _make_comparable_abtag(abtag, _ctx):
    val = abtag["custom_tag"]
    val_in_angle_brackets = "<" + val + ">"
    return [val_in_angle_brackets]


def _make_comparable_str(in_str, stack_ctx=None):
    strings = re.split(f"([ {hpu.MAQ}])", in_str)
    if strings[0] == "":
        strings = strings[1:]
    if strings and strings[-1] == "":
        strings = strings[:-1]
    strings_and_separators = strings
    return sl_map((_give_stack_ctx, stack_ctx), strings_and_separators)


def _qualify_separators(elements):
    trailing = None, None
    accum = []
    for elem in elements:
        if trailing[-1] in seps.SEPARATORS:
            lett_trn2 = _my_letters(trailing[-2])
            if lett_trn2 is not None:
                lett_elem = _my_letters(elem)
                if lett_elem is not None:
                    accum[-1] = trailing[-1], lett_trn2, lett_elem
        accum.append(elem)
        trailing = trailing[-1], elem
    return accum


def _my_letters(elem):
    if isinstance(elem, str):
        return hlw.letters_and_maqafs(elem)
    if qamats_var_arg_1 := _triple_yod(elem, "מ:קמץ:1"):
        dalet = _strip_prefix("ד=", qamats_var_arg_1)
        return hlw.letters_and_maqafs(dalet)
    if qamats_var_arg_2 := _triple_yod(elem, "מ:קמץ:2"):
        # maqaf compound inside מ:קמץ template can result in
        # no expected prefix
        samekh = _maybe_strip_prefix("ס=", qamats_var_arg_2)
        return hlw.letters_and_maqafs(samekh)
    return None


def _strip_prefix(prefix, string):
    assert string.startswith(prefix)
    return string[len(prefix) :]


def _maybe_strip_prefix(prefix, string):
    if string.startswith(prefix):
        return string[len(prefix) :]
    return string


def _triple_yod(siden, argspec):
    if not isinstance(siden, tuple):
        return None
    if siden[0] != "ייי":
        return None
    if siden[2] == (argspec,):
        return siden[1]
    return None


def _give_stack_ctx(stack_ctx, obj):
    return ("ייי", obj, stack_ctx) if stack_ctx else obj
