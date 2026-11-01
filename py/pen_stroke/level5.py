"""Level 5: the kinds a stroke group may have, each congruent to a code point.

A kind names a sign instance as a reader would, "tav letter" or "qamats vowel",
without linking it to any transcription (Ben, 2026-10-30: linking is a later
level).  Each kind gives the Unicode name it is congruent to, or None where the
kind leaves the sign undetermined, and the pass its strokes belong to: the
letters, or the marks written over and under them.
"""

import unicodedata

LETTERS = "letters"
MARKS = "marks"

_LETTER_NAMES = {
    "alef": "ALEF",
    "bet": "BET",
    "gimel": "GIMEL",
    "dalet": "DALET",
    "he": "HE",
    "vav": "VAV",
    "zayin": "ZAYIN",
    "ḥet": "HET",
    "tet": "TET",
    "yod": "YOD",
    "final kaf": "FINAL KAF",
    "kaf": "KAF",
    "lamed": "LAMED",
    "final mem": "FINAL MEM",
    "mem": "MEM",
    "final nun": "FINAL NUN",
    "nun": "NUN",
    "samekh": "SAMEKH",
    "ayin": "AYIN",
    "final pe": "FINAL PE",
    "pe": "PE",
    "final tsadi": "FINAL TSADI",
    "tsadi": "TSADI",
    "qof": "QOF",
    "resh": "RESH",
    "shin": "SHIN",
    "tav": "TAV",
}

_MARK_KINDS = {
    "sheva mark": "HEBREW POINT SHEVA",
    "ḥiriq vowel": "HEBREW POINT HIRIQ",
    "tsere vowel": "HEBREW POINT TSERE",
    "segol vowel": "HEBREW POINT SEGOL",
    "pataḥ vowel": "HEBREW POINT PATAH",
    "qamats vowel": "HEBREW POINT QAMATS",
    "ḥolam dot": "HEBREW POINT HOLAM",
    "qubuts vowel": "HEBREW POINT QUBUTS",
    "ḥataf pataḥ vowel": "HEBREW POINT HATAF PATAH",
    "dagesh mark": "HEBREW POINT DAGESH OR MAPIQ",
    "shuruq dot": "HEBREW POINT DAGESH OR MAPIQ",
    "shin dot": "HEBREW POINT SHIN DOT",
    "sin dot": "HEBREW POINT SIN DOT",
    "meteg mark": "HEBREW POINT METEG",
    "silluq accent": "HEBREW POINT METEG",
    "maqaf mark": "HEBREW PUNCTUATION MAQAF",
    "sof pasuq mark": "HEBREW PUNCTUATION SOF PASUQ",
    "paseq mark": "HEBREW PUNCTUATION PASEQ",
    "atnaḥ accent": "HEBREW ACCENT ETNAHTA",
    "revia accent": "HEBREW ACCENT REVIA",
    "geresh accent": "HEBREW ACCENT GERESH",
    "gershayim accent": "HEBREW ACCENT GERSHAYIM",
    "darga accent": "HEBREW ACCENT DARGA",
    "pashta accent": "HEBREW ACCENT PASHTA",
    "qadma accent": "HEBREW ACCENT QADMA",
    "tevir accent": "HEBREW ACCENT TEVIR",
    "tipeḥa accent": "HEBREW ACCENT TIPEHA",
    "munaḥ accent": "HEBREW ACCENT MUNAH",
    "merkha accent": "HEBREW ACCENT MERKHA",
    "mahapakh accent": "HEBREW ACCENT MAHAPAKH",
    "zaqef accent": "HEBREW ACCENT ZAQEF QATAN",
    "masora circle mark": "HEBREW MARK MASORA CIRCLE",
    "bar under the letter": None,
    "bar over the letter": None,
    "dot under the letter": None,
    "dot over the letter": None,
    "unidentified mark": None,
    # Ink that is likely unintentional, a stray bit of ink rather than a sign: transcribed,
    # since it is ink, and marked as likely stray (Ben, 2026-10-31).
    "stray mark": None,
}

KINDS = {
    f"{name} letter": (f"HEBREW LETTER {uni}", LETTERS)
    for name, uni in _LETTER_NAMES.items()
}
# Part of a letter that a crop's edge cuts too short to name, such as the top of a
# letter of the next line.
KINDS["unidentified letter"] = (None, LETTERS)
KINDS.update({kind: (uni, MARKS) for kind, uni in _MARK_KINDS.items()})

for _kind, (_uni, _nib) in KINDS.items():
    if _uni is not None:
        unicodedata.lookup(_uni)

# The parts rule of the ink-region profile (doc/ink-region-representation.md): how
# many written parts, shapes this manuscript writes apart, a sign of each kind has.
# None where the kind has no count: a letter, a kind that leaves the sign
# undetermined, and ink set aside.
_MARK_PARTS = {
    "sheva mark": 2,  # two dots, one over the other
    "ḥiriq vowel": 1,
    "tsere vowel": 2,  # two dots side by side
    "segol vowel": 3,  # three dots
    "pataḥ vowel": 1,
    "qamats vowel": 2,  # a bar and a dot under it
    "ḥolam dot": 1,
    "qubuts vowel": 3,  # three dots on a slant
    "ḥataf pataḥ vowel": 3,  # a bar and the two dots of a sheva
    "dagesh mark": 1,
    "shuruq dot": 1,
    "shin dot": 1,
    "sin dot": 1,
    "meteg mark": 1,
    "silluq accent": 1,
    "maqaf mark": 1,
    "sof pasuq mark": 2,  # two dots, one over the other
    "paseq mark": 1,
    "atnaḥ accent": 1,
    "revia accent": 1,
    "geresh accent": 1,
    "gershayim accent": 2,  # two strokes side by side
    "darga accent": 1,
    "pashta accent": 1,
    "qadma accent": 1,
    "tevir accent": 2,  # a stroke and a dot
    "tipeḥa accent": 1,
    "munaḥ accent": 1,
    "merkha accent": 1,
    "mahapakh accent": 1,
    "zaqef accent": 2,  # two dots, one over the other
    "masora circle mark": None,
    "bar under the letter": 1,
    "bar over the letter": 1,
    "dot under the letter": 1,
    "dot over the letter": 1,
    "unidentified mark": None,
    "stray mark": None,
}
PARTS = {kind: None for kind in KINDS if KINDS[kind][1] == LETTERS}
PARTS.update(_MARK_PARTS)
if set(PARTS) != set(KINDS):
    raise ValueError("the parts table and the kinds disagree")


def pass_of(kind):
    """The pass a stroke of this kind belongs to; an unknown kind raises."""
    if kind not in KINDS:
        raise ValueError(f"unknown stroke-group kind {kind!r}")
    return KINDS[kind][1]


def parts_of(kind):
    """How many written parts a sign of this kind has, or None where the kind has
    no count; an unknown kind raises."""
    if kind not in PARTS:
        raise ValueError(f"unknown stroke-group kind {kind!r}")
    return PARTS[kind]
