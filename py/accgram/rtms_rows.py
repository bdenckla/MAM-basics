from __future__ import annotations

import json
from pathlib import Path

from accgram import rtms_ref

ParsedRow = tuple[dict[str, object], str, str]


def read_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as f_in:
        return json.load(f_in)


def parse_ref(ref: str, *, row_kind: str = "troublemaker") -> tuple[str, int, int]:
    return rtms_ref.parse_ref(ref, row_kind=row_kind)


def to_compact_bcv(bb: str, chnu: int, vrnu: int) -> str:
    return rtms_ref.to_compact_bcv(bb, chnu, vrnu)


def to_ref(bb: str, chnu: int, vrnu: int) -> str:
    return rtms_ref.to_ref(bb, chnu, vrnu)


def parse_ungrammatical_rows(
    ungrammatical_in_path: Path,
    refs_by_book: dict[str, set[tuple[int, int]]],
) -> list[ParsedRow]:
    return _parse_rows(
        in_path=ungrammatical_in_path,
        payload_key="oddballs",
        row_kind="ungrammatical",
        invalid_payload_message=(
            f"Expected list at ungrammatical payload key 'ungrammatical': {ungrammatical_in_path}"
        ),
        row_object_message="Ungrammatical rows must be JSON objects",
        missing_ref_message="Ungrammatical row is missing string field 'ref'",
        refs_by_book=refs_by_book,
    )


def _parse_rows(
    *,
    in_path: Path,
    payload_key: str,
    row_kind: str,
    invalid_payload_message: str,
    row_object_message: str,
    missing_ref_message: str,
    refs_by_book: dict[str, set[tuple[int, int]]],
) -> list[ParsedRow]:
    payload = read_json(in_path)
    rows = payload.get(payload_key) if isinstance(payload, dict) else None
    if not isinstance(rows, list):
        raise ValueError(invalid_payload_message)

    parsed_rows: list[ParsedRow] = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError(row_object_message)
        ref_value = row.get("ref")
        if not isinstance(ref_value, str):
            raise ValueError(missing_ref_message)

        bb, chnu, vrnu = parse_ref(ref_value, row_kind=row_kind)
        bcv = to_compact_bcv(bb, chnu, vrnu)
        ref = to_ref(bb, chnu, vrnu)
        refs_by_book.setdefault(bb, set()).add((chnu, vrnu))
        parsed_rows.append((row, bcv, ref))

    return parsed_rows
