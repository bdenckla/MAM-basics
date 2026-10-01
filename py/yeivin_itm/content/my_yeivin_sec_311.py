import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_CONT_PARA_1 = [
    # Below, ITM has "introduced" not "introducing"
    ["Some information on $gaya"],
    [" is included in the rules on the accents given in the"],
    [" ", sub.diqduqe_dotan_sec_str("sections 14, 15, 20, and elsewhere"), "."],
    [" The statements on $gaya"],
    [" in the masoretic literature and"],
    [" the works of the early grammarians are few and unsystematic."],
    [" The most detailed treatment of the rules for $gaya"],
    [" is that given by ", sub.yequtiel_hn(), " (published in Gumpertz, 1958)."],
    [" It was ", sub.yequtiel(), " who set up different categories of the use of"],
    [" $gaya, introducing the terms"],
    [" “light $gaya” ($gaya_os)"],
    [" and"],
    [" “heavy $gaya” ($gaya_cs)."],
]
_CONT_PARA_4 = [
    ["A few surveys of the system of marking $gaya in early manuscripts"],
    [" have been published. The system used in ", sub.ms_cairo()],
    [" is briefly described in Hartom, 1952. The use of $gaya"],
    [" in several manuscripts is briefly"],
    [" described in Greenspan, 1961. A detailed description of the"],
    [" use of $gaya in ", sub.ms_aleppo()],
    [" is given in Yeivin, 1968,"],
    [" p. 89–194 (on the 21 books) and p. 241–277 (on the three books)."],
]
_EMDASH_PHRASE = [
    sub.emdash(),
    "though less systematic than those of ",
    sub.yequtiel_hn(),
    sub.emdash(),
]
_CONT_PARA_2 = [
    ["The survey of rules for $gaya"],
    [" in the ", hlp.rom("Miqneh Abram"), " of Abram di Balmes,"],
    [" and in Heidenheim’s ", hlp.rom("Sefer Mispeṭe ha-Ṭeʿamim")],
    [" (45a–60b) was based on those of ", sub.yequtiel_hn(), "."],
    [" Eliahu ha-Levi also gives detailed rules on the use of"],
    [" $gaya", *_EMDASH_PHRASE, "in"],
    [" ", sub.tuv_taam(), " chapter 7."],
    [" The same is true of Shelomo Yedidyah Norzi’s"],
    [" ", hlp.rom("Maʾamar ha-Maʾarik"), "."],
]

_CONT_PARA_3 = [
    ["The most comprehensive survey of the rules for $gaya"],
    [" is that in Baer 1869."],
    [" These rules were derived from the study of $gaya"],
    [" in late manuscripts, and in some cases Baer imposes a system"],
    [" where none is evident in his sources."],
    [" Nevertheless, Baer’s rules were adopted in scholarly grammars,"],
    [" such as Bergsträsser 1918 (vol. 1, num. 11)."],
]

SEC = [
    sub.para(_CONT_PARA_1),
    sub.para(_CONT_PARA_2),
    sub.para(_CONT_PARA_3),
    sub.para(_CONT_PARA_4),
]
