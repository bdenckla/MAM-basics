import mb_cmn.hebrew_accents as ha
import mb_cmn.hebrew_punctuation as hpu
import mb_cmn.hebrew_points as hpo
import mb_cmn.cantsys as cantsys


def get_bccvec_from_accvec(the_cantsys, accvec):
    fun = _GET_BCCVEC_FN[the_cantsys]
    return fun(accvec)


def _get_bccvec_from_accvec_prose(accvec):
    return _DIC_FROM_ACCVEC_TO_BCCVEC_PROSE.get(accvec) or accvec


def _get_bccvec_from_accvec_poetic(accvec):
    return _DIC_FROM_ACCVEC_TO_BCCVEC_POETIC.get(accvec) or accvec


_GET_BCCVEC_FN = cantsys.mk_cantsys_struct(
    _get_bccvec_from_accvec_prose, _get_bccvec_from_accvec_poetic
)


_DIC_FROM_ACCVEC_TO_BCCVEC_PROSE = {
    (hpo.MTGOSLQ, hpu.SOPA): (ha.NU_SLQ, hpu.SOPA),
    (ha.MER, hpo.MTGOSLQ, hpu.SOPA): (ha.MER, ha.NU_SLQ, hpu.SOPA),
    (ha.TIP, hpo.MTGOSLQ, hpu.SOPA): (ha.TIP, ha.NU_SLQ, hpu.SOPA),
    #
    (ha.SHA, hpu.PASOLEG): (ha.NU_SHA_LEG, hpu.PASOLEG),
    (ha.MUN, hpu.PASOLEG): (ha.NU_MUN_LEG, hpu.PASOLEG),
    (ha.MER, ha.MUN, hpu.PASOLEG): (ha.MER, ha.NU_MUN_LEG, hpu.PASOLEG),
    #
    (ha.Z_OR_TSOR,): (ha.NU_Z,),
    (ha.ZSH_OR_TSIT, ha.Z_OR_TSOR): (ha.NU_Z, ha.NU_Z),
    # Above, we switch from zazi to "self-help" (zizi).
}
_ACCVEC_TSIT_MER_SLQ_SOPA = ha.ZSH_OR_TSIT, ha.MER, hpo.MTGOSLQ, hpu.SOPA
_BCCVEC_TSIT_MER_SLQ_SOPA = ha.NU_TSIT, ha.MER, ha.NU_SLQ, hpu.SOPA
_DIC_FROM_ACCVEC_TO_BCCVEC_POETIC = {
    (hpo.MTGOSLQ, hpu.SOPA): (ha.NU_SLQ, hpu.SOPA),
    (ha.MER, hpo.MTGOSLQ, hpu.SOPA): (ha.MER, ha.NU_SLQ, hpu.SOPA),
    (ha.TIP, hpo.MTGOSLQ, hpu.SOPA): (ha.TIP, ha.NU_SLQ, hpu.SOPA),
    _ACCVEC_TSIT_MER_SLQ_SOPA: _BCCVEC_TSIT_MER_SLQ_SOPA,
    #
    (ha.SHA, hpu.PASOLEG): (ha.NU_SHA_LEG, hpu.PASOLEG),
    (ha.MAH, hpu.PASOLEG): (ha.NU_MAH_LEG, hpu.PASOLEG),
    (ha.QOM, hpu.PASOLEG): (ha.NU_AZL_LEG, hpu.PASOLEG),
    (ha.MAH, ha.QOM, hpu.PASOLEG): (ha.MAH, ha.NU_AZL_LEG, hpu.PASOLEG),
    (ha.MER, ha.QOM, hpu.PASOLEG): (ha.MER, ha.NU_AZL_LEG, hpu.PASOLEG),
    (ha.ILU, ha.QOM, hpu.PASOLEG): (ha.ILU, ha.NU_AZL_LEG, hpu.PASOLEG),
    #
    (ha.Z_OR_TSOR,): (ha.NU_TSOR,),
    (ha.Z_OR_TSOR, ha.Z_OR_TSOR): (ha.NU_TSOR, ha.NU_TSOR),
    (ha.MER, ha.Z_OR_TSOR): (ha.MER, ha.NU_TSOR),
    (ha.MAH, ha.Z_OR_TSOR): (ha.MAH, ha.NU_TSOR),
    #
    (ha.ZSH_OR_TSIT, ha.MAH, ha.REV): (ha.NU_TSIT, ha.MAH, ha.REV),
    (ha.ZSH_OR_TSIT, ha.MAH): (ha.NU_TSIT, ha.MAH),
    (ha.MER, ha.ZSH_OR_TSIT, ha.MAH): (ha.MER, ha.NU_TSIT, ha.MAH),
    (ha.MAH, ha.ZSH_OR_TSIT, ha.MER): (ha.MAH, ha.NU_TSIT, ha.MER),
    (ha.ZSH_OR_TSIT, ha.MER): (ha.NU_TSIT, ha.MER),
}
_GET_STRESS_INFO_FROM_BCCVEC_PROSE = {
    (ha.ATN,): -1,
    (ha.SEG_A,): -1,
    (ha.ZAQ_Q,): -1,
    (ha.ZAQ_G,): -1,
    (ha.TIP,): -1,
    (ha.REV,): -1,
    (ha.PASH,): -1,
    (ha.YET,): -1,
    (ha.TEV,): -1,
    (ha.GER,): -1,
    (ha.GER_2,): -1,
    (ha.QAR,): -1,
    (ha.TEL_G,): -1,
    (ha.PAZ,): -1,
    (ha.MUN,): -1,
    (ha.MAH,): -1,
    (ha.MER,): -1,
    (ha.MER_2,): -1,
    (ha.DAR,): -1,
    (ha.QOM,): -1,
    (ha.TEL_Q,): -1,
    (ha.NU_Z,): -1,
    (ha.YBY,): -1,
    #
    (ha.NU_SLQ, hpu.SOPA): -2,
    #
    (ha.G2_TG, ha.G2_TG): -1,
    (ha.G1_TG, ha.G1_TG): -1,
    (ha.G2_TG,): -1,
    (ha.G1_TG,): -1,
    #
    (ha.MAH + ha.QOM,): -1,
    #
    #
    (ha.TIP, ha.NU_SLQ, hpu.SOPA): -2,
    (ha.MER, ha.NU_SLQ, hpu.SOPA): -2,
    (ha.MAH, ha.PASH): -1,
    (ha.MAH, ha.PASH, ha.PASH): -2,
    (ha.NU_SHA_LEG, hpu.PASOLEG): -2,
    (ha.NU_MUN_LEG, hpu.PASOLEG): -2,
    (ha.MER, ha.NU_MUN_LEG, hpu.PASOLEG): -2,
    (ha.MUN, ha.ZAQ_Q): -1,
    (ha.MUN, ha.ATN): -1,
    (ha.MUN, ha.REV): -1,
    (ha.MUN, ha.PAZ): -1,
    (ha.MUN, ha.MAH): -1,
    (ha.QOM, ha.ZAQ_Q): -1,
    (ha.QOM, ha.GER): -1,
    (ha.QOM, ha.MER): -1,
    (ha.QOM, ha.MAH): -1,
    (ha.QOM, ha.DAR): -1,
    (ha.MER, ha.TEV): -1,
    (ha.MER, ha.TIP): -1,
    (ha.MER, ha.PASH, ha.PASH): -2,
    (ha.TIP, ha.ATN): -1,
    # Postpositives
    (ha.SEG_A, ha.SEG_A): -2,
    (ha.PASH, ha.PASH): -2,
    (ha.TEL_Q, ha.TEL_Q): -2,
    (ha.NU_Z, ha.NU_Z): -2,
    #
    (ha.TEL_G, ha.TEL_G): -1,
    (ha.YET, ha.YET): -1,  # not real; yetiv stress helper synthesized for שתים
}
_GET_STRESS_INFO_FROM_BCCVEC_POETIC = {
    (ha.MAH,): -1,
    (ha.ATN,): -1,
    (ha.TIP,): -1,
    (ha.REV,): -1,
    (ha.SHA,): -1,
    (ha.PAZ,): -1,
    (ha.ATN_H,): -1,
    (ha.MUN,): -1,
    (ha.MER,): -1,
    (ha.QOM,): -1,
    (ha.YBY,): -1,
    (ha.ILU,): -1,
    (ha.DEX,): -1,
    (ha.DEX, ha.DEX): -1,
    (ha.NU_TSOR,): -1,
    (ha.NU_TSOR, ha.NU_TSOR): -2,
    #
    (ha.NU_SLQ, hpu.SOPA): -2,
    #
    (ha.MER, ha.NU_SLQ, hpu.SOPA): -2,
    (ha.TIP, ha.NU_SLQ, hpu.SOPA): -2,
    (ha.NU_TSIT, ha.MER, ha.NU_SLQ, hpu.SOPA): -1,
    #
    (ha.NU_SHA_LEG, hpu.PASOLEG): -2,
    (ha.NU_MAH_LEG, hpu.PASOLEG): -2,
    (ha.NU_AZL_LEG, hpu.PASOLEG): -2,
    (ha.MAH, ha.NU_AZL_LEG, hpu.PASOLEG): -2,
    (ha.MER, ha.NU_AZL_LEG, hpu.PASOLEG): -2,
    (ha.ILU, ha.NU_AZL_LEG, hpu.PASOLEG): -2,
    #
    (ha.OLE, ha.MER): -1,
    #
    (ha.GER_M, ha.REV): -1,
    #
    (ha.MER, ha.REV): -1,
    (ha.GER_M, ha.MER, ha.REV): -1,
    (ha.NU_TSIT, ha.MAH, ha.REV): -1,
    (ha.NU_TSIT, ha.MAH): -1,
    (ha.MER, ha.NU_TSIT, ha.MAH): -1,
    (ha.NU_TSIT, ha.MER): -1,
    (ha.MAH, ha.NU_TSIT, ha.MER): -1,
    (ha.ATN_H, ha.OLE): -2,
    (ha.ATN_H, ha.OLE, ha.MER): -1,
    #
    (ha.MER, ha.MUN): -1,
    (ha.MAH, ha.MUN): -1,
    (ha.TIP, ha.MUN): -1,
    (ha.MUN, ha.MUN): -1,
    #
    (ha.MAH, ha.MER): -1,
    (ha.MER, ha.MER): -1,
    #
    (ha.YBY, ha.PAZ): -1,
    (ha.MER, ha.PAZ): -1,
    #
    (ha.MUN, ha.ATN): -1,
    (ha.MER, ha.ATN): -1,
    #
    (ha.MAH, ha.OLE): -2,  # occurs only once: Ps53:5 פֹּ֤עֲלֵ֫י
    (ha.MER, ha.QOM): -1,
    (ha.MAH, ha.QOM): -1,
    (ha.MER, ha.NU_TSOR): -1,
    (ha.MAH, ha.NU_TSOR): -1,
    (ha.DEX, ha.MUN, ha.DEX): -1,
    (ha.MAH, ha.TIP): -1,
    #
    (ha.MER, ha.OLE, ha.MER): -1,
    (ha.MER, ha.TIP): -1,
}
CS_GET_STRESS_INFO_FROM_BCCVEC = cantsys.mk_cantsys_struct(
    _GET_STRESS_INFO_FROM_BCCVEC_PROSE,
    _GET_STRESS_INFO_FROM_BCCVEC_POETIC,
)
CS_BCCVECS_THAT_ARE_KNOWN = cantsys.mk_cantsys_struct(
    list(_GET_STRESS_INFO_FROM_BCCVEC_PROSE.keys()),
    list(_GET_STRESS_INFO_FROM_BCCVEC_POETIC.keys()),
)
