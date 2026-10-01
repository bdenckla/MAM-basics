import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_MSS_C_S_S1 = sub.three_comma_and(sub.ms_cairo(), sub.ms_s_507(), sub.ms_s1_1053())
_MSS_L_S1 = sub.ms_lenin(), " and ", sub.ms_s1_1053()
SEC = [
    sub.para(
        [
            "$Gaya is generally written to the left of (“after”)"
            " a vowel sign marked under the same letter."
            " In some manuscripts, such as ",
            sub.ms_a_and_l(" and "),
            ", this convention is carefully maintained, with very few exceptions",
            sub.emdash(),
            "and those usually due to correction,"
            " or to lack of space in the regular position."
            " In other manuscripts, such as ",
            *_MSS_C_S_S1,
            ", $gaya is often written to the right of the vowel sign,"
            " without any particular reason."
            " $Gaya is also generally written to the left of the"
            " $simshewa sign,"
            " but there are manuscripts in which it is often written to the right."
            " The same is generally true of $x_shewa signs, but in some manuscripts, such as ",
            *_MSS_L_S1,
            ", $gaya may be written between the two parts of the $xatef sign; ",
            hlp.hbo("אאֲ‍ֽא"),
            sub.thspp(),
            " This does not occur in ",
            sub.ms_a_and_c(" and "),
            ".",
        ]
    )
]
