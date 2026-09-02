"""What kind of thing each record on the findings report is, and the filter that says so.

THE REPORT HOLDS TWO BODIES OF HOLMAN'S WORK SINCE 2026-09-02, on Ben Denckla's
instruction of that date, and this module is the dimension that tells them apart:
the 77-row ketiv/qere review extracted from his ``.docx``, and the suggested
corrections to MAM extracted from his emails.  They are shown on one page and
separated by a filter rather than by two pages, so that a reader can see either
body alone or both together without navigating.

The kinds partition the page: every card carries exactly one, so the counts in the
"Suggestion kind" group add up to the card count.

WHY THE MAM SUGGESTIONS SPLIT INTO TWO KINDS, AND WHY THE SPLIT IS DERIVED.  The
34 cases divide into ones about a meteg and ones about where an accent sits, and
that division is worth filtering on because it is what decides how hard a case is
to act on -- Ben, in the message that started this work, distinguished the clear
wins from the ones needing a merkha-versus-meteg judgment call.  Deriving the
division from the two forms Holman supplies rather than from which edition he
compares against is what keeps it honest: today every meteg case happens to be an
Aleppo Codex comparison and every accent-placement case a Jerusalem Crown one, and
a classification keyed to the edition would silently mislabel the first message
that breaks that coincidence.
"""

from __future__ import annotations

METEG = "\N{HEBREW POINT METEG}"

KETIV_QERE_KIND = "ketiv-qere"
METEG_KIND = "meteg"
ACCENT_PLACEMENT_KIND = "accent-placement"

# Display order, which is also the order the summary group lists them in.
KIND_ORDER = (KETIV_QERE_KIND, METEG_KIND, ACCENT_PLACEMENT_KIND)

KIND_DISPLAY_TEXT = {
    KETIV_QERE_KIND: "ketiv/qere",
    METEG_KIND: "meteg",
    ACCENT_PLACEMENT_KIND: "accent placement",
}


def kind_filter_id(kind: str) -> str:
    if kind not in KIND_DISPLAY_TEXT:
        raise ValueError(f"unknown record kind {kind!r}")
    return f"kind-{kind}"


def kind_display_text(kind: str) -> str:
    try:
        return KIND_DISPLAY_TEXT[kind]
    except KeyError as exc:
        raise ValueError(f"unknown record kind {kind!r}") from exc


def suggestion_kind(mam_form: str, comparison_form: str) -> str:
    """Whether a MAM suggestion is about a meteg or about where an accent sits.

    A meteg case is one whose two forms become equal once every meteg is dropped
    from both -- so the meteg is the whole of the difference.  Everything else is
    an accent-placement case, which is what the four Jerusalem Crown cases are: a
    qadma added, and a merkha, a geresh and a munaḥ each sitting on a different
    letter in the two editions.

    Note that a meteg is not an accent, which is why the two kinds are named as
    they are rather than as two kinds of accent difference.
    """
    if mam_form.replace(METEG, "") == comparison_form.replace(METEG, ""):
        return METEG_KIND
    return ACCENT_PLACEMENT_KIND
