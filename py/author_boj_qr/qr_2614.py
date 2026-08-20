from author_boj_util import author
from author_boj_util.job_common import suffix

_BHQ_COMMENT = [
    "$BHS does not catch this quirk in μL: it reflects the consensus rather than μL.",
    " $BHQ half-fixes the error in $BHS:",
    " it updates its marginal קרי note to reflect μL rather than the consensus,",
    " but it does not correspondingly update its bottom-of-page critical apparatus note.",
    " This error is similar to $BHQ’s error regarding the μL קרי of",
    [" ", author.span_unpointed_tanakh("ידעתה השחר"), " in $link_38_12_YD3F_HJXR."],
]

_GENCOM_PART1 = [
    "The consensus is that חולם stays חסר in the קרי, i.e. ",
    ["the ", suffix("רתו"), " ending in the כתיב merely expands to "],
    [suffix("רתיו"), " in the קרי."],
    " In contrast to the consensus, in μL, ",
    ["the ", suffix("רתו"), " ending in the כתיב expands all the way to "],
    [suffix("רותיב"), " in the קרי."],
    " The marginal קרי note in μL is a little hard to parse until you realize",
    " that it is “invaded” from above by the descender of a big dotted ק.",
]
_GENCOM_PART2 = [
    "In general I do not cover מלא/חסר differences here,",
    " but this one seemed worth noting because it involves a כתיב/קרי difference,",
    " and it was called out by a $WLC note.",
]

RECORD_2614 = {
    "qr-cv": "26:14",
    "qr-lc-proposed": "גְּ֝בוּרוֹתָ֗יו",
    "qr-what-is-weird": "חולם becomes מלא in קרי",
    "qr-consensus": "גְּ֝בוּרֹתָ֗יו",
    "qr-consensus-ketiv": "גְּ֝בוּרֹתָ֗ו",
    "qr-ac-loc": {"page": "276v", "column": 2, "line": 9, "word": 4},
    "qr-generic-comment": [
        author.para(_GENCOM_PART1),
        author.para(_GENCOM_PART2),
    ],
    "qr-highlight-lc-proposed": 5,
    "qr-lc-loc": {"page": "404A", "column": 2, "line": -5},
    "qr-bhq-comment": _BHQ_COMMENT,
    "qr-noted-by": "nWLC",
}
