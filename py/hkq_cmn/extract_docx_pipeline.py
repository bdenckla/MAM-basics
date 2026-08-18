from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import cast
import zipfile
from xml.etree import ElementTree as ET

from mb_cmn.uni_denorm import give_std_mark_order
from mb_cmn.hebrew_punctuation import SOPA
from hkq_cmn.extract_docx_notes import (
    apply_notes_fixes,
    assert_text_columns_before_drop,
    notes_structured_signature_for_row,
    split_notes_components,
    strip_trailing_sof_pasuq_from_uxlc_qere,
    split_uxlc_pointed_prefix_atoms,
    standardize_verse_book_name,
    verse_book_name,
)
from hkq_cmn.extract_docx_xml_utils import (
    NS,
    cell_payload,
    export_images,
    intro_markdown,
    paragraph_text,
    slugify,
)
from hkq_cmn.json_io import write_json


@dataclass(frozen=True)
class ParsedExtract:
    intro_paragraphs: list[str]
    headers: list[object]
    column_keys: list[str]
    data_rows: list[dict[str, object]]
    finding_value_counts: list[dict[str, object]]
    notes_structured_counts: list[dict[str, object]]
    verse_book_names: list[str]


def parse_docx_archive(
    archive: zipfile.ZipFile, image_dir: Path, data_root: Path
) -> ParsedExtract:
    body, rel_map = _docx_body_and_relationships(archive)
    intro_paragraphs, table_element = _intro_and_table(body)
    table_rows = _table_rows(table_element, rel_map)
    if not table_rows:
        raise ValueError("table has no rows")

    header_row = table_rows[0]
    headers = [cell["text"] for cell in header_row]
    column_keys = [
        slugify(header if isinstance(header, str) else "") for header in headers
    ]

    data_rows, notes_signatures, leningrad_quote_count = _parse_data_rows(
        archive=archive,
        table_rows=table_rows,
        column_keys=column_keys,
        image_dir=image_dir,
        data_root=data_root,
    )
    _validate_leningrad_quote_count(leningrad_quote_count)

    verse_book_names = sorted({verse_book_name(str(row["verse"])) for row in data_rows})
    finding_value_counts = [
        {
            "finding": finding,
            "count": count,
        }
        for finding, count in sorted(
            Counter(str(row["finding"]) for row in data_rows).items()
        )
    ]
    notes_structured_counts = [
        {
            "notes-UXLC": notes_uxlc,
            "notes-UXLC-pointed-prefix-atoms": notes_uxlc_pointed_prefix_atoms,
            "notes-UXLC-yatir": notes_uxlc_yatir,
            "notes-HaKeter": notes_haketer,
            "count": count,
        }
        for (
            notes_uxlc,
            notes_uxlc_pointed_prefix_atoms,
            notes_uxlc_yatir,
            notes_haketer,
        ), count in sorted(
            Counter(notes_signatures).items(),
            key=lambda item: (-item[1], item[0]),
        )
    ]

    return ParsedExtract(
        intro_paragraphs=intro_paragraphs,
        headers=headers,
        column_keys=column_keys,
        data_rows=data_rows,
        finding_value_counts=finding_value_counts,
        notes_structured_counts=notes_structured_counts,
        verse_book_names=verse_book_names,
    )


def write_extract_files(
    nonserved_output_dir: Path,
    source_document: str,
    parsed: ParsedExtract,
) -> tuple[Path, Path]:
    nonserved_output_dir.mkdir(parents=True, exist_ok=True)
    intro_path = nonserved_output_dir / "introduction.md"
    intro_path.write_text(
        intro_markdown(parsed.intro_paragraphs), encoding="utf-8", newline=""
    )

    json_payload = {
        "source_document": source_document,
        "introduction_paragraph_count": len(parsed.intro_paragraphs),
        "table": {
            "header_labels": parsed.headers,
            "column_keys": parsed.column_keys,
            "row_count": len(parsed.data_rows),
            "finding_value_counts": parsed.finding_value_counts,
            "notes_structured_counts": parsed.notes_structured_counts,
            "verse_book_names": parsed.verse_book_names,
            "rows": parsed.data_rows,
        },
    }
    json_path = nonserved_output_dir / "table_data.json"
    write_json(json_path, json_payload)
    return intro_path, json_path


def _docx_body_and_relationships(
    archive: zipfile.ZipFile,
) -> tuple[ET.Element, dict[str, str]]:
    document = ET.fromstring(archive.read("word/document.xml"))
    relationships = ET.fromstring(archive.read("word/_rels/document.xml.rels"))

    rel_map = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in relationships
        if rel.tag.endswith("Relationship")
    }
    body = document.find("w:body", NS)
    if body is None:
        raise ValueError("document body not found")
    return body, rel_map


def _intro_and_table(body: ET.Element) -> tuple[list[str], ET.Element]:
    intro_paragraphs: list[str] = []
    table_element: ET.Element | None = None
    for child in body:
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p" and table_element is None:
            text = paragraph_text(child)
            if text:
                intro_paragraphs.append(text)
            continue
        if tag == "tbl":
            table_element = child
            break

    if table_element is None:
        raise ValueError("no table found in document")
    return intro_paragraphs, table_element


def _table_rows(
    table_element: ET.Element, rel_map: dict[str, str]
) -> list[list[dict[str, object]]]:
    table_rows = []
    for row in table_element.findall("./w:tr", NS):
        row_cells = []
        for cell in row.findall("./w:tc", NS):
            row_cells.append(cell_payload(cell, rel_map))
        table_rows.append(row_cells)
    return table_rows


def _parse_data_rows(
    archive: zipfile.ZipFile,
    table_rows: list[list[dict[str, object]]],
    column_keys: list[str],
    image_dir: Path,
    data_root: Path,
) -> tuple[
    list[dict[str, object]],
    list[tuple[str, str | None, str | None, str | None]],
    int,
]:
    data_rows = []
    notes_signatures: list[tuple[str, str | None, str | None, str | None]] = []
    leningrad_quote_count = 0

    for row_index, row in enumerate(table_rows[1:], start=1):
        ordered_row_data, notes_signature, quote_count_increment = _ordered_row_data(
            archive=archive,
            row_index=row_index,
            row=row,
            column_keys=column_keys,
            image_dir=image_dir,
            data_root=data_root,
        )
        data_rows.append(ordered_row_data)
        notes_signatures.append(notes_signature)
        leningrad_quote_count += quote_count_increment

    return data_rows, notes_signatures, leningrad_quote_count


def _ordered_row_data(
    archive: zipfile.ZipFile,
    row_index: int,
    row: list[dict[str, object]],
    column_keys: list[str],
    image_dir: Path,
    data_root: Path,
) -> tuple[dict[str, object], tuple[str, str | None, str | None, str | None], int]:
    row_data: dict[str, object] = {
        "row_number": row_index,
    }
    image_refs: dict[str, list[str]] = {}

    for column_index, key in enumerate(column_keys):
        if column_index >= len(row):
            row_data[key] = ""
            continue

        payload = row[column_index]
        text = payload["text"]
        row_data[key] = text

        targets_obj = payload["image_targets"]
        if not isinstance(targets_obj, list):
            raise ValueError(
                f"unexpected image target payload type at row {row_index}: {targets_obj!r}"
            )
        targets = cast(list[str], targets_obj)
        if targets:
            image_refs[key] = export_images(
                archive=archive,
                row_number=row_index,
                column_key=key,
                targets=targets,
                image_dir=image_dir,
                data_root=data_root,
            )

    if image_refs:
        row_data["image_files"] = image_refs

    _strip_trailing_sof_pasuq_from_word(row_data)
    _normalize_word_to_mam_mark_order(row_data)
    quote_count_increment = assert_text_columns_before_drop(row_data)
    apply_notes_fixes(row_data)

    verse_text = row_data.get("verse")
    if not isinstance(verse_text, str):
        raise ValueError(f"unexpected verse type at row {row_index}: {verse_text!r}")
    row_data["verse"] = standardize_verse_book_name(verse_text)

    notes = str(row_data["notes"])
    word = str(row_data["word"])
    notes_uxlc, notes_uxlc_yatir, notes_haketer = split_notes_components(notes)
    notes_uxlc, notes_uxlc_pointed_prefix_atoms = split_uxlc_pointed_prefix_atoms(
        notes_uxlc=notes_uxlc,
        mam_word=word,
    )
    notes_uxlc, notes_uxlc_orig = strip_trailing_sof_pasuq_from_uxlc_qere(notes_uxlc)

    # Preserve column order and place notes-* exactly where notes used to be.
    ordered_row_data: dict[str, object] = {
        "row_number": row_data["row_number"],
    }
    for key in column_keys:
        if key in {"entry", "aleppo", "leningrad"}:
            continue
        if key == "word":
            ordered_row_data[key] = row_data[key]
            if "word_orig" in row_data:
                ordered_row_data["word_orig"] = row_data["word_orig"]
            continue
        if key == "notes":
            ordered_row_data["notes-UXLC"] = notes_uxlc
            if notes_uxlc_orig is not None:
                ordered_row_data["notes-UXLC_orig"] = notes_uxlc_orig
            if notes_uxlc_pointed_prefix_atoms is not None:
                ordered_row_data["notes-UXLC-pointed-prefix-atoms"] = (
                    notes_uxlc_pointed_prefix_atoms
                )
            ordered_row_data["notes-UXLC-yatir"] = notes_uxlc_yatir
            ordered_row_data["notes-HaKeter"] = notes_haketer
            continue
        ordered_row_data[key] = row_data[key]

    if "image_files" in row_data:
        ordered_row_data["image_files"] = row_data["image_files"]
    if "notes_orig" in row_data:
        ordered_row_data["notes_orig"] = row_data["notes_orig"]

    return (
        ordered_row_data,
        notes_structured_signature_for_row(notes=notes, mam_word=word),
        quote_count_increment,
    )


def _strip_trailing_sof_pasuq_from_word(row_data: dict[str, object]) -> None:
    word = row_data.get("word")
    if not isinstance(word, str) or not word.endswith(SOPA):
        return

    row_data["word_orig"] = word
    row_data["word"] = word.removesuffix(SOPA)


def _normalize_word_to_mam_mark_order(row_data: dict[str, object]) -> None:
    word = row_data.get("word")
    if not isinstance(word, str):
        return
    row_data["word"] = give_std_mark_order(word)


def _validate_leningrad_quote_count(leningrad_quote_count: int) -> None:
    if leningrad_quote_count > 1:
        raise ValueError(
            "unexpected multiple non-empty leningrad text values; expected at most one "
            f"meaningless quote marker, found {leningrad_quote_count}"
        )
