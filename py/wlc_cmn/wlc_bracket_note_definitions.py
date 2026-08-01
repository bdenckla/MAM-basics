from __future__ import annotations

"""WLC bracket-note definitions keyed by bracket code.

Provenance:
- manual422: user-supplied manual transcription from WLC_Manual422.pdf.
- supplmt_wts: legacy right-hand bracket section in wlc422/supplmt.wts.
- amos_xml: <notes> block in Tanach.../Books/Amos.xml.

Rule: record all source definitions; dedupe only exact text matches.
"""

SOURCE_MANUAL422 = "manual422"
SOURCE_SUPPLMT_WTS = "supplmt_wts"
SOURCE_AMOS_XML = "amos_xml"

# Exact duplicate wording across sources after newline-wrap normalization.
_SUPPLMT_AMOS_DEF_1 = (
    "BHS has been faithful to the Leningrad Codex where there might be a question of the "
    "validity of the form and we keep the same form as BHS."
)
_SUPPLMT_AMOS_DEF_A = (
    "Adaptations to a Qere which L and BHS, by their design, do not indicate."
)
_SUPPLMT_AMOS_DEF_Q = (
    "We have abandoned or added a ketib/qere relative to BHS. In doing this we agree with "
    "L against BHS."
)
_SUPPLMT_AMOS_DEF_Y = (
    "Yathir readings in L which we have designated as Qeres when both Dothan and BHS list "
    "a Qere."
)
_MANUAL_SUPPLMT_DEF_5 = "Large letter(s)"
_MANUAL_SUPPLMT_DEF_6 = "Small letter(s)"
_MANUAL_SUPPLMT_DEF_7 = "Suspended letter(s)"

BRACKET_NOTE_DEFINITIONS: dict[str, dict[str, str]] = {
    "]1": {
        SOURCE_MANUAL422: (
            "BHS has been faithful to ל (the Leningrad Codex) where there might be a "
            "question of the validity of the form and we keep the same form as BHS. (This is "
            "similar to the note \u201c]U\u201d, but the latter refers to cases where BHQ has "
            "been published and we keep the same form as both BHS and BHQ.)"
        ),
        SOURCE_SUPPLMT_WTS: _SUPPLMT_AMOS_DEF_1,
        SOURCE_AMOS_XML: _SUPPLMT_AMOS_DEF_1,  # Exact-match wording in supplmt_wts and amos_xml.
    },
    "]2": {
        SOURCE_MANUAL422: (
            "WLC versions 4.4 and earlier inserted a Sof Pasuq at the end of the text of this "
            "verse because it would be expected, but those Sof Pasuqs were removed for version "
            "4.6 through 4.14 because those Sof Pasuqs were not actually present in ל. "
            "(The \u201c]2\u201d bracket notes were kept through WLC 4.14 for historical "
            "purposes, but have all been replaced in WLC 4.16 and later by \u201c]1\u201d (or, "
            "if appropriate, by \u201c]U\u201d).) (Only used in WLC 4.14 and earlier)"
        ),
        SOURCE_SUPPLMT_WTS: "We have added a sop pasuq where L and BHS omit it.",
    },
    "]3": {
        SOURCE_MANUAL422: (
            "We read or understand ל differently from BHS. Often this note indicates a "
            "typographical error in BHS. (\u201c]3\u201d was completely replaced by the more "
            "specific bracket notes \u201c]c\u201d, \u201c]k\u201d, \u201c]p\u201d, and \u201c]v\u201d "
            "in WLC 4.16 and later.) (Only used in WLC 4.14 and earlier)"
        ),
        SOURCE_SUPPLMT_WTS: (
            "We read or understand L differently than BHS (1983 Edition). Often this notation "
            "indicates a typographical error in BHS."
        ),
    },
    "]4": {
        SOURCE_MANUAL422: (
            "Puncta Extraordinaria \u2014 a <52> is used to represent such marks in the text "
            "when they are above the line and <53> when below the line."
        ),
        SOURCE_SUPPLMT_WTS: (
            "Puncta Extraordaria -- a 52 is used to mark such marks in the text when they are "
            "above the line and 53 when they are below the line."
        ),
        SOURCE_AMOS_XML: (
            "Puncta extraordinaria -- a \\u05c4 is used to mark such marks in the text when "
            "they are above the line and a \\u05c5 when they are below the line."
        ),
    },
    "]5": {
        SOURCE_MANUAL422: _MANUAL_SUPPLMT_DEF_5,
        SOURCE_SUPPLMT_WTS: _MANUAL_SUPPLMT_DEF_5,  # Exact-match wording in manual422 and supplmt_wts.
        SOURCE_AMOS_XML: "Large letter(s). Shown as large letters without a superscript note number.",
    },
    "]6": {
        SOURCE_MANUAL422: _MANUAL_SUPPLMT_DEF_6,
        SOURCE_SUPPLMT_WTS: _MANUAL_SUPPLMT_DEF_6,  # Exact-match wording in manual422 and supplmt_wts.
        SOURCE_AMOS_XML: "Small letter(s). Shown as small letters without a superscript note number.",
    },
    "]7": {
        SOURCE_MANUAL422: _MANUAL_SUPPLMT_DEF_7,
        SOURCE_SUPPLMT_WTS: _MANUAL_SUPPLMT_DEF_7,  # Exact-match wording in manual422 and supplmt_wts.
        SOURCE_AMOS_XML: "Suspended letter(s). Shown as suspended letters without a superscript note number.",
    },
    "]8": {
        SOURCE_MANUAL422: "Inverted Nun (<N> in the text)",
        SOURCE_SUPPLMT_WTS: "Inverted Nun (N]8 in the text)",
        SOURCE_AMOS_XML: "Inverted nun in the text. Shown without a superscript note number.",
    },
    "]9": {
        SOURCE_MANUAL422: (
            "BHS has abandoned ל and we (used to) concur. All of these occurrences are "
            "Ketiv/Qere problems. This bracket note became obsolete as of WLC 4.16. We changed "
            "the text at all of those places to follow ל and thus disagree with BHS. "
            "(Only used in WLC 4.14 and earlier)"
        ),
        SOURCE_SUPPLMT_WTS: (
            "BHS has abandoned L and we concur. All of these occurrences are ketib/qere problems."
        ),
    },
    "]C": {
        SOURCE_MANUAL422: (
            "We read an accent in ל differently from BHQ. (This is similar to the note "
            "\u201c]c\u201d, but the latter refers to accent differences against BHS.)"
        ),
        SOURCE_AMOS_XML: "We read one or more accents in L differently from BHQ.",
    },
    "]F": {
        SOURCE_MANUAL422: (
            "Marks a word with an anomalous consonant that is word-medial but has a word-final form."
        ),
        SOURCE_AMOS_XML: "Marks a consonant with an anomalous final form that is word-medial.",
    },
    "]K": {
        SOURCE_MANUAL422: (
            "We read a consonant in ל differently from BHQ. (This is similar to the note "
            "\u201c]k\u201d, but the latter refers to consonant differences against BHS.) This is "
            "the only occurrence of \u201c]K\u201d in WLC 4.16 \u2013 4.22."
        ),
        SOURCE_AMOS_XML: "We read one or more consonants in L differently from BHQ.",
    },
    "]M": {
        SOURCE_MANUAL422: (
            "Marks a word with an anomalous consonant that is word-final but has a word-medial form."
        ),
        SOURCE_AMOS_XML: "Marks a word with a final consonant that is a medial (not a final) form.",
    },
    "]P": {
        SOURCE_MANUAL422: (
            "We read a punctuation character (Maqqef, Mappiq, Dagesh, space, or Sof Pasuq) in "
            "ל differently from BHQ. (This is similar to the note \u201c]p\u201d, but the "
            "latter refers to punctuation differences against BHS.)"
        ),
        SOURCE_AMOS_XML: "We read the punctuation in L differently from BHQ.",
    },
    "]Q": {
        SOURCE_MANUAL422: (
            "Marks a place where we agree with BHQ against BHS in reading ל. This note "
            "will be preceded or followed by one or more bracket notes to specify the type(s) "
            "of disagreement(s) with BHS."
        ),
        SOURCE_AMOS_XML: "Marks a place where we agree with BHQ against BHS in reading L.",
    },
    "]S": {
        SOURCE_MANUAL422: (
            "Marks a Tsinnorit accent <82> that is written after (to the left of) a final Lamed "
            "in BHQ but is written before (to the right of) the Lamed in ל and other printed "
            "Hebrew Bibles (other than BHQ and BHS). This note marks a typesetting problem in BHQ."
        ),
    },
    "]U": {
        SOURCE_MANUAL422: (
            "BHS and BHQ have both been faithful to ל (the Leningrad Codex) where there "
            "might be a question of the validity of the form and we keep the same form as both "
            "BHS and BHQ. This is similar to the note \u201c]1\u201d, but the latter refers to "
            "cases where we keep the same form as just BHS. (\u201c]U\u201d only applies when "
            "the relevant fascicle of BHQ has been published and BHQ has the same reading as BHS.)"
        ),
        SOURCE_AMOS_XML: "We agree with both BHS 1997 and BHQ on an unexpected reading.",
    },
    "]V": {
        SOURCE_MANUAL422: (
            "We read a vowel in ל differently from BHQ. (This is similar to the note "
            "\u201c]v\u201d, but the latter refers to vowel differences againt BHS 1997.)"
        ),
        SOURCE_AMOS_XML: "We read one or more vowels in L differently from BHQ.",
    },
    "]a": {
        SOURCE_MANUAL422: (
            "Adaptations to a Qere that ל and BHS, by their design, do not indicate. Usually "
            "this indicates the addition of a Maqqef to our Qere text that is not present in the "
            "margin of ל, or to the addition of a Dagesh or Mappiq to our Qere text that is "
            "not present in the Ketiv consonants in the main text of ל."
        ),
        SOURCE_SUPPLMT_WTS: _SUPPLMT_AMOS_DEF_A,
        SOURCE_AMOS_XML: _SUPPLMT_AMOS_DEF_A,  # Exact-match wording in supplmt_wts and amos_xml.
    },
    "]c": {
        SOURCE_MANUAL422: (
            "We read an accent in ל differently from BHS. (This is similar to the note "
            "\u201c]C\u201d, but the latter refers to accent differences against BHQ.)"
        ),
        SOURCE_AMOS_XML: "We read one or more accents in L differently than BHS. Often this notation indicates a typographical error in BHS.",
    },
    "]e": {
        SOURCE_MANUAL422: (
            "This marks a Qere reading that is abbreviated in the margin of ל. In this example "
            "we would expect the Qere reading in the margin of ל to be <HMWNW>, but in fact, "
            "it has only <NW>, presumably because that is all that is needed to differentiate the "
            "ending of the Qere <HMWNW> from the ending of the Ketiv <HMWNH>."
        ),
    },
    "]k": {
        SOURCE_MANUAL422: (
            "We read a consonant in ל differently from BHS. (This is similar to the note "
            "\u201c]K\u201d, but the latter refers to consonant differences against BHQ.)"
        ),
        SOURCE_AMOS_XML: "We read one or more consonants in L differently from BHS.",
    },
    "]m": {
        SOURCE_MANUAL422: (
            "Miscellaneous notes to the text and occasions where more than one bracket category "
            "applies. All of these notes were re-examined for WLC 4.16 and either removed or "
            "replaced with a more appropriate bracket note. (Only used in WLC 4.14 and earlier)"
        ),
        SOURCE_SUPPLMT_WTS: (
            "Miscellaneous notes to the text and occasions where more than one bracket category applies."
        ),
    },
    "]n": {
        SOURCE_MANUAL422: (
            "An anomalous form in the text of ל. This bracket note was new to WLC 4.14 "
            "(only two occurrences in that version), and was not yet widely used at first, occurring "
            "on only 23 words in WLC 4.16. However, this bracket note occurs on 111 words (167 "
            "morphemes) in WLC 4.20."
        ),
        SOURCE_AMOS_XML: "Marks an anomalous form.",
    },
    "]p": {
        SOURCE_MANUAL422: (
            "We read a punctuation character (Maqqef, Mappiq, Dagesh, space, or Sof Pasuq) in "
            "ל differently from BHS. (This is similar to the note \u201c]P\u201d, but the latter "
            "refers to a punctuation difference against BHQ.)"
        ),
        SOURCE_AMOS_XML: "We read punctuation in L differently from BHS.",
    },
    "]q": {
        SOURCE_MANUAL422: (
            "We have abandoned or added a Ketiv/Qere relative to BHS. In doing this we agree "
            "with ל against BHS."
        ),
        SOURCE_SUPPLMT_WTS: _SUPPLMT_AMOS_DEF_Q,
        SOURCE_AMOS_XML: _SUPPLMT_AMOS_DEF_Q,  # Exact-match wording in supplmt_wts and amos_xml.
    },
    "]s": {
        SOURCE_MANUAL422: (
            "Marks a Tsinnorit accent <82> that is written after (to the left of) a final Lamed in "
            "BHS but is written before (to the right of) the Lamed in ל and other printed Hebrew "
            "Bibles (other than BHS). This note marks a typesetting problem in BHS."
        ),
    },
    "]t": {
        SOURCE_MANUAL422: (
            "We read one or more consonants, vowels or punctuation (Maqqef, Dagesh, Mappiq, "
            "or Sof Pasuq) in ל differently from BHS. (This bracket note was only used in "
            "WLC 4.12.) (This note was only used in WLC 4.12 and was replaced in WLC 4.14 "
            "and later by the more specific bracket notes \u201c]c\u201d, \u201c]k\u201d, \u201c]p\u201d, "
            "and \u201c]v\u201d.)"
        ),
    },
    "]v": {
        SOURCE_MANUAL422: (
            "We read a vowel in ל differently from BHS. (This is similar to the note \u201c]V\u201d, "
            "but the latter refers to vowel differences against BHQ.)"
        ),
        SOURCE_AMOS_XML: "We read one or more vowels in L differently from BHS.",
    },
    "]w": {
        SOURCE_MANUAL422: (
            "This note marks a reading which is exceptional but that does not quite rise to the level "
            "of what we would call an \u201cerror\u201d in ל. Dageshes in guttural letters are unusual, "
            "but there are a few cases such as in this Resh that seem to follow an expected pattern. "
            "The preceding word in this case ends in a vowel sound, so this could be considered a "
            "\u201ceuphonic\u201d Dagesh, even though it occurs in the semi-guttural letter Resh."
        ),
    },
    "]y": {
        SOURCE_MANUAL422: (
            "Yathir readings in ל which we have designated as Qeres. In WLC 4.14 and earlier, "
            "a few Yathir readings in ל were not marked as such because they were not treated as "
            "Qeres in either BHS or in the Dotan ADI edition of 1973, but beginning with 4.16 we "
            "rely only on whether or not something is a Yathir reading in ל."
        ),
        SOURCE_SUPPLMT_WTS: _SUPPLMT_AMOS_DEF_Y,
        SOURCE_AMOS_XML: _SUPPLMT_AMOS_DEF_Y,  # Exact-match wording in supplmt_wts and amos_xml.
    },
}

# Legacy right-hand bracket definitions present in supplmt.wts.
SUPPLMT_WTS_CODES = frozenset(
    (
        "]1",
        "]2",
        "]3",
        "]4",
        "]5",
        "]6",
        "]7",
        "]8",
        "]9",
        "]a",
        "]m",
        "]q",
        "]y",
    )
)

# Manual 4.22 chart bracket definitions in the user transcription.
MANUAL422_CODES = frozenset(
    (
        "]1",
        "]2",
        "]3",
        "]4",
        "]5",
        "]6",
        "]7",
        "]8",
        "]9",
        "]C",
        "]F",
        "]K",
        "]M",
        "]P",
        "]Q",
        "]S",
        "]U",
        "]V",
        "]a",
        "]c",
        "]e",
        "]k",
        "]m",
        "]n",
        "]p",
        "]q",
        "]s",
        "]t",
        "]v",
        "]w",
        "]y",
    )
)

AMOS_XML_NOTE_ENTRIES: dict[str, dict[str, str]] = {
    "1": {"gccode": "1", "bracket_code": "]1", "note_text": _SUPPLMT_AMOS_DEF_1},
    "2": {
        "gccode": "4",
        "bracket_code": "]4",
        "note_text": (
            "Puncta extraordinaria -- a \\u05c4 is used to mark such marks in the text when "
            "they are above the line and a \\u05c5 when they are below the line."
        ),
    },
    "3": {
        "gccode": "5",
        "bracket_code": "]5",
        "note_text": "Large letter(s). Shown as large letters without a superscript note number.",
    },
    "4": {
        "gccode": "6",
        "bracket_code": "]6",
        "note_text": "Small letter(s). Shown as small letters without a superscript note number.",
    },
    "5": {
        "gccode": "7",
        "bracket_code": "]7",
        "note_text": "Suspended letter(s). Shown as suspended letters without a superscript note number.",
    },
    "6": {
        "gccode": "8",
        "bracket_code": "]8",
        "note_text": "Inverted nun in the text. Shown without a superscript note number.",
    },
    "7": {"gccode": "a", "bracket_code": "]a", "note_text": _SUPPLMT_AMOS_DEF_A},
    "8": {
        "gccode": "c",
        "bracket_code": "]c",
        "note_text": "We read one or more accents in L differently than BHS. Often this notation indicates a typographical error in BHS.",
    },
    "9": {
        "gccode": "k",
        "bracket_code": "]k",
        "note_text": "We read one or more consonants in L differently from BHS.",
    },
    "10": {
        "gccode": "n",
        "bracket_code": "]n",
        "note_text": "Marks an anomalous form.",
    },
    "11": {
        "gccode": "p",
        "bracket_code": "]p",
        "note_text": "We read punctuation in L differently from BHS.",
    },
    "12": {"gccode": "q", "bracket_code": "]q", "note_text": _SUPPLMT_AMOS_DEF_Q},
    "13": {
        "gccode": "v",
        "bracket_code": "]v",
        "note_text": "We read one or more vowels in L differently from BHS.",
    },
    "14": {"gccode": "y", "bracket_code": "]y", "note_text": _SUPPLMT_AMOS_DEF_Y},
    "15": {
        "gccode": "C",
        "bracket_code": "]C",
        "note_text": "We read one or more accents in L differently from BHQ.",
    },
    "16": {
        "gccode": "F",
        "bracket_code": "]F",
        "note_text": "Marks a consonant with an anomalous final form that is word-medial.",
    },
    "17": {
        "gccode": "K",
        "bracket_code": "]K",
        "note_text": "We read one or more consonants in L differently from BHQ.",
    },
    "18": {
        "gccode": "M",
        "bracket_code": "]M",
        "note_text": "Marks a word with a final consonant that is a medial (not a final) form.",
    },
    "19": {
        "gccode": "P",
        "bracket_code": "]P",
        "note_text": "We read the punctuation in L differently from BHQ.",
    },
    "20": {
        "gccode": "Q",
        "bracket_code": "]Q",
        "note_text": "Marks a place where we agree with BHQ against BHS in reading L.",
    },
    "21": {
        "gccode": "U",
        "bracket_code": "]U",
        "note_text": "We agree with both BHS 1997 and BHQ on an unexpected reading.",
    },
    "22": {
        "gccode": "V",
        "bracket_code": "]V",
        "note_text": "We read one or more vowels in L differently from BHQ.",
    },
}

AMOS_XML_GCCODE_TO_BRACKET_CODE = {
    entry["gccode"]: entry["bracket_code"] for entry in AMOS_XML_NOTE_ENTRIES.values()
}


def bracket_note_codes() -> tuple[str, ...]:
    """Returns all bracket-note codes available in the merged map."""
    return tuple(sorted(BRACKET_NOTE_DEFINITIONS.keys()))


def bracket_note_definition(code: str, source_key: str) -> str | None:
    """Returns a source-specific definition for a code, or None if absent."""
    return BRACKET_NOTE_DEFINITIONS.get(code, {}).get(source_key)
