from __future__ import annotations

from dataclasses import dataclass

# Base SAT row shape before notes-column expansion: (value, middle_description, key).
SatRow = tuple[str, str, str]

# Expanded SAT row shape when rendering: (value, notes, middle_description, key).
SatRenderRow = tuple[str, str, str, str]


@dataclass(frozen=True)
class SatNotesColumnPlan:
    include_notes_column: bool
    render_rows: tuple[SatRenderRow, ...]


def build_sat_notes_column_plan(
    rows: list[SatRow],
    *,
    notes_by_key: dict[str, str] | None = None,
) -> SatNotesColumnPlan:
    notes_lookup = notes_by_key or {}
    include_notes_column = _should_include_notes_column(rows, notes_lookup)

    render_rows: list[SatRenderRow] = []
    for value, middle_description, key in rows:
        notes_value = notes_lookup.get(key, "") if include_notes_column else ""
        render_rows.append((value, notes_value, middle_description, key))

    return SatNotesColumnPlan(
        include_notes_column=include_notes_column,
        render_rows=tuple(render_rows),
    )


def notes_cell_attr(include_notes_column: bool) -> dict[str, str] | None:
    if not include_notes_column:
        return None
    return {"style": "text-align: right;"}


def _should_include_notes_column(
    rows: list[SatRow], notes_by_key: dict[str, str]
) -> bool:
    if not notes_by_key:
        return False

    for _value, _middle_description, key in rows:
        notes_value = notes_by_key.get(key)
        if isinstance(notes_value, str) and notes_value.strip():
            return True

    return False
