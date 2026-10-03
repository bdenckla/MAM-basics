import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_LHBO_GEN_47_20_MANU = hlp.lhbo("@Gen 47:20", "כִּֽי־מָכְר֤וּ")
_LHBO_GEN_47_20_PRIN = hlp.lhbo("@Gen 47:20", "כִּי־מָֽכְר֤וּ")
_CF_2C_20_2 = hlp.compare_with(sub.ms_aleppo(), "לִיהֽוֹשָׁפָט֙")
_TABLE_1 = hlp.table_std_rtl(
    [
        [*hlp.lns("@1S 19:1", "וִיהֽוֹנָתָן֙", hlp.sy4("וִי-הֽוֹ-נָ-תָן֙"))],
        [*hlp.lns("@2S 2:22", "מֵאַֽחֲרָ֑י", hlp.sy4("מֵ-אַֽ--חֲרָ֑י"))],
        [*hlp.lns("@1S 30:15", "וְאוֹרִֽדְךָ֖", hlp.sy4("וְאוֹ-רִֽדְ--ךָ֖"))],
        [*hlp.lns("@Jos 10:20", "גְדוֹלָֽה־מְאֹ֖ד", hlp.sy4("גְדוֹ-לָֽה־מְ--אֹ֖ד"))],
    ]
)
_TABLE_2_DATA = [
    [sub.ms_lenin(), hlp.lhbo("@2C 20:2", "לִֽיהוֹשָׁפָט֙"), _CF_2C_20_2],
    [sub.ms_cairo(), hlp.lhbo("@Amos 4:1", "הָֽרֹצְצ֖וֹת")],
    [sub.ms_cairo(), hlp.hbo("הָֽאֹמְרֹ֥ת")],
    [sub.ms_b_4445(), hlp.lhbo("@Lev 13:7", "הֵֽרָאֹת֛וֹ")],
]
_TABLE_2 = hlp.table_std(_TABLE_2_DATA, coldirs=["ltr", "rtl", "ltr"])
_TABLE_3 = hlp.table_std_rtl(
    [
        [*hlp.lns("@Ez 42:5", "מֵֽהַתַּחְתֹּנ֛וֹת", "מֵֽ-הַ-תַּחְ-תֹּ-נ֛וֹת")],
        # MAM lacks gaʿya on מ; see trope#380 (private tracker)
    ]
)
_TABLE_4 = hlp.table_std_rtl(
    [
        [_LHBO_GEN_47_20_MANU],
        [hlp.lhbo("@Gen 31:52", "לֹֽא־תַעֲבֹ֨ר")],  # MAM lacks gaʿya on ל
        [hlp.lhbo("@Gen 35:22", "בְנֵֽי־יַעֲקֹ֖ב")],
        [hlp.lhbo("@Is 60:5", "כִּֽי־יֵהָפֵ֤ךְ")],
        [hlp.lhbo("@Dt 9:3", "הֽוּא־הָעֹבֵ֤ר")],
    ]
)
SEC = [
    sub.para(
        [
            "If two adjacent syllables are both candidates for $gaya_osr,"
            " the one closer to the stress is usually chosen. E.g.:",
        ]
    ),
    # sub.para([
    #     'If a word contains two syllables which are open, or '
    #     'contain ',sub.alvfb_shewa(),', and so are suitable for ',
    #     sub.gaya(),', and these come one after the other, then ',sub.gaya(),' is '
    #     'usually marked on the one close to the accent in preference to '
    #     'the other. E.g.:'
    # ]),
    _TABLE_1,
    sub.para_paren(
        [
            "The table above includes one syllable, ",
            hlp.hbo("לָֽה־מְ"),
            sub.thspc(),
            " that, awkwardly, spans a $maqqef boundary!",
        ]
    ),
    sub.para(
        [
            "This preference for the closer candidate"
            " is used in printed texts, and in some manuscripts, such as ",
            sub.ms_aleppo(),
            ". In some other manuscripts, however, the candidate farther from the stress"
            " is preferred, either consistently or sporadically. E.g.:",
        ]
    ),
    _TABLE_2,
    sub.para(
        [
            "We have also seen an example in ",
            hlp.rtn(327),
            " in which the candidate farther from the stress is chosen:",
        ]
    ),
    _TABLE_3,
    sub.para(
        [
            "If the candidate farther from the stress is on a word with $maqqef,"
            " and so preserves something of the original"
            " main stress of that word, then this farther candidate is given"
            " preference over the nearer one in the manuscripts. E.g.:",
        ]
    ),
    _TABLE_4,
    sub.para(
        [
            "There are a few exceptions to this rule in the manuscripts, but not many."
            " However, printed texts still give preference to the $gaya",
            " nearer the stress. E.g. in such texts the first example above would be pointed ",
            _LHBO_GEN_47_20_PRIN,
            sub.thspp(),
        ]
    ),
]
