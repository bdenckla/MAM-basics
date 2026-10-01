import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_MSS_C_S = sub.ms_cairo(), " and ", sub.ms_s_507()
_TABLE_DATA_1 = [
    [hlp.hboloc("תָּבִ֣יאּוּ׀ לֶ֣חֶם", "@Lev 23:17")],
    [hlp.hboloc("וַיָּבִ֥יאּוּ ל֛וֹ", "@Gen 43:26")],
    [hlp.hboloc("וַיָּבִ֨יאּוּ לָ֜נוּ", "@Ezra 8:18")],
]
_TABLE_DATA_2_JOB_33_21 = [[hlp.hboloc("רֻאּֽוּ׃", "@Job 33:21")]]
_TABLE_DATA_3 = [
    [
        hlp.hboloc("שְׁאַּלְתִּיאֵל֙", "@Ḥag 1:1")
    ],  # As expected, MAM has doesn't have the mappiq in א, i.e. it has שְׁאַלְתִּיאֵל֙
    [
        hlp.hboloc("בְּלוֹאֵּ֨י", "@Jer 38:12")
    ],  # As expected, MAM has doesn't have the mappiq in א, i.e. it has בְּלוֹאֵ֨י
    [
        hlp.hboloc("קֹרְאֹּתַ֔יִךְ", "@Is 51:19")
    ],  # As expected, MAM has doesn't have the mappiq in א, i.e. it has קֹרְאֹתַ֔יִךְ
]
_COMPARE_WITH_THE_CONTRARY = [
    ["Compare with the contrary phenomenon in ", hlp.hbo("יִשְׁתַּחֲוּוּ")],
    [" covered in ", hlp.rtn(396), "."],
    # MAM has no mappiq in the 1st vav of related words like וַיִּֽשְׁתַּחֲו֖וּ
]

SEC = [
    sub.para(
        [
            "(ii) ",
            sub.alef(cap=True),
            " is marked with ",
            sub.mappiq(),
            " in four words in the Bible. Three derive from the root בוא: ",
        ]
    ),
    hlp.table_std_rtl(_TABLE_DATA_1),
    sub.para(
        [
            "These three represent most of the cases in which these words"
            " are followed by an initially-stressed word starting with ",
            sub.lamed(),
            ". Possibly there was a tendency to slur over the ",
            sub.alef(),
            " in this situation. ",
            hlp.paren(
                [
                    "The use of $gaya to mark guttural-closed syllables"
                    " may address a similar concern. See ",
                    hlp.rtn(354),
                    ".",
                ]
            ),
        ]
    ),
    sub.para(
        ["The fourth and final case of ", sub.alef(), " with ", sub.mappiq(), " is"]
    ),
    hlp.table_std_rtl(_TABLE_DATA_2_JOB_33_21),
    sub.para(
        [
            "Possibly the ",
            sub.mappiq(),
            " here is intended to emphasize"
            " the need to use the glottal stop"
            " rather than a /w/ glide between the two /u/ vowels."
            " ",
            hlp.paren(_COMPARE_WITH_THE_CONTRARY),
        ]
    ),
    sub.para(
        [
            "In some manuscripts such as ",
            sub.ms_cairo(),
            ", ",
            sub.mappiq(),
            " is used to mark ",
            sub.alef(),
            " as a consonant in words"
            " other than the agreed-upon four described above."
            " These additional cases of ",
            sub.mappiq(),
            " ",
            sub.alef(),
            " are more common where its value might be in doubt. E.g.:",
        ]
    ),
    hlp.table_std_rtl(_TABLE_DATA_3),
    sub.para(
        [
            "Non-consonantal ",
            sub.alef(),
            " is marked with ",
            sub.rafe(),
            " in nearly all manuscripts, but not consistently.",
        ]
    ),
    sub.para(
        [
            "A few manuscripts, particularly ",
            *_MSS_C_S,
            ", often mark ",
            sub.rafe(),
            " on the ",
            sub.alef(),
            " in ישראל, i.e. ",
            hlp.hbo("יִשְׂרָאֵֿל"),
            sub.thspp(),
            ""
            " This may reflect a pronunciation in which a glottal stop was absent there.",
        ]
    ),
]
