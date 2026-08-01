from __future__ import annotations

from accgram.hebrew_verse_sanitize import sanitize_verse_text_payload
from accgram.rtms_token_like import texts_from_token_like_payload

_HEBREW_MAQAF = "\u05be"
_HEBREW_METEG = "\u05bd"
_HEBREW_LETTER_START = ord("\u05d0")
_HEBREW_LETTER_END = ord("\u05ea")

INTERNAL_WLC422_WITNESS_KEY = "_wlc422_verse_meteg_witness"
INTERNAL_UXLC_WITNESS_KEY = "_uxlc_verse_meteg_witness"
INTERNAL_MAM_WITNESS_KEY = "_mam_simple_verse_meteg_witness"
INTERNAL_WITNESS_KEYS = {
    INTERNAL_WLC422_WITNESS_KEY,
    INTERNAL_UXLC_WITNESS_KEY,
    INTERNAL_MAM_WITNESS_KEY,
}


def witness_payload_for_side(
    enriched_row: dict[str, object],
    *,
    side_key: str,
) -> object | None:
    if side_key == "wlc422":
        return enriched_row.get(INTERNAL_WLC422_WITNESS_KEY)
    if side_key == "uxlc":
        return enriched_row.get(INTERNAL_UXLC_WITNESS_KEY)
    if side_key == "mam_simple":
        return enriched_row.get(INTERNAL_MAM_WITNESS_KEY)
    return None


def attach_internal_meteg_witnesses(
    enriched_row: dict[str, object],
    *,
    wlc422_witness: object,
    uxlc_witness: object,
    mam_simple_witness: object,
) -> None:
    enriched_row[INTERNAL_WLC422_WITNESS_KEY] = wlc422_witness
    enriched_row[INTERNAL_UXLC_WITNESS_KEY] = uxlc_witness
    enriched_row[INTERNAL_MAM_WITNESS_KEY] = mam_simple_witness


def strip_internal_witness_fields_from_rows(
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    return [_strip_internal_witness_fields(row) for row in rows]


def _strip_internal_witness_fields(value: object) -> object:
    if isinstance(value, list):
        return [_strip_internal_witness_fields(item) for item in value]

    if isinstance(value, dict):
        out: dict[str, object] = {}
        for key, child in value.items():
            if key in INTERNAL_WITNESS_KEYS:
                continue
            out[key] = _strip_internal_witness_fields(child)
        return out

    return value


def match_unique_witness_token(
    *,
    sanitized_token: str,
    source_witness_payload: object,
) -> str | None:
    normalized_target = _normalize_token_for_compare(sanitized_token)
    if not normalized_target:
        return None

    target_variants = _sanitized_compare_variants(normalized_target)

    candidate_tokens: list[str] = []
    for token in texts_from_token_like_payload(source_witness_payload):
        candidate_sanitized = _normalize_token_for_compare(
            _default_sanitized_token(token)
        )
        if not candidate_sanitized:
            continue
        candidate_variants = _sanitized_compare_variants(candidate_sanitized)
        if target_variants.isdisjoint(candidate_variants):
            continue
        candidate_tokens.append(token)

    if not candidate_tokens:
        return None

    unique_tokens = _unique_nonempty_tokens(candidate_tokens)
    if len(unique_tokens) != 1:
        return None

    return unique_tokens[0]


def token_has_meteg(token: str) -> bool:
    return _HEBREW_METEG in token


def token_has_maqaf(token: str) -> bool:
    return _HEBREW_MAQAF in token


def is_last_word_in_witness(
    *,
    sanitized_token: str,
    source_witness_payload: object,
) -> bool | None:
    hebrew_tokens = _hebrew_tokens_in_payload(source_witness_payload)
    if len(hebrew_tokens) <= 1:
        return None

    matched_token = match_unique_witness_token(
        sanitized_token=sanitized_token,
        source_witness_payload=source_witness_payload,
    )
    if not isinstance(matched_token, str) or not matched_token.strip():
        return None

    last_hebrew_token = _last_hebrew_token_in_payload(source_witness_payload)
    if not isinstance(last_hebrew_token, str) or not last_hebrew_token.strip():
        return None

    return _normalize_token_for_compare(matched_token) == _normalize_token_for_compare(
        last_hebrew_token
    )


def _default_sanitized_token(token: str) -> str:
    payload = {"word": token}
    sanitized_payload = sanitize_verse_text_payload(payload)
    if isinstance(sanitized_payload, dict) and isinstance(
        sanitized_payload.get("word"), str
    ):
        return sanitized_payload["word"]
    return ""


def _normalize_token_for_compare(token: str) -> str:
    return " ".join(token.split())


def _sanitized_compare_variants(token: str) -> set[str]:
    normalized = _normalize_token_for_compare(token)
    if not normalized:
        return set()

    without_meteg = normalized.replace(_HEBREW_METEG, "")
    out = {normalized}
    if without_meteg:
        out.add(without_meteg)
    return out


def _last_hebrew_token_in_payload(payload: object) -> str | None:
    hebrew_tokens = _hebrew_tokens_in_payload(payload)
    if not hebrew_tokens:
        return None
    return hebrew_tokens[-1]


def _hebrew_tokens_in_payload(payload: object) -> list[str]:
    out: list[str] = []
    for token in texts_from_token_like_payload(payload):
        if _has_hebrew_letter(token):
            out.append(token)
    return out


def _has_hebrew_letter(text: str) -> bool:
    return any(_HEBREW_LETTER_START <= ord(ch) <= _HEBREW_LETTER_END for ch in text)


def _unique_nonempty_tokens(tokens: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()

    for token in tokens:
        normalized = _normalize_token_for_compare(token)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        out.append(normalized)

    return out
