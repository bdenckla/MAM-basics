"""Read the one table of a Miqra Mevoar Word file by a closed dispatch over its XML.

A .docx file is a zip of XML parts. This reads word/document.xml and word/styles.xml
with the standard library. At every level, the body, the table, its rows, cells,
paragraphs and runs, each element is either one this module names or an error, so a
file laid out in a way the converter has not seen stops it rather than being guessed
at. Joshua's file also has a table of contents after its table, which is read past.
"""

import zipfile
from xml.etree import ElementTree

_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def read_rows(docx_path):
    """Each row of the file's one table: its cells, each a list of (style, text)."""
    name = docx_path.name
    with zipfile.ZipFile(docx_path) as zf:
        style_names = _style_names(ElementTree.fromstring(zf.read("word/styles.xml")))
        document = ElementTree.fromstring(zf.read("word/document.xml"))
    tables = []
    for child in document.find(f"{_W}body"):
        tag = _local(child.tag)
        if tag == "tbl":
            tables.append(child)
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
    rows = []
    for child in tables[0]:
        tag = _local(child.tag)
        if tag == "tr":
            rows.append(_row_cells(child, style_names, name))
        elif tag not in _TABLE_SKIP:
            raise ValueError(f"{name}: unknown table element {tag}")
    return rows


def _row_cells(row, style_names, name):
    cells = []
    for child in row:
        tag = _local(child.tag)
        if tag == "tc":
            cells.append(_cell_paragraphs(child, style_names, name))
        elif tag not in _ROW_SKIP:
            raise ValueError(f"{name}: unknown row element {tag}")
    return cells


def _cell_paragraphs(cell, style_names, name):
    paragraphs = []
    for child in cell:
        tag = _local(child.tag)
        if tag == "p":
            paragraphs.append(
                (_para_style(child, style_names, name), _para_text(child, name))
            )
        elif tag not in _CELL_SKIP:
            raise ValueError(f"{name}: unknown cell element {tag}")
    return paragraphs


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
    out = []
    for child in para:
        tag = _local(child.tag)
        if tag == "r":
            out.append(_run_text(child, name))
        elif tag in _PARA_CONTAINERS:
            out.append(_para_text(child, name))
        elif tag not in _PARA_SKIP:
            raise ValueError(f"{name}: unknown paragraph element {tag}")
    return "".join(out)


def _run_text(run, name):
    out = []
    for child in run:
        tag = _local(child.tag)
        if tag == "t":
            out.append(child.text or "")
        elif tag in _RUN_TEXT:
            out.append(_RUN_TEXT[tag])
        elif tag not in _RUN_SKIP:
            raise ValueError(f"{name}: unknown run element {tag}")
    return "".join(out)


def _require_table_of_contents(sdt, name):
    """Read past a body-level content control only if Word built it as a table of contents."""
    gallery = sdt.find(f"{_W}sdtPr/{_W}docPartObj/{_W}docPartGallery")
    kind = None if gallery is None else gallery.get(f"{_W}val")
    if kind != "Table of Contents":
        raise ValueError(
            f"{name}: a content control outside the table, of kind {kind!r}"
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
