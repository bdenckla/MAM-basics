from __future__ import annotations

from collections.abc import Callable

from accgram import rtms_focus_highlight
from accgram import rtmsr_sat
from py_html import wlc_utils_html

_GOERWITZ_TMS_VERSE_CLASS = "goerwitz-tms-verse"
_GOERWITZ_TMS_FOCUS_HIGHLIGHT_CLASS = "goerwitz-tms-focus-highlight"
_GOERWITZ_TMS_READING_LABEL_CLASS = "goerwitz-tms-reading-label"
_GOERWITZ_TMS_CONTEXT_CLASS = "goerwitz-tms-context"

StructuredTextLookup = Callable[[dict[str, object], str], object]


def render_dual_cant_reading_paragraphs(
    readings: list[dict[str, object]],
    *,
    focus_bcv: str | None = None,
) -> tuple[object, ...]:
    """For a dually-cantillated verse, one labelled Hebrew line per reading (issue #36),
    replacing the combined WLC verse line (e.g. taxton + elyon)."""
    paragraphs: list[object] = []
    for reading in readings:
        label = reading.get("display_label")
        span = reading.get("span_label")
        contents = _dual_cant_verse_contents(
            words=reading.get("words"),
            word_bcvs=reading.get("word_bcvs"),
            focus_bcv=focus_bcv,
        )
        label_text = str(label) if isinstance(label, str) else ""
        if isinstance(span, str) and span:
            label_text = f"{label_text} ({span})"
        paragraphs.append(
            wlc_utils_html.para(
                label_text,
                {"class": _GOERWITZ_TMS_READING_LABEL_CLASS},
            )
        )
        paragraphs.append(
            wlc_utils_html.para(
                contents,
                {
                    "class": _GOERWITZ_TMS_VERSE_CLASS,
                    "lang": "hbo",
                    "dir": "rtl",
                },
            )
        )
    return tuple(paragraphs)


def _dual_cant_verse_contents(
    *, words: object, word_bcvs: object, focus_bcv: str | None
) -> object:
    """The verse-line contents for one reading: a plain space-joined string, or — when a
    focus verse and a parallel per-word bcv list are available — a sequence in which each
    run of words from a numbered verse other than ``focus_bcv`` is wrapped in a gray
    context span (issue #36).

    An elyon chanted verse groups several numbered verses, so on the dt 5:8 row its 5:7 /
    5:9 / 5:10 words become context and only the 5:8 part stays in normal color.  Runs of
    same-emphasis words are coalesced into one span and single spaces are interleaved
    between runs, so the visible spacing is identical to the plain join."""
    if not isinstance(words, list):
        return ""
    nonempty = [(i, w) for i, w in enumerate(words) if w]
    plain = " ".join(w for _, w in nonempty)
    if not focus_bcv or not isinstance(word_bcvs, list) or len(word_bcvs) != len(words):
        return plain

    pieces: list[object] = []
    run_words: list[str] = []
    run_is_context = False

    def flush() -> None:
        if not run_words:
            return
        text = " ".join(run_words)
        if run_is_context:
            pieces.append(
                wlc_utils_html.span(text, {"class": _GOERWITZ_TMS_CONTEXT_CLASS})
            )
        else:
            pieces.append(text)
        run_words.clear()

    for i, word in nonempty:
        is_context = word_bcvs[i] != focus_bcv
        if run_words and is_context != run_is_context:
            flush()
        run_is_context = is_context
        run_words.append(word)
    flush()

    if not pieces:
        return ""
    if len(pieces) == 1 and isinstance(pieces[0], str):
        return pieces[0]
    spaced: list[object] = []
    for idx, piece in enumerate(pieces):
        if idx:
            spaced.append(" ")
        spaced.append(piece)
    return tuple(spaced)


def render_wlc_verse_paragraph(
    row: dict[str, object],
    *,
    structured_text_lookup: StructuredTextLookup,
) -> object:
    verse_text = _wlc_verse_text(row)
    wlc_focus = structured_text_lookup(row, "wlc_focus")
    wlc_focus_str = wlc_focus if isinstance(wlc_focus, str) else None
    contents = _wlc_verse_contents_with_highlight(
        verse_text=verse_text,
        wlc_focus=wlc_focus_str,
    )
    return wlc_utils_html.para(
        contents,
        {
            "class": _GOERWITZ_TMS_VERSE_CLASS,
            "lang": "hbo",
            "dir": "rtl",
        },
    )


def wlc_verse_vels(row: dict[str, object]) -> list[object]:
    wlc_verse = row.get("wlc422_kq_u_verse")
    if not isinstance(wlc_verse, dict):
        return []
    vels = wlc_verse.get("vels")
    if not isinstance(vels, list):
        return []
    return vels


def _wlc_verse_contents_with_highlight(
    *, verse_text: str, wlc_focus: str | None
) -> object:
    normalized_focus = _normalize_whitespace(wlc_focus)
    if not normalized_focus:
        return verse_text

    before_focus, focus_text, after_focus = _split_unique_focus_by_tokens(
        verse_text=verse_text,
        wlc_focus=normalized_focus,
    )
    if focus_text is None:
        return verse_text

    contents: list[object] = []
    if before_focus:
        contents.append(f"{before_focus} ")
    contents.append(
        wlc_utils_html.span(
            focus_text,
            {"class": _GOERWITZ_TMS_FOCUS_HIGHLIGHT_CLASS},
        )
    )
    if after_focus:
        contents.append(f" {after_focus}")

    if len(contents) == 1:
        return contents[0]
    return tuple(contents)


def _split_unique_focus_by_tokens(
    *, verse_text: str, wlc_focus: str
) -> tuple[str, str | None, str]:
    return rtms_focus_highlight.split_unique_focus_by_tokens(
        verse_text=verse_text,
        wlc_focus=wlc_focus,
    )


def _normalize_whitespace(value: str | None) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.split())


def _wlc_verse_text(row: dict[str, object]) -> str:
    tokens = wlc_verse_vels(row)
    text_parts = [_token_text(token) for token in tokens]
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

    return rtmsr_sat.render_sat_value(token)
