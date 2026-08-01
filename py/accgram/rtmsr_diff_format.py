from __future__ import annotations

from typing import Callable


def contains_hebrew(text: str) -> bool:
    return any("\u0590" <= char <= "\u05ff" for char in text)


def is_plain_hebrew_string(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False

    for char in stripped:
        if char.isspace():
            continue
        if "\u0590" <= char <= "\u05ff":
            continue
        return False

    return True


def normalize_diff_rows(
    label: str,
    diff_value: object,
    *,
    row: dict[str, object],
    rhs_key: str,
    render_sat_value: Callable[[object], str],
    structured_text_lookup: Callable[[dict[str, object], str], object],
) -> list[tuple[str, str]]:
    entries = _as_nonempty_list(diff_value)
    rows: list[tuple[str, str]] = []
    for idx, entry in enumerate(entries, start=1):
        row_label = label if len(entries) == 1 else f"{label}[{idx}]"

        rows.append(
            (
                row_label,
                _render_diff_entry_value(
                    entry,
                    row=row,
                    rhs_key=rhs_key,
                    render_sat_value=render_sat_value,
                    structured_text_lookup=structured_text_lookup,
                ),
            )
        )
    return rows


def _render_diff_entry_value(
    entry: object,
    *,
    row: dict[str, object],
    rhs_key: str,
    render_sat_value: Callable[[object], str],
    structured_text_lookup: Callable[[dict[str, object], str], object],
) -> str:
    if not isinstance(entry, dict):
        return render_sat_value(entry)

    if "wlc422" not in entry or rhs_key not in entry:
        return render_sat_value(entry)

    wlc_focus = structured_text_lookup(row, "wlc_focus")
    if not isinstance(wlc_focus, str):
        return render_sat_value(entry)

    wlc_side = render_sat_value(entry.get("wlc422"))
    rhs_side = render_sat_value(entry.get(rhs_key))
    if wlc_side == wlc_focus:
        return rhs_side

    return render_sat_value(entry)


def _as_nonempty_list(value: object) -> list[object]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if item is not None]
    return [value]
