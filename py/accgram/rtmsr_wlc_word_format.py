from __future__ import annotations

from typing import Callable


def collect_wlc_word_bracket_notes(
    tokens: list[object],
    wlc_focus: str | None,
    *,
    render_sat_value: Callable[[object], str],
) -> list[str]:
    if not wlc_focus:
        return []

    notes: list[str] = []
    for token in tokens:
        if not isinstance(token, dict):
            continue
        if token.get("word") != wlc_focus:
            continue
        token_notes = token.get("notes")
        if token_notes is None:
            continue
        rendered_notes = render_sat_value(token_notes).strip()
        if rendered_notes:
            notes.append(rendered_notes)

    # Preserve order while dropping duplicates.
    return list(dict.fromkeys(notes))


def render_note_values(values: list[str]) -> str:
    if not values:
        return ""
    if len(values) == 1:
        return values[0]
    return f"[{' | '.join(values)}]"


def is_redundant_wlc_word_bracket_notes_row(
    bracket_notes: list[str],
    *,
    wlc_focus: str | None,
    wlc_focus_notes: list[str],
) -> bool:
    if not wlc_focus or not wlc_focus_notes:
        return False

    wlc_focus_bracket_notes = {f"{wlc_focus}: {note}" for note in wlc_focus_notes}
    return bool(bracket_notes) and set(bracket_notes).issubset(wlc_focus_bracket_notes)
