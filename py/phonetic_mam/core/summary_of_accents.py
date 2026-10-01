from functools import reduce
from mb_cmn.my_utils import increment_at_key
import mb_cmn.my_utils as my_utils
import phonetic_mam.core.bccvecs_that_are_known as knowns
import phonetic_mam.core.stress_2_cmn as two_cmn
import phonetic_mam.core.dtx_struct as dtxs
import mb_cmn.cantsys as cantsys

EDITION_PROJECTION = {
    "documentation": "note bodies excluded; Scripture target selected when present",
    "dualcant": "א (taḥton)",
    "qamats": "ד",
    "dexi-stress-helper": "2 (with helper when supplied)",
    "tsinnor-stress-helper": "2 (with helper when supplied)",
}


def get_summary_of_accents(dtx_per_book):
    """Summarize the accent vectors of one explicit implied edition.

    The phonetic products contain alternative branches.  The census is limited
    to one branch from each family.  ``EDITION_PROJECTION`` states the choice
    for five families.  It does not list ketiv and qere, where the census reads
    the qere, the branch the phonetic route takes.
    """
    cs_seen_counts = reduce(
        _accum_dtx_into_cs_seen_counts, dtx_per_book.values(), empty_cs_seen_counts()
    )
    cs_seen_examps = reduce(
        _accum_dtx_into_cs_seen_examps, dtx_per_book.values(), empty_cs_seen_examps()
    )
    return _get_summary_of_accents_2(cs_seen_counts, cs_seen_examps)


def empty_cs_seen_counts():
    return cantsys.mk_cantsys_struct({}, {})


def empty_cs_seen_examps():
    return cantsys.mk_cantsys_struct({}, {})


def record_bccvec(dtx, the_cantsys, bccvec):
    _record_bccvec_in_seen_counts(dtx, the_cantsys, bccvec)
    _record_bccvec_in_seen_examps(dtx, the_cantsys, bccvec)


def _record_bccvec_in_seen_counts(dtx, the_cantsys, bccvec):
    cs_seen_counts = dtx["dtx-out-cs-hccvec-seen-counts"]
    seen_counts = cs_seen_counts[the_cantsys]
    increment_at_key(seen_counts, bccvec)


def _record_bccvec_in_seen_examps(dtx, the_cantsys, bccvec):
    cs_seen_examps = dtx["dtx-out-cs-hccvec-seen-examples"]
    seen_examps = cs_seen_examps[the_cantsys]
    if bccvec not in seen_examps:
        seen_examps[bccvec] = []
    if len(seen_examps[bccvec]) >= 5:
        return
    bcv_str = dtxs.get_bcv_str(dtx)
    seen_examps[bccvec].append(bcv_str)


def _get_summary_of_accents_2(cs_seen_counts, cs_seen_examps):
    cs_knowns = knowns.CS_BCCVECS_THAT_ARE_KNOWN
    cs_sbnk = _dv_binop(cs_seen_counts, cs_knowns, _my_set_diff)
    cs_kbns = _dv_binop(cs_knowns, cs_seen_counts, _my_set_diff)
    cs_sbnk_hcc = my_utils.dv_map(_get_hccvecs_from_bccvecs, cs_sbnk)
    cs_kbns_hcc = my_utils.dv_map(_get_hccvecs_from_bccvecs, cs_kbns)
    cs_seen_counts_hcc = my_utils.dv_map(_convert_to_hcc_keys, cs_seen_counts)
    cs_seen_examps_hcc = my_utils.dv_map(_convert_to_hcc_keys, cs_seen_examps)
    summary = {
        "edition-projection": EDITION_PROJECTION,
        "hccvecs-that-are-seen-but-not-known": cs_sbnk_hcc,
        "hccvecs-that-are-known-but-not-seen": cs_kbns_hcc,
        "hccvec-counts": cs_seen_counts_hcc,
        "hccvec-examples": cs_seen_examps_hcc,
    }
    return summary


def _get_hccvecs_from_bccvecs(bccvecs):
    return list(map(two_cmn.get_hccvec_from_bccvec, bccvecs))


def _convert_to_hcc_keys(seen_counts):
    dic_with_hcc_keys = my_utils.dk_map(two_cmn.get_hccvec_from_bccvec, seen_counts)
    dic_with_sorted_keys = dict(sorted(dic_with_hcc_keys.items()))
    return dic_with_sorted_keys


def _accum_dtx_into_cs_seen_counts(cs_seen_counts, dtx):
    new_cs_seen_counts = _dv_binop(
        cs_seen_counts, dtx["dtx-out-cs-hccvec-seen-counts"], _dv_integer_addition
    )
    return new_cs_seen_counts


def _accum_dtx_into_cs_seen_examps(cs_seen_examps, dtx):
    new_cs_seen_examps = _dv_binop(
        cs_seen_examps, dtx["dtx-out-cs-hccvec-seen-examples"], _dv_limited_add
    )
    return new_cs_seen_examps


def _my_set_diff(seq1, seq2):
    return sorted(list(set(seq1) - set(seq2)))


def _dv_binop(dic1, dic2, binop):
    """
    Return a new dict whose values are binop applied to the
    corresponding values of dic1 and dic2.
    The dicts dic1 and dic2 are asserted to be same-keyed.
    binop: binary operator
    """
    assert list(dic1.keys()) == list(dic2.keys())
    return {k: binop(dic1[k], dic2[k]) for k in dic2}


def _dv_integer_addition(sc1, sc2):
    """
    Return a new dict whose values are addition applied to the
    corresponding values of dic1 and dic2.
    The dicts dic1 and dic2 are not assumed to be same-keyed.
    A default vaue of zero (0) is supplied where keys are missing.
    """
    all_keys = set(sc1.keys()) | set(sc2.keys())
    out = {k: sc1.get(k, 0) + sc2.get(k, 0) for k in all_keys}
    return out


def _dv_limited_add(sc1, sc2):
    """
    Return a new dict whose values are "size-limited list add" applied to the
    corresponding values of dic1 and dic2.
    The dicts dic1 and dic2 are not assumed to be same-keyed.
    A default vaue of [] (the empty list) is supplied where keys are missing.
    """
    all_keys = set(sc1.keys()) | set(sc2.keys())
    out = {k: _limited_add(sc1.get(k, []), sc2.get(k, [])) for k in all_keys}
    return out


def _limited_add(list_1, list_2):
    list_sum = list_1 + list_2
    list_sum = list(sorted(list_sum))  # sorted, for stability in face of multithreading
    return list_sum[:5]
