from taamey_d.doc import tad_distinctive
from taamey_d.doc import tad_challenging
from taamey_d.doc import tad_floating_xolam_xaser
from taamey_d.doc import tad_corpus
from taamey_d_build.font_version import VERSION
from mb_cmn.he_wikisource_url import he_page_url
from taamey_d.doc.html_helpers import *
from taamey_d.doc.book_chapter_verse import BOOK_PROPERTIES, cv_str_html

_TANACH_DOT_US = anchor("https://tanach.us", "tanach.us")
_MAM_HE_WIKISOURCE_URL = he_page_url("מקרא_על_פי_המסורה")
_MAM_HE_WIKISOURCE = anchor(_MAM_HE_WIKISOURCE_URL, "Hebrew Wikisource")
_MAM_WITH_DOC = anchor(
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/", "$MAM’s documentation notes"
)
_NEAR_ALEPPO_EDITION = anchor(
    "https://bdenckla.github.io/MAM-basics/near-aleppo/edition/", "near-Aleppo edition"
)
_TAIL = """
</body>
</html>
"""
# Until Taamey D's release tool and its downloads move to this repository, the
# downloads link names hbofonts' downloads index.
_HEAD = (
    headfun(
        gregorian_document_version="2026-10-27",
        hebrew_document_version="ט״ז בְּחֶשְׁוָן תשפ״ז",
        font_version=VERSION,
    )
    + """
<h2>Introduction</h2>
<p>
    $Taamey_D is derived from Taamey Frank $cap_CLM,
    a font designed by Yoram Gnat, of blessed memory.
    $Taamey_D’s goal is to support every word
    in the following two Hebrew Bible datasets:</p>
        <ul>
            <li>
                $cap_UXLC
                (<span class="hair-space-before">Unicode</span>
                $XML Leningrad Codex), whose canonical edition is hosted at
                """
    + _TANACH_DOT_US
    + """</li>
            <li>
                $cap_MAM
                (<span class="hair-space-before">Miqra</span>
                according to the Masorah), whose canonical edition is hosted at
                """
    + _MAM_HE_WIKISOURCE
    + """</li>
        </ul>
<p>
    $Taamey_D also supports a few words from
    """
    + _MAM_WITH_DOC
    + " and from the "
    + _NEAR_ALEPPO_EDITION
    + """.
</p>
<p>
    Current font binaries, corresponding source archives, checksums, and the
    preserved historical release are available from the
    <a href="https://bdenckla.github.io/hbofonts/downloads/">Taamey D downloads page</a>.
</p>
"""
)
_ACK = """
<p>
    Many people have helped me develop this font and
    develop my Hebrew enough to develop this font.
    Thanks to:
</p>
<ul>
    <li>Simon Cozens,
        for “collidoscope” and his other useful software for font development,
        and for helping me get started using it.
    </li>
    <li>Scott-Martin Kosofsky,
        for answering my questions about Hebrew fonts &amp; typesetting.
    </li>
    <li>John Hudson,
        for answering my questions about Hebrew fonts &amp; typesetting.
        I’d also like to thank John
        for his $SBL_Hebrew Font User Manual,
        the best reference for how to use Unicode
        to tell a font what you want in Biblical Hebrew.
    </li>
    <li>Avi Kadish,
        for teaching me much of what I know about the Hebrew Bible and
        for giving me the opportunity to work on $MAM.
    </li>
    <li>Chris Kimball,
        for giving me the opportunity to work on $UXLC.
    </li>
    <li>Ron Tabeka,
        for teaching me Hebrew &amp; chanting.
    </li>
</ul>
"""


_SEC_DISTINCTIVE = {}
_SEC_DISTINCTIVE["sec_title"] = "$h2_title_distinctive_features"
_SEC_DISTINCTIVE["id"] = "h2_distinctive_features"
_SEC_DISTINCTIVE["body_fun"] = tad_distinctive.sec_body
#
_SEC_CHALLENGING = {}
_SEC_CHALLENGING["sec_title"] = "$h2_title_challenging_cases"
_SEC_CHALLENGING["id"] = "h2_challenging_cases"
_SEC_CHALLENGING["body_fun"] = tad_challenging.sec_body
#
_SEC_ALEF = {}
_SEC_ALEF["sec_title"] = "$h2_title_floating_xx"
_SEC_ALEF["sec_title_abbrev"] = "$h2_title_floating_xx"
_SEC_ALEF["id"] = "h2_floating_xolam_xaser"
_SEC_ALEF["body_fun"] = tad_floating_xolam_xaser.sec_body
#
_SEC_CORPUS = {}
_SEC_CORPUS["sec_title"] = "$h2_title_notes_on_the_limited_corpus"
_SEC_CORPUS["id"] = "h2_notes_on_the_limited_corpus"
_SEC_CORPUS["body_fun"] = tad_corpus.sec_body
#
_SECTIONS = (_SEC_DISTINCTIVE, _SEC_CHALLENGING, _SEC_ALEF, _SEC_CORPUS)


def _make_section(accum, section):
    my_xheading2 = xheading2(section["sec_title"], section["id"])
    sec_body_fun = section["body_fun"]
    return my_xheading2, sec_body_fun(accum, section)


def _make_section_anchor(section):
    return anchor("#" + section["id"], section["sec_title"])


def get_section_title(section):
    return section["sec_title"]


def _table_of_contents():
    return para("This document has the following sections:") + _toc_proper()


def _toc_proper():
    list_items = tuple(map(_make_section_anchor, _SECTIONS))
    return unordered_list(*list_items)


def _make_refnum_anchor(ref_num_int, generate_id):
    num_str = str(ref_num_int)
    num_attrs = {}
    if generate_id:
        num_attrs["id"] = "ref_" + num_str
    num_attrs["href"] = "#callout_" + num_str
    return xanchor2(num_str, num_attrs)


def _make_display_tuple(accum_entry, generate_id):
    book_code = accum_entry["book_code"]
    short_display_name = BOOK_PROPERTIES[book_code][0]
    sec_title_abbrev = accum_entry["sec_title_abbrev"]
    subsec_title_abbrev = accum_entry["subsec_title_abbrev"]
    subsec_or_sec = subsec_title_abbrev or sec_title_abbrev
    return (
        _make_refnum_anchor(accum_entry["ref_num"], generate_id),
        short_display_name,
        cv_str_html(accum_entry["chap_colon_ver"]),
        subsec_or_sec,
    )


def _cv_str_mam(chap_colon_ver):
    if isinstance(chap_colon_ver, str):
        return chap_colon_ver
    return chap_colon_ver["MAM"]


def _bcv_sort_key(accum_entry):
    book_code = accum_entry["book_code"]
    chap_colon_ver = accum_entry["chap_colon_ver"]
    ordered_short_name = BOOK_PROPERTIES[book_code][1]
    cv_str_mam = _cv_str_mam(chap_colon_ver)
    chap, ver = map(int, cv_str_mam.split(":"))
    return ordered_short_name, chap, ver


def _make_ref_list(accum):
    heading = xheading2("Numbered Biblical references", "ref_list")
    cols_excl_fr_rowspan = frozenset((1,))  # book
    specifics = heading, cols_excl_fr_rowspan
    return _make_ref_list_or_index(accum, specifics, generate_id=True)


def _make_index(accum):
    heading = xheading2("Index of Biblical references", "index")
    cols_excl_fr_rowspan = frozenset((3,))  # sec. or subsec.
    specifics = heading, cols_excl_fr_rowspan
    return _make_ref_list_or_index(accum, specifics, sort_key_fn=_bcv_sort_key)


def _make_ref_list_or_index(accum, specifics, generate_id=False, sort_key_fn=None):
    heading, cols_excl_fr_rowspan = specifics
    accum_sorted = sorted(accum, key=sort_key_fn) if sort_key_fn else accum
    display_tuples = tuple(_make_display_tuple(a, generate_id) for a in accum_sorted)
    rowspans = _rowspans(display_tuples, cols_excl_fr_rowspan)
    inside = xtable_rows_of_cells(display_tuples, rowspans)
    header_cells = "N", "book", "c:v", "section or subsection"
    return heading, xtable(header_cells, inside)


def _ones(row):
    return [1] * len(row)


def _rowspans(rows, excluded_columns=None):
    my_excl_col = excluded_columns or frozenset()
    rowspans = list(map(_ones, rows))
    lasts = [dict(val=None, i=None) for col in rows[0]]
    for i, row_i in enumerate(rows):
        for j, cell_i_j in enumerate(row_i):
            if cell_i_j == lasts[j]["val"] and j not in my_excl_col:
                lasts_j_i = lasts[j]["i"]
                rowspans[lasts_j_i][j] += 1
                rowspans[i][j] = 0
            else:
                lasts[j] = dict(val=cell_i_j, i=i)
    return rowspans


def _sections():
    accum = []
    sections = tuple(_make_section(accum, sec) for sec in _SECTIONS)
    sum_of_sections = sum(sections, tuple())
    transition = (
        xpara("This document now concludes with the following:"),
        xunordered_list(
            (
                "a section providing the book, chapter, and verse for each"
                + " of this document’s numbered Biblical references"
            ),
            (
                "an index of those Biblical references"
                + " in order of their appearance in the Hebrew Bible"
            ),
        ),
    )
    ref_list = _make_ref_list(accum)
    index = _make_index(accum)
    return sum_of_sections + transition + ref_list + index


BIG_STR = _HEAD + _table_of_contents() + _ACK + to_str(_sections()) + _TAIL
