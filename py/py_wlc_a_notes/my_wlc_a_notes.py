"""Exports RECORDS."""


def _does_not_carry(mpk_letter, qere_letter, mark="dagesh"):
    return (
        f"The MPK’s {mpk_letter} does not carry a {mark} for the qere’s {qere_letter}, "
    )


def _does_not_carry_pi(mpk_letter, qere_letter, mark="dagesh"):
    return (
        _does_not_carry(mpk_letter, qere_letter, mark)
        + "perhaps because that would be illegal."
    )


def _has_no_letter_to_carry(qere_letter, mark="dagesh"):
    return f"The MPK has no letter to carry a {mark} for the qere’s {qere_letter}."


def _has_no_letters_at_all(qere_letter, points, mark="dagesh"):
    return (
        _has_no_letter_to_carry(qere_letter, mark) + " "
        f"The MPK (points on no letters) is {points}."
    )


def _unlike(mark, where):
    return (
        f"Unlike the dagesh, the {mark} does not need a letter to carry it; it is allowed to be an orphan. "
        f"It appears {where}. "
        f"Unlike the manuscript, our MPK shows that orphan {mark} on a dotted circle."
    )


def _between(mark1, mark2, lett1, lett2):
    return (
        f"between the {mark1} and the {mark2} (of the {lett1} and {lett2} respectively)"
    )


_QUBUTS_TO_SHURUQ_REMARK = "The qubuts in the MPK becomes a shuruq dot in the qere."
_WLC_C_BRACKET_NOTE_DEFINITION = (
    "We read an accent in ל differently from BHS. "
    + "(This is similar to the note “]C”, "
    + "but the latter refers to accent differences against BHQ.)"
)
_WLC_1_BRACKET_NOTE_DEFINITION = (
    "BHS has been faithful to ל [...] "
    + "where there might be a question of the validity of the form "
    + "and we keep the same form as BHS. "
    + "(This is similar to the note “]U”, but the latter refers to cases where "
    + "BHQ has been published and we keep the same form as both BHS and BHQ.)"
)
_DOTAN_PAGE_XX_QUOTE = (
    "Another example [of a point created ex nihilo] is "
    "an ʿayin of the ketiv that cannot carry a dagesh that is due in the qere, "
    "as in the manuscript in Deut. 28:27 "
    "in the [body] text @וּבַעְפֹלִים# and "
    "in the margin ק̇ ובטחרים; "
    "in the printed edition a dagesh was added[, yielding] @וּבַטְּחֹרִים#."
)
_DOTAN_PAGE_XX = (
    "Dotan remarks, in his Foreword to BHL (page xx):",
    #
    {"sn-blockquote": _DOTAN_PAGE_XX_QUOTE},
    #
    "(In this quote, Dotan omits the accent (zaqef qatan) on "
    "the ל of @וּבַעְפֹלִים# and on "
    "the ר of @וּבַטְּחֹרִים#, "
    "perhaps because it is not germane to the topic at hand.)",
    #
    "Dotan’s example from dt28:27 is not a-noted in WLC, which has merely the following:",
    #
    {"sn-blockquote": "*W/B/(PLYM **W./BA/+.:XORI80YM"},
)

RECORD_01 = {
    "wlc-index": 1,
    "uxlc-change-proposal": 101,
    "bcv": "gn27:29",
    "img": "01-gn27v29.png",
    "folio": "Folio_016A",
    "column": 2,
    "line": 4,
    "qere": "וְיִֽשְׁתַּחֲו֤וּ",
    "MPK": "וְיִֽשְׁתַּחֲוֻ֤",
    "at issue": "וּ",
    "summary": "אֻ/אוּ",
    "remarks": [_QUBUTS_TO_SHURUQ_REMARK],
    "side-notes": [
        "Although Dotan does not note this word, "
        "he notes a later version of this word in this verse, @וְיִשְׁתַּחֲוּ֥וּ#. "
        "Presumably he notes this later word for the unexpected dagesh in its next-to-last vav. "
        "This later word is a normal (non-qere) word."
    ],
}
RECORD_02 = {
    "wlc-index": 2,
    "uxlc-change-proposal": 102,
    "bcv": "gn43:28",
    "img": "02-gn43v28.png",
    "folio": "Folio_027A",
    "column": 3,
    "line": 15,
    "qere": "וַיִּֽשְׁתַּחֲוּֽוּ׃",
    "MPK": "וַיִּֽשְׁתַּחֲוֻּֽ׃",
    "at issue": "וּ",
    "summary": "אֻ/אוּ",
    "remarks": [_QUBUTS_TO_SHURUQ_REMARK],
    "side-notes": [
        "In WLC, this word has not only an a-note but also a 1-note, "
        "presumably because of the unexpected dagesh in the qere’s next-to-last vav.",
        #
        "As a reminder, a WLC 1-note (bracket-1 note) is defined as follows:",
        {"sn-blockquote": _WLC_1_BRACKET_NOTE_DEFINITION},
        #
        "Although Dotan has a note about this ketiv/qere, "
        "I do not take him to have noted it for the issue at hand: "
        "the qubuts-to-shuruq issue. "
        "I take him to have noted this ketiv/qere "
        "only for the unexpected dagesh in the last vav of the MPK. "
        "(This implies a dagesh in the qere’s next-to-last vav.)",
        #
        "I do not think Dotan finds the qubuts-to-shuruq issue notable "
        "because he does not note the similar ketiv/qere "
        "in gn27:29 words 3 and 4, @וישתחו/וְיִֽשְׁתַּחֲו֤וּ#. "
        "That gn27:29 ketiv/qere has the same qubuts-to-shuruq pattern as this one "
        "except the next-to-last vav of its qere is free of a dagesh, as expected, "
        "and therefore Dotan finds nothing notable about it.",
        #
        "We know that Dotan finds the dagesh notable "
        "because he notes gn27:29 word 10, @וְיִשְׁתַּחֲוּ֥וּ#, "
        "a normal (non-qere) word that is analogous to this qere, "
        "including having an unexpected dagesh in its next-to-last vav.",
    ],
}
RECORD_03 = {
    "wlc-index": 3,
    "uxlc-change-proposal": 201,
    "bcv": "ex4:2",
    "img": "03-ex4v2.png",
    "folio": "Folio_033A",
    "column": 1,
    "line": 27,
    "qere": "מַה־זֶּ֣ה",
    "qere-atom-at-issue": "מַה־",
    "MPK": "מַזֶּ֣ה",
    "at issue": "־",
    "summary": "+mqf",
    "remarks": [],
}
RECORD_04 = {
    "wlc-index": 4,
    "uxlc-change-proposal": 301,
    "bcv": "js22:7",
    "img": "04-js22v7.png",
    "folio": "Folio_133B",
    "column": 3,
    "line": 10,
    "Dotan": "UXLC disagrees with BHL Appendix A",
    "qere": "בְּעֵ֥בֶר",
    "MPK": "מְעֵ֥בֶר",
    "at issue": "בּ",
    "summary": "+dg",
    "remarks": [_does_not_carry("מ", "ב") + "for some reason."],
    "side-notes": [
        "This is the dual of js24:15.",
        #
        "Dotan notes that strictly speaking, the implied qere is "
        "@בְעֵ֥בֶר#, which leaves the ב unexpectedly free of a dagesh.",
    ],
}
RECORD_05 = {
    "wlc-index": 5,
    "uxlc-change-proposal": 302,
    "bcv": "js24:15",
    "img": "05-js24v15.png",
    "folio": "Folio_135B",
    "column": 1,
    "line": 2,
    "Dotan": "UXLC disagrees with BHL Appendix A",
    "qere": "מֵעֵ֣בֶר",
    "MPK": "בְּעֵ֥בֶר",
    "at issue": "מ",
    "summary": "-dg",
    "remarks": [
        "The MPK’s בּ seems to carry a dagesh for the qere’s מ but it is rejected."
    ],
    "side-notes": [
        "This is the dual of js22:7.",
        "Dotan notes that strictly speaking, the implied qere is "
        "@מֵּעֵ֣בֶר#, which gives the מ an unexpected dagesh.",
    ],
}
RECORD_06 = {
    "wlc-index": 6,
    "uxlc-change-proposal": 401,
    "bcv": "ju20:13",
    "img": "06-ju20v13.png",
    "folio": "Folio_149A",
    "column": 1,
    "line": 8,
    "qere": "בְּנֵ֣י",
    "MPK": (
        "\N{DOTTED CIRCLE}\N{HEBREW POINT SHEVA}"
        "\N{DOTTED CIRCLE}\N{HEBREW POINT TSERE}\N{HEBREW ACCENT MUNAH}"
        "\N{DOTTED CIRCLE}"
    ),
    "at issue": "בּ",
    "summary": "+dg",
    "remarks": [_has_no_letters_at_all("ב", "sheva, tsere, and munaḥ")],
    "side-notes": [
        "Why in the margin does it say not only «בני קר ולא כת» but also «בני ק»?",
        #
        "Although Dotan does not note this word, "
        "he notes that the next word has an unexpected dagesh in its ב. "
        "I.e., it unexpectedly starts with בּ not ב. "
        "i.e. @בִנְיָמִ֔ן# (Vinyamin) would be expected.",
    ],
}
RECORD_07 = {
    "wlc-index": 7,
    "uxlc-change-proposal": 103,
    "bcv": "ju21:20",
    "img": "07-ju21v20.png",
    "folio": "Folio_150A",
    "column": 2,
    "line": 8,
    "qere": "וַיְצַוּ֕וּ",
    "MPK": "וַיְצַוֻּ֕",
    "at issue": "וּ",
    "summary": "אֻ/אוּ",
    "remarks": [_QUBUTS_TO_SHURUQ_REMARK],
}
RECORD_08 = {
    "wlc-index": 8,
    "uxlc-change-proposal": 501,
    "bcv": "1s5:6",
    "img": "08-1s5v6.png",
    "folio": "Folio_152B",
    "column": 1,
    "line-excluding-blanks": 26,
    "line-including-blanks": 27,
    "qere": "בַּטְּחֹרִ֔ים",
    "MPK": "בַּעְפֹלִ֔ים",
    "at issue": "טּ",
    "summary": "+dg",
    "remarks": [_does_not_carry_pi("ע", "ט")],
    "side-notes": [
        "Same issue, indeed same word modulo accent, six verses later, in 5:12.",
        #
        *_DOTAN_PAGE_XX,
    ],
}
RECORD_09 = {
    "wlc-index": 9,
    "uxlc-change-proposal": 502,
    "bcv": "1s5:12",
    "img": "09-1s5v12.png",
    "folio": "Folio_152B",
    "column": 2,
    "line": 27,
    "qere": "בַּטְּחֹרִ֑ים",
    "MPK": "בַּעְפֹלִ֑ים",
    "at issue": "טּ",
    "summary": "+dg",
    "remarks": [_does_not_carry_pi("ע", "ט")],
    "side-notes": [
        "Same issue, indeed same word modulo accent, six verses before, in 5:6.",
        #
        *_DOTAN_PAGE_XX,
    ],
}
RECORD_10 = {
    "wlc-index": 10,
    "uxlc-change-proposal": "2024.04.01/2024.01.14-1",
    "bcv": "1s9:1",
    "img": "10-1s9v1.png",
    "folio": "Folio_154A",
    "column": 2,
    "line-excluding-blanks": 4,
    "line-including-blanks": 5,
    "Dotan": "UXLC disagrees with BHL Appendix A",
    "qere": "מִבִּנְיָמִ֗ין",
    "MPK": "מִבִּן־יָמִ֗ין",
    "at issue": "נְ",
    "summary": "+shva",
    "remarks": [_does_not_carry_pi("ן in מבן", "נ", "sheva")],
    "side-notes": [
        "Also, understandably, the maqaf disappears from the MPK when forming the implied qere. "
        "It is unclear why the maqaf is supplied in the first place. "
        "Perhaps it is supplied because without it, @מִבִּן# would be illegal: "
        "a word without an accent.",
        #
        "Dotan notes that strictly speaking, the implied qere is "
        "@מִבִּניָמִ֗ין#, which leaves the נ unexpectedly free of a sheva.",
    ],
}
RECORD_11 = {
    "wlc-index": 11,
    "uxlc-change-proposal": 104,
    "bcv": "1s12:10",
    "img": "11-1s12v10.png",
    "folio": "Folio_156A",
    "column": 1,
    "line": 5,
    "qere": "וַיֹּאמְר֣וּ",
    "MPK": "וַיֹּאמְרֻ֣",
    "at issue": "וּ",
    "summary": "אֻ/אוּ",
    "remarks": [_QUBUTS_TO_SHURUQ_REMARK],
}
RECORD_12 = {
    "wlc-index": 12,
    "uxlc-change-proposal": 105,
    "bcv": "1s13:19",
    "img": "12-1s13v19.png",
    "folio": "Folio_156B",
    "column": 2,
    "line-excluding-blanks": 22,
    "line-including-blanks": 23,
    "qere": "אָמְר֣וּ",
    "MPK": "אָמְרֻ֣",
    "at issue": "וּ",
    "summary": "אֻ/אוּ",
    "remarks": [_QUBUTS_TO_SHURUQ_REMARK],
    "side-notes": [
        "There’s a large, clear dot above the ר; "
        "I don’t know what it is supposed to mean, if anything. "
        "Surely not a revia!"
    ],
}
RECORD_13 = {
    "wlc-index": 13,
    "uxlc-change-proposal": 600,
    "bcv": "1s17:23",
    "img": "13-1s17v23.png",
    "folio": "Folio_159B",
    "column": 2,
    "line": 11,
    "Dotan": "UXLC disagrees with BHL Appendix A",
    "qere": "מִמַּעַרְכ֣וֹת",
    "MPK": "מִמַּעֲרְ֣וֹת",
    "at issue": "עַ",
    "summary": "עֲ/עַ",
    "remarks": ["The MPK’s ע has a ḥataf pataḥ where the qere has a pataḥ."],
    "side-notes": [
        "Unexpected ḥataf vowels are a known feature (bug?) of ל. "
        "I.e. this is rare but hardly unique. "
        "This unexpected ḥataf may well be unrelated "
        "to the ketiv/qere differences in this word. "
        "If it is unrelated, "
        "this should have been a bracket-1 or bracket-U note in WLC, not a bracket-a note.",
        #
        "Breuer notes that א and ק have the expected pataḥ under ע. "
        "(א is the Aleppo Codex and ק is the Cairo Codex of The Prophets.)",
        #
        "Dotan notes that strictly speaking, the implied qere is "
        "@מִמַּעֲרְכ֣וֹת# (ḥataf pataḥ under ע).",
    ],
}
RECORD_14 = {
    "wlc-index": 14,
    "uxlc-change-proposal": 452,
    "bcv": "2s3:2",
    "img": "14-2s3v2.png",
    "folio": "Folio_169B",
    "column": 3,
    "line": 11,
    "qere": "וַיִּוָּלְד֧וּ",
    "MPK": ("וַיִּ" "\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}" "לְד֧וּ"),
    "at issue": "וָּ",
    "summary": "+dg",
    "remarks": [_has_no_letter_to_carry("וָּ")],
    "side-notes": [_unlike("qamats", _between("ḥiriq", "sheva", "yod", "ל"))],
}
RECORD_15 = {
    "wlc-index": 15,
    "uxlc-change-proposal": 403,
    "bcv": "2s8:3",
    "img": "15-2s8v3.png",
    "folio": "Folio_172B",
    "column": 2,
    "line": 20,
    "qere": "פְּרָֽת׃",
    "MPK": (
        "\N{DOTTED CIRCLE}\N{HEBREW POINT SHEVA}"
        "\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}\N{HEBREW POINT METEG}"
        "\N{DOTTED CIRCLE}"
        "׃"
    ),
    "at issue": "פּ",
    "summary": "+dg",
    "remarks": [_has_no_letters_at_all("פ", "sheva, qamats, and siluq")],
}
RECORD_16 = {
    "wlc-index": 16,
    "uxlc-change-proposal": 412,
    "bcv": "2s18:20",
    "imgs": {
        "LC": "16-2s18v20-L.png",
        "BHS": "16-2s18v20-BHS.jpg",  # JPG for some reason
        "AC": "16-2s18v20-A.png",
    },
    "folio": "Folio_179A",
    "column": 3,
    "line": 10,
    "qere-context": "כִּֽי־עַל־כֵּ֥ן",
    "qere": "כֵּ֥ן",
    "MPK": (
        "\N{DOTTED CIRCLE}\N{HEBREW POINT TSERE}\N{HEBREW ACCENT MUNAH}"
        "\N{DOTTED CIRCLE}"
    ),
    "at issue": "כּ",
    "summary": "+dg",
    "remarks": [_has_no_letters_at_all("כ", "tsere and merkha")],
    "side-notes": [
        "Dotan notes that strictly speaking, the implied qere and the atom preceding it "
        "form the phrase @עַל כֵ֥ן#. "
        "(This implies the more complete phrase @כִּֽי־עַל כֵ֥ן#.) "
        "I do not take him to find @עַל כֵ֥ן# notable for the issue at hand: "
        "the lack of a dagesh in the כ of the implied qere @כֵ֥ן#. "
        "I take him to find the phrase @עַל כֵ֥ן# notable "
        "only because its atoms are, unexpectedly, separated merely by a space rather than a maqaf.",
        #
        "Note that, contrary to UXLC, @עַל# is a normal atom, i.e. it is not part of a ketiv/qere. "
        "It is abnormal only in that it precedes a qere velo ketiv. "
        "I.e. UXLC has <k>@על#</k><q>@עַל־#</q> where I think it should merely have <w>@עַל־#</w>.",
        #
        "The manuscript’s lack of a trailing maqaf on @עַל# "
        "is the subject of a currently-pending "
        "change proposal, 2024.04.01/2024.01.18-2.",
    ],
}
RECORD_17 = {
    "wlc-index": 17,
    "uxlc-change-proposal": 454,
    "bcv": "2s21:9",
    "img": "17-2s21v9.png",
    "folio": "Folio_181B",
    "column": 1,
    "line": 26,
    "qere": "בִּתְחִלַּ֖ת",
    "MPK": "\N{DOTTED CIRCLE}\N{HEBREW POINT HIRIQ}תְחִלַּ֖ת",
    "at issue": "בּ",
    "summary": "+dg",
    "remarks": [_has_no_letter_to_carry("ב")],
    "side-notes": [_unlike("ḥiriq", "before the sheva of the initial ת")],
}
RECORD_18 = {
    "wlc-index": 18,
    "uxlc-change-proposal": 455,
    "bcv": "2s22:8",
    "img": "18-2s22v8.png",
    "folio": "Folio_182A",
    "column": 1,
    "line": 11,
    "column-remark": "This page has only one column. It has a river of whitespace through its middle.",
    "qere": "וַיִּתְגָּעַ֤שׁ",
    "MPK": ("וַ" "\N{DOTTED CIRCLE}\N{HEBREW POINT HIRIQ}" "תְגָּעַ֤שׁ"),
    "at issue": "יּ",
    "summary": "+dg",
    "remarks": [_has_no_letter_to_carry("yod")],
    "side-notes": [_unlike("ḥiriq", _between("pataḥ", "sheva", "vav", "ת"))],
}
RECORD_19 = {
    "wlc-index": 19,
    "uxlc-change-proposal": 503,
    "bcv": "1k7:45",
    "img": "19-1k7v45.png",
    "folio": "Folio_189B",
    "column": 3,
    "line": 15,
    "qere": "הָאֵ֔לֶּה",
    "MPK": "הָאֵ֔הֶה",
    "at issue": "לּ",
    "summary": "+dg",
    "remarks": [_does_not_carry_pi("ה", "ל")],
}
RECORD_20 = {
    "wlc-index": 20,
    "uxlc-change-proposal": None,
    "bcv": "1k9:9",
    "img": "20-1k9v9.png",
    "folio": "Folio_191B",
    "column": 3,
    "line": 10,
    "qere": "וַיִּשְׁתַּחֲו֥וּ",
    "MPK": "וַיִּשְׁתַּחֲוּ֥",
    "at issue": "?",
    "summary": "?",
    "remarks": ["I don’t see what motivates WLC’s a-note on this word."],
    "side-notes": [
        "I don’t see what motivates the a-note because "
        "the MPK has all the qere’s marks, "
        "as long as we interpret the MPK’s dot in the vav to be "
        "a shuruq dot not a dagesh.",
        #
        "The MPK suffix @וּ֥ #becomes @ו֥וּ# in the qere. "
        "In contrast, on closely-analogous words, gn27:29 and gn43:28 use a qubuts: "
        "@וֻ֤ #becomes @ו֤וּ# and "
        "@וֻּֽ׃ #becomes @וּֽוּ׃# respectively.",
        #
        "BTW no shin dot is visible, although a shin dot might be hard to see here. "
        "The condition of the manuscript is not great here. "
        "The focus of the photograph is also not great here.",
    ],
}
RECORD_21 = {
    "wlc-index": 21,
    "uxlc-change-proposal": 106,
    "bcv": "1k12:7",
    "img": "21-1k12v7.png",
    "folio": "Folio_194A",
    "column": 1,
    "line": 3,
    "qere": "וַיְדַבְּר֨וּ",
    "MPK": "וַיְדַבְּרֻ֨",
    "at issue": "וּ",
    "summary": "אֻ/אוּ",
    "remarks": [_QUBUTS_TO_SHURUQ_REMARK],
    "side-notes": [
        "In WLC, this word has not only an a-note but also a c-note, "
        "presumably because WLC has qadma where BHS (in error) has pashta.",
        #
        "As a reminder, a WLC c-note (bracket-c note) is defined as follows:",
        {"sn-blockquote": _WLC_C_BRACKET_NOTE_DEFINITION},
    ],
}
RECORD_22 = {
    "wlc-index": 22,
    "uxlc-change-proposal": 504,
    "bcv": "2k4:3",
    "img": "22-2k4v3.png",
    "folio": "Folio_204A",
    "column": 3,
    "line": 20,
    "qere-context": "כָּל־שְׁכֵנָ֑יִךְ",
    "qere": "שְׁכֵנָ֑יִךְ",
    "MPK": "שְׁכֵנָ֑כִי",
    "at issue": "ךְ",
    "summary": "+shva",
    "remarks": [_does_not_carry_pi("yod", "ך", "sheva")],
}
RECORD_23 = {
    "wlc-index": 23,
    "uxlc-change-proposal": 505,
    "bcv": "2k6:25",
    "img": "23-2k6v25.png",
    "folio": "Folio_206B",
    "column": 1,
    "line": 11,
    "qere": "דִּבְיוֹנִ֖ים",
    "MPK": "חִרְייֹונִ֖ים",
    "at issue": "דּ",
    "summary": "+dg",
    "remarks": [_does_not_carry_pi("ח", "ד")],
    "side-notes": [
        "The ḥolam malei dot on the qere’s vav comes from the (illegal) ḥolam (ḥaser?) dot on the second yod of the MPK!",
        #
        "Instead of being on the second yod of the MPK, why isn’t this dot on the vav of the MPK?",
        #
        "In other words, instead of @חִ רְ י יֹ ו נִ֖ י ם#, why isn’t the MPK @חִ רְ י י וֹ נִ֖ י ם#? "
        "(I have spaced out the letters for clarity.)",
        #
        "More regarding the odd placement of this dot: the last five letters of ketiv and qere, יונים, "
        "are in common between ketiv and qere. "
        "So why not point them in the MPK as they are in the (implied) qere?",
        #
        "Yet another way of stating this question: "
        "I see the ketiv/qere variation in this word as restricted to "
        "the prefixes חרי and דב respectively. "
        "So in the common suffix יונים, i.e. after that variation, "
        "why should the MPK be any different than the (implied) qere?",
    ],
}
RECORD_24 = {
    "wlc-index": 24,
    "uxlc-change-proposal": 430,
    "bcv": "2k19:31",
    "img": "24-2k19v31.png",
    "folio": "Folio_216A",
    "column": 3,
    "line": 22,
    "qere": "צְבָא֖וֹת",
    "MPK": (
        "\N{DOTTED CIRCLE}\N{HEBREW POINT SHEVA}"
        "\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}"
        "\N{DOTTED CIRCLE}\N{HEBREW ACCENT TIPEHA}"
        "\N{DOTTED CIRCLE}"
        "\N{DOTTED CIRCLE}"
    ),
    "at issue": "וֹ",
    "summary": "+ḥlm dt",
    "remarks": [
        _has_no_letters_at_all("vav", "sheva, qamats, and tipeḥa", "ḥolam dot")
    ],
}
RECORD_25 = {
    "wlc-index": 25,
    "uxlc-change-proposal": 406,
    "bcv": "2k19:37",
    "img": "25-2k19v37.png",
    "folio": "Folio_216B",
    "column": 1,
    "line": 14,
    "qere": "בָּנָיו֙",
    "MPK": (
        "\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}"
        "\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}"
        "\N{DOTTED CIRCLE}"
        "\N{DOTTED CIRCLE}\N{HEBREW ACCENT PASHTA}"
    ),
    "at issue": "בּ",
    "summary": "+dg",
    "remarks": [_has_no_letters_at_all("ב", "two qamats marks and pashta")],
    "side-notes": [
        "There is also a dot near the pashta, which we ignore. "
        "I.e. we assume it is not ink, or in any case not intentional."
    ],
}
RECORD_26 = {
    "wlc-index": 26,
    "uxlc-change-proposal": 107,
    "bcv": "2k20:18",
    "img": "26-2k20v18.png",
    "folio": "Folio_217A",
    "column": 1,
    "line": 10,
    "qere": "יִקָּ֑חוּ",
    "MPK": "יִקָּ֑חֻ",
    "at issue": "וּ",
    "summary": "אֻ/אוּ",
    "remarks": [_QUBUTS_TO_SHURUQ_REMARK],
    "side-notes": ["The dagesh in the qof is way off center, but still legit IMO."],
}
RECORD_27 = {
    "wlc-index": 27,
    "uxlc-change-proposal": 303,
    "bcv": "2k23:33",
    "img": "27-2k23v33.png",
    "folio": "Folio_219A",
    "column": 2,
    "line": 12,
    "qere": "מִמְּלֹ֖ךְ",
    "MPK": "בִּמְּלֹ֖ךְ",
    "at issue": "מ",
    "summary": "-dg",
    "remarks": [
        "The MPK’s בּ seems to carry a dagesh for the qere’s מ but it is rejected."
    ],
    "side-notes": [
        "See js24:15, which is similar.",
        "Dotan does not note this case, though he does note js24:15.",
    ],
}
RECORD_28 = {
    "wlc-index": 28,
    "uxlc-change-proposal": 202,
    "bcv": "is3:15",
    "img": "28-is3v15.png",
    "folio": "Folio_221B",
    "column": 2,
    "line": 10,
    "qere": "מַה־לָּכֶם֙",
    "qere-atom-at-issue": "מַה־",
    "MPK": "מַלָּכֶם֙",
    "at issue": "־",
    "summary": "+mqf",
    "remarks": [],
}
RECORD_29 = {
    "wlc-index": 29,
    "uxlc-change-proposal": 203,
    "bcv": "je18:3",
    "img": "29-je18v3.png",
    "folio": "Folio_255A",
    "column": 3,
    "line-excluding-blanks": 5,
    "line-including-blanks": 6,
    "line-remark": "the line at issue isn’t exactly blank; it as a פ with a dot above, indicating a petuḥah division between columns",
    "qere": "וְהִנֵּה־ה֛וּא",
    "qere-atom-at-issue": "וְהִנֵּה־",
    "MPK": "וְהִנֵּה֛וּ",
    "at issue": "־",
    "summary": "+mqf",
    "remarks": [],
}
RECORD_30 = {
    "wlc-index": 30,
    "uxlc-change-proposal": 407,
    "bcv": "je31:38",
    "img": "30-je31v38.png",
    "folio": "Folio_263A",
    "column": 3,
    "line": 7,
    "qere": "בָּאִ֖ים",
    "MPK": (
        "\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}"
        "\N{DOTTED CIRCLE}\N{HEBREW POINT HIRIQ}\N{HEBREW ACCENT TIPEHA}"
        "\N{DOTTED CIRCLE}"
        "\N{DOTTED CIRCLE}"
    ),
    "at issue": "בּ",
    "summary": "+dg",
    "remarks": [_has_no_letters_at_all("ב", "qamats, ḥiriq, and tipeḥa")],
}
RECORD_31 = {
    "wlc-index": 31,
    "uxlc-change-proposal": 450,
    "bcv": "je50:29",
    "img": "31-je50v29.png",
    "folio": "Folio_274A",
    "column": 2,
    "line": 24,
    "qere-context": "אַל־יְהִי־לָהּ֙",
    "qere": "לָהּ֙",
    "MPK": (
        "\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}"
        "\N{DOTTED CIRCLE}\N{HEBREW ACCENT PASHTA}"
    ),
    "at issue": "הּ",
    "summary": "הּ",
    "remarks": [_has_no_letters_at_all("ה", "qamats and pashta", "mapiq")],
}
RECORD_32 = {
    "wlc-index": 32,
    "uxlc-change-proposal": 458,
    "bcv": "ek14:14",
    "img": "32-ek14v14.png",
    "folio": "Folio_282B",
    "column": 2,
    "line": 13,
    "qere": "דָּנִיֵּ֣אל",
    "MPK": (
        "דָּנִ" "\N{DOTTED CIRCLE}\N{HEBREW POINT TSERE}\N{HEBREW ACCENT MUNAH}" "אל"
    ),
    "at issue": "יּ",
    "summary": "+dg",
    "remarks": [_has_no_letter_to_carry("yod")],
}
RECORD_33 = {
    "wlc-index": 33,
    "uxlc-change-proposal": 459,
    "bcv": "ek14:20",
    "img": "33-ek14v20.png",
    "folio": "Folio_282B",
    "column": 3,
    "line": 6,
    "qere": "דָּנִיֵּ֣אל",
    "MPK": (
        "דָּנִ" "\N{DOTTED CIRCLE}\N{HEBREW POINT TSERE}\N{HEBREW ACCENT MUNAH}" "אל"
    ),
    "at issue": "יּ",
    "summary": "+dg",
    "remarks": [_has_no_letter_to_carry("yod")],
}
RECORD_34 = {
    "wlc-index": 34,
    "uxlc-change-proposal": 460,
    "bcv": "ek28:3",
    "img": "34-ek28v3.png",
    "folio": "Folio_291A",
    "column": 1,
    "line": 11,
    "qere": "מִדָּֽנִיֵּ֑אל",
    "MPK": (
        "מִדָּֽנִ"
        "\N{DOTTED CIRCLE}\N{HEBREW POINT TSERE}\N{HEBREW ACCENT ETNAHTA}"
        "אֿל"
    ),
    "at issue": "יּ",
    "summary": "+dg",
    "remarks": [_has_no_letter_to_carry("yod")],
    "side-notes": [
        "The rafeh on the א makes it clear that the qere’s yod functions as a consonant not a vowel, "
        "i.e. the qere’s syllables are @מִ דָּֽ נִ יֵּ֑אל#."
    ],
}
RECORD_35 = {
    "wlc-index": 35,
    "uxlc-change-proposal": 506,
    "bcv": "pr23:26",
    "img": "35-pr23v26.png",
    "folio": "Folio_417B",
    "column": 2,
    "line": 9,
    "qere": "תִּצֹּֽרְנָה׃",
    "MPK": "תִּרֽצְֹנָהֿ׃",
    "at issue": "צּ",
    "summary": "+dg",
    "remarks": [_does_not_carry_pi("ר", "צ")],
    "side-notes": [
        "Nor does the MPK’s צ carry a dagesh for the qere’s צ.",
        #
        "More generally, the MPK is a mess, both in terms of neatness "
        "and in terms of what marks ended up on what letters.",
        #
        "The below-marks make sense, though one has to sort of squint to see what one expects to see. "
        "I.e. the below marks follow the expected order, i.e. the qere order: ḥiriq, siluq, sheva, qamats.",
        #
        "The above-marks is where it gets weird, since the qere צ’s ḥolam ḥaser dot "
        "is already present on the צ of the MPK. "
        "I would expect the ḥolam ḥaser dot to be on the ר of the MPK, i.e. I would expect it to be "
        "in its qere POSITION, not on its qere LETTER. I.e. I would expect @תִּרֹֽצְנָה׃#.",
        #
        "Avi, in the MAM documentation, reports that the MPK of א follows this pattern more completely: "
        "for the two letters at issue in this ketiv/qere, i.e. for the two transposed letters, "
        "the pointing is already present on the LETTER it will “land on” in the qere, "
        "not in the POSITION it will land on in the qere. "
        "That is to say, א-כתיב is @תִּרְצֹּֽנָה׃#. "
        "I.e. to form the pointed qere from the pointed ketiv, all that needs to be done is to "
        "transpose the ר and the צ ALONG with their marks!",
        #
        "Dotan’s Appendix A notes, as I have noted above, that the ḥolam ḥaser dot would be expected "
        "on (the left side of) the ר of the MPK, whereas it is on (the left side of) the צ. "
        "Dotan does not note anything about the creation ex nihilo of the dagesh on the qere’s צ.",
        #
        "A final, unimportant remark is that I’ve put a rafeh above the ה of the MPK "
        "but I’m not sure about this; it might belong above the נ.",
    ],
}
RECORD_36 = {
    "wlc-index": 36,
    "uxlc-change-proposal": 461,
    "bcv": "lm4:16",
    "img": "36-lm4v16.png",
    "folio": "Folio_432A",
    "column": 2,
    "line": 13,
    "qere": "וּזְקֵנִ֖ים",
    "MPK": "זְקֵנִ֖ים",
    "at issue": "וּ",
    "summary": "+shrq dt",
    "remarks": [_has_no_letter_to_carry("vav", "shuruq dot")],
}
RECORD_37 = {
    "wlc-index": 37,
    "uxlc-change-proposal": 108,
    "bcv": "es9:27",
    "img": "37-es9v27.png",
    "folio": "Folio_437B",
    "column": 1,
    "line": 14,
    "qere": "וְקִבְּל֣וּ",
    "MPK": "וְקִבְּלֻ֣",
    "at issue": "וּ",
    "summary": "אֻ/אוּ",
    "remarks": [_QUBUTS_TO_SHURUQ_REMARK],
}
RECORD_38 = {
    "wlc-index": 38,
    "uxlc-change-proposal": 462,
    "bcv": "da2:9",
    "img": "38-da2v9.png",
    "folio": "Folio_438B",
    "column": 1,
    "line": 18,
    "qere": "הִזְדְּמִנְתּוּן֙",
    "MPK": ("הִזְ" "\N{DOTTED CIRCLE}\N{HEBREW POINT SHEVA}" "מִנְתּוּן֙"),
    "at issue": "דּ",
    "summary": "+dg",
    "remarks": [_has_no_letter_to_carry("ד")],
    "side-notes": [_unlike("sheva", _between("sheva", "ḥiriq", "ז", "מ"))],
}
RECORD_39 = {
    "wlc-index": 39,
    "uxlc-change-proposal": 109,
    "bcv": "er3:3",
    "img": "39-er3v3.png",
    "folio": "Folio_449A",
    "column": 1,
    "line": 21,
    "qere": "וַיַּעֲל֨וּ",
    "MPK": "וַיַּעֲלֻ֨",
    "at issue": "וּ",
    "summary": "אֻ/אוּ",
    "remarks": [_QUBUTS_TO_SHURUQ_REMARK],
}
POSITION_RECORDS = [
    {"wlc-index": 1, "qere_atom": "וְיִֽשְׁתַּחֲו֤וּ", "pos-within-verse": 3},
    {"wlc-index": 2, "qere_atom": "וַיִּֽשְׁתַּחֲוּֽוּ׃", "pos-within-verse": 8},
    {"wlc-index": 7, "qere_atom": "וַיְצַוּ֕וּ", "pos-within-verse": 1},
    {"wlc-index": 11, "qere_atom": "וַיֹּאמְר֣וּ", "pos-within-verse": 4},
    {"wlc-index": 12, "qere_atom": "אָמְר֣וּ", "pos-within-verse": 8},
    {"wlc-index": 21, "qere_atom": "וַיְדַבְּר֨וּ", "pos-within-verse": 1},
    {"wlc-index": 26, "qere_atom": "יִקָּ֑חוּ", "pos-within-verse": 7},
    {"wlc-index": 37, "qere_atom": "וְקִבְּל֣וּ", "pos-within-verse": 2},
    {"wlc-index": 39, "qere_atom": "וַיַּעֲל֨וּ", "pos-within-verse": 10},
    {"wlc-index": 3, "qere_atom": "מַה־", "pos-within-verse": 4},
    {"wlc-index": 28, "qere_atom": "מַה־", "pos-within-verse": 1},
    {"wlc-index": 29, "qere_atom": "וְהִנֵּה־", "pos-within-verse": 4},
    {"wlc-index": 4, "qere_atom": "בְּעֵ֥בֶר", "pos-within-verse": 12},
    {"wlc-index": 5, "qere_atom": "מֵעֵ֣בֶר", "pos-within-verse": 20},
    {"wlc-index": 27, "qere_atom": "מִמְּלֹ֖ךְ", "pos-within-verse": 7},
    {"wlc-index": 6, "qere_atom": "בְּנֵ֣י", "pos-within-verse": 15},
    {"wlc-index": 15, "qere_atom": "פְּרָֽת׃", "pos-within-verse": 13},
    {"wlc-index": 25, "qere_atom": "בָּנָיו֙", "pos-within-verse": 9},
    {"wlc-index": 30, "qere_atom": "בָּאִ֖ים", "pos-within-verse": 3},
    {"wlc-index": 16, "qere_atom": "כֵּ֥ן", "pos-within-verse": 19},
    {"wlc-index": 24, "qere_atom": "צְבָא֖וֹת", "pos-within-verse": 10},
    {"wlc-index": 31, "qere_atom": "לָהּ֙", "pos-within-verse": 13},
    {"wlc-index": 14, "qere_atom": "וַיִּוָּלְד֧וּ", "pos-within-verse": 1},
    {"wlc-index": 17, "qere_atom": "בִּתְחִלַּ֖ת", "pos-within-verse": 16},
    {"wlc-index": 18, "qere_atom": "וַיִּתְגָּעַ֤שׁ", "pos-within-verse": 1},
    {"wlc-index": 32, "qere_atom": "דָּנִיֵּ֣אל", "pos-within-verse": 7},
    {"wlc-index": 33, "qere_atom": "דָּנִיֵּ֣אל", "pos-within-verse": 2},
    {"wlc-index": 34, "qere_atom": "מִדָּֽנִיֵּ֑אל", "pos-within-verse": 4},
    {"wlc-index": 36, "qere_atom": "וּזְקֵנִ֖ים", "pos-within-verse": 11},
    {"wlc-index": 38, "qere_atom": "הִזְדְּמִנְתּוּן֙", "pos-within-verse": 12},
    {"wlc-index": 8, "qere_atom": "בַּטְּחֹרִ֔ים", "pos-within-verse": 9},
    {"wlc-index": 9, "qere_atom": "בַּטְּחֹרִ֑ים", "pos-within-verse": 6},
    {"wlc-index": 19, "qere_atom": "הָאֵ֔לֶּה", "pos-within-verse": 10},
    {"wlc-index": 22, "qere_atom": "שְׁכֵנָ֑יִךְ", "pos-within-verse": 10},
    {"wlc-index": 23, "qere_atom": "דִּבְיוֹנִ֖ים", "pos-within-verse": 16},
    {"wlc-index": 35, "qere_atom": "תִּצֹּֽרְנָה׃", "pos-within-verse": 7},
    {"wlc-index": 13, "qere_atom": "מִמַּעַרְכ֣וֹת", "pos-within-verse": 12},
]
RECORDS = [
    RECORD_01,
    RECORD_02,
    RECORD_03,
    RECORD_04,
    RECORD_05,
    RECORD_06,
    RECORD_07,
    RECORD_08,
    RECORD_09,
    RECORD_10,
    RECORD_11,
    RECORD_12,
    RECORD_13,
    RECORD_14,
    RECORD_15,
    RECORD_16,
    RECORD_17,
    RECORD_18,
    RECORD_19,
    RECORD_20,
    RECORD_21,
    RECORD_22,
    RECORD_23,
    RECORD_24,
    RECORD_25,
    RECORD_26,
    RECORD_27,
    RECORD_28,
    RECORD_29,
    RECORD_30,
    RECORD_31,
    RECORD_32,
    RECORD_33,
    RECORD_34,
    RECORD_35,
    RECORD_36,
    RECORD_37,
    RECORD_38,
    RECORD_39,
]
