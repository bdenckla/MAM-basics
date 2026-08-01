from __future__ import annotations

import re

from accgram import rtms_focus_highlight

_MAQAF = "־"


def structured_wlc_focus(structured_text: object) -> str | None:
    if not isinstance(structured_text, dict):
        return None

    wlc_focus = structured_text.get("wlc_focus")
    if not isinstance(wlc_focus, str):
        return None

    return wlc_focus.strip() or None


def normalized_wlc_verse_text_from_payload(wlc422_kq_u_verse: object) -> str:
    if not isinstance(wlc422_kq_u_verse, dict):
        return ""

    vels = wlc422_kq_u_verse.get("vels")
    if not isinstance(vels, list):
        return ""

    text_parts = [_token_text(token) for token in vels]
    compact = " ".join(part for part in text_parts if part)
    return " ".join(compact.split())


def count_focus_occurrences_in_verse_text(*, verse_text: str, wlc_focus: str) -> int:
    normalized_focus = _normalize_focus_for_match(wlc_focus)
    if not normalized_focus:
        return 0

    normalized_verse = " ".join(verse_text.split())
    if not normalized_verse:
        return 0

    pattern = _focus_occurrence_pattern(normalized_focus)
    return len(list(pattern.finditer(normalized_verse)))


def split_unique_focus_by_tokens(
    *, verse_text: str, wlc_focus: str
) -> tuple[str, str | None, str]:
    return rtms_focus_highlight.split_unique_focus_by_tokens(
        verse_text=verse_text,
        wlc_focus=wlc_focus,
    )


def validate_unique_focus_occurrence(
    *,
    ref: str,
    wlc422_kq_u_verse: object,
    wlc_focus: str | None,
) -> None:
    if not wlc_focus:
        return

    verse_text = normalized_wlc_verse_text_from_payload(wlc422_kq_u_verse)
    occurrences = count_focus_occurrences_in_verse_text(
        verse_text=verse_text,
        wlc_focus=wlc_focus,
    )
    if occurrences == 1:
        return

    normalized_focus = _normalize_focus_for_match(wlc_focus)
    raise ValueError(
        "wlc_focus must occur exactly once in WLC verse text "
        f"for {ref}. Found {occurrences} occurrences for wlc_focus={normalized_focus!r} "
        f"in verse_text={verse_text!r}. Expand wlc_focus with neighboring token(s) "
        "to make it unique."
    )


def validate_focus_highlightable(
    *,
    ref: str,
    wlc422_kq_u_verse: object,
    wlc_focus: str | None,
) -> None:
    return rtms_focus_highlight.validate_focus_highlightable(
        ref=ref,
        wlc422_kq_u_verse=wlc422_kq_u_verse,
        wlc_focus=wlc_focus,
    )


def expand_subset_diff_to_wlc_focus(
    diff_value: object,
    *,
    wlc_focus: str | None,
    rhs_key: str,
) -> object:
    if not wlc_focus:
        return diff_value

    if isinstance(diff_value, dict):
        return _expand_subset_diff_entry_to_wlc_focus(
            diff_value,
            wlc_focus=wlc_focus,
            rhs_key=rhs_key,
        )

    if isinstance(diff_value, list):
        return [
            _expand_subset_diff_entry_to_wlc_focus(
                entry,
                wlc_focus=wlc_focus,
                rhs_key=rhs_key,
            )
            for entry in diff_value
        ]

    return diff_value


def _expand_subset_diff_entry_to_wlc_focus(
    entry: object,
    *,
    wlc_focus: str,
    rhs_key: str,
) -> object:
    if not isinstance(entry, dict):
        return entry

    wlc_side = entry.get("wlc422")
    rhs_side = entry.get(rhs_key)
    if not isinstance(wlc_side, str) or not isinstance(rhs_side, str):
        return entry

    expanded_rhs = _replace_subset_words_in_focus(
        wlc_focus,
        subset_wlc=wlc_side,
        subset_rhs=rhs_side,
    )
    if expanded_rhs is None:
        return entry

    return {
        **entry,
        "wlc422": wlc_focus,
        rhs_key: expanded_rhs,
    }


def _replace_subset_words_in_focus(
    wlc_focus: str,
    *,
    subset_wlc: str,
    subset_rhs: str,
) -> str | None:
    focus_tokens = wlc_focus.split()
    subset_wlc_tokens = subset_wlc.split()
    subset_rhs_tokens = subset_rhs.split()
    if not focus_tokens or not subset_wlc_tokens or not subset_rhs_tokens:
        return None

    match_starts: list[int] = []
    match_len = len(subset_wlc_tokens)
    last_start = len(focus_tokens) - match_len
    for start in range(last_start + 1):
        if focus_tokens[start : start + match_len] == subset_wlc_tokens:
            match_starts.append(start)

    if len(match_starts) != 1:
        return None

    start = match_starts[0]
    end = start + match_len
    expanded_tokens = focus_tokens[:start] + subset_rhs_tokens + focus_tokens[end:]
    return " ".join(expanded_tokens)


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
    # Canonicalize whitespace while allowing optional spaces after maqaf in matching.
    return " ".join(wlc_focus.split())


def _focus_occurrence_pattern(normalized_focus: str) -> re.Pattern[str]:
    escaped_focus = re.escape(normalized_focus)
    escaped_focus = escaped_focus.replace(re.escape(_MAQAF), f"{_MAQAF}\\s*")
    escaped_focus = escaped_focus.replace(r"\ ", r"\s+")
    return re.compile(rf"(?<!\S){escaped_focus}(?!\S)")
