import phonetic_mam.core.deep_latin as deeplat
import phonetic_mam.core.fully_translate as ft


def get_ipa(udlcw):  # udlcw: unambiguous-deeplat chanted word
    return ft.fully_translate(udlcw, _IPA_FROM_UDL)


_IPA_FROM_UDL = {
    deeplat.BLACK_MAQAF: ".",  # syllable divider
    deeplat.GRAY_MAQAF: ".",  # syllable divider
    deeplat.ALEF_1MAPIQ: "ʔ",
    deeplat.ALEF_0MAPIQ_CON: "ʔ",
    deeplat.ALEF_0MAPIQ_ML: "",
    deeplat.BET_1DAG_QAL: "b",
    deeplat.BET_1DAG_XAZAQ: "bb",
    deeplat.BET_0DAG: "v",
    deeplat.GIMEL_1DAG_QAL: "g",
    deeplat.GIMEL_1DAG_XAZAQ: "gg",
    deeplat.GIMEL_0DAG: "g",  # ɣ ?
    deeplat.DALET_1DAG_QAL: "d",
    deeplat.DALET_1DAG_XAZAQ: "dd",
    deeplat.DALET_0DAG: "d",  # ð ?
    deeplat.HE_1MAPIQ: "h",
    deeplat.HE_0MAPIQ_CON: "h",
    deeplat.HE_0MAPIQ_ML: "",
    deeplat.VAV_0DAGOSD_CON: "v",
    deeplat.VAV_0DAGOSD_ML: "",
    deeplat.ZAYIN_1DAG: "zz",
    deeplat.ZAYIN_0DAG: "z",
    deeplat.XET_0DAG: "x",  # ħ ? χ ?
    deeplat.TET_1DAG: "tt",  # tˤ ?
    deeplat.TET_0DAG: "t",  # tˤ ?
    deeplat.YOD_1DAG: "jj",
    deeplat.YOD_0DAG_CON: "j",
    deeplat.YOD_0DAG_ML: "",
    deeplat.KAF_1DAG_QAL: "k",
    deeplat.KAF_1DAG_XAZAQ: "kk",
    deeplat.KAF_0DAG: "x",  # χ ?
    deeplat.LAMED_1DAG: "ll",
    deeplat.LAMED_0DAG: "l",
    deeplat.MEM_1DAG: "mm",
    deeplat.MEM_0DAG: "m",
    deeplat.NUN_1DAG: "nn",
    deeplat.NUN_0DAG: "n",
    deeplat.SAMEKH_1DAG: "ss",
    deeplat.SAMEKH_0DAG: "s",
    deeplat.AYIN_0DAG: "ʔ",  # ʕ ?
    deeplat.PE_1DAG_QAL: "p",
    deeplat.PE_1DAG_XAZAQ: "pp",
    deeplat.PE_0DAG: "f",
    deeplat.TSADI_1DAG: "t͡s",  # XXX not sure how to lengthen this; t͡st͡s seems wrong
    deeplat.TSADI_0DAG: "t͡s",  # sˤ ?
    deeplat.QOF_1DAG: "kk",  # q ?
    deeplat.QOF_0DAG: "k",  # q ?
    deeplat.RESH_1DAG: "ʁʁ",  # r ?
    deeplat.RESH_0DAG: "ʁ",  # r ?
    deeplat.TRUESHIN_1DAG: "ʃʃ",
    deeplat.TRUESHIN_0DAG: "ʃ",
    deeplat.SIN_1DAG: "ss",
    deeplat.SIN_0DAG: "s",
    deeplat.TAV_1DAG_QAL: "t",
    deeplat.TAV_1DAG_XAZAQ: "tt",
    deeplat.TAV_0DAG: "t",  # θ ?
    #
    deeplat.FKAF_1DAG_QAL: "k",
    deeplat.FKAF_1DAG_XAZAQ: "kk",
    deeplat.FKAF_0DAG: "x",  # χ ?
    deeplat.FMEM_0DAG: "m",
    deeplat.FNUN_0DAG: "n",
    deeplat.FPE_1DAG_QAL: "p",
    deeplat.FPE_0DAG: "f",
    deeplat.FTSADI_0DAG: "t͡s",  # sˤ ?
    #
    deeplat.VAV_1DAG: "vv",
    #
    deeplat.SHEVA_NA: "ə",
    deeplat.SHEVA_NAX: "",
    deeplat.VARIKA_WITH_GENERIC_SHEVA: "ə",
    deeplat.VARIKA_WITH_VOCAL_SHEVA: "ə",
    deeplat.XSEGOL: "e",
    deeplat.XPATAX: "a",
    deeplat.XQAMATS: "o",
    deeplat.XIRIQ_Q: "i",
    deeplat.TSERE: "e",
    deeplat.SEGOL_V: "e",  # ɛ ?
    deeplat.PATAX: "a",
    deeplat.QAMATS_G: "a",  # ɔ ?
    deeplat.QAMATS_Q: "o",  # ɔ ?
    deeplat.VAV_XOLAM: "o",
    deeplat.XOLAM_HASER: "o",
    deeplat.QUBUTS: "u",
    deeplat.SHURUQ: "u",
    deeplat.XIRIQ_G: "i",
    deeplat.YOD_0DAG_PART2_OF_DIPHTHONG: "i",
    deeplat.SHURUQ_PART1_OF_YOD_DIPHTHONG: "u",
    deeplat.VAV_XOLAM_PART1_OF_YOD_DIPHTHONG: "o",
    deeplat.ALEF_SHURUQ_VOWEL: "u",
    deeplat.FPP_PATAX_MAPIQ_HE: "ah",
    deeplat.FPP_PATAX_XET: "ax",
    deeplat.FPP_PATAX_AYIN: "aʔ",
}
