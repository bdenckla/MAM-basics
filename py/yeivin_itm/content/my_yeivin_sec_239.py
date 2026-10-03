import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_MSS_L_C = sub.ms_lenin(), " and ", sub.ms_cairo()
_NOT_REPEATED_EXAMPLES = [
    [hlp.hboloc("מִזְבֵּחַ֙", "@Is 19:19"), ","],
    [" ", hlp.hboloc("הֱטִיבֹתָ֙", "@2K 10:30"), ","],
    [" ", hlp.hboloc("יְרוּשָׁלַ͏ִם֙", "@Is 52:1"), ", and"],
    [" ", hlp.hboloc("וְשַׁתִּהָ֙", "@Ho 2:5")],
]
_QIMXI_BLOCKQUOTE_CONT = [
    ["When the two letters"],
    [" ", hlp.paren(["on which the $pashta signs would be marked"])],
    [" are separated only by one vowel, with no vowel letter,"],
    [" there is a difference of opinion."],
    [" Some read two $pashta signs,"],
    [" others only one, as in ", hlp.hboloc("הָרִ֤ימִי בַכֹּחַ֙", "@Is 40:9"), "."],
]
_CONT_PAREN = [
    ["i.e. every word with penultimate stress, including words with"],
    [" ", sub.patax(), " ", hlp.dquotes("furtive")],
]
_EMDASH_PHRASE = [
    sub.emdash(),
    "for instance ",
    *_MSS_L_C,
    sub.emdash(),
]
_CONT_PARA_1 = [
    ["$Pashta is the only accent sign in standard Tiberian"],
    [" manuscripts which is regularly repeated on a penultimate stress syllable."],
    [" In standard printed editions, the $pashta sign"],
    [" is repeated on every word in which the stressed vowel is not the last"],
    [" ", hlp.paren(_CONT_PAREN), "."],
    [" Most early manuscripts", _EMDASH_PHRASE, "follow the same system,"],
    [" but some manuscripts show a different convention."],
]
_CONT_PARA_2 = [
    ["In ", sub.ms_a_and_s(), ","],
    [" and some other manuscripts, the sign is only repeated"],
    [" where at least one letter stands between the two letters to be"],
    [" marked with the signs, as"],
    [" ", hlp.hboloc("הִשְׁמִ֙יעַ֙", "@Is 62:11"), " and"],
    [" ", hlp.hboloc("לְפָנֶ֙יךָ֙", "@Is 58:8"), "."],
    [" Where this is not the case, the $pashta sign is not repeated,"],
    [" as ", *_NOT_REPEATED_EXAMPLES, "."],
    [" This system of marking $pashta"],
    [" is mentioned in some treatises, such as Qimḥi’s"],
    [" ", sub.cet_sofer(), ", p. 31b:", sub.blockquote(_QIMXI_BLOCKQUOTE_CONT)],
]
_CONT_PARA_3 = [
    ["In ", sub.ms_b_and_s1(), ","],
    [" and some other manuscripts, $pashta is not repeated"],
    [" not only where two letters on which it would be marked are"],
    [" not separated by a third, but also in other situations as well, as"],
    [" ", hlp.hbo_loc_ms("לַחֹדֶשׁ֙", "@Ex 12:18", sub.ms_b_4445()), " and"],
    [" ", hlp.hbo_loc_ms("מִשְׁפַּחַת֙", "@Nu 3:33", sub.ms_b_4445()), "."],
    [" This usage is not consistent, however, as $pashta"],
    [" sometimes is repeated on such words."],
]
_CONT_PARA_4 = [
    ["In ", sub.ms_lenin_02(), ", $pashta is never repeated."],
    [" Thus ", hlp.hboloc("תָּבוֹאתָה֙", "@Dt 33:16")],
    [" and ", hlp.hboloc("זְבָחֵימוֹ֙", "@Dt 32:38"), "."],
]
_ISE_JER_31_19 = "@Jer 31:19"  # 31:18 in MAM
_CONT_PARA_5 = [
    ["In some cases, where the position of the word stress might be in doubt,"],
    [" the $pashta sign is repeated on a stressed final syllable, as"],
    [" ", hlp.hbo_loc_ms("שׁוּבִ֙י֙", _ISE_JER_31_19, sub.ms_c_and_s1()), ","],
    [" ", hlp.hbo_loc_ms("שָׁב֙וּ֙", "@2C 25:12", sub.ms_s1_1053()), ","],
    [" and ", hlp.hbo_loc_ms("וְכוֹבַ֙ע֙", "@Ez 27:10", sub.ms_s1_1053()), "."],
]
_CONT_PARA_6 = [
    ["In many manuscripts pointed in the expanded Tiberian system, $pashta"],
    [" is repeated on every word in which the last letter does not represent"],
    [" the first consonant of the stress syllable, as"],
    [" ", hlp.hboloc("בָּֽרְבִיעִ֙י֙", "@Ez 1:1"), ","],
    [" ", hlp.hboloc("כְּכַ֙ף֙", "@Ez 1:7"), ", and"],
    [" ", hlp.hboloc("גָּד֙וֹל֙", "@Ez 1:4"), "."],
]


SEC = [
    sub.para(_CONT_PARA_1),
    sub.para(_CONT_PARA_2),
    sub.para(_CONT_PARA_3),
    sub.para(_CONT_PARA_4),
    sub.para(_CONT_PARA_5),
    sub.para(_CONT_PARA_6),
]
