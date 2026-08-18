"""The filter column above the cards, by book.

There were two others. Filtering by source email did what the book column
already did, a message being one book's worth of cases; the messages themselves
are still listed, in the page's Source emails section. Filtering by what Holman
asks for -- a change to the text, an apparatus note, or both -- went on
2026-08-11 at Ben's request, and the classification behind it went with it.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from html import escape

from mb_cmn import bib_locales as tbn
from py_render.uc_case_card import book_filter_id
from hkq_cmn.uxlc_email_extract import CorrectionCase
from hkq_cmn.uxlc_external_links import book_display_name


@dataclass(frozen=True)
class FilterRow:
    filter_id: str
    label: str
    count: int


def summary_html(cases: list[CorrectionCase]) -> str:
    return (
        '<div class="summary-columns">\n'
        + _group_html("Book", _book_rows(cases))
        + "\n</div>"
    )


def all_filter_ids(cases: list[CorrectionCase]) -> list[str]:
    return [row.filter_id for row in _book_rows(cases)]


def _book_rows(cases: list[CorrectionCase]) -> list[FilterRow]:
    counts = Counter(case.ref.book for case in cases)
    return [
        FilterRow(book_filter_id(book), book_display_name(book), counts[book])
        for book in sorted(counts, key=tbn.get_bknu)
    ]


def _group_html(title: str, rows: list[FilterRow]) -> str:
    row_html = "\n".join(
        (
            f'<tr data-filter-id="{escape(row.filter_id)}">\n'
            f'<td><span class="cat-swatch cat-{escape(row.filter_id)}"></span>'
            f"{escape(row.label)}</td>\n"
            f"<td>{row.count}</td>\n"
            "</tr>"
        )
        for row in rows
    )
    return (
        '<section class="summary-group">\n'
        f'<h2 class="summary-group-title">{escape(title)}</h2>\n'
        f'<table class="summary">\n{row_html}\n</table>\n'
        "</section>"
    )
