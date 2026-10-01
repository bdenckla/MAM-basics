import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_FTNT_LIBERTIES = sub.footnote(
    [
        "I substituted “length” for $itm’s “quantity” and “ultra-short” for its"
        " “very short”, and restructured $itm’s prose into the list below."
        " I also added the alternative name ",
        hlp.rom("qameṣ qaṭan"),
        " and the description of /ɔ/ as open-mid back rounded.",
    ]
)
_TABLE_1 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Job 9:13", "שָׁ֝חֲח֗וּ")],
        [hlp.lhbo("@Ps 98:8", "יִמְחֲאוּ־")],
        [hlp.lhbo("@Nu 13:22", "אֲחִימַן֙")],
    ]
)
_TABLE_2 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Ez 16:6", "חֲיִ֔י")],
        [hlp.lhbo("@Jud 18:19", "הֱיוֹתְךָ֣")],
        [hlp.lhbo("@Ps 88:5", "אֱיָֽל׃")],
    ]
)
SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para(
        [
            "From the point of view of length, a $vocshewa was an ultra-short vowel",
            sub.emdash(),
            "even shorter than a short vowel. From the point of view of quality, a"
            " $vocshewa usually had the quality of a ",
            sub.patax(),
            ". But, on a non-guttural before a guttural, a"
            " $vocshewa had the same quality as the vowel after the guttural,"
            " and this vowel was of course not always ",
            sub.patax(),
            ". Thus:",
        ]
    ),
    sub.unordered_list(
        [
            [
                "in ",
                hlp.hbo("בְּאֵר"),
                " the $vocshewa was pronounced as an ultra-short ",
                sub.tsere(),
                ",",
            ],
            ["in ", hlp.hbo("מְאֹד"), " as an ultra-short ", sub.xolem(), ", and "],
            [
                "in ",
                hlp.lhbo("@Gen 2:23", "לֻֽקְחָה־זֹּֽאת׃"),
                " as an ultra-short ",
                sub.qamets(),
                " (indeed here some manuscripts have ",
                sub.x_qamets(),
                ", i.e. ",
                hlp.hbo("לֻֽקֳחָה־זֹּֽאת"),
                "). ",
                hlp.paren(
                    [
                        "For the Tiberians, the ",
                        sub.qamets(),
                        " sign always represented the"
                        " same vowel quality, /ɔ/ (open-mid back rounded),"
                        " so ",
                        sub.x_qamets(),
                        " and ",
                        sub.qamets_x_paren_qamets_q(),
                        " differed from ",
                        sub.qamets_g(),
                        " only in length.",
                    ]
                ),
            ],
        ]
    ),
    sub.para(
        [
            "On a guttural before another guttural,"
            " i.e. on the first of a pair of gutturals,"
            " a $vocshewa had the quality of a ",
            sub.patax(),
            ", and was notated as such, with a ",
            sub.x_patax(),
            ". I.e. it was not influenced by the quality of the vowel"
            " after the second guttural of the pair."
            " E.g.:",
        ]
    ),
    _TABLE_1,
    sub.para(
        [
            "On a non-guttural before a ",
            sub.yod(),
            ", a $vocshewa was pronounced as an ultra-short ",
            sub.xireq(),
            ", as in ",
            hlp.hbo_varacc("בְּיוֹם"),
            " and ",
            hlp.lhbo("@1C 24:12", "לְיָקִ֖ים"),
            ". However, on a guttural, it was pronounced as an ultra-short ",
            sub.segol(),
            ", ",
            sub.patax(),
            ", or ",
            sub.qamets(),
            ", and was notated as such, with the $xatef symbols for those vowels. E.g.:",
        ]
    ),
    _TABLE_2,
    sub.para(
        [
            "The pronunciation of $vocshewa with $gaya is described in ",
            hlp.rtn(336),
            ".",
        ]
    ),
]
