"""Ben Denckla's corrections to Holman's wording, shown in square brackets.

The page quotes Holman's messages, so a word of his that is wrong stays wrong
unless something says otherwise. This is that something: a table of one-word
replacements, each applied where it is filed and shown bracketed, which is the
ordinary notation for an editor's word standing in a quotation. The page's
intro says whose the brackets are, because the notation alone does not.

Four entries so far. Two are from the Judges message of 7 August 2026:

  * Its subject says Joshua, and its one case is Judges 11:24. Holman had sent
    four Joshua cases four hours earlier and the subject line did not follow him
    to the next book.

  * Its Note says the munach is under the tet of אוֹתוֹ, a word whose letters are
    alef, vav, tav, vav. The mark is under the tav, which is what the change
    item the card links, 2026.04.10-7, calls it too.

The other two are the "Current UXLC" forms of Psalms 31:24.1 and
Proverbs 30:15.1 in Holman's messages. Each stores a meteg before its vowel
with no CGJ between them, so a font shows the meteg left of the vowel. The
UXLC had a CGJ after the meteg until UXLC 2.6 changed those atoms' marks
(records 2026.08.05-53 and -94). Each bracketed form adds that CGJ. The
intro does not quote Holman's two forms, which would put forms lacking the
CGJ back on the page: it shows each bracketed form and says what it adds.
Ben, 2026-10-31, when the intro still quoted them: "dont' treat holman's
text as so sacred as to present the originals: just present the fixed, and
say you fixed it"; and, shown the wording the intro now has, "Yes, rewrite
it".

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
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_letters as hl
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import str_defs as sd


@dataclass(frozen=True)
class BracketedCorrection:
    """One word of Holman's, and the word shown in square brackets instead.

    The explanation, if any, follows the correction in the intro's sentence.
    With quote_original false, that sentence leaves the original out and shows
    only the bracketed word, so the explanation, which must then say what the
    bracketed word changed, is required.
    """

    original: str
    replacement: str
    explanation: str = ""
    quote_original: bool = True

    def __post_init__(self) -> None:
        if not self.quote_original and not self.explanation:
            raise ValueError(
                f"the correction to {self.replacement!r} quotes no original, so "
                "it needs an explanation of what it changed"
            )

    @property
    def bracketed(self) -> str:
        return f"[{self.replacement}]"


def _with_cgj_after_meteg(form: str) -> str:
    """Return the form with a CGJ after its one meteg."""
    if form.count(hpo.MTGOSLQ) != 1:
        raise ValueError(f"{form!r} does not hold exactly one meteg")
    return form.replace(hpo.MTGOSLQ, hpo.MTGOSLQ + sd.CGJ)


# The "Current UXLC" forms of two cases as Holman's messages give them, each
# with a meteg before its vowel and no CGJ between them. The Proverbs form keeps
# the field's trailing paseq so that the closing bracket falls after it: between
# the word and the paseq, the bracket would sit inside the page's right-to-left
# element (py_render/uc_hebrew_runs) and display mirrored.
_PSALMS_31_24_1 = (
    hl.ALEF
    + hpo.MTGOSLQ
    + hpo.SEGOL_V
    + hl.HE
    + hpo.XSEGOL
    + hl.BET
    + ha.MER
    + hl.VAV
    + hpo.DAGOMOSD
)
_PROVERBS_30_15_1 = (
    hl.LAMED
    + hpo.MTGOSLQ
    + hpo.PATAX
    + hl.AYIN
    + hpo.XPATAX
    + hl.LAMED
    + hl.VAV
    + hpo.DAGOMOSD
    + hl.QOF
    + hpo.QAMATS
    + ha.QOM
    + hl.HE
    + hpu.PASOLEG
)

# Keyed by (case reference, field label). The reference is spelled as
# uxlc_email_extract.CaseRef.key spells it, and the label is the message's own.
CASE_FIELD_CORRECTIONS = {
    ("Judges 11:24.7", "Note"): (BracketedCorrection("Tet", "Tav"),),
    ("Psalms 31:24.1", "Current UXLC"): (
        BracketedCorrection(
            _PSALMS_31_24_1,
            _with_cgj_after_meteg(_PSALMS_31_24_1),
            "with a CGJ added after the meteg, as the UXLC had it, so that the meteg"
            " stands right of the segol",
            quote_original=False,
        ),
    ),
    ("Proverbs 30:15.1", "Current UXLC"): (
        BracketedCorrection(
            _PROVERBS_30_15_1,
            _with_cgj_after_meteg(_PROVERBS_30_15_1),
            "with a CGJ added after the meteg, as the UXLC had it, so that the meteg"
            " stands right of the pata\N{LATIN SMALL LETTER H WITH DOT BELOW}",
            quote_original=False,
        ),
    ),
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
        f" {_shown_as(correction)}"
        for source_email in emails
        for correction in EMAIL_SUBJECT_CORRECTIONS.get(source_email.key, ())
    ]
    phrases.extend(
        f"on the {label} line of {book_display_name(case.ref.book)}"
        f" {case.ref.chapter}:{case.ref.verse}, {_shown_as(correction)}"
        for case in cases
        for label, _value in case.fields
        for correction in CASE_FIELD_CORRECTIONS.get((case.ref.key, label), ())
    )
    return tuple(phrases)


def _shown_as(correction: BracketedCorrection) -> str:
    if not correction.quote_original:
        return f"{correction.bracketed} is the message's word {correction.explanation}"
    phrase = f"{correction.original} is shown as {correction.bracketed}"
    if correction.explanation:
        return f"{phrase}, {correction.explanation}"
    return phrase


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
