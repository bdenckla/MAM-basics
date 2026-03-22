"""Exports main"""

from py_misc import my_html
from pycmn import my_utils
from pycmn import hebrew_punctuation as hpu
from pyauthor_util import author
from pyauthor_rocc import rocc_util as ru
from pyauthor_rocc import rocc_0_review_of_ctr_header as rocc_0


def anchor():
    return author.std_anchor(_ANCHOR, _H1_CONTENTS)


def gen_html_file(tdm_ch):
    return author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, _CBODY)


def _my_join(mam, other):
    return [[mamval[0], *other[key]] for key, mamval in mam.items()]


def _gray_maqaf(string: str):
    split_result = string.split(hpu.MAQ)
    gm = author.span_gray(hpu.MAQ)
    return my_utils.intersperse(gm, split_result)


def _hbo_gray(string: str):
    return author.hbo(_gray_maqaf(string))


_TITLE = "Mid-word געיה with Shewa"
_H1_CONTENTS = "Mid-word געיה with $Shewa"
_FNAME = "rocc_4_mid_word_ga3ya_with_shewa.html"
_ANCHOR = my_html.anchor_h("document", f"./{_FNAME}")
_Y_URL_YEIVIN = "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-318_344.html#ns335"
_Y_ANC_YEIVIN = my_html.anchor_h("section 335", _Y_URL_YEIVIN)
_X_050_CPARA = [
    ["(This document is a sort of appendix to a parent ", rocc_0.anchor(), ")"],
]
_X_051_CPARA = [
    ["The combination of $gaya with $shewa"],
    [" rarely appears in the middle of a word."],
    [" It is briefly mentioned in ", _Y_ANC_YEIVIN, " of Yeivin’s"],
    [" ", author.book_title("Introduction to the Tiberian Masorah"), "."],
    [" I find eight cases in Tanakh."],
    [" They are shown below. They are shown as they appear in $MAM."],
    [" They are shown with $MAM’s special $maqaf shown in gray."],
]
_Y_070_GCS = "guttural-closed syllable"
_X_060_CTABLE = {
    "Pr 8:34": (_hbo_gray("אַ֥שְֽׁרֵי־אָדָם֮"), ""),
    "Ps 1:1": (_hbo_gray("אַ֥שְֽׁרֵי־הָאִ֗ישׁ"), ""),
    "Ps 32:2": (_hbo_gray("אַ֥שְֽׁרֵי־אָדָ֗ם"), ""),
    "Ps 40:5": (_hbo_gray("אַ֥שְֽׁרֵי־הַגֶּ֗בֶר"), ""),
    "Ps 98:9": (_hbo_gray("לִ֥פְֽנֵי־יְהֹוָ֗ה"), ""),
    "Ps 64:7": (_hbo_gray("יַ֥חְפְּֽשׂוּ־עוֹלֹ֗ת"), _Y_070_GCS),
    "Ps 89:25": (author.hbo_es("וֶ֥אֱֽמוּנָתִ֣י"), "$xataf"),
    "Ps 98:3": (author.hbo_es("וֶ֥אֱֽמוּנָתוֹ֮"), "$xataf"),
}
_X_070_CPARA = [
    ["The eight cases have a lot in common:"],
]
_X_071_LIST_ITEMS = [
    "Their first syllable has $merkha on a short vowel ($hairsp$patax, $xiriq_qatan, or $segol$hairsp).",
    [
        "Their second syllable:",
        author.unordered_list(
            [
                "Starts with $gaya with $shewa (simple $shewa or $xataf_segol$hairsp).",
                "Ends with a long vowel ($tsere or $shuruq).",
            ]
        ),
    ],
    "Their third syllable is unstressed. (In one case, it starts with $shewa: לפני־יהוה.)",
    [
        "Their fourth syllable has the primary stress.",
        " In one case, the primary accent is a conjunctive: $munax."
        " In all the other cases, it is a disjunctive ($tsinnor or $revia).",
    ],
    "In one case, there is a fifth syllable: אשרי־הגבר.",
]
_X_072_CPARA = """(Above, we use the Masoretic notion of a syllable
where vocal $shewa is not considered to be an independent syllable.
Rather, it is considered to be attached forward,
i.e. attached to the syllable right after it.)""".replace("\n", " ")
_X_073_CPARA = [
    ["Above, the Ps 64:7 case, יחפשו־עולת, is marked “", _Y_070_GCS, "”"],
    [" because the $merkha is on a guttural-closed syllable,"],
    [" i.e. the $gaya with $shewa comes right after a guttural-closed syllable."],
    [" So, it is a little different than all the other cases,"],
    [" since all the other cases have $merkha on an open syllable."],
]
_X_074_CPARA = [
    ["Above, the last two cases are marked “$xataf$thinsp”"],
    [" because the $gaya with $shewa is a $gaya with a $xataf_shewa,"],
    [" i.e. a $gaya with a (vocal) $shewa notated as a $xataf vowel"],
    [" (in this case, notated as a $xataf_segol$hairsp)."],
    [" So, they are a little different than all the other cases,"],
    [" since all the other cases are notated with a simple $shewa."],
    [" But this difference is mostly cosmetic,"],
    [" i.e. they are still quite analogous."],
    [" Those last two cases are also a little different"],
    [" because they involve a simple rather than compound word."],
    [" Again, this difference is mostly cosmetic,"],
    [" i.e. they are still quite analogous."],
]
_X_075_CPARA = [
    ["Speaking of the compound word cases,"],
    [" in all six of them, the $maqaf in $MAM"],
    [" is one of $MAM’s special $maqaf marks."],
    [" ", ru.MAM_SPECIAL_MAQAF],
]
_X_080_CPARA = "Here is $KCT (shown with $MAM for comparison):"
_Y_GWMHM = "$gaya where $MAM has $merkha"
_Y_KCT_8925 = [_Y_GWMHM, "; ", "no $gaya with $shewa"]
_Y_KCT_9803 = "same as above but with $gaya on $mem"
_Y_081_KCT = {
    "Pr 8:34": ("אַֽשְֽׁרֵי־אָדָם֮", _Y_GWMHM),  # page 92 (צב)
    "Ps 1:1": ("אַֽשְֽׁרֵי־הָאִ֗ישׁ", "same as above"),  # page 1 (א)
    "Ps 32:2": ("אַֽשְֽׁרֵי־אָדָ֗ם", "same as above"),  # page 15 (טו)
    "Ps 40:5": ("אַֽשְֽׁרֵי־הַגֶּ֗בֶר", "same as above"),  # page 21 (כא)
    "Ps 98:9": ("לִֽפְֽנֵי־יְהֹוָ֗ה", "same as above"),  # page 53 (נג)
    "Ps 64:7": ("יַֽחְפְּֽשׂוּ־עוֹלֹ֗ת", "same as above"),  # page 33 (לג)
    "Ps 89:25": (author.hbo_es("וֶֽאֱמוּנָתִ֣י"), _Y_KCT_8925),  # page 49 (מט)
    "Ps 98:3": (author.hbo_es("וֶֽאֱמֽוּנָתוֹ֮"), _Y_KCT_9803),  # page 53 (נג)
}
_X_081_TABLE = _my_join(_X_060_CTABLE, _Y_081_KCT)
_X_090_CPARA = "Here is $CTR (shown with $MAM for comparison):"
_Y_091_CTR = {
    "Pr 8:34": (
        "אַ֥שְֽׁרֵי אָדָם֘",
        ru.eq("$MAM (modulo $MAM’s special $maqaf$thinsp)"),
    ),
    "Ps 1:1": (
        "אַֽשְֽׁרֵ֥י הָאִ֗ישׁ",
        "$gaya on $shin awkward: bad injection from $KCT?",
    ),
    "Ps 32:2": ("אַֽשְֽׁרֵ֥י אָדָ֗ם", "same as above"),
    "Ps 40:5": ("אַֽשְֽׁרֵ֥י הַגֶּ֗בֶר", "same as above"),
    "Ps 98:9": ("לִֽפְ֥נֵי־יְהֹוָ֗ה", "error: $merkha on $shewa"),
    "Ps 64:7": ("יַֽחְפְּשׂ֥וּ עוֹלֹ֗ת", "no $gaya with $shewa"),
    "Ps 89:25": (
        author.hbo_es("וֶֽאֱמֽוּנָתִ֣י"),
        [ru.aeq("$KCT"), " ($KCT has no $gaya on $mem)"],
    ),
    "Ps 98:3": (author.hbo_es("וֶֽאֱמֽוּנָתוֹ֮"), ru.eq("$KCT")),
}
_X_091_TABLE = _my_join(_X_060_CTABLE, _Y_091_CTR)
_X_100_CPARA = [
    [
        "(Above I have “normalized” $CTR’s accent on Ps 98:3 ואמונתו to be Unicode $ZINOR."
    ],
    [
        " The rather strange uses and abuses of Unicode in $CTR are covered in the parent"
    ],
    [" ", rocc_0.anchor(), ".)"],
]
_CD_LRL = ("ltr", "rtl", "ltr")
_CD_RRL = ("rtl", "rtl", "ltr")
_CBODY = [
    author.heading_level_1(_H1_CONTENTS),
    author.para(_X_050_CPARA),
    author.para(_X_051_CPARA),
    author.std_table(_X_060_CTABLE, coldirs=_CD_LRL),
    author.para(_X_070_CPARA),
    author.unordered_list(_X_071_LIST_ITEMS),
    author.para(_X_072_CPARA),
    author.para(_X_073_CPARA),
    author.para(_X_074_CPARA),
    author.para(_X_075_CPARA),
    author.para(_X_080_CPARA),
    author.std_table(_X_081_TABLE, coldirs=_CD_RRL, arg_to_troh=["$MAM", "$KCT"]),
    author.para(_X_090_CPARA),
    author.std_table(_X_091_TABLE, coldirs=_CD_RRL, arg_to_troh=["$MAM", "$CTR"]),
    author.para(_X_100_CPARA),
]
