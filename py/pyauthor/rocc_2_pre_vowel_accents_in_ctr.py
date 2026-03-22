"""Exports main"""

from py_misc import my_html
from pyauthor_util import author
from pyauthor import rocc_1_on_the_provenance_of_ctr as prov
from pycmn.my_utils import intersperse
from pyauthor_util.author import hbo


def anchor():
    return author.std_anchor(_ANCHOR, _H1_CONTENTS)


def gen_html_file(tdm_ch):
    return author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, _CBODY)


def _comma(the_list: list):
    if len(the_list) > 2:
        out = list(intersperse(", ", the_list))
        out[-2] = ", and "
        return out
    assert len(the_list) == 2
    return [the_list[0], " and ", the_list[1]]


def _plus_notation(bar):
    return hbo(f"{bar[:-1]}+{bar[:-2]}{bar[-1]}")


def _to_encode(mark_or_marks, prep, letter, bibref, s_word, f_word):
    """
    prep: preposition, e.g. "under" preceding the letter
    s_word: non-fully-pointed word
    f_word: fully-pointed word
    bibref: e.g. "Psalm 32:3"
    """
    if f_word:
        f_word_seq = " (fully: ", hbo(f_word), "$thinsp)"
    else:
        f_word_seq = []
    return [
        [f"to encode the {mark_or_marks}"],
        [f" {prep} the letter {letter} in ", hbo(s_word)],
        [f" ({bibref})", *f_word_seq, ","],
    ]


def _unlikely(hbo_cont):
    return [
        ["This is very unlikely to have the desired appearance in most fonts."],
        [" Plus, in normalizing contexts like most web browsers,"],
        [" the font won’t even get a chance to try."],
        [" In this document’s context, it will look like this:"],
        [" ", hbo(hbo_cont), "."],
    ]


def _instead(normal, weird):
    return _instead_f("instead", normal, weird)


def _instead_c(normal, weird):
    return _instead_f("Instead", normal, weird)


def _instead_f(instead, normal, weird):
    return f"{instead} of ", normal, ", $CTR uses ", weird, "."


def _instead_plus(normal, weird):
    return [
        ["I.e., ", _instead(_plus_notation(normal), _plus_notation(weird))],
        [" (The plus sign expression indicates a kind of concatenation,"],
        [" and is meant to be read right to left.)"],
    ]


def _normal(foo, bar_or_baz):
    if bar_or_baz.endswith(" (!)"):
        return bar_or_baz
    return f"{bar_or_baz} (the normal meaning of {foo})"


def _codes_both_summary(foo, bar, baz):
    return [
        f"The code point {foo} means either {bar} or {baz}, depending on context.",
        author.unordered_list(
            [
                f"Before a vowel, it means {_normal(foo, bar)}.",
                f"After a vowel (the normal order), it means {_normal(foo, baz)}.",
            ]
        ),
    ]


def _codes_both_detail(foo, bar, baz):
    return [
        [
            f"The code point {foo} before a vowel means {bar}, e.g. ",
            _EXAMPLES_BEFORE_VOWEL[foo],
        ],
        [
            f"The code point {foo} after a vowel means {baz}, e.g. ",
            _EXAMPLES_AFTER_VOWEL[foo],
        ],
    ]


_TITLE = "Pre-vowel Accents in Chabad’s CTR"
_H1_CONTENTS = "Pre-vowel Accents in Chabad’s $CTR"
_FNAME = "rocc_2_pre_vowel_accents_in_ctr.html"
_ANCHOR = my_html.anchor_h("document", f"./{_FNAME}")
_TIPEHA_BEFORE_VOWEL_INTRO = _to_encode(
    "$segol and $dexi", "under", "$hehe", "Psalm 32:3", "הֶ֭חרשתי", "הֶ֭חֱרַשְׁתִּי"
)
# (more commonly transliterated as $gaya_with_half_ring_for_ayin)
_Y_ABOVE = """Above I have ignored a $gaya
that $CTR also has under the $hehe.
I have ignored it because
(1) it is not relevant to the issue at hand and
(2) it is one of many “extra” $gaya marks that $CTR has
compared to many other editions."""
_TIPEHA_BEFORE_VOWEL_CONT_UL = [
    _instead_c("‹$POINT_SEGOL, $DEHI›", "‹$TIPEHA, $POINT_SEGOL›"),
    _instead_plus("הֶ֭", "הֶ֖"),
    _unlikely("הֶ֖חרשתי"),
    _Y_ABOVE.replace("\n", " "),
]
_TIPEHA_AFTER_VOWEL = hbo("וְאֵ֖ין"), " (Psalm 32:2)."
_GERESH_BEFORE_VOWEL_INTRO = _to_encode(
    "$tsere and $germuq", "on", "$alef", "Psalm 32:6", "אֵ֝ליו", "אֵ֝לָ֗יו"
)
_GERESH_BEFORE_VOWEL_CONT_UL = [
    _instead_c("‹$TSERE, $GERMUQ›", "‹$GERESH, $TSERE›"),
    _instead_plus("אֵ֝", "אֵ֜"),
    [
        ["This is very unlikely to have quite the desired appearance in most fonts,"],
        [" though the appearance will likely be close to what is desired."],
        [" In normalizing contexts like most web browsers,"],
        [" the font won’t even get a chance to try."],
        [" In this document’s context, it will look like this:"],
        [" ", hbo("אֵ֜ליו"), "."],
        [" Because the two marks in question are not both below-marks,"],
        [" this looks pretty close to the desired appearance."],
        [" But it is still not quite what is desired."],
    ],
]
_GERESH_AFTER_VOWEL = hbo("הַמַּ֜יִם"), " (Genesis 1:9)."
_YETIV_BEFORE_VOWEL_INTRO = _to_encode(
    "$xiriq and $yetiv", "under", "$kaf", "Joshua 2:11", "כִּ֚י", None
)
_YETIV_BEFORE_VOWEL_CONT_UL = [
    _instead_c("‹$HIRIQ, $YETIV›", "‹$YETIV, $HIRIQ›"),
    _instead_plus("כִּ֚", "כִּ֚"),
    [
        ["Although this is a strange order to encode it in,"],
        [" this is very likely to have the desired appearance in most fonts."],
    ],
]
_YETIV_AFTER_VOWEL_INTRO = _to_encode(
    "$qamats and $mahapakh", "under", "$tav", "Psalm 32:7", "אתָּ֤ה", "אַתָּ֤ה׀"
)
_YETIV_AFTER_VOWEL_CONT_UL = [
    _instead_c("‹$QAMATS, $MAHAPAKH›", "‹$QAMATS, $YETIV›"),
    _instead_plus("תָּ֤", "תָּ֚"),
    _unlikely("אתָּ֚ה"),
]

_EXAMPLES_BEFORE_VOWEL = {
    "$TIPEHA": [
        *_TIPEHA_BEFORE_VOWEL_INTRO,
        author.unordered_list(_TIPEHA_BEFORE_VOWEL_CONT_UL),
    ],
    "$GERESH": [
        *_GERESH_BEFORE_VOWEL_INTRO,
        author.unordered_list(_GERESH_BEFORE_VOWEL_CONT_UL),
    ],
    "$YETIV": [
        *_YETIV_BEFORE_VOWEL_INTRO,
        author.unordered_list(_YETIV_BEFORE_VOWEL_CONT_UL),
    ],
}
_EXAMPLES_AFTER_VOWEL = {
    "$TIPEHA": _TIPEHA_AFTER_VOWEL,
    "$GERESH": _GERESH_AFTER_VOWEL,
    "$YETIV": [
        *_YETIV_AFTER_VOWEL_INTRO,
        author.unordered_list(_YETIV_AFTER_VOWEL_CONT_UL),
    ],
}
_CONT_PARA_01 = [
    ["The $anc_Chabad_website has an edition of the Hebrew Bible"],
    [" called $anc_Chabad_CTR ($CTR)."],
    [" ", author.paren(["See my ", prov.anchor()])],
]
_CONT_PARA_02 = """The $CTR edition distinguishes three pairs of accents
using a nonstandard mechanism rather than using the code points
dedicated to making these distinctions.
On a letter with a code point for a vowel mark (including $HOLAM), $CTR
distinguishes the following prepositives from their impositive “lookalikes”
by the logical order of an accent code point relative to that vowel:""".replace(
    "\n", " "
)
_CODES_BOTH_TIPEHA = "$TIPEHA", "$dexi (!)", "$tarxa$hs_sl_hs$tipeha"
_CODES_BOTH_GERESH = "$GERESH", "$germuq (!)", "$geresh"
_CODES_BOTH_YETIV = "$YETIV", "$yetiv", "$mahapakh (!)"
_CONT_02_UL = [
    _codes_both_summary(*_CODES_BOTH_TIPEHA),
    _codes_both_summary(*_CODES_BOTH_GERESH),
    _codes_both_summary(*_CODES_BOTH_YETIV),
]
_CONT_PARA_03 = """There are four levels of strangeness here.""".replace("\n", " ")
_CONT_03_UL = [
    [
        ["As mentioned above,"],
        [" there are code points dedicated to making these distinctions."],
        [" These code points have been around since"],
        [" the introduction of Hebrew accent code points, in Unicode 2.0."],
    ],
    [
        ["The accent-before-vowel order"],
        [" will be normalized away in some environments,"],
        [" notably, in most web browsers."],
    ],
    [
        ["The use of $YETIV breaks the pattern established by $TIPEHA and $GERESH,"],
        [" where the impositive code point does double duty,"],
        [" and the prepositive code point is not used."],
        [" If the pattern were followed,"],
        [" $MAHAPAKH rather than $YETIV would be used:"],
        [" $MAHAPAKH before a vowel would mean $yetiv"],
        [" (surprising but at least following the pattern) and"],
        [" $MAHAPAKH after a vowel (the normal order) would mean $mahapakh"],
        [" (the normal meaning of $MAHAPAKH)."],
    ],
    [
        ["No font I am aware of will “understand” this encoding."],
    ],
]
_CONT_PARA_04 = """In some but not all cases,
the logical order of these code points
reflects a desired horizontal visual order.
Even when it does reflect a desired visual order,
this visual order is very unlikely to be achieved,
except in the case of $YETIV before a vowel.
In all other cases,
few if any fonts will render the marks in the desired visual order, and
in normalizing contexts like most web browsers,
the font won’t even get a chance to try.
In detail:""".replace("\n", " ")
_CONT_04_UL = [
    *_codes_both_detail(*_CODES_BOTH_TIPEHA),
    *_codes_both_detail(*_CODES_BOTH_GERESH),
    *_codes_both_detail(*_CODES_BOTH_YETIV),
]
_RCC = "(rendering $CTR’s contents in this document’s context)"
_CONT_PARA_05 = [
    ["As noted above, $CTR’s strange vowel-relative distinctions"],
    [" apply not only to the below-vowels but also to the one above-vowel, $HOLAM."],
]
_CONT_PARA_10D_LI_1 = [
    ["The $TIPEHA code point before $HOLAM means $dexi,"],
    [" e.g. ", _RCC],
    [" ", _comma([hbo("אֹ֖זֶן"), hbo("אֹ֖מֶר"), hbo("כָּל־רֹ֖אַי")])],
    [" (Psalm ", _comma(["18:45", "19:4", "22:8"]), ")."],
    [" But, consistent with the general sloppiness of $CTR,"],
    [" sometimes $TIPEHA appears after $HOLAM,"],
    [" even when a $dexi is (or should be) intended,"],
    [" e.g. ", _RCC],
    [" in ", _comma([hbo("בֹּ֖קֶר"), hbo("עֹ֖ז")])],
    [" (Psalm ", _comma(["5:4", "22:11"]), ")."],
    [" Note that $TIPEHA before $HOLAM"],
    [" is somewhat analogous to $GERESH before a below-vowel."],
    [" In both cases,"],
    [" the logical order does not reflect a desired horizontal visual order,"],
    [" since in each case,"],
    [" one of the marks is a below-mark and the other is an above-mark."],
    [" Rather, the logical order reflects"],
    [" at most a desired horizontal visual alignment"],
    [" (right-biased rather than centered)"],
    [" of the accent relative to a vowel-free area of its letter."],
    [" (That area being the letter’s top for $GERESH and bottom for $TIPEHA)."],
    [" Because this is completely nonstandard, the desired visual alignment"],
    [" is very unlikely to be achieved in most or all fonts."],
]
_CONT_PARA_10D_LI_2 = [
    ["The $GERESH code point before $HOLAM means $germuq,"],
    [" e.g. ", _RCC],
    [" ", _comma([hbo("מִכָּל־רֹ֜דְפַ֗י"), hbo("פֹּ֜רֵ֗ק"), hbo("כָּל־אֹ֜יְבָ֗יו")])],
    [" (Psalm ", _comma(["7:2", "7:3", "18:1"]), ")."],
    [" Note that $GERESH before $HOLAM,"],
    [" like $GERESH before a below-vowel,"],
    [" does not reflect a desired distinction in horizontal visual order,"],
    [" since both $geresh and $germuq should, visually, appear before $xolam."],
    [" Rather, the logical order reflects at most"],
    [" a desired distinction in horizontal visual alignment"],
    [" (right-biased rather than centered) of the accent relative to its letter."],
    [" Or, if you like, you can think of $GERESH logically before $HOLAM"],
    [" as meaning a $geresh visually ", my_html.emphasis("far"), " before $xolam,"],
    [" as opposed to $GERESH logically after $HOLAM,"],
    [" which means a $geresh still visually before $xolam,"],
    [" but not so far before it."],
]
_ELS = {"class": "extra-letter-spacing"}
_CONT_PARA_10D_LI_3 = [
    ["The $YETIV code point before $HOLAM means $yetiv,"],
    [" e.g. ", hbo("כֹּ֚ל"), " (Joshua 1:4) and"],
    [" $YETIV after $HOLAM means $mahapakh,"],
    [" e.g. ", _RCC, " ", hbo("יֵ֘בֹ֚שׁוּ", _ELS), " (Psalm 6:11)"],
    [" Note that $YETIV before $HOLAM"],
    [" is yet another case where"],
    [" the logical order does not reflect a desired horizontal visual order,"],
    [" since $YETIV is a below-mark and $HOLAM an above-mark."],
]
_CONT_05_UL = [_CONT_PARA_10D_LI_1, _CONT_PARA_10D_LI_2, _CONT_PARA_10D_LI_3]
_CONT_PARA_06 = [
    ["One might naturally wonder how, on a letter"],
    [" ", my_html.emphasis("without"), " a vowel, $CTR encodes"],
    [" the six accents of these three “lookalike” pairs."],
    [" I.e. one might naturally wonder how these six accents are encoded"],
    [" when they are “bare,” i.e. not sharing their letter with a vowel mark."],
]
_CONT_06_UL = [
    [
        ["The $TIPEHA code point is used for both bare $dexi and bare $tarxa."],
        [" This results in an ambiguity."],
        [" E.g. $CTR codes the bare $dexi in ", hbo("כִּי־ה֭וּא"), " (Psalm 24:2)"],
        [" as $TIPEHA."],
        [" In this document’s context, that $TIPEHA will look like this:"],
        [" ", hbo("ה֖וּא"), "$thinsp, i.e. it will look like a $tarxa."],
        [" This makes it indistinguishable, for example,"],
        [" from the bare $tarxa Psalm 59:5 ", hbo("ע֖וּרָה"), "$thinsp."],
    ],
    [
        ["The $GERESH code point is used for both bare $germuq and bare $geresh."],
        [" These accents are exclusive"],
        [" to the poetic and prose systems respectively"],
        [" so even when these accents are bare,"],
        [" there is no ambiguity"],
        [" (assuming we know what accent system the word belongs to)."],
        [" As always,"],
        [" it is important to be aware that though Job is,"],
        [" for the most part, a poetically-accented book,"],
        [" its introduction and conclusion are prose-accented."],
        [" So, a bare $geresh in Job could be either a $germuq or $geresh,"],
        [" depending on whether or not"],
        [" its verse is in the range 3:2 to 42:6 (inclusive)."],
    ],
    [
        ["The $YETIV code point is used for both bare $yetiv and bare $mahapakh."],
        [" $Yetiv is exclusive to the prose system"],
        [" so there is no ambiguity"],
        [" if we know that the word belongs to the poetic system."],
        [" If the word belongs to the prose system, then $YETIV is ambiguous."],
    ],
    [
        ["With no pattern I can discern, sometimes"],
        [" $MAHAPAKH is used for a bare $mahapakh, as in"],
        [" ", hbo("שִׂמְח֤וּ"), " (Psalm 32:11)."],
    ],
]
_CONT_PARA_07 = """In conclusion,
$CTR uses and abuses Unicode in strange ways that in most environments
(font, browser, etc.) will not have the desired effect.""".replace("\n", " ")
_CBODY = [
    author.heading_level_1(_H1_CONTENTS),
    author.para(_CONT_PARA_01),
    author.para_ul(_CONT_PARA_02, _CONT_02_UL),
    author.para_ul(_CONT_PARA_03, _CONT_03_UL),
    author.para_ol(_CONT_PARA_04, _CONT_04_UL),
    author.para_ul(_CONT_PARA_05, _CONT_05_UL),
    author.para_ul(_CONT_PARA_06, _CONT_06_UL),
    author.para(_CONT_PARA_07),
]
