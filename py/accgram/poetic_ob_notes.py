"""Hand-authored structured research notes for poetic ungrammatical verses.

The poetic ungrammatical set is small and closed, and most cases need no hand
annotation: the mechanically auto-derived WLC-vs-MAM-simple summary
(``poetic_oddball_summary.derive_tentative_summary``) is the relevant datum.
This module is the optional prose-style annotation layer for the few ungrammatical verses
that warrant more — the poetic analogue of the per-book ``ob_notes_*`` modules
the prose ``goerwitz.html`` report consumes via ``prose_ob_notes.get_structured_text``.

Entries are keyed by the two-letter ``bb`` reference form ("jb 31:15") that
``poetic_oddballs._bb_ref`` produces, and may carry the same fields the prose
report understands. The poetic report currently renders:

  * ``st-summary``      -- a hand-authored summary, shown alongside the
    auto-derived one (labelled to distinguish the two).
  * ``comment``         -- review prose; a string, or a list/tuple of items
    (each item a string or a sequence of inline HTML contents) rendered one
    paragraph apiece (see ``rtmsr_media.render_comment_paragraphs``).
  * ``uxlc_note_page``  -- external tanach.us UXLC note URL, linked next to the
    Mwd/UXLC reference links.
  * ``github-issue``    -- external GitHub issue URL, linked likewise.
  * ``img``             -- a Leningrad-Codex image filename under ``gh-pages/img/``
    (the ``LC-<folio>-col-<n>-line-<n>-<ref>.png`` form), shown with an auto-derived
    source caption; ``Da-at Miqra img`` / ``Aleppo img`` add a captioned companion
    image (see ``rtmsr_media.render_image_paragraphs``).
"""

from __future__ import annotations

from accgram.prose_ob_notes_shared import (
    DEXI,
    MUNAX,
)

from py_html import wlc_utils_html

_JOB_31_15_NOTE_URL = "https://tanach.us/Notes/Job/Job.31.15.1-t.html"


# NOTE: Ps 17:14 (the unique double tsinnor) once had an entry here, but the
# checker now accepts that verse (poetic_ply_grammar.parse_tokens_accepting_repeats
# collapses the repeated divider), so it no longer surfaces as a poetic ungrammatical and
# this layer can no longer render notes for it.  Its manuscript / MAM / Breuer
# discussion, plus the LC and S1 images, now live on the hand-authored page
# gh-pages/wlc/accgram/ps17v14-double-tsinnor.html.
BY_REF: dict[str, dict[str, object]] = {
    "ps 56:10": {
        "st-summary": (
            "On the verse-initial chanted word אָ֥֨ז, WLC transcribes TWO "
            "accents on the one alef — a merkha (below) and a qadma/azla (above). "
            "(This transcription is plausible but uncertain: see the LC image and its "
            "discussion below.) MAM "
            "has the azla alone; according to Breuer, the Aleppo Codex likewise has "
            "azla and Sassoon 1053 has merkha. The checker fuses the pair into one "
            "order-less merkha!azla bang-pair and flags the verse as a lexical anomaly: "
            f"only a few accent pairs (revia + geresh muqdam, {DEXI} + {MUNAX}, oleh + yored) "
            "may legitimately share one letter, and merkha + azla is not among them."
        ),
        "img": "LC-376B-col-2-line-5-Ps-56v10.png",
        "Da-at Miqra img": "Da-at-Miqra-Ps-56v10.png",
        "comment": (
            "Across the sources the two marks split cleanly one-each: MAM has azla; "
            "according to Breuer, the Aleppo Codex likewise has azla and Sassoon 1053 has "
            "merkha. That the LC has BOTH, on a single letter, could be an attempt to "
            "preserve two single-accent traditions — recording the two options rather than "
            "choosing.",
            "The upper mark (transcribed as the qadma/azla) is in any case oddly placed "
            "and oddly shaped; it could as easily be a misshapen part of the alef as a "
            "deliberate accent — so even the azla half of the supposed pair is uncertain, "
            "much as the Job 31:15 geresh muqdam is.",
            "The checker represents the cluster faithfully as one merkha!azla bang-pair "
            "but does NOT bless it grammatically (it is not a licit servus), so the verse is a "
            "NO_PARSE ungrammatical verse rather than a silently-clean parse. Each of the four "
            "interpretations — merkha alone, azla alone, and the two orderings as a "
            "sequence — does parse, but only weakly: our poetic conjunctive grammar is "
            "permissive, so it cannot yet make “both options are well-formed” a strong "
            "claim. Strengthening that is a noted, separate direction.",
        ),
    },
    "jb 31:15": {
        "uxlc_note_page": _JOB_31_15_NOTE_URL,
        "st-summary": (
            "On the verse-initial chanted word, WLC transcribes a malformed mark — absent "
            "from MAM (and from BHL) — that the UXLC note page (linked above) flags "
            "with a transcription-uncertainty marker."
        ),
        "comment": (
            [
                "The UXLC ",
                wlc_utils_html.anchor(
                    "note for this verse", {"href": _JOB_31_15_NOTE_URL}
                ),
                " describes the mark WLC transcribes here as a geresh muqdam of “a "
                "very odd shape,” a vertical straight line arising from the top front "
                "of the he, and flags it with a transcription-uncertainty “t” marker; "
                "BHL lacks the geresh muqdam entirely.",
            ],
            "In my opinion, to transcribe this mark at all is uncharitable. To "
            "continue to transcribe it with the benefit of the high-resolution color "
            "images now available seems not just uncharitable but aggressively "
            "uncharitable, almost absurd.",
        ),
    },
}


def get_structured_text() -> dict[str, dict[str, object]]:
    return BY_REF
