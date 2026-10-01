import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_SHORTHAND = "“buffer could have $gaya, no $vocshewa”"
_FTNT_LIBERTIES = sub.footnote(
    [
        f"I coined the {_SHORTHAND} shorthand for this category,",
        " described these words in terms of the ",
        sub.afr3(),
        " pattern, and added the parenthetical remark on why this section"
        " rather than the next covers them.",
    ]
)
_FTNT_JER_5_7 = sub.footnote(
    [
        sub.irrelevant_ketiv("@Jer 5:7", "אֶֽסְלַֽח־", "אסלוח"),
        " ",
        sub.ITM_PRESENTS_KQ_IN_MANU_STYLE,
    ]
)
_TABLE_1 = hlp.table_std_rtl(
    [
        [*hlp.lns("@1C 5:32", "וּֽזְרַֽחְיָ֖ה", hlp.sy4pe("וּֽזְ-רַֽחְ-יָ֖ה"))],
        [*hlp.lns("@1C 27:19", "יִֽשְׁמַֽעְיָ֖הוּ", hlp.sy4("יִֽשְׁ-מַֽעְ-יָ֖-הוּ"))],
        # MAM does not have gaʿya on מ
        [*hlp.lns("@1S 26:19", "יִֽשְׁמַֽע־נָא֙", hlp.sy4pe("יִֽשְׁ-מַֽע־-נָא֙"))],
        [
            *hlp.lns("@Jer 5:7", "אֶֽסְלַֽח־לָ֔ךְ", hlp.sy4pe("אֶֽסְ-לַֽח־-לָ֔ךְ")),
            _FTNT_JER_5_7,
        ],
    ]
)
SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para(
        [
            "$Gaya is sometimes marked on a closed syllable in"
            " a single word having both of the following two irregularities:",
        ]
    ),
    sub.unordered_list(
        [
            "A buffer syllable that has, or could have, $gaya.",
            "No $vocshewa, i.e. the stress syllable comes right after the buffer syllable.",
        ]
    ),
    sub.para_paren(
        [
            "While this structure is non-regular, it is close enough to regular"
            " that we mention it here rather than in the next section, which covers"
            " cases where $gaya",
            " is marked on a closed syllable in more arbitrarily non-regular words.",
        ]
    ),
    sub.para(
        [
            f"Words of this {_SHORTHAND} category include the following two sub-categories:",
        ]
    ),
    sub.para(
        [
            "1) Words of a closed syllable followed by some form"
            " from the root היה or חיה which could have $gaya",
            " on the first syllable ",
            hlp.rtn_p(355),
            ", as ",
            hlp.lhbo("@Is 10:22", "אִם־יִהְיֶ֞ה"),
            sub.emdash(),
            "bN has ",
            hlp.hbo("אִֽם־"),
            sub.thspp(),
        ]
    ),
    sub.para(
        [
            "2) Words with a buffer syllable marked with $gaya and closed by a guttural ",
            hlp.rtn_p(354),
            ". E.g.:",
        ]
    ),
    _TABLE_1,
    sub.para_paren(
        [
            "In all four examples above, the first $gaya is musical, the second phonetic.",
        ]
    ),
    sub.para(
        [
            f"These {_SHORTHAND} words are somewhat similar to words of pattern ",
            sub.afr3(),
            ", which have prototype ",
            sub.hbo_pat_mitbarekhim(),
            " ",
            hlp.rtn_p(322),
            ". They are similar since in ",
            sub.afr3(),
            " words, too, the buffer syllable ",
            hlp.paren_tt(hlp.hbo("בָּ")),
            " could have $gaya (albeit on an open syllable).",
        ]
    ),
    # XXX turn the comment below into a footnote?
    # There used to be a sentence here saying:
    #     "Gaʿya in words of regular structure is the most common use of gaʿya on a closed syllable."
    # I moved that sentence sentence from here to the start of Section 324 because
    # this section is about words with irregular structure so it didn't make sense to me here.
]
