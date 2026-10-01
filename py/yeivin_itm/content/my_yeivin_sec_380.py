import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub
import mb_cmn.str_defs as sd

_DT_12_24 = "תֹּאכְלֶ֑נּוּ", "תֹּא*כְלֶ֑*נּוּ", "@Dt 12:24"
_NU_11_19 = "תֹּאכְל֖וּן", "*תֹּאכְ*ל֖וּן", "@Nu 11:19"
_QOH_5_10 = "אֹכְלֶ֑יהָ", "*אֹכְ*לֶ֑יהָ", "@Qoh 5:10"
_EX_4_18 = "אֵ֣לְכָה" + sd.NBSP + "נָּ֗א", "אֵ֣*לְכָה*" + sd.NBSP + "נָּ֗א", "@Ex 4:18"
# MAM has the vav-plene spelling (אוֹכְלֶ֑יהָ)
_PARA_CONTENTS_FOR_HE_LAMED_KAF = [
    "Rules for the root הלך – $Shewa on the ",
    sub.lamed(),
    " is silent except in"
    " the long form of the imperfect"
    " where the stress is retracted to the first syllable,"
    " and the next word has $dexiq ",
    hlp.paren("conjunctive $dagesh"),
    " ",
    hlp.rtn_p(405),
    ", as ",
    hlp.some_hi(_EX_4_18),
    " (",
    sub.diqduqe_dotan_sec_num(25),
    "). (",
    sub.ms_lenin(),
    " has ",
    sub.x_patax(),
    ".)",
]
_TABLE_1 = hlp.table_std(
    [
        [
            sub.dol(
                [
                    "If the ",
                    sub.lamed(),
                    " has ",
                    sub.segol(),
                    ", then a $shewa on the ",
                    sub.kaf(),
                    " is vocal.",
                ]
            ),
            hlp.some_hi(_DT_12_24),
        ],
        [sub.dol(["Otherwise, the $shewa is silent."]), hlp.some_hi(_NU_11_19)],
        [
            hlp.line_break(
                sub.dol(["Except, in the following word, the $shewa is considered"]),
                sub.dol(
                    [
                        " silent even though the ",
                        sub.lamed(),
                        " has a ",
                        sub.segol(),
                        ".",
                    ]
                ),
            ),
            hlp.some_hi(_QOH_5_10),
        ],
    ],
    arg_to_troh=["Rules for the root אכל", "Example"],
)
SEC = [
    sub.para_with_initial_uah(
        ["$Shewa on letters other than ", sub.resh()],
        [
            "The Masorah gives rules for the pronunciation of $shewa"
            " in some other verb forms:",
        ],
    ),
    _TABLE_1,
    sub.para(
        [
            # XXX turn the comment below into a footnote?
            # Does this reference to diqduqe & sefer_ha_xillufim apply only to the third row above,
            # or does it apply to the whole set of 3 rows (rules)?
            # I decided that it applies to the whole set, but see "Rules for the root ברך"
            # for a case where I went the other way, deciding that it applies only to the third
            # row (the exception row).
            "The rules above for the root אכל are stated in ",
            sub.diqduqe_dotan_sec_num(22),
            ", and are also given in the ",
            sub.sefer_ha_xillufim(),
            " as the opinion of bA. However, bN regards the $shewa on ",
            sub.kaf(),
            " as silent in all cases.",
        ]
    ),
    sub.para(_PARA_CONTENTS_FOR_HE_LAMED_KAF),
]
