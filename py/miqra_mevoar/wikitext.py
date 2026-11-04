"""The base-chapter pages of Miqra Mevoar on Hebrew Wikisource, as MediaWiki stores them.

A base chapter is titled מקרא מבואר/פרקי בסיס/ספר <book>/<chapter>, a subpage of the
base-chapter index, INDEX_TITLE, with the book named as mam_bknas.he_bk39_name names it
and the chapter by its Hebrew numeral. A base chapter's first line is the chapter
heading. Each verse is one line, wrapped in Labeled Section Transclusion
tags named by the verse numeral, and a section heading is a line of its own before its
verse, starting with "*" and wrapped in tags named כותרת <verse>. The last line is the
category. Template מקרא מבואר transcludes these sections beside MAM's verse. These are
the line shapes of the live pages, and the only ones written here.

page_title takes a book as its pair of names in mam_bknas, a BS_ pair, so that it titles
any of MAM's chapters, not only those of the books in books.BOOKS: the index,
py/miqra_mevoar/index_page.py, links every chapter, whether or not its page exists.

MediaWiki stores a saved page in Unicode NFC with its trailing whitespace trimmed, so a
page is generated in exactly that form, with no final newline, and a saved page can be
compared with its source byte for byte. A save's pre-save transform would also rewrite
signatures, subst: and the pipe trick, and the parser would interpret markup, so a
heading or a paraphrase with any of the hazards that wikitext_hazards finds is refused.
"""

import unicodedata

from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn import mam_bknas


def page_title(mam_book, chapter_number):
    """The title of the base chapter of a book, given as its BS_ pair of mam_bknas."""
    book = mam_bknas.he_bk39_name(*mam_book)
    return f"{_TITLE_PREFIX}{book}/{hvn.INT_TO_STR_DIC[chapter_number]}"


def chapter_wikitext(chapter):
    """A base chapter's page text from its tracked record, exactly as a save stores it."""
    lines = [f"==פרק {hvn.INT_TO_STR_DIC[chapter['chapter']]}=="]
    for verse in chapter["verses"]:
        numeral = hvn.INT_TO_STR_DIC[verse["verse"]]
        where = f"chapter {chapter['chapter']} verse {verse['verse']}"
        if verse["heading"] is not None:
            heading = _plain(verse["heading"], f"the heading before {where}")
            section = f"{HEADING_SECTION}{numeral}"
            lines.append(f"*<{_START}{section}/>{heading}<{_END}{section}/>")
        paraphrase = _plain(verse["paraphrase"], f"the paraphrase of {where}")
        lines.append(f"<{_START}{numeral}/>{paraphrase}<{_END}{numeral}/>")
    lines.append(CATEGORY)
    # NFC, the form MediaWiki stores, is right here: the paraphrase is Rabbi Kokhav's
    # text, not MAM's, and the tracked JSON keeps the Word file's own mark order.
    return unicodedata.normalize("NFC", "\n".join(lines))


def wikitext_hazards(text):
    """What in text MediaWiki would interpret or transform, in the order checked."""
    found = [hazard for hazard in _HAZARDS if hazard in text]
    if "subst:" in text.casefold():
        found.append("subst:")
    if any(unicodedata.category(char) == "Cc" for char in text):
        found.append("a control character, such as a line break or a tab")
    if text != text.strip(" "):
        found.append("a space at either end")
    return found


def _plain(text, where):
    if not isinstance(text, str) or not text:
        raise ValueError(f"{where} is {text!r}, not a non-empty string")
    if hazards := wikitext_hazards(text):
        raise ValueError(f"{where} has {hazards}: {text!r}")
    return text


INDEX_TITLE = "מקרא מבואר/פרקי בסיס"
# The category line ends both the base chapters and the index.
CATEGORY = "[[קטגוריה:מקרא מבואר]]"
_TITLE_PREFIX = f"{INDEX_TITLE}/ספר "
_START = "קטע התחלה="
_END = "קטע סוף="
# A heading's section is named by this and its verse's numeral, the name by which a
# display page transcludes the heading from its base chapter.
HEADING_SECTION = "כותרת "
# Links, templates, tags, signatures, italics and bold, magic words and entities.
_HAZARDS = ("[[", "]]", "{{", "}}", "<", ">", "~~~", "''", "__", "&")
