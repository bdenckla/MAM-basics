"""Exports note-page prose: the *actual* tanach.us note, read from a local copy.

UXLC's ``<x>`` code points at a per-(atom, code) note page on tanach.us, e.g.
``https://tanach.us/Notes/Proverbs/Proverbs.5.19.4-m.html``. Its reader-facing
*note* prose is the manuscript note we want to render, plus (issue UXLC-utils#30) the
page's own ``<h2>`` change-summary line, included verbatim as the note's opening
sentence -- however imperative-sounding, it is real content of this same
downloaded page, same trust boundary as the ``<p>`` prose. This is unrelated to
the *separately-ingested* local UXLC changes XML (``in/UXLC-misc/*.xml``, parsed
by ``py/uxlc_changes/``), whose ``<correction><description>`` is an imperative
instruction to the editor and is never used as note prose (issue UXLC-utils#19) -- it
survives only as the atom-letter consistency guard
(``clc_collect._check_atom_consistency``).

To keep the CLC build deterministic and offline, those pages are downloaded as a
separate, non-default step (``main_clc_download_notes``) into committed files
under ``in/UXLC-notes/``; this module only *reads* that local copy and extracts
its prose. No network here -- a page missing locally just returns ``None``.

Two page formats are in the wild and must both be handled:

  * NoteMaker-generated (newer): prose is the ``<h2>`` change-summary line
    followed by body-level ``<p>`` paragraphs; the author is
    ``<p><b><i>...</i></b></p>`` and the change link a
    ``<p align="right"><b><a>...</a></b></p>``.

  * Hand-authored (older, ~2021): the note's lead line is an ``<h4>`` and the rest
    of the prose is *bare* body text split by self-closing ``<p/>`` separators (no
    ``<p>...</p>`` wrappers at all); the author is a bare ``<b><i>...</i></b>``.

Both formats share the same noise, so one rule covers them: the prose is the body
text that is NOT inside a ``<table>`` (image credit / note index), NOT inside the
``<h1>`` citation, and NOT inside inline markup (``<b>``/``<i>``/``<a>``, which
wrap the author and the change link). Everything else in the body -- ``<h2>``
text, ``<p>`` text, ``<h4>`` text, and bare text -- is note prose.
"""

import html.parser
import re

import uxlc_paths

_WS_RE = re.compile(r"\s+")


def local_page_path(book_id, ch, v, position, code):
    """Committed local path of one (atom, code) note page.

    Keyed by the CLC bk39 ``book_id`` (the downloader maps it to the canonical
    tanach.us name for the remote URL; locally we keep the CLC id for uniformity).
    """
    filename = f"{book_id}.{ch}.{v}.{position}-{code}.html"
    return uxlc_paths.uxlc_notes_dir() / book_id / filename


def local_note_prose(book_id, ch, v, position, code):
    """Return the downloaded note page's prose (paragraphs joined), or None.

    None means no usable local page -- it was never downloaded (not yet fetched,
    or tanach.us has none), or the page carries no plain-text prose. The build
    then shows a bare ``[note not yet downloaded]`` placeholder, never a
    fabricated substitute (clc_collect; issue UXLC-utils#19).
    """
    path = local_page_path(book_id, ch, v, position, code)
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as page_fp:
        paragraphs = _extract_prose_paragraphs(page_fp.read())
    return " ".join(paragraphs) if paragraphs else None


def _extract_prose_paragraphs(page_text):
    parser = _NoteProseExtractor()
    parser.feed(page_text)
    return parser.paragraphs


# Inline markup that wraps non-prose (author byline, change link, image credit).
# Text inside any of these is skipped in both page formats.
_SKIP_TEXT_TAGS = frozenset({"b", "i", "a", "em", "strong"})
# Heading that is not prose: the citation (redundant with the ch:v.pos context
# already shown alongside the note). The <h2> change-summary heading is prose --
# see the module docstring -- and is deliberately NOT in this set.
_SKIP_HEADING_TAGS = frozenset({"h1"})
# Block-level tags whose boundaries end one prose run and start the next.
_BLOCK_TAGS = frozenset(
    {"p", "br", "div", "center", "tr", "li", "h1", "h2", "h3", "h4", "h5", "h6"}
)


class _NoteProseExtractor(html.parser.HTMLParser):
    """Collect the body note prose across both tanach.us note-page formats.

    Prose is body text outside any ``<table>``, outside the ``<h1>`` citation
    heading, and outside inline ``<b>``/``<i>``/``<a>`` author and change-link
    markup. Block boundaries split it into paragraphs.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._in_body = False
        self._table_depth = 0
        self._heading_depth = 0  # inside <h1> (citation heading)
        self._inline_depth = 0  # inside <b>/<i>/<a> (author, link, credit)
        self._buf = []
        self.paragraphs = []

    def _collecting(self):
        return (
            self._in_body
            and not self._table_depth
            and not self._heading_depth
            and not self._inline_depth
        )

    def _flush(self):
        text = _WS_RE.sub(" ", "".join(self._buf)).strip()
        if text:
            self.paragraphs.append(text)
        self._buf = []

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self._in_body = True
        elif tag in _BLOCK_TAGS:
            self._flush()  # close any run before a block boundary
        if tag == "table":
            self._table_depth += 1
        elif tag in _SKIP_HEADING_TAGS:
            self._heading_depth += 1
        elif tag in _SKIP_TEXT_TAGS:
            self._inline_depth += 1

    def handle_startendtag(self, tag, attrs):
        if tag in _BLOCK_TAGS:
            self._flush()  # self-closing <p/> and <br/> are paragraph separators

    def handle_endtag(self, tag):
        if tag in _BLOCK_TAGS:
            self._flush()
        if tag == "table":
            self._table_depth = max(self._table_depth - 1, 0)
        elif tag in _SKIP_HEADING_TAGS:
            self._heading_depth = max(self._heading_depth - 1, 0)
        elif tag in _SKIP_TEXT_TAGS:
            self._inline_depth = max(self._inline_depth - 1, 0)

    def handle_data(self, data):
        if self._collecting():
            self._buf.append(data)
