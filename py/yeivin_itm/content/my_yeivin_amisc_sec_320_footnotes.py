import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub


def _maybe_my_xxx(the_xxx):
    return "Maybe my ", the_xxx, " differs significantly from that of $itm."


def _which_which(mark, prop_a, prop_b):
    return "Which ", mark, " marks are considered ", prop_a, ", and which ", prop_b, "."


_TEG = "the expected $gaya"
_STEG = "without ", _TEG
_D1_STEG = "disjunctive ", *_STEG
_DS_STEG = "disjunctives ", *_STEG
_WTEGOAD = "with ", _TEG, " of a disjunctive"
_CS_STEG = "conjunctives ", *_WTEGOAD
_WWWEAG = "where we would expect a $gaya"

# Numbers below from Excel are from the workbook named "alhatorah-musical-gaya.xlsx",
# mainly in the sheet named "counts-main-reshaped".

_CNT_FR_ALL = 3584  # from Excel row "FR-star" column "sum"
_CNT_FR_DSG = 133  # from Excel row "FR-star" column "dsg"
_CNT_FR_CWG = 222  # from Excel row "FR-star" column "cwg"
_CNT_FR_DSG_OGC = 31  # from Excel
_CNT_FR_DSG_METIGAH = 6  # from Excel
_CNT_FR_DSG_MERKA = "two"  # from Excel
# Each of the above 6 counts is a count of FR words ...
#    of all types
#    that are 'disj-sans-gtbs' (DSG)
#    that are 'conj-with-gtbs' (CWG)
#    that are 'disj-sans-gtbs' with gaya somewhere other than tbs (two before [the] stress) (DSG_OGC)
#    that are 'disj-sans-gtbs' with metigah "instead of" gaya (DSG_METIGAH)
#    that are 'disj-sans-gtbs' with merka "instead of" gaya (DSG_MERKA)  # translit-ok
_CNT_FR_SURP = _CNT_FR_DSG + _CNT_FR_CWG
#
# How to calculate _CNT_FR_DSG_OGC:
#     Step 1: Filter the Excel sheet named "words"
#     to show only rows whose "phonrec-musical-gaya" column
#     has the one of the following values:
#         FR1-disj-sans-gtbs
#         FR2-disj-sans-gtbs
#         FR3-disj-sans-gtbs
#     Step 2: Additionally filter those rows down to ones whose "ogc" column
#     is not blank (probably this means that it has value 1)
#     Step 3: Confirm that there are 31 rows of them.
#
# How to calculate _CNT_FR_DSG_METIGAH:
#     Step 1: See Step 1 above for _CNT_FR_DSG_OGC.
#     Step 2: Additionally filter those rows down to ones whose "acc" column
#     has the value "(qom)"
#     ("qom" meaning "qadma or metigah")
#     Step 3: Confirm that these are indeed metigah not qadma
#     and confirm that there are 6 rows of them.
#
#
# How to calculate _CNT_FR_DSG_MERKA:
#     Step 1: See Step 1 above for _CNT_FR_DSG_OGC.
#     Step 2: Additionally filter those rows down to ones whose "acc" column
#     has the value "(mer)"
#     Step 3: Confirm that these are indeed merka paired with azla legarmeh  # translit-ok
#     and confirm that there are 2 rows of them.
#
_FR_SURPRISE_RATE = 9.9  # from Excel row "FR-star" column "surp"
_CONJ_SURPRISE_RATE_IN_FR1 = 28.5  # from Excel row "FR1" column "csurp"
_CONJ_SURPRISE_RATE_IN_FR2 = 20.1  # from Excel row "FR2" column "csurp"
_CONJ_SURPRISE_RATE_IN_FR3 = 6.7  # from Excel row "FR3" column "csurp"
#
_CONT_FTNT_90_PERCENT = [
    "My research agrees almost exactly with this estimate of 90%. "
    f"I find {_CNT_FR_ALL:,} fully regular words, "
    f"of which {_CNT_FR_SURP} ({_FR_SURPRISE_RATE:.1f}%) are exceptions to the rule, "
    "breaking down as follows:",
    sub.unordered_list(
        [
            [f"{_CNT_FR_DSG} ", _DS_STEG, "."],
            [f"{_CNT_FR_CWG} ", _CS_STEG, "."],
        ]
    ),
]

FTNT_90_PERCENT = sub.footnote(_CONT_FTNT_90_PERCENT)
_CONT_HUFT_FEW_DOZEN_PARA_1 = [
    ["My research disagrees with this estimate of a few dozen."],
    [" I find ", f"{_CNT_FR_DSG} ", _DS_STEG, "."],
    [" This is far more than could be called a few dozen."],
    [" This discrepancy probably comes from one or more of the following sources:"],
]

_HUFT_FEW_DOZEN_PARA_1 = sub.para(_CONT_HUFT_FEW_DOZEN_PARA_1)
_CONT_PAREN = [
    ["Except for ", sub.xireq(), ", my interpretation of ambiguous marks comes from"],
    [" ", sub.alhatorah(), " and ", sub.mam(), "."],
    [" For ", sub.xireq(), ", for the moment I use the approximation that it is"],
    [" ", sub.gadol(), " only in full spellings, i.e."],
    [" ", sub.gadol(), " only if followed by a non-consonantal ", sub.yod(), ","],
    [" and ", sub.qatan(), " otherwise."],
]
_CONT_LI_HUFT_1 = sub.dol(
    [
        [_maybe_my_xxx("base text")],
        [" In particular, maybe its use of $gaya differs significantly."],
        [" ", hlp.paren(["My base text is ", sub.mam(), "."])],
    ]
)
_CONT_LI_HUFT_2 = [
    _maybe_my_xxx("interpretation of ambiguous marks"),
    " In particular, maybe one or more of the following differs significantly:",
    sub.unordered_list(
        [
            _which_which("$shewa", "vocal", "silent"),
            _which_which(
                [sub.begad_kefat(), " ", sub.dagesh()], sub.xazaq(), sub.qal()
            ),
            _which_which(sub.qamets(), sub.gadol(), sub.xatuf_paren_qatan()),
            _which_which(sub.xireq(), sub.gadol(), sub.qatan()),
        ]
    ),
    hlp.paren(_CONT_PAREN),
]
_CONT_LI_HUFT_3 = [
    _maybe_my_xxx("placement of stress"),
    [" A non-impositive accent without a stress helper"],
    [" can be considered a kind of ambiguous mark,"],
    [" somewhat like the ambiguous marks discussed above."],
    [" For example, without a stress helper,"],
    [" the placement of stress is ambiguous in a word with "],
    [" the prepositive ", sub.telisha_gedolah()],
    [" or the postpositive ", sub.pashta(), "."],
    [" The placement of stress can also be ambiguous"],
    [" for certain paired poetic accents."],
    [" ", hlp.paren(["My placement of stress comes from ", sub.mam(), "."])],
]
_CONT_LI_HUFT_4 = [_maybe_my_xxx(["definition of “a ", _D1_STEG, "”"])]
_HUFT_FEW_DOZEN_UL = sub.unordered_list(
    [
        _CONT_LI_HUFT_1,
        _CONT_LI_HUFT_2,
        _CONT_LI_HUFT_3,
        _CONT_LI_HUFT_4,
    ]
)
_CONT_HUFT_FEW_DOZEN_PARA_2 = [
    ["I’ll expand on that final possible source of discrepancy between me and"],
    [" $itm."],
    [" The definition of “a ", _D1_STEG, "”"],
    [" may, at first glance, seem clear, but there are some gray areas."],
    [" Should a word like ", hlp.hboloc(sub.FK_6_22[1], sub.FK_6_22[0])],
    [" be counted as an ", sub.fr1(), " ", _D1_STEG, "?"],
    [" For sure, it does lack a $gaya in the expected location:"],
    [" it lacks a $gaya on ", hlp.hbo("שֶׁר"), sub.thspc()],
    [" the main part of the closed, short-vowelled syllable two before the stress."],
    [" But, as covered in ", hlp.rtn(333), ","],
    [" this likely reflects a preference (at least in this word) for"],
    [" $gaya on $shewa over ", _TEG, "."],
    [" A word pointed according to this preference"],
    [" is not as strong an exception to the rule as"],
    [" a word that has no $gaya marks anywhere,"],
    [" like the ", sub.fr3(), " words"],
    [" ", hlp.hboloc("אֲשֶׁר־יַעֲבֹ֖ר", "@Lev 27:32"), " and"],
    [" ", hlp.hboloc("אֲשֶׁר־תַּעֲשֶׂ֑ה", "@1K 20:22"), sub.thspp()],
    [" Should an exception of any “strength” be counted,"],
    [" or only the starkest exceptions?"],
    [" I find that", f" {_CNT_FR_DSG_OGC} of the {_CNT_FR_DSG} ", _DS_STEG],
    [" nonetheless have a $gaya elsewhere."],
    [" Some additional examples are"],
    [
        " ",
        hlp.hboloc("בְּאֶֽרֶץ־הַצְּבִ֖י", "@Dan 11:16"),
        " ",
        hlp.paren(sub.fr1()),
        ",",
    ],
    [" ", hlp.hboloc("וַיִּֽנְהֲג֔וּ", "@1S 30:2"), " ", hlp.paren(sub.fr2()), ","],
    [
        " and ",
        hlp.hboloc("וַיְנַֽאֲפוּ֙", "@Jer 29:23"),
        " ",
        hlp.paren(sub.fr3()),
        ".",
    ],
]

_HUFT_FEW_DOZEN_PARA_2 = sub.para(_CONT_HUFT_FEW_DOZEN_PARA_2)
_CONT_HUFT_FEW_DOZEN_PARA_3 = [
    [f"How should we count words having a secondary accent {_WWWEAG}?"],
    [" E.g., should a word like ", hlp.hboloc("וְלִ֨בְהֶמְתְּךָ֔", "@Lev 25:7")],
    [" be counted as an ", sub.fr2(), " ", _D1_STEG, ","],
    [" or does the ", sub.metigah(), " function as ", _TEG, "?"],
    [" I find that", f" {_CNT_FR_DSG_METIGAH} of the {_CNT_FR_DSG} ", _DS_STEG],
    [" nonetheless have a ", sub.metigah(), f" {_WWWEAG}."],
    [" Also, in", f" {_CNT_FR_DSG_MERKA} cases I find a"],
    [
        " ",
        sub.merka(),  # translit-ok
        " (paired with the poetic accent ",
        sub.azla_legarmeh(),
        ")",
    ],
    [f" {_WWWEAG}:"],
    [" ", hlp.hboloc("יִ֥תְיַצְּב֨וּ׀", "@Ps 2:2"), " ", hlp.paren(sub.fr1()), " and"],
    [" ", hlp.hboloc("עַ֥ל־נַהֲר֨וֹת׀", "@Ps 137:1"), " ", hlp.paren(sub.fr3()), "."],
    [" But I don’t know whether this ", sub.merka()],  # translit-ok
    [" implies some secondary stress like a $gaya."],
    [" Stress-wise, perhaps this ", sub.merka()],  # translit-ok
    [" is as meaningless as a ", sub.geresh_muqdam(), "."],
    [" E.g., though"],
    [" ", hlp.hboloc("יִ֝תְאַמְּר֗וּ", "@Ps 94:4"), " ", hlp.paren(sub.fr1())],
    [" has ", sub.geresh_muqdam(), f" {_WWWEAG},"],
    [" I have no reservations about counting it as an exception, since"],
    [" if it “wanted” a $gaya it could have one, as in "],
    [hlp.hboloc("וַֽ֝יִּלְמְד֗וּ", "@Ps 106:35"), " ", hlp.paren(sub.fr2()), "."],
]

_HUFT_FEW_DOZEN_PARA_3 = sub.para(_CONT_HUFT_FEW_DOZEN_PARA_3)
HUGE_FTNT_REC_FOR_FEW_DOZEN = {
    "huge-ftnt-rec-path-rel-web-publish-topdir": "yeivin_itm-huge-ftnt-320.html",
    "huge-ftnt-rec-title": "More than a few dozen disjunctives without the expected gaʿya",
    "huge-ftnt-rec-h1-contents": sub.dol(
        [f"More than a few dozen disjunctives without {_TEG}"]
    ),
    "huge-ftnt-rec-main": [
        _HUFT_FEW_DOZEN_PARA_1,
        _HUFT_FEW_DOZEN_UL,
        _HUFT_FEW_DOZEN_PARA_2,
        _HUFT_FEW_DOZEN_PARA_3,
    ],
}
FTNT_FOR_FEW_DOZEN = sub.footnote(
    hlp.ftnt_contents_for_pointer_to_huge(HUGE_FTNT_REC_FOR_FEW_DOZEN)
)
_CONT_FTNT_200 = [
    ["My research agrees, roughly, with this estimate of 200."],
    [" I find ", f"{_CNT_FR_CWG} ", _CS_STEG, "."],
    [" I find about", f" {_CONJ_SURPRISE_RATE_IN_FR1:.0f}% of ", sub.fr1()],
    [" conjunctives to have this $gaya,"],
    [" about", f" {_CONJ_SURPRISE_RATE_IN_FR2:.0f}% of ", sub.fr2()],
    [" conjunctives to have it, and only"],
    [" about", f" {_CONJ_SURPRISE_RATE_IN_FR3:.0f}% of ", sub.fr3()],
    [" conjunctives to have it."],
]

FTNT_200 = sub.footnote(_CONT_FTNT_200)
