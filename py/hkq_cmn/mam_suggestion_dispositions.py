"""What has been decided about a MAM suggestion, where anything has been.

A suggestion arrives as Holman's proposal and stays open until somebody rules on
it.  This is where a ruling is written down: which case, what was decided, why,
and who decided it.  The extract carries the ruling per case and the report routes
a suppressed case to its Suppressed page, so a reader of either sees the decision
beside the suggestion rather than having to know it.

WHY THE REASONS CITE SETH (AVI) KADISH BY NAME, when the ingest beside this file
goes to some trouble to store nothing he wrote.  Those are two different things,
and Ben Denckla drew the line between them on 2026-09-02: what must not leave the
mailbox is Avi's PERSONAL correspondence -- being too busy to work through a batch
of suggestions, and the like.  His SUBSTANTIVE judgments about the text are the
opposite case: they are the reason a suggestion is settled, they are worth
attributing to him rather than presenting as though nobody in particular reached
them, and Ben asked outright that they be cited.

So a reason here may quote and attribute his scholarly point.  It may not carry
anything about his availability, his circumstances, or anyone else's.  The same
holds for Ben's own remarks.  ``mam_suggestion_extract``'s module docstring states
the boundary the ingest keeps; this is the one exception to it, and it is narrow.

SUPPRESSED MEANS HANDLED, AND DELIBERATELY DOES NOT SAY HOW.  Ben Denckla settled
this on 2026-09-02, having been asked: a handled suggestion may have been
accepted, rejected, or something in between such as partially taken, and the
report does not distinguish those.  ``state`` therefore has one value and is
expected to keep having one.  **Do not add ``accepted`` and ``declined``**, or the
report grows a distinction its ketiv/qere half cannot make: those rows are
suppressed off a closed GitHub issue, `is_closed` is a bare boolean, and all 21
closed issues carry GitHub's default `COMPLETED` reason, `NOT_PLANNED` never
having been used.  Half a page able to say which kind of closure a record got is
worse than neither half saying it.

What carries the how is ``summary`` and ``reason``, in prose, per case.  That is
the right place for it because the answer is rarely one of two words: of the
eighteen ketiv/qere rows suppressed as of 2026-09-02, twelve close on a Wikisource
diff, two by pointing at a `bdenckla/mgketer` issue, two on an accepted judgment,
one on a rejection of Holman's framing that still produced a note, and one on a
research aside that states no disposition at all.

THE PHONETIC TANAKH IS NOT MENTIONED IN A REASON, and this is a decision rather
than an oversight.  Two of the Jerusalem Crown cases carry a note in the mailbox,
Ben Denckla's own, saying the fix is needed in the Phonetic Tanakh as well.  It
was put to him on 2026-09-02 as a candidate for the reasons here and he declined
it: *"Thanks for raising the possibility that Phonetic Tanakh should be mentioned
here, but I've decided it should not be mentioned here."*  A reason says what was
decided about the suggestion; a downstream edition's own to-do is a different
matter and does not belong on these cards.  Do not re-propose it.

A SUPPRESSED CASE IS NOT A DELETED ONE.  It keeps its card, its crop and its
number, and moves to the Suppressed page beside the ketiv/qere rows whose issues
are closed.  Suppression says the suggestion has been handled, not that it was
never made.
"""

from __future__ import annotations

from dataclasses import dataclass

# The only state there is, and the module docstring says why a second one would be
# a mistake rather than an improvement.
SUPPRESSED = "suppressed"


@dataclass(frozen=True)
class Disposition:
    """One ruling on one suggestion.

    ``outcome`` is FREE PROSE AND NOT AN ENUM, which is the same decision as the
    one about ``state`` above seen from the other side.  Ben Denckla asked on
    2026-09-02 that it lead with the suggestion's fate -- "Suggestion taken",
    "Suggestion not taken" -- and the point of leaving it as text is that a third
    and a fourth are expected: "Suggestion partly taken" is the case he named
    outright, and a suggestion right about the problem and wrong about the fix
    would want wording of its own again.  ``state`` does the routing; ``outcome``
    tells the reader what happened; neither is a substitute for the other.

    It is also the card's LABEL for the summary line, so it is written without
    trailing punctuation and reads as one: "Suggestion not taken: MAM is right;
    the geresh is misplaced in the Jerusalem Crown."
    """

    state: str
    outcome: str
    summary: str
    reason: str
    decided_by: str
    decided_on: str

    def payload(self) -> dict[str, str]:
        return {
            "state": self.state,
            "outcome": self.outcome,
            "summary": self.summary,
            "reason": self.reason,
            "decided_by": self.decided_by,
            "decided_on": self.decided_on,
        }


# Keyed by the case reference as Holman sent it, which is what the corrections
# table beside this one is keyed by too, so that a derived atom index moving does
# not orphan an entry.
DISPOSITION_BY_REF: dict[str, Disposition] = {
    "2Ki 17:15.15": Disposition(
        state=SUPPRESSED,
        outcome="Suggestion not taken",
        summary="MAM is right; the geresh is misplaced in the Jerusalem Crown",
        reason=(
            "The Aleppo Codex is not extant at this verse — its leaves jump "
            "from 2 Kings 14:21 to 18:13 — so the Leningrad Codex is the "
            "primary reference manuscript here. Seth (Avi) Kadish, 2026-08-28: "
            "the geresh appears to have been erased in the Leningrad Codex, and "
            "the UXLC has it that way, but even erased it stood over the כ "
            "(kaf) rather than over the final ו (vav). Avi notes the same "
            "misplacement onto the final ו (vav) in BHS and in Mechon Mamre, "
            "and takes the three editions sharing it as evidence that they "
            "share a source. Avi added a note in MAM about the geresh in the "
            "Leningrad Codex rather than moving the accent."
        ),
        decided_by="Seth (Avi) Kadish",
        decided_on="2026-08-28",
    ),
    "Josh 10:12.3": Disposition(
        state=SUPPRESSED,
        outcome="Suggestion taken",
        summary="MAM now has the pashta repeated over the ש (shin)",
        reason=(
            "Seth (Avi) Kadish, 2026-08-28: the word did not follow MAM's style "
            "guideline, which calls for the pashta to be repeated on the "
            "stressed syllable, and which is Breuer's guideline too. For this "
            "purpose a furtive pataḥ counts as a syllable of its own, so the "
            "stress on the שֻׁ (shu) is not final and the repetition is called "
            "for. Nothing in the manuscripts was at issue: Yeivin (ITM §239) "
            "names words with a furtive pataḥ among those whose pashta is "
            "repeated in the standard printed editions and in the Leningrad and "
            "Cairo codices, and describes the Aleppo Codex as repeating it only "
            "where at least one letter stands between the two letters that "
            "would carry it — and here the ש (shin) stands immediately before "
            "the ע (ayin). Avi made the "
            "[change](https://he.wikisource.org/w/index.php?title=%D7%99%D7%94%D7%95%D7%A9%D7%A2_%D7%99/%D7%98%D7%A2%D7%9E%D7%99%D7%9D&diff=3079454&oldid=3005767) "
            "on Hebrew Wikisource that day."
        ),
        decided_by="Seth (Avi) Kadish",
        decided_on="2026-08-28",
    ),
    "Judg 10:11.1": Disposition(
        state=SUPPRESSED,
        outcome="Suggestion not taken",
        summary="MAM is right; the merkha is misplaced in the Jerusalem Crown",
        reason=(
            "Seth (Avi) Kadish, 2026-08-28: the stressed syllable begins with "
            "the י (yod), so the merkha belongs where MAM has it, and the "
            "Aleppo Codex agrees. The Jerusalem Crown has it under the ו (vav) "
            "instead, an error Avi also finds in Mechon Mamre and one Avi notes "
            "the Jerusalem Crown rarely makes. Avi added documentation about it "
            "in MAM."
        ),
        decided_by="Seth (Avi) Kadish",
        decided_on="2026-08-28",
    ),
    "Zech 2:4.11": Disposition(
        state=SUPPRESSED,
        outcome="Suggestion taken",
        summary="MAM now has the munaḥ on the ר (resh)",
        reason=(
            "The Aleppo Codex is not extant at this verse — its leaves jump "
            "from Zephaniah 3:20 to Zechariah 9:17 — so the Leningrad Codex is "
            "the primary reference manuscript here. Seth (Avi) Kadish, "
            "2026-08-28: the munaḥ belongs on the ר (resh), as expected and as "
            "in the Leningrad Codex. Avi made the "
            "[change](https://he.wikisource.org/w/index.php?title=%D7%96%D7%9B%D7%A8%D7%99%D7%94_%D7%91/%D7%98%D7%A2%D7%9E%D7%99%D7%9D&diff=3079481&oldid=2988137) "
            "on Hebrew Wikisource that day. Note that the accent being moved is "
            "a munaḥ, not a merkha: Holman accidentally described his "
            "suggestion as moving a merkha, which this word does not have."
        ),
        decided_by="Seth (Avi) Kadish",
        decided_on="2026-08-28",
    ),
}


def apply_disposition(payload: dict[str, object], ref_as_sent: str) -> bool:
    """Attach this case's ruling, if it has one. True when one was attached."""
    disposition = DISPOSITION_BY_REF.get(ref_as_sent)
    if disposition is None:
        return False
    payload["disposition"] = disposition.payload()
    return True


def require_every_disposition_applied(applied_refs: set[str]) -> None:
    """Raise unless every table entry fired, so a stale key cannot sit unnoticed."""
    unused = set(DISPOSITION_BY_REF) - applied_refs
    if unused:
        raise ValueError(
            f"dispositions naming no case in this mailbox: {sorted(unused)}"
        )


def is_suppressed(case: dict[str, object]) -> bool:
    disposition = case.get("disposition")
    return isinstance(disposition, dict) and disposition.get("state") == SUPPRESSED
