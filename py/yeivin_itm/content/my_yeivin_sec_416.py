import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

# Transliteration scheme
# ʾ א b ב g ג d ד h ה w ו z ז x ח ṭ ט y י k כ l ל m מ n נ s ס ʿ ע p פ ṣ צ q ק r ר ś שׂ š שׁ t ת
# u for shuruq or qibbuṣ, o for xolem
# ɔ for qametṣ (ɔ̆ for xaṭef qametṣ)
# a for patax (ă for xaṭef patax)
# ɛ for segol (ɛ̆ for xaṭef segol)
# e for ṣere, i for xireq, ə for shewa
# (Note that the (cup-shaped) breve diacritic plays the role of the xaṭef shewa.)

_FTNT_LIBERTIES = sub.footnote(
    [
        "I restructured $itm’s argument that these uses of $dagesh indicate"
        " doubling, posing it as a question and answer, and I put its phonetic"
        " transcriptions into IPA. I also tightened its reasoning about ",
        hlp.hbo("מִשְׁכָּנ֥וֹת לֹּא־לֽוֹ"),
        ": where $itm says only that the first word ends with a consonant,"
        " I name the letter, ",
        sub.tav(),
        ", and say that it closes the syllable.",
    ]
)
_FTNT_MAHZEH = sub.footnote(
    [
        sub.para(["This example, מה־זה, is perhaps “too cute” because, confusingly:"]),
        sub.unordered_list(
            [
                "It uses זה, coincidentally, as the word to which מה is $maqqef-connected.",
                [
                    "It is using מה־זה as an example"
                    " of a phenomenon that can also start with זה, e.g. ",
                    hlp.hboloc("זֶה־לִּ֞י", "@Gen 31:41"),
                    sub.thspp(),
                ],
            ]
        ),
        sub.para(
            [
                "The situation is even worse in $itm than it is here,",
                " because, confusingly, $itm does not provide the pointed Hebrew",
                " for this example."
                " It merely provides the phonetic transcription /maz-zɛh/ for this example,"
                " leaving the reader to back-infer what pointed Hebrew is being implied.",
            ]
        ),
    ]
)
_QUMU_TSEU_HBO_STR = "ק֤וּמוּ צְּאוּ֙"
_PARA_1_FOR_FTNT_VOCSHEWA = sub.para(
    [
        "The $vocshewa in ",
        hlp.hbo(_QUMU_TSEU_HBO_STR),
        " is notated with /ŭ/:"
        " the Latin small letter “u” with breve (a cup-shaped above-mark)."
        " This represents a short /u/ sound."
        " One might wonder why /ŭ/ is used rather than the generic $shewa"
        " /ə/."
        " The answer is that,"
        " according to masoretic theory at least,"
        " before gutturals, the $shewa"
        " was"
        " pronounced as a short vowel of the same quality as the vowel sound"
        " after the guttural ",
        hlp.rtn_p(336),
        ". In the case of ",
        hlp.hbo(_QUMU_TSEU_HBO_STR),
        sub.thspc(),
        " this means, specifically, that the $shewa in ",
        hlp.hbo("צְּ"),
        ""
        " was pronounced as a short /u/"
        " since it comes before a guttural (א)"
        " and the vowel sound after that guttural is a /u/ sound."
        " In other words, the general rule is:",
    ]
)
_TABLE_1_FOR_FTNT_VOCSHEWA = [
    [sub.simvocshewa(), "guttural", "vowel sound V"],
    ["is pronounced", "", ""],
    ["vowel sound “short V”", "guttural", "vowel sound V"],
]
_PARA_2_FOR_FTNT_VOCSHEWA = sub.para(
    ["So we can apply the rule specifically as follows:"]
)
_TABLE_2_FOR_FTNT_VOCSHEWA = [
    [sub.simvocshewa(), sub.alef(), sub.shureq()],
    ["is pronounced", "", ""],
    ["/ŭ/", "/ʾ/", "/u/"],
]
_FTNT_VOCSHEWA = sub.footnote(
    [
        _PARA_1_FOR_FTNT_VOCSHEWA,
        hlp.table_std(_TABLE_1_FOR_FTNT_VOCSHEWA),
        _PARA_2_FOR_FTNT_VOCSHEWA,
        hlp.table_std(_TABLE_2_FOR_FTNT_VOCSHEWA),
    ]
)
_YETSAWEL_LAK_PHONETIC_1 = "/yəṣawwɛl-lɔk/"
_YETSAWEL_LAK_PHONETIC_2 = "/yăṣawwɛl-lɔk/"
_YETSAWEL_LAK_HBO_STR = "יְצַוֶּה־לָּ֑ךְ"
_FTNT_GENERIC_SHEWA = sub.footnote(
    [
        "Here $itm uses the generic $shewa /ə/ rather than the specific /ă/. I.e., here ",
        hlp.hbo(_YETSAWEL_LAK_HBO_STR),
        " is transcribed as ",
        _YETSAWEL_LAK_PHONETIC_1,
        " rather than ",
        _YETSAWEL_LAK_PHONETIC_2,
        ". I mention the alternative of /ă/"
        " because at least in theory, it is the sound of initial $shewa. See ",
        hlp.rtn(336),
        ".",
    ]
)
_FTNT_DASH = sub.footnote(
    [
        "Here $itm transcribes with a dash,"
        " i.e. as /qúmuṣ-ṣŭʾú/."
        " I removed this dash, since there is no $maqqef.",
        " But it is possible that this dash meant something other than $maqqef.",
    ]
)
_QUMU_TSEU_PHON_PLUS_FTNTS = ["/qúmuṣ ṣŭʾú/?", " ", _FTNT_VOCSHEWA, ", ", _FTNT_DASH]
_DATA_FOR_TABLE = [
    [hlp.hboloc("יָֽלְדָה־לּ֖וֹ", "@Gen 24:47"), "/yɔldɔl-ló/?"],
    [hlp.hboloc(_QUMU_TSEU_HBO_STR, "@Ex 12:31"), _QUMU_TSEU_PHON_PLUS_FTNTS],
]
SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para(
        [
            "What is the phonetic value of $dagesh in its special uses covered in ",
            hlp.rtn(403),
            " and beyond?"
            " Its phonetic value is uncertain."
            " Is it simply a diacritic used to separate words, slowing the reading down,"
            " or does it have some phonetic value,"
            " i.e. does it indicate some particular pronunciation?"
            " $Dagesh generally indicates some particular pronunciation,"
            " indicating either that a ",
            sub.begad_kefat(),
            " letter represents a stop,"
            " or that a consonant should be doubled."
            " So it is likely that $dagesh would have one of these two phonetic values"
            " in these special uses as well."
            " Since these special uses of $dagesh are not restricted to ",
            sub.begad_kefat(),
            " letters,"
            " the more fitting of the two possible phonetic values is doubling."
            " So, it is likely that these special uses"
            " represent $dagesh_xazaq.",
        ]
    ),
    sub.para(
        [
            "This is easy to accept in cases where the $dagesh is used after a short vowel, ",
            sub.patax(),
            " or ",
            sub.segol(),
            ", as with:",
        ]
    ),
    sub.unordered_list(
        [
            [
                "$Dagesh after ",
                hlp.hbo("מַה"),
                " or ",
                hlp.hbo("זֶה"),
                sub.thspc(),
                " e.g. ",
                hlp.hboloc("מַה־זֶּ֛ה", "@Gen 27:20"),
                " ",
                hlp.rtn_p2(409, 410),
                hlp.ftntjoin(".", _FTNT_MAHZEH),
            ],
            [
                "$Dexiq after ",
                sub.segol(),
                ", e.g. ",
                hlp.hboloc(_YETSAWEL_LAK_HBO_STR, "@Ps 91:11"),
                " or even ",
                hlp.hboloc("יֵעָ֥שֶׂה לּֽוֹ", "@Ex 21:31"),
                " ",
                hlp.rtn_p(404),
                ".",
            ],
        ]
    ),
    sub.para(
        [
            "There is no problem in understanding $dagesh here"
            " as indicating doubling: /maz-zɛh/, ",
            _YETSAWEL_LAK_PHONETIC_1,
            hlp.ftntjoin(".", _FTNT_GENERIC_SHEWA),
        ]
    ),
    sub.para(
        [
            "In some other cases, however, this view seems less acceptable. In ",
            hlp.hboloc("וַיֹּ֣אמֶר׀ לֹּ֗א", "@Jos 5:14"),
            sub.thspc(),
            " ben Naftali’s $dagesh in the ",
            sub.lamed(),
            " cannot mark the preceding syllable, ",
            hlp.hbo("מֶר"),
            sub.thspc(),
            " as closed, since it is already closed by ",
            sub.resh(),
            ", and the word has a disjunctive accent, ",
            sub.legarmeh(),
            " ",
            hlp.rtn_p(278),
            ". The situation is similar in ",
            hlp.hboloc("מִשְׁכָּנ֥וֹת לֹּא־לֽוֹ", "@Ḥab 1:6"),
            " for here again the $dagesh in the ",
            sub.lamed(),
            " cannot mark the preceding syllable, ",
            hlp.hbo("נוֹת"),
            sub.thspc(),
            " as closed, since it is already closed, in this case by ",
            sub.tav(),
            ". In the same way, it is hard to accept that $dexiq after a long vowel",
            " marks the preceding syllable as closed. E.g.:",
        ]
    ),
    hlp.table_std(_DATA_FOR_TABLE, coldirs=["rtl", "ltr"]),
    sub.para_paren(
        [
            "A closed syllable with a long vowel"
            " normally only occurs as a word-final stressed syllable."
        ]
    ),
    sub.para(
        [
            "How can we resolve these issues while still continuing to assume"
            " that the $dagesh indicates doubling in these cases?"
            " We can resolve them as follows."
            " Rather than closing one syllable and starting the next,"
            " as in ",
            hlp.hbo("קִטֵּל"),
            " /qiṭ·ṭel/,"
            " we can view"
            " both parts of the doubled consonant as starting its “home” syllable."
            " This yields /wayyómer lló/, /yɔldɔ-lló/, /qúmu ṣṣŭʾú/, etc."
            " In this situation, presumably,"
            " the long vowel of the preceding syllable need not be shortened.",
        ]
    ),
]
