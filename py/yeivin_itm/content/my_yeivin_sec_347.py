import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_TABLE_1 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@2S 10:3", "הַֽמְכַבֵּ֨ד")],
        [hlp.lhbo("@Is 40:20", "הַֽמְסֻכָּ֣ן")],
        [hlp.lhbo("@1C 27:21", "הַֽמְנַשֶּׁה֙")],
        [hlp.lhbo("@Job 3:21", "הַֽמְחַכִּ֣ים")],
        [hlp.lhbo("@Nu 20:19", "בַּֽמְסִלָּ֣ה")],
    ]
)
_AXP = sub.ms_a_x_patax("מ")
_TABLE_2_DATA = [
    [hlp.lhbo("@Ez 46:24", "הַֽמְבַשְּׁלִ֔ים"), sub.ms_aleppo()],
    [hlp.lhbo("@2C 32:31", "הַֽמְשַׁלְּחִ֤ים"), sub.ms_lenin(), _AXP],
]
_TABLE_2 = hlp.table_std(_TABLE_2_DATA, coldirs=["rtl", "ltr", "ltr"])
SEC = [
    sub.para(
        [
            "This section and the next few will cover the following classes of"
            " $pgaya on a short vowel:",
        ]
    ),
    sub.ordered_list_with_lcromnum(
        [
            sub.cmn_347_lcromnum_i(),
            sub.cmn_347_lcromnum_ii(),
            sub.cmn_347_lcromnum_iii(),
        ]
    ),
    sub.para_with_romnum_and_initial_uah(
        "i",
        sub.cmn_347_lcromnum_i(),
        sub.dol(
            [
                "$Gaya is often marked in this situation, where that ",
                sub.he(),
                " represents either the definite article or ",
                sub.he(),
                " “interrogative.”",
                " $Gaya",
                " is generally not marked if the ",
                sub.he(),
                " starts the syllable right before the stress syllable, as ",
                hlp.lhbo("@Is 7:13", "הַמְעַ֤ט"),
                ", and similarly it is not marked if the ",
                sub.he(),
                " starts the ",
                hlp.emphasis("third"),
                " syllable before the stress syllable, as ",
                hlp.lhbo("@Gen 30:41", "הַמְקֻשָּׁרוֹת֒"),
                ". However, if the syllable in question is the ",
                hlp.emphasis("second"),
                " before the stress syllable, $gaya generally is marked. E.g.:",
            ]
        ),
    ),
    _TABLE_1,
    sub.para(
        [
            "In all of the examples above that are preserved in ",
            sub.ms_aleppo(),
            " (which is all but the last), ",
            sub.ms_aleppo(),
            " has ",
            sub.x_patax(),
            " on the ",
            sub.mem(),
            ".",
        ]
    ),
    sub.para(
        [
            "Consider the cases where only $simshewa is used on the ",
            sub.mem(),
            ", and the word in question would have"
            " regular structure if we assume that the $shewa"
            " is silent. E.g.:",
        ]
    ),
    _TABLE_2,
    sub.para(
        [
            "In such cases, it is uncertain whether the $gaya is a"
            " $pgaya, in which case the $shewa that follows is vocal, or a"
            " $mgaya, in which case the $shewa that follows is silent. However, where ",
            sub.x_patax(),
            " is used on the ",
            sub.mem(),
            ", as in ",
            sub.ms_aleppo(),
            " in ",
            hlp.hbo("הַֽמֲשַׁלְּחִ֤ים"),
            sub.thspc(),
            " it is certain that the $gaya is phonetic.",
        ]
    ),
    sub.para(
        [
            ["There are a number of exceptions to this rule, in which "],
            ["$gaya is not marked before ", sub.mem(), "."],
            # XXX turn the comment below into a footnote?
            # Are they exceptions just in that gaʿya is not marked,
            # or also in that the shewa is silent?
            [" Examples include ", hlp.lhbo("@Ḥab 3:19", "לַמְנַצֵּ֖חַ")],
            [" and all of its accent-variants. "],
            # XXX turn the comment below into a footnote?
            # Aside: it isn't relevant to the point being made here, but
            # other than this Xab case, all 47 accent-variants I find of this word
            # are in Psalms.
            ["In some other words $gaya"],
            [" is not marked and the ", sub.mem()],
            [" has $dagesh (and so the $shewa is vocal)"],
            [" as ", hlp.lhbo("@Jos 19:13", "הַמְּתֹאָ֖ר")],
            [" and ", hlp.lhbo("@Qoh 11:5", "הַמְּלֵאָ֑ה"), "."],
        ]
    ),
]
