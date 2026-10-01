import phonetic_mam.core.deep_latin as deeplat

UNAMB_CONSONANTS = {
    deeplat.ALEF_1MAPIQ,
    deeplat.BET_1DAG_QAL,
    deeplat.BET_1DAG_XAZAQ,
    deeplat.BET_0DAG,
    deeplat.GIMEL_1DAG_QAL,
    deeplat.GIMEL_1DAG_XAZAQ,
    deeplat.GIMEL_0DAG,
    deeplat.DALET_1DAG_QAL,
    deeplat.DALET_1DAG_XAZAQ,
    deeplat.DALET_0DAG,
    deeplat.HE_1MAPIQ,
    deeplat.VAV_0DAGOSD_CON,
    deeplat.ZAYIN_1DAG,
    deeplat.ZAYIN_0DAG,
    deeplat.XET_0DAG,
    deeplat.TET_1DAG,
    deeplat.TET_0DAG,
    deeplat.YOD_1DAG,
    deeplat.KAF_1DAG_QAL,
    deeplat.KAF_1DAG_XAZAQ,
    deeplat.KAF_0DAG,
    deeplat.LAMED_1DAG,
    deeplat.LAMED_0DAG,
    deeplat.MEM_1DAG,
    deeplat.MEM_0DAG,
    deeplat.NUN_1DAG,
    deeplat.NUN_0DAG,
    deeplat.SAMEKH_1DAG,
    deeplat.SAMEKH_0DAG,
    deeplat.AYIN_0DAG,
    deeplat.PE_1DAG_QAL,
    deeplat.PE_1DAG_XAZAQ,
    deeplat.PE_0DAG,
    deeplat.TSADI_1DAG,
    deeplat.TSADI_0DAG,
    deeplat.QOF_1DAG,
    deeplat.QOF_0DAG,
    deeplat.RESH_1DAG,
    deeplat.RESH_0DAG,
    deeplat.TRUESHIN_1DAG,
    deeplat.TRUESHIN_0DAG,
    deeplat.SIN_1DAG,
    deeplat.SIN_0DAG,
    deeplat.TAV_1DAG_XAZAQ,
    deeplat.TAV_1DAG_QAL,
    deeplat.TAV_0DAG,
    #
    deeplat.FKAF_1DAG_QAL,
    deeplat.FKAF_1DAG_XAZAQ,
    deeplat.FKAF_0DAG,
    deeplat.FMEM_0DAG,
    deeplat.FNUN_0DAG,
    deeplat.FPE_1DAG_QAL,
    deeplat.FPE_0DAG,
    deeplat.FTSADI_0DAG,
    #
    deeplat.ALEF_0MAPIQ_CON,
    deeplat.HE_0MAPIQ_CON,
    deeplat.YOD_0DAG_CON,
    deeplat.YOD_0DAG_PART2_OF_DIPHTHONG,  # for these purposes we consider it a consonant
    deeplat.VAV_1DAG,
}
UNAMB_VOWELS = [
    deeplat.SHEVA_NA,
    deeplat.VARIKA_WITH_GENERIC_SHEVA,
    deeplat.VARIKA_WITH_VOCAL_SHEVA,
    deeplat.XSEGOL,
    deeplat.XPATAX,
    deeplat.XQAMATS,
    deeplat.XIRIQ_G,
    deeplat.XIRIQ_Q,
    deeplat.TSERE,
    deeplat.SEGOL_V,
    deeplat.PATAX,
    deeplat.QAMATS_G,
    deeplat.QAMATS_Q,
    deeplat.XOLAM_HASER,
    deeplat.QUBUTS,
    #
    deeplat.VAV_XOLAM,
    deeplat.SHURUQ,
    #
    deeplat.SHURUQ_PART1_OF_YOD_DIPHTHONG,
    deeplat.VAV_XOLAM_PART1_OF_YOD_DIPHTHONG,
    #
    deeplat.ALEF_SHURUQ_VOWEL,
]
UNAMB_MLS = [
    deeplat.ALEF_0MAPIQ_ML,
    deeplat.HE_0MAPIQ_ML,
    deeplat.YOD_0DAG_ML,
    deeplat.VAV_0DAGOSD_ML,
]


def _regexp_class(charseq):
    join_result = "".join(charseq)
    return f"[{join_result}]"


RE_CLS_UNAMB_CONSONANT = _regexp_class(sorted(UNAMB_CONSONANTS))
RE_CLS_UNAMB_VOWEL = _regexp_class(sorted(UNAMB_VOWELS))
RE_CLS_UNAMB_ML = _regexp_class(sorted(UNAMB_MLS))
