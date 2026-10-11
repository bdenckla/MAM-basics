"""Add the approved near-Aleppo link cues without reserializing the HTML.

Only anchor attributes and the stylesheet declaration are inserted. Scripture,
documentation, source-data scripts, URLs and Hebrew mark order remain untouched.
Direction follows document order, so the same fragment can have up and down links.
"""

from __future__ import annotations

import posixpath
import re
from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from mb_cmn import provenance

STYLESHEET = "link-presentation.css"
_SITE_HOST = "bdenckla.github.io"
_SITE_ROOT = "/MAM-basics/"
_PAGE_ROOT = _SITE_ROOT + "near-aleppo/"
_VOID = frozenset(
    "area base br col embed hr img input link meta param source track wbr".split()
)


@dataclass(frozen=True)
class _Link:
    start: int
    insertion: int
    href: str
    containers: tuple[str, ...]


class _Scan(HTMLParser):
    def __init__(self, document):
        super().__init__(convert_charrefs=True)
        self._line_starts = [0, *(match.end() for match in re.finditer("\n", document))]
        self._stack = []
        self.targets = {}
        self.links = []
        self.feed(document)

    def _offset(self):
        line, column = self.getpos()
        return self._line_starts[line - 1] + column

    def _start(self, tag, pairs, *, push):
        attrs = dict(pairs)
        identifiers = tuple(
            value
            for value in (attrs.get("id"), attrs.get("name") if tag == "a" else None)
            if value
        )
        start = self._offset()
        for identifier in identifiers:
            # Browsers resolve a duplicated identifier to its first occurrence.
            self.targets.setdefault(identifier, start)
        if tag == "a" and "href" in attrs:
            if "data-na-link" in attrs:
                raise ValueError("Near-Aleppo link presentation was applied twice")
            raw = self.get_starttag_text()
            end = start + len(raw) - (2 if raw.endswith("/>") else 1)
            parents = tuple(value for _, ids in self._stack for value in ids)
            self.links.append(_Link(start, end, attrs["href"] or "", parents))
        if push and tag not in _VOID:
            self._stack.append((tag, identifiers))

    def handle_starttag(self, tag, attrs):
        self._start(tag, attrs, push=True)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs, push=False)

    def handle_endtag(self, tag):
        for index in range(len(self._stack) - 1, -1, -1):
            if self._stack[index][0] == tag:
                del self._stack[index:]
                break


def _kind(page, link, targets):
    address = urlsplit(link.href)
    current = _PAGE_ROOT + page
    if address.scheme or address.netloc:
        if (
            address.scheme not in {"http", "https"}
            or address.hostname != _SITE_HOST
            or not address.path.startswith(_SITE_ROOT)
        ):
            return "external"
        destination = address.path
    else:
        destination = (
            posixpath.normpath(posixpath.join(posixpath.dirname(current), address.path))
            if address.path
            else current
        )
    if unquote(destination) != current or address.query or "#" not in link.href:
        return "page"
    identifier = unquote(address.fragment)
    if not identifier:
        return "up"
    target = targets.get(identifier)
    if target is None or identifier in link.containers or target == link.start:
        # Keep the existing down cue when no earlier destination is established.
        return "down"
    return "up" if target < link.start else "down"


def stylesheet():
    """The one authored stylesheet, copied for publication or embedded offline."""
    comment = "/* " + provenance.generated_html_comment(__file__) + " */"
    source = Path(__file__).with_suffix(".css").read_text(encoding="utf-8")
    return comment + "\n" + source


def apply(document, page, *, css_href=None):
    """Decorate a freshly rendered page; omit css_href for an offline export."""
    scan = _Scan(document)
    edits = [
        (link.insertion, f' data-na-link="{_kind(page, link, scan.targets)}"')
        for link in scan.links
    ]
    if document.count("</head>") != 1:
        raise ValueError(f"Near-Aleppo HTML requires one head element: {page}")
    style = (
        f'<link rel="stylesheet" href="{escape(css_href, quote=True)}">\n'
        if css_href is not None
        else f"<style>\n{stylesheet()}</style>\n"
    )
    edits.append((document.index("</head>"), style))
    for position, addition in sorted(edits, reverse=True):
        document = document[:position] + addition + document[position:]
    return document
