"""Contextual links a MAM-suggestion card may carry, keyed by Holman's own reference.

WHY THIS IS RENDERER-OWNED AND NOT IN THE DATA.  ``holman/docs-not-served/mam_suggestions.json``
is derived from Holman's messages: it holds what he sent and what the ingest derived from it.
A link to a page this repository published later is neither, so putting one there would mix an
explanation written afterwards into the extracted record.  The map lives here instead, beside
the renderer that emits it, and the extract stays what it says it is.

KEYED BY THE REFERENCE AS SENT, never by the M number.  ``M23`` is an ordinal the renderer
prints from ``case_number``; the reference is the stable thing about a case.  The card resolves
``ref_as_sent`` before ``ref`` and this lookup reads the same value, so the two cannot come to
disagree about which case is which -- the same keying, and the same reason for it, as
``rt_mam_suggestion_card.EXTRA_LETTER_SPACING_REFS``.

ONE ENTRY, AND A CARD WITH NO ENTRY GETS NO LINK.  Nothing here derives a link from a case's
contents: a card carries one only if its reference is written out below.
"""

from __future__ import annotations

from dataclasses import dataclass

from author_site import site_data


@dataclass(frozen=True)
class ContextLink:
    """A neutral pointer from a card to a page that gives its mark some background."""

    label: str
    href: str


# The published survey of MAM's metegs after the primary stress, which is where a reader of
# M23's card learns what kind of meteg the case is about and how common that kind is.
#
# The href is a sibling-directory hop: the Holman pages are published under gh-pages/holman/
# and the survey at the deploy root, so ``../`` reaches it.  Its three parts are the site's own
# constants rather than a string typed here, so a rename of the page cannot leave this pointing
# at nothing.
_POST_STRESS_METEG = ContextLink(
    label=site_data.POST_STRESS_METEG_TITLE,
    href=f"../{site_data.POST_STRESS_METEG_FNAME}#{site_data.POST_STRESS_METEG_M23_ID}",
)

CONTEXT_BY_REF: dict[str, ContextLink] = {
    # M23, Isaiah 23:12 -- the one suggestion of the thirty that ADDED a meteg, and the
    # occasion for the survey the link points at.
    "Isa 23:12.11": _POST_STRESS_METEG,
}


def context_link_for(ref_as_sent: str) -> ContextLink | None:
    return CONTEXT_BY_REF.get(ref_as_sent)
