"""Ben Denckla's corrections to Holman's MAM suggestions.

The same shape, and for the same reason, as ``uxlc_bracketed_corrections`` beside
this file: the extract holds what Holman sent, so a line or a form of his that is
wrong stays wrong unless something says otherwise, and this is that something.
Each entry replaces one field of one case, keeps what he sent under an ``_as_sent``
key, and names Ben as the corrector, because the data alone cannot say whose words
these are.  Two entries stand: a line of prose for Zechariah 2:4 and a quoted form
for Joshua 10:12, both described below.

HOLMAN DID NOT CORRECT THIS HIMSELF, AND THE RECORD MUST NOT IMPLY THAT HE DID.
Checked 2026-09-02 across the whole mailbox: "Place Mereka on first syllable" for
Zechariah 2:4 occurs in exactly one message, the one of 2026-08-27, in both its body
and its attached workbook.  The message of 2026-08-21 carries the same four cases
with NO suggestion column at all, so it neither states nor corrects the line;
every other occurrence in the mailbox is the 2026-08-27 message quoted back inside a
reply.  There is no follow-up in which he revises it.  Attributing the correction to
him would be a false statement about a third party's words, which is worse than the
error it would tidy away.

WHAT IS WRONG WITH THE ZECHARIAH 2:4 LINE, twice over.  The mark in question is
U+05A3 munaḥ, not the merkha that "Mereka" names -- the Judges 10:11 row, whose
suggestion is worded identically, genuinely is a merkha, which is where the
wording looks to have been carried down from.  And MAM already has that mark on the
first syllable of זֵרוּ, the comparison edition having it on the second, so the line
as sent describes MAM's existing state rather than the change toward that edition.
The corrected wording names the mark and the syllable the change actually moves it to.

WHAT IS WRONG WITH THE JOSHUA 10:12 FORM, and why it is a slip of the same kind.
That case's comparison form spells the stress helper of the pashta as U+05A8 qadma,
where MAM spells it as a second U+0599 pashta.  Measured 2026-09-02 over
MAM-parsed/plus: 3,824 atoms have two U+0599, and only two have a qadma before a
pashta -- וְי֨וֹם֙ at Exodus 20:9 and at Deuteronomy 5:13, one in each Decalogue's
combined cantillation.  Holman's suggestion for the case reads "Add helper accent",
which is that doubled pashta, so the qadma is a typing slip rather than a proposal
to use Unicode QADMA.  Ben Denckla settled it on 2026-09-02: "I am 100% sure he
wasn't honestly suggesting use of Unicode QADMA."

THE CORRECTED FORM DOES NOT REACH ``mam_plus_check``, and that is a limitation
rather than a choice.  ``main_ingest_mam_suggestions`` calls ``check_case`` on the
case as extracted and applies this table to the payload afterwards, so the
``comparison_form_already_present`` reported for Joshua 10:12 still asks whether
MAM has the qadma spelling, which it never will.  The atom index is unaffected --
both spellings differ from the MAM form in the same single atom -- so only that one
flag is wrong, and it reads false today for the separate reason that the local
MAM-parsed predates the Wikisource edit of 2026-08-28.

Applying an entry is fail-fast in both directions.  A replacement whose original is
not the field's exact current value raises, so a reworded message cannot leave a
correction silently unapplied; and an entry naming no case or no field raises, so a
mistyped key is loud.
"""

from __future__ import annotations

from dataclasses import dataclass

CORRECTOR = "Ben Denckla"

# Joshua 10:12.3's comparison form, in the spelling sent and in the corrected one.
# EVERY MARK IS A NAMED ESCAPE, for two reasons.  U+05A8 and U+0599 are hard to
# tell apart in a literal, and which of the two is meant is the whole of this
# correction.  And the shin dot precedes the qubuts here, which is MAM-normal
# mark order rather than the Unicode-normal order a keyboard or a paste through
# anything that normalizes will produce -- typing the stem instead of spelling it
# put the qubuts first, and the fail-fast check below is what caught it.
_JOSH_STEM = (
    "י\N{HEBREW POINT SHEVA}"
    "ה"
    "ו\N{HEBREW POINT HOLAM}"
    "ש\N{HEBREW POINT SHIN DOT}\N{HEBREW POINT QUBUTS}"
)
_JOSH_TAIL = "ע\N{HEBREW POINT PATAH}\N{HEBREW ACCENT PASHTA}"
_JOSH_AS_SENT = _JOSH_STEM + "\N{HEBREW ACCENT QADMA}" + _JOSH_TAIL
_JOSH_CORRECTED = _JOSH_STEM + "\N{HEBREW ACCENT PASHTA}" + _JOSH_TAIL


@dataclass(frozen=True)
class FieldCorrection:
    """One field of Holman's, the wording shown instead, and why."""

    original: str
    replacement: str
    reason: str


# Keyed by (case reference as Holman sent it, field name in the case payload).
# The reference is spelled with HIS atom index, not the derived one, so that an
# entry keeps naming the same case if a derivation later moves the index.
CASE_FIELD_CORRECTIONS: dict[tuple[str, str], FieldCorrection] = {
    ("Zech 2:4.11", "suggestion"): FieldCorrection(
        original="Place Mereka on first syllable",
        replacement="Place Munaḥ on second syllable",
        reason=(
            "The mark is a munaḥ, not a merkha, and MAM already has it on the "
            "first syllable of זֵרוּ; the comparison edition has it on the second. "
            "The wording as sent looks carried down from the Judges 10:11 row, "
            "where the mark genuinely is a merkha and 'first syllable' is right."
        ),
    ),
    ("Josh 10:12.3", "comparison_form"): FieldCorrection(
        original=_JOSH_AS_SENT,
        replacement=_JOSH_CORRECTED,
        reason=(
            "MAM spells the stress helper of a pashta as a second U+0599 "
            "pashta, not as the U+05A8 qadma the form as sent has. Measured "
            "2026-09-02 over MAM-parsed/plus, 3,824 atoms have two U+0599, "
            "while only two have a qadma before a pashta: וְי֨וֹם֙ at Exodus "
            "20:9 and at Deuteronomy 5:13, one in each Decalogue's combined "
            "cantillation. Holman's suggestion for this case reads 'Add helper "
            "accent', and the helper he means is that doubled pashta; the "
            "qadma is a slip of the same kind as the 'Mereka' of Zechariah 2:4 "
            "above, not a proposal to use Unicode QADMA."
        ),
    ),
}


def apply_corrections(payload: dict[str, object], ref_as_sent: str) -> None:
    """Correct one case's payload in place, recording what was replaced.

    Adds ``<field>_as_sent`` holding Holman's wording, and a ``corrections`` list
    naming the field, the corrector and the reason, so a reader of the extract can
    see that the line was changed and by whom without opening this file.
    """
    corrections: list[dict[str, str]] = []
    for (case_ref, field), correction in CASE_FIELD_CORRECTIONS.items():
        if case_ref != ref_as_sent:
            continue
        if field not in payload:
            raise ValueError(
                f"correction for {case_ref} names field {field!r}, which the case "
                "payload does not have"
            )
        current = payload[field]
        if current != correction.original:
            raise ValueError(
                f"correction for {case_ref} field {field!r} expected "
                f"{correction.original!r} but found {current!r}; the message has "
                "been reworded, so re-read it before changing this entry"
            )
        payload[field] = correction.replacement
        payload[f"{field}_as_sent"] = correction.original
        corrections.append(
            {
                "field": field,
                "corrected_by": CORRECTOR,
                "reason": correction.reason,
            }
        )

    if corrections:
        payload["corrections"] = corrections


def require_every_correction_applied(applied_keys: set[tuple[str, str]]) -> None:
    """Raise unless every table entry fired, so a stale key cannot sit unnoticed."""
    unused = set(CASE_FIELD_CORRECTIONS) - applied_keys
    if unused:
        raise ValueError(
            f"corrections naming no case in this mailbox: {sorted(unused)}"
        )
