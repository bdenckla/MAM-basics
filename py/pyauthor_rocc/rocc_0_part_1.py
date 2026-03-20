from pyauthor import rocc_1_on_the_provenance_of_ctr as prov
from pyauthor import rocc_2_pre_vowel_accents_in_ctr as pre_vowel
from pyauthor_rocc import rocc_util as ru
from pyauthor_util import author
from pyauthor_rocc import rocc_121_schematic as c121

_X107_CONT_PARA = [
    ["The $anc_Chabad_website has an edition of the Hebrew Bible"],
    [" called $anc_Chabad_CTR ($CTR)."],
    [" ", author.paren(["See my ", prov.anchor()])],
]
_X108_CONT_PARA = """This $CTR is certainly the weirdest Hebrew Bible on the web,
and possibly the worst.
Whether it is the worst depends somewhat on (1) taste
and (2) what purpose $CTR would be put to.""".replace("\n", " ")
_X109_CONT_PARA = """For example, this $CTR,
though full of what most people would consider errors,
might still be correct in some cases where other editions are wrong.
In other words, its very weirdness, though usually a negative,
might in some cases be a positive.""".replace("\n", " ")
_X110_CONT_PARA = """I will not comprehensively review $CTR.
Instead, I will review its $anc_Chabad_Psalm_32.
If its Psalm 32 is representative,
my review should give a good idea of $CTR as a whole.
At a minimum, my review is likely to give a good idea of
$CTR’s poetic books, since some of $CTR’s issues are specific
to the poetic accents.""".replace("\n", " ")
_X111_CONT_PARA = """First, I will discuss
the ways in which $CTR’s Psalm 32 uses Unicode in
ways that differ from other web editions.
Then I will discuss the more substantive
ways in which $CTR’s Psalm 32
differs from various other editions of Psalm 32, both on the web and on paper.""".replace(
    "\n", " "
)
_X112_CONT_PARA = """In its Psalm 32 (and perhaps in its entire Tanakh),
$CTR is restricted to the code points in Unicode 2.0.
There are three code points that were introduced later
that are used in some editions of Psalm 32:""".replace("\n", " ")
_X112_LIST_ITEMS_QQ_AH_XXFV = ["$QQ", "$AH", "$HHFV"]
_X113_CONT_PARA = """In the first two of the three cases,
the fact that $CTR does not use the newer code point
causes no problems.
Indeed many editions, even quite recent ones,
are like $CTR in that they do not make the following distinctions:""".replace("\n", " ")
_X113_LIST_ITEMS_Q_VS_QQ_ETC = ["$qamats vs. $qq", "$yby vs. $ah"]
_X114_CONT_PARA = """Both distinctions were introduced in Unicode 4.1,
although $AH was introduced in a way
that makes its adoption difficult, even to this day.
See my $anc_proposal_alt_yby to the Unicode $SEWG.""".replace("\n", " ")
_X115_CONT_PARA = """The third post-2.0 code point that $CTR might have used
is $HHFV. In this case, the fact that $CTR does not use it
causes a problem.
It causes a problem because $CTR does not merely decline to make the distinction
that this code point enables.
Rather, $CTR uses a nonstandard workaround to try to make this distinction.
This workaround may work (accidentally or intentionally) in some fonts,
but not in all fonts.""".replace("\n", " ")
_X116_ZWJ_HOLAM = "‹$ZWJ, $HOLAM›"
_X116_CONT_PARA = [
    f"The workaround is the sequence {_X116_ZWJ_HOLAM}.",
    [" For example,"],
    [" ", ru.to_encode("$xolam_xaser", "on", "$vav", "32:5", "עוֺן", "עֲוֺ֖ן")],
    [" ", ru.instead("$HOLAM_HASER_FOR_VAV", _X116_ZWJ_HOLAM)],
    [" In some fonts,"],
    [" this may accidentally have something like the desired appearance,"],
    [" since the $ZWJ may “confuse” the font"],
    [" into putting the $HOLAM fully after the $vav."],
    [" But in other fonts, the $HOLAM will still appear directly over the $vav,"],
    [" as it would if there were no $ZWJ."],
]
_X117_CONT_PARA = """The $CTR edition even declines to avail itself of distinctions
that were available in Unicode 2.0. For example, $CTR does not distinguish
$tsinnor from $tsinnorit, using only the $ZARQA code point for both.
To be fair, the names of the $ZARQA and $ZINOR code points were botched,
and so were their annotations, in my opinion.
That could explain why $CTR uses only $ZARQA.
According to the annotation for $ZARQA, it should be used
for both $tsinnor and $tsinnorit if an above-center (rather than above-left)
placement of $tsinnor is desired.
In my opinion, this annotation encourages the use of Unicode to make
a typographic choice that should be left up to fonts, not
“baked in” to the encoding.
(See my $anc_proposal_zarqa to the Unicode $SEWG.)""".replace("\n", " ")
_X118_CONT_PARA = """In addition to $tsinnor and $tsinnorit,
there are three other pairs of accents for which
$CTR declines to avail itself
of distinctions that were available in Unicode 2.0:""".replace("\n", " ")
X118_TIPEHA = "$TIPEHA", "$dexi (!)", "$tarxa$hs_sl_hs$tipeha"
X118_GERESH = "$GERESH", "$germuq (!)", "$geresh"
X118_YETIV = "$YETIV", "$yetiv", "$mahapakh (!)"
_X118_LIST_ITEMS_TIP_GER_YET = [
    ru.codes_both_summary(*X118_TIPEHA),
    ru.codes_both_summary(*X118_GERESH),
    ru.codes_both_summary(*X118_YETIV),
]
_X119_CONT_PARA = [
    ["Each of these three pairs consists of a prepositive accent"],
    [" and an impositive “lookalike.”"],
    [" Sometimes $CTR makes these distinctions in nonstandard ways,"],
    [" and sometimes it makes no distinction at all."],
    [" ", author.paren(["See my ", pre_vowel.anchor()])],
]
_X120_CPARA = """Now let’s move on from encoding (Unicode) differences to more substantive ones.
I will compare $CTR primarily to the edition called Miqra al pi ha-Masorah ($MAM).
Here’s an overview of where $CTR and $MAM differ in Psalm 32,
showing what $MAM has in those places:""".replace(
    "\n", " "
)

BODY_ELEMENTS_1 = [
    author.para(_X107_CONT_PARA),
    author.para(_X108_CONT_PARA),
    author.para(_X109_CONT_PARA),
    author.para(_X110_CONT_PARA),
    author.para(_X111_CONT_PARA),
]
BODY_ELEMENTS_2 = [
    *author.para_ul(_X112_CONT_PARA, _X112_LIST_ITEMS_QQ_AH_XXFV),
    *author.para_ul(_X113_CONT_PARA, _X113_LIST_ITEMS_Q_VS_QQ_ETC),
    author.para(_X114_CONT_PARA),
    author.para(_X115_CONT_PARA),
    author.para(_X116_CONT_PARA),
    author.para(_X117_CONT_PARA),
    *author.para_ul(_X118_CONT_PARA, _X118_LIST_ITEMS_TIP_GER_YET),
    author.para(_X119_CONT_PARA),
]
BODY_ELEMENTS_3 = [
    author.para(_X120_CPARA),
    author.ordered_list(c121.VERSES, {"dir": "rtl"}),
]
