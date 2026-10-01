import yeivin_itm.helpers as hlp


def sigil(sigil):
    expansion = _MANUS[sigil]
    return hlp.abbr_tit("μ" + sigil, expansion)  # e.g. μA


_MS_B3 = "Leningrad MS B3, a codex of the"
_MANUS = {
    "A": "Aleppo Codex (see section #26)",
    "B": "British Museum MS Or. 4445 (see section #31)",
    "C": "Cairo Codex of The Prophets (see section #32)",
    "L": "Leningrad MS B19a (see section #30)",
    "L1": "Leningrad Firkowitsch II.17 (see section #36)",
    "L2": "Leningrad Firkowitsch II.159 (see section #37)",
    "L6": "Leningrad Firkowitsch II.115 (see section #41)",
    "L10": "Leningrad Firkowitsch II.1283 (see section #43)",
    "L13": "Leningrad Firkowitsch II.34 (see section #46)",
    "L15": "Leningrad Museum of the Peoples of Asia MS 62 (see section #47)",
    "L18": "Leningrad Firkowitsch I.59 (see section #50)",
    "L20": "Leningrad Firkowitsch II.9 (see section #51)",
    "N": "New York, Jewish Theological Seminary MS 232 (see section #53) ",
    "P": f"[{_MS_B3}] Prophets with Babylonian vowel signs, dated 1228 S.E. = 916 C.E",
    # I have no "see section N" for P because I couldn't find any mention of P in a numbered section.
    "S": "[formerly] Sassoon 507; now Jer. Nat. Uni. & Lib. Heb 24° 5702 (see section #33)",
    "S1": "Sassoon 1053 (see section #34) ",
    "R": "[Karlsruhe MS #3. Codex] Reuchlinianus of the Prophets, dated 1105-6. “Expanded Tiberian” pointing.",
    # I have no "see section N" for R because I couldn't find any mention of R in a numbered section.
}
