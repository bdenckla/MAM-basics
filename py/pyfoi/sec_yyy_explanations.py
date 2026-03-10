def _wrap(inner):
    return f"{_IN_DET}, {inner}. {_A_SBR}"


_A_SBR_RAW = """
The “profile” is the accent/mqf/mtg profile.
Comma means one or more letters (but no mqf marks) intervene;
dash means exactly one maqaf intervenes.
Breuer references (if any) are listed alongside examples"""
_A_SBR = _A_SBR_RAW.replace("\n", " ").strip()
_IN_DET = "that the profile ends in atn and is, in detail"
_NOTHING = "where “nothing” means an atom with no marks of note"
#
#
_MER_C_ATN = _wrap("mer,atn")
_MER_D_ATN = _wrap("mer-atn")
_D_MER_C_MTG_C_ATN = _wrap("nothing-(mer,mtg,atn) " + _NOTHING)
EXPLANATIONS = {
    ("poetic", "b-(atn)", "(mer),(atn)"): _MER_C_ATN,
    ("poetic", "b-(atn)", "(mer)-(atn)"): _MER_D_ATN,
    ("poetic", "b-(atn)", "-(mer),(ümtg),(atn)"): _D_MER_C_MTG_C_ATN,
}
