import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_TABLE_1 = hlp.table_std(
    [
        [["a non-guttural other than ", sub.yod()], [sub.x_patax(), " is used"]],
        [["a guttural pointed with ", sub.patax()], [sub.x_patax(), " is used"]],
        [["a guttural pointed with ", sub.qamets()], [sub.x_qamets(), " is used"]],
    ],
    arg_to_troh=["Before ...", ["Type of ", sub.xatef()]],
)
SEC = [
    sub.para(["This $gaya is marked in various situations:"]),
    sub.unordered_list(
        [
            "before a letter which has lost its historical doubling,",
            "before a sibilant letter,",
            "before a group of similar-sounding letters,",
            "etc.",
        ]
    ),
    sub.para(
        [
            "In some cases this $gaya is used even though a",
            " $x_shewa follows it rather than a $simshewa",
            " ",
            hlp.rtn_p(391),
            ". In such cases this $gaya resolves no ambiguity,"
            " because there is no ambiguity to be resolved."
            " But this use of $xatef is not done consistently either with words of"
            " the same structure, or with the same words in different manuscripts."
            " Some manuscripts ",
            hlp.paren(["notably ", sub.ms_aleppo()]),
            " mark the $xatef often. Others mark it rarely. The quality of this $xatef",
            " is determined by the Tiberian rules for the pronunciation of $vocshewa ",
            hlp.rtn_p2(336, 387),
            ":",
        ]
    ),
    _TABLE_1,
    sub.para_paren(
        [
            "Such a $xatef is unlikely to occur"
            " in cases not covered by the table above."
            " I.e. it is unlikely to occur before"
            " a guttural pointed with other vowels, or before ",
            sub.yod(),
            ".",
        ]
    ),
]
