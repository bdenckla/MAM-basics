"""Exports main"""

from py_misc import my_html
from pyauthor_util import author
from pyauthor import tsinnorit_and_the_xxd_in_bhs as tatx_in_bhs


def anchor():
    return author.std_anchor(_ANCHOR, _H1_CONTENTS)


def gen_html_file(tdm_ch):
    cbody = [
        author.heading_level_1(_H1_CONTENTS),
        author.para(_CONT_PARA_06A),
        author.table_c(_CONT_TABLE),
        author.para(_CONT_PARA_06B),
        author.unordered_list(_CONT_UL),
        author.para(_CONT_PARA_06C),
        author.para(_CONT_PARA_06D),
        author.para(_CONT_PARA_07),
        author.para(_CONT_PARA_08),
    ]
    return author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, cbody)


_TITLE = "Tsinnorit in Psalm 32:5 ועוני"
_H1_CONTENTS = "$Tsinnorit in Psalm 32:5 ועוני"
_FNAME = "tsinnorit_in_psalm_32v5.html"
_ANCHOR = my_html.anchor_h("document", f"./{_FNAME}")
_CONT_PARA_06A = """What accents, if any, can appear on a non-initial vocal $shewa? The
answer is: none, except for a misplaced $tsinnorit that is seen in
Psalm 32:5 ועוני in some editions. In these editions, the $tsinnorit
of ועוני appears on its $ayin whereas it should appear on its
second $vav:""".replace("\n", " ")
_CONT_CELLS = [
    ["wrong", author.hbo_big_es("וַעֲ֘וֺנִ֤י")],
    ["right", author.hbo_big_es("וַעֲוֺ֘נִ֤י")],
]
_CONT_PARA_06B = """I've found this error in these editions:""".replace("\n", " ")
_URL_MMA = "https://mechon-mamre.org/c/ct/c2632.htm"
_URL_CTR = "https://www.chabad.org/library/bible_cdo/aid/16253/#lt=he"
_ANC_MMA = my_html.anchor_h("Mechon Mamre", _URL_MMA)
_ANC_CTR = my_html.anchor_h("Chabad", _URL_CTR)
_CONT_UL = [
    ['Tana"kh (', _ANC_MMA, ")"],
    ["Complete Tanach with Rashi (", _ANC_CTR, ") (Judaica Press)"],
]
# (more commonly transliterated as $gaya_with_half_ring_for_ayin)
_CONT_PARA_06C = """(Both of the above editions also have a $gaya
on the first $vav,
but that is a legitimate variant.
This variant reflects the more $gaya-heavy style
associated with the printed tradition
rather than the tradition of the most authoritative manuscripts.)""".replace("\n", " ")
_CONT_PARA_06D = """(In the Chabad edition, this word has
two other problems.
(1) Instead of Unicode $HOLAM_HASER_FOR_VAV, it uses $ZWJ followed by $HOLAM.
(2) Instead of $MAHAPAKH, it uses $YETIV.
Those two problems are widespread in the Chabad edition,
i.e., not specific to this word.)""".replace("\n", " ")
_CONT_TABLE = [
    my_html.table_row_of_data(_CONT_CELLS[0]),
    my_html.table_row_of_data(_CONT_CELLS[1]),
]
_CONT_PARA_07 = [
    "The correctly-accented version of this word is typographically challenging,",
    " particularly with the “tilde” form of $tsinnorit. (This “tilde” form is the",
    " form shown above.) It is challenging because the $tsinnorit contends for",
    " space with a $xolam_xaser dot on a narrow letter, namely, $vav.",
]
_ANC_PRE_PRE = "For info about how $BHS meets these typographic challenges, see my "
_CONT_PARA_08 = author.paren([_ANC_PRE_PRE, tatx_in_bhs.anchor()])
