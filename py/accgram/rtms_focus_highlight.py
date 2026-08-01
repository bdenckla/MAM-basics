from __future__ import annotations


def split_unique_focus_by_tokens(
    *, verse_text: str, wlc_focus: str
) -> tuple[str, str | None, str]:
    normalized_verse = " ".join(verse_text.split())
    normalized_focus = _normalize_focus_for_match(wlc_focus)
    if not normalized_verse or not normalized_focus:
        return normalized_verse, None, ""

    verse_tokens = normalized_verse.split()
    focus_tokens = normalized_focus.split()
    if len(focus_tokens) > len(verse_tokens):
        return normalized_verse, None, ""

    match_indexes = _token_window_match_indexes(
        verse_tokens=verse_tokens,
        focus_tokens=focus_tokens,
    )
    if len(match_indexes) != 1:
        return normalized_verse, None, ""

    start = match_indexes[0]
    end = start + len(focus_tokens)
    before_focus = " ".join(verse_tokens[:start])
    focus_text = " ".join(verse_tokens[start:end])
    after_focus = " ".join(verse_tokens[end:])
    return before_focus, focus_text, after_focus


def validate_focus_highlightable(
    *,
    ref: str,
    wlc422_kq_u_verse: object,
    wlc_focus: str | None,
) -> None:
    if not wlc_focus:
        return

    verse_text = _normalized_wlc_verse_text_from_payload(wlc422_kq_u_verse)
    _, focus_text, _ = split_unique_focus_by_tokens(
        verse_text=verse_text,
        wlc_focus=wlc_focus,
    )
    if focus_text is not None:
        return

    normalized_focus = _normalize_focus_for_match(wlc_focus)
    normalized_verse = " ".join(verse_text.split())
    raise ValueError(
        "wlc_focus must match a unique token window in WLC verse text "
        f"for {ref}. Could not render highlight for wlc_focus={normalized_focus!r} "
        f"in verse_text={normalized_verse!r}."
    )


def _normalized_wlc_verse_text_from_payload(wlc422_kq_u_verse: object) -> str:
    if not isinstance(wlc422_kq_u_verse, dict):
        return ""

    vels = wlc422_kq_u_verse.get("vels")
    if not isinstance(vels, list):
        return ""

    text_parts = [_token_text(token) for token in vels]
    compact = " ".join(part for part in text_parts if part)
    return " ".join(compact.split())


def _token_text(token: object) -> str:
    if isinstance(token, str):
        return token

    if isinstance(token, dict):
        word = token.get("word")
        if isinstance(word, str):
            return word

        text = token.get("text")
        if isinstance(text, str):
            return text

    return ""


def _normalize_focus_for_match(wlc_focus: str) -> str:
    return " ".join(wlc_focus.split())


def _token_window_match_indexes(
    *, verse_tokens: list[str], focus_tokens: list[str]
) -> list[int]:
    if not verse_tokens or not focus_tokens:
        return []

    match_indexes: list[int] = []
    focus_len = len(focus_tokens)
    last_start = len(verse_tokens) - focus_len
    for start in range(last_start + 1):
        if verse_tokens[start : start + focus_len] == focus_tokens:
            match_indexes.append(start)
    return match_indexes
