import itertools
import re


def _int_default_zero(x):
    return 0 if x is None else int(x)


_SOE_KEYS = (  # SOE: shaper output element, e.g. tav=4+1026 or zaqefqatan=0@592,0+0
    ("glyph", str),
    ("index_of_base", int),
    ("relposx", _int_default_zero),
    ("relposy", _int_default_zero),
    ("advance", int),
)
_SOE_PATC = re.compile(
    r"([A-Za-z0-9._-]+)"
    + "="
    + r"([0-9]+)"
    + r"(?:@(-?[0-9]+),(-?[0-9]+))?"
    + "[+]"
    + r"([0-9]+)"
)


def _parse_soe(
    soe_str,
):  # soe: shaper output element (glyph name plus various coordinates)
    # Example input: tav=4+1026 or zaqefqatan=0@592,0+0
    groups = _SOE_PATC.match(soe_str).groups()
    assert len(groups) == len(_SOE_KEYS)
    return {kstr: kfn(v) for (kstr, kfn), v in zip(_SOE_KEYS, groups)}


def _parse_shaper_output(s):
    # Example input: tav=4+1026|vavxolam=2+484|zaqefqatan=0@592,0+0|alef=0+1048
    return tuple(map(_parse_soe, s.split("|")))


_EQUIV_GLYPH_NAMES = {
    # 'xiriq': 'xiriq_or_xiriq.orphan',
    # 'xiriq.orphan': 'xiriq_or_xiriq.orphan',
    # 'telishagedola.hlp': 'telishagedola',
    # 'alef.con': 'alef',
    # 'ayin.alt': 'ayin',
    # 'alef.xolam': 'alef'
}


def _equiv_glyph_name(name):
    return _EQUIV_GLYPH_NAMES.get(name) or name


def _so_neq(a, b, k):
    return a[k] != b[k]


# def _so_nclose(a, b, k):
#     return abs(a[k] - b[k]) > 3


def _so_nequiv_glyph_name(a, b):
    k = "glyph"
    return _equiv_glyph_name(a[k]) != _equiv_glyph_name(b[k])


def _group_by_iob(shaper_output):  # iob: index of base
    lazy = itertools.groupby(shaper_output, lambda x: x["index_of_base"])
    eager = tuple(tuple(val) for _, val in lazy)  # _ is key
    return eager


def _soe_sortkeyfn(soe):
    soe2 = dict(soe, glyph=_equiv_glyph_name(soe["glyph"]))
    return tuple(soe2.values())


def _clear_iob_of_soe(soe):
    return dict(soe, index_of_base=None)


def _clear_iob_of_soetup(soetups):
    return tuple(map(_clear_iob_of_soe, soetups))


def _clear_iob_of_pair_of_soetups(pair_of_soetups):
    return tuple(map(_clear_iob_of_soetup, pair_of_soetups))


def _cook_raw_shaper_output(so):
    return _clear_iob_of_soetup(_parse_shaper_output(so))


def _cook_raw_acc_diff(rad):
    return tuple(map(_cook_raw_shaper_output, rad))


def _cook_raw_acc_diffs(rads):
    return tuple(map(_cook_raw_acc_diff, rads))


_RAW_EQUIV_CLUSTERS = (
    # order is (actual, expected)
    # (
    #     'xiriq.orphan=9@-96,0+0|tipxa=9@350,0+0|patax=9@647,0+0|lamed=9+901',
    #     'tipxa=9@-308,0+0|xiriq=9@-96,0+0|patax=9@499,0+0|lamed=9+901'
    # ),
    # (
    #     '',
    #     ''
    # ),
)
_EQUIV_CLUSTERS = _cook_raw_acc_diffs(_RAW_EQUIV_CLUSTERS)

# def _glyph_names_eq(a, b, name):
#     return a['glyph'] == name and b['glyph'] == name


def _clusters_are_equiv(clusa, clusb):
    actexp = _clear_iob_of_pair_of_soetups((clusa, clusb))
    if actexp in _EQUIV_CLUSTERS:
        return True
    return False
    # return (
    #     _clusters_are_equiv0(actexp) or
    #     _clusters_are_equiv1(actexp))


# def _clusters_are_equiv0(actexp):
#     act, exp = actexp
#     n = 0
#     return (
#         len(act) == n+2 and len(exp) == n+1 and
#         act[n+1]['glyph'] == 'vav' and
#         act[n]['glyph'] == 'xolamxaser' and
#         exp[n]['glyph'] == 'vavxolamxaser')


# def _clusters_are_equiv1(actexp):
#     act, exp = actexp
#     n = 1
#     return (
#         len(act) == n+2 and len(exp) == n+1 and
#         act[n+1]['glyph'] == 'vav' and
#         act[n]['glyph'] == 'xolamxaser' and
#         exp[n]['glyph'] == 'vavxolamxaser' and
#         exp[0]['glyph'] == exp[0]['glyph'] and
#         exp[0]['relposx'] == exp[0]['relposx'] and
#         exp[0]['relposy'] == exp[0]['relposy'])


def _major_diff_btwn_soes(soea, soeb):
    if _so_nequiv_glyph_name(soea, soeb):
        return True
    if _so_neq(soea, soeb, "relposx"):
        return True
    if _so_neq(soea, soeb, "relposy"):
        return True
    if _so_neq(soea, soeb, "advance"):
        return True
    return False


def _major_diff_btwn_clusters(clusa, clusb):
    if _clusters_are_equiv(clusa, clusb):
        return False  # NOT a major diff
    return _do_they_differ(clusa, clusb, _major_diff_btwn_soes)


def _do_they_differ(a, b, fn):
    if len(a) != len(b):
        return True
    for x, y in zip(a, b):
        if fn(x, y):
            return True
    return False


def major(a, b):
    return True  # by default we consider all diffs major
    if b == "dummy":
        return False  # not a major diff
    ap, bp = map(_parse_shaper_output, (a, b))
    ap_clusters, bp_clusters = map(_group_by_iob, (ap, bp))
    return _do_they_differ(ap_clusters, bp_clusters, _major_diff_btwn_clusters)
