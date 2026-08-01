from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from accgram import ob_error_context
from accgram import ob_page
from accgram import ob_report
from accgram import rtms_missing_sof_pasuq_descriptions
from accgram import rtms_ref
from accgram import rtms_report
from accgram import rtmsr_bracket_notes
from accgram import rtmsr_intro
from accgram import rtmsr_sat
from accgram import rtmsr_subsets
from accgram import rtmsr_verse
import wlc_provenance as provenance
from py_html import wlc_utils_html

_REPORT_TITLE = "Goerwitz Run on WLC"
_REPORT_HEADING = "Goerwitz Run on WLC"
_FILTER_SCRIPT_NAME = "goerwitz-filter.js"

StructuredTextLookup = Callable[[dict[str, object], str], object]


@dataclass
class _Entry:
    """One ungrammatical verse on the page, tagged along the filter dimensions."""

    ref: str
    # "msp" (missing sof pasuq), "msl" (missing silluq), "zwhim" (zarqa whim),
    # or "other"
    category: str
    # Which witness in the LC->BHS->WLC pipeline the ungrammatical is blamed on,
    # inferred from the prose summary: "wlc", "bhs", "lc", or "tbd" (unclear/TBD).
    source: str
    # Independent boolean dimensions, ANDed with the category filter.
    has_uxlc_change: bool  # the verse has a "UXLC change" link
    has_wlc_note: bool  # the verse's SAT table displays a WLC bracket-note
    anchor_id: str
    structured_text_lookup: StructuredTextLookup
    row: dict[str, object]
    error_tree: ob_error_context.ErrorTree | None


def write_goerwitz_combined_html_report(
    main_html_out_path: Path,
    enriched_ungrammatical_rows: list[dict[str, object]],
    base_dir: Path | None,
) -> Path:
    """Write goerwitz.html: every ungrammatical verse in one flat,
    client-side-filterable list (see goerwitz-filter.js)."""
    html_out_path = rtmsr_subsets.overview_html_out_path(main_html_out_path)
    html_out_path.parent.mkdir(parents=True, exist_ok=True)

    error_trees_by_ref: dict[str, ob_error_context.ErrorTree | None] = {}
    if enriched_ungrammatical_rows and isinstance(base_dir, Path):
        error_trees_by_ref = ob_error_context.collect_error_trees_by_ref(
            enriched_ungrammatical_rows, base_dir
        )

    entries = _build_entries(enriched_ungrammatical_rows, error_trees_by_ref)
    body_contents = _build_body_contents(entries)

    wlc_utils_html.write_html_to_file(
        body_contents=body_contents,
        write_ctx=wlc_utils_html.WriteCtx(
            title=_REPORT_TITLE,
            path=str(html_out_path),
            html_comment=provenance.generated_html_comment(__file__),
        ),
        path_to_style=rtms_report.path_to_gh_pages_style(html_out_path),
    )
    return html_out_path


def _build_entries(
    enriched_ungrammatical_rows: list[dict[str, object]],
    error_trees_by_ref: dict[str, ob_error_context.ErrorTree | None],
) -> list[_Entry]:
    entries: list[_Entry] = []

    for row in enriched_ungrammatical_rows:
        ref = _row_ref(row)
        bcv = ob_report.ref_bcv(ref)
        structured_text = ob_report.structured_text_dict(row)
        entries.append(
            _Entry(
                ref=ref,
                category=_category(row, structured_text),
                source=_source(structured_text, ref),
                has_uxlc_change=_has_uxlc_change(structured_text),
                has_wlc_note=_has_wlc_note(row, ref),
                anchor_id=ob_report.ungrammatical_anchor_id(bcv),
                structured_text_lookup=ob_report.structured_text_value,
                row=row,
                error_tree=error_trees_by_ref.get(ref),
            )
        )

    entries.sort(key=lambda entry: rtms_ref.reading_order_key(entry.ref))
    return entries


def _category(row: dict[str, object], structured_text: object) -> str:
    return rtms_missing_sof_pasuq_descriptions.row_category(
        row, structured_text=structured_text
    )


# Display label for each "Source" slug (the slug is stored per ungrammatical in its
# prose_ob_notes "st-source" field, and used as the filter checkbox's value and the
# verse's data-source attribute), in filter-display order.
_SOURCE_LABELS = {
    "wlc": "WLC",
    "bhs": "BHS/BHQ",
    "lc": "LC",
    "tbd": "unclear/TBD",
}


def _source(structured_text: object, ref: str) -> str:
    """Return the ungrammatical's hardcoded source slug (see _SOURCE_LABELS).

    The attribution lives beside the prose in each prose_ob_notes entry's "st-source"
    field rather than being re-derived from the summary, so editing a summary
    never silently changes a verse's source. Every ungrammatical must carry a valid
    st-source; a missing or unknown value is a hard error.
    """
    source = (
        structured_text.get("st-source") if isinstance(structured_text, dict) else None
    )
    if source not in _SOURCE_LABELS:
        raise ValueError(
            f"Ungrammatical {ref!r} has a missing or invalid 'st-source' (got "
            f"{source!r}); expected one of {sorted(_SOURCE_LABELS)}."
        )
    return source


def _has_uxlc_change(structured_text: object) -> bool:
    # Counts either a landed "UXLC change" or a "Pending UXLC change" link.
    if not isinstance(structured_text, dict):
        return False
    return any(
        isinstance(value := structured_text.get(key), str) and bool(value.strip())
        for key in ("uxlc_change", "pending_uxlc_change")
    )


def _has_wlc_note(row: dict[str, object], ref: str) -> bool:
    # Only bracket notes the verse's SAT table actually displays count, so the
    # flag agrees with the visible "]"-spans (not notes on undisplayed words).
    return rtmsr_sat.row_has_rendered_bracket_note(
        row,
        row_ref=ref,
        structured_text_lookup=ob_report.structured_text_value,
        wlc_tokens=rtmsr_verse.wlc_verse_vels(row),
    )


def _build_body_contents(entries: list[_Entry]) -> tuple[object, ...]:
    counts = _counts(entries)
    all_rows = [entry.row for entry in entries]

    descriptor = ob_page.CorpusDescriptor(
        heading_blocks=(
            wlc_utils_html.heading_level_1(_REPORT_HEADING),
            *rtmsr_intro.build_intro_contents(counts["total"]),
            *rtmsr_intro.checker_article_citation_contents(),
        ),
        facets=_build_facets(counts),
        count_para_class="gf-count",
        verse_sections=tuple(
            _render_verse_section(entry, is_first=index == 0)
            for index, entry in enumerate(entries)
        ),
        tail_blocks=tuple(
            rtmsr_bracket_notes.build_wlc_bracket_notes_section(all_rows)
        ),
        filter_script_name=_FILTER_SCRIPT_NAME,
    )
    return ob_page.build_page_body(descriptor)


def _render_verse_section(entry: _Entry, *, is_first: bool) -> object:
    # A dually-cantillated ungrammatical (dt 5:8) is laid out by reading -- its own section
    # builder emits both readings' verse lines, per-strand focus/diff tables, and parse
    # trees -- so it bypasses the generic single-table / single-tree flow (issue #36).
    if entry.row.get("dual_cant_readings"):
        items = list(
            rtms_report.render_dual_cant_section(
                entry.row,
                section_anchor_id=entry.anchor_id,
                structured_text_lookup=entry.structured_text_lookup,
            )
        )
        return ob_page.render_verse_section(
            items,
            is_first=is_first,
            data_attrs={
                "data-category": entry.category,
                "data-source": entry.source,
                "data-uchange": _flag_attr(entry.has_uxlc_change),
                "data-wnote": _flag_attr(entry.has_wlc_note),
            },
        )

    items = list(
        rtms_report.render_row_section_with_anchor_id(
            entry.row,
            section_anchor_id=entry.anchor_id,
            structured_text_lookup=entry.structured_text_lookup,
        )
    )
    items.extend(
        ob_report.render_error_context_section(entry.row, error_tree=entry.error_tree)
    )
    return ob_page.render_verse_section(
        items,
        is_first=is_first,
        data_attrs={
            "data-category": entry.category,
            "data-source": entry.source,
            "data-uchange": _flag_attr(entry.has_uxlc_change),
            "data-wnote": _flag_attr(entry.has_wlc_note),
        },
    )


def _flag_attr(value: bool) -> str:
    return "1" if value else "0"


def _build_facets(counts: dict[str, int]) -> tuple[ob_page.Facet, ...]:
    """The prose filter facets, in display order (see ob_page.build_filter_controls).

    The "has"/"doesn't have" tristate counts are the no-JS fallback; the filter
    script recomputes them live to the number of currently-visible matching verses
    (see goerwitz-filter.js)."""
    total = counts["total"]
    return (
        ob_page.CheckboxFacet(
            "Grammar error",
            "gf-category",
            (
                ("msp", "missing sof pasuq", counts["msp"]),
                ("msl", "missing silluq", counts["msl"]),
                ("zwhim", "zarqa whim", counts["zwhim"]),
                ("other", "other", counts["other"]),
            ),
        ),
        ob_page.CheckboxFacet(
            "Source",
            "gf-source",
            tuple(
                (slug, label, counts["src_" + slug])
                for slug, label in _SOURCE_LABELS.items()
            ),
        ),
        ob_page.TristateFacet(
            "UXLC change", "gf-uchange", counts["uchange_has"], total
        ),
        ob_page.TristateFacet(
            "WLC bracket-note", "gf-wnote", counts["wnote_has"], total
        ),
    )


def _counts(entries: list[_Entry]) -> dict[str, int]:
    counts = {
        "msp": 0,
        "msl": 0,
        "zwhim": 0,
        "other": 0,
        "uchange_has": 0,
        "wnote_has": 0,
        "total": len(entries),
    }
    for slug in _SOURCE_LABELS:
        counts[f"src_{slug}"] = 0
    for entry in entries:
        counts[entry.category] += 1
        counts[f"src_{entry.source}"] += 1
        if entry.has_uxlc_change:
            counts["uchange_has"] += 1
        if entry.has_wlc_note:
            counts["wnote_has"] += 1
    return counts


def _row_ref(row: dict[str, object]) -> str:
    ref = row.get("ref")
    if not isinstance(ref, str) or not ref.strip():
        raise ValueError("Row is missing non-empty string field 'ref'")
    return ref.strip()
