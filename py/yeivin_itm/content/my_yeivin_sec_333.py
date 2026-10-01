import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_FTNT = sub.footnote(
    [
        "I include only one of the two ",
        sub.pazer(),
        " examples provided by $itm. The example I exclude is ",
        hlp.lhbo("@1C 12:41", "וּֽבַבָּקָ֡ר"),
        ". I exclude it because it doesn’t seem fit the pattern"
        " being discussed, since it starts with $gaya",
        " on ",
        hlp.hbo("וּ"),
        " ",
        hlp.paren(sub.shureq()),
        " not ",
        hlp.hbo("וְ"),
        " ",
        hlp.paren([sub.waw(), " with $simshewa"]),
        ".",
    ]
)
_DLOC_GEN_AND_1C = hlp.make_dloc("@Gen 10:14", "@1C 1:12")
_TABLE_1 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@2K 24:14", "וְֽאֶת־כׇּל־הַשָּׂרִ֞ים")],
        [hlp.lhbo(_DLOC_GEN_AND_1C, "וְֽאֶת־פַּתְרֻסִ֞ים")],
        [hlp.lhbo("@Jos 10:24", "כְּֽהוֹצִיאָ֞ם")],
        [hlp.lhbo("@Ez 43:11", "וְֽכׇל־צוּרֹתָ֡ו")],
        [hlp.lhbo("@Jer 42:5", "כְּֽכׇל־הַ֠דָּבָ֠ר")],
        [hlp.lhbo("@Gen 24:30", "וְֽאֶת־הַצְּמִדִים֮")],
        [hlp.lhbo("@Ez 35:12", "וְֽיָדַעְתָּ֮")],
    ]
)
_TABLE_2 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Ez 41:9", "אֲֽשֶׁר־לַצֵּלָ֛ע")],
        [hlp.lhbo("@Jud 4:9", "בְֽיַד־אִשָּׁ֔ה")],
        [hlp.lhbo(*sub.FK_6_22)],
    ]
)
_TABLE_3 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Song 1:5", "וְֽנָאוָ֔ה")],
        [hlp.lhbo("@Jer 51:61", "וְֽרָאִ֔יתָ וְֽקָרָ֔אתָ")],
        [hlp.lhbo("@Is 13:2", "שְֽׂאוּ־נֵ֔ס")],
    ]
)
_TABLE_4 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Song 1:8", "צְֽאִי־לָ֞ךְ")],
        [hlp.lhbo("@Jer 34:3", "וְֽ֠עֵינֶ֠יךָ")],
    ]
)
_GPTZ = sub.gershayim(), hlp.ftntjoin(sub.pazer(), _FTNT), sub.telisha(), sub.zarqa()
_CONT_PARA_2 = [
    ["This $gaya is marked"],
    [" on the second, third, or fourth syllable before the stress."],
    [" It is usually used with “high” accents ", hlp.rtn_p(195), ","],
    [" as we see in the examples below, with"],
    [" ", sub.four_comma_and(*_GPTZ), "."],
]

SEC = [
    sub.para(
        [
            "$Gaya marked with either ",
            sub.simple_or_xatef(),
            " at the start of a word indicates (as $gaya",
            " always does)"
            " that the syllable must be slowed or lengthened."
            " Consequently that $shewa"
            " becomes a vowel",
            sub.emdash(),
            "probably equivalent to an ordinary short vowel. This $gaya",
            " is rare in the twenty one books (only some 200 cases"
            " occur) but it is common in the three books."
            " This is a $mgaya, but it is often used before a guttural, which"
            " suggests that there may be phonetic reasons for its use."
            " The system of marking it is similar to that for $gaya_cs,"
            " but there are no firm rules for its use.",
        ]
    ),
    sub.para(_CONT_PARA_2),
    _TABLE_1,
    sub.para(["It also occasionally occurs with other accents as"]),
    _TABLE_2,
    sub.para_paren(
        [
            "In the last example above, ",
            hlp.hbo(sub.FK_6_22[1]),
            sub.thspc(),
            " we see that $gaya",
            " with $shewa"
            " is given preference over $gaya_cs in a word with regular structure.",
        ]
    ),
    sub.para(
        [
            "$Gaya is also used on $shewa"
            " before the vowel of the"
            " syllable right before the stress syllable."
            " This occurs mostly on words with ",
            sub.zaqef(),
            ". E.g.:",
        ]
    ),
    _TABLE_3,
    sub.para(["This does occasionally occur with other accents as"]),
    _TABLE_4,
]
