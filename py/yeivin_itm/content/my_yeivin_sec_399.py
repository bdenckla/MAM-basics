import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

SEC = [
    sub.para(
        [
            "A word-initial ",
            sub.begad_kefat(),
            " letter is $dagesh-free ",
            hlp.paren(["and so may be marked with ", sub.rafe()]),
            " if it follows a word ending with an open syllable"
            " which has a conjunctive accent or $maqqef.",
            " This rule is given in various masoretic sources such as ",
            sub.diqduqe_baer(29),
            " and ",
            sub.horayat_d(78, 386),
            ". As a general rule, the vowel of the open syllable at the end of the first word"
            " of the pair is marked by a"
            " vowel letter ",
            hlp.paren(sub.mater_lectionis()),
            ", i.e. marked with ",
            sub.comma_list_of_heb_ahw_or_y(),
            ", so that the rule is referred to"
            " in treatises as סימן אוי״ה ובג״ד כפ״ת."
            " It should, however, be noted that:",
        ]
    ),
    sub.unordered_list(
        [
            [
                "The rule applies to some open syllables that lack a vowel letter, as ",
                hlp.hboloc("נָחִ֥יתָ בְחַסְדְּךָ֖", "@Ex 15:13"),
                sub.thspp(),
            ],
            [
                "The rule does not apply to syllables that may look open at first glance,"
                " but are in fact closed, as ",
                hlp.hboloc("וַיַּ֥רְא בָּלָ֖ק", "@Nu 22:2"),
                sub.thspp(),
                # XXX do some research into this extraodinary phenomenon
                # of a "truly silent" א. Occurs not only with ר.
                # E.g. וְא and טְא and יְא
            ],
        ]
    ),
]
