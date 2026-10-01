import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_FTNT_LIBERTIES = sub.footnote(
    [
        "I introduced the term “chanted word”, with its parenthetical gloss,"
        " where $itm says “word or word group”."
        " I also restructured $itm’s argument about where $gaya"
        " would be expected, giving each of its two examples its own paragraph.",
    ]
)
_ISE_JER_31_20 = "@Jer 31:20"  # 31:19 in MAM
_TABLE_1 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Ezra 9:12", "בְּֽנוֹתֵיכֶ֞ם")],
        [hlp.lhbo(_ISE_JER_31_20, "אֲֽרַחֲמֶ֖נּוּ")],
    ]
)
_MSS_A_L_C = sub.ms_a_and_l(), ", ", sub.ms_cairo()
SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para(
        [
            "In early manuscripts, such as ",
            *_MSS_A_L_C,
            ", two $gayas are only rarely marked on the same chanted word ",
            hlp.paren(["simple word or $maqqef compound"]),
            ". Where a chanted word could have more than one $gaya,",
            " only one of them is generally marked."
            " E.g., in the following two words, $gaya",
            " is marked on the initial $shewa"
            " but not on the open syllable that follows it:",
        ]
    ),
    _TABLE_1,
    sub.para(
        [
            "In ",
            hlp.lhbo("@Ex 15:26", "כׇּֽל־הַמַּחֲלָ֞ה"),
            sub.thspc(),
            " $gaya",
            " is marked on the initial closed syllable,"
            " despite the fact that, given the word’s regular structure,"
            " we would expect $gaya to be marked on the closed syllable starting with ",
            sub.he(),
            ". ",
        ]
    ),
    sub.para(
        [
            "Conversely, in ",
            sub.ms_aleppo(),
            " in ",
            hlp.lhbo("@2K 23:12", "וְאֶת־הַֽמִּזְבְּח֡וֹת"),
            sub.thspc(),
            " $gaya is marked on the closed syllable we would expect,"
            " given the word’s regular structure."
            " $Gaya is not marked on the following two other candidate locations:",
        ]
    ),
    sub.unordered_list(
        [
            ["On the initial closed syllable, on the ", sub.alef(), "."],
            ["On the initial $shewa."],
        ]
    ),
    sub.para_paren("$Gaya is marked on the initial $shewa by bN."),
]
