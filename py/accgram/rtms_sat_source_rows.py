from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class SatSourceRow:
    key: str
    value: str
    origin_value: object
    description_key: str | None


StructuredTextLookup = Callable[[dict[str, object], str], object]
RenderSatValue = Callable[[object], str]


def build_wlc_focus_source_row(wlc_focus: object) -> SatSourceRow:
    normalized_value = (
        _normalize_whitespace(wlc_focus) if isinstance(wlc_focus, str) else ""
    )
    return SatSourceRow(
        key="wlc_focus",
        value=normalized_value,
        origin_value=normalized_value,
        description_key="wlc",
    )


def normalize_diff_source_rows(
    label: str,
    diff_value: object,
    *,
    row: dict[str, object],
    rhs_key: str,
    description_key: str | None,
    render_sat_value: RenderSatValue,
    structured_text_lookup: StructuredTextLookup,
) -> list[SatSourceRow]:
    entries = _as_nonempty_list(diff_value)
    rows: list[SatSourceRow] = []
    for idx, entry in enumerate(entries, start=1):
        row_label = label if len(entries) == 1 else f"{label}[{idx}]"
        rendered_value, origin_value = _render_diff_entry_value_and_origin(
            entry,
            row=row,
            rhs_key=rhs_key,
            render_sat_value=render_sat_value,
            structured_text_lookup=structured_text_lookup,
        )
        rows.append(
            SatSourceRow(
                key=row_label,
                value=rendered_value,
                origin_value=origin_value,
                description_key=description_key,
            )
        )
    return rows


def _render_diff_entry_value_and_origin(
    entry: object,
    *,
    row: dict[str, object],
    rhs_key: str,
    render_sat_value: RenderSatValue,
    structured_text_lookup: StructuredTextLookup,
) -> tuple[str, object]:
    if not isinstance(entry, dict):
        return render_sat_value(entry), entry

    if "wlc422" not in entry or rhs_key not in entry:
        return render_sat_value(entry), entry

    wlc_focus = structured_text_lookup(row, "wlc_focus")
    if not isinstance(wlc_focus, str):
        return render_sat_value(entry), entry

    wlc_side = render_sat_value(entry.get("wlc422"))
    rhs_side = render_sat_value(entry.get(rhs_key))
    if wlc_side == wlc_focus:
        return rhs_side, entry.get(rhs_key)

    return render_sat_value(entry), entry


def _as_nonempty_list(value: object) -> list[object]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if item is not None]
    return [value]


def _normalize_whitespace(value: str | None) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.split())
