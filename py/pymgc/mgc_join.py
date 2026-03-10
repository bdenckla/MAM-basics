""" Exports join """


def join(multi_dic_of_diffs, multi_dic_of_cles):
    """Join multi_dics on their bcv field"""
    join_result = {
        bcv: (diffs_for_bcv, multi_dic_of_cles.get(bcv) or [])
        for bcv, diffs_for_bcv in multi_dic_of_diffs.items()
    }
    out_row_groups = tuple(map(_make_out_rows_for_bcv, join_result.values()))
    out_rows = sum(out_row_groups, [])
    return out_rows


def _make_out_row(diff, cle, num_cles=1):
    return {**diff, "num_cles": num_cles, **cle}


def _make_out_rows_for_diff(diff, cles):
    if cles:
        return [_make_out_row(diff, cle, len(cles)) for cle in cles]
    return [_make_out_row(diff, {}, 0)]


def _make_out_rows_for_bcv(diffs_and_cles):
    diffs, cles = diffs_and_cles
    if matching_rows := _try_to_match(diffs, cles):
        return matching_rows
    groups_of_rows = [_make_out_rows_for_diff(diff, cles) for diff in diffs]
    return sum(groups_of_rows, [])


def _try_to_match(diffs, cles):
    for diffi, diff in enumerate(diffs):
        if _is_varika(diff):
            outrow = _make_out_row(diff, {}, 0)
            rest_diffs = diffs[:diffi] + diffs[diffi + 1 :]
            return [outrow] + _make_out_rows_for_bcv((rest_diffs, cles))
        for cle in cles:
            if _seems_to_match(diff, cle):
                outrow = _make_out_row(diff, cle)
                rest_diffs = diffs[:diffi] + diffs[diffi + 1 :]
                return [outrow] + _make_out_rows_for_bcv((rest_diffs, cles))
    return None


def _is_varika(diff):
    refine_cat = diff["refine_cat"]
    return refine_cat == "add varika"


def _seems_to_match(diff, cle):
    diff_refine = diff["refine"]
    diff_gc = diff["gc"]
    cle_what = cle and cle["what"]
    cle_what_y_heb = cle and cle["what_y_heb"]
    if diff_refine is None or cle_what is None:
        return False
    for diff_rec, cle_rec in _DETAILED_PAIRS:
        if diff_gc and cle_what_y_heb:
            if diff_rec["refine"] in diff_refine and cle_rec["what"] in cle_what:
                if (
                    diff_rec["gc"] == diff_gc
                    and cle_rec["what_y_heb"] == cle_what_y_heb
                ):
                    return True
    for refine_str, what_str in _REFINE_STR_AND_WHAT_STR_PAIRS:
        if refine_str in diff_refine and what_str in cle_what:
            return True
    return False


_DETAILED_PAIRS = (
    (
        {"refine": "add meteg/silluq", "gc": "בְּנֵֽי"},
        {"what": "Added meteg to", "what_y_heb": "אֶת־בְּנֵֽי־יִשְׂרָאֵ֖ל"},
    ),
    (
        {"refine": "add meteg/silluq", "gc": "תִּֽהְיֶה"},
        {"what": "Added meteg to", "what_y_heb": "תִּֽהְיֶה־לִּ֜י"},
    ),
)
_REFINE_STR_AND_WHAT_STR_PAIRS = (
    ("maqaf", "maqaph"),
    ("geresh-muqdam", "geresh muqdam"),
    ("resh-1", "indentation"),
    ("resh-2", "indentation"),
    ("resh-3", "indentation"),
    ("Added qamats variation", "Added qamaz qatan within template"),
    ("replace merkha/yored with meteg/silluq", "meteg instead of merkha"),
    ("replace mahapakh with yetiv", "Replaced accent mahpah with the accent yativ"),
    ("add telisha-qetana to shin", 'Added "stress helper" accent in "הִשָּׁ֩בְעָה֩"'),
    (
        "on gimel, replace dagesh/mapiq/shuruq-dot with rafeh",
        'Removed dagesh from ג of "מִגְֿבֽוּרָתָם֙" and added rafe in its place',
    ),
)
