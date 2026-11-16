"""Read the one table of a Miqra Mevoar Word file by a closed dispatch over its XML.

A .docx file is a zip of XML parts. This reads word/document.xml and word/styles.xml
with the standard library. At every level, the body, the table, its rows, cells,
paragraphs and runs, each element is either one this module names or an error, so a
file laid out in a way the converter has not seen stops it rather than being guessed
at. Three things that hold none of the book's text are read past:

- A picture in a table cell: a drawing whose graphic data is one picture and which
  holds no text, as Judges and Zephaniah have. read_table gives each one's row and
  cell, so that the converter can name it. Any other drawing, such as a text box, and a
  picture anywhere but a table cell, are errors.
- A table of contents that Word built as a content control, as Joshua's file has after
  its table.
- A table of contents that Word built as a field after the table, as Daniel's file has:
  empty paragraphs, and paragraphs styled "toc" with a level, within one field whose
  instruction is TOC, with the PAGEREF fields nested in it, and nothing else. A field
  character or a field instruction anywhere else is an error.
"""

import dataclasses
import re
import zipfile
from xml.etree import ElementTree

_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
_PIC = "{http://schemas.openxmlformats.org/drawingml/2006/picture}"


@dataclasses.dataclass(frozen=True)
class Picture:
    """A picture read past in the table: the index of its row and of its cell, from 0."""

    row: int
    cell: int


@dataclasses.dataclass(frozen=True)
class Table:
    """The file's one table: each row's cells, each a list of (style, text), and the
    pictures read past in its cells, in the table's order."""

    rows: list
    pictures: list


def read_table(docx_path):
    """The file's one table: its rows and the pictures read past in its cells."""
    name = docx_path.name
    with zipfile.ZipFile(docx_path) as zf:
        style_names = _style_names(ElementTree.fromstring(zf.read("word/styles.xml")))
        document = ElementTree.fromstring(zf.read("word/document.xml"))
    tables, after_table = [], []
    for child in document.find(f"{_W}body"):
        tag = _local(child.tag)
        if tag == "tbl":
            tables.append(child)
        elif tag == "p" and tables:
            after_table.append(child)
        elif tag == "p":
            text = _para_text(child, name)
            if text.strip():
                raise ValueError(f"{name}: text outside the table: {text!r}")
        elif tag == "sdt":
            _require_table_of_contents(child, name)
        elif tag != "sectPr":
            raise ValueError(f"{name}: unknown body element {tag}")
    if len(tables) != 1:
        raise ValueError(f"{name}: expected one table, found {len(tables)}")
    _read_past_contents_field(after_table, style_names, name)
    rows, pictures = [], []
    for child in tables[0]:
        tag = _local(child.tag)
        if tag == "tr":
            cells = []
            for at, (paragraphs, count) in enumerate(
                _row_cells(child, style_names, name)
            ):
                cells.append(paragraphs)
                pictures.extend(Picture(len(rows), at) for _ in range(count))
            rows.append(cells)
        elif tag not in _TABLE_SKIP:
            raise ValueError(f"{name}: unknown table element {tag}")
    return Table(rows, pictures)


def _row_cells(row, style_names, name):
    """Each cell of a row: its paragraphs, and how many pictures were read past in it."""
    cells = []
    for child in row:
        tag = _local(child.tag)
        if tag == "tc":
            cells.append(_cell_paragraphs(child, style_names, name))
        elif tag not in _ROW_SKIP:
            raise ValueError(f"{name}: unknown row element {tag}")
    return cells


def _cell_paragraphs(cell, style_names, name):
    paragraphs, pictures = [], 0
    for child in cell:
        tag = _local(child.tag)
        if tag == "p":
            text = []
            for kind, value in _para_items(child, name):
                if kind == _TEXT:
                    text.append(value)
                elif kind == _PICTURE:
                    pictures += 1
                else:
                    raise ValueError(f"{name}: a {kind} in a table cell: {value!r}")
            paragraphs.append((_para_style(child, style_names, name), "".join(text)))
        elif tag not in _CELL_SKIP:
            raise ValueError(f"{name}: unknown cell element {tag}")
    return paragraphs, pictures


def _para_style(para, style_names, name):
    """The name of a paragraph's style, or "" for the default style."""
    style = para.find(f"{_W}pPr/{_W}pStyle")
    if style is None:
        return ""
    style_id = style.get(f"{_W}val")
    if style_id not in style_names:
        raise ValueError(f"{name}: paragraph style {style_id!r} is not in styles.xml")
    return style_names[style_id]


def _para_text(para, name):
    """The text of a paragraph before the table, where a picture or a field is an error."""
    out = []
    for kind, value in _para_items(para, name):
        if kind != _TEXT:
            raise ValueError(f"{name}: a {kind} before the table: {value!r}")
        out.append(value)
    return "".join(out)


def _para_items(para, name):
    """A paragraph's items in order, each (kind, value): text, a picture read past, a
    field character, or a field instruction. Whether each kind may stand where it
    stands is the caller's to decide."""
    for child in para:
        tag = _local(child.tag)
        if tag == "r":
            yield from _run_items(child, name)
        elif tag in _PARA_CONTAINERS:
            yield from _para_items(child, name)
        elif tag not in _PARA_SKIP:
            raise ValueError(f"{name}: unknown paragraph element {tag}")


def _run_items(run, name):
    for child in run:
        tag = _local(child.tag)
        if tag == "t":
            yield _TEXT, child.text or ""
        elif tag in _RUN_TEXT:
            yield _TEXT, _RUN_TEXT[tag]
        elif tag == "drawing":
            _require_picture(child, name)
            yield _PICTURE, None
        elif tag == "fldChar":
            yield _FIELD_CHAR, child.get(f"{_W}fldCharType")
        elif tag == "instrText":
            yield _INSTRUCTION, child.text or ""
        elif tag not in _RUN_SKIP:
            raise ValueError(f"{name}: unknown run element {tag}")


def _require_picture(drawing, name):
    """Raise unless a drawing is one picture, inline or anchored, that holds no text."""
    frames = list(drawing)
    if len(frames) != 1 or frames[0].tag not in _PICTURE_FRAMES:
        raise ValueError(f"{name}: a drawing that is not one inline or anchored frame")
    graphics = [child for child in frames[0] if child.tag == f"{_A}graphic"]
    data = list(graphics[0]) if len(graphics) == 1 else []
    if (
        len(data) != 1
        or data[0].tag != f"{_A}graphicData"
        or data[0].get("uri") != _PICTURE_URI
        or [child.tag for child in data[0]] != [f"{_PIC}pic"]
    ):
        raise ValueError(f"{name}: a drawing whose graphic data is not one picture")
    for node in frames[0].iter():
        local = node.tag.rpartition("}")[2]
        if node.tag.startswith(_W) or local in _TEXT_HOLDERS:
            raise ValueError(f"{name}: a picture that holds text, in its {local}")


def _require_table_of_contents(sdt, name):
    """Read past a body-level content control only if Word built it as a table of contents."""
    gallery = sdt.find(f"{_W}sdtPr/{_W}docPartObj/{_W}docPartGallery")
    kind = None if gallery is None else gallery.get(f"{_W}val")
    if kind != "Table of Contents":
        raise ValueError(
            f"{name}: a content control outside the table, of kind {kind!r}"
        )


def _read_past_contents_field(paragraphs, style_names, name):
    """Read past the body's paragraphs after the table: each is empty, or a paragraph
    of the one table of contents that Word may build there as a field."""
    field = _ContentsField(name)
    for para in paragraphs:
        style = _para_style(para, style_names, name)
        for kind, value in _para_items(para, name):
            if kind == _TEXT:
                field.text(value, style)
            elif kind == _FIELD_CHAR:
                field.char(value)
            elif kind == _INSTRUCTION:
                field.instruction(value)
            else:
                raise ValueError(f"{name}: a {kind} after the table")
    field.finish()


class _ContentsField:
    """The one table of contents that Word may build as a field after the table.

    The field's instruction is TOC, and each field nested in its result is a PAGEREF
    field, with none nested in that. Text stands only in a field's result, and only in
    a paragraph styled "toc" with a level; any other text after the table is an error.
    """

    def __init__(self, name):
        self._name = name
        # The open fields, outermost first, each [its instruction's parts, separated].
        self._open = []
        self._begun = False

    def char(self, kind):
        """A field character: a field's begin, its separator or its end."""
        if kind == "begin":
            self._begin()
        elif kind == "separate":
            self._require_open("a field separator")
            if self._open[-1][1]:
                raise ValueError(f"{self._name}: a field with two separators")
            self._require_instruction()
            self._open[-1][1] = True
        elif kind == "end":
            self._require_open("a field's end")
            if not self._open[-1][1]:
                self._require_instruction()
            self._open.pop()
        else:
            raise ValueError(f"{self._name}: a field character {kind!r}")

    def instruction(self, text):
        """A part of the instruction of the innermost field, before its separator."""
        if not self._open or self._open[-1][1]:
            raise ValueError(
                f"{self._name}: a field instruction outside a field's instruction:"
                f" {text!r}"
            )
        self._open[-1][0].append(text)

    def text(self, text, style):
        """Text after the table, in a paragraph of this style."""
        if not text.strip():
            return
        if not self._open:
            raise ValueError(f"{self._name}: text outside the table: {text!r}")
        if not self._open[-1][1]:
            raise ValueError(f"{self._name}: text in a field's instruction: {text!r}")
        if not _CONTENTS_STYLE.fullmatch(style):
            raise ValueError(
                f"{self._name}: text of a table of contents styled {style!r}: {text!r}"
            )

    def finish(self):
        """Raise if a field is still open at the end of the body."""
        if self._open:
            raise ValueError(f"{self._name}: a field after the table has no end")

    def _begin(self):
        if not self._open:
            if self._begun:
                raise ValueError(f"{self._name}: a second field after the table")
            self._begun = True
        elif len(self._open) == len(_FIELD_INSTRUCTIONS):
            raise ValueError(f"{self._name}: a field nested in a page reference")
        elif not self._open[-1][1]:
            raise ValueError(f"{self._name}: a field nested in a field's instruction")
        self._open.append([[], False])

    def _require_open(self, what):
        if not self._open:
            raise ValueError(f"{self._name}: {what} outside a field")

    def _require_instruction(self):
        words = "".join(self._open[-1][0]).split()
        expected = _FIELD_INSTRUCTIONS[len(self._open) - 1]
        if not words or words[0] != expected:
            raise ValueError(
                f"{self._name}: a field after the table whose instruction is"
                f" {' '.join(words)!r}, not {expected}"
            )


def _style_names(styles):
    return {
        style.get(f"{_W}styleId"): style.find(f"{_W}name").get(f"{_W}val")
        for style in styles.iter(f"{_W}style")
    }


def _local(tag):
    if not tag.startswith(_W):
        raise ValueError(f"an element outside WordprocessingML's namespace: {tag}")
    return tag[len(_W) :]


# The kinds of a paragraph's items.
_TEXT = "text"
_PICTURE = "picture"
_FIELD_CHAR = "field character"
_INSTRUCTION = "field instruction"
# Elements that carry layout or bookkeeping and no text.
_TABLE_SKIP = frozenset({"tblPr", "tblGrid"})
_ROW_SKIP = frozenset({"trPr"})
_CELL_SKIP = frozenset({"tcPr"})
_PARA_SKIP = frozenset(
    {
        "pPr",
        "bookmarkStart",
        "bookmarkEnd",
        "proofErr",
        "commentRangeStart",
        "commentRangeEnd",
        "permStart",
        "permEnd",
        # A tracked deletion, whose text is not the document's.
        "del",
    }
)
_RUN_SKIP = frozenset({"rPr", "lastRenderedPageBreak", "softHyphen"})
# Paragraph elements whose runs are the paragraph's text, a tracked insertion's
# included.
_PARA_CONTAINERS = frozenset({"hyperlink", "ins", "smartTag", "customXml", "fldSimple"})
# Run elements that stand for characters. A line break or a tab in a heading or a
# paraphrase is rejected by extract.py.
_RUN_TEXT = {
    "tab": "\t",
    "br": "\n",
    "cr": "\n",
    "noBreakHyphen": "\N{NON-BREAKING HYPHEN}",
}
# A picture's frame, inline or anchored, and its graphic data's kind.
_PICTURE_FRAMES = frozenset({f"{_WP}inline", f"{_WP}anchor"})
_PICTURE_URI = "http://schemas.openxmlformats.org/drawingml/2006/picture"
# The local names of the elements that hold a drawing's text: WordprocessingML's and
# DrawingML's text, a text box and a shape's text body.
_TEXT_HOLDERS = frozenset({"t", "txbx", "txbxContent", "txBody"})
# The fields after the table: a table of contents, and the page references in it.
_FIELD_INSTRUCTIONS = ("TOC", "PAGEREF")
_CONTENTS_STYLE = re.compile("toc [1-9]")
