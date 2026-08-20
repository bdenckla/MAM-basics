from author_boj_util import author
from author_boj_util.golinets import golinets_citation

_BHQ_COMMENT_PART_1 = [
    "$BHQ drops the note that $BHS has on this quirk.",
    " Usually $BHQ preserves notes that $BHS has on quirks.",
    " As usual, we don’t know whether $BHQ dropped this note on purpose or by accident.",
]
_BHQ_COMMENT_PART_2 = [
    "$BHQ silently lets the faint possible דגש “win” over the clear רפה in μL.",
    " In my opinion, $BHQ should have transcribed either both marks (דגש and רפה) or neither.",
    " Thus I consider $BHQ to have not accurately transcribed μL here.",
    " Also, $BHQ should have had a note.",
]

RECORD_1905 = {
    "qr-cv": "19:5",
    "qr-lc-q": "(?)",
    "qr-lc-proposed": "חֶרְפָּתִּֽֿי׃",
    "qr-what-is-weird": "דגש fights רפה",
    "qr-consensus": "חֶרְפָּתִֽי׃",
    "qr-generic-comment": [
        "A דגש on a letter with רפה doesn’t make sense.",
        " The color image of μL reveals this דגש to be unlikely.",
        [" It is judged to be just a speck, not a דגש, in ", golinets_citation("251")],
        " See $link_24_16.",
    ],
    "qr-highlight": 4,
    "qr-lc-loc": {"page": "402A", "column": 2, "line": -5},
    "qr-ac-loc": {"page": "274v", "column": 2, "line": 27, "word": 7},
    "qr-bhq-comment": [
        author.para(_BHQ_COMMENT_PART_1),
        author.para(_BHQ_COMMENT_PART_2),
    ],
    "qr-noted-by": "nBHL-nWLC",
}
