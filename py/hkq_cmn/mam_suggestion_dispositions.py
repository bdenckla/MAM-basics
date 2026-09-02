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
    """One ruling on one suggestion."""

    state: str
    summary: str
    reason: str
    decided_by: str
    decided_on: str

    def payload(self) -> dict[str, str]:
        return {
            "state": self.state,
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
        summary="MAM is right; the geresh is misplaced in the Jerusalem Crown",
        reason=(
            "Seth (Avi) Kadish, 2026-08-28: the geresh appears to have been erased "
            "in the Leningrad Codex, and the UXLC has it that way, but even erased "
            "it stood over the כ rather than over the final ו. He notes the same "
            "misplacement onto the final ו in BHS and in Mechon Mamre, and reads "
            "the three editions sharing it as evidence that they share a source. "
            "He added a note in MAM about the geresh in the Leningrad Codex rather "
            "than moving the accent."
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
