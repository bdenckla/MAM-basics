import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_BUT_WHEN_DDD_FULL_LENGTH = [
    "But, when it was marked with $gaya, it was pronounced like a full-length",
]
_CONTENTS_OF_TABLE = [
    [
        sub.dol(
            [
                "A $shewa"
                " at the start of a word was generally pronounced as a small (short) ",
                sub.patax(),
                " (פתחה קטנה).",
            ]
        ),
        sub.dol([_BUT_WHEN_DDD_FULL_LENGTH, " ", sub.patax(), " (בפתחה גדולה תצא)."]),
    ],
    [
        sub.dol(
            [
                "A $shewa"
                " before a guttural"
                " was pronounced as a short vowel of"
                " the same quality as the vowel after the guttural.",
            ]
        ),
        sub.dol(
            [
                _BUT_WHEN_DDD_FULL_LENGTH,
                " vowel of that quality. Thus, for example, ",
                hlp.lhbo("@Jud 1:7", "בְּֽהֹנוֹת֩"),
                " would be pronounced with three full-length ",
                sub.xolem(),
                " sounds.",
            ]
        ),
    ],
    [
        sub.dol(
            [
                "A $shewa at the start of a word before a ",
                sub.yod(),
                " was pronounced as a short ",
                sub.xireq(),
                ".",
            ]
        ),
        sub.dol([_BUT_WHEN_DDD_FULL_LENGTH, " ", sub.xireq(), "."]),
    ],
]
_TABLE = hlp.table_std(_CONTENTS_OF_TABLE)

SEC = [
    sub.para(
        [
            "$Gaya with $shewa"
            " is regularly marked in early manuscripts."
            " But the rules for it are described neither in early sources, nor"
            " even by ",
            sub.yequtiel_hn(),
            ". Heidenheim and Baer were the first to establish these rules."
            " The pronunciation of $shewa"
            " with $gaya",
            " is described in the masoretic literature ",
            hlp.paren(
                [
                    "as in the ",
                    sub.diqduqe_baer(11),
                    sub.emdash(),
                    "see also Morag, 1963, p. 160 ff.",
                ]
            ),
            ". They state that:",
        ]
    ),
    _TABLE,
]
