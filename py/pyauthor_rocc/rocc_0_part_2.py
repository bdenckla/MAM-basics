from py_misc import my_html
from pyauthor_util import author
from pyauthor import rocc_4_mid_word_ga3ya_with_shewa as mwgws
from pyauthor import rocc_3_where_other_sources_stand as stand
from pyauthor import rocc_1_on_the_provenance_of_ctr as prov
from pyauthor_rocc import rocc_util as ru
from pyauthor_rocc import rocc_212_pj3 as pj3
from pyauthor_rocc import rocc_213_ajry as ajry
from pyauthor_rocc import rocc_213_ajry as ajry
from pyauthor_rocc import rocc_214_la as la
from pyauthor_rocc import rocc_216_yvmm as yvmm
from pyauthor_rocc import rocc_217_vlylh as vlylh
from pyauthor_rocc import rocc_220_v3vny as v3vny
from pyauthor_rocc import rocc_221_njaf as njaf
from pyauthor_rocc import rocc_223_fhyv as fhyv
from pyauthor_rocc import rocc_227_qrb_qrvb as qrb_qrvb


_Y_WORD_WHERE = "word where $CTR differs from both $MAM and $JP:"
_X303_CPARA = [
    ["First let’s look at the words in which $CTR differs"],
    [" not only from $MAM but also from $JP"],
    [" (", ru.edition_jp_full(), ")."],
    [" This is a reasonable starting point since"],
    [" $JP is, among the sources I have looked at,"],
    [" the one that most closely resembles $CTR."],
    [" For each word, I will also show what is present in $KCT"],
    [" (", ru.edition_kct_full(), ")"],
    [" for reasons that will be explained below."],
    [" Here is the first ", _Y_WORD_WHERE],
]
_X304_TABLE_DATA_PJ3 = {
    "$CTR, $KCT": (pj3.TD_CTR_KCT_WMG[0], "$revia on $pe"),
    "$JP": (pj3.TD_JP_SBB[0], "$revia on $shin"),
}
_X305_CPARA = [
    ["In both $CTR and in $JP, the accent is $revmug."],
    [" But $CTR and $JP differ in their placement of $revia."],
    [" Perhaps $CTR is a transcription of $JP"],
    [" later altered to conform more closely to a Koren Tanakh in some places."],
    [" I base this speculation on documentation found on the"],
    [" Soncino Classics Collection $CD_ROM."],
    [" This $CD_ROM may be related to $CTR."],
    [" ", author.paren(["See my ", prov.anchor()]), "."],
    [" Here is the relevant quote from the $CD_ROM documentation:"],
]
_X306_CONT_BLOCKQUOTE = """The text of the Tanach is based on
the 1895 Warsaw edition of the Mikraot
Gedolot which has been carefully compared with other versions such as the
Jerusalem Koren Tanach. In some instances (involving mainly Ken
[sic; Kere intented?]
and Ketiv
and Chaser and Malay) the text has been modified to conform to the Koren
edition. However, the responsibility for such decisions is solely that of
the CD ROM publishers.""".replace("\n", " ")
_Y_NOW_LETS_LOOK = f"Now let’s look at the next {_Y_WORD_WHERE}"
_X310_CPARA = [
    ["My speculation is consistent with the contents of $KCT here"],
    [" since $KCT matches $CTR here, having $revmug with $revia on $pe."],
    [" ", _Y_NOW_LETS_LOOK],
]
_X311_TABLE_DATA_AJRY = {
    "$CTR": (ajry.TD_CTR[0], "$gaya on $shin"),
    "$JP": (ajry.TD_JP[0], "no $gaya on $shin"),
    "$KCT": (ajry.TD_KCT_SBB[0], "see discussion below"),
}
# _X312A_CPARA = author.note_on_arabizi_3()
_X312B_CPARA = [
    ["Here, $KCT is quite different from $CTR:"],
    [" there is only a $tsere on $resh (no $merkha)"],
    [" and there is a $maqaf joining אשרי to אדם"],
    [" (rather than a space separating them)."],
    [" But the fact that both $CTR and $KCT have a $gaya on $shin may be significant."],
    [" I speculate that the $gaya on $shin in $CTR was added to make a transcription"],
    [" of $JP conform more closely to $KCT."],
]
# _X312C_CPARA = [
#     ["It is usually considered no big deal"],
#     [" when one edition has $gaya and another has neither $gaya nor an accent."],
#     [" However, in this case, the presence of $gaya in $CTR is worth noting"],
#     [" because it, too, is consistent with my speculation about the origin"],
#     [" of $CTR."],
# ]
_X312_CPARAS = [_X312B_CPARA]
_X320_CPARA = [
    ["I think this $gaya does not “go with” the rest of $CTR’s pointing of this word."],
    [" I think this because this $gaya is a mid-word $gaya with $shewa,"],
    [" and that construction is used in quite limited contexts"],
    [" that are not analogous to $CTR’s use here."],
    [" See my ", mwgws.anchor()],
    [" As we shall see, this is one of three cases where $CTR seems to have made"],
    [" an infelicitous mix of the pointing of $JP and $KCT."],
    [" See לא and יומם below."],
    [" ", _Y_NOW_LETS_LOOK],
]
# XXX TODO does this shewa on shin even make sense if merkha is on resh?
_X321_TABLE_DATA_LA = {
    "$CTR": la.TD_CTR,
    "$JP": la.TD_JP_SBB,
    "$KCT": la.TD_MAM_KCT_WMG,
}
_X330_CPARA = [
    ["This is an error in $CTR: לא needs an accent and/or a $maqaf."],
    [" It is widely agreed to be illegal to have only a $gaya on an independent word."],
    [" Here $CTR’s error may just be a careless error. But, it may be an"],
    [" error caused by another effort"],
    [" to make $CTR conform more closely to $KCT."],
    [" Here both $KCT and $CTR have a space separating לא from יחשב,"],
    [" although $KCT has a $mahapakh"],
    [" rather than a $gaya on לא."],
    [" ", _Y_NOW_LETS_LOOK],
]
_X331_TABLE_DATA_YVMM = {
    "$CTR": yvmm.TD_CTR,
    "$JP": yvmm.TD_JP,
    "$KCT": yvmm.TD_MAM_KCT_ETC,
}
_X340_CPARA = [
    ["This is an error in $CTR."],
    [" It is widely agreed to be illegal to combine $tsinnorit and $munax."],
    [" (A $tsinnorit always and only precedes either a $merkha or a $mahapakh.)"],
    [" This could be the result of another effort"],
    [" to make $CTR conform more closely to $KCT."],
    [" ", _Y_NOW_LETS_LOOK],
]
_X341_TABLE_DATA_VLYLH = {
    "$CTR": vlylh.TD_CTR,
    "$JP image": vlylh.TD_JP,
    "$JP charitable": (
        vlylh.TD_JP_CHARITABLE[0],
        "floating $azla read as if on $lamed",
    ),
    "$KCT": vlylh.TD_MAM_KCT_ETC,
}
_X316A_CPARA = [
    ["(By “$JP charitable,” I mean the (charitable) interpretation of $JP,"],
    [" where the floating $azla is assigned to the $lamed.)"],
]
_X316B_CPARA = [
    ["The location of $azla in $CTR (on $vav) is likely an error."],
    [" This error may stem from mistranscribing the floating $azla in $JP."],
    [" It makes more sense to assign the floating $azla to $lamed than to $vav."],
    [" The only analogy I find in all of Tanakh"],
    [" is $munax on $vav in Exodus 36:38 ", author.hbo_es("וְאֶת־וָ֣וֵיהֶ֔ם"), "$thinsp."],
    [" The analogy is distant because $munax is not the primary accent"],
    [" on that word."],
]
_X342_CPARAS = vlylh.CPARA_WE_ASSUME, _X316A_CPARA, _X316B_CPARA
_Y_THE_CHAR = "(the charitable interpretation of$hairsp)"
_X350_CPARA = [
    ["Here with ולילה, for the first time,"],
    [" conformance with $KCT cannot explain why $CTR differs from"],
    [" ", _Y_THE_CHAR, " $JP."],
    [" ", _Y_NOW_LETS_LOOK],
]
_Y_ABOVE_TSERE = "“above $tsere” read as $xolam_xaser_xx on $vav"
_Y_PLUS_EXPRESSION = author.hbo("וֺ֘ = וֺ+ו֘")
_X351_TABLE_DATA_V3VNY = {
    "$CTR": v3vny.TD_CTR,
    "$JP image": v3vny.TD_JP,
    "$JP charitable": (v3vny.TD_JP_CHARITABLE[0], _Y_ABOVE_TSERE),
    "$KCT": (v3vny.TD_SBB_KCT[0], _Y_PLUS_EXPRESSION),
}
_X319A_CPARA = [
    ["(By “$JP charitable,” I mean the (charitable) interpretation of $JP,"],
    [" where the “above $tsere” on $nun is interpreted as"],
    [" a $xolam_xaser on $vav plus an ignored dot.)"],
]
_X319B_CPARA = [
    "The location of $tsinnorit in $CTR (on $ayin) is an error.",
    *v3vny.NO_ACCENT,
]
_X352_CPARAS = _X319A_CPARA, _X319B_CPARA, v3vny.IN_JP_THERE_ARE_TWO
_X360_CPARA = [
    ["Here, as with ולילה,"],
    [" conformance with $KCT cannot explain why $CTR differs from"],
    [" ", _Y_THE_CHAR, " $JP."],
    [" Though one could say that the placement of $tsinnorit on $ayin in $CTR"],
    [" compromises between $vav #1 ($JP) and $vav #2 in ($KCT),"],
    [" I doubt that this is why $tsinnorit appears on $ayin in $CTR."],
    [" ", _Y_NOW_LETS_LOOK],
]
_X361_TABLE_DATA_NJAF = {
    "$CTR": njaf.TD_CTR,
    "$JP, $KCT": njaf.TD_MAM_KCT_JP_ETC,
}
_X370_CPARA = [
    ["Here, as with ולילה and ועוני,"],
    [" conformance with $KCT cannot explain why $CTR differs from $JP."],
    [" ", _Y_NOW_LETS_LOOK],
]
_X371_TABLE_DATA_FHYV = {
    "$CTR": (fhyv.TD_CTR[0], "$azla on $yod"),
    "$JP": fhyv.TD_JP,
    "$KCT": (fhyv.TD_KCT_ETC[0], "$mahapakh on $yod"),
}
_X380_CPARA = [
    ["Here $JP has a pretty wild pointing of this word."],
    [" Here $CTR may be retaining the $azla of $JP while"],
    [" removing the wild features of the $JP pointing, using"],
    [" $KCT as a guide, albeit rejecting the $gaya found in $KCT."],
    [" ", _Y_NOW_LETS_LOOK],
]
_X381_TABLE_DATA_QRB_QRVB = {
    "$CTR": qrb_qrvb.TD_CTR,
    "$JP, $KCT": qrb_qrvb.TD_MAM_KCT_ETC,
}
_Y_VLYLH = my_html.bdi("ולילה")
_Y_V3VNY = my_html.bdi("ועוני")
_Y_NJAF = my_html.bdi("נשאת")
_X382_CPARA = [
    ["Here, as with ", _Y_VLYLH, ", ", _Y_V3VNY, ", and ", _Y_NJAF, ","],
    [" conformance with $KCT cannot explain why $CTR differs from $JP."],
]
#
_X390 = [
    ["For the rest of my review of the differences between $CTR and $MAM,"],
    [" see my ", stand.anchor()],
    [" That document goes beyond this one in the following ways:"],
]
BODY_ELEMENTS = [
    author.para_table(_X303_CPARA, _X304_TABLE_DATA_PJ3, [_X305_CPARA]),
    author.blockquote(_X306_CONT_BLOCKQUOTE),
    author.para_table(_X310_CPARA, _X311_TABLE_DATA_AJRY, _X312_CPARAS),
    author.para_table(_X320_CPARA, _X321_TABLE_DATA_LA),
    author.para_table(_X330_CPARA, _X331_TABLE_DATA_YVMM),
    author.para_table(_X340_CPARA, _X341_TABLE_DATA_VLYLH, _X342_CPARAS),
    author.para_table(_X350_CPARA, _X351_TABLE_DATA_V3VNY, _X352_CPARAS),
    author.para_table(_X360_CPARA, _X361_TABLE_DATA_NJAF),
    author.para_table(_X370_CPARA, _X371_TABLE_DATA_FHYV, [fhyv.CPARA_WE_ASSUME]),
    author.para_table(_X380_CPARA, _X381_TABLE_DATA_QRB_QRVB, [_X382_CPARA]),
    #
    author.para_ul(_X390, stand.X_02_LIST_ITEMS),
]
