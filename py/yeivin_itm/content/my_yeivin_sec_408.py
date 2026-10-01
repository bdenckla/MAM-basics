import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

TABLE_1_DATA = [
    ("וַאֲנַ֥חְנוּ קַּ֝֗מְנוּ", "@Ps 20:9"),
    ("יִסְּרַ֣נִּי יָּ֑הּ", "@Ps 118:18"),
    ("קָרָ֣אתִי יָּ֑הּ", "@Ps 118:5"),
]
TABLE_2_DATA = [
    ("ק֤וּמוּ צְּאוּ֙", "@Gen 19:14"),
    ("תַּשְׁבִּ֥יתוּ שְּׂאֹ֖ר", "@Ex 12:15"),
    ("הָיִ֤יתִי שְּׂחֹק֙", "@Lam 3:14"),
]
_GEN_19_2 = "הִנֶּ֣ה נָּא־אֲדֹנַ֗י", "@Gen 19:2"
_JUD_6_39 = "אֲנַסֶּ֤ה נָּא־רַק־הַפַּ֙עַם֙", "@Jud 6:39"
_FTNT_JUD_6_39 = sub.footnote(
    [
        "I give both of the last two examples explicitly: ",
        hlp.hboloc(*_GEN_19_2),
        " and ",
        hlp.hboloc(*_JUD_6_39),
        sub.thspp(),
        " But $itm gives only the next-to-last example explicitly."
        " It gives the last two examples as ",
        hlp.hboloc(*_GEN_19_2),
        " “and the similar case in Jud 6:39.”",
    ]
)

TABLE_3_DATA = [
    ("הִשְׁמִ֥יעוּ זְּעָקָ֖ה", "@Jer 48:4"),
    ("חֶלְבָּ֥מוֹ סָּגְר֑וּ", "@Ps 17:10"),
    ("יָבִ֣ינוּ סִּירֹתֵכֶ֣ם", "@Ps 58:10"),
    _GEN_19_2,
    _JUD_6_39,
]
SEC = [
    sub.para_with_romnum_and_initial_uah(
        "ii",
        sub.cmn_407_lcromnum_ii(),
        [
            ["Where α ends with a long vowel other than ", sub.qamets(), ", "],
            ["$dexiq is sometimes marked when β has initial stress, as "],
        ],
    ),
    hlp.table_std_alpha_beta_2col_std(TABLE_1_DATA, arg_to_troh=None),
    sub.para(["This occurs most often where $shewa precedes the stress. E.g.:"]),
    hlp.table_std_alpha_beta_2col_std(TABLE_2_DATA, arg_to_troh=None),
    sub.para_with_romnum_and_initial_uah(
        "iii",
        sub.cmn_407_lcromnum_iii(),
        [
            "$Dexiq is used in a few cases that do not fit any of the rules given above. ",
            hlp.ftntjoin("E.g.:", _FTNT_JUD_6_39),
        ],
    ),
    hlp.table_std_alpha_beta_2col_std(TABLE_3_DATA, arg_to_troh=None),
]
