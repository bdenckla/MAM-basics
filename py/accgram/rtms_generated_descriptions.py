from __future__ import annotations

from accgram import rtms_meteg_witness
from accgram.rtms_token_like import texts_from_token_like_payload
from accgram.tm_descriptor import infer_descriptor


def try_generated_description(
    *,
    description_key: str,
    enriched_row: dict[str, object],
    wlc_focus: str | None,
    specific_origin_value: str | None = None,
) -> str | None:
    if description_key == "manuscript":
        return None

    for (
        hebrew_token,
        witness_token,
        is_last_word,
    ) in _candidate_tokens_for_generated_description(
        description_key=description_key,
        enriched_row=enriched_row,
        wlc_focus=wlc_focus,
        specific_origin_value=specific_origin_value,
    ):
        descriptor = _infer_descriptor(
            hebrew_token,
            hebrew_token_w=witness_token,
            is_last_word=is_last_word,
        )
        if isinstance(descriptor, str) and descriptor.strip():
            return descriptor

    return None


def diff_rhs_tokens(diff_value: object, *, rhs_key: str) -> list[str]:
    if isinstance(diff_value, list):
        out_tokens: list[str] = []
        for item in diff_value:
            out_tokens.extend(diff_rhs_tokens(item, rhs_key=rhs_key))
        return out_tokens

    if not isinstance(diff_value, dict):
        return []

    if rhs_key not in diff_value:
        return []

    return texts_from_token_like_payload(diff_value.get(rhs_key))


def infer_generated_description_for_token(hebrew_token: str) -> str | None:
    return _infer_descriptor(
        hebrew_token,
    )


def _candidate_tokens_for_generated_description(
    *,
    description_key: str,
    enriched_row: dict[str, object],
    wlc_focus: str | None,
    specific_origin_value: str | None = None,
) -> list[tuple[str, str | None, bool | None]]:
    candidates: list[tuple[str, str | None, bool | None]] = []

    wlc_witness_payload = rtms_meteg_witness.witness_payload_for_side(
        enriched_row,
        side_key="wlc422",
    )

    if description_key == "wlc":
        if isinstance(wlc_focus, str):
            candidates.append(
                _candidate_with_optional_witness(
                    hebrew_token=wlc_focus,
                    source_witness_payload=wlc_witness_payload,
                )
            )

    if description_key == "uxlc":
        uxlc_witness_payload = rtms_meteg_witness.witness_payload_for_side(
            enriched_row,
            side_key="uxlc",
        )
        if isinstance(specific_origin_value, str):
            candidates.append(
                _candidate_with_optional_witness(
                    hebrew_token=specific_origin_value,
                    source_witness_payload=uxlc_witness_payload,
                )
            )
        else:
            candidates.extend(
                _candidate_tokens_from_diff_side(
                    diff_value=enriched_row.get("diff_wlc_uxlc"),
                    rhs_key="uxlc",
                    source_witness_payload=uxlc_witness_payload,
                )
            )
            if isinstance(wlc_focus, str):
                candidates.append(
                    _candidate_with_optional_witness(
                        hebrew_token=wlc_focus,
                        source_witness_payload=wlc_witness_payload,
                    )
                )

    if description_key == "mam":
        mam_witness_payload = rtms_meteg_witness.witness_payload_for_side(
            enriched_row,
            side_key="mam_simple",
        )
        if isinstance(specific_origin_value, str):
            candidates.append(
                _candidate_with_optional_witness(
                    hebrew_token=specific_origin_value,
                    source_witness_payload=mam_witness_payload,
                )
            )
        else:
            candidates.extend(
                _candidate_tokens_from_diff_side(
                    diff_value=enriched_row.get("diff_wlc_mam"),
                    rhs_key="mam_simple",
                    source_witness_payload=mam_witness_payload,
                )
            )
            if isinstance(wlc_focus, str):
                candidates.append(
                    _candidate_with_optional_witness(
                        hebrew_token=wlc_focus,
                        source_witness_payload=wlc_witness_payload,
                    )
                )

    return _unique_candidate_tokens(candidates)


def _candidate_tokens_from_diff_side(
    *,
    diff_value: object,
    rhs_key: str,
    source_witness_payload: object,
) -> list[tuple[str, str | None, bool | None]]:
    return [
        _candidate_with_optional_witness(
            hebrew_token=token,
            source_witness_payload=source_witness_payload,
        )
        for token in diff_rhs_tokens(diff_value, rhs_key=rhs_key)
    ]


def _candidate_with_optional_witness(
    *,
    hebrew_token: str,
    source_witness_payload: object,
) -> tuple[str, str | None, bool | None]:
    collapsed_token = " ".join(hebrew_token.split())
    if not collapsed_token:
        return "", None, None

    witness_token: str | None = None
    is_last_word: bool | None = None
    if source_witness_payload is not None:
        witness_token = rtms_meteg_witness.match_unique_witness_token(
            sanitized_token=collapsed_token,
            source_witness_payload=source_witness_payload,
        )
        is_last_word = rtms_meteg_witness.is_last_word_in_witness(
            sanitized_token=collapsed_token,
            source_witness_payload=source_witness_payload,
        )
    return collapsed_token, witness_token, is_last_word


def _unique_candidate_tokens(
    values: list[tuple[str, str | None, bool | None]],
) -> list[tuple[str, str | None, bool | None]]:
    out: list[tuple[str, str | None, bool | None]] = []
    seen_idx_by_token: dict[str, int] = {}

    for token, witness, is_last_word in values:
        collapsed_token = " ".join(token.split())
        if not collapsed_token:
            continue

        collapsed_witness = None
        if isinstance(witness, str):
            maybe_witness = " ".join(witness.split())
            if maybe_witness:
                collapsed_witness = maybe_witness

        existing_idx = seen_idx_by_token.get(collapsed_token)
        if existing_idx is None:
            seen_idx_by_token[collapsed_token] = len(out)
            out.append((collapsed_token, collapsed_witness, is_last_word))
            continue

        existing_token, existing_witness, existing_is_last = out[existing_idx]
        merged_witness = _merge_candidate_witness(existing_witness, collapsed_witness)
        merged_is_last = _merge_candidate_is_last_word(
            existing_is_last,
            is_last_word,
        )
        out[existing_idx] = (existing_token, merged_witness, merged_is_last)

    return out


def _merge_candidate_witness(
    existing_witness: str | None,
    incoming_witness: str | None,
) -> str | None:
    if existing_witness is None:
        return incoming_witness
    if incoming_witness is None:
        return existing_witness
    if existing_witness == incoming_witness:
        return existing_witness
    return None


def _merge_candidate_is_last_word(
    existing_is_last: bool | None,
    incoming_is_last: bool | None,
) -> bool | None:
    if existing_is_last is None:
        return incoming_is_last
    if incoming_is_last is None:
        return existing_is_last
    if existing_is_last == incoming_is_last:
        return existing_is_last
    return None


def _infer_descriptor(
    hebrew_token: str,
    *,
    hebrew_token_w: str | None = None,
    is_last_word: bool | None = None,
) -> str | None:
    return infer_descriptor(
        hebrew_token,
        hebrew_token_w=hebrew_token_w,
        is_last_word=is_last_word,
    )
