from pyauthor_rocc.rocc_util import MAM_SPECIAL_MAQAF
from pyauthor_rocc import rocc_util as ru
from pyauthor import rocc_4_mid_word_ga3ya_with_shewa as mwgws

_CPARA = "Now let’s look at אשרי in Psalm 32:2 (ignoring $CTR):"

TD_CTR = (ru.gray_abg_adm("אַֽשְֽׁרֵ֥י" + " "), "$merkha on $resh, space")
TD_MAM = (ru.gray_abg_adm("אַ֥שְֽׁרֵי־"), "$merkha on $alef, $maqaf")
TD_KCT_SBB = (ru.gray_abg_adm("אַֽשְֽׁרֵי־"), "$gaya on $alef, $maqaf")
TD_JP = (ru.gray_abg_adm("אַֽשְׁרֵ֥י" + " "), "$merkha on $resh, space")
TD_WMG = (ru.gray_abg_adm("אַשְׁרֵ֥י" + " "), ru.aeq("$JP"))

_TABLE_DATA = {
    "$JP": TD_JP,
    "$WMG": TD_WMG,
    "$MAM": TD_MAM,
    "$KCT, $SBB": TD_KCT_SBB,
}
# _X20_CPARA = author.note_on_arabizi_3()

_X30_CPARA = [
    ["In $MAM, the $maqaf after אשרי is marked up as a special kind of $maqaf."],
    [" ", MAM_SPECIAL_MAQAF],
    [" That section of the documentation even makes reference to"],
    [" Psalm 32:2 אשרי־אדם in particular."],
]
_X40_CPARA = [
    ["The combination of $gaya with $shewa"],
    [" ($MAM, $KCT, $SBB)"],
    [" rarely appears like this, in the middle of a word."],
    [" See my ", mwgws.anchor()],
]
ARGS = _CPARA, _TABLE_DATA, [_X30_CPARA, _X40_CPARA]
