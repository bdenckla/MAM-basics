""" Exports main """

from py_misc import my_html
from pyauthor_util import author


def anchor():
    return author.std_anchor(_ANCHOR, _H1_CONTENTS)


def gen_html_file(tdm_ch):
    cbody = [
        author.heading_level_1(_H1_CONTENTS),
        author.para(_CONT_PARA_06A),
        author.para(_CONT_PARA_06B, {"class": "center-and-spaced"}),
        author.para(_CONT_PARA_07),
        author.para(_CONT_PARA_08, {"class": "center-and-spaced"}),
        author.para(_CONT_PARA_09),
        author.para(_CONT_PARA_10),
        author.para(_CONT_PARA_11, {"class": "center-and-spaced"}),
        author.para(_CONT_PARA_12),
        author.para_for_img("BHS/Psalm 32v5 ועוני -- BHS.png"),
        author.para(_CONT_PARA_13A),
        author.para_for_img("BHS/Psalm 32v5 ועוני -- BHS - speculative.png"),
        author.para(_CONT_PARA_13B),
        author.para_for_img("BHS/Job 15v23 נדד -- BHS.jpg", "width10em"),
        author.para_for_img("BHS/Job 34v37 יסיף -- BHS.png", "width10em"),
        author.para(_CONT_PARA_14),
        author.para_for_img("BHS/Psalm 2v7 אמר -- BHS.png", "width10em"),
        author.para(_CONT_PARA_15),
        author.para_for_img("BHS/Job 39v25 יאמר -- BHS.jpg", "width10em"),
        author.para_for_img("BHS/Psalm 9v10 ויהי -- BHS.jpg", "width10em"),
        author.para_for_img("BHS/Psalm 10v3 נאץ -- BHS.jpg", "width10em"),
        # para_for_img("BHS/Psalm 10v5 יחילו -- BHS.jpg", "width10em"),
        # para_for_img("BHS/Psalm 96v4 גדול -- BHS.jpg", "width10em"),
        author.para(_CONT_PARA_16),
    ]
    author.assert_stem_eq(__file__, _FNAME)
    author.help_gen_html_file(tdm_ch, _FNAME, _TITLE, cbody)


_TITLE = "Tsinnorit and the Ḥolam Ḥaser dot in BHS"
_H1_CONTENTS = "$Tsinnorit and the $Xolam_xaser Dot in $BHS"
_FNAME = "tsinnorit_and_the_xxd_in_bhs.html"
_ANCHOR = my_html.anchor_h("document", f"./{_FNAME}")
_CONT_PARA_06A = [
    ["A $tsinnorit"],
    [" and a $xolam_xaser dot"],
    [" must share a $vav in Psalm 32:5 ועוני:"],
]
_CONT_PARA_06B = [author.hbo_big("וַעֲוֺ֘נִ֤י")]
_CONT_PARA_07 = """This word is typographically challenging, particularly with the
“tilde” form of $tsinnorit. (This “tilde” form is the form shown above.) It is
challenging because the $tsinnorit contends for space with a $xolam_xaser dot
on a narrow letter, namely, $vav. This challenge is also present in three
words in Job (15:23, 34:37, and 39:25).""".replace("\n", " ")
_CONT_PARA_08 = [[author.hbo_big("נֹ֘דֵ֤ד יֹ֘סִ֤יף יֹ֘אמַ֤ר")]]
_CONT_PARA_09 = [
    ["(In some fonts such as the font used above,"],
    [" the challenge is not as great in יאמר as it is in נדד and יסיף."],
    [" It is not as great because in those fonts, the $xolam_xaser dot"],
    [" is pulled forward onto the $alef.)"],
]
_CONT_PARA_10 = [
    ["An analogous challenge is present with the $zarqa"],
    [" helper in 2 Sam 3:8 and Isaiah 18:2:"],
]
_CONT_PARA_11 = [[author.hbo_big("אָנֹ֘כִי֮ וּבִכְלֵי־גֹ֘מֶא֮")]]
_CONT_PARA_12 = [
    ["Getting back to Psalm 32:5 ועוני specifically,"],
    [" its typographic challenge may help explain why, in $BHS,"],
    [" the $tsinnorit appears a bit early:"],
]
_CONT_PARA_13A = [
    ["On the other hand, the challenge is not as great in"],
    [" $BHS because it uses the “cane”"],
    [" rather than the “tilde” form of $tsinnorit,"],
    [" freeing up enough space, in theory, for the $tsinnorit"],
    [" to be centered on the $vav if that were desired."],
    [" For example, consider the following speculative rendering of ועוני:"],
]
_CONT_PARA_13B = [
    ["Perhaps, in practice, that was not feasible,"],
    [" given the technology used to typeset $BHS."],
    [" $Tsinnorit is pretty early on the two other words"],
    [" in Job that have the same typographic challenge,"],
    [" strongly suggesting that whatever the reason for the early placement,"],
    [" it was not some quirk specific to Psalm 32:5 ועוני:"],
]
_CONT_PARA_14 = [
    ["One might think that $BHS"],
    [" puts $tsinnorit early on its letter"],
    [" not because of space constraints, but rather to mimic the placement"],
    [" found in some manuscripts."],
    [" But, from examples on wide letters,"],
    [" such as the $mem below in Psalm 2:7 אמר,"],
    [" we can see that this is not the case:"],
    [" the $tsinnorit is centered."],
]
_CONT_PARA_15 = [
    ["It is also pretty clear, even on narrow letters, that centering $tsinnorit"],
    [" was the goal,"],
    [" as can be seen in the following examples,"],
    [" which include Job 39:25 יאמר, a non-challenging case"],
    [" because in $BHS the $xolam_xaser"],
    [" dot is pulled forward onto the $alef:"],
]
_CONT_PARA_16 = [
    ["Regardless of why $BHS puts $tsinnorit"],
    [" early on narrow letters"],
    [" with a $xolam_xaser dot,"],
    [" the fact remains that it does so."],
]
