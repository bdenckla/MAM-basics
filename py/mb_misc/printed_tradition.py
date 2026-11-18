"""The hover that explains "the printed tradition", the English of MAM's sigil דפוסים.

Our English renderings of MAM's notes say "the printed tradition" for the sigil, as the
hebrew-prose skill's references/terminology.md says in its section on it. A page that
shows such a rendering gives each "the printed tradition" the hover HOVER on a span of
the class CLASS, whose style is a dotted underline. The phrase inside "part of the
printed tradition" or "most of the printed tradition" gets the hover too. A page's own
definition of the term, such as the key of sigils on
gh-pages/wlc/accgram/telg-doc-notes.html, gets none.

The stress-helpers page had the hover first. On 2026-11-18 Ben accepted the
recommendation that each "the printed tradition" on the other pages get it too, defined
once, here: "I concur with all 3 of your recommendations."

The pages build their HTML in two ways, so this module has a function for each:
explain() for an element tree, of mb_html or of py_html.wlc_utils_html, and
explain_html() for HTML built as a string.
"""

from html import escape
import re

from mb_misc import mb_html

# The hover on each "the printed tradition", which renders MAM's sigil דפוסים in the
# notes.  Ben, 2026-11-18: "When translating MAM doc-notes, in this document and
# elsewhere [...] for דפסים or whatever the word is you sometimes translate as "printed
# editions", please instead use "the printed tradition"".  The hebrew-prose skill's
# terminology reference quotes the rest of his instruction.  The hover's definition is
# the MAM introduction's, in in/mam-ws-intro/appendices.mediawiki, line 272, and Ben
# asked, of its draft, the same day: "I would like it to reiterate what it is talking
# about".
HOVER = (
    "In MAM’s notes, דפוסים, which we usually translate as “the printed tradition”,"
    " means the customary text of a selection of widespread editions from the 19th and"
    " early 20th centuries, in the lineage of the second Venice Miqraot Gedolot. The"
    " notes cite that Venice edition, and Koren, apart."
)
# The class of a term with a hover, which a page's style underlines with dots, as the
# browser underlines an abbr's.
CLASS = "explained"
# That style, for a page whose generator writes its style.  gh-pages/document.css and
# doc/near-aleppo-avi-ketiv-investigation.html have the same rule.
STYLE = f".{CLASS} {{ text-decoration: underline dotted; cursor: help; }}"
# "the printed tradition", or "The printed tradition" at the head of a sentence, with any
# whitespace between its words, as where a line of a page's source breaks it.
_PHRASE = re.compile(r"((?<!\w)[Tt]he\s+printed\s+tradition(?!\w))")
_TITLE = escape(HOVER, quote=True)


def explain(text):
    """The text as an element's contents: a list of its strings, with each "the printed
    tradition" in a span with the hover.  The span is an element of mb_html, which a
    tree of py_html.wlc_utils_html takes too."""
    return [
        mb_html.span(piece, {"class": CLASS, "title": HOVER}) if index % 2 else piece
        for index, piece in enumerate(_PHRASE.split(text))
        if piece
    ]


def explain_html(text, plain=escape):
    """The text as HTML: each "the printed tradition" in a span with the hover, and each
    run of the rest as plain makes it HTML, which by default is escaped."""
    return "".join(
        (
            f'<span class="{CLASS}" title="{_TITLE}">{escape(piece)}</span>'
            if index % 2
            else plain(piece)
        )
        for index, piece in enumerate(_PHRASE.split(text))
        if piece
    )
