"""Attachments whose filename does not name the case they belong to.

Holman names an attachment after its case -- ``Josh 20.4.12 Daat Miqra.png`` --
and ``uxlc_email_extract._assign_images`` reads the case out of the filename. A
message with a single case may attach whatever it likes, because there is only
one case for an image to belong to. In a multi-case message a filename naming no
case, or naming a case the message does not write up, is an error rather than a
guess, and the two tables here are where such a filename is decided instead.

Both tables are keyed by the attachment filename as it arrives, and both raise
on an entry no message has, so a filename that changes is loud rather than
silently inert.
"""

from __future__ import annotations

# An image whose filename names something other than its own case. The value is
# the case it belongs to, keyed as uxlc_email_extract.CaseRef.key spells a
# reference.
#
# Holman's Job message of 2026-08-09 attaches an image of Job 14:19 to his Job
# 30:1.2 case, whose Note ends "Compare UXLC (with Merekha) in Job 14:19." The
# filename names the word he is comparing against, not the word the case is
# about, and Job 14:19 is not a case in that message.
COMPANION_IMAGE_CASES = {
    # Holman's filename verbatim, so the agentive "reads" is his and not ours.
    "Job 14.19 where UXLC reads as Merekha.png": "Job 30:1.2",  # prose-ok
}

# An image naming a case its message does not write up at all, so there is
# nothing for it to belong to. These are not written out by the ingest step and
# do not reach the page.
#
# Holman's "28 Suggested Corrections (Psalms Part 2 of 2)" of 2026-08-11
# attaches 29 images: one per case, plus this one. Its subject line, its
# preamble and its numbering all say 28, and the body has 28 cases ending at Ps
# 143:10.2, with no mention of Ps 140:4 anywhere. So the image is of a case that
# was not written up, rather than a case whose write-up was mislaid.
IMAGES_WITH_NO_CASE = {
    "Ps 140.4.1.png": (
        "Attached to the Psalms Part 2 message, which writes up no Ps 140 case."
    ),
    # The Jeremiah message of 2026-08-12 says "24 proposed suggested
    # corrections" and writes up 24, attaching 24 images -- but the two sets do
    # not line up: it writes up Amos 8:12.8 and attaches no image of it, and
    # attaches this image and writes up no Ezek 10:3 case. Ezekiel 10 is not
    # mentioned anywhere in the body.
    "Ezek 10.3.2.png": (
        "Attached to the Jeremiah/Ezekiel/Minor Prophets/Daniel message, which "
        "writes up no Ezek 10:3 case."
    ),
}


def require_known_attachments(source_filenames: list[str]) -> None:
    """Raise on a table entry naming an attachment no message has."""
    present = set(source_filenames)
    for table, name in (
        (COMPANION_IMAGE_CASES, "COMPANION_IMAGE_CASES"),
        (IMAGES_WITH_NO_CASE, "IMAGES_WITH_NO_CASE"),
    ):
        unmatched = sorted(set(table) - present)
        if unmatched:
            raise ValueError(f"{name} names attachments no message has: {unmatched}")
