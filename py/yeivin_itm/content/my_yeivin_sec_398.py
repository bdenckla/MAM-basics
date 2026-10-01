import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

SEC = [
    sub.para(
        [
            "In the manuscripts, ",
            sub.rafe(),
            " is used on other letters besides ",
            sub.begad_kefat(),
            ", mainly in the following categories.",
        ]
    ),
    sub.para(
        [
            "1) ",
            sub.rafe(cap=True),
            " is used after ",
            sub.waw(),
            " with $shewa at the start of a word, especially with verb forms, as ",
            hlp.hboloc("וְיִֿשְׁמַ֖ע", "@Is 42:23"),
            " and ",  # MAM וְיִשְׁמַ֖ע
            hlp.hboloc("וְיִֿבֹ֣א", "@1S 4:3"),
            " ",  # MAM וְיָבֹ֣א
            hlp.paren(["both in ", sub.ms_aleppo()]),
            ". This probably emphasizes the fact that ",
            sub.waw(),
            " consecutive"
            " is not being used, but the same phenomenon occurs with nouns, as ",
            hlp.hboloc("וְיָֿדִ֖י", "@1S 24:14"),
            " and ",  # MAM וְיָדִ֖י
            hlp.hboloc("וְיִֿשְׁמָעֵ֣אל", "@Jer 40:8"),
            " ",  # MAM וְיִשְׁמָעֵ֣אל
            hlp.paren(["both in ", sub.ms_aleppo()]),
            ". In manuscripts that often mark ",
            sub.rafe(),
            ", it may be marked not only after ",
            hlp.hbo("וְ"),
            " but also after other consonants with $shewa"
            " at the start of a word. E.g. ",
            sub.rafe(),
            " is marked after ",
            hlp.hbo("מְ"),
            " and ",
            hlp.hbo("תְּ"),
            " in ",
            *hlp.hbo_loc_ms("מְנֻֿחָת֖וֹ", "@Is 11:10", sub.ms_cairo()),
            ", ",  # MAM מְנֻחָת֖וֹ
            *hlp.hbo_loc_ms("מְלֵֿ֥א", "@Jer 6:11", sub.ms_cairo()),
            ", and ",  # MAM מְלֵ֥א
            *hlp.hbo_loc_ms("תְּמִֿימָ֑ה", "@Lev 14:10", sub.ms_s_507()),
            ".",  # MAM תְּמִימָ֑ה
        ]
    ),
    sub.para(
        [
            "2) ",
            sub.rafe(cap=True),
            " is used on a letter, particularly ",
            sub.yod(),
            ", which is pointed with $shewa and has no $dagesh, as ",
            hlp.hboloc("וַיְֿבַקְשׁ֔וּ", "@Jud 6:29"),
            " and ",  # MAM וַיְבַקְשׁ֔וּ
            hlp.hboloc("שִׁלְֿח֣וּ", "@Ps 74:7"),
            " ",  # MAM שִׁלְח֣וּ
            hlp.paren(["both in ", sub.ms_aleppo()]),
            ".",
        ]
    ),
    sub.para(
        [
            "3) ",
            sub.rafe(cap=True),
            " is used on ",
            sub.nun(),
            " in the first and third person pronominal prefixes, since the ",
            sub.nun(),
            " of the first person sometimes has $dagesh, as ",
            hlp.hboloc("פְּ֭דֵנִֿי", "@Ps 119:134"),
            " and ",  # MAM פְּ֭דֵנִי
            hlp.hboloc("שַׂמְתַּ֣נִֿי", "@Job 7:20"),
            " ",  # MAM שַׂמְתַּ֣נִי
            hlp.paren(["both in ", sub.ms_aleppo()]),
            ". ",
            hlp.paren(["See ", sub.diqduqe_dotan_sec_num(17), "."]),
            " However, in manuscripts that often mark ",
            sub.rafe(),
            ", we find that ",
            sub.rafe(),
            " is marked on ",
            sub.nun(),
            " even where there seems no likelihood of confusion, as ",
            hlp.hbo_varacc("לָנֿוּ"),
            sub.thspc(),
            " ",
            hlp.hbo_varacc("אֲנִֿי"),
            sub.thspc(),
            " and ",
            *hlp.hbo_loc_ms("יִדְּעֹנִֿ֖י", "@Lev 20:27", sub.ms_s_507()),
            ".",  # MAM יִדְּעֹנִ֖י
        ]
    ),
    sub.para(
        [
            "4) ",
            sub.rafe(cap=True),
            " is used on other letters where $dagesh might be expected, as:",
        ]
    ),
    sub.ordered_list_with_lcromalpha(
        [
            [
                "Where $dexiq ",
                hlp.paren("conjunctive $dagesh"),
                " is absent.",
            ],
            ["Where $dagesh is not marked following an accent."],
        ]
    ),
    sub.para(
        [
            "Examples of (a): ",
            *hlp.hbo_loc_ms("שִׂ֣יחָה לִֽֿי׃", "@Ps 119:99", sub.ms_aleppo()),
            ", ",  # MAM שִׂ֣יחָה לִֽי׃
            *hlp.hbo_loc_ms("מֹ֣שְׁלָה לֿ֑וֹ", "@Is 40:10", sub.ms_a_and_n()),
            ", and ",  # MAM מֹ֣שְׁלָה ל֑וֹ
            *hlp.hbo_loc_ms("יוֹרֶ֥ה שָֿׁ֖ם", "@Is 37:33", sub.ms_cairo()),
            ".",  # MAM יוֹרֶ֥ה שָׁ֖ם
        ]
    ),
    sub.para(
        [
            "Examples of (b): ",
            *hlp.hbo_loc_ms("יִבֹּ֑לֿוּ", "@2S 22:46", sub.ms_aleppo()),
            ", ",  # MAM יִבֹּ֑לוּ
            *hlp.hbo_loc_ms("לָ֤מָֿה", "@Job 7:20", sub.ms_aleppo()),
            ", ",  # MAM לָ֤מָה
            *hlp.hbo_loc_ms("שָׁ֣סֿוּ", "@Ps 44:11", sub.ms_a_and_l6()),
            ", and ",  # MAM שָׁ֣סוּ
            *hlp.hbo_loc_ms("מָ֣טֿוּ", "@Ps 46:7", sub.ms_aleppo()),
            ".",  # MAM מָ֣טוּ
        ]
    ),
    sub.para(
        [
            "Manuscripts that often mark ",
            sub.rafe(),
            " may also mark it on the letters ",
            hlp.comma_list_of_bdis("ל", "מ", "or נ"),
            " in other situations, as ",
            *hlp.hbo_loc_ms("גְּמָלָֿ֖נוּ", "@Is 63:7", sub.ms_cairo()),
            ", ",  # MAM גְּמָלָ֖נוּ
            *hlp.hbo_loc_ms("חֻמְֿצָתֽוֹ׃", "@Ho 7:4", sub.ms_cairo()),
            ", and ",  # MAM חֻמְצָתֽוֹ׃
            *hlp.hbo_loc_ms("וְלִשְׁנִֿינָֿ֑ה", "@Dt 28:37", sub.ms_s_507()),
            ".",  # MAM וְלִשְׁנִינָ֑ה
        ]
    ),
]
