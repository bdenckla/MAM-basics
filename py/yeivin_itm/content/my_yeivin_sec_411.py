import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_FTNT_1 = sub.footnote(
    [
        "In the great majority of cases the conjunctive accent is ",
        sub.merka(),  # translit-ok
        " serving ",
        sub.silluq(),
        " in the phrase ",
        hlp.hbo("אֶל־מֹשֶׁ֥ה לֵּאמֹֽר׃"),
        sub.thspp(),
        " Compare with ",
        hlp.hboloc("אֶל־מֹשֶׁ֖ה לֵאמֹ֑ר", hlp.make_dloc("@Nu 17:27", "@Nu 32:25")),
        ".",
    ]
)
_FTNT_2 = sub.footnote(
    [
        "In $itm, Babylonian vowel signs are used for these examples."
        " Presumably this was easy to do, since all pointing in $itm was done by hand!"
        " In contrast, my pointing is done using a font supporting only Tiberian signs."
        " Luckily, the type of pointing is irrelevant to the issue at hand."
        " All we miss is the ability to impart some of the “feel”"
        " of the manuscript in question, ",
        sub.ms_p(),
        ".",
    ]
)
_FTNT_3 = sub.footnote(
    [
        "Here $itm gives the locale Jer 1:4 for ",
        hlp.hbo("אל֣י לאמ֔ר"),
        sub.thspc(),
        " but I find it only at Jer 1:11. At Jer 1:4 I find only ",
        hlp.hboloc("אל֥י לאמֽר׃", "@Jer 1:4"),
        sub.thspp(),  # MAM אֵלַ֥י לֵאמֹֽר׃
    ]
)
_DATA_FOR_TABLE = [
    ("אֵלַ֣י לֵּאמֹ֔ר", "@Jer 1:11"),  # MAM אֵלַ֣י לֵאמֹ֔ר
    ("שֵׁנִ֣ית לֵּאמֹ֔ר", "@Jer 1:13"),  # MAM שֵׁנִ֣ית לֵאמֹ֔ר
]
SEC = [
    sub.para(
        [
            "In the pair ",
            hlp.hbo("מֹשֶׁה לֵּאמֹר"),
            sub.thspc(),
            " $dagesh is used in the ",
            sub.lamed(),
            " if משה has a conjunctive ",
            hlp.ftntjoin("accent.", _FTNT_1),
            " In some manuscripts, such as ",
            sub.ms_p(),
            ", $dagesh is used in the ",
            sub.lamed(),
            " of לאמר even after a word ending with a closed syllable. ",
            hlp.ftntjoin2("E.g.:", _FTNT_2, _FTNT_3),
        ]
    ),
    hlp.table_std_alpha_beta_2col_std(_DATA_FOR_TABLE, arg_to_troh=None),
    sub.para(
        [
            "This $dagesh appears to be used to emphasize the division"
            " between the words of these pairs.",
        ]
    ),
]
