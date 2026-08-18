"""Wrap the Hebrew inside a line of Holman's prose for right-to-left display.

Holman's field values mix English with pointed Hebrew: "Add note regarding
Mereka OR change Meteg to Mereka (וַיֵּהָ֥פְכ֛וּ)." Each Hebrew stretch is put in
its own ``dir="rtl"`` element so the browser lays it out as Hebrew and the
English around it as English.

The unit is the whitespace-delimited token. A token holding any Hebrew letter
contributes a Hebrew element running from its first Hebrew-block character to
its last, so an enclosing paren or a trailing full stop stays outside and is not
mirrored, and anything between those two stays inside. Adjacent Hebrew tokens
separated by one space become one element, keeping a phrase such as
וַיַּעַזְבוּ שָׁ֖ם in a single right-to-left run.

Nothing here has to cope with a bidi control: ``uxlc_email_extract`` drops the
one Latin note letter a message embeds mid-word, controls and all, and raises
on any control it does not recognize, so a value reaching this module has none.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape

from py_render.rt_render_utils import HEBREW_CHAR_RANGES


@dataclass(frozen=True)
class TextSegment:
    text: str
    is_hebrew: bool


def inline_text_html(value: str) -> str:
    """Escape a line of prose, marking its Hebrew for right-to-left display."""
    return "".join(
        (
            f'<bdi class="pointed-heb" lang="he" dir="rtl">'
            f"{escape(segment.text)}</bdi>"
            if segment.is_hebrew
            else escape(segment.text)
        )
        for segment in split_hebrew_runs(value)
    )


def split_hebrew_runs(value: str) -> tuple[TextSegment, ...]:
    segments: list[TextSegment] = []
    for token in _tokens_with_gaps(value):
        if not _has_hebrew(token):
            _append(segments, TextSegment(token, is_hebrew=False))
            continue
        first = next(i for i, char in enumerate(token) if _is_hebrew(char))
        last = max(i for i, char in enumerate(token) if _is_hebrew(char))
        _append(segments, TextSegment(token[:first], is_hebrew=False))
        _append(segments, TextSegment(token[first : last + 1], is_hebrew=True))
        _append(segments, TextSegment(token[last + 1 :], is_hebrew=False))
    return _merge_hebrew_across_single_spaces(segments)


def _tokens_with_gaps(value: str) -> list[str]:
    """Split into runs of non-space and runs of space, keeping both."""
    tokens: list[str] = []
    current = ""
    current_is_space: bool | None = None
    for char in value:
        char_is_space = char.isspace()
        if current_is_space is None or char_is_space == current_is_space:
            current += char
            current_is_space = char_is_space
            continue
        tokens.append(current)
        current = char
        current_is_space = char_is_space
    if current:
        tokens.append(current)
    return tokens


def _append(segments: list[TextSegment], segment: TextSegment) -> None:
    if not segment.text:
        return
    if segments and segments[-1].is_hebrew == segment.is_hebrew:
        segments[-1] = TextSegment(
            segments[-1].text + segment.text, is_hebrew=segment.is_hebrew
        )
        return
    segments.append(segment)


def _merge_hebrew_across_single_spaces(
    segments: list[TextSegment],
) -> tuple[TextSegment, ...]:
    merged: list[TextSegment] = []
    index = 0
    while index < len(segments):
        segment = segments[index]
        index += 1
        if not segment.is_hebrew:
            merged.append(segment)
            continue
        text = segment.text
        while (
            index + 1 < len(segments)
            and segments[index].text == " "
            and segments[index + 1].is_hebrew
        ):
            text = f"{text} {segments[index + 1].text}"
            index += 2
        merged.append(TextSegment(text, is_hebrew=True))
    return tuple(merged)


def _is_hebrew(char: str) -> bool:
    return any(start <= char <= end for start, end in HEBREW_CHAR_RANGES)


def _has_hebrew(text: str) -> bool:
    return any(_is_hebrew(char) for char in text)
