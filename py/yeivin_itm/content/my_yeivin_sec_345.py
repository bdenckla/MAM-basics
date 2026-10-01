import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_CONTENTS_OF_TABLE = [
    [
        sub.dol(["$gaya on a short vowel (or even a long vowel)"]),
        sub.dol(["to show that a $shewa that follows it is vocal"]),
    ],
    [
        sub.dol(["$gaya before a guttural sound"]),
        # XXX turn the comment below into a footnote?
        # I added the qualification "sound" to "guttural",
        # i.e. I used "guttural sound" instead of just "guttural",
        # to cover the case of furtive patax.
        [
            "to slow down the reading of the vowel so that the guttural may be pronounced properly"
        ],
    ],
]
_TABLE_1 = hlp.table_std(_CONTENTS_OF_TABLE)
SEC = [
    sub.para(
        [
            "Some $gayas are not affected by"
            " syllable structure or accent."
            " They have a phonetic rather than a musical function."
            " They have several purposes, among them the following:",
        ]
    ),
    _TABLE_1,
    sub.para(
        [
            "It is not always clear what particular fault in pronunciation",
            " $pgaya was intended to remedy. However, the effect of",
            " $pgaya is the same as that of",
            " $mgaya: the slowing down of the reading.",
        ]
    ),
]
