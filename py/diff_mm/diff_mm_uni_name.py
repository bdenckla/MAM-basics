"""Exports name"""

import unicodedata
from pycmn import hebrew_letters as hl
from pycmn import hebrew_points as hpo
from pycmn import hebrew_accents as ha
from pycmn import hebrew_punctuation as hpu
from pycmn import str_defs as sd


def name(string_len_1):
    """Convert string_len_1 to a name elucidation"""
    return _SHORT_NAMES.get(string_len_1) or unicodedata.name(string_len_1)


_SHORT_NAMES = {
    " ": "space",  # 0020
    sd.CGJ: "combining-grapheme-joiner",  # 034f
    sd.ZWJ: "zero-width-joiner",  # 200d
    ha.ATN: "atnax",  # 0591
    ha.SEG_A: "segol-accent",  # 0592
    ha.SHA: "shalshelet",  # 0593
    ha.ZAQ_Q: "zaqef-qatan",  # 0594
    ha.ZAQ_G: "zaqef-gadol",  # 0595
    ha.TIP: "tipexa/tarxa",  # 0596
    ha.REV: "revia",  # 0597
    ha.ZSH_OR_TSIT: "zarqa-stress-helper/tsinnorit",  # 0598
    ha.PASH: "pashta",  # 0599
    ha.YET: "yetiv",  # 059a
    ha.TEV: "tevir",  # 059b
    ha.GER: "geresh",  # 059c
    ha.GER_M: "geresh-muqdam",  # 059d
    ha.GER_2: "gershayim",  # 059e
    ha.QAR: "qarney-para",  # 059f
    ha.TEL_G: "telisha-gedola",  # 05a0
    ha.PAZ: "pazer",  # 05a1
    ha.ATN_H: "atnax-hafukh",  # 05a2
    ha.MUN: "munax",  # 05a3
    ha.MAH: "mahapakh",  # 05a4
    ha.MER: "merkha/yored",  # 05a5
    ha.MER_2: "merkha-kefula",  # 05a6
    ha.DAR: "darga",  # 05a7
    ha.QOM: "qadma/metigah/azla",  # 05a8
    ha.TEL_Q: "telisha-qetana",  # 05a9
    ha.YBY: "yerax-ben-yomo/galgal",  # 05aa
    ha.OLE: "ole",  # 05ab
    ha.ILU: "iluy",  # 05ac
    ha.DEX: "dexi",  # 05ad
    ha.Z_OR_TSOR: "zarqa/tsinnor",  # 05ae
    hpo.SHEVA: "sheva",  # 05b0
    hpo.XSEGOL: "xataf-segol",  # 05b1
    hpo.XPATAX: "xataf-patax",  # 05b2
    hpo.XQAMATS: "xataf-qamats",  # 05b3
    hpo.XIRIQ: "xiriq",  # 05b4
    hpo.TSERE: "tsere",  # 05b5
    hpo.SEGOL_V: "segol-vowel",  # 05b6
    hpo.PATAX: "patax",  # 05b7
    hpo.QAMATS: "qamats",  # 05b8
    hpo.XOLAM: "xolam",  # 05b9
    hpo.XOLAM_XFV: "xolam-xaser-for-vav",  # 05ba
    hpo.QUBUTS: "qubuts",  # 05bb
    hpo.DAGOMOSD: "dagesh/mapiq/shuruq-dot",  # 05bc
    hpo.MTGOSLQ: "meteg/silluq",  # 05bd
    hpu.MAQ: "maqaf",  # 05be
    hpo.RAFE: "rafeh",  # 05bf
    hpu.PASOLEG: "paseq/legarmeih",  # 05c0
    hpo.SHIND: "shin-dot",  # 05c1
    hpo.SIND: "sin-dot",  # 05c2
    hpu.SOPA: "sof-pasuq",  # 05c3
    hpu.UPDOT: "upper-dot",  # 05c4
    hpu.LODOT: "lower-dot",  # 05c5
    hpu.NUN_HAF: "nun-hafukha",  # 05c6
    hpo.QAMATS_Q: "qamats-qatan",  # 05c7
    hl.ALEF: "alef",  # 05d0
    hl.BET: "bet",  # 05d1
    hl.GIMEL: "gimel",  # 05d2
    hl.DALET: "dalet",  # 05d3
    hl.HE: "he",  # 05d4
    hl.VAV: "vav",  # 05d5
    hl.ZAYIN: "zayin",  # 05d6
    hl.XET: "xet",  # 05d7
    hl.TET: "tet",  # 05d8
    hl.YOD: "yod",  # 05d9
    hl.FKAF: "final-kaf",  # 05da
    hl.KAF: "kaf",  # 05db
    hl.LAMED: "lamed",  # 05dc
    hl.FMEM: "final-mem",  # 05dd
    hl.MEM: "mem",  # 05de
    hl.FNUN: "final-nun",  # 05df
    hl.NUN: "nun",  # 05e0
    hl.SAMEKH: "samekh",  # 05e1
    hl.AYIN: "ayin",  # 05e2
    hl.FPE: "final-pe",  # 05e3
    hl.PE: "pe",  # 05e4
    hl.FTSADI: "final-tsadi",  # 05e5
    hl.TSADI: "tsadi",  # 05e6
    hl.QOF: "qof",  # 05e7
    hl.RESH: "resh",  # 05e8
    hl.SHIN: "shin",  # 05e9
    hl.TAV: "tav",  # 05ea
    hpo.VARIKA: "varika",
}
