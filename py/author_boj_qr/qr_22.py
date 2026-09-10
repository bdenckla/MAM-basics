from author_boj_util import author
from author_boj_util.job_common import (
    RECORD_2221_CMN_AB,
    CAM1753_PAGE_URL_BASE,
    BHQ_COMMENT_XELSEWHERE_DUBIOUS,
)

RECORD_2210 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "22:10",
    "qr-consensus": "וִ֝יבַהֶלְךָ֗",
    "qr-lc-proposed": "וִֽ֝יבַהֶלְךָ",
    "qr-what-is-weird": "רביע of רביע מוגרש is absent",
    "qr-highlight": 6,
    "qr-generic-comment": [
        "Aside: in μL, the געיה (under $vav) has either",
        " survived much better than the other pointing of this word,"
        " been carefully re-inked (unlikely: the re-inking is rarely careful),"
        " or been added during re-inking (most likely).",
    ],
    "qr-ignore-g3yh-diff": True,
    "qr-lc-loc": {"page": "403B", "column": 1, "line": 10},
    "qr-ac-loc": {"page": "275v", "column": 2, "line": 25, "word": 2},
}

RECORD_2212 = {
    "qr-cv": "22:12",
    "qr-lc-proposed": "רֹ֭אשׁ",
    "qr-what-is-weird": "דחי not טרחא",
    "qr-consensus": "רֹ֖אשׁ",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "403B", "column": 1, "line": 12},
    "qr-ac-loc": {"page": "275v", "column": 2, "line": 27, "word": 6},
    "qr-bhq-comment": [
        "The transcription differs from the consensus in way opposite to most such reports here:",
        " here we see a דחי versus טרחא difference, with $BHQ having דחי,",
        " whereas most such reports involving these two accents",
        " involve a טרחא versus דחי difference, with $BHQ having טרחא.",
    ],
    "qr-noted-by": "tBHQ-zmiscWLC",
}
# jb22:12	רֹ֖אשׁ (has טרחא in WLC)
# It is now definitely a דחי in BHQ.
# It is ambiguous in 1997 BHS because of the conventions regarding mark
# placment under ר.
# It looks more like a דחי in 1984 BHS than in 1997 BHS.
# My guess is that the WLC editors read it as a דחי
# in whatever version of BHS they were looking at,
# but felt that טרחא was a better transcription of μL,
# and hence coded it as טרחא with a bracket-c note.
# So, the BHQ change (to unambiguous דחי) disagrees with WLC.
# So, the change in BHQ isn't really a change at all,
# if we take BHS to have what I think the WLC editors thought BHS
# had, namely, a דחי.

RECORD_2214 = {
    "qr-cv": "22:14",
    "qr-lc-proposed": "ל֖וֹ",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "ל֭וֹ",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "403B", "column": 1, "line": 14},
    "qr-ac-loc": {"page": "276r", "column": 1, "line": 1, "word": 6},
    "qr-noted-by": "tBHQ-zdexiWLC",
}

_COMMENT_2221_A = [
    "A dot under the מ of %עמו is fairly clear.",
    " It is (charitably) not transcribed by $BHL_A,",
    " presumably based on the consensus expectation that it is absent.",
]
_BHQ_COMMENT_2221_A = [
    "$BHQ fails to note that the אתנח it transcribes on %עמו",
    " disagrees with μA and μY.",
]
_COMMENT_2221_A_CALLOUT = [
    "Note that instead of a masorah circle, μY uses a pair of above-dots",
    " as a “callout” for a Masorah parva note;",
    " hence the pair of above-dots above ל in %ושלם.",
    " See $link_19_16_BMV0PY for another example of this two-dot callout notation.",
]
RECORD_2221_3MV = {
    **RECORD_2221_CMN_AB,
    "qr-word-id": "3MV",
    "qr-lc-q": "(?)",
    "qr-lc-proposed": "עִמּ֑וֹ",
    "qr-what-is-weird": "אתנח not מונח",
    "qr-consensus": "עִמּ֣וֹ",
    "qr-generic-comment": [
        author.para(_COMMENT_2221_A),
        author.para(_COMMENT_2221_A_CALLOUT),
    ],
    "qr-highlight": 2,
    "qr-bhq-comment": _BHQ_COMMENT_2221_A,
    "qr-noted-by": "tBHQ-nBHL-nWLC",
    "qr-cam1753-page-url": f"{CAM1753_PAGE_URL_BASE}/n83/mode/1up",
    "qr-ac-loc": {"page": "276r", "column": 1, "line": 10, "word": 3},
}

_COMMENT_2221_B = [
    "Perhaps some very faint remains of an אתנח under ל can be seen.",
    " The top dot of the שווא (under the ש) is very faint.",
]
_BHQ_COMMENT_2221_B = [
    "$BHQ (charitably) transcribes the top dot of the שווא",
    " using, as one often has to, faint evidence bolstered by consensus expectations.",
    " $BHQ notes (as does $BHS) that whereas the ל of %ושלם is unpointed in μL,",
    " that ל has קמץ and אתנח in μA and μY.",
]
RECORD_2221_VJL6 = {
    **RECORD_2221_CMN_AB,
    "qr-word-id": "VJL6",
    "qr-lc-proposed": "וּשְׁלם",
    "qr-what-is-weird": "ל lacks קמץ-אתנח",
    "qr-consensus": "וּשְׁלָ֑ם",
    "qr-generic-comment": _COMMENT_2221_B,
    "qr-highlight": 3,
    "qr-lc-loc": {"page": "403B", "column": 1, "line": -6},
    "qr-ac-loc": {"page": "276r", "column": 1, "line": 10, "word": 4},
    "qr-bhq-comment": _BHQ_COMMENT_2221_B,
    "qr-noted-by": "nBHQ-nWLC",
}

RECORD_2224 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "22:24",
    "qr-consensus": "וּכְצ֖וּר",
    "qr-lc-proposed": "וּבְצ֖וּר",
    "qr-what-is-weird": "ב not כ",
    "qr-highlight": 2,
    "qr-bhq-comment": [
        "$BHQ hints at the $khaf consensus via note on V (the Vulgate).",
        " Nonetheless, perhaps uncharitably, we consider $BHQ to not note this quirk.",
        " Aside: the שורוק dot and the טרחא had to be transcribed with great charity here,",
        " as is often the case in re-inked sections, since often only the letters are",
        " re-inked, not the pointing.",
    ],
    "qr-lc-loc": {"page": "403B", "column": 1, "line": 25},
    "qr-ac-loc": {"page": "276r", "column": 1, "line": 14, "word": 1},
    "qr-generic-comment": [
        "Although my focus is pointing rather than spelling,",
        " I am interested in a spelling difference like this,",
        " since it is not just a מלא/חסר difference.",
    ],
}

_BHQ_COMMENT = [
    "$BHQ places the mark a little left of center.",
    #
    " Though this placement is odd,",
    " this makes it clear that a טרחא was intended by $BHQ rather than a דחי.",
    " Thus $BHQ somewhat-accurately transcribes the quirk in μL,",
    " but should have noted the quirk.",
    #
    " Perhaps even better would have been to (charitably) transcribe this as a דחי,",
    " and note the quirk.",
    " But it is not the editorial policy of $BHQ to make such notes:",
    " although $BHQ is full of charitable transcriptions,",
    " as far as I know it never notes its charity.",
]
RECORD_2228 = {
    "qr-cv": "22:28",
    "qr-lc-proposed": "א֖וֹמֶר",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "אֹ֭מֶר",
    "qr-intermediate": "א֭וֹמֶר",
    "qr-generic-comment": [
        "The scribe of μL probably intended a דחי but placed it like a טרחא.",
        " The מלא/חסר spelling difference is not important to us here.",
    ],
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "403B", "column": 2, "line": 2},
    "qr-ac-loc": {"page": "276r", "column": 1, "line": 17, "word": 5},
    "qr-bhq-comment": [author.para(_BHQ_COMMENT)],
    "qr-noted-by": "tBHQ-nBHL",
}

_BHQ_COMMENT_2230_A = [
    "$BHQ has the געיה but makes no note as to whether the געיה diverges from consensus.",
    " There is no consensus in many cases of געיה, since most cases of געיה are optional.",
    " געיה with שווא (whether before or after שווא) occurs often,",
    " but further research would be needed to say whether this is a case in which",
    " געיה with שווא would be expected (or at least an expected option).",
]

RECORD_2230_YMLE = {
    "qr-cv": "22:30",
    "qr-word-id": "YMLE",
    "qr-lc-proposed": "יֽ͏ְמַלֵּ֥ט",
    "qr-lc-q": "(?)",
    "qr-what-is-weird": "$yod has געיה",
    "qr-consensus": "יְמַלֵּ֥ט",
    "qr-generic-comment": [
        "The possible געיה is before שווא.",
        " There is another mark below those marks.",
        " It is likely unintentional,",
        " and is treated accordingly, i.e. ignored,",
        " by all editions I know.",
    ],
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "403B", "column": 2, "line": 4},
    "qr-ac-loc": {"page": "276r", "column": 1, "line": 20, "word": 2},
    "qr-bhq-comment": _BHQ_COMMENT_2230_A,
    "qr-noted-by": "tBHQ-nWLC",
    "qr-uxlc-needs-fix": "add t-note (transcription uncertain)",
}

RECORD_2230_VNMLE = {
    "qr-cv": "22:30",
    "qr-word-id": "VNMLE",
    "qr-lc-proposed": "וְ֝נִּמְלַ֗ט",
    "qr-lc-q": "(?)",
    "qr-what-is-weird": "נ has דגש",
    "qr-consensus": "וְ֝נִמְלַ֗ט",
    "qr-generic-comment": "The dot in question is suspiciously smaller than nearby ones.",
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "403B", "column": 2, "line": 4},
    "qr-ac-loc": {"page": "276r", "column": 1, "line": 20, "word": 5},
    "qr-bhq-comment": BHQ_COMMENT_XELSEWHERE_DUBIOUS,
    "qr-noted-by": "nBHQ",
    "qr-uxlc-needs-fix": True,
}
