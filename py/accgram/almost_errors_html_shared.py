"""Small HTML render helpers shared across the "almost errors" page sections.

The lowest presentation layer: verse-reference formatting, UXLC/MAM link
anchors, and the shared error-tree table wrapper.  Imported by the per-section
modules (``almost_errors_charities``, ``almost_errors_oddities``) and the
``almost_errors_html`` coordinator; depends on nothing else in the page.
"""

from __future__ import annotations

import re

from accgram import ob_error_context
from accgram import ob_tree_table
from accgram import rtms_report
from accgram.uni_to_marks import is_accent, is_base_letter
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id
from mb_cmn import bib_locales as bl
from mb_misc import osis_book_abbrevs as oba
from py_html import wlc_utils_html as H
from py_wlc import my_wlc_bcv_str


def ref_display(bcv: str) -> str:
    bb = bcv[:2]
    chv = bcv[2:]
    return f"{wlc_bb_to_bk39id(bb)} {chv}"


def ref_abbrev(bcv: str) -> str:
    """The bcv as visible prose names a verse -- "Gen. 2:7", "1 Chr. 15:17".

    The book is its OSIS abbreviation, with a period when the abbreviation truncates the
    book's name (so Job, Ruth, Ezra, Joel, Amos and Jonah take none) and a space after a
    leading numeral ("1Chr" being fine in a filename and jarring as prose).

    Written for ``maqaf_nonfinal_accents_page``, which still holds the only other spelling of
    a reference this repo renders (``ref_display``'s bare bk39id, and ``ref_short``'s compact
    ``G5:29``).  It moved here when a second page wanted it.
    """
    bk39 = wlc_bb_to_bk39id(bcv[:2])
    abbrev = oba.BOOK_ABBREVS[bk39]
    dot = "" if abbrev == bk39 else "."
    spaced = f"{abbrev[0]} {abbrev[1:]}" if abbrev[0].isdigit() else abbrev
    return f"{spaced}{dot} {bcv[2:]}"


def ref_short(bcv: str) -> str:
    """Compact ``G5:29``-style reference (short book name, no space) for a ``gn5:29`` bcv."""
    chnu, vrnu = (int(part) for part in bcv[2:].split(":"))
    return bl.short_bcv((wlc_bb_to_bk39id(bcv[:2]), chnu, vrnu))


def accents_and_letters(word: str) -> str:
    """Reduce a pointed Hebrew word to just its base letters and accents, dropping vowels,
    dagesh, and other points.  Used for the alternate-form columns, which illustrate accent
    placement, not vocalization."""
    return "".join(ch for ch in word if is_base_letter(ch) or is_accent(ch))


def verse_links(bcv: str) -> object:
    bb, chnu, vrnu, _bcv = rtms_report.parse_ref_to_wlc_bcv(f"{bcv[:2]} {bcv[2:]}")
    links = (
        H.anchor("UXLC", {"href": my_wlc_bcv_str.get_tanach_dot_us_url(bcv)}),
        " | ",
        H.anchor(
            "MAM", {"href": rtms_report.mam_with_doc_url(bb=bb, chnu=chnu, vrnu=vrnu)}
        ),
    )
    return H.para(links)


def render_tree(tree_text: str) -> object:
    tree = ob_error_context.parse_tree_from_text(tree_text)
    if tree is not None:
        return H.div(
            (ob_tree_table.render_error_tree_table(tree),),
            {"class": "goerwitz-obs-tree-wrap"},
        )
    return H.div(
        (H.htel_mk("pre", None, tree_text),),
        {"class": "goerwitz-obs-tree-wrap"},
    )


def hbo(text: str) -> object:
    return H.span(text, {"lang": "hbo"})


# A run of Hebrew-block characters -- letters, points, accents, and the maqaf / sof pasuq
# that join or end an accent-word.  Covers both bare letter skeletons and fully-pointed
# words, so the whole word stays in one hbo span rather than being split at its marks.
# Inter-word spaces are kept inside the run so a whole Hebrew phrase (multiple space-separated
# words) stays in one hbo span; leading/trailing spaces bordering non-Hebrew text stay out.
_HEBREW_RUN_RE = re.compile(r"[֐-׿]+(?: +[֐-׿]+)*")

# Any Hebrew combining mark -- vowel, dagesh, accent, meteg.  The ranges are written as
# numeric escapes because a bare combining mark in a literal renders as a floating diacritic
# on the quote: U+0591-U+05BD accents through meteg, U+05BF rafe, U+05C1-U+05C2 the shin/sin
# dots, U+05C4-U+05C5 the upper/lower dots, U+05C7 qamats qatan.  Deliberately NOT here:
# U+05BE maqaf, U+05C0 paseq, U+05C3 sof pasuq -- spacing punctuation, not pointing.
_HEBREW_MARK_RE = re.compile("[\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7]")


def wrap_hebrew_runs(text: str) -> tuple[object, ...]:
    """Split ``text`` into a flat (string | hbo-span) sequence, wrapping each *pointed* run.

    Each maximal Hebrew phrase -- consecutive Hebrew words and the spaces between them --
    is kept in a single hbo span rather than one span per word.  Wrapping the Hebrew in
    ``lang="hbo"`` spans gives it the Hebrew font and (via the stylesheet) keeps it upright
    -- Hebrew is never italicized.

    A run carrying no point or accent is left alone, in whatever font the surrounding English
    prose is set in (Ben, 2026-07-28, of the strand name עליון: "just let it stay in whatever
    the default font is for surrounding Latin-alphabet (English-language) text").  The hbo
    font is Taamey D at 140%, chosen so pointing and accents are legible; an unpointed name or
    term has no pointing to show, so the size and the font switch buy nothing and only make
    the term shout in the middle of a sentence.  Bare letters plus maqaf or sof pasuq count as
    unpointed -- those are punctuation, not marks to be read."""
    pieces: list[object] = []
    cursor = 0
    for match in _HEBREW_RUN_RE.finditer(text):
        run = match.group(0)
        if not _HEBREW_MARK_RE.search(run):
            continue
        start, end = match.span()
        if start > cursor:
            pieces.append(text[cursor:start])
        pieces.append(hbo(run))
        cursor = end
    if cursor < len(text):
        pieces.append(text[cursor:])
    return tuple(pieces)


def text_para(text: str) -> object:
    """``H.para(wrap_hebrew_runs(text))`` -- the shape nearly every prose paragraph takes.

    One string in, one paragraph out, its pointed Hebrew runs wrapped.  A paragraph built
    from non-text pieces (links, splices) still composes ``H.para`` directly."""
    return H.para(wrap_hebrew_runs(text))


def link(text: str, href: str) -> object:
    return H.anchor(text, {"href": href})


# Yeivin's book, written short with the full title on hover (Ben, 2026-07-28: "'Breuer, Chapter
# 9' doesn't say what breuer book ... use CoS and ITM respectively, and make these hover-reveal
# the full title").  Written for ``maqaf_nonfinal_accents_page``, which still holds the two books
# only it cites; this one moved here when ``wlc_chanted_word_residue_page`` wanted the same
# spelling, so the two pages cannot come to cite it differently.
ITM_TITLE = "Introduction to the Tiberian Masorah"


def itm() -> object:
    """Yeivin's ITM as a page names it: the abbreviation, the full title on hover."""
    return H.abbr("ITM", ITM_TITLE)


def uxlc_change_link(compact: str) -> object:
    """Anchor to a tanach.us changeset, labelled by its ``changeset-n`` id.

    ``compact`` is the ``release/changeset-n`` form (e.g. ``2020.10.19/2020.09.22-1``)
    the goerwitz page's “UXLC change” links use, expanded by the shared
    ``rtms_report`` helper so the URL form stays single-sourced."""
    changeset_n = compact.partition("/")[2]
    return H.anchor(changeset_n, {"href": rtms_report.expand_uxlc_change_ref(compact)})
