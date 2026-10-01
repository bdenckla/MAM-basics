import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_TABLE_1_DATA = [
    ("שְׂפָתֶ֣יהָ נָּע֔וֹת", "@1S 1:13", ""),
    ("אַחֲרֶ֣יךָ נָּר֑וּצָה", "@Song 1:4", ""),
    ("עָבִ֣יתָ כָּשִׂ֑יתָ", "@Dt 32:15", ""),
    ("אָבִ֣יךָ קָּנֶ֔ךָ", "@Dt 32:6", ""),
    (
        "הִרְגִּ֣יעָה לִּילִ֔ית",
        "@Is 34:14",
        sub.dol("$dexiq used for phonetic reasons"),
    ),
]
_TABLE_2_DATA = [
    ("גָּאַ֣לְתָּ בִּזְר֣וֹעַ", "@Ps 77:16"),
    ("אֵלֶ֣יךָ תִּלְאֶ֑ה", "@Job 4:2"),
]
_TABLE_3_DATA = [("וַיְשִׂימֶ֤הָ תֵּל־עוֹלָם֙", "@Jos 8:28")]
SEC = [
    sub.para(
        [
            "If a word with penultimate stress"
            " has a conjunctive accent and ends with an open syllable,"
            " $dexiq is sometimes used under circumstances other than those listed above."
            " These fall into several classes, but there are not many examples in any of them."
            " The classes are:",
        ]
    ),
    sub.ordered_list_with_lcromnum(
        [
            sub.cmn_407_lcromnum_i(),
            sub.cmn_407_lcromnum_ii(),
            sub.cmn_407_lcromnum_iii(),
        ]
    ),
    sub.para_with_romnum_and_initial_uah(
        "i",
        sub.cmn_407_lcromnum_i(),
        [
            ["In a few cases, where α ends with ", sub.qamets(), ","],
            [" $dexiq is used in the first letter of β"],
            [" even where β’s second syllable is stressed rather than its first."],
            [" In most cases β’s first syllable is open. E.g.:"],
        ],
    ),
    hlp.table_std_alpha_beta_3col_std(_TABLE_1_DATA, arg_to_troh=None),
    sub.para(["In a few cases β’s first syllable is closed. E.g.:"]),
    hlp.table_std_alpha_beta_2col_std(_TABLE_2_DATA, arg_to_troh=None),
    sub.para(
        [
            "The $dexiq may even be used when the stress is as late"
            " as the third syllable, as ",
        ]
    ),
    hlp.table_std_alpha_beta_2col_std(_TABLE_3_DATA, arg_to_troh=None),
]
