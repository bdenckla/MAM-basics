from __future__ import annotations

import html
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class GoerwitzTroublemakerSection:
    ref: str
    has_verse_paragraph: bool
    has_sat_table: bool
    verse_before_sat: bool
    sat_keys: tuple[str, ...]
    wlc_focus_values: tuple[str, ...]
    focus_highlights: tuple[str, ...]


def inspect_goerwitz_tms_html_contracts(
    html_text: str,
) -> list[GoerwitzTroublemakerSection]:
    sections: list[GoerwitzTroublemakerSection] = []
    matches = list(_SECTION_HEADING_RE.finditer(html_text))
    for idx, match in enumerate(matches):
        ref = _normalize_space(_strip_tags(match.group("ref")))
        section_start = match.end()
        section_end = (
            matches[idx + 1].start() if idx + 1 < len(matches) else len(html_text)
        )
        section_html = html_text[section_start:section_end]
        sections.append(_inspect_single_section(ref, section_html))
    return sections


def _inspect_single_section(ref: str, section_html: str) -> GoerwitzTroublemakerSection:
    verse_match = _VERSE_PARAGRAPH_RE.search(section_html)
    sat_match = _SAT_TABLE_RE.search(section_html)

    has_verse_paragraph = verse_match is not None
    has_sat_table = sat_match is not None
    verse_before_sat = bool(
        has_verse_paragraph
        and has_sat_table
        and verse_match.start() < sat_match.start()
    )

    sat_keys: list[str] = []
    wlc_focus_values: list[str] = []
    if sat_match is not None:
        sat_keys, wlc_focus_values = _extract_sat_keys_and_focus_values(
            sat_match.group("table")
        )

    focus_highlights: tuple[str, ...] = ()
    if verse_match is not None:
        focus_highlights = tuple(
            _normalize_space(_strip_tags(v))
            for v in _FOCUS_HIGHLIGHT_RE.findall(verse_match.group("verse"))
            if _normalize_space(_strip_tags(v))
        )

    return GoerwitzTroublemakerSection(
        ref=ref,
        has_verse_paragraph=has_verse_paragraph,
        has_sat_table=has_sat_table,
        verse_before_sat=verse_before_sat,
        sat_keys=tuple(sat_keys),
        wlc_focus_values=tuple(wlc_focus_values),
        focus_highlights=focus_highlights,
    )


def _extract_sat_keys_and_focus_values(
    sat_table_html: str,
) -> tuple[list[str], list[str]]:
    sat_keys: list[str] = []
    wlc_focus_values: list[str] = []
    for row_html in _TABLE_ROW_RE.findall(sat_table_html):
        td_cells = _TABLE_DATA_CELL_RE.findall(row_html)
        if len(td_cells) < 3:
            continue
        value = _normalize_space(_strip_tags(td_cells[0]))
        key = _normalize_space(_strip_tags(td_cells[-1]))
        if not key:
            continue
        sat_keys.append(key)
        if key == "wlc_focus":
            wlc_focus_values.append(value)
    return sat_keys, wlc_focus_values


def _strip_tags(text: str) -> str:
    without_tags = _HTML_TAG_RE.sub("", text)
    return html.unescape(without_tags)


def _normalize_space(text: str) -> str:
    return " ".join(text.split())


_SECTION_HEADING_RE = re.compile(
    r'<h2\s+id="tm[^"]+">(?P<ref>.*?)</h2>',
    re.IGNORECASE | re.DOTALL,
)
_VERSE_PARAGRAPH_RE = re.compile(
    r'<p\s+class="goerwitz-tms-verse"[^>]*>(?P<verse>.*?)</p>',
    re.IGNORECASE | re.DOTALL,
)
_SAT_TABLE_RE = re.compile(
    r'<table\s+class="goerwitz-tms-sat"[^>]*>(?P<table>.*?)</table>',
    re.IGNORECASE | re.DOTALL,
)
_FOCUS_HIGHLIGHT_RE = re.compile(
    r'<span\s+class="goerwitz-tms-focus-highlight"[^>]*>(.*?)</span>',
    re.IGNORECASE | re.DOTALL,
)
_TABLE_ROW_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.IGNORECASE | re.DOTALL)
_TABLE_DATA_CELL_RE = re.compile(
    r"<td[^>]*>(.*?)</td>",
    re.IGNORECASE | re.DOTALL,
)
_HTML_TAG_RE = re.compile(r"<[^>]+>")
