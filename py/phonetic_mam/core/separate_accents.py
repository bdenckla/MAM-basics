import re
import mb_cmn.my_utils as my_utils
import mb_cmn.hebrew_punctuation as hpu
import mb_cmn.hebrew_points as hpo
import mb_cmn.hebrew_accents as ha
import phonetic_mam.core.trans_tables as tt
import phonetic_mam.core.bccvecs_that_are_known as knowns


def get_sepacc(the_cantsys, accar):  # accar: accents and related
    if accar == "ש֚תים":
        accar = "ש֚ת֚ים"  # add yetiv "stress helper"
    parts_0 = re.split(_RE_GRP_ACCAR, accar)
    assert parts_0[0]
    parts_1 = _split_some_accents(parts_0)
    parts_2 = _strip_gaya_leave_slq(parts_1)
    lomvec = tuple(_take_even(parts_2))
    accvec = tuple(_take_odd(parts_2))
    bccvec = knowns.get_bccvec_from_accvec(the_cantsys, accvec)
    # lomvec: tuple of strings where each char is a letter or maqaf
    # bccvec: tuple of strings where each char is an accent or an accent-related char like sof pasuq
    return lomvec, bccvec


def _take_even(seq):
    return [x[1] for x in enumerate(seq) if x[0] % 2 == 0]


def _take_odd(seq):
    return [x[1] for x in enumerate(seq) if x[0] % 2 == 1]


def _regexp_class(charseq):
    join_result = "".join(charseq)
    return f"[{join_result}]"


def _regexp_group(inside):
    return f"({inside})"


def _resolve_gaya_vs_slq(an_parts):
    # This assumes that the last Unicode METEG is silluq.
    # The only case in which I know this is false
    # is a case we don't have to worry about, because it is
    # only in the LC: נְחֹֽשֶֽׁת׃ in 1 Sam 17:5.
    # (MAM doesn't follow the LC there.)
    #
    # Example I/O: (input (an_parts) represents 'וֽיהי־אֽור׃')
    # Input       | Output
    # ------------| ------------
    # 'ו'         |  [same]
    # hpo.MTGOSLQ | 'rgvs-gaʿya'
    # 'יהי־א'     |  [same]
    # hpo.MTGOSLQ |  [same]
    # 'ור'        |  [same]
    # '׃'         |  [same]
    # ''          |  [same]
    #
    assert len(an_parts) > 1
    has_sopa = an_parts[-2] == hpu.SOPA
    an_parts_rev = list(reversed(an_parts))
    resolved_rev = _resolve_gaya_vs_slq_rev(has_sopa, an_parts_rev)
    resolved = list(reversed(resolved_rev))
    return resolved


def _resolve_gaya_vs_slq_rev(has_sopa, an_parts_rev):
    accum = []
    next_mtgoslq_is_slq = has_sopa
    for an_part in an_parts_rev:
        if an_part != hpo.MTGOSLQ:
            accum.append(an_part)
            continue
        if next_mtgoslq_is_slq:
            next_mtgoslq_is_slq = False
            accum.append(hpo.MTGOSLQ)
            continue
        accum.append("rgvs-gaʿya")
    return accum


def _split_some_accents(an_parts):
    le_an_parts = list(enumerate(an_parts))
    out_1 = list(map(_split_some_1, le_an_parts))
    out_2 = my_utils.sum_of_seqs(out_1)
    return out_2


def _split_some_1(idx_and_part):
    idx, an_part = idx_and_part
    if idx % 2 and len(an_part) > 1:
        return _split_some_2(an_part)
    return [an_part]


def _split_some_2(an_part):
    assert len(an_part) == 2
    handler = _DUAL_ACCENT_HANDLERS[an_part]
    return handler(an_part)


def _dah_keep_together(an_part):
    return [an_part]


def _dah_split(an_part):
    return [an_part[0], "", an_part[1]]


def _dah_split_and_reverse(an_part):
    return [an_part[1], "", an_part[0]]


def _dah_take_second(an_part):
    return [an_part[1]]


_DUAL_ACCENT_HANDLERS = {
    ha.GER + ha.TEL_G: _dah_keep_together,
    ha.GER_2 + ha.TEL_G: _dah_keep_together,
    ha.MAH + ha.QOM: _dah_keep_together,
    #
    ha.GER_M + ha.REV: _dah_split,
    #
    ha.MER + ha.OLE: _dah_split_and_reverse,
    # MER-then-OLE order is "wrong" in some sense
    # (should be oleh-ve-yored in that order)
    # but it is "right" in that it respects below-mark-then-above-mark order.
    # (Below-then-above is suggested by John Hudson in the SBL Hebrew manual.)
    #
    hpo.MTGOSLQ + hpu.SOPA: _dah_split,
    ha.MUN + hpu.PASOLEG: _dah_split,
    ha.QOM + hpu.PASOLEG: _dah_split,
    ha.MAH + hpu.PASOLEG: _dah_split,
    ha.SHA + hpu.PASOLEG: _dah_split,
    #
    ha.MUN + ha.DEX: _dah_take_second,
    ha.MER + ha.GER_M: _dah_take_second,
    #
    hpo.MTGOSLQ + ha.TEL_G: _dah_take_second,
    hpo.MTGOSLQ + ha.GER_M: _dah_take_second,
    hpo.MTGOSLQ + ha.DEX: _dah_take_second,
    hpo.MTGOSLQ + ha.OLE: _dah_take_second,
}


def _strip_gaya_leave_slq(an_parts):
    resolved = _resolve_gaya_vs_slq(an_parts)
    last = None
    accum = []
    for an_part in resolved:
        if last == "rgvs-gaʿya":
            accum[-1] += an_part
        elif an_part != "rgvs-gaʿya":
            accum.append(an_part)
        last = an_part
    return accum


_RE_GRP_ACCAR = _regexp_group(_regexp_class(tt.ACCENTS_AND_RELATED) + "+")
