import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_JOB = "לֹא יִשְׁנוּ", "@Job 29:22"
_PROV = "לֹא יִֽשְׁנוּ", "@Prov 4:16"
_CONT_PARA_1 = [
    "$Gaya ",
    hlp.paren_tt([hlp.hbo("גַעְיָה"), " or ", hlp.hbo("גִיעְיָה")]),
    " is the older name for this sign"
    " (a short vertical stroke under the word), and is used in the"
    " masoretic literature."
    " The absence of $gaya is called $xatef, as in the masorah magna of ",
    sub.ms_aleppo(),
    " at ",
    hlp.isolated_slocale("@Prov 4:16"),
    ":",
]

CONT_BLOCKQUOTE_1 = [
    sub.para(
        [["איוב ", hlp.hboloc(*_JOB), " חטף"], [" משלי ", hlp.hboloc(*_PROV), " געי"]]
    ),
    sub.para(
        [
            ["Job ", hlp.hboloc(*_JOB), " has no $gaya;"],
            [" Proverbs ", hlp.hboloc(*_PROV), " has $gaya."],
        ]
    ),
]

CONT_PARA_2 = [
    ["(Note that the word ישנו has a different meaning in the two cases.) "],
    [sub.metheg(cap=True), " ", hlp.paren_tt([hlp.hbo("מֶתֶג")])],
    [", the later name for the sign, and that"],
    [" common today, is first known from the work of "],
    [sub.yequtiel_hn(), " (first half of the thirteenth century)."],
    [" Eliahu ha-Levi (beginning of the sixteenth century) already suggests that "],
    [sub.metheg(), " is the correct term, "],
    ["and that $gaya was only a name for one of the classes of ", sub.metheg()],
    [" (that with $shewa)."],
]

SEC = [
    sub.para(_CONT_PARA_1),
    sub.blockquote(CONT_BLOCKQUOTE_1),
    sub.para(CONT_PARA_2),
]
