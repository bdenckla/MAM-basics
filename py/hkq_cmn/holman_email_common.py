"""Message-level helpers shared by the two Holman ingests, and the address boundary they keep.

holman-ketiv-qere is public and every ``.eml`` Holman sends carries his address,
his other correspondents' and Ben Denckla's.  The rule both ingests keep is that
nothing derived from a mail header reaches a tracked file except the sender's
display name and the message's subject and date -- ``sender_display_name`` below
raises rather than let a ``From`` with no display name through, which is what
makes the rule enforced rather than merely intended.

WHY THIS MODULE DUPLICATES FIVE PRIVATE FUNCTIONS OF ``uxlc_email_extract``
RATHER THAN THAT MODULE IMPORTING FROM HERE.  It should not, and the end state
is that ``uxlc_email_extract`` uses these and its own copies go.  That change was
deliberately not made on 2026-09-02, when this module was written: a second
session was live in the same two repos, working on a new UXLC correction
message, so editing the file it was in would have traded a tidier tree for a
merge conflict in the one file both sessions wanted.  The duplication is ~40
lines, it is confined to this file, and undoing it is a one-file edit.  Do that
when no other session is in ``uxlc_email_extract``.
"""

from __future__ import annotations

from datetime import datetime, timezone
import email.message
import email.utils
from pathlib import Path
import re

NON_SLUG_RE = re.compile(r"[^a-z0-9]+")


def sender_display_name(from_header: object) -> str:
    """The From header's display name, never its address."""
    display_name, address = email.utils.parseaddr(str(from_header))
    if not display_name or "@" in display_name:
        raise ValueError(
            f"From header has no address-free display name: {address!r}. "
            "This repo is public; supply the name rather than letting an "
            "address reach the derivative."
        )
    return display_name


def email_key(path: Path) -> str:
    """A filename reduced to a slug, which is how a message is named downstream."""
    key = NON_SLUG_RE.sub("-", path.stem.lower()).strip("-")
    if not key:
        raise ValueError(f"{path.name}: filename reduces to an empty email key")
    return key


def parts_of_type(message: email.message.EmailMessage, content_type: str) -> list[str]:
    """Every non-attachment part of one content type, decoded."""
    return [
        part.get_content()
        for part in message.walk()
        if part.get_content_type() == content_type and part.get_filename() is None
    ]


def plain_text_body(message: email.message.EmailMessage, path: Path) -> str:
    """The message's one text/plain part, or None when it has none.

    Unlike ``uxlc_email_extract``'s counterpart this does NOT fall back to
    reading the HTML, because the caller here needs to know which it got: a
    Holman message whose cases are in the body is plain text, and one whose
    cases are in an attached workbook has an HTML body carrying only a greeting.
    Returning HTML-read-as-text for the second would make the two shapes look
    alike at exactly the point the caller is telling them apart.
    """
    bodies = parts_of_type(message, "text/plain")
    if len(bodies) > 1:
        raise ValueError(
            f"{path.name}: {len(bodies)} text/plain parts; decide which is the "
            "message body before ingesting it"
        )
    return bodies[0] if bodies else ""


def utc(when: datetime) -> datetime:
    """An aware UTC datetime, tolerating the naive result of a -0000 header."""
    if when.tzinfo is None:
        return when.replace(tzinfo=timezone.utc)
    return when.astimezone(timezone.utc)


def message_date(message: email.message.EmailMessage, path: Path) -> datetime:
    raw = message.get("Date")
    if raw is None:
        raise ValueError(f"{path.name}: message has no Date header")
    parsed = email.utils.parsedate_to_datetime(str(raw))
    return utc(parsed)
