from pyauthor_util import author


_CPARA = "Now let’s look at יומם in Psalm 32:4 (ignoring $CTR):"
TD_CTR = (author.hbo_es("י֘וֹמָ֣ם"), "$munax with $tsinnorit (!)")
TD_MAM_KCT_ETC = (author.hbo_es("יוֹמָ֣ם"), "$munax")
TD_JP = (author.hbo_es("י֘וֹמָ֤ם"), "$mahapakh with $tsinnorit")
_TABLE_DATA = {
    "$JP": TD_JP,
    "$MAM, $KCT, $WMG, $SBB": TD_MAM_KCT_ETC,
}
ARGS = _CPARA, _TABLE_DATA
