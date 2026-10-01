import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub


def _naftali(hbo_contents):
    return sub.xxx_hbo_in_parens("bN", hbo_contents)


_FTNT_LIBERTIES = sub.footnote(
    [
        "As in ",
        hlp.rtn(405),
        ", I recast $itm’s running prose here as an explicit case analysis,"
        " labeling the two words α and β, numbering the three cases, and"
        " tagging each example below with the case it illustrates.",
    ]
)
_TABLE_DATA = [
    ("אֵ֣לֶּה לָּ֑ךְ", "@Gen 33:5", "1"),
    ("שָׂ֥דֶה טּ֛וֹב", "@Ez 17:8", "2"),
    ("אִקָּ֥רֶה כֹּֽה׃", "@Nu 23:15", "2"),
    ("תֵּ֥רֶא יַּיִן֮", "@Prov 23:31", "2 (the only example ending in א)"),
    ("עֹ֤שֶׂה פְּרִי֙", "@Gen 1:11", "2"),
    ("וּמִשְׁנֶה־כֶּ֛סֶף", "@Gen 43:15", "3"),
    ("תַּעֲשֶׂה־לְּךָ֣", "@Prov 24:6", "3"),
    ("יִֽהְיֶה־לְּעָ֖ם", "@Gen 48:19", ["3 ", _naftali("לֿ")]),
    ("כֹּֽרֶה־שַּׁ֭חַת", "@Prov 26:27", "3"),
]

_CASE_1 = ["α has penultimate stress normally, i.e. not via accent retraction"]
_CASE_2 = ["α has penultimate stress via accent retraction"]
_CASE_3 = ["α has $maqqef"]
SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para_with_romnum_and_initial_uah(
        "i", sub.cmn_403_lcromnum_i(), ["This is used:"]
    ),
    sub.ordered_list_with_warabnum(
        [["When ", *_CASE_1, "."], ["When ", *_CASE_2, "."], ["When ", *_CASE_3, "."]]
    ),
    hlp.table_std_alpha_beta_3col_std(_TABLE_DATA),
    sub.para(
        [
            "There are a few exceptions to the rule, as ",
            hlp.hboloc("אֵ֥לֶּה פֹ֛ה", "@Dt 5:3"),
            sub.thspp(),
        ]
    ),
]
