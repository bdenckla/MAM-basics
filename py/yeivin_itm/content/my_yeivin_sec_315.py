import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

# XXX should many "para_paren" instances be turned into a footnote?
# Or, if left inline, should they be formatted to show that they are my addition,
# when indeed they are my addition? (Sometimes they may be in the original, i.e.
# not my addition.)
_FTNT = sub.footnote(
    [
        "I assume “backwards” means “counterclockwise from the vertical.”"
        " I.e. to the right, assuming the mark is made starting at its top. ",
        hlp.paren("“To the right” being backwards in a right-to-left script."),
        [" See ", hlp.rtn(313), "."],
    ]
)
SEC = [
    sub.para(
        [
            "$Gaya has no musical motif of its own, but indicates"
            " that the reading of its syllable is to be"
            " slowed down, and not slurred over, as noted in ",
            sub.horayat_d(77, 385),
            ":",
        ]
    ),
    sub.blockquote_p(
        sub.dol(
            [
                "But $gaya, which has the form of a stroke inclined ",
                hlp.ftntjoin("backwards,", _FTNT),
                " and is found under some words,"
                " is neither a disjunctive nor a conjunctive accent, but"
                " indicates that the syllable must be lengthened a bit.",
            ]
        )
    ),
    sub.para(
        [
            "It is probable that this slowing down of the reading of the syllable"
            " is the main function of $gaya, not the raising or trilling of the tone."
            " It is possible however, that, as time went on, $gaya"
            " came to be viewed as a secondary accent, and the rules"
            " for its use were changed, so that it came to be read with a"
            " raising of the pitch, and a short motif of its own.",
        ]
    ),
]
