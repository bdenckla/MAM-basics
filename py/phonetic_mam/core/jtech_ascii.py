from itertools import pairwise, zip_longest
import phonetic_mam.core.deep_latin as deeplat
import phonetic_mam.core.fully_translate as ft
from mb_cmn.my_utils import sl_map


def get_jtech_ascii(dialect, sas):
    syls_per_atom = sas["sas-syls-per-atom"]
    isps_two_d = sas["sas-isps-two-d"]
    # isps: index of syllable with primary stress
    jta_atoms = sl_map((_get_jta_from_sylrecs_for_atom, dialect), syls_per_atom)
    joiners = list(map(_joiner_for_jta_atom_pair, pairwise(jta_atoms)))
    aj_structs = list(map(_add_joiner, zip_longest(jta_atoms, joiners)))
    if isps_two_d is not None:
        atom_idx, syl_idx = isps_two_d
        aj_structs[atom_idx]["aj-atom"][syl_idx].insert(0, "!")
    strs_for_aj_structs = list(map(_str_for_aj_struct, aj_structs))
    return "".join(strs_for_aj_structs)


def _str_for_aj_struct(aj_struct):
    strs_for_syls = list(map("".join, aj_struct["aj-atom"]))
    out_str = ".".join(strs_for_syls) + aj_struct["aj-joiner"]
    return out_str


def _add_joiner(atom_joiner_pair):
    atom, joiner = atom_joiner_pair
    aj_struct = {"aj-atom": atom, "aj-joiner": joiner if joiner else ""}
    return aj_struct


def _joiner_for_jta_atom_pair(jta_atom_pair):
    return "-"


def _get_jta_from_sylrecs_for_atom(dialect, sylrecs_for_atom):
    jta_syllables = sl_map((_get_jtech_ascii_from_sylrec, dialect), sylrecs_for_atom)
    return jta_syllables


def _get_jtech_ascii_from_sylrec(dialect, sylrec):
    udl_str_for_syllable = sylrec["sylrec-udl"]
    if sylrec.get("sylrec-this-syl-swp2g"):
        start_jta = [_HALF[udl_str_for_syllable[0]]]
        mid_udl = udl_str_for_syllable[1:]
    else:
        start_jta = []
        mid_udl = udl_str_for_syllable
    if geminate := sylrec.get("sylrec-next-syl-swp1g"):
        stop_jta = [_HALF[geminate]]
    else:
        stop_jta = []
    return start_jta + _jta(dialect, mid_udl) + stop_jta


def _jta(dialect, udl_str):
    return ft.fully_translate_nj(udl_str, _JTECH_FROM_UDL[dialect])


def _half(full):
    lenfull = len(full)
    assert lenfull in (2, 4)
    lenhalf = lenfull // 2
    half0 = full[:lenhalf]
    half1 = full[lenhalf:]
    assert half0 == half1
    return half0


_JTECH_SEFARAD_FROM_UDL = {
    deeplat.ALEF_1MAPIQ: "'",
    deeplat.ALEF_0MAPIQ_CON: "'",
    deeplat.ALEF_0MAPIQ_ML: "",
    deeplat.BET_1DAG_QAL: "b",
    deeplat.BET_1DAG_XAZAQ: "bb",
    deeplat.BET_0DAG: "v",
    deeplat.GIMEL_1DAG_QAL: "g",
    deeplat.GIMEL_1DAG_XAZAQ: "gg",
    deeplat.GIMEL_0DAG: "g",
    deeplat.DALET_1DAG_QAL: "d",
    deeplat.DALET_1DAG_XAZAQ: "dd",
    deeplat.DALET_0DAG: "d",
    deeplat.HE_1MAPIQ: "h",
    deeplat.HE_0MAPIQ_CON: "h",
    deeplat.HE_0MAPIQ_ML: "",
    deeplat.VAV_0DAGOSD_CON: "v",
    deeplat.VAV_0DAGOSD_ML: "",
    deeplat.ZAYIN_1DAG: "zz",
    deeplat.ZAYIN_0DAG: "z",
    deeplat.XET_0DAG: "x",
    deeplat.TET_1DAG: "tt",
    deeplat.TET_0DAG: "t",
    deeplat.YOD_1DAG: "yy",
    deeplat.YOD_0DAG_CON: "y",
    deeplat.YOD_0DAG_ML: "",
    deeplat.KAF_1DAG_QAL: "k",
    deeplat.KAF_1DAG_XAZAQ: "kk",
    deeplat.KAF_0DAG: "kh",
    deeplat.LAMED_1DAG: "ll",
    deeplat.LAMED_0DAG: "l",
    deeplat.MEM_1DAG: "mm",
    deeplat.MEM_0DAG: "m",
    deeplat.NUN_1DAG: "nn",
    deeplat.NUN_0DAG: "n",
    deeplat.SAMEKH_1DAG: "ss",
    deeplat.SAMEKH_0DAG: "s",
    deeplat.AYIN_0DAG: "`",
    deeplat.PE_1DAG_QAL: "p",
    deeplat.PE_1DAG_XAZAQ: "pp",
    deeplat.PE_0DAG: "f",
    deeplat.TSADI_1DAG: "tsts",
    deeplat.TSADI_0DAG: "ts",
    deeplat.QOF_1DAG: "kk",
    deeplat.QOF_0DAG: "k",
    deeplat.RESH_1DAG: "rr",
    deeplat.RESH_0DAG: "r",
    deeplat.TRUESHIN_1DAG: "shsh",
    deeplat.TRUESHIN_0DAG: "sh",
    deeplat.SIN_1DAG: "ss",
    deeplat.SIN_0DAG: "s",
    deeplat.TAV_1DAG_QAL: "t",
    deeplat.TAV_1DAG_XAZAQ: "tt",
    deeplat.TAV_0DAG: "t",
    #
    deeplat.FKAF_1DAG_QAL: "k",
    deeplat.FKAF_1DAG_XAZAQ: "kk",
    deeplat.FKAF_0DAG: "kh",
    deeplat.FMEM_0DAG: "m",
    deeplat.FNUN_0DAG: "n",
    deeplat.FPE_1DAG_QAL: "p",
    deeplat.FPE_0DAG: "f",
    deeplat.FTSADI_0DAG: "ts",
    #
    deeplat.VAV_1DAG: "vv",
    #
    deeplat.SHEVA_NA: "^",
    deeplat.SHEVA_NAX: "",
    deeplat.VARIKA_WITH_GENERIC_SHEVA: "^",
    deeplat.VARIKA_WITH_VOCAL_SHEVA: "^",
    deeplat.XSEGOL: "6",  #  used to be ambiguous 'e'; 6 as in  60 as in ס as in סגול
    deeplat.XPATAX: "8",  #  used to be ambiguous 'a'; 8 as in  80 as in פ as in פתח
    deeplat.XQAMATS: "0",  # used to be ambiguous 'o'; 0 as in 100 as in ק as in קמץ
    deeplat.XIRIQ_Q: "i",
    deeplat.TSERE: "E",
    deeplat.SEGOL_V: "e",
    deeplat.PATAX: "a",
    deeplat.QAMATS_G: "a",
    deeplat.QAMATS_Q: "o",
    deeplat.VAV_XOLAM: "O",
    deeplat.XOLAM_HASER: "O",
    deeplat.QUBUTS: "u",
    deeplat.SHURUQ: "u",
    deeplat.XIRIQ_G: "I",
    deeplat.YOD_0DAG_PART2_OF_DIPHTHONG: "y",  # page triple-x (Roman numeral 30)
    deeplat.SHURUQ_PART1_OF_YOD_DIPHTHONG: "u",  # page triple-x (Roman numeral 30)
    deeplat.VAV_XOLAM_PART1_OF_YOD_DIPHTHONG: "o",  # page triple-x (Roman numeral 30)
    deeplat.ALEF_SHURUQ_VOWEL: "u",
    deeplat.FPP_PATAX_MAPIQ_HE: "ah",
    deeplat.FPP_PATAX_XET: "ax",
    deeplat.FPP_PATAX_AYIN: "a`",
}
_HALF = {g: _half(_JTECH_SEFARAD_FROM_UDL[g]) for g in deeplat.GEMINATES}
# geminates don't vary between dialects so we only have 1 flavor of "_HALF"
_JTECH_ASHKENAZ_FROM_UDL = dict(_JTECH_SEFARAD_FROM_UDL)
_JTECH_ASHKENAZ_FROM_UDL[deeplat.TAV_0DAG] = "s"
_JTECH_ASHKENAZ_FROM_UDL[deeplat.QAMATS_G] = "o"
_JTECH_FROM_UDL = {
    "jta-dialect-sefarad": _JTECH_SEFARAD_FROM_UDL,
    "jta-dialect-ashkenaz": _JTECH_ASHKENAZ_FROM_UDL,
}
