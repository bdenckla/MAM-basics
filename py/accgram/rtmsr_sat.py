from __future__ import annotations

import json
import string
from collections.abc import Callable

from accgram import rtms_sat_descriptions
from accgram import rtms_sat_source_rows
from accgram import rtmsr_bracket_notes
from accgram import rtmsr_diff_format
from accgram import rtmsr_sat_notes_column
from accgram import rtmsr_wlc_word_format
from accgram.rtms_sat_source_rows import SatSourceRow
from py_html import wlc_utils_html

_WLC_FOCUS_ROW_KEYS = {"wlc_focus"}
_SAT_ROW_SUPPRESSIONS_BY_REF: dict[str, set[str]] = {
    "1k 16:33": {"diff_wlc_uxlc[1]"},
    "1k 20:25": {"diff_wlc_mam[1]"},
    "2k 18:17": {"diff_wlc_mam[2]"},
    "2s 23:9": {"diff_wlc_mam[1]"},
    "ex 28:1": {"diff_wlc_mam[1]"},
    "gn 32:24": {"diff_wlc_mam[1]"},
    "je 44:17": {
        "diff_wlc_mam[2]"
    },  # secondary tsinnorit diff on השמים, unrelated to the telisha
    "js 4:8": {"diff_wlc_mam[2]"},
    "mi 2:7": {"diff_wlc_mam[2]"},
}

# Internal SAT row shape: (value_cell, middle_description_cell, key_cell).
SatRow = tuple[str, str, str]
StructuredTextLookup = Callable[[dict[str, object], str], object]


def render_sat_table(
    row: dict[str, object],
    *,
    row_ref: str,
    structured_text_lookup: StructuredTextLookup,
    wlc_tokens: list[object],
) -> object:
    sat_rows = _build_sat_rows(
        row,
        row_ref=row_ref,
        structured_text_lookup=structured_text_lookup,
        wlc_tokens=wlc_tokens,
    )

    notes_column_plan = rtmsr_sat_notes_column.build_sat_notes_column_plan(
        sat_rows,
        notes_by_key=_sat_notes_by_key(
            row,
            structured_text_lookup=structured_text_lookup,
            wlc_tokens=wlc_tokens,
        ),
    )

    table_rows: list[object] = []
    for value, notes_value, middle_description, key in notes_column_plan.render_rows:
        if notes_column_plan.include_notes_column:
            table_rows.append(
                wlc_utils_html.table_row_of_data(
                    (
                        rtmsr_bracket_notes.annotate_bracket_note_tokens(value),
                        rtmsr_bracket_notes.annotate_bracket_note_tokens(notes_value),
                        middle_description,
                        key,
                    ),
                    tdattrs=(
                        _sat_value_cell_attr(key, value),
                        rtmsr_sat_notes_column.notes_cell_attr(
                            notes_column_plan.include_notes_column
                        ),
                        None,
                        None,
                    ),
                )
            )
            continue

        table_rows.append(
            wlc_utils_html.table_row_of_data(
                (
                    rtmsr_bracket_notes.annotate_bracket_note_tokens(value),
                    middle_description,
                    key,
                ),
                tdattrs=(_sat_value_cell_attr(key, value), None, None),
            )
        )

    return wlc_utils_html.table(
        tuple(table_rows),
        {"class": "goerwitz-tms-sat"},
    )


def row_has_rendered_bracket_note(
    row: dict[str, object],
    *,
    row_ref: str,
    structured_text_lookup: StructuredTextLookup,
    wlc_tokens: list[object],
) -> bool:
    """True if this verse's rendered SAT table displays any bracket-note code.

    Mirrors render_sat_table's note sources exactly (the value cells, plus the
    notes column when it is shown), so the flag agrees with the visible
    bracket-note spans. A bracket note sitting on some other word of the verse,
    one the SAT table does not display, deliberately does not count."""
    sat_rows = _build_sat_rows(
        row,
        row_ref=row_ref,
        structured_text_lookup=structured_text_lookup,
        wlc_tokens=wlc_tokens,
    )
    notes_column_plan = rtmsr_sat_notes_column.build_sat_notes_column_plan(
        sat_rows,
        notes_by_key=_sat_notes_by_key(
            row,
            structured_text_lookup=structured_text_lookup,
            wlc_tokens=wlc_tokens,
        ),
    )
    for value, notes_value, _middle_description, _key in notes_column_plan.render_rows:
        if rtmsr_bracket_notes.parse_bracket_note_codes(value):
            return True
        if notes_column_plan.include_notes_column and (
            rtmsr_bracket_notes.parse_bracket_note_codes(notes_value)
        ):
            return True
    return False


def derive_summary_from_sat_descriptors(
    row: dict[str, object],
    *,
    row_ref: str,
    structured_text_lookup: StructuredTextLookup,
    wlc_tokens: list[object],
) -> str | None:
    sat_rows = _build_sat_rows(
        row,
        row_ref=row_ref,
        structured_text_lookup=structured_text_lookup,
        wlc_tokens=wlc_tokens,
    )

    observed_desc = _first_sat_row_description(sat_rows, key_equals="wlc_focus")
    expected_desc = _first_sat_row_description(sat_rows, key_prefix="diff_wlc_")
    if not observed_desc or not expected_desc:
        return None

    return (
        "Somewhere in the LC-BHS-WLC pipeline, "
        f"{observed_desc} appears rather than {expected_desc}."
    )


def render_summary_template_from_sat_descriptors(
    row: dict[str, object],
    *,
    row_ref: str,
    summary_template: str,
    structured_text_lookup: StructuredTextLookup,
    wlc_tokens: list[object],
) -> str:
    sat_rows = _build_sat_rows(
        row,
        row_ref=row_ref,
        structured_text_lookup=structured_text_lookup,
        wlc_tokens=wlc_tokens,
    )

    placeholders = _summary_template_placeholders(sat_rows)
    template = string.Template(summary_template)
    try:
        return template.substitute(placeholders)
    except KeyError as exc:
        missing_name = exc.args[0] if exc.args else str(exc)
        if not isinstance(missing_name, str):
            missing_name = str(missing_name)
        raise ValueError(
            "Ungrammatical st-summary template has unresolved placeholder "
            f"${missing_name} (ref={row_ref!r})."
        ) from exc
    except ValueError as exc:
        raise ValueError(
            f"Ungrammatical st-summary template is invalid (ref={row_ref!r}): {exc}"
        ) from exc


def _build_sat_rows(
    row: dict[str, object],
    *,
    row_ref: str,
    structured_text_lookup: StructuredTextLookup,
    wlc_tokens: list[object],
) -> list[SatRow]:
    wlc_focus_source_row = rtms_sat_source_rows.build_wlc_focus_source_row(
        structured_text_lookup(row, "wlc_focus")
    )
    wlc_focus_str = wlc_focus_source_row.value or None

    source_rows: list[SatSourceRow] = [wlc_focus_source_row]
    source_rows.extend(
        rtms_sat_source_rows.normalize_diff_source_rows(
            "diff_wlc_uxlc",
            row.get("diff_wlc_uxlc"),
            row=row,
            rhs_key="uxlc",
            description_key="uxlc",
            render_sat_value=render_sat_value,
            structured_text_lookup=structured_text_lookup,
        )
    )
    source_rows.extend(
        rtms_sat_source_rows.normalize_diff_source_rows(
            "diff_wlc_mam",
            row.get("diff_wlc_mam"),
            row=row,
            rhs_key="mam_simple",
            description_key="mam",
            render_sat_value=render_sat_value,
            structured_text_lookup=structured_text_lookup,
        )
    )

    sat_rows = [
        _sat_row_from_source(
            source_row=source_row,
            row=row,
            row_ref=row_ref,
            wlc_focus=wlc_focus_str,
        )
        for source_row in source_rows
    ]

    return _apply_sat_row_suppressions(row_ref, sat_rows)


def _sat_notes_by_key(
    row: dict[str, object],
    *,
    structured_text_lookup: StructuredTextLookup,
    wlc_tokens: list[object],
) -> dict[str, str]:
    wlc_focus_source_row = rtms_sat_source_rows.build_wlc_focus_source_row(
        structured_text_lookup(row, "wlc_focus")
    )
    wlc_focus_str = wlc_focus_source_row.value

    wlc_focus_notes = rtmsr_wlc_word_format.collect_wlc_word_bracket_notes(
        wlc_tokens,
        wlc_focus_str or None,
        render_sat_value=render_sat_value,
    )
    sat_notes_by_key: dict[str, str] = {}
    rendered_wlc_focus_notes = rtmsr_wlc_word_format.render_note_values(wlc_focus_notes)
    if rendered_wlc_focus_notes:
        sat_notes_by_key["wlc_focus"] = rendered_wlc_focus_notes
    return sat_notes_by_key


def _first_sat_row_description(
    sat_rows: list[SatRow],
    *,
    key_equals: str | None = None,
    key_prefix: str | None = None,
) -> str | None:
    for _value, middle_description, key in sat_rows:
        if key_equals is not None and key != key_equals:
            continue
        if key_prefix is not None and not key.startswith(key_prefix):
            continue
        normalized = middle_description.strip()
        if normalized:
            return normalized
    return None


def _summary_template_placeholders(sat_rows: list[SatRow]) -> dict[str, str]:
    placeholders: dict[str, str] = {}

    wlc_focus_desc = _first_sat_row_description(sat_rows, key_equals="wlc_focus")
    if wlc_focus_desc:
        placeholders["wlc_focus_desc"] = wlc_focus_desc

    diff_wlc_mam_desc = _first_sat_row_description(
        sat_rows,
        key_prefix="diff_wlc_mam",
    )
    if diff_wlc_mam_desc:
        placeholders["diff_wlc_mam_desc"] = diff_wlc_mam_desc

    diff_wlc_uxlc_desc = _first_sat_row_description(
        sat_rows,
        key_prefix="diff_wlc_uxlc",
    )
    if diff_wlc_uxlc_desc:
        placeholders["diff_wlc_uxlc_desc"] = diff_wlc_uxlc_desc

    diff_wlc_desc = _first_sat_row_description(sat_rows, key_prefix="diff_wlc_")
    if diff_wlc_desc:
        placeholders["diff_wlc_desc"] = diff_wlc_desc

    return placeholders


def render_sat_value(value: object) -> str:
    if isinstance(value, str):
        return value

    if value is None:
        return ""

    if isinstance(value, list):
        rendered_items = [render_sat_value(item) for item in value if item is not None]
        rendered_items = [item for item in rendered_items if item]
        if not rendered_items:
            return "[]"
        return f"[{' | '.join(rendered_items)}]"

    if isinstance(value, dict):
        token_like = _render_token_like_dict(value)
        if token_like is not None:
            return token_like

        parts = []
        for key, val in value.items():
            rendered = render_sat_value(val)
            parts.append(f"{key}: {rendered}" if rendered else str(key))
        return "; ".join(parts)

    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(value)


def _sat_row_from_source(
    *,
    source_row: SatSourceRow,
    row: dict[str, object],
    row_ref: str,
    wlc_focus: str | None,
) -> SatRow:
    value, middle_description = rtms_sat_descriptions.build_sat_value_and_description(
        source_row=source_row,
        enriched_row=row,
        row_ref=row_ref,
        wlc_focus=wlc_focus,
    )
    return _sat_row(
        key=source_row.key,
        value=value,
        middle_description=middle_description,
    )


def _sat_value_cell_attr(label: str, value: str) -> dict[str, str] | None:
    if label in _WLC_FOCUS_ROW_KEYS and rtmsr_diff_format.contains_hebrew(value):
        return {"lang": "hbo", "dir": "rtl"}

    if label.startswith("diff_wlc_") and rtmsr_diff_format.is_plain_hebrew_string(
        value
    ):
        return {"lang": "hbo", "dir": "rtl"}

    return None


def _apply_sat_row_suppressions(ref: str, rows: list[SatRow]) -> list[SatRow]:
    suppressed_labels = _SAT_ROW_SUPPRESSIONS_BY_REF.get(ref)
    if not suppressed_labels:
        return rows

    return [
        sat_row for sat_row in rows if _sat_row_key(sat_row) not in suppressed_labels
    ]


def _sat_row(*, key: str, value: str, middle_description: str = "") -> SatRow:
    return (value, middle_description, key)


def _sat_row_key(row: SatRow) -> str:
    return row[2]


def _render_token_like_dict(value: dict[str, object]) -> str | None:
    token_text: str | None = None
    if isinstance(value.get("word"), str):
        token_text = str(value["word"])
    elif isinstance(value.get("text"), str):
        token_text = str(value["text"])

    if token_text is None:
        return None

    note_key: str | None = None
    if "notes" in value:
        note_key = "notes"
    elif "note" in value:
        note_key = "note"

    out = token_text
    if note_key is not None:
        note_text = render_sat_value(value.get(note_key))
        if note_text:
            out = f"{out} ({note_key}: {note_text})"

    extras: list[str] = []
    for key, val in value.items():
        if key in {"word", "text", "notes", "note"}:
            continue
        rendered = render_sat_value(val)
        extras.append(f"{key}: {rendered}" if rendered else str(key))

    if extras:
        out = f"{out} ({'; '.join(extras)})"

    return out
