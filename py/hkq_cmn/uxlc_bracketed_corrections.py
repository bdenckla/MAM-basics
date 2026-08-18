"""Ben Denckla's corrections to Holman's wording, shown in square brackets.

The page quotes Holman's messages, so a word of his that is wrong stays wrong
unless something says otherwise. This is that something: a table of one-word
replacements, each applied where it is filed and shown bracketed, which is the
ordinary notation for an editor's word standing in a quotation. The page's
intro says whose the brackets are, because the notation alone does not.

Two entries so far, both from the Judges message of 7 August 2026:

  * Its subject says Joshua, and its one case is Judges 11:24. Holman had sent
    four Joshua cases four hours earlier and the subject line did not follow him
    to the next book.

  * Its Note says the munach is under the tet of אוֹתוֹ, a word whose letters are
    alef, vav, tav, vav. The mark is under the tav, which is what the change
    item the card links, 2026.04.10-7, calls it too.

Applying an entry is fail-fast in both directions. A replacement whose original
is not in the text exactly once raises, so a reworded message cannot leave a
correction silently unapplied; and a table key naming no case, no field, or no
message raises, so a mistyped key is loud. Between them, every entry here is
known to have fired.

The redaction marker ``[address removed]`` is bracketed too and is not one of
these: it stands where an address was, rather than replacing a word Holman
wrote. ``uxlc_email_extract.ADDRESS_REDACTION`` is that one.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from hkq_cmn.uxlc_email_extract import CorrectionCase, SourceEmail
from hkq_cmn.uxlc_external_links import book_display_name


@dataclass(frozen=True)
class BracketedCorrection:
    """One word of Holman's, and the word shown in square brackets instead."""

    original: str
    replacement: str

    @property
    def bracketed(self) -> str:
        return f"[{self.replacement}]"


# Keyed by (case reference, field label). The reference is spelled as
# uxlc_email_extract.CaseRef.key spells it, and the label is the message's own.
CASE_FIELD_CORRECTIONS = {
    ("Judges 11:24.7", "Note"): (BracketedCorrection("Tet", "Tav"),),
}

# Keyed by email key, which is the .eml filename slugged.
EMAIL_SUBJECT_CORRECTIONS = {
    "suggested-uxlc-corrections-for-joshua-one-case": (
        BracketedCorrection("Joshua", "Judges"),
    ),
}


def apply_bracketed_corrections(
    emails: list[SourceEmail], cases: list[CorrectionCase]
) -> tuple[list[SourceEmail], list[CorrectionCase]]:
    """Return the messages and cases with every correction in place."""
    _require_known_targets(emails, cases)
    return (
        [
            replace(
                source_email,
                subject=_corrected(
                    source_email.subject,
                    EMAIL_SUBJECT_CORRECTIONS.get(source_email.key, ()),
                    f"the subject of {source_email.key}",
                ),
            )
            for source_email in emails
        ],
        [
            replace(
                case,
                fields=tuple(
                    (label, _corrected_case_field(case.ref.key, label, value))
                    for label, value in case.fields
                ),
            )
            for case in cases
        ],
    )


def bracketed_correction_phrases(
    emails: list[SourceEmail], cases: list[CorrectionCase]
) -> tuple[str, ...]:
    """One phrase per correction, for the intro's sentence about the brackets.

    Built from the table rather than written out beside it, so the page cannot
    end up describing a set of corrections it is not making.
    """
    phrases = [
        f"on the subject of the message of {source_email.date_display},"
        f" {correction.original} is shown as {correction.bracketed}"
        for source_email in emails
        for correction in EMAIL_SUBJECT_CORRECTIONS.get(source_email.key, ())
    ]
    phrases.extend(
        f"on the {label} line of {book_display_name(case.ref.book)}"
        f" {case.ref.chapter}:{case.ref.verse},"
        f" {correction.original} is shown as {correction.bracketed}"
        for case in cases
        for label, _value in case.fields
        for correction in CASE_FIELD_CORRECTIONS.get((case.ref.key, label), ())
    )
    return tuple(phrases)


def _corrected_case_field(ref_key: str, label: str, value: str) -> str:
    return _corrected(
        value,
        CASE_FIELD_CORRECTIONS.get((ref_key, label), ()),
        f"the {label} field of {ref_key}",
    )


def _corrected(
    text: str, corrections: tuple[BracketedCorrection, ...], where: str
) -> str:
    for correction in corrections:
        found = text.count(correction.original)
        if found != 1:
            raise ValueError(
                f"{where} holds {correction.original!r} {found} times, not once, "
                f"so the bracketed correction to {correction.replacement!r} "
                "cannot be placed. Reread the message and update "
                "hkq_cmn/uxlc_bracketed_corrections."
            )
        text = text.replace(correction.original, correction.bracketed)
    return text


def _require_known_targets(
    emails: list[SourceEmail], cases: list[CorrectionCase]
) -> None:
    email_keys = {source_email.key for source_email in emails}
    unmatched_emails = sorted(set(EMAIL_SUBJECT_CORRECTIONS) - email_keys)
    if unmatched_emails:
        raise ValueError(
            "EMAIL_SUBJECT_CORRECTIONS names messages that are not here: "
            f"{unmatched_emails}"
        )

    case_fields = {
        (case.ref.key, label) for case in cases for label, _value in case.fields
    }
    unmatched_fields = sorted(set(CASE_FIELD_CORRECTIONS) - case_fields)
    if unmatched_fields:
        raise ValueError(
            "CASE_FIELD_CORRECTIONS names case fields that are not here: "
            f"{unmatched_fields}"
        )
