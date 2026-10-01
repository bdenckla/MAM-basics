import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_TABLE_1 = hlp.table_std_rtl(
    [
        [
            sub.ms_b_4445(),
            *hlp.lns("@Gen 42:35", "וַיִּֽירָֽאוּ׃", "וַ_-יִּֽי-רָֽ-אוּ׃"),
        ],
        [sub.ms_lenin(), *hlp.lns("@1S 26:20", "דָּֽמִי֙", "-דָּֽ-מִי֙-")],
    ]
)
_A_L = sub.ms_a_and_l()
_TABLE_2_DATA = [
    [_A_L, hlp.lhbo("@Jer 17:4", "כִּֽי־אֵ֛שׁ")],
    [sub.ms_aleppo(), hlp.lhbo("@Is 10:12", "עַל־פְּרִֽי־גֹ֙דֶל֙")],
    [sub.ms_aleppo(), hlp.lhbo("@Naḥ 2:4", "אַנְשֵֽׁי־חַ֙יִל֙")],
    [sub.ms_b_4445(), hlp.lhbo("@Gen 45:12", "כִּֽי־פִ֖י")],
    [sub.ms_b_4445(), hlp.lhbo("@Ex 4:6", "הָבֵֽא־נָ֤א")],  # MAM has gaʿya on ה
]
_TABLE_2 = hlp.table_std(_TABLE_2_DATA, coldirs=["ltr", "rtl"])
_TABLE_3 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Jer 15:2", "לַֽחֶ֙רֶב֙")],
        [hlp.lhbo("@Jer 26:2", "הַבָּֽאִים֙")],
    ]
)
_TABLE_4 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Ez 1:1", "בִּשְׁלֹֽשִׁ֣ים")],
        [hlp.lhbo("@Ez 1:3", "הָֽיֹ֣ה הָֽיָ֣ה")],
    ]
)
_FTNT_STRIPPED_RAFE = sub.footnote(
    [
        "In $itm, many ",
        sub.rafe(),
        " signs are used in these examples. The font I am using does not support ",
        sub.rafe(),
        " well, so I have not included these marks."
        " Luckily, these marks are irrelevant to the issue at hand."
        " All that is lost is some of the “feel” of the manuscript in question.",
    ]
)
SEC = [
    sub.para(
        [
            "As a general rule, $gaya",
            " is only marked on an open syllable if there is some sort of buffer ",
            hlp.paren_xt("a full vowel or a $xatef"),
            " between the open syllable and the stress syllable."
            " But occasionally in the manuscripts, $gaya",
            " is marked even without such a buffer. E.g.:",
        ]
    ),
    _TABLE_1,
    sub.para(
        "This occurs most commonly in cases where two words are joined by $maqqef. E.g.:"
    ),
    _TABLE_2,
    sub.para(
        [
            sub.ms_lenin_20(),
            " and some other manuscripts use $gaya",
            " in this position quite often in the same word as the accent,"
            " especially if the accent is $pashta. E.g.:",
        ]
    ),
    _TABLE_3,
    sub.para(
        [
            "Some manuscripts with expanded Tiberian pointing also use $gaya",
            " in these positions quite often. E.g., in Vatican manuscript ",
            hlp.ftntjoin("Urbino 2:", _FTNT_STRIPPED_RAFE),
        ]
    ),
    _TABLE_4,
    sub.para("$Gaya is not used in these situations in printed texts."),
]
