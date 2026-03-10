from pyauthor_rocc import rocc_util as ru
from py_misc import my_html

_CPARA = "Now let’s look at תהיו in Psalm 32:9 (ignoring $JP):"


_JP_COMMENT = ["$azla on $hehe (!)", my_html.line_break(), "$hehe has $xiriq (!)"]
TD_CTR = (ru.gray_abg_al("תִּהְי֨וּ׀"), "$azla $legarmeh")
TD_MAM = (ru.gray_abg_al("תִּהְי֤וּ׀"), "$mahapakh $legarmeh")
TD_KCT_ETC = (ru.gray_abg_al("תִּֽהְי֤וּ׀"), ru.aeq("$MAM"))
TD_JP = (ru.gray_abg_al("תִּהִ֨יוּ׀"), _JP_COMMENT)
_TABLE_DATA = {
    "$CTR": TD_CTR,
    "$MAM": TD_MAM,
    "$KCT, $WMG, $SBB": TD_KCT_ETC,
}
CPARA_WE_ASSUME = [
    ["(I assume that the vertical bar after תהיו"],
    [" is a $legarmeh rather than a $paseq."],
    [" As such, I include it as part of the word.)"],
]
ARGS = _CPARA, _TABLE_DATA, [CPARA_WE_ASSUME]
