"""Genuine SAT focus-word table for the poetic ungrammatical-verse report (issue wlc-utils#10).

The "SAT" table is goerwitz.html's per-witness focus-word table: the WLC focus
word against its UXLC and MAM-simple readings, with inline WLC bracket-notes and
an accent description (its columns are: Hebrew value | WLC bracket-notes | accent
description | witness key). The acronym itself is not expanded anywhere in the
codebase.

This module reuses the prose enrichment + renderer (rtms_data.build_enriched_row,
rtmsr_sat.render_sat_table) to reproduce that table on the poetic page, and is
split out of poetic_oddballs so that module stays focused on ungrammatical collection
and page assembly. The poetic page localizes the focus to the verse-final chanted word
(the missing-silluq locus); NO_PARSE verses have no single focus word and so get
no SAT table.
"""

from __future__ import annotations

from pathlib import Path

from accgram import rtms_data
from accgram import rtms_focus_diff_expand
from accgram import rtmsr_sat
from accgram import rtmsr_verse


def focus_word(*, final_word: str | None, wlc_verse: object) -> str | None:
    """The verse-final chanted word as the SAT focus, or None if it is absent or occurs
    more than once in the verse -- build_enriched_row requires a unique focus, so a
    non-unique final word degrades to no SAT table."""
    if not final_word:
        return None
    verse_text = rtms_focus_diff_expand.normalized_wlc_verse_text_from_payload(
        wlc_verse
    )
    occurrences = rtms_focus_diff_expand.count_focus_occurrences_in_verse_text(
        verse_text=verse_text, wlc_focus=final_word
    )
    return final_word if occurrences == 1 else None


def build_focus_enriched_row(
    *,
    bb_ref: str,
    bcv: str,
    output_file: str,
    wlc_focus: str,
    wlc422_by_bcv: dict[str, dict[str, object]],
    uxlc_by_bcv: dict[str, dict[str, object]],
    mam_simple_by_bcv: dict[str, dict[str, object]],
    wlc422_kq_u_dir: Path,
    uxlc_dir: Path,
    mam_simple_dir: Path,
) -> dict[str, object] | None:
    """The build_enriched_row payload for one verse's SAT table, filtered to the
    focus word, or None when a witness verse is missing (so the run stays
    non-fatal)."""
    try:
        enriched_row, _diff = rtms_data.build_enriched_row(
            row={"ref": bb_ref, "output_file": output_file, "wlc_focus": wlc_focus},
            bcv=bcv,
            ref=bb_ref,
            wlc422_by_bcv=wlc422_by_bcv,
            uxlc_by_bcv=uxlc_by_bcv,
            mam_simple_by_bcv=mam_simple_by_bcv,
            wlc422_kq_u_dir=wlc422_kq_u_dir,
            uxlc_dir=uxlc_dir,
            mam_simple_dir=mam_simple_dir,
            wlc_focus=wlc_focus,
        )
    except ValueError:
        return None
    # build_enriched_row keeps every word-level diff in the verse; the SAT table is
    # a focus-WORD table, so drop the incidental non-focus diffs (the prose page does
    # this per-verse via rtmsr_sat's hand-curated _SAT_ROW_SUPPRESSIONS_BY_REF).
    enriched_row["diff_wlc_uxlc"] = _focus_only_diff(
        enriched_row.get("diff_wlc_uxlc"), wlc_focus=wlc_focus
    )
    enriched_row["diff_wlc_mam"] = _focus_only_diff(
        enriched_row.get("diff_wlc_mam"), wlc_focus=wlc_focus
    )
    return enriched_row


def render_table(enriched_row: object, *, row_ref: str) -> object | None:
    """The goerwitz SAT focus-word table, reusing the prose renderer
    (rtmsr_sat.render_sat_table). Returns None when there is no enriched row -- i.e.
    for NO_PARSE verses (no localized focus) or a non-unique final word."""
    if not isinstance(enriched_row, dict) or not enriched_row.get("wlc_focus"):
        return None
    return rtmsr_sat.render_sat_table(
        enriched_row,
        row_ref=row_ref,
        structured_text_lookup=lambda r, key: r.get(key),
        wlc_tokens=rtmsr_verse.wlc_verse_vels(enriched_row),
    )


def _focus_only_diff(diff_value: object, *, wlc_focus: str) -> object:
    """Keep only diff entries whose WLC side is the focus word itself, collapsing a
    lone survivor back to a bare dict (so it renders as ``diff_wlc_mam`` rather than
    ``diff_wlc_mam[1]``, matching the single-diff verses)."""
    if isinstance(diff_value, list):
        entries = [entry for entry in diff_value if entry is not None]
    elif diff_value is None:
        entries = []
    else:
        entries = [diff_value]
    kept = [
        entry
        for entry in entries
        if isinstance(entry, dict)
        and rtmsr_sat.render_sat_value(entry.get("wlc422")) == wlc_focus
    ]
    if not kept:
        return []
    if len(kept) == 1:
        return kept[0]
    return kept
