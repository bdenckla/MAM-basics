import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_FTNT_LIBERTIES = sub.footnote(
    [
        "I introduced the term “plain” for initial stress that does not include"
        " a $vocshewa, and split $itm’s single remark on rarity into separate"
        " remarks on the plain and $shewa types. I also added the parenthetical"
        " remark on how such a $vocshewa may be notated.",
    ]
)
_TABLE_1_DATA = [
    ("עֲבָדֶ֥יךָֽ אֵ֛לֶּה", "@2K 1:13"),
    ("עָשִׂ֤יתָֽה חֶ֙סֶד֙", "@1S 15:6"),
    ("עָ֤לָֽה מָ֙וֶת֙", "@Jer 9:20"),
    ("ס֤וּרֽוּ ס֙וּרוּ֙", "@Is 52:11"),  # MAM does not have gaʿya on the ר of ס֤וּרוּ
    ("הוּחַ֤דָּֽה חֶ֙רֶב֙", "@Ez 21:16"),  # MAM does not have gaʿya on the ד
    ("גִּבּ֤וֹרֵֽי חַ֙יִל֙", "@1C 12:26"),
    ("הֵילִ֤ילִֽי שַׁ֙עַר֙", "@Is 14:31"),
]
_TABLE_1 = hlp.table_std_alpha_beta_2col_std(_TABLE_1_DATA, arg_to_troh=None)
_TABLE_2_DATA = [
    ("פַּדֶּ֣נָֽה אֲרָ֔ם", hlp.make_aeloc("@Gen 28:2"), ""),
    ("וַיֵּנִקֵ֤הֽוּ דְבַשׁ֙", "@Dt 32:13", ""),
    ("לְמַ֨עְלָֽה לְמַ֜עְלָה", "@Ez 41:7", "(2× in this verse)"),
    # I added "2× in this verse"
    # MAM does not have gaʿya on the לָ of לְמַ֨עְלָה
    ("בֹּ֤שְׁנֽוּ מְאֹד֙", "@Jer 9:18", ""),
]
_TABLE_2 = hlp.table_std_alpha_beta_3col_std(_TABLE_2_DATA, arg_to_troh=None)
SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para(
        [
            "A special case of $gaya_os is after the stress."
            " $Gaya may be marked on an open syllable after penultimate stress"
            " if the next word has initial stress."
            " Here are some examples where that initial stress is plain,"
            " where by “plain” we mean that it does not include a $vocshewa:",
        ]
    ),
    _TABLE_1,
    sub.para(
        [
            "This plain type of this $gaya is rare."
            " It is most common in early manuscripts,"
            " but even there it occurs only in scattered places.",
        ]
    ),
    sub.para(
        [
            "This $gaya occurs more often where"
            " the stress syllable of the next word includes a $vocshewa. E.g.:",
        ]
    ),
    _TABLE_2,
    sub.para_paren(
        [
            "As usual, the $vocshewa may be notated either as a $simshewa"
            " or as a $x_shewa.",
        ]
    ),
    sub.para(
        [
            "Like the plain type of this $gaya, the $shewa type"
            " is most common in early manuscripts,"
            " and is not marked in printed texts.",
        ]
    ),
]
