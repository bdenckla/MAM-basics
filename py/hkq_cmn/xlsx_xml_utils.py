"""Read a .xlsx the way ``extract_docx_xml_utils`` reads a .docx: zipfile plus ElementTree.

WHY THERE IS NO THIRD-PARTY DEPENDENCY HERE.  ``openpyxl`` would do this in fewer
lines, and this repo's venv does not have it.  The precedent that settled the
question is beside this file: the ketiv/qere review's DOCX is read with the
standard library alone, and adding a spreadsheet dependency for two messages'
worth of cells would be the only such dependency in the tree.

WHAT THE CALLER ACTUALLY NEEDS FROM A HOLMAN SPREADSHEET, and why the drawing
half of this module exists.  Holman's two Jerusalem Crown messages carry their cases in an
attached workbook rather than in the message body, and carry the page crops
*inside that workbook* rather than as message attachments.  So neither half of
the shape ``uxlc_email_extract`` expects is present: ``_png_attachments`` walking
the message for image parts returns nothing, and the images that do exist are
named ``image1.png``..``image4.png``, which says nothing about which case each
belongs to.  The correspondence is recoverable only from the drawing anchors --
each picture declares the cell it is anchored to, and that cell's row is its
case's row.  ``anchored_image_targets_by_row`` below is that resolution, and it
is the reason this module reads drawings at all rather than stopping at cells.

Both readers are fail-fast in the same way the rest of ``hkq_cmn`` is: a part
that is absent where the caller asked for it raises rather than yielding an
empty result, because an empty result here is indistinguishable from a message
whose shape changed.
"""

from __future__ import annotations

from pathlib import Path
import posixpath
import re
import zipfile
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "xdr": "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
}

CELL_REF_PATTERN = re.compile(r"^(?P<column>[A-Z]+)(?P<row>[0-9]+)$")


def _qname(prefix: str, tag: str) -> str:
    return f"{{{NS[prefix]}}}{tag}"


def shared_strings(archive: zipfile.ZipFile) -> list[str]:
    """The workbook's shared-string table, in index order.

    A workbook with no string cells has no such part at all, which is legitimate
    and yields an empty table -- distinct from a part that is present and
    unreadable, which raises out of ``ET.fromstring``.
    """
    try:
        raw = archive.read("xl/sharedStrings.xml")
    except KeyError:
        return []

    root = ET.fromstring(raw)
    return [
        "".join(node.text or "" for node in item.iter(_qname("s", "t")))
        for item in root.findall(_qname("s", "si"))
    ]


def parse_cell_ref(ref: str) -> tuple[str, int]:
    """Split an A1-style reference into its column letters and 1-based row number."""
    match = CELL_REF_PATTERN.fullmatch(ref)
    if match is None:
        raise ValueError(f"unexpected cell reference: {ref!r}")
    return match.group("column"), int(match.group("row"))


def sheet_cells(
    archive: zipfile.ZipFile,
    sheet_part: str,
    strings: list[str],
) -> dict[tuple[int, str], str]:
    """Every non-empty cell of one worksheet, keyed by (row number, column letters).

    Numeric and inline-string cells are read as their literal text; a shared-string
    cell is resolved through ``strings``.  An index outside that table raises rather
    than yielding a blank, since a blank is what an unrelated bug would also produce.
    """
    root = ET.fromstring(archive.read(sheet_part))
    cells: dict[tuple[int, str], str] = {}

    for cell in root.iter(_qname("s", "c")):
        ref = cell.get("r")
        if ref is None:
            raise ValueError(f"cell with no reference in {sheet_part}")
        column, row_number = parse_cell_ref(ref)
        cell_type = cell.get("t")

        if cell_type == "inlineStr":
            text = "".join(node.text or "" for node in cell.iter(_qname("s", "t")))
        else:
            value = cell.find(_qname("s", "v"))
            if value is None:
                continue
            if cell_type == "s":
                index = int(value.text or "")
                if not 0 <= index < len(strings):
                    raise ValueError(
                        f"shared-string index {index} out of range in {sheet_part}"
                    )
                text = strings[index]
            else:
                text = value.text or ""

        if text != "":
            cells[(row_number, column)] = text

    return cells


def _relationship_targets(archive: zipfile.ZipFile, rels_part: str) -> dict[str, str]:
    root = ET.fromstring(archive.read(rels_part))
    targets: dict[str, str] = {}
    for relationship in root:
        rel_id = relationship.get("Id")
        target = relationship.get("Target")
        if rel_id is None or target is None:
            raise ValueError(f"relationship with no Id or Target in {rels_part}")
        targets[rel_id] = target
    return targets


def _resolve_relationship_target(source_part: str, target: str) -> str:
    """Resolve a relationship's target against its own part's directory.

    A relationship target is written relative to the part that declares it, and
    routinely climbs out of that directory: a worksheet's relationship to its
    drawing reads ``../drawings/drawing1.xml``.  ``posixpath.normpath`` is what
    collapses that, and zip member names are posix paths regardless of platform,
    so ``Path`` is deliberately not used here.
    """
    base = posixpath.dirname(source_part)
    return posixpath.normpath(posixpath.join(base, target))


def anchored_image_targets_by_row(
    archive: zipfile.ZipFile,
    drawing_part: str,
) -> dict[int, list[str]]:
    """Zip-member names of the pictures anchored to each 1-based worksheet row.

    THIS IS THE IMAGE-TO-CASE MAPPING, and it is the only thing in the workbook
    that carries it -- see the module docstring.  An anchor's ``<xdr:from>`` gives
    a 0-based row, which is returned 1-based so that it can be compared directly
    against ``sheet_cells``' keys.

    A picture with no resolvable image relationship raises: a workbook whose
    drawing references a part that is not there has changed shape, and silently
    dropping the picture would lose a case's crop without saying so.
    """
    rels_part = (
        f"{Path(drawing_part).parent.as_posix()}/_rels/{Path(drawing_part).name}.rels"
    )
    targets = _relationship_targets(archive, rels_part)

    by_row: dict[int, list[str]] = {}
    for anchor in ET.fromstring(archive.read(drawing_part)):
        from_node = anchor.find(_qname("xdr", "from"))
        if from_node is None:
            continue
        row_node = from_node.find(_qname("xdr", "row"))
        if row_node is None or row_node.text is None:
            raise ValueError(f"anchor with no row in {drawing_part}")
        row_number = int(row_node.text) + 1

        for blip in anchor.iter(_qname("a", "blip")):
            rel_id = blip.get(_qname("r", "embed"))
            if rel_id is None:
                continue
            target = targets.get(rel_id)
            if target is None:
                raise ValueError(
                    f"drawing {drawing_part} references unknown relationship {rel_id!r}"
                )
            by_row.setdefault(row_number, []).append(
                _resolve_relationship_target(drawing_part, target)
            )

    return by_row


def first_sheet_part(archive: zipfile.ZipFile) -> str:
    """The zip-member name of the workbook's first worksheet.

    Holman's two workbooks name their single sheet differently (``Sheet1`` in the
    earlier message, ``Sheet2`` in the later), so the sheet is chosen by position
    and never by name.  The part itself is ``sheet1.xml`` in both.
    """
    parts = sorted(
        name for name in archive.namelist() if name.startswith("xl/worksheets/sheet")
    )
    if not parts:
        raise ValueError("workbook has no worksheet part")
    return parts[0]


def drawing_part_for_sheet(archive: zipfile.ZipFile, sheet_part: str) -> str | None:
    """The drawing part a worksheet references, or None when it embeds no pictures."""
    rels_part = (
        f"{Path(sheet_part).parent.as_posix()}/_rels/{Path(sheet_part).name}.rels"
    )
    try:
        targets = _relationship_targets(archive, rels_part)
    except KeyError:
        return None

    for target in targets.values():
        if "drawing" in target:
            return _resolve_relationship_target(sheet_part, target)
    return None
