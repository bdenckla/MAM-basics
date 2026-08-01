import re
import mb_cmn.hebrew_points as hpo
import mb_cmn.hebrew_accents as ha
import mb_cmn.hebrew_punctuation as hpu
import mb_cmn.str_defs as sd


def tword(mcword: str):
    stage = mcword.replace(":A", "a").replace(":F", "f").replace(":E", "e")
    stage = re.sub(_XOLAM_PATT1, _XOLAM_REPL1, stage)
    stage = re.sub(_XOLAM_PATT2, _XOLAM_REPL2, stage)
    stage = re.sub(_XOLAM_PATT3, _XOLAM_REPL3, stage)
    stage = re.sub(_EARLY_MTG_PATT, _EARLY_MTG_REPL, stage)
    stage = re.sub(_PREPOS_PATT, _PREPOS_REPL, stage)
    stage = re.sub(_FINAL_PATT, _final_replacement, stage)
    stage = re.sub(_LAOY_PATT, _LAOY_REPL, stage)
    stage = re.sub(_DD75_PATT, _dd75_replacement, stage)
    stage = re.sub(_OVER_UNDER_PATT, _OVER_UNDER_REPL, stage)
    stage = stage.replace("81" + "11", "11" + "81")  # rev-ger_m becomes ger_m-rev
    return stage


def uword(mcword: str):
    return uword_x(_TRANSLATION_TABLE, mcword)


def uword_retaining_slash(mcword: str):
    return uword_x(_TRANSLATION_TABLE_RETAINING_SLASH, mcword)


def uword_x(ttab, mcword: str):
    if mcword in _PASS_THRUS:
        return mcword
    stage = tword(mcword)
    stage = stage.translate(ttab)
    return re.sub(r"\d\d", _digits_replacement, stage)


def _sqbrac(guts):
    return f"[{guts}]"


def _sqbrac_not(guts):
    return _sqbrac(f"^{guts}")


def _paren(guts):
    return f"({guts})"


_LETT_GUTS = ")BGDHWZX+YKLMNS(PCQR#&$T"
_LETT_GUTS_NO_VAV = _LETT_GUTS.replace("W", "")
_LETT = _sqbrac(_LETT_GUTS)
_NON_LETT = _sqbrac_not(_LETT_GUTS)
_NON_LETT_STAR = _NON_LETT + "*"
_NON_LETT_STAR_DOLL = _NON_LETT_STAR + "$"
_NON_LETT_NO_DIGIT = _sqbrac_not(_LETT_GUTS + "0123456789")
# _PREPOS_PATT / _PREPOS_REPL are defined below, after _OVER_ACCENTS.
_EARLY_MTG_PATT = '([afeAFE"I:U])95'
_EARLY_MTG_REPL = r"95\1"
_XOLAM_PATT1_END = _sqbrac(_LETT_GUTS_NO_VAV) + '|W[AFE"I:U]'
_XOLAM_PATT1 = "O" + _paren(_NON_LETT_STAR) + _paren(_XOLAM_PATT1_END)
_XOLAM_REPL1 = r"o\1\2"
_XOLAM_PATT2 = "O" + _paren(_NON_LETT_STAR) + "W"
_XOLAM_REPL2 = r"\1WO"
# The precomposed het (U+1E25) here and at the _TRANSLATION_DIC entry below is a
# private single-codepoint *sentinel* for XOLAM_XFV, not transliteration: it must
# be precomposed because it is used as a str.maketrans() key, and maketrans keys
# must be length 1 (a decomposed h+U+0323 would raise ValueError at import).
# This is simply the repo's standard NFC form used deliberately as a sentinel --
# not an exception to it (issue #49).
_XOLAM_PATT3 = "W" + _paren(_NON_LETT_STAR) + "o"
_XOLAM_REPL3 = r"W\1ḥ"
_FINAL_PATT = r"[KMNPC]" + _NON_LETT_STAR_DOLL


def _final_replacement(matchobj):
    nonfinal = matchobj.group()
    return nonfinal.translate(_TRANSLATION_TABLE_FOR_FINAL_FORMS)


def _dd75_replacement(matchobj):
    digit_pair = matchobj.group(1)
    if _ACCENTS[digit_pair] in ha.UNI_OVER_ACCENTS:
        return "75" + digit_pair
    return digit_pair + "75"


def _digits_replacement(matchobj):
    digit_pair = matchobj.group()
    return _ACCENTS[digit_pair]


_TRANSLATION_TABLE_FOR_FINAL_FORMS = str.maketrans(
    {
        "K": "k",
        "M": "m",
        "N": "n",
        "P": "p",
        "C": "c",
    }
)
_TRANSLATION_DIC_RETAINING_SLASH = {
    ")": "א",
    "B": "ב",
    "G": "ג",
    "D": "ד",
    "H": "ה",
    "W": "ו",
    "Z": "ז",
    "X": "ח",
    "+": "ט",
    "Y": "י",
    "K": "כ",
    "k": "ך",
    "L": "ל",
    "M": "מ",
    "m": "ם",
    "N": "נ",
    "n": "ן",
    "S": "ס",
    "(": "ע",
    "P": "פ",
    "p": "ף",
    "C": "צ",
    "c": "ץ",
    "Q": "ק",
    "R": "ר",
    "#": "ש",
    "&": "ש" + hpo.SIND,
    "$": "ש" + hpo.SHIND,
    "T": "ת",
    "A": hpo.PATAX,
    "a": hpo.XPATAX,  # a was :A
    "F": hpo.QAMATS,
    "f": hpo.XQAMATS,  # f was :F
    "E": hpo.SEGOL_V,
    "e": hpo.XSEGOL,  # e was :E
    '"': hpo.TSERE,
    "I": hpo.XIRIQ,
    "O": hpo.XOLAM,
    "o": hpo.XOLAM,
    "ḥ": hpo.XOLAM_XFV,  # precomposed sentinel (maketrans key); see _XOLAM_REPL3 note
    "U": hpo.QUBUTS,
    ":": hpo.SHEVA,
    ".": hpo.DAGOMOSD,
    ",": hpo.RAFE,
    "-": hpu.MAQ,
}
_TRANSLATION_DIC = {
    "/": None,
    **_TRANSLATION_DIC_RETAINING_SLASH,
}
# Official documentation for these M-C 2-digit accent codes lives in two files
# of the WLC distribution (see in/wlc422/):
#   - michigan.man : the Michigan coding manual. The seven same-graphic-form
#     pairs (e.g. zarqa 02 / tsinnorit 82, telisa qaton 04 / medial 24, telisa
#     gadol 14 / medial 44) are defined in section 3.5.5; the "medial" variants
#     24/44 are introduced in the list of code modifications near the top.
#   - supplmt.wts  : the WTS supplement accent table, one line per code with a
#     name and a glyph sketch (e.g. "24  -&-- telisha parvum (med)").
# The per-code comments below record observed usage in the corpus, not the
# official gloss; consult those two files for the authoritative definitions.
_ACCENTS = {
    "00": hpu.SOPA,
    "01": ha.SEG_A,
    "02": ha.Z_OR_TSOR,
    "03": ha.PASH,
    "04": ha.TEL_Q,
    "05": hpu.PASOLEG,
    "10": ha.YET,
    "11": ha.GER_M,
    "12": ha.GER_2,  # garshayim (preposed)
    "13": ha.DEX,
    "14": ha.TEL_G,
    "24": ha.TEL_Q,  # 4 uses as stress-helper to acc04 (24\S+04); 1 use as non-stress-helper
    "33": ha.PASH,  # >3800 uses as stress-helper to acc03 (33\S+03); number of uses as non-stress-helper is unknown (may be 0)
    "35": sd.ZWJ + hpo.MTGOSLQ,  # medial
    "44": ha.TEL_G,  # 1 use as stress-helper to acc14 ([^a-z]14\S+44); 3 uses as non-stress-helper
    "52": hpu.UPDOT,
    "53": hpu.LODOT,
    "60": ha.OLE,
    "61": ha.GER,
    "62": ha.GER_2,
    "63": ha.QOM,
    "64": ha.ILU,
    "65": ha.SHA,
    "70": ha.MAH,
    "71": ha.MER,
    "72": ha.MER_2,
    "73": ha.TIP,
    "74": ha.MUN,
    "75": hpo.MTGOSLQ,  # left (normal)
    "80": ha.ZAQ_Q,
    "81": ha.REV,
    "82": ha.ZSH_OR_TSIT,  # 2 uses as stress-helper to acc02 (82\S+02); >200 uses as tsinnorit; 12 wrong-headed uses as pre-lamed-ascender zarqa
    "83": ha.PAZ,
    "84": ha.QAR,  # aka pazer gadol
    "85": ha.ZAQ_G,
    "91": ha.TEV,
    "92": ha.ATN,
    "93": ha.YBY,  # aka galgal
    "94": ha.DAR,
    "95": hpo.MTGOSLQ,  # right ("early")
}
# uword('A12C34')
# uword('A1234')
_TRANSLATION_TABLE = str.maketrans(_TRANSLATION_DIC)
_TRANSLATION_TABLE_RETAINING_SLASH = str.maketrans(_TRANSLATION_DIC_RETAINING_SLASH)
_PASS_THRUS = {"*kk", "**qq"}
_OVER_ACCENTS = [a for a in _ACCENTS.keys() if _ACCENTS[a] in ha.UNI_OVER_ACCENTS]
_UNDER_ACCENTS = [a for a in _ACCENTS.keys() if _ACCENTS[a] in ha.UNI_UNDER_ACCENTS]
_OA_PM = [*_OVER_ACCENTS, "75"]  # over-accents plus "mos" (meteg or silluq)
# XXX Normal meteg (75) is treated like an over-accent, i.e. like O in LAYO!
_OA_PM_PATT = _paren("|".join(_OA_PM))
_LAOY_PATT = r"L([AF])" + _OA_PM_PATT + r"([I:])"
_LAOY_REPL = r"L\1\3\2"
_DD75_PATT = r"(\d\d)75"
_OACCENTS_PATT = _paren("|".join(_OVER_ACCENTS))
# BIL ("before-its-letter") accent relocation. A BIL code (10-14) floats
# rightward past its letter and the letter's points, meteg, and below-accents,
# but STOPS before a co-located over-accent (e.g. telisha gedola 44). Stopping
# there preserves the source order of two over-accents sharing one letter, so the
# three same-letter telg!gerstar words (gn5:29, zp2:15, 2k17:13) stay
# gerstar-then-telg (manuscript order) instead of being permuted to telg-first.
_PREPOS_FLOAT = (
    "(?:" + _NON_LETT_NO_DIGIT + r"|(?!" + "|".join(_OVER_ACCENTS) + r")\d\d)*"
)
_PREPOS_PATT = r"^(\*\*|)(10|11|12|13|14)" + _paren(_LETT + _PREPOS_FLOAT)
_PREPOS_REPL = r"\1\3\2"
_UACCENTS_PATT = _paren("|".join(_UNDER_ACCENTS))
_OVER_UNDER_PATT = _OACCENTS_PATT + _UACCENTS_PATT
_OVER_UNDER_REPL = r"\2\1"
