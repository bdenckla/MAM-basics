from author_boj_util import author
from author_boj_util.all_verses_but_this import reiteration_new_in_bhq

_GENCOM_PARA1 = [
    "Consensus has no כתיב/קרי here, or, if you like,",
    " %לא are the letters of both the כתיב and קרי.",
    " So, we could say that the consensus כתיב/קרי is",
    [" ", author.span_unpointed_tanakh("לא/לא"), " and"],
    " the proposed כתיב/קרי for μL is",
    [" ", author.span_unpointed_tanakh("לא/לו"), "."],
]
_GENCOM_PARA2 = [
    ["Aside: don’t be confused by what might look like an L (ell)"],
    [" open to the southeast, above the א of %לא;"],
    [" it is the bar of a קמץ connected to a מרכא, both belonging to the ב of"],
    [" ", author.hbo("בָּ֥אוּ"), " on the line above."],
]
RECORD_0621 = {
    "qr-noted-by": "nBHQ-nDM",
    "qr-cv": "6:21",
    "qr-consensus": "לֹ֑א",
    "qr-lc-proposed": "ל֑וֹ",
    "qr-what-is-weird": "קרי of %לו not %לא",
    "qr-highlight": [1, 2],
    "qr-generic-comment": [author.para(_GENCOM_PARA1), author.para(_GENCOM_PARA2)],
    "qr-bhq-comment": reiteration_new_in_bhq("6:21"),
    "qr-lc-loc": {"page": "398B", "column": 2, "line": 20},
    "qr-ac-loc": {"page": "271v", "column": 2, "line": 17, "word": 6},
}
