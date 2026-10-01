import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_CONT_FTNT_NOT_SCRUPULOUS = [
    "In manuscripts that are not scrupulous about stroke angles,",
    " $gaya can be easily confused with a ",
    sub.merka(),  # translit-ok
    " used as a secondary accent.",
]
_CONT_FTNT_GAYA_AFTER_PRISTRESS = [
    ["See ", hlp.rtn(332)],
    [" for an example of a type of  $gaya that,"],
    [" extraordinarily, comes after the stress."],
]
_CONT_FTNT_TO_THE_RIGHT = [
    ["I.e., slanted counterclockwise from the vertical, like ", sub.tifxa(), "."],
    [" I.e. to the right, assuming the mark is made starting at its top."],
]
_CONT_FTNT_TO_THE_LEFT = [
    "I.e., slanted clockwise from the vertical."
    " I.e. to the left, assuming the mark is made starting at its top."
]
_CONT_FTNT_TIFXA = [
    ["This slanted form could be confused with ", sub.mayela(), "."],
    [" But this is still the better slant, since ", sub.merka(), ","],  # translit-ok
    [" unlike ", sub.mayela(), ","],
    [" can often be used where $gaya is used."],
]
_FTNT_NOT_SCRUPULOUS = sub.footnote(_CONT_FTNT_NOT_SCRUPULOUS)
_FTNT_GAYA_AFTER_PRISTRESS = sub.footnote(_CONT_FTNT_GAYA_AFTER_PRISTRESS)
_FTNT_TO_THE_RIGHT = sub.footnote(_CONT_FTNT_TO_THE_RIGHT)
_FTNT_TO_THE_LEFT = sub.footnote(_CONT_FTNT_TO_THE_LEFT)
_FTNT_TIFXA = sub.footnote(_CONT_FTNT_TIFXA)
_PARA_1_CONT = [
    ["$Gaya is a short vertical stroke under the word "],
    hlp.paren(
        [
            "generally on a syllable before the main stress syllable,"
            " on which most primary accent signs are marked"
        ]
    ),
    ". In printed texts the"
    " stroke is really vertical, and this is also the case in most"
    " manuscripts, but in some manuscripts it is slanted a little ",
    hlp.ftntjoin("to the right", _FTNT_TO_THE_RIGHT),
    " ",
    hlp.paren(
        [
            ["to distinguish it from ", sub.merka()],  # translit-ok
            hlp.ftntjoin(",", _FTNT_TIFXA),
            " which is slanted ",
            hlp.ftntjoin("to the left", _FTNT_TO_THE_LEFT),
        ]
    ),
    [". The ", sub.horayat(), " says that bA and bN use this slanted form of "],
    ["the sign, but it is characteristic of only a few early manuscripts."],
]
_PARA_2_CONT = [
    ["$Gaya forms part of the accent system, and is generally"],
    [" marked only in manuscripts in which the accent signs are marked, and"],
    [" not in those which mark only vowel signs. $Gaya is not easily"],
    [" confused with a word’s primary accent sign,"],
    [" even if that sign is ", sub.silluq(), "."],
    [" This is because $gaya"],
    [" is generally marked before the stress syllable,"],
    [" while most primary accent signs are marked on the stress syllable"],
    hlp.ftntjoin2(".", _FTNT_NOT_SCRUPULOUS, _FTNT_GAYA_AFTER_PRISTRESS),
]

SEC = [
    sub.para(_PARA_1_CONT),
    sub.para(_PARA_2_CONT),
]
