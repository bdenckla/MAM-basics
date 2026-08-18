"""Render the hand-authored commentary entries filed under a case.

The entry shape is documented in ``uxlc_comments/all_comments.py``, which is the
file a contributor edits. Everything here is presentation.
"""

from __future__ import annotations

from html import escape

from py_render.uc_hebrew_runs import inline_text_html
from uxlc_comments.comment_parts import Raw


def comments_html(entries: tuple[dict[str, object], ...]) -> str:
    if not entries:
        return ""
    rendered = "\n".join(_entry_html(entry) for entry in entries)
    return f'<section class="commentary">\n{rendered}\n</section>'


def _entry_html(entry: dict[str, object]) -> str:
    for required in ("author", "date", "body"):
        if required not in entry:
            raise ValueError(f"comment entry is missing {required!r}: {entry!r}")
    author = str(entry["author"])
    date = str(entry["date"])
    paragraphs = "\n".join(
        f"<p>{_paragraph_html(paragraph)}</p>"
        for paragraph in _as_paragraphs(entry["body"])
    )
    return (
        '<article class="comment">\n'
        f'<p class="comment-byline">{escape(author)}, {escape(date)}</p>\n'
        f"{paragraphs}\n"
        "</article>"
    )


def _as_paragraphs(body: object) -> tuple[object, ...]:
    if isinstance(body, str):
        return (body,)
    if isinstance(body, (list, tuple)):
        return tuple(body)
    raise ValueError(f"comment body must be a string or a sequence: {body!r}")


def _paragraph_html(paragraph: object) -> str:
    if isinstance(paragraph, str):
        return inline_text_html(paragraph)
    if isinstance(paragraph, (list, tuple)):
        return "".join(_part_html(part) for part in paragraph)
    raise ValueError(f"comment paragraph must be a string or a sequence: {paragraph!r}")


def _part_html(part: object) -> str:
    if isinstance(part, Raw):
        return part.html
    if isinstance(part, str):
        return inline_text_html(part)
    raise ValueError(f"comment part must be a string or a raw(...): {part!r}")
