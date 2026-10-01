import mb_cmn.hebrew_accents as ha
import mb_cmn.hebrew_points as hpo
import mb_cmn.hebrew_punctuation as hpu

_VOWELS_AND_RELATED = [
    hpo.SHEVA_NA,
    hpo.DAGESH_XAZAQ,
    hpo.DAGOMOSD,
    hpo.SHIND,
    hpo.SIND,
    hpo.SHEVA,
    hpo.XSEGOL,
    hpo.XPATAX,
    hpo.XQAMATS,
    hpo.XIRIQ,
    hpo.TSERE,
    hpo.SEGOL_V,
    hpo.PATAX,
    hpo.QAMATS,
    hpo.QAMATS_Q,
    hpo.XOLAM_XFV,
    hpo.XOLAM,
    hpo.QUBUTS,
    hpo.VARIKA,
]
ACCENTS_AND_RELATED = [
    hpo.MTGOSLQ,
    hpu.SOPA,
    hpu.PASOLEG,
    ha.ATN,
    ha.SEG_A,
    ha.SHA,
    ha.ZAQ_Q,
    ha.ZAQ_G,
    ha.TIP,
    ha.REV,
    ha.ZSH_OR_TSIT,
    ha.PASH,
    ha.YET,
    ha.TEV,
    ha.GER,
    ha.GER_M,
    ha.GER_2,
    ha.QAR,
    ha.TEL_G,
    ha.PAZ,
    ha.ATN_H,
    ha.MUN,
    ha.MAH,
    ha.MER,
    ha.MER_2,
    ha.DAR,
    ha.QOM,
    ha.TEL_Q,
    ha.YBY,
    ha.OLE,
    ha.ILU,
    ha.DEX,
    ha.Z_OR_TSOR,
]
TRANS_TABLE_TO_RM_MISC = str.maketrans(
    {
        hpu.UPDOT: None,
        hpu.LODOT: None,
        hpo.RAFE: None,
        hpu.NUN_HAF: None,
    }
)
TRANS_TABLE_TO_RM_ACCENTS_AR = str.maketrans({d: None for d in ACCENTS_AND_RELATED})
TRANS_TABLE_TO_RM_VOWELS_AR = str.maketrans({d: None for d in _VOWELS_AND_RELATED})
