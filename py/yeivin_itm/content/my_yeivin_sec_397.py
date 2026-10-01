import yeivin_itm.substitutions as sub

_MSS_C_S = sub.ms_cairo(), " and ", sub.ms_s_507()
SEC = [
    sub.para(
        [
            "In most manuscripts, the ",
            sub.rafe(),
            " sign, a horizontal stroke above the letter, is used on the ",
            sub.begad_kefat(),
            " letters where they do not have $dagesh. If two letters together both require ",
            sub.rafe(),
            ", the sign is generally only"
            " marked once, over the space between them."
            " ",
            sub.rafe(cap=True),
            " is also used to mark non-consonantal ",
            sub.he(),
            " and ",
            sub.alef(),
            ", as noted above. The ",
            sub.rafe(),
            " sign is not used consistently."
            " It is used more often where there is some possibility of confusion,"
            " as with ",
            sub.begad_kefat(),
            " letters at the start of a word"
            " after a word ending with a vowel."
            " But even there it is not marked consistently."
            " Some manuscripts, such as ",
            sub.ms_b_4445(),
            ", mark ",
            sub.rafe(),
            " very rarely. Others, such as ",
            *_MSS_C_S,
            ", mark it often.",
        ]
    ),
]
