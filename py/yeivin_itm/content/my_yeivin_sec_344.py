import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

SEC = [
    sub.para(
        [
            "This difference is reflected in the system of preference"
            " for marking $gaya. If a word could have $gaya both"
            " on a closed syllable and on an open syllable,"
            " that on the open syllable is marked in printed text, as ",
            hlp.lhbo("@Ex 14:19", "וַיַּֽעֲמֹ֖ד", hlp.hbo_attr_for_els()),
            " whereas that on the closed syllable"
            " would be marked in early manuscripts, i.e. ",
            hlp.hbo_els("וַֽיַּעֲמֹ֖ד"),
            sub.thspp(),
        ]
    ),
    sub.para(
        [
            "In a number of scholarly editions, such as those of Baer,"
            " Heidenheim, Qoren (Koren), and others,"
            " $gaya is marked as completely as possible, so that both $gayas"
            " are marked in a word like ",
            hlp.hbo_els("וַֽיַּֽעֲמֹ֖ד"),
            sub.thspp(),
            " Similar usage is found in a number of manuscripts, as noted by"
            " Eliahu ha-Levi in his ",
            sub.tuv_taam(),
            " chapter 7:",
        ]
    ),
    sub.blockquote_p(
        [
            "When there is $dagesh in the second letter of a word,"
            " and this letter is followed by ",
            hlp.comma_list_of_bdis("א", "ה", "ח", "or ע"),
            " pointed with ",
            sub.x_patax(),
            ", then that word has two ",
            sub.methegs(),
            ": one on the first letter ",
            hlp.paren(["the principal ", sub.metheg()]),
            " and one on the letter before the guttural",
            sub.emdash(),
            "but only if the word has a disjunctive accent, as ",
            hlp.hbo_els("וַֽיַּֽעֲמֹד"),
            " and ",
            hlp.hbo_els("וַֽיַּֽעֲבֹד"),
            sub.thspp(),
        ]
    ),
]
