from taamey_d.doc.html_helpers import headfun, para, to_str, xtable
from taamey_d.doc.html_helpers import xtable_rows_of_cells

# TODO: How many words would change with this proposal?
# TODO: example words in tables
# TODO: What would this proposal look like for non-conforming fonts?
#       I.e. what is/are the failure mode(s)?

# Draft TypeDrawers post never sent:
#
# @"John Hudson" and @"Scott-Martin Kosofsky", as a result of our discussion
# here, I've begun to question my initial claim that Unicode needs a way to
# encode what I was calling “xolam male on alef.” I've already dropped my
# initial claim that a new code point is needed, but now I've begun to
# question whether any encoding (e.g., using ZWJ and/or ZWNJ) is needed.
#
# The reason for my doubt is that I'm no longer sure that the only valid
# interpretation of this dot on alef is as a xolam male dot. I still think it
# is a valid interpretation, but I'm no longer sure that it is the only valid
# interpretation. It could just as easily, perhaps more easily, be seen as a
# “late” placement of a xolam xaser dot.
#
# It is popular to interpret a xolam xaser dot as a vowel point. But it can
# also be interpreted as an “orphan” xolam male dot, i.e., a xolam male dot
# missing its vav “parent.” In this light, it is a little like the orphan
# xiriq or orphan sheva that usually appears on Jerusalem-related words. I.e.,
# in this light, any word with xolam xaser is a perpetual qere, i.e., a qere
# whose ketiv is implicit.

_HHFV_ABBREVS_HEADER_CELLS = "short", "long"
_HHFV_ABBREVS_ROWS = (
    ("$u_xxfv_short", "$u_xxfv"),
    ("$alef-con.", "$alef as a consonant"),
    ("voa", "$vav or $alef"),
    ("$xm-dot", "$xolam_male dot"),
    ("$xx-dot", "$xolam_xaser dot"),
)
_HHFV_ABBREVS_INSIDE = xtable_rows_of_cells(_HHFV_ABBREVS_ROWS)
#
_HHFV_TABLE_1_HEADER_CELLS = (
    "code point 1",
    "code point 2",
    "code point 3",
    "interpretation (display) of code point 2",
)
_HHFV_TABLE_1_ROWS = (
    ("$vav", "$u_xolam", "", "$xm-dot on $vav"),
    ("$vav", "$u_xxfv_short", "", "$xx-dot on $vav"),
    ("non-$vav", "$u_xolam", "$alef-$ML", "$xm-dot on $alef-ML"),
    ("non-$vav", "$u_xolam", "$alef-con.", "$xx-dot on non-$vav"),
    ("non-$vav", "$u_xxfv_short", "", "undefined"),
)
_HHFV_TABLE_1_INSIDE = xtable_rows_of_cells(_HHFV_TABLE_1_ROWS)
#
_HHFV_TABLE_2_HEADER_CELLS = (
    "code point 1",
    "code point 2",
    "interpretation (display) of code point 2",
)
_HHFV_TABLE_2_ROWS = (
    ("voa", "$u_xolam", "$xm-dot on voa"),
    ("voa", "$u_xxfv_short", "$xx-dot on voa"),
    ("non-voa", "$u_xolam", "$xx-dot on non-voa"),
    ("non-voa", "$u_xxfv_short", "undefined"),
)
_HHFV_TABLE_2_INSIDE = xtable_rows_of_cells(_HHFV_TABLE_2_ROWS)
#
_HHFV_TABLE_3_HEADER_CELLS = ("today’s name", "fantasy name", "applies to")
_HHFV_TABLE_3_ROWS = (
    ("$u_xolam", "$u_hypothetical_xm", "$vav or $alef"),
    ("$u_xxfv", "$u_hypothetical_xx", "any letter"),
)
_HHFV_TABLE_3_INSIDE = xtable_rows_of_cells(_HHFV_TABLE_3_ROWS)
#
_HHFV_TABLE_4_HEADER_CELLS = (
    "code point 1",
    "code point 2",
    "interpretation (display) of code point 2",
)
_HHFV_TABLE_4_ROWS = (
    ("voa", "$u_xolam", "$xm-dot on voa"),
    ("non-voa", "$u_xolam", "undefined"),
    ("letter", "$u_xxfv_short", "$xx-dot on letter"),
)
_HHFV_TABLE_4_INSIDE = xtable_rows_of_cells(_HHFV_TABLE_4_ROWS)
#
BIG_STR = (
    headfun()
    + para("Assuming these abbreviations:")
    + to_str(xtable(_HHFV_ABBREVS_HEADER_CELLS, _HHFV_ABBREVS_INSIDE))
    + para("Today we have this mess:")
    + to_str(xtable(_HHFV_TABLE_1_HEADER_CELLS, _HHFV_TABLE_1_INSIDE))
    + para(
        "Now let’s imagine that we started interpreting $u_xxfv"
        + " as if it applied to not just $vav but $alef, too."
        + " Then we’d have this simpler situation:"
    )
    + to_str(xtable(_HHFV_TABLE_2_HEADER_CELLS, _HHFV_TABLE_2_INSIDE))
    + para(
        "As long as we’re indulging our fantasies, now let’s imagine"
        + " things as they really should have been:"
    )
    + to_str(xtable(_HHFV_TABLE_3_HEADER_CELLS, _HHFV_TABLE_3_INSIDE))
    + para("Or, in the style of our tables above:")
    + to_str(xtable(_HHFV_TABLE_4_HEADER_CELLS, _HHFV_TABLE_4_INSIDE))
    + """"""
)
