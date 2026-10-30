"""Level 5: the kinds a stroke group may have, each congruent to a code point.

A kind names a sign instance as a reader would, "tav letter" or "qamats vowel",
without linking it to any transcription (Ben, 2026-10-30: linking is a later
level).  Each kind gives the Unicode name it is congruent to, or None where the
kind leaves the sign undetermined, and the nib a stroke of it is written with.
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
    "pashta accent": "HEBREW ACCENT PASHTA",
    "qadma accent": "HEBREW ACCENT QADMA",
    "tevir accent": "HEBREW ACCENT TEVIR",
    "tipeḥa accent": "HEBREW ACCENT TIPEHA",
    "munaḥ accent": "HEBREW ACCENT MUNAH",
    "merkha accent": "HEBREW ACCENT MERKHA",
    "mahapakh accent": "HEBREW ACCENT MAHAPAKH",
    "zaqef accent": "HEBREW ACCENT ZAQEF QATAN",
    "bar under the letter": None,
    "bar over the letter": None,
    "dot under the letter": None,
    "dot over the letter": None,
    "unidentified mark": None,
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


def nib_class(kind):
    """The nib a stroke of this kind is written with; an unknown kind raises."""
    if kind not in KINDS:
        raise ValueError(f"unknown stroke-group kind {kind!r}")
    return KINDS[kind][1]
