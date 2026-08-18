from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Mapping

from hkq_cmn.qere_projection import strip_accents_and_meteg

HEBREW_LETTER_PATTERN = re.compile(r"[\u05D0-\u05EA]+")
HEBREW_PUNCTUATION_PATTERN = re.compile(r"[\u05BE\u05C0\u05C3]")
QYV_QERE_ENDING = "\N{HEBREW POINT QAMATS}יו"


@dataclass(frozen=True)
class QyvEvaluation:
    matches: bool
    reason: str | None
    row_number: str
    verse: str
    word: str
    ketiv: str | None
    qere: str | None
    expected_qere: str | None


def evaluate_qyv_row(row: Mapping[str, object]) -> QyvEvaluation:
    row_number = _as_text(row.get("row_number", ""))
    verse = _as_text(row.get("verse", ""))
    word = _as_text(row.get("word", ""))
    notes_uxlc = _as_text(row.get("notes-UXLC", ""))
    notes_tokens = notes_uxlc.split()
    if len(notes_tokens) != 2:
        return QyvEvaluation(
            matches=False,
            reason=(
                f"row {row_number} {verse} must have exactly 2 UXLC note tokens, "
                f"got {notes_tokens!r}"
            ),
            row_number=row_number,
            verse=verse,
            word=word,
            ketiv=None,
            qere=None,
            expected_qere=None,
        )

    ketiv, qere = notes_tokens
    expected_qere = expected_qyv_qere(word)
    if expected_qere is None:
        return QyvEvaluation(
            matches=False,
            reason=(f"row {row_number} {verse} has no final vav in MAM word {word!r}"),
            row_number=row_number,
            verse=verse,
            word=word,
            ketiv=ketiv,
            qere=qere,
            expected_qere=None,
        )

    if hebrew_letters_only(word) != hebrew_letters_only(ketiv):
        return QyvEvaluation(
            matches=False,
            reason=(
                f"row {row_number} {verse} violates ketiv-letter match: "
                f"MAM {word!r}, UXLC ketiv {ketiv!r}"
            ),
            row_number=row_number,
            verse=verse,
            word=word,
            ketiv=ketiv,
            qere=qere,
            expected_qere=expected_qere,
        )

    expected_qere_core = HEBREW_PUNCTUATION_PATTERN.sub(
        "",
        strip_accents_and_meteg(expected_qere),
    )
    qere_core = HEBREW_PUNCTUATION_PATTERN.sub("", strip_accents_and_meteg(qere))
    if qere_core != expected_qere_core:
        return QyvEvaluation(
            matches=False,
            reason=(
                f"row {row_number} {verse} violates expected qere after accent stripping: "
                f"expected {expected_qere_core!r}, got {qere_core!r}"
            ),
            row_number=row_number,
            verse=verse,
            word=word,
            ketiv=ketiv,
            qere=qere,
            expected_qere=expected_qere,
        )

    if not qere_core.endswith(QYV_QERE_ENDING):
        return QyvEvaluation(
            matches=False,
            reason=(
                f"row {row_number} {verse} must end with {QYV_QERE_ENDING!r} "
                f"after accent stripping, got {qere_core!r}"
            ),
            row_number=row_number,
            verse=verse,
            word=word,
            ketiv=ketiv,
            qere=qere,
            expected_qere=expected_qere,
        )

    return QyvEvaluation(
        matches=True,
        reason=None,
        row_number=row_number,
        verse=verse,
        word=word,
        ketiv=ketiv,
        qere=qere,
        expected_qere=expected_qere,
    )


def require_qyv_row_match(row: Mapping[str, object], *, context: str) -> None:
    evaluation = evaluate_qyv_row(row)
    if evaluation.matches:
        return
    raise ValueError(f"{evaluation.reason} ({context})")


def expected_qyv_qere(word: str) -> str | None:
    last_vav_index = word.rfind("ו")
    if last_vav_index == -1:
        return None
    return f"{word[:last_vav_index]}י{word[last_vav_index:]}"


def hebrew_letters_only(text: str) -> str:
    return "".join(HEBREW_LETTER_PATTERN.findall(text))


def _as_text(value: object) -> str:
    return value if isinstance(value, str) else str(value)
