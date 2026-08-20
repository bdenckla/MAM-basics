from author_boj_util import author
from author_boj_util.job_ov_and_de import make_example_row

_VARIANTS = {
    "intro-header-only": "Each entry below",
    "intro-details": "The header of each entry below",
}


_WHERE_LIST = [
    "proposed is a proposed transcription of μL or, rarely, μA",
    "consensus is the Masoretic consensus reading (or a good guess of it)",
    "# (hash sign) (number sign) is a link to more details on this quirk",
    "c:v is the chapter and verse of the book of Job",
]


def qr_table_intro(ov_or_de):
    each = _VARIANTS[ov_or_de]
    return [
        author.para(_each(each)),
        author.table_c(make_example_row()),
        *_where(),
    ]


def here_is(start, jda=None):
    out = [
        f"{start} some quirks in μL in the book of Job.",
    ]
    if jda is not None:
        jdae = [" For more details, see the ", jda]
        return out + jdae
    return out


def _each(each):
    return [f"{each} takes the following form:"]


def _where():
    return [
        author.para("Where:"),
        author.unordered_list(_WHERE_LIST),
    ]
