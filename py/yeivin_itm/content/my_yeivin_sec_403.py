import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

SEC = [
    sub.para(
        [
            "Consider a situation in which a pair of words (α, β) has the following properties:"
        ]
    ),
    sub.unordered_list(
        [
            [
                "Word α has a conjunctive accent and"
                " ends with an open syllable pointed with ",
                sub.qamets(),
                " or ",
                sub.segol(),
                ".",
            ],
            [
                "Word β is initially stressed. ",
                hlp.paren(
                    [
                        "As usual, we use the masoretic notion of a syllable,"
                        " so initial stress means stress on the first full vowel,"
                        " whether or not there is an initial $shewa.",
                    ]
                ),
            ],
        ]
    ),
    sub.para(
        [
            "In such a situation, the first letter of β may take a",
            " $dagesh. This is referred to as a conjunctive",
            " $dagesh. In the Masorah, this phenomenon is called $dexiq (דחיק) or ",
            sub.ate_meraxiq(),
            " (אתי מרחיק)."
            " In some sources, these names are used for two different categories"
            " of this phenomenon,"
            " but Dotan has recently suggested"
            " that the phenomenon itself was called ",
            sub.ate_meraxiq(),
            ", while the $dagesh used to mark it was called $dexiq."
            " Rules governing this phenomenon were formulated by Baer,"
            " but the practice of the best Biblical manuscripts"
            " has not yet been studied in detail.",
        ]
    ),
    sub.para(
        [
            "The next two sections will cover the following classes of $dexiq:",
        ]
    ),
    sub.ordered_list_with_lcromnum(
        [sub.cmn_403_lcromnum_i(), sub.cmn_403_lcromnum_ii()]
    ),
]
