"""Exports main"""

from py_misc import my_html
from pyauthor_util import author


def anchor():
    return author.std_anchor(_ANCHOR, _H1_CONTENTS)


def gen_html_file(tdm_ch):
    cbody = [
        author.heading_level_1(_H1_CONTENTS),
        author.para(_CONT_PARA_04A1),
        author.para(_CONT_PARA_04A2),
        author.para(_CONT_PARA_04B),
        author.para(_CONT_PARA_04D),
        author.para(_CONT_PARA_04F),
        author.para(_CONT_PARA_04G),
    ]
    author.assert_stem_eq(__file__, _FNAME)
    author.help_gen_html_file(tdm_ch, _FNAME, _TITLE, cbody)


_TITLE = "About Tsinnorit & Oleh"
_H1_CONTENTS = "About $Tsinnorit & $Oleh"
_FNAME = "tsinnorit_and_oleh_facts.html"
_ANCHOR = my_html.anchor_h("document", f"./{_FNAME}")
_CONT_PARA_04A1 = [
    "$Tsinnorit and $oleh always appear as part of a pair.",
    " $Tsinnorit is always paired with either",
    " $merkha or $mahapakh.",
    " $Oleh is always paired with $yored.",
    " ($Yored looks the same as $merkha,",
    " although their roles are quite different.)",
    " These partner accents ($merkha, $mahapakh, and $yored)",
    " behave like normal accents, which among other things means",
    " they never appear on an initial vocal $shewa.",
]
# XXX TODO metsunnar vs metsunneret
_CONT_PARA_04A2 = [
    "Because $oleh is always paired with $yored,",
    " in many contexts it is useful to think of them as forming",
    " a single accent that happens to require two marks.",
    " This accent is called $oleh_veyored.",
    " Similarly, in many contexts it is useful to think of the $tsinnorit pairs",
    " as $merkha_metsunneret and $mahapakh_metsunneret,",
    " although these names are not widely used.",
    " Note that these are all somewhat analogous to the two-mark accent $revmug,",
    " especially in editions where the $revia of $revmug is always explicit.",
]
_CONT_PARA_04B = [
    "$Yored never appears without $oleh, but $merkha and $mahapakh can appear without $tsinnorit.",
]
_CONT_PARA_04D = [
    "Neither $tsinnorit nor $oleh is ever the primary accent on its word.",
    " $Yored is always the primary accent on its word,",
    " but the partners of $tsinnorit may or may not be the primary accent on their words.",
]
_CONT_PARA_04F = [
    "$Oleh usually appears before $yored but, rarely, can appear on the same letter as $yored.",
]
_CONT_PARA_04G = [
    "$Tsinnorit always appears before its partner.",
]
