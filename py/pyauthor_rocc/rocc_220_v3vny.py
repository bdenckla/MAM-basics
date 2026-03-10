from py_misc import my_html
from pyauthor_util import author
from pyauthor import tsinnorit_and_oleh_on_ivs as ivs
from pyauthor import tsinnorit_in_psalm_32v5 as tip_32v5
from pyauthor_rocc import rocc_util as ru


_CPARA = [
    "Now let’s look at ועוני in Psalm 32:5 (ignoring $CTR).",
    "This is the word that originally sparked my interest in Psalm 32 in $CTR.",
    [" ", author.paren(["See my ", tip_32v5.anchor()])],
]
_IMG_220_PATH = "img/rocc Judaica Press Psalm 32v5 ועוני.png"
_IMG_220 = my_html.img({"src": _IMG_220_PATH, "class": "width5em"})
TD_CTR = (author.hbo_es("וַֽעֲ֘וֺנִ֤י"), "$ayin (!) holds $tsinnorit")
TD_MAM = (author.hbo_es("וַעֲוֺ֘נִ֤י"), "$vav #2 holds $tsinnorit")
TD_SBB_KCT = (author.hbo_es("וַֽעֲוֺ֘נִ֤י"), ru.aeq("$MAM"))
_TD_JP_COMMENT = [
    "$vav #1 (!) holds $tsinnorit",
    my_html.line_break(),
    "“above $tsere” on $nun (!)",
]
TD_JP = (_IMG_220, _TD_JP_COMMENT)
TD_JP_CHARITABLE = (author.hbo_es("וַ֘עֲוֺנִ֤י"), "$vav #1 holds $tsinnorit")
TD_WMG = (author.hbo_es("וַֽעֲוֺנִ֤֘י"), "$nun (!) holds $tsinnorit")
_TABLE_DATA = {
    "$JP charitable": TD_JP_CHARITABLE,
    "$WMG": TD_WMG,
    "$MAM": TD_MAM,
    "$SBB, $KCT": TD_SBB_KCT,
}
NO_ACCENT = [
    " It is widely agreed that no accent ever appears on a vocal $shewa that is not initial.",
    " (This is true regardless of whether that vocal $shewa",
    " is notated as a simple $shewa or a $xataf_shewa,",
    " i.e. a $xataf vowel).",
    [" ", author.paren(["See my ", ivs.anchor()])],
]
IN_JP_THERE_ARE_TWO = [
    "In $JP, there are two dots above the $nun, almost like an “above $tsere,”",
    " if such a thing existed.",
    " Perhaps the first of these two dots is the $xolam_xaser dot of the $vav,",
    " placed too far to the left.",
    " But the second dot is inexplicable.",
    " A far less serious issue is that the $xataf_patax of the $ayin seems unnecessarily early.",
    " Such early placement is needed when the “tail” of the $ayin is a descender,",
    " but the tail of this $ayin is not a descender: it is tucked to the side.",
]
_CPARA_4 = """(I represent $WMG as if it had special placement for $xolam_xaser on
$vav, but it does not.)""".replace("\n", " ")
ARGS = _CPARA, _TABLE_DATA, [_CPARA_4]
