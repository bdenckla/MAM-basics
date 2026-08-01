from __future__ import annotations

from accgram import rtms_generated_descriptions
from accgram import rtms_meteg_witness
from accgram import rtmsr_diff_format
from accgram.rtms_sat_source_rows import SatSourceRow

_NON_STRING_ORIGIN_ALLOWLIST: dict[tuple[str, str], str] = {}


def build_sat_value_and_description(
    *,
    source_row: SatSourceRow,
    enriched_row: dict[str, object],
    row_ref: str,
    wlc_focus: str | None,
) -> tuple[str, str]:
    value = source_row.value
    description_key = source_row.description_key
    if not isinstance(description_key, str):
        return value, ""

    if not rtmsr_diff_format.is_plain_hebrew_string(value):
        return value, ""

    if not _origin_value_is_describable(
        row_ref=row_ref,
        row_key=source_row.key,
        origin_value=source_row.origin_value,
    ):
        return value, ""

    origin_value = source_row.origin_value
    description = rtms_generated_descriptions.try_generated_description(
        description_key=description_key,
        enriched_row=enriched_row,
        wlc_focus=wlc_focus,
        specific_origin_value=origin_value if isinstance(origin_value, str) else None,
    )
    if not isinstance(description, str) or not description.strip():
        return value, ""

    restored_value = maybe_restore_value_from_witness(
        row=enriched_row,
        target_key=source_row.key,
        target_value=value,
        description=description,
    )
    return restored_value, description


def maybe_restore_value_from_witness(
    *,
    row: dict[str, object],
    target_key: str,
    target_value: str,
    description: str,
) -> str:
    normalized_description = description.strip()
    if not normalized_description.startswith("meteg-"):
        return target_value

    if not rtmsr_diff_format.is_plain_hebrew_string(target_value):
        return target_value

    side_key = _witness_side_key_for_sat_row_key(target_key)
    if side_key is None:
        return target_value

    source_witness_payload = rtms_meteg_witness.witness_payload_for_side(
        row,
        side_key=side_key,
    )
    if source_witness_payload is None:
        return target_value

    witness_token = rtms_meteg_witness.match_unique_witness_token(
        sanitized_token=target_value,
        source_witness_payload=source_witness_payload,
    )
    if not isinstance(witness_token, str) or not witness_token.strip():
        return target_value

    if not rtms_meteg_witness.token_has_meteg(witness_token):
        return target_value

    has_maqaf = rtms_meteg_witness.token_has_maqaf(witness_token)
    if normalized_description == "meteg-space" and has_maqaf:
        return target_value
    if normalized_description in {"meteg-maqaf", "meteg-meteg-maqaf"} and not has_maqaf:
        return target_value

    return witness_token


def _origin_value_is_describable(
    *, row_ref: str, row_key: str, origin_value: object
) -> bool:
    if isinstance(origin_value, str):
        return rtmsr_diff_format.is_plain_hebrew_string(origin_value)

    if _is_non_string_origin_allowlisted(row_ref=row_ref, row_key=row_key):
        return False

    return False


def _is_non_string_origin_allowlisted(*, row_ref: str, row_key: str) -> bool:
    return (row_ref, _sat_row_base_key(row_key)) in _NON_STRING_ORIGIN_ALLOWLIST


def _sat_row_base_key(row_key: str) -> str:
    bracket_idx = row_key.find("[")
    if bracket_idx >= 0:
        return row_key[:bracket_idx]
    return row_key


def _witness_side_key_for_sat_row_key(row_key: str) -> str | None:
    base_key = _sat_row_base_key(row_key)

    if base_key == "wlc_focus":
        return "wlc422"
    if base_key == "diff_wlc_uxlc":
        return "uxlc"
    if base_key == "diff_wlc_mam":
        return "mam_simple"
    return None
