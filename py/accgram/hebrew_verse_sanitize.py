from __future__ import annotations

from mb_cmn import hebrew_accent_strip as has
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_punctuation as hpunc

_HEBREW_LETTER_START = ord("\u05d0")
_HEBREW_LETTER_END = ord("\u05ea")

# MAM marks word stress by duplicating a word's disjunctive accent onto the
# stressed syllable.  The canonical accent sits at one edge of the word and the
# extra copy (the "stress helper") sits on the stressed syllable; WLC has
# only the canonical copy.  To suppress this spurious MAM-vs-WLC difference we
# keep the canonical-edge copy and drop the helper(s):
#   - telisha gedola is prepositive (canonical copy at the word start) -> keep first
#   - segol/segolta  is postpositive (canonical copy at the word end)  -> keep last
_KEEP_FIRST_STRESS_HELPER_ACCENTS = (ha.TEL_G,)
_KEEP_LAST_STRESS_HELPER_ACCENTS = (ha.SEG_A,)


def sanitize_verse_text_payload(
    payload: object,
    *,
    remove_mam_stress_helper_duplicates: bool = False,
    preserve_all_meteg: bool = False,
) -> object:
    mutable = _deep_clone_jsonish(payload)
    slots: list[tuple[list[object] | dict[str, object], int | str]] = []
    _collect_hebrew_string_slots(mutable, slots)

    # Preserve Unicode METEG only on the final Hebrew token in the verse payload.
    last_hebrew_slot: tuple[list[object] | dict[str, object], int | str] | None = None
    for container, key in slots:
        value = container[key]
        if isinstance(value, str) and _has_hebrew_letter(value):
            last_hebrew_slot = (container, key)

    for container, key in slots:
        value = container[key]
        if not isinstance(value, str):
            continue
        keep_last_meteg = (
            last_hebrew_slot is not None
            and container is last_hebrew_slot[0]
            and key == last_hebrew_slot[1]
        )
        keep_all_meteg = preserve_all_meteg and _has_hebrew_letter(value)
        container[key] = _sanitize_hebrew_token(
            value,
            keep_last_meteg=keep_last_meteg,
            keep_all_meteg=keep_all_meteg,
            remove_mam_stress_helper_duplicates=remove_mam_stress_helper_duplicates,
        )

    return mutable


def _deep_clone_jsonish(value: object) -> object:
    if isinstance(value, dict):
        return {k: _deep_clone_jsonish(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_deep_clone_jsonish(v) for v in value]
    return value


def _collect_hebrew_string_slots(
    value: object,
    out: list[tuple[list[object] | dict[str, object], int | str]],
) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if isinstance(child, str):
                if _has_hebrew_block_char(child):
                    out.append((value, key))
            else:
                _collect_hebrew_string_slots(child, out)
        return

    if isinstance(value, list):
        for idx, child in enumerate(value):
            if isinstance(child, str):
                if _has_hebrew_block_char(child):
                    out.append((value, idx))
            else:
                _collect_hebrew_string_slots(child, out)


def _has_hebrew_block_char(text: str) -> bool:
    return any(0x0590 <= ord(ch) <= 0x05FF for ch in text)


def _has_hebrew_letter(text: str) -> bool:
    return any(_HEBREW_LETTER_START <= ord(ch) <= _HEBREW_LETTER_END for ch in text)


def _sanitize_hebrew_token(
    text: str,
    *,
    keep_last_meteg: bool,
    keep_all_meteg: bool,
    remove_mam_stress_helper_duplicates: bool,
) -> str:
    # Delegate the generic "strip to letters + accents + accent-coupled
    # punctuation" kernel to the vendored mb_cmn.hebrew_accent_strip; our two
    # booleans map onto its three-valued meteg policy.  The MAM stress-helper
    # dedup below is WLC-specific and stays local.
    if keep_all_meteg:
        keep_meteg = has.METEG_ALL
    elif keep_last_meteg:
        keep_meteg = has.METEG_SILLUQ
    else:
        keep_meteg = has.METEG_DROP
    sanitized = has.strip_to_accents(text, keep_meteg=keep_meteg)
    if remove_mam_stress_helper_duplicates:
        sanitized = _drop_mam_stress_helper_duplicates(sanitized)
    return sanitized


def _drop_mam_stress_helper_duplicates(text: str) -> str:
    # Dedup per word: maqaf/pasoleg/sopa-joined units are treated as separate words.
    out_chars: list[str] = []
    word: list[str] = []
    for ch in text:
        if ch in {hpunc.MAQ, hpunc.PASOLEG, hpunc.SOPA}:
            out_chars.extend(_dedup_word_stress_helpers(word))
            out_chars.append(ch)
            word = []
            continue
        word.append(ch)
    out_chars.extend(_dedup_word_stress_helpers(word))
    return "".join(out_chars)


def _dedup_word_stress_helpers(word: list[str]) -> list[str]:
    result = list(word)
    for accent in _KEEP_FIRST_STRESS_HELPER_ACCENTS:
        positions = [i for i, ch in enumerate(result) if ch == accent]
        for i in reversed(positions[1:]):  # drop all but the first (canonical) copy
            del result[i]
    for accent in _KEEP_LAST_STRESS_HELPER_ACCENTS:
        positions = [i for i, ch in enumerate(result) if ch == accent]
        for i in reversed(positions[:-1]):  # drop all but the last (canonical) copy
            del result[i]
    return result
