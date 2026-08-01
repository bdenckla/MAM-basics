"""Exports compare_vyls"""

import py_wlc_json_and_unicode.wlc_uword as wlc_uword
import mb_cmn.uni_heb as uh
import mb_cmn.my_diffs as my_diffs


def compare_vyls(io_diff, bcv, vyla, vylb):
    """Compare vyla and vylb, putting result in io_diff"""
    typa, typb = _vyltype(vyla), _vyltype(vylb)
    if typa != typb:
        io_diff["type changes"].append(
            {
                "bcv": bcv,
                **_vyla_to_cells(vyla),
                **_vylb_to_cells(vylb),
            }
        )
        return
    if typa == _VYLTYPE_WN:
        if vyla["notes"] != vylb["notes"]:
            _record_notes_diff(io_diff, bcv, vyla, vylb)
        worda_ns = vyla["word"].replace("/", "")
        wordb_ns = vylb["word"].replace("/", "")
        if worda_ns != wordb_ns:
            _record_word_diff(io_diff, bcv, vyla, vylb)
        return
    assert typa == _VYLTYPE_SPI
    assert vyla == vylb


def _record_word_diff(io_diff, bcv, vyla, vylb):
    vyla, vylb = _wd_new_fields_for_two(vyla, vylb)
    io_diff["word differences"].append(_word_diff(bcv, vyla, vylb))


def _word_diff(bcv, vyla, vylb):
    worda, wordb = vyla["word"], vylb["word"]
    diffs = my_diffs.get(_ensh(worda), _ensh(wordb))
    return {
        "bcv": bcv,
        "diff_type": _WORD_DIFF_TYPE[vyla["notes"] != vylb["notes"]],
        "diffs": _slim(diffs),
        "ab_word": _newline_sep(vyla, vylb, "word"),
        "ab_notes": _newline_sep(vyla, vylb, "cnotes"),
    }


def _ensh(word):
    return list(enumerate(uh.t_shunnas(word)))


def _slim(diffs):
    if len(diffs) != 1:
        return None
    diffs0 = diffs[0]
    assert len(diffs0) == 2
    aside, bside = diffs0[0], diffs0[1]
    # E.g.
    # aside == [(5, '(zaq_q)'), (6, 'HMA UPPER DOT')]
    # bside == [(5, 'HMA UPPER DOT'), (6, '(zaq_q)')]
    if not len(aside) == len(bside) == 2:
        return None
    aside_idxs = aside[0][0], aside[1][0]
    bside_idxs = bside[0][0], bside[1][0]
    if not aside_idxs == bside_idxs:
        return None
    aside_vals = aside[0][1], aside[1][1]
    bside_vals = bside[0][1], bside[1][1]
    if aside_vals[0] != bside_vals[1]:
        return None
    if aside_vals[1] != bside_vals[0]:
        return None
    return f"swap {aside_vals}"


def _wd_new_fields_for_two(vyla, vylb):
    return _wd_new_fields_for_one(vyla), _wd_new_fields_for_one(vylb)


def _wd_new_fields_for_one(vylx):
    return {
        **vylx,
        "cnotes": "".join(vylx["notes"]),
        "uword": wlc_uword.uword(vylx["word"]),
    }


def _newline_sep(dica, dicb, key):
    return dica[key] + "\n" + dicb[key]


def _record_notes_diff(io_diff, bcv, vyla, vylb):
    io_diff["notes differences"].append(_notes_diff(bcv, vyla, vylb))


def _notes_diff(bcv, vyla, vylb):
    vyla, vylb = _nd_new_fields_for_two(vyla, vylb)
    change = " → ".join((vyla["cnotes"] or "∅", vylb["cnotes"] or "∅"))
    change_cat = _NC_CATEGORIES.get(change)
    if change_cat is None:
        print(f"Warning: No category for notes change {change}")
    return {
        "bcv": bcv,
        "diff_type": _NOTES_DIFF_TYPE[vyla["nsword"] != vylb["nsword"]],
        "ab_word": _newline_sep(vyla, vylb, "word"),
        "ab_notes": _newline_sep(vyla, vylb, "cnotes"),
        "change": change,
        "change_category": change_cat,
        **_set_differences(vyla["notes"], vylb["notes"]),
    }


def _nd_new_fields_for_two(vyla, vylb):
    return _nd_new_fields_for_one(vyla), _nd_new_fields_for_one(vylb)


def _nd_new_fields_for_one(vylx):
    return {
        **vylx,
        "cnotes": "".join(vylx["notes"]),
        "nsword": vylx["word"].replace("/", ""),
    }


def _set_differences(notesa, notesb):
    seta = set(notesa)
    setb = set(notesb)
    b_minus_a = setb - seta
    a_minus_b = seta - setb
    bma_sorted_list = sorted(list(b_minus_a))
    amb_sorted_list = sorted(list(a_minus_b))
    bma_str = "".join(bma_sorted_list)
    amb_str = "".join(amb_sorted_list)
    return {"b-a": bma_str, "a-b": amb_str}


def _vyla_to_cells(vyla):
    return _vyl_to_cells(vyla, "vela_type", "vela_0", "vela_1")


def _vylb_to_cells(vylb):
    return _vyl_to_cells(vylb, "velb_type", "velb_0", "velb_1")


def _vyl_to_cells(vyl, typlbl, lbl0, lbl1):
    vyltype = _vyltype(vyl)
    if vyltype == _VYLTYPE_WN:
        datacells = vyl["word"], "".join(vyl["notes"])
    elif vyltype == _VYLTYPE_SPI:
        datacells = vyl["sam_pe_inun"], ""
    elif vyltype == _VYLTYPE_NONE:
        datacells = "", ""
    else:
        assert False
    return {typlbl: vyltype, lbl0: datacells[0], lbl1: datacells[1]}


def _vyltype(vyl):
    if vyl is None:
        return _VYLTYPE_NONE
    assert isinstance(vyl, dict)
    keys = tuple(vyl.keys())
    if keys == ("word", "notes"):
        return _VYLTYPE_WN
    if keys == ("sam_pe_inun",):
        return _VYLTYPE_SPI
    assert False


_VYLTYPE_NONE = "vyltype-∅"
_VYLTYPE_WN = "vyltype-wn"
_VYLTYPE_SPI = "vyltype-sam_pe_inun"

_NC_CATEGORIES = {
    # Below are categories of note changes on unchanged words.
    # nc: named category, i.e. not "other" (misc.)
    "∅ → ]1": "nc + ]1",
    "∅ → ]1]P": "nc + ]1",
    "∅ → ]c]p": "nc + ]p",
    "∅ → ]e": "nc + ]e",
    "∅ → ]p": "nc + ]p",
    "∅ → ]Q]n]p": "nc + ]p",
    "∅ → ]U": "nc + ]U",
    "∅ → ]w": "nc + ]w",
    "]1 → ∅": "other ]1 → ∅",
    "]1 → ]C]U": "nc .*]1.* → .*]U.*",
    "]1 → ]s": "nc ]1/]U → ]s/]S]s",
    "]1 → ]S]s": "nc ]1/]U → ]s/]S]s",
    "]1 → ]U": "nc .*]1.* → .*]U.*",
    "]1]a → ]U]a": "nc .*]1.* → .*]U.*",
    "]c → ∅": "other ]c → ∅",
    "]c → ]C]c": "other ]c → ]C]c",
    "]c → ]C]P]c": "other ]c → ]C]P]c",
    "]c]p → ]C]P]c]p": "other ]c]p → ]C]P]c]p",
    "]k → ]Q]k": "other ]k → ]Q]k",
    "]p → ]n]p": "other ]p → ]n]p",
    "]q → ]Q]n]q": "other ]q → ]Q]n]q",
    "]q → ]Q]q": "other ]q → ]Q]q",
    "]Q]c → ]Q]c]e": "nc + ]e",
    "]U → ]S]s": "nc ]1/]U → ]s/]S]s",
    "]v → ∅": "other ]v → ∅",
    "]v → ]Q]v": "other ]v → ]Q]v",
    #
    # Below are categories of note changes that appear only on changed words.
    "∅ → ]c": "other ∅ → ]c",
    "∅ → ]C]c": "other ∅ → ]C]c",
    "∅ → ]P]p": "other ∅ → ]P]p",
    "∅ → ]Q]c": "other ∅ → ]Q]c",
    "∅ → ]Q]c]n": "other ∅ → ]Q]c]n",
    "∅ → ]Q]n]v": "other ∅ → ]Q]n]v",
    "∅ → ]v": "other ∅ → ]v",
    "]1 → ]Q]p": "other ]1 → ]Q]p",
    "]1 → ]Q]U]v": "other ]1 → ]Q]U]v",
    "]n]p → ∅": "other ]n]p → ∅",
    "]p → ∅": "other ]p → ∅",
    "]p → ]1": "other ]p → ]1",
    "]P]p]v → ]Q]n]v": "other ]P]p]v → ]Q]n]v",
}
_WORD_DIFF_TYPE = {
    False: "word changed but notes did not",
    True: "word changed and notes changed",
}
_NOTES_DIFF_TYPE = {
    False: "notes changed but word did not",
    True: "notes changed and word changed",
}
