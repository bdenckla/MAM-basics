import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_FTNT = sub.footnote(
    [
        ["I added the $maqqef qualification; $itm simply refers to a closed syllable."],
        [" But, from context"],
        [" ", hlp.paren(["see ", hlp.rtn(337)]), ","],
        [" I feel that the $maqqef qualification is justified and helpful."],
    ]
)
_MUSICAL = sub.ordered_list_with_lcromalpha(
    [
        [
            "$Gaya_cs (“small” or “heavy” $gaya) in a"
            " word the structure of which can be either “regular” or “non-regular.”"
        ],
        "$Gaya_os (“great” or “light” $gaya).",
        "$Shewa $gaya.",
        ["$Gaya on a ", sub.mclv(), hlp.ftntjoin(" syllable.", _FTNT)],
    ]
)
_PHONETIC = sub.ordered_list_with_lcromalpha(
    [
        "$Gaya used to mark a $shewa that follows it as vocal.",
        "$Gaya used on account of a guttural.",
        "$Gaya used in the roots היה and חיה.",
    ]
)
_CONT_PARA = [
    ["The use of $gaya in different sources differs greatly."],
    [" In general, most categories of $gaya"],
    [" are not marked consistently in manuscripts,"],
    [" while in printed texts a number of categories are marked systematically."],
    [" For the study of the early manuscripts it is most important to note"],
    [" the categories of $gaya which are mentioned in masoretic treatises,"],
    [" and those mentioned in the ", sub.sefer_ha_xillufim(), ","],
    [" since the use of $gaya is the area"],
    [" in which bA and bN differ most often."],
    [" The categories of $gaya are as follows:"],
]

SEC = [
    sub.para(_CONT_PARA),
    sub.ordered_list_with_lcromnum(
        [
            ["Musical.", _MUSICAL],
            ["Phonetic.", _PHONETIC],
        ]
    ),
]
