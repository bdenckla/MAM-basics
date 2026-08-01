from __future__ import annotations

from mb_cmn import hebrew_points as hp
from mb_cmn import hebrew_punctuation as hpunc

_HEBREW_LETTER_START = ord("\u05d0")
_HEBREW_LETTER_END = ord("\u05ea")


def normalize_token(token: str) -> str:
    return " ".join(token.split())


def token_has_hebrew_letter(token: str) -> bool:
    return any(_HEBREW_LETTER_START <= ord(ch) <= _HEBREW_LETTER_END for ch in token)


def token_compare_variants(token: str) -> set[str]:
    normalized = normalize_token(token)
    if not normalized:
        return set()

    without_meteg = normalized.replace(hp.MTGOSLQ, "")
    out = {normalized}
    if without_meteg:
        out.add(without_meteg)
    return out


def last_hebrew_token(verse_hebrew_tokens: list[str] | None) -> str | None:
    if not isinstance(verse_hebrew_tokens, list):
        return None

    for token in reversed(verse_hebrew_tokens):
        if not isinstance(token, str):
            continue
        normalized = normalize_token(token)
        if normalized and token_has_hebrew_letter(normalized):
            return normalized
    return None


def token_is_last_hebrew_token(
    *,
    token: str,
    verse_hebrew_tokens: list[str] | None,
    hebrew_token_w: str | None = None,
) -> bool | None:
    last_token = last_hebrew_token(verse_hebrew_tokens)
    if last_token is None:
        return None

    candidate = normalize_token(hebrew_token_w or token)
    if not candidate:
        return False

    candidate_variants = token_compare_variants(candidate)
    last_variants = token_compare_variants(last_token)
    if not candidate_variants or not last_variants:
        return False
    return not candidate_variants.isdisjoint(last_variants)


def u05bd_is_silluq(
    *,
    token: str,
    verse_hebrew_tokens: list[str] | None,
    hebrew_token_w: str | None = None,
) -> bool | None:
    inspected = normalize_token(hebrew_token_w or token)
    if hp.MTGOSLQ not in inspected:
        return None

    is_last = token_is_last_hebrew_token(
        token=token,
        verse_hebrew_tokens=verse_hebrew_tokens,
        hebrew_token_w=hebrew_token_w,
    )
    if is_last is not None:
        return is_last

    if hpunc.SOPA in inspected or hpunc.PASOLEG in inspected:
        return True

    return None
