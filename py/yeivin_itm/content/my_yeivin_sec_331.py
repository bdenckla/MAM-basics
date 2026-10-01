import yeivin_itm.substitutions as sub

_MSS_L_S = sub.ms_lenin(), " and ", sub.ms_s_507()
_MSS_B_S1 = sub.ms_b_4445(), " and ", sub.ms_s1_1053()
_MSS_B_C = sub.ms_b_4445(), " and ", sub.ms_cairo()
SEC = [
    sub.para(
        [
            "$Gaya_osr is the most common category of $gaya in the"
            " Bible, and occurs in thousands of words."
            " In the early manuscripts,"
            " this $gaya",
            " is not marked on all the words where it could be,"
            " but only on some of them, and in some manuscripts it is marked"
            " more commonly than in others."
            " It seems probable that it was not"
            " considered important to mark it",
            sub.emdash(),
            "possibly because it made less"
            " difference to the pronunciation of the word than did $gaya_cs.",
        ]
    ),
    sub.para(
        [
            "In ",
            sub.ms_aleppo(),
            ", this $gaya",
            " is most commonly marked on words with $pashta or ",
            sub.zaqef(),
            ", less commonly on words with other disjunctives,"
            " and only rarely on words with conjunctives."
            " It is marked in"
            " about 30% of the possible cases.",
        ]
    ),
    sub.para(
        [
            "In ",
            *_MSS_L_S,
            " it is marked in about 40% of the possible cases. In ",
            *_MSS_B_S1,
            " it is marked in about 20% of the possible cases. In ",
            sub.ms_cairo(),
            " this $gaya",
            " is marked much more commonly",
            sub.emdash(),
            "in about 75% of the possible cases.",
        ]
    ),
    sub.para(
        [
            "The other early manuscripts mark this $gaya",
            " in varying proportions"
            " of the possible cases."
            " It is not always true that earlier manuscripts"
            " mark it less, as is shown by ",
            *_MSS_B_C,
            ", which are roughly"
            " contemporary."
            " It is, however, generally true that later manuscripts"
            " mark this $gaya",
            " more commonly, and the printed texts mark $gaya_os regularly"
            " on every syllable suitable for it.",
        ]
    ),
]
