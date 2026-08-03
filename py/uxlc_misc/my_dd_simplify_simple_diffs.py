"""Exports qcp_make, qcp_get, qualify_code_points, simplify_simple_diffs"""

import re


def qcp_make(code_point, letter, count):
    """Make a QCP ([letter-]qualified code-point)"""
    return code_point, letter, count


def qcp_get(qcp, key):
    """Get the keyed value from a QCP"""
    key_to_idx_dic = {"code_point": 0, "letter": 1, "count": 2}
    idx = key_to_idx_dic[key]
    return qcp[idx]


def qualify_code_points(string):
    """Qualify non-letter code points with the letter that precedes them"""
    letter = None
    out = []
    letter_counts = {}
    for code_point in string:
        if re.match("[א-ת]", code_point):
            letter = code_point
            _init_to_1_or_add_1(letter_counts, letter)
            out.append(_qcp_make_tmp(code_point, letter, letter_counts))
        else:
            # Here we used to
            # assert letter is not None
            # But
            # letter can be None for a string of a lone vowel point or accent
            out.append(_qcp_make_tmp(code_point, letter, letter_counts))
    out2 = tuple(_add_total(out_el, letter_counts) for out_el in out)
    return out2


def simplify_simple_diffs(diffs):
    """Present the diffs in English, if possible.
    Returns a pair with the following contents:
    Element 1 of the pair is a string describing the diff in detail.
    Element 2 of the pair is a string describing the category, i.e. the kind of diff.
    E.g.:
        add merkha to bet
        add merkha to bet-2
        remove tipeḥa from gimel
        on dalet, replace darga with meteg
        move pazer forward from bet to shin
    """
    diff_types = tuple(map(_diff_type, diffs))
    handlers = {
        ("dt_replace",): _ssd1_dt_replace,
        ("dt_add",): _ssd1_dt_add,
        ("dt_remove",): _ssd1_dt_remove,
        ("dt_add", "dt_remove"): _ssd2_dt_add_dt_remove,
        ("dt_remove", "dt_add"): _ssd2_dt_remove_dt_add,
    }
    handler = handlers.get(diff_types)
    desc = handler and handler(*diffs)
    return desc or (str(diffs), None)


def _qcp_cp_and_lwc(qcp):  # lwc: letter with count
    letter = qcp_get(qcp, "letter")
    count = qcp_get(qcp, "count")
    if count == (None, None):  # simple case: 1 of 1
        # letter can be None for a string of a lone vowel point or accent
        lwc = "no letter"
    elif count == (1, 1):  # simple case: 1 of 1
        lwc = letter
    else:
        ordinals = {
            1: "first",
            2: "second",
            3: "third",
        }
        ordinal = ordinals[count[0]]
        lwc = f"the {ordinal} {letter}"
    return qcp_get(qcp, "code_point"), lwc


def _qcp_make_tmp(code_point, letter, letter_counts_so_far):
    # letter can be None for a string of a lone vowel point or accent
    letter_count_so_far = letter and letter_counts_so_far[letter]
    return qcp_make(code_point, letter, letter_count_so_far)


def _add_total(qcp, letter_counts):
    code_point = qcp_get(qcp, "code_point")
    letter = qcp_get(qcp, "letter")
    this_num = qcp_get(qcp, "count")
    # letter can be None for a string of a lone vowel point or accent
    tot_num = letter and letter_counts[letter]
    n_of_m = this_num, tot_num
    return qcp_make(code_point, letter, n_of_m)


def _init_to_1_or_add_1(dic, key):
    if key in dic:
        dic[key] += 1
        return
    dic[key] = 1


def _ssd1_dt_replace(diff0):
    d0a = diff0[0]
    add = diff0[1]
    if not (len(d0a) == 1 and len(add) == 1):
        return None
    d0a0 = d0a[0]
    add0 = add[0]
    d0a0_cp, d0a0_lett = _qcp_cp_and_lwc(d0a0)
    add0_cp, add0_lett = _qcp_cp_and_lwc(add0)
    assert d0a0_lett == add0_lett
    lett = d0a0_lett
    detail = f"on {lett}, replace {d0a0_cp} with {add0_cp}"
    return detail, "replace"


def _ssd1_dt_add(diff0):
    add = diff0[1]
    if len(add) != 1:
        return None
    add0 = add[0]
    add0_cp, add0_lett = _qcp_cp_and_lwc(add0)
    category = "add varika" if add0_cp == "varika" else "add non-varika"
    return f"add {add0_cp} to {add0_lett}", category


def _ssd1_dt_remove(diff0):
    d0a = diff0[0]
    if len(d0a) != 1:
        return None
    d0a0 = d0a[0]
    d0a0_cp, d0a0_lett = _qcp_cp_and_lwc(d0a0)
    return f"remove {d0a0_cp} from {d0a0_lett}", "remove"


def _ssd2_dt_add_dt_remove(diff0, diff1):
    add = diff0[1]
    rem = diff1[0]
    if not (len(add) == 1 and len(rem) == 1):
        return None
    add0 = add[0]
    add0_cp, add0_lett = _qcp_cp_and_lwc(add0)
    rem0 = rem[0]
    rem0_cp, rem0_lett = _qcp_cp_and_lwc(rem0)
    if add0_cp != rem0_cp:
        return None
    ltl = "from " + rem0_lett + " to " + add0_lett
    return "move " + add0_cp + " back " + ltl, "move"


def _ssd2_dt_remove_dt_add(diff0, diff1):
    rem = diff0[0]
    add = diff1[1]
    if not (len(add) == 1 and len(rem) == 1):
        return None
    add0 = add[0]
    add0_cp, add0_lett = _qcp_cp_and_lwc(add0)
    rem0 = rem[0]
    rem0_cp, rem0_lett = _qcp_cp_and_lwc(rem0)
    if add0_cp != rem0_cp:
        return None
    ltl = "from " + rem0_lett + " to " + add0_lett
    return "move " + add0_cp + " forward " + ltl, "move"


def _diff_type(diff):
    aside, bside = diff
    noneness = aside is None, bside is None
    dic = {
        (False, False): "dt_replace",
        (True, False): "dt_add",
        (False, True): "dt_remove",
    }
    return dic[noneness]
