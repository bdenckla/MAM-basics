"""Exports gen_html_file"""

from boj_render import boj_html
from mb_cmn import bib_locales as tbn
from author_boj_util import author
from author_boj_util.common_titles_etc import D5_TITLE, D5_H1_CONTENTS, D5_FNAME

_MWD = "https://bdenckla.github.io/MAM-basics/MAM-with-doc"
_UXLC = "https://tanach.us/Tanach.xml"


def gen_html_file(tdm_ch):
    author.assert_stem_eq(__file__, D5_FNAME)
    cbody = _make_cbody()
    author.help_gen_html_file(tdm_ch, D5_FNAME, D5_TITLE, cbody)


def _links_to_u_and_m(bkid, ch, vr):
    cv = f"{ch}:{vr}"
    cn_v_vn = f"c{ch}v{vr}"
    osdf = tbn.ordered_short_dash_full_39(bkid)
    u = boj_html.anchor_h("U", f"{_UXLC}?{bkid}{cv}")
    m = boj_html.anchor_h("M", f"{_MWD}/{osdf}.html#{cn_v_vn}")
    return u, ", ", m


def _make_cbody():
    return [
        author.heading_level_1(D5_H1_CONTENTS),
        author.para(_INTRO),
        #
        author.heading_level_2("$2Kings_4_7"),
        author.para(_KINGS_INTRO),
        author.para(_KINGS_DISCUSSION_1),
        author.para(_KINGS_DISCUSSION_2),
        author.para(_KINGS_DISCUSSION_3),
        _img("Aleppo-2Kings-c4v7.png"),
        _img("Lenin-2Kings-c4v7.png"),
        author.para(_KINGS_DISCUSSION_4),
        author.para(_KINGS_DISCUSSION_5),
        author.para(_KINGS_DISCUSSION_6),
        #
        author.heading_level_2("$Lamentations_4_16"),
        author.para(_LAMENTATIONS_INTRO),
        author.para(_LAMENTATIONS_DISCUSSION_1),
        _img("Sassoon-1053-Lamentations-c4v16.png"),
        author.para(_LAMENTATIONS_DISCUSSION_2),
        #
        author.heading_level_2("$2Samuel_18_20"),
        author.para(_SAMUEL_INTRO),
        author.para(_SAMUEL_DISCUSSION_1),
        _img("Lenin-2Samuel-c18v20.png"),
        author.para(_SAMUEL_DISCUSSION_2),
    ]


def _img(img):
    return author.para_for_img(img, "maxwidth50pc")


_INTRO = [
    "In Job $link_38_12_YD3F_HJXR, the Jerusalem Crown edition puts a פתח on no letter.",
    " The פתח floats before the ש of %שחר.",
    #
    " Although neither μA nor μL presents this כתיב/קרי like this,",
    " there is manuscript precedent for such a floating presentation.",
    " This page presents some examples of that precedent.",
]

_KINGS_INTRO = [
    ["In $2Kings_4_7 (", *_links_to_u_and_m(tbn.BK_SND_KGS, 4, 7), "),"],
    [" there is a קרי of ", author.hbo("וּבָנַ֔יִךְ")],
    [" corresponding to a כתיב of ", author.hbo("בניכי"), "."],
]
_KINGS_DISCUSSION_1 = [
    "This is hard to show in the “pointed כתיב”",
    " style of קרי/כתיב presentation favored by the manuscripts.",
    " In such a style, a קובוץ floats before the ב of %בניכי.",
    " The קובוץ is an orphan: it belongs to no letter of the כתיב word.",
]
_WLCAU = "https://bdenckla.github.io/MAM-basics/wlc/wlc-a-notes/"
_KINGS_DISCUSSION_2 = [
    "Actually, it belongs to no letter of the קרי word either!",
    #
    " But it is understood to represent a שורוק.",
    #
    " Or, another way of looking at this קובוץ is that",
    " it is understood to represent just a שורוק dot,",
    " not the entire שורוק.",
    #
]
_KINGS_DISCUSSION_3 = [
    "The first image below is from μA; the second is from μL.",
    " The קובוץ is faint in μL, almost invisible.",
    " (They are under the ת of the previous word.)",
]
_KINGS_DISCUSSION_4 = [
    "My assumption is that a שורוק dot was not allowed to be an orphan",
    " for one or more of the following reasons:",
    " (1) it is placed too high, i.e. not a below-mark,",
    " (2) it is too small, and",
    " (3) it has too many other meanings (דגש and מפיק).",
]
_KINGS_DISCUSSION_5 = [
    "It is more common for a כתיב to lack a final שורוק",
    " than for it to lack initial שורוק.",
    #
    " When a כתיב lacks a final שורוק, we see a related use of קובוץ.",
    #
    " An example is found in $1Samuel_12_10",
    [" (", *_links_to_u_and_m(tbn.BK_FST_SAM, 12, 10), ")"],
    " where, in Tiberian manuscripts,",
    [" a pointed כתיב of ", author.hbo("וַיֹּאמְרֻ֣")],
    [" is paired with an unpointed קרי of ", author.hbo("ויאמרו"), "."],
    #
    " In many printed editions, this would be shown as",
    [" an unpointed כתיב of ", author.hbo("ויאמר")],
    [" paired with a pointed קרי of ", author.hbo("וַיֹּאמְר֣וּ"), "."],
]
_KINGS_DISCUSSION_6 = [
    ["Note that the קובוץ of ", author.hbo("וַיֹּאמְרֻ֣"), " is not really an orphan,"],
    " since it belongs to the last letter of the word (ר)."
    #
    " Nevertheless, I consider the notations to be related, if not strictly analogous.",
    [" See ", author.anc_h("this list of $WLC a-notes", _WLCAU)],
    " for more examples of final קובוץ.",
    #
    " Also, that list shows many examples where דגש is not allowed to be an orphan,",
    " supporting my claims as to why שורוק dot, too, is not allowed to be an orphan.",
]

_LAMENTATIONS_INTRO = [
    ["In $Lamentations_4_16 (", *_links_to_u_and_m(tbn.BK_LAMENT, 4, 16), "),"],
    [" there is a קרי of ", author.hbo("וּזְקֵנִ֖ים")],
    [" corresponding to a כתיב of ", author.hbo("זקנים"), "."],
]
_LAMENTATIONS_DISCUSSION_1 = [
    "As in $2Kings_4_7,",
    " the קובוץ floats before the first letter of the word,",
    " which in this case is ז.",
    " Here is the way this word looks in Sassoon 1053:",
]
_LAMENTATIONS_DISCUSSION_2 = [
    "(We provide an image from Sassoon 1053 rather than from μA and/or μL because",
    " μA is lost here and",
    " μL does not use this (or any other)",
    " notation representing the שורוק dot in the קרי.)",
]

_SAMUEL_INTRO = [
    ["$2Samuel_18_20 (", *_links_to_u_and_m(tbn.BK_SND_SAM, 18, 20), ")"],
    [" is a קרי ולא כתיב: the word ", author.hbo("כֵּ֥ן")],
    " is read but not written, where by “not written” we mean not written in formal texts.",
    #
    " Such formal texts include the main columns of a Tiberian manuscript",
    " and the text of an unpointed scroll.",
]
_SAMUEL_DISCUSSION_1 = [
    "So, in the main columns of a Tiberian manuscript, there are no letters %כן",
    " on which to put the קרי pointing.",
    #
    " This represents a more extreme case of orphan קרי points than the previous two examples,"
    " since there is no word to which the orphan points can “snuggle up” to.",
    #
    " In other words, the vowel and accent marks of the קרי word, %כן,",
    " float in the space between the surrounding כתיב words.",
    #
    " Or rather, the marks would float in that space if enough space had been left for them.",
    #
    " As it is, they reside somewhat awkwardly and confusingly beneath the ל.",
]
_SAMUEL_DISCUSSION_2 = [
    "Several other examples of complete orphans like this can be found in the same",
    [" ", author.anc_h("list of $WLC a-notes", _WLCAU), " mentioned above."],
]
