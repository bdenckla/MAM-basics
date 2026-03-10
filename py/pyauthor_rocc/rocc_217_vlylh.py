from py_misc import my_html
from pyauthor_rocc import rocc_0_review_of_ctr_header as rocc_0
from pyauthor_util import author


# author.pasoleg_qm("וָ֨לַיְלָה׀"),
# author.pasoleg_qm("וָלַ֨יְלָה׀"),

_CPARA = "Now let’s look at ולילה in Psalm 32:4 (ignoring $CTR):"
_IMG_217_PATH = "img/rocc Judaica Press Psalm 32v4 ולילה floating azla.jpg"
_IMG_217 = my_html.img({"src": _IMG_217_PATH, "class": "width5em"})
TD_CTR = ("וָ֨לַיְלָה׀", "$azla on $vav (!)")
TD_MAM_KCT_ETC = ("וָלַיְלָה֮", "$tsinnor")
TD_JP = (_IMG_217, "$azla floats between $vav and $lamed")
TD_JP_CHARITABLE = ("וָלַ֨יְלָה׀", "$azla $legarmeh")
_TABLE_DATA = {
    "$JP charitable": TD_JP_CHARITABLE,
    "$MAM, $KCT, $WMG, $SBB": TD_MAM_KCT_ETC,
}
CPARA_WE_ASSUME = [
    ["(I assume that the vertical bar after ולילה"],
    [" is a $legarmeh rather than a $paseq."],
    [" As such, I include it as part of the word.)"],
]
_FOR_AN_EXP = "For an explanation of what is meant by “$JP charitable,” see the parent "
_SEE_OTHER = author.paren([_FOR_AN_EXP, rocc_0.anchor()])
ARGS = _CPARA, _TABLE_DATA, [CPARA_WE_ASSUME, _SEE_OTHER]
