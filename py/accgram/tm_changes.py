from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

from wlc_cmn.wlc_book_codes import bk39id_to_wlc_bb
from mb_cmn.uxlc_change_url import uxlc_change_url
from py_uxlc.my_uxlc_book_abbreviations import BKNA_MAP_UXLC_TO_STD


def _normalize_book_token(book: str) -> str:
    return re.sub(r"[\s.]", "", book).lower()


_CITATION_BOOK_TO_STD_BKID = {
    _normalize_book_token(book_ua): std_bkid
    for book_ua, std_bkid in BKNA_MAP_UXLC_TO_STD.items()
}

_REF_RE = re.compile(r"^(?P<bb>[0-9a-z]{2})\s+(?P<ch>\d+):(?P<vr>\d+)$")
_CITATION_RE = re.compile(r"^(?P<book>.+?)\s+(?P<ch>\d+):(?P<vr>\d+)(?:\.\d+)?$")
_RELEASE_LABEL_RE = re.compile(r"^(?P<date>\d{4}\.\d{2}\.\d{2})\s*-\s*Changes$")
_COMPACT_CHANGE_RE = re.compile(r"^(?P<release>\d{4}\.\d{2}\.\d{2})/(?P<change_id>.+)$")


def load_all_changes_by_url(all_changes_path: Path) -> dict[str, dict[str, object]]:
    if not all_changes_path.is_file():
        raise FileNotFoundError(f"all_changes.json not found: {all_changes_path}")

    all_changes = _read_json(all_changes_path)
    if not isinstance(all_changes, list):
        raise ValueError(f"Expected list in all_changes.json: {all_changes_path}")

    by_change_url: dict[str, dict[str, object]] = {}
    for row in all_changes:
        if not isinstance(row, dict):
            continue
        url = _url_for_all_changes_row(row)
        by_change_url[url] = row
    return by_change_url


def canonicalize_uxlc_change_url(url: str) -> str | None:
    compact = _COMPACT_CHANGE_RE.match(url.strip())
    if compact is not None:
        return uxlc_change_url(compact.group("release"), compact.group("change_id"))

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return None
    if not parsed.query:
        return None

    path_parts = [part for part in parsed.path.split("/") if part]
    if len(path_parts) < 2:
        return None

    release_label = unquote(path_parts[-2])
    match = _RELEASE_LABEL_RE.match(release_label)
    if match is None:
        return None

    release = match.group("date")
    change_id = parsed.query
    return uxlc_change_url(release, change_id)


def citation_matches_ref(citation: str, ref: str) -> bool:
    citation_bb, citation_ch, citation_vr = _parse_citation(citation)
    ref_bb, ref_ch, ref_vr = _parse_ref(ref)
    return citation_bb == ref_bb and citation_ch == ref_ch and citation_vr == ref_vr


def _read_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as f_in:
        return json.load(f_in)


def _url_for_all_changes_row(row: dict[str, object]) -> str:
    release = row.get("release")
    changeset = row.get("changeset")
    n = row.get("n")
    if (
        not isinstance(release, str)
        or not isinstance(changeset, str)
        or not isinstance(n, int)
    ):
        raise ValueError("Malformed all_changes.json row: missing release/changeset/n")
    return uxlc_change_url(release, f"{changeset}-{n}")


def _parse_ref(ref: str) -> tuple[str, int, int]:
    match = _REF_RE.match(ref.strip())
    if match is None:
        raise ValueError(f"Malformed ref: {ref}")
    return match.group("bb"), int(match.group("ch")), int(match.group("vr"))


def _parse_citation(citation: str) -> tuple[str, int, int]:
    match = _CITATION_RE.match(citation.strip())
    if match is None:
        raise ValueError(f"Malformed citation: {citation}")

    citation_book = match.group("book")
    std_bkid = _CITATION_BOOK_TO_STD_BKID.get(_normalize_book_token(citation_book))
    if std_bkid is None:
        raise ValueError(f"Unknown citation book abbreviation: {citation_book}")

    try:
        bb = bk39id_to_wlc_bb(std_bkid)
    except ValueError as exc:
        raise ValueError(
            f"Could not map citation book to WLC bb code: {citation_book}"
        ) from exc

    return bb, int(match.group("ch")), int(match.group("vr"))
