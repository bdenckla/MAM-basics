import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp


def qatlu():
    return hlp.hbo("קָֽטְלוּ")


_FTNT_LIBERTIES = sub.footnote(
    [
        "I coined the name $gaya_osr for this $gaya;"
        " $itm names it only as “light” and “great”."
        " I also added the two parenthetical paragraphs below, which define"
        " a full vowel and note that the qualification is redundant under"
        " the masoretic notion of a syllable.",
    ]
)
_ON_A_SYL = sub.dol("$gaya on a syll. that is")
_BEFORE_A_LET = hlp.line_break("before a", "letter with")
_OFV = "open, full-vow."
_TYPE_2_EXS = hlp.line_break(hlp.hbo("שָֽׁאֲלָ֖ה"), hlp.hbo("יַֽעֲמֹ֖ד"))
_DATA_FOR_TABLE_1 = [
    ["i", _OFV, "a full vowel", hlp.hbo("אָֽנֹכִ֖י")],
    ["ii", _OFV, ["a ", sub.x_shewa()], _TYPE_2_EXS],
    ["iii", sub.sclv_abbr(), "(any)", qatlu()],
]
_TABLE_1 = hlp.table_std(
    _DATA_FOR_TABLE_1,
    arg_to_troh=["", _ON_A_SYL, _BEFORE_A_LET, "e.g."],
    coldirs=["ltr", "ltr", "ltr", "rtl"],
)
_TABLE_2 = hlp.table_std_rtl(
    [
        ["i", *hlp.lns("@Gen 22:14", "יֵֽאָמֵ֣ר", hlp.sy4ps("יֵֽ-אָ-מֵ֣ר"))],
        # MAM lacks ITM's gaʿya; see trope#377 (private tracker)
        [
            sub.saa(),
            *hlp.lns("@Gen 22:17", "כִּֽי־בָרֵ֣ךְ", hlp.sy4ps("כִּֽי־-בָ-רֵ֣ךְ")),
        ],
        [sub.saa(), *hlp.lns("@Gen 22:9", "אָֽמַר־ל֣וֹ", hlp.sy4ps("אָֽ-מַר־-ל֣וֹ"))],
        [
            sub.saa(),
            *hlp.lns(
                "@Gen 24:43", "הַשְׁקִֽינִי־נָ֥א", hlp.sy4("הַשְׁ-קִֽי-נִי־-נָ֥א")
            ),
        ],
        ["ii", *hlp.lns("@Gen 21:30", "בַּֽעֲבוּר֙", hlp.sy4ps("בַּֽ--עֲבוּר֙"))],
        # MAM lacks ITM's gaʿya; see trope#377 (private tracker)
        [sub.saa(), *hlp.lns("@Ez 37:14", "כִּֽי־אֲנִ֧י", hlp.sy4ps("כִּֽי־--אֲנִ֧י"))],
        ["iii", *hlp.lns("@Gen 22:12", "יָֽדְךָ֙", hlp.sy4ps("יָֽדְ--ךָ֙"))],
        [sub.saa(), *hlp.lns("@Gen 22:5", "נֵֽלְכָ֖ה", hlp.sy4ps("נֵֽלְ--כָ֖ה"))],
        # MAM lacks ITM's gaʿya; see trope#377 (private tracker)
        [
            sub.saa(),
            *hlp.lns("@Gen 47:4", "וַיֹּֽאמְר֣וּ", hlp.sy4("וַ-יֹּֽאמְ--ר֣וּ")),
        ],
        # MAM lacks ITM's gaʿya; see trope#377 (private tracker)
        [
            sub.saa(),
            *hlp.lns("@Gen 22:12", "כִּֽי־יְרֵ֤א", hlp.sy4ps("כִּֽי־יְ--רֵ֤א")),
        ],
    ]
)
SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para(["This section covers $gaya on syllables of the following types:"]),
    sub.unordered_list(
        [
            ["Open, with either a long or a short vowel."],
            [sub.sheclo(cap=True), ", with a long vowel."],
        ]
    ),
    sub.para(
        [
            ["This is the $gaya called “light” by ", sub.yequtiel_hn(), ","],
            [" and “great” by Dotan. We refer to it as $gaya_osr, where "],
            [sub.osr(), " stands for"],
        ]
    ),
    sub.unordered_list(
        [
            ["[on an] ", hlp.emphasis("Open Syllable")],
            ["[or on the] ", hlp.emphasis("Related"), " ", sub.osr_case()],
        ]
    ),
    sub.para(
        [
            "With some exceptions ",
            hlp.rtn_p2(352, 386),
            ", the Masoretes regarded $shewa"
            " after a long vowel within a word as silent"
            " (לא יצא בפה)."
            " So, in a word like ",
            qatlu(),
            sub.thspc(),
            " the syllable marked by $gaya",
            " is, in their view, closed, not open. However, because the rules for $gaya",
            " in this situation are similar to"
            " those for its use on an open syllable, the two situations are described together."
            " Note, however, that two different types of syllable are involved.",
        ]
    ),
    sub.para("We divide the main uses of $gaya_osr into the following three cases:"),
    _TABLE_1,
    sub.para_paren(
        [
            "A full vowel is a long or short vowel."
            " The short vowels do not include the ultra-short vowels."
            " I.e., they do not include $vocshewa vowels, whether notated as ",
            sub.simple_or_xatef(),
            ".",
        ]
    ),
    sub.para_paren(
        [
            "Above, we characterize some syllables as full-vowelled"
            " even though this is redundant,"
            " since we are using the masoretic notion of a syllable,"
            " in which all syllables are, by definition, full-vowelled,"
            " though they may start with a letter with some notation for $vocshewa.",
        ]
    ),
    sub.para(
        [
            "The use of $gaya",
            " in these cases is not affected by the accent on the word."
            " It occurs both with disjunctive and conjunctive accents."
            " E.g.: ",
        ]
    ),
    _TABLE_2,
    sub.para_paren(
        [
            "The table above includes one syllable, ",
            hlp.hbo("כִּֽי־יְ"),
            sub.thspc(),
            " that, awkwardly, spans a $maqqef boundary!",
        ]
    ),
]
