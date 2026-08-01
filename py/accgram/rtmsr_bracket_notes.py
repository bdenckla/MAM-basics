from __future__ import annotations

import re

from wlc_cmn.wlc_bracket_note_definitions import SOURCE_MANUAL422
from wlc_cmn.wlc_bracket_note_definitions import bracket_note_definition
from py_html import wlc_utils_html

_BRACKET_NOTE_CODE_RE = re.compile(r"\][0-9A-Za-z]")
WLC_BRACKET_NOTES_ANCHOR_ID = "wlc-bracket-notes"
WLC_BRACKET_NOTES_HEADING = "WLC Bracket Notes"
_WLC_BRACKET_NOTES_SECTION_INTRO = (
    "The following bracket-note codes are used on this page."
)


def _bracket_notes_heading() -> object:
    return wlc_utils_html.heading_level_2(
        WLC_BRACKET_NOTES_HEADING, {"id": WLC_BRACKET_NOTES_ANCHOR_ID}
    )


def build_wlc_bracket_notes_section(
    enriched_rows: list[dict[str, object]],
) -> tuple[object, ...]:
    codes = sorted(_collect_page_bracket_note_codes(enriched_rows))
    if not codes:
        return (
            _bracket_notes_heading(),
            wlc_utils_html.para("No bracket-note tokens detected on this page."),
        )

    list_items = []
    for code in codes:
        list_items.append(
            (
                wlc_utils_html.code(code),
                ": ",
                manual422_definition_for_code(code),
            )
        )

    return (
        _bracket_notes_heading(),
        wlc_utils_html.para(_WLC_BRACKET_NOTES_SECTION_INTRO),
        wlc_utils_html.unordered_list(tuple(list_items)),
    )


def annotate_bracket_note_tokens(value_text: str) -> object:
    matches = list(_BRACKET_NOTE_CODE_RE.finditer(value_text))
    if not matches:
        return value_text

    pieces: list[object] = []
    cursor = 0
    for match in matches:
        start, end = match.span()
        if start > cursor:
            pieces.append(value_text[cursor:start])

        code = match.group(0)
        pieces.append(
            wlc_utils_html.span(
                code,
                {"title": manual422_definition_for_code(code)},
            )
        )
        cursor = end

    if cursor < len(value_text):
        pieces.append(value_text[cursor:])

    if len(pieces) == 1:
        return pieces[0]
    return tuple(pieces)


def parse_bracket_note_codes(note_text: str) -> list[str]:
    compact_codes = [
        match.group(0) for match in _BRACKET_NOTE_CODE_RE.finditer(note_text)
    ]
    return list(dict.fromkeys(compact_codes))


def manual422_definition_for_code(code: str) -> str:
    definition = bracket_note_definition(code, SOURCE_MANUAL422)
    if isinstance(definition, str) and definition.strip():
        return definition.strip()
    return f"No manual422 definition available for {code}."


def _collect_page_bracket_note_codes(
    enriched_rows: list[dict[str, object]],
) -> list[str]:
    page_codes: list[str] = []
    for row in enriched_rows:
        _append_bracket_note_codes_from_value(row, out_codes=page_codes)

    # Preserve first-seen order before optional downstream ordering.
    return list(dict.fromkeys(page_codes))


def _append_bracket_note_codes_from_value(
    value: object, *, out_codes: list[str]
) -> None:
    if isinstance(value, str):
        out_codes.extend(parse_bracket_note_codes(value))
        return

    if isinstance(value, list):
        for item in value:
            _append_bracket_note_codes_from_value(item, out_codes=out_codes)
        return

    if isinstance(value, dict):
        for nested_value in value.values():
            _append_bracket_note_codes_from_value(nested_value, out_codes=out_codes)
