from author_boj_util import author
from author_boj_util.uxlc_change import uxlc_change
from author_boj_util.golinets import golinets_citation
from author_boj_util.all_verses_but_this import reiteration_new_in_bhq

_GENCOM_PARA_1 = [
    "As $UXLC notes, an erasure under the כ is apparent.",
]
_GENCOM_PARA_2 = [
    "The שווא in question is present in μY.",
    " Relatedly, and importantly, μY has no רפה above its א.",
    " (The ink roughly between the כ and the א is the pair of above-dots",
    " that is μY’s equivalent of a masorah circle.)",
    " Thus, though μY presents a different word than the μL/μA word,",
    " it is still a valid word,",
    " i.e. the word makes sense according to the syllabic grammar of Biblical Hebrew.",
]
_GENCOM_PARA_3 = [
    "In contrast, transcription in $BHQ results in a word that does not make sense,",
    " if it were supplemented with the רפה that is clearly present in μL.",
    " This is one of several cases we’ve seen where רפה,",
    " though generally safe to ignore (and discard),",
    " is not always safe to ignore (and discard).",
    " See also $link_31_7.",
]
RECORD_1902 = {
    "qr-cv": "19:2",
    "qr-lc-proposed": "וּֽתְדַכְּאוּנַ֥נִי",
    "qr-what-is-weird": "כ has שווא",
    "qr-consensus": "וּֽתְדַכּאוּנַ֥נִי",
    "qr-generic-comment": [
        author.para(_GENCOM_PARA_1),
        author.para(_GENCOM_PARA_2),
        author.para(_GENCOM_PARA_3),
    ],
    "qr-highlight": 4,
    "qr-lc-loc": {"page": "402A", "column": 2, "line": 19},
    "qr-ac-loc": {"page": "274v", "column": 2, "line": 24, "word": 5},
    "qr-noted-by": "tBHQ-zUXLC",
    "qr-uxlc-change-url": uxlc_change("2023.10.19", "2023.06.10-19"),
}

_BHQ_COMMENT_PART_1 = [
    "$BHQ drops the note that $BHS has on this quirk.",
    " Usually $BHQ preserves notes that $BHS has on quirks.",
    " As usual, we don’t know whether $BHQ dropped this note on purpose or by accident.",
]
_BHQ_COMMENT_PART_2 = [
    "$BHQ silently lets the faint possible דגש “win” over the clear רפה in μL.",
    " In my opinion, $BHQ should have transcribed either both marks (דגש and רפה) or neither.",
    " Thus I consider $BHQ to have not accurately transcribed μL here.",
    " Also, $BHQ should have had a note.",
]

RECORD_1905 = {
    "qr-cv": "19:5",
    "qr-lc-q": "(?)",
    "qr-lc-proposed": "חֶרְפָּתִּֽֿי׃",
    "qr-what-is-weird": "דגש fights רפה",
    "qr-consensus": "חֶרְפָּתִֽי׃",
    "qr-generic-comment": [
        "A דגש on a letter with רפה doesn’t make sense.",
        " The color image of μL reveals this דגש to be unlikely.",
        [" It is judged to be just a speck, not a דגש, in ", golinets_citation("251")],
        " See $link_24_16.",
    ],
    "qr-highlight": 4,
    "qr-lc-loc": {"page": "402A", "column": 2, "line": -5},
    "qr-ac-loc": {"page": "274v", "column": 2, "line": 27, "word": 7},
    "qr-bhq-comment": [
        author.para(_BHQ_COMMENT_PART_1),
        author.para(_BHQ_COMMENT_PART_2),
    ],
    "qr-noted-by": "nBHL-nWLC",
}

RECORD_1916_QRAFY = {
    "qr-cv": "19:16",
    "qr-word-id": "QRAFY",
    "qr-lc-q": "(?)",
    "qr-lc-proposed": "קָּ֭רָאתִי",
    "qr-what-is-weird": "ק has דגש",
    "qr-consensus": "קָ֭רָאתִי",
    "qr-generic-comment": "The dot is suspiciously brown rather than black.",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "402B", "column": 1, "line": 8},
    "qr-ac-loc": {"page": "275r", "column": 1, "line": 11, "word": 4},
    "qr-bhq-comment": [
        "$BHQ notes that the דגש on the ק in μL disagrees with μA and μY.",
        " ",
        reiteration_new_in_bhq("19:16"),
    ],
    "qr-noted-by": "nBHQ-nBHL",
}

_GENCOM_PARA_1_1916_BMV0PY = [
    "μL omits the רביע of רביע מוגרש,",
    " which is expected,",
    " since μL’s habit is to omit the רביע in cases like this,",
    " where the רביע and the גרש מוקדם would be cramped together on the same letter.",
    " So, while μL doesn’t literally match the consensus we have presented,",
    " we can say that it implies that consensus,",
    " that consensus being merely the explicit notation of what μL implies.",
]
_GENCOM_PARA_2_1916_BMV0PY = [
    "In μL, there is some extra ink on the right side of the גרש מוקדם,",
    " which could, perhaps, be a misplaced רביע,",
    " but I find this unlikely.",
]
_GENCOM_PARA_3_1916_BMV0PY = [
    "Here μY matches μL,",
    " with the exception of two dots roughly between the ב and the מ.",
    " These dots are of unequal size, which is odd.",
    " They are likely a Masorah parva “callout”—note that",
    " instead of a masorah circle,",
    " μY uses a pair of above-dots",
    " as a “callout” for a Masorah parva note.",
    " See $link_22_21_3MV for another example of this two-dot callout notation.",
]
RECORD_1916_BMV0PY = {
    "qr-noted-by-mam": True,
    "qr-noted-by": "aDM",
    "qr-cv": "19:16",
    "qr-word-id": "BMV0PY",
    "qr-ac-proposed": "בְּ֝מוֹ־פִ֗י",
    "qr-consensus": "בְּמוֹ־פִ֝֗י",
    "qr-highlight-ac-proposed": [1, 5],
    "qr-highlight-consensus": 5,
    "qr-what-is-weird": "רביע מוגרש spans מקף",
    "qr-lc-loc": {"page": "402B", "column": 1, "line": 8},
    "qr-ac-loc": {"page": "275r", "column": 1, "line": 12, "word": 2},
    "qr-generic-comment": [
        author.para(_GENCOM_PARA_1_1916_BMV0PY),
        author.para(_GENCOM_PARA_2_1916_BMV0PY),
        author.para(_GENCOM_PARA_3_1916_BMV0PY),
    ],
}

RECORD_1928 = {
    "qr-cv": "19:28",
    "qr-lc-proposed": "תֹ֖אמְרוּ",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "תֹ֭אמְרוּ",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "402B", "column": 1, "line": 23},
    "qr-ac-loc": {"page": "275r", "column": 1, "line": 24, "word": 5},
    "qr-noted-by": "tBHQ-zdexiWLC",
}
