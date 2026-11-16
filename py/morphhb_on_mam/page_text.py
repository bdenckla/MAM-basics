"""The visible text of the study's page, for reading and checking.

Written by Claude (Opus 5.5) on 2026-11-15 for build_page.py, and moved into this package on
2026-11-16, when the study was put on ice (morphhb-on-mam/README.md).  visible_text(page)
returns what a reader of the page sees, as plain lines: a heading begins with one "#" per
level, a list item with "- " or its number, a caption with "Table: ", a table row is its
cells joined by " | ", a line break inside a cell is " / ", and code is in backticks.  The
head, the style and any script are left out.  Runs of white space, no-break spaces among
them, become one space.
"""

from html.parser import HTMLParser

BLOCKS = {
    "body",
    "div",
    "html",
    "nav",
    "ol",
    "p",
    "section",
    "table",
    "tbody",
    "thead",
    "ul",
}
HEADINGS = {"h1": 1, "h2": 2, "h3": 3, "h4": 4}


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines = []
        self.cur = []
        self.skip = 0
        self.cells = None
        self.cell = None
        self.lists = []

    def _put(self, s):
        (self.cell if self.cell is not None else self.cur).append(s)

    def _flush(self):
        text = " ".join("".join(self.cur).split())
        if text:
            self.lines.append(text)
        self.cur = []

    def handle_starttag(self, tag, attrs):
        if tag in ("head", "style", "script"):
            self.skip += 1
            return
        if self.skip:
            return
        if tag == "tr":
            self._flush()
            self.cells = []
        elif tag in ("td", "th"):
            self.cell = []
        elif tag == "br":
            if self.cell is not None:
                self.cell.append(" / ")
            else:
                self._flush()
        elif tag == "code":
            self._put("`")
        elif tag in HEADINGS:
            self._flush()
            self._put("#" * HEADINGS[tag] + " ")
        elif tag == "caption":
            self._flush()
            self._put("Table: ")
        elif tag == "li":
            self._flush()
            if self.lists and self.lists[-1] is not None:
                self.lists[-1] += 1
                self._put("%d. " % self.lists[-1])
            else:
                self._put("- ")
        elif tag in ("ol", "ul"):
            self._flush()
            self.lists.append(0 if tag == "ol" else None)
        elif tag in BLOCKS:
            self._flush()

    def handle_endtag(self, tag):
        if tag in ("head", "style", "script"):
            self.skip -= 1
            return
        if self.skip:
            return
        if tag in ("td", "th"):
            self.cells.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr":
            # A row whose last cells are empty would end in spaces.
            self.lines.append(" | ".join(self.cells).rstrip())
            self.cells = None
        elif tag == "code":
            self._put("`")
        elif tag in ("ol", "ul"):
            self._flush()
            self.lists.pop()
        elif tag in HEADINGS or tag in ("caption", "li") or tag in BLOCKS:
            self._flush()

    def handle_data(self, data):
        if not self.skip:
            self._put(data)


def visible_text(page):
    """The visible text of an HTML page, one line per block, ending in a newline."""
    parser = _Text()
    parser.feed(page)
    parser.close()
    parser._flush()
    return "\n".join(parser.lines) + "\n"
