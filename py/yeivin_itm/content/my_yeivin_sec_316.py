import yeivin_itm.substitutions as sub

SEC = [
    sub.para(["The use of $gaya can be divided into two groups of categories:"]),
    sub.ordered_list(
        [
            [
                sub.pseudo_heading("Musical"),
                ": Categories determined by the needs of the Biblical chant."
                " The use of $gaya in these categories is dependent"
                " on the syllable structure of the word, and dependent on the accent on"
                " that word or the accent on its neighbors."
                " Most examples of $gaya belong in these musical categories.",
            ],
            [
                sub.pseudo_heading("Phonetic"),
                ": Categories dependent on the letters and"
                " vowel-points of the word or its neighbors."
                " Few examples of $gaya belong in these phonetic categories.",
            ],
        ]
    ),
    sub.para(
        [
            "It is not always possible to determine whether $gaya",
            " is used for a musical or phonetic reason."
            " In some cases the reason could be either musical or phonetic,"
            " but this is of no importance."
            " Whatever the reason for using $gaya, its function is always the same:"
            " to slow the reading of the syllable,"
            " whether this is required"
            " for musical reasons at the start of a particular motif, or"
            " for phonetic reasons, to ensure the clear pronunciation of all"
            " the sounds of a word.",
        ]
    ),
]
