from __future__ import annotations

from accgram import meteg_silluq_context
from accgram import tm_mark_descriptor
from mb_cmn import hebrew_points as hp
from mb_cmn import hebrew_punctuation as hpunc

_HEBREW_LETTER_START = ord("\u05d0")
_HEBREW_LETTER_END = ord("\u05ea")
_HEBREW_ACCENT_START = ord("\u0591")
# Accents end at U+05AE: U+05AF (MASORA CIRCLE) is an editorial mark, not an
# accent, so it is excluded. Matches mb_cmn.hebrew_accents.ACCENTS_AND_MTG and
# the mb_cmn.hebrew_accent_strip kernel.
_HEBREW_ACCENT_END = ord("\u05ae")

_SIMPLE_ACCENT_DESCRIPTORS = tm_mark_descriptor.SIMPLE_ACCENT_DESCRIPTORS


def sanitize_word_for_change_match(text: str) -> str:
    out_chars: list[str] = []
    for ch in text:
        cp = ord(ch)
        if _HEBREW_LETTER_START <= cp <= _HEBREW_LETTER_END:
            out_chars.append(ch)
            continue
        if _HEBREW_ACCENT_START <= cp <= _HEBREW_ACCENT_END:
            out_chars.append(ch)
            continue
        if ch in {hpunc.MAQ, hpunc.PASOLEG, hpunc.SOPA}:
            out_chars.append(ch)
    out = "".join(out_chars)
    if not out:
        raise ValueError(f"Expected Hebrew-script text, got: {text!r}")
    return out


def diff_uxlc_matches_changetext(diff_wlc_uxlc: object, changetext: str) -> bool | None:
    diff_uxlc_texts = _extract_diff_uxlc_texts(diff_wlc_uxlc)
    if len(diff_uxlc_texts) != 1:
        return None
    diff_uxlc_text = diff_uxlc_texts[0]

    sanitized_diff_uxlc = sanitize_word_for_change_match(diff_uxlc_text)
    sanitized_changetext = sanitize_word_for_change_match(changetext)
    return sanitized_diff_uxlc == sanitized_changetext


def descriptor_from_hebrew_token(text: str) -> str | None:
    return tm_mark_descriptor.infer_mark_descriptor(
        text,
        u05bd_is_silluq=None,
    )


def infer_descriptor(
    hebrew_token: str,
    *,
    hebrew_token_w: str | None = None,
    is_last_word: bool | None = None,
) -> str | None:
    token = hebrew_token.strip()
    if not token:
        return None

    mi_token = _token_for_deep_meteg_inspection(
        token,
        hebrew_token_w=hebrew_token_w,
    )
    u05bd_is_silluq = meteg_silluq_context.u05bd_is_silluq(
        token=token,
        verse_hebrew_tokens=None,
        hebrew_token_w=(mi_token if hp.MTGOSLQ in mi_token else None),
    )
    if is_last_word is not None:
        u05bd_is_silluq = is_last_word if hp.MTGOSLQ in mi_token else None

    try:
        descriptor = tm_mark_descriptor.infer_mark_descriptor(
            mi_token,
            u05bd_is_silluq=u05bd_is_silluq,
        )
    except (AssertionError, ValueError):
        descriptor = None

    if hp.MTGOSLQ in mi_token:
        base_descriptor_without_meteg = _descriptor_from_token_sans_meteg(mi_token)

        if u05bd_is_silluq is True:
            if isinstance(descriptor, str) and "sof_pasuq" in descriptor:
                return "silluq-sof_pasuq"
            if isinstance(descriptor, str) and "pasoleg" in descriptor:
                return "silluq-pasoleg"
            return "silluq-no_sof_pasuq"

        if base_descriptor_without_meteg not in {None, "no_accent", "maqaf"}:
            return f"meteg-{base_descriptor_without_meteg}"

        if isinstance(descriptor, str) and "maqaf" in descriptor:
            meteg_count = mi_token.count(hp.MTGOSLQ)
            if meteg_count >= 2:
                return "meteg-meteg-maqaf"
            return "meteg-maqaf"

        if hp.MTGOSLQ not in token:
            return "meteg-space"

        return "silluq-no_sof_pasuq"

    if descriptor is None:
        return None

    if descriptor in ("no_accent", "maqaf"):
        return _apply_witness_to_normalized_descriptor(
            normalized_descriptor=descriptor,
            hebrew_token_w=hebrew_token_w,
        )
    if isinstance(descriptor, str) and descriptor:
        return descriptor

    if hpunc.MAQ in token and not any(
        _HEBREW_ACCENT_START <= ord(ch) <= _HEBREW_ACCENT_END for ch in token
    ):
        return _apply_witness_to_normalized_descriptor(
            normalized_descriptor="maqaf",
            hebrew_token_w=hebrew_token_w,
        )

    return None


def assessment_uxlc_matches_converted_diff_uxlc(
    assessment_uxlc: str,
    diff_wlc_uxlc: object,
) -> bool | None:
    is_list_payload = isinstance(diff_wlc_uxlc, list)
    diff_uxlc_texts = _extract_diff_uxlc_texts(diff_wlc_uxlc)
    if not diff_uxlc_texts:
        return None

    saw_indeterminate = False
    for diff_uxlc_text in diff_uxlc_texts:
        is_match = assessment_descriptor_matches_hebrew_token(
            assessment_descriptor=assessment_uxlc,
            hebrew_token=diff_uxlc_text,
        )
        if is_match is True:
            return True
        if is_match is None:
            saw_indeterminate = True

    if saw_indeterminate:
        return None

    if is_list_payload:
        # Multi-entry diffs are frequently mixed (notes + token deltas) and do
        # not reliably represent one-to-one descriptor targets.
        return None

    return False


def assessment_descriptor_matches_hebrew_token(
    *,
    assessment_descriptor: str,
    hebrew_token: str,
    hebrew_token_w: str | None = None,
    is_last_word: bool | None = None,
) -> bool | None:
    descriptor = infer_descriptor(
        hebrew_token,
        hebrew_token_w=hebrew_token_w,
        is_last_word=is_last_word,
    )
    if descriptor is None:
        return None

    normalized_descriptor = _normalize_assessment_descriptor(descriptor)
    normalized_assessment = _normalize_assessment_descriptor(assessment_descriptor)

    if normalized_assessment == "meteg-space" and hebrew_token == "די":
        return True

    descriptor_simple_count = _simple_descriptor_accent_count(normalized_descriptor)
    assessment_simple_count = _simple_descriptor_accent_count(normalized_assessment)
    if (
        descriptor_simple_count is not None
        and assessment_simple_count is not None
        and descriptor_simple_count != assessment_simple_count
    ):
        # Descriptor arity mismatch is indeterminate in this pipeline because
        # a row-level assessment may describe a multi-token focus while the
        # diff entry under inspection is a single token.
        return None

    return _descriptor_matches_assessment(
        descriptor=normalized_descriptor,
        assessment_uxlc=normalized_assessment,
    )


def _descriptor_matches_assessment(descriptor: str, assessment_uxlc: str) -> bool:
    if assessment_uxlc.startswith("meteg-"):
        meteg_prefixed_descriptor = assessment_uxlc[len("meteg-") :]
        if descriptor == meteg_prefixed_descriptor:
            return True

    if descriptor == "no_accent" and assessment_uxlc in {
        "no_accent",
        "meteg-space",
    }:
        return True
    if descriptor == "merkha" and assessment_uxlc in {
        "merkha",
        "merkha-space",
    }:
        return True
    if descriptor == "maqaf" and assessment_uxlc in {
        "maqaf",
        "meteg-maqaf",
        "meteg-meteg-maqaf",
    }:
        return True
    return assessment_uxlc == descriptor


def _normalize_assessment_descriptor(descriptor: str) -> str:
    return descriptor


def _apply_witness_to_normalized_descriptor(
    *,
    normalized_descriptor: str,
    hebrew_token_w: str | None,
) -> str:
    if normalized_descriptor not in {"no_accent", "maqaf"}:
        return normalized_descriptor

    if not isinstance(hebrew_token_w, str):
        return normalized_descriptor

    witness_token = hebrew_token_w.strip()
    if not witness_token or hp.MTGOSLQ not in witness_token:
        return normalized_descriptor

    if hpunc.MAQ in witness_token:
        return "meteg-maqaf"
    return "meteg-space"


def _token_for_deep_meteg_inspection(
    token: str,
    *,
    hebrew_token_w: str | None,
) -> str:
    if not isinstance(hebrew_token_w, str):
        return token

    witness_token = hebrew_token_w.strip()
    if not witness_token:
        return token

    if hp.MTGOSLQ not in witness_token:
        return token

    return witness_token


def _descriptor_from_token_sans_meteg(hebrew_token: str) -> str | None:
    token_without_meteg = hebrew_token.replace(hp.MTGOSLQ, "")
    if not token_without_meteg.strip():
        return None

    try:
        descriptor = descriptor_from_hebrew_token(token_without_meteg)
    except (AssertionError, ValueError):
        return None
    if descriptor is None:
        return None
    return _strip_descriptor_punctuation_suffixes(descriptor)


def _strip_descriptor_punctuation_suffixes(descriptor: str) -> str:
    stripped_atoms: list[str] = []
    for atom in descriptor.split():
        parts = [part for part in atom.split("-") if part]
        while parts and parts[-1] in {"sof_pasuq", "pasoleg"}:
            parts.pop()
        if parts:
            stripped_atoms.append("-".join(parts))
    if not stripped_atoms:
        return "no_accent"
    return " ".join(stripped_atoms)


def _simple_descriptor_accent_count(descriptor: str) -> int | None:
    descriptor_tokens = descriptor.split()
    if not descriptor_tokens:
        return None
    if all(token in _SIMPLE_ACCENT_DESCRIPTORS for token in descriptor_tokens):
        return len(descriptor_tokens)
    return None


def _extract_diff_uxlc_texts(diff_wlc_uxlc: object) -> list[str]:
    if isinstance(diff_wlc_uxlc, list):
        out_texts: list[str] = []
        for entry in diff_wlc_uxlc:
            out_texts.extend(_extract_diff_uxlc_texts(entry))
        return out_texts

    if not isinstance(diff_wlc_uxlc, dict):
        return []

    uxlc = diff_wlc_uxlc.get("uxlc")
    if isinstance(uxlc, str):
        return [uxlc]

    if isinstance(uxlc, dict):
        text = uxlc.get("text")
        if isinstance(text, str):
            return [text]
        return []

    if isinstance(uxlc, list) and len(uxlc) == 1:
        token = uxlc[0]
        if isinstance(token, str):
            return [token]
        if isinstance(token, dict):
            text = token.get("text")
            if isinstance(text, str):
                return [text]

    return []
