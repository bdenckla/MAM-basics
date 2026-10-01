"""Independent display projection reading only the frozen public HTML.

This is a migration oracle, not the production exporter. It deliberately has no
private paths, source-record readers, or source-derived exception dictionaries.
Its whole candidate output supplies the constructive comparison for release
review; equivalence of a renderer alone cannot establish the publication boundary.
"""

from html.parser import HTMLParser
from pathlib import Path

from mb_cmn import bib_locales
from phonetic_mam import display_schema as schema


class _Chapter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.verses = []
        self.number = 1
        self.rows = None
        self.row = None
        self.cell = None
        self.inline = []
        self.heading = False
        self.heading_text = ""

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        schema.require(len(attr) == len(attrs), "duplicate HTML attribute")
        if tag == "h2":
            schema.require(
                not self.inline and self.rows is None, "nested verse heading"
            )
            self.number += 1
            schema.require(
                attr == {"class": "verse-number", "id": f"v{self.number}"},
                "unexpected verse heading",
            )
            self.heading = True
            self.heading_text = ""
        elif tag == "table":
            schema.require(not attrs and self.rows is None, "unexpected table")
            self.rows = []
        elif tag == "tr":
            schema.require(
                not attrs and self.rows is not None and self.row is None,
                "unexpected row",
            )
            self.row = []
        elif tag == "td":
            schema.require(
                self.row is not None and self.cell is None, "unexpected cell"
            )
            schema.require(
                attr in ({}, {"dir": "rtl", "lang": "hbo"}), "unknown cell attributes"
            )
            self.cell = {"hebrew": bool(attr), "content": []}
        elif self.cell is not None:
            if tag == "sup" and not attrs:
                node = {"kind": "superscript-e", "content": []}
            elif tag == "span" and attr == {"class": "jt-stressed"}:
                node = {"kind": "stressed", "content": []}
            elif tag == "span" and attr == {"class": "mam-implicit-maqaf"}:
                node = {"kind": "implicit-maqaf", "content": []}
            elif (
                tag == "span"
                and set(attr) == {"title"}
                and attr["title"] in schema.READING_LABELS
            ):
                node = {"kind": "reading", "label": attr["title"], "content": []}
            else:
                raise schema.PublicReleaseError(f"unknown inline HTML: {tag}, {attrs}")
            self._content().append(node)
            self.inline.append((tag, node))
        else:
            schema.require(
                tag in {"html", "head", "meta", "title", "link", "body"},
                f"unknown outer HTML: {tag}",
            )

    def _content(self):
        return self.inline[-1][1]["content"] if self.inline else self.cell["content"]

    def handle_data(self, data):
        if self.cell is not None:
            data = data.replace("\n", " ")
            if not data:
                return
            content = self._content()
            if content and isinstance(content[-1], str):
                content[-1] += data
            else:
                content.append(data)
        elif self.heading:
            self.heading_text += data

    def handle_endtag(self, tag):
        if self.inline:
            current_tag, node = self.inline.pop()
            schema.require(current_tag == tag, "unbalanced inline HTML")
            if node["kind"] == "superscript-e":
                schema.require(node.pop("content") == ["e"], "unknown superscript")
            elif node["kind"] == "implicit-maqaf":
                schema.require(
                    node.pop("content") == ["\N{HEBREW PUNCTUATION MAQAF}"],
                    "unknown implicit maqaf",
                )
        elif tag == "td":
            schema.require(self.cell is not None, "unmatched cell end")
            self.row.append(self.cell)
            self.cell = None
        elif tag == "tr":
            schema.require(self.row is not None, "unmatched row end")
            self.rows.append(self.row)
            self.row = None
        elif tag == "table":
            schema.require(bool(self.rows), "missing or empty table")
            self.verses.append((self.number, self.rows))
            self.rows = None
        elif tag == "h2":
            schema.require(
                self.heading_text == str(self.number), "verse heading identity"
            )
            self.heading = False
        else:
            schema.require(
                tag in {"html", "head", "title", "body"},
                f"unknown outer closing HTML: {tag}",
            )


def _read_chapter(path):
    parser = _Chapter()
    parser.feed(Path(path).read_text(encoding="utf-8"))
    parser.close()
    schema.require(
        parser.rows is None and parser.cell is None and not parser.inline,
        "unclosed chapter HTML",
    )
    schema.require(bool(parser.verses), "empty chapter projection")
    return parser.verses


def _split_columns(rows):
    h_count = max(
        index + 1 for row in rows for index, cell in enumerate(row) if cell["hebrew"]
    )
    total = len(rows[0])
    schema.require(all(len(row) == total for row in rows), "nonrectangular verse table")
    for row in rows:
        for index, cell in enumerate(row):
            if cell["content"]:
                schema.require(
                    cell["hebrew"] == (index < h_count),
                    "mixed Hebrew/transcription columns",
                )
    return h_count, total - h_count


def project_chapter(sephardic_path, ashkenazic_path):
    """Extract paired cells; refuse any disagreement in shared public structure."""
    first, second = _read_chapter(sephardic_path), _read_chapter(ashkenazic_path)
    schema.require(len(first) == len(second), "pronunciation verse count differs")
    verses = []
    for (number, arows), (other_number, brows) in zip(first, second):
        schema.require(
            number == other_number and len(arows) == len(brows),
            "pronunciation verse/row sequence differs",
        )
        h_count, a_count = _split_columns(arows)
        other_h_count, b_count = _split_columns(brows)
        schema.require(
            h_count == other_h_count,
            "pronunciation Hebrew table layout differs",
        )
        rows = []
        for ar, br in zip(arows, brows):
            schema.require(
                ar[:h_count] == br[:h_count], "pronunciation Hebrew projection differs"
            )
            rows.append(
                {
                    "hebrew": [c["content"] or None for c in ar[:h_count]],
                    "transcriptions": {
                        "sephardic": [c["content"] or None for c in ar[h_count:]],
                        "ashkenazic": [c["content"] or None for c in br[h_count:]],
                    },
                }
            )
        verses.append(
            {
                "number": number,
                "hebrew_columns": h_count,
                "transcription_columns": {"sephardic": a_count, "ashkenazic": b_count},
                "rows": rows,
            }
        )
    return verses


def project_book(pages_root, book):
    """Read one entire canonical book from the two sanctioned path families."""
    schema.require(book in bib_locales.ALL_BK39_IDS, "unknown book")
    suffix = bib_locales.ordered_short_dash_full_39(book)
    first = Path(pages_root) / "tnkh" / suffix
    second = Path(pages_root) / "tnkh-ashkenaz" / suffix
    chapters = sorted(first.glob("*.html"), key=lambda path: int(path.stem))
    schema.require(bool(chapters), f"missing chapter corpus: {first}")
    schema.require(
        {p.name for p in chapters} == {p.name for p in second.glob("*.html")},
        "pronunciation chapter path set differs",
    )
    book_data = {
        "schema": schema.SCHEMA_ID,
        "book": book,
        "chapters": [
            {
                "number": int(path.stem),
                "verses": project_chapter(path, second / path.name),
            }
            for path in chapters
        ],
    }
    return schema.validate_book(book_data)
