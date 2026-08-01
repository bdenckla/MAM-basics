from __future__ import annotations

from accgram import ob_error_context
from accgram import prose_ob_notes
from accgram import ob_tree_table
from accgram import rtms_ref
from accgram import rtmsr_sat
from accgram import rtmsr_verse
from py_html import wlc_utils_html


def render_error_context_section(
    row: dict[str, object],
    *,
    error_tree: ob_error_context.ErrorTree | None,
) -> tuple[object, ...]:
    if error_tree is None:
        raise ValueError(
            "Ungrammatical row is missing a parsed ERROR tree; ungrammatical must include at "
            f"least one ERROR leaf (ref={_row_ref(row)!r})."
        )

    return (
        wlc_utils_html.div(
            (ob_tree_table.render_error_tree_table(error_tree),),
            {"class": "goerwitz-obs-tree-wrap"},
        ),
    )


def structured_text_dict(row: dict[str, object]) -> dict[str, object] | None:
    row_ref = _row_ref(row)
    structured_text = prose_ob_notes.get_structured_text().get(row_ref)
    if not isinstance(structured_text, dict):
        return None
    return structured_text


def structured_text_value(row: dict[str, object], key: str) -> object:
    structured_text = structured_text_dict(row)
    if structured_text is None:
        return None

    value = structured_text.get(key)
    if key != "st-summary":
        return value

    if not isinstance(value, str):
        return value
    if "$" not in value:
        return value

    return rtmsr_sat.render_summary_template_from_sat_descriptors(
        row,
        row_ref=_row_ref(row),
        summary_template=value,
        structured_text_lookup=structured_text_value,
        wlc_tokens=rtmsr_verse.wlc_verse_vels(row),
    )


def _row_ref(row: dict[str, object]) -> str:
    ref = row.get("ref")
    if not isinstance(ref, str) or not ref.strip():
        raise ValueError("Ungrammatical row is missing non-empty string field 'ref'")
    return ref.strip()


def ref_bcv(ref: str) -> str:
    bb, chnu, vrnu = rtms_ref.parse_ref(ref, row_kind="ungrammatical")
    return rtms_ref.to_compact_bcv(bb, chnu, vrnu)


def ungrammatical_anchor_id(bcv: str) -> str:
    return f"ob{bcv.replace(':', 'v')}"
