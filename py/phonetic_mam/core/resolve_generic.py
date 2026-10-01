import re
import phonetic_mam.core.deep_latin as deeplat
import phonetic_mam.core.udl_char_classes as cc
import phonetic_mam.core.resolve_common as pra


def res_ndns_amb_in_atom(deeplat_atom):
    """
    Resolve ambiguities of type ndns in an atom.
    Note that ndns ambiguities are not specific to the nDnS-H format,
    which uses the Hebrew Unicode block.
    Here we're in the nDnS-L format rather than nDnS-H format,
    but the same ambiguities remain, namely, the ambiguities
    present when neither dagesh nor sheva distinctions have been made.

    nDnS-L: nDnS represented in deeplat (as opposed to the Hebrew Unicode block)
    """
    dl_str_1, concerns_1 = _do_one_pass_of_res_t12amb_in_atom(deeplat_atom)
    if concerns_1 is None:
        udl_str = dl_str_1
        return udl_str
    dl_str_2, _concerns_2 = _do_one_pass_of_res_t12amb_in_atom(dl_str_1)
    dl_str_3 = dl_str_2.replace(deeplat.SHEVA_AMB, deeplat.SHEVA_NAX)
    dl_str_4 = dl_str_3
    for amb, qal_and_xazak in pra.BGDKPT_AMB_TO_QX.items():
        _qal, xazak = qal_and_xazak
        dl_str_4 = dl_str_4.replace(amb, xazak)
    return dl_str_4


def _do_one_pass_of_res_t12amb_in_atom(deeplat_atom):
    out_dl_atom = deeplat_atom
    out_dl_atom = pra.yco_nco_sub(_VAV_1DAGOSD_PATTS_AND_REPLS, out_dl_atom)
    for amb, qal_and_xazak in pra.BGDKPT_AMB_TO_QX.items():
        qal, _xazak = qal_and_xazak
        out_dl_atom = re.sub(_QAL_PATT_1 + amb, _QAL_REPL_1 + qal, out_dl_atom)
        out_dl_atom = re.sub(_QAL_PATT_3 + amb, _QAL_REPL_3 + qal, out_dl_atom)
    out_dl_atom = re.sub(_INITIAL_SHEVA_PATT, _INITIAL_SHEVA_REPL, out_dl_atom)
    out_dl_atom = re.sub(_DAG_SHEVA_PATT, _DAG_SHEVA_REPL, out_dl_atom)
    out_dl_atom = re.sub(_X_SHEVA_Y_SHEVA_PATT, _X_SHEVA_Y_SHEVA_REPL, out_dl_atom)
    out_dl_atom = re.sub(_X_VOWEL_R_SHEVA_PATT, _X_VOWEL_R_SHEVA_REPL, out_dl_atom)
    # out_dl_atom = re.sub(_FINAL_SHEVA_PATT, _FINAL_SHEVA_REPL, out_dl_atom)
    out_dl_atom = re.sub(pra.ALEF_ML_SHURUQ_PATT, pra.ALEF_ML_SHURUQ_REPL, out_dl_atom)
    out_dl_atom = pra.yco_nco_sub(pra.ALEF_0MAPIQ_PATTS_AND_REPLS, out_dl_atom)
    out_dl_atom = pra.yco_nco_sub(pra.HE_0MAPIQ_PATTS_AND_REPLS, out_dl_atom)
    out_dl_atom = pra.yco_nco_sub(pra.YOD_0DAG_PATTS_AND_REPLS, out_dl_atom)
    out_dl_atom = pra.yco_nco_sub(pra.VAV_0DAGOSD_PATTS_AND_REPLS, out_dl_atom)
    out_dl_atom = re.sub(pra.MISC_PATT, pra.misc_repl_fun, out_dl_atom)
    return out_dl_atom, pra.find_concerns_in_atom(out_dl_atom)


def _regexp_group(inside):
    return f"({inside})"


def _regexp_class(charseq):
    join_result = "".join(charseq)
    return f"[{join_result}]"


def _regc(charseq):
    return _regexp_group(_regexp_class(charseq))


_VAV_1DAGOSD_AUU = deeplat.VAV_1DAGOSD, deeplat.VAV_1DAG, deeplat.SHURUQ
_VAV_1DAGOSD_PATTS_AND_REPLS = pra.patts_and_repls_1(_VAV_1DAGOSD_AUU)
_QAL_PATT_1 = "^"  # XXX should be restricted to start of chanted word (currently applies to start of any atom)
_QAL_REPL_1 = ""
_SHEVAS = deeplat.SHEVA_AMB, deeplat.SHEVA_NA, deeplat.SHEVA_NAX
_QAL_PATT_3 = _regc(_SHEVAS)
_QAL_REPL_3 = r"\1"
#
_INITIAL_SHEVA_PATT = "^" + _regc(pra.CON_A_OKAY) + deeplat.SHEVA_AMB
_INITIAL_SHEVA_REPL = r"\1" + deeplat.SHEVA_NA
# XXX handle שתים specially: its initial sheva is silent!
#

_LETTS_WITH_DAG = [
    *pra.BGDKPT_AMB,
    #
    deeplat.BET_1DAG_QAL,
    deeplat.BET_1DAG_XAZAQ,
    deeplat.GIMEL_1DAG_QAL,
    deeplat.GIMEL_1DAG_XAZAQ,
    deeplat.DALET_1DAG_QAL,
    deeplat.DALET_1DAG_XAZAQ,
    deeplat.ZAYIN_1DAG,
    deeplat.TET_1DAG,
    deeplat.YOD_1DAG,
    deeplat.KAF_1DAG_QAL,
    deeplat.KAF_1DAG_XAZAQ,
    deeplat.LAMED_1DAG,
    deeplat.MEM_1DAG,
    deeplat.NUN_1DAG,
    deeplat.SAMEKH_1DAG,
    deeplat.PE_1DAG_QAL,
    deeplat.PE_1DAG_XAZAQ,
    deeplat.TSADI_1DAG,
    deeplat.QOF_1DAG,
    deeplat.RESH_1DAG,
    deeplat.TRUESHIN_1DAG,
    deeplat.SIN_1DAG,
    deeplat.TAV_1DAG_XAZAQ,
    deeplat.TAV_1DAG_QAL,
    #
    deeplat.FKAF_1DAG_QAL,
    deeplat.FKAF_1DAG_XAZAQ,
    deeplat.FPE_1DAG_QAL,
    deeplat.VAV_1DAG,
]
_DAG_SHEVA_PATT = _regc(_LETTS_WITH_DAG) + deeplat.SHEVA_AMB
_DAG_SHEVA_REPL = r"\1" + deeplat.SHEVA_NA
_X_SHEVA_Y_SHEVA_PATT = "(.)" + deeplat.SHEVA_AMB + "(.)" + deeplat.SHEVA_AMB
_X_SHEVA_Y_SHEVA_REPL = r"\1" + deeplat.SHEVA_NAX + r"\2" + deeplat.SHEVA_NA
_QG_OR_TS = _regc([deeplat.QAMATS_G, deeplat.TSERE])
_X_VOWEL_R_SHEVA_PATT = "^(." + _QG_OR_TS + ")" + deeplat.RESH_0DAG + deeplat.SHEVA_AMB
_X_VOWEL_R_SHEVA_REPL = r"\1" + deeplat.RESH_0DAG + deeplat.SHEVA_NA
#
# _FINAL_SHEVA_PATT = deeplat.SHEVA_AMB + deeplat.ALEF_0MAPIQ_ML + '?' + '$'
# _FINAL_SHEVA_REPL = deeplat.SHEVA_NAX
#
