from pyauthor_rocc import rocc_util as ru

_CPARA = "Now let’s look at לא in Psalm 32:2 (ignoring $CTR):"
TD_CTR = (ru.gray_abg_yxjb("לֹֽא "), "$gaya with space (!)")
TD_MAM_KCT_WMG = (ru.gray_abg_yxjb("לֹ֤א "), "$mahapakh with space")
TD_JP_SBB = (ru.gray_abg_yxjb("לֹֽא־"), "$gaya with $maqaf")
_TABLE_DATA = {
    "$JP, $SBB": TD_JP_SBB,
    "$MAM, $KCT, $WMG": TD_MAM_KCT_WMG,
}
ARGS = _CPARA, _TABLE_DATA
