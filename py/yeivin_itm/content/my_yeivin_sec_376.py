import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_GEN_25_18 = "וַיִּשְׁכְּנ֨וּ", "וַ_-יִּשְׁ-כְּנ֨וּ", "@Gen 25:18"
_EST_9_3 = "וְהָאֲחַשְׁדַּרְפְּנִ֣ים", "וְהָ-אֲחַשְׁ-דַּרְ-פְּנִ֣ים", "@Est 9:3"
_GEN_2_12 = "וּֽזְהַ֛ב", "וּֽ-זְהַ֛ב", "@Gen 2:12"
_GEN_25_18_NORM, _GEN_25_18_SYL_SEP_INL = hlp.norm_and_syl_inline(_GEN_25_18)
_EST_9_3_NORM, _EST_9_3_SYL_SEP_INL = hlp.norm_and_syl_inline(_EST_9_3)
_GEN_2_12_NORM, _GEN_2_12_SYL_SEP_INL = hlp.norm_and_syl_inline(_GEN_2_12)
_TABLE_1_DATA = [
    ["E.g., in", _GEN_25_18_NORM],
    [["the ", sub.silshewa()], hlp.hbo("וישְכנו"), " goes with what precedes, and "],
    [["the ", sub.vocshewa()], hlp.hbo("וישכְנו"), " goes with what follows."],
    ["So,", _GEN_25_18_SYL_SEP_INL, "is the syllable structure of this word."],
]
_TABLE_2_DATA = [
    ["And, in", _EST_9_3_NORM],
    [
        ["the silent ", sub.shewas()],
        hlp.hbo("והאחשְדרְפנים"),
        "go with what precedes, and ",
    ],
    [["the vocal ", sub.shewas()], hlp.hbo("וְהאֲחשדרפְנים"), "go with what follows."],
    ["So,", _EST_9_3_SYL_SEP_INL, "is the syllable structure of this word."],
]
_TABLE_1 = hlp.table_std(_TABLE_1_DATA, coldirs=["ltr", "rtl", "ltr"])
_TABLE_2 = hlp.table_std(_TABLE_2_DATA, coldirs=["ltr", "rtl", "ltr"])
SEC = [
    sub.para(
        [
            "The distinction of silent from $vocshewa",
            " was a great concern for the Masoretes for two reasons:",
        ]
    ),
    sub.ordered_list(
        [
            [
                "This was necessary for correct pronunciation, since $vocshewa",
                " was realized as an ultra-short vowel, but $silshewa as no vowel.",
            ],
            [
                "$Shewa",
                " acted as a guide to the syllable structure of the word."
                " Neither type of $shewa"
                " was considered to form a syllable. Rather, both types of $shewa"
                " were considered to be dependent on an adjacent “full vowel”;"
                " $silshewa on the previous, and $vocshewa on the next.",
            ],
        ]
    ),
    _TABLE_1,
    _TABLE_2,
    sub.para_paren(
        [
            "From ",
            hlp.hbo("אֲחַשְׁ"),
            " in the example above, we can see that ",
            sub.x_patax(),
            ", like ",
            sub.simvocshewa(),
            ", goes with the syllable of the next vowel.",
        ]
    ),
    sub.para(
        [
            "Phonetic $gaya",
            " ",
            hlp.rtn_p(346),
            " could change $silshewa to vocal, and"
            " so change the syllable structure of a word."
            " The word ",
            hlp.hbo("וּזְהַב"),
            " without $gaya",
            " has syllable structure ",
            hlp.syl_inline("וּזְ-הַב"),
            sub.thspc(),
            " but with $gaya, ",
            _GEN_2_12_NORM,
            sub.thspc(),
            " it becomes ",
            _GEN_2_12_SYL_SEP_INL,
            ". ",
            hlp.paren(["This word only appears in the Bible with $gaya."]),
            " In the same way at the end of a word, $silshewa",
            " (whether marked or only potential) marks the structure. In ",
            hlp.lhbo("@Gen 1:1", "בְּרֵאשִׁית בָּרָא"),
            ", if the potential $shewa on ",
            sub.tav(),
            " were vocal, the structure would be ",
            hlp.syl_inline("בְּרֵא-שִׁי-תְבָּ-רָא"),
            ".",
        ]
    ),
]
