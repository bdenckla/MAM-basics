from pyauthor_util import author
from pyauthor_rocc import rocc_util as ru
from pyauthor import rocc_2_pre_vowel_accents_in_ctr as pre_vowel

_CPARA = """First let’s look at פשע in Psalm 32:1:"""
TD_CTR_KCT_WMG = ru.gray_abg_njvy("פֶּ֝֗שַׁע"), "$revia on $pe & $germuq_gm on $pe"
TD_MAM = ru.gray_abg_njvy("פֶּ֗שַׁע"), "$revia alone (no $germuq_gm)"
TD_JP_SBB = ru.gray_abg_njvy("פֶּ֝שַׁ֗ע"), "$revia on $shin & $germuq_gm on $pe"
_TABLE_DATA = {
    "$CTR, $KCT, $WMG": TD_CTR_KCT_WMG,
    "$JP, $SBB": TD_JP_SBB,
    "$MAM": TD_MAM,
}
_CPARA_WMG = ["($WMG = ", ru.edition_wmg_full(), ")"]
_CPARA_SBB = ["($SBB = ", ru.edition_sbb_full(), ")"]
_CPARA_2 = """All except $MAM agree that the accent is $revmug.
But $MAM is not really an outlier here.
It is simply the only edition we cited that agrees with the $TM tradition here.
By “$TM tradition” I mean, broadly,
the tradition stemming from
the authoritative Tiberian manuscripts
such as those of Aleppo and Leningrad.
(Much further below we will introduce the $JC and $FS editions,
among which $MAM is rarely an outlier, i.e. with which $MAM usually agrees,
at least on the most substantive issues.)""".replace("\n", " ")
#         ["I will use “the $MG tradition” to mean, broadly,"],
#         [" the printed tradition stemming from"],
#         [" the second Venice Miqraot Gedolot (that of 1525)."],
#     [
#         ["I will use “an $MG tradition” to mean"],
#         [" a printed tradition stemming from"],
#         [" one or more Miqraot Gedolot editions, but not the Venice 1525 one."],
#     ],

_CPARA_3 = "In $JP and $SBB, the $revia is on ש. All others have it on פ."
_BAL_AND_XESED = author.hbo("בַּ֜֗ל"), " and ", author.hbo("חֶ֜֗סֶד")
_CPARA_4 = [
    ["Side note: In $CTR, פשע is accented with the $CTR coding for $geresh"],
    [" rather than $germuq."],
    [" (E.g., compare with the coding of ", *_BAL_AND_XESED, " in 32:9 and 32:10.)"],
    [" Nonetheless, I interpret it as $germuq."],
    [" ", author.paren(["See my ", pre_vowel.anchor()])],
]
_POST = _CPARA_WMG, _CPARA_SBB, _CPARA_2, _CPARA_3, _CPARA_4
ARGS = _CPARA, _TABLE_DATA, _POST
