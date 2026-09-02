"""Daniel Holman's suggested-UXLC-correction emails, ingested and parsed.

Each message from Daniel Holman to Chris Kimball and Ben Denckla proposes
corrections to the UXLC. The body is a short preamble, a run of per-atom cases,
and a sign-off. A case is a heading line followed by ``Label: value`` lines; the
label vocabulary drifts from message to message (``Word / Verse`` in one,
``Current Text`` in another), so the labels are kept verbatim rather than
normalized, and the renderer shows the email's wording.

The heading drifts too. It is usually the reference, numbered or not, and in
the Chronicles, Jeremiah, Job and Ezra messages it carries the word as well,
parenthesised or after an em dash -- which in those messages is the only place
the form as it stands is written, there being no ``Current UXLC`` line. In the
Proverbs message it is a bare ordinal and the reference is in the ``Verse``
field. The Jeremiah message additionally divides its cases by book, with
``JEREMIAH`` and its three fellows alone on a line; see
``_without_section_dividers``.

Two steps, because this repo is public and a .eml file's headers carry the
correspondents' addresses:

  ``ingest_eml_files``  reads the .eml files from a local, untracked mailbox and
    writes the tracked derivative: one address-redacted body text and one small
    metadata JSON per message, plus each attached PNG. Run it when a new message
    arrives; it is the only step that needs the mailbox. Where a message has no
    plain-text part -- true of every message from Psalms Part I onwards -- that
    body text is read out of the HTML by ``_text_from_html``, there being no
    original plain text to prefer.

    A PARTIAL MAILBOX IS THE ORDINARY CASE, not a broken one, and the step is
    built for it: a .eml is untracked, so it sits only on the machine the
    message was read on, and a second machine has whichever ones were forwarded
    there. Ingesting one message writes that message's derivative and leaves
    every other message's alone. The orphan check is made against the tracked
    derivative rather than against what the mailbox held, so it holds either
    way; the attachment-table check cannot be, and says in the summary whether
    it ran.

  ``read_emails``  reads that derivative. This is what the report is generated
    from, so a fresh clone can regenerate the page without the .eml files.

One thing is read out of a body rather than read off it: a Latin note letter
Holman's mail client embedded inside a Hebrew word, with the bidi controls that
carry it. See ``_without_embedded_note_letter``.

Parsing is deliberately fail-fast: an unrecognized field label, whether inside
a case or in the position that would have opened one, a heading whose reference
disagrees with its first field, an attachment that cannot be assigned to a
case, and a duplicate reference all raise rather than dropping content. What is
assumed rather than checked is that a field value is one line, and that the
prose after a message's last case is its sign-off.

What is NOT checked is that a case's atom index names the word the case quotes.
Measured 2026-08-12 against the UXLC core XML in the sibling UXLC-utils, 122 of
the 124 cases agree, and the two that do not differ only by a combining grapheme
joiner (Psalms 31:24.1 and Proverbs 30:15.1). Holman counts a ketiv/qere pair as
one atom, so the count his index is compared against has to do the same:
``uxlc_misc.my_uxlc.read_all_books`` instead drops the ``<k>`` and keeps every
``<q>``, which agrees with him wherever a pair is one of each and parts company
where it is not. Ezekiel 8:6 is the one case in the 124 where it is not -- that
verse's ketiv מהם has two qere atoms, מָ֣ה and הֵ֣ם -- and it was read as a real
disagreement until the numberings were worked out.

``CaseRef.atom`` is therefore Holman's and is left as he wrote it, which is what
makes it a stable key for everything filed against a case: his attachments are
named that way, and so are the tables in ``uxlc_change_records``,
``uxlc_holman_forms``, ``uxlc_attachment_notes`` and ``uxlc_comments``. It is
not the number a card shows. ``uxlc_standard_atoms`` holds that one, and sets
out the three numberings in play and how each was established.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import email
import email.message
import email.policy
import email.utils
import html
import json
from pathlib import Path
import re

from mb_cmn import bib_locales as tbn
from hkq_cmn.uxlc_atom_index_notes import (
    atom_index_for_verse_case,
    require_known_cases,
)
from hkq_cmn.uxlc_attachment_notes import (
    COMPANION_IMAGE_CASES,
    IMAGES_WITH_NO_CASE,
    require_known_attachments,
)

# The first labelled line of every case carries one of these labels. A heading
# is recognized by being the prose line directly above such a label.
FIRST_FIELD_LABELS = (
    "Word / Verse",
    "Word/Verse",
    "Current UXLC",
    "Current Text",
    "Verse",
    # From the Chronicles, Jeremiah, Job and Ezra messages of 2026-08-09 to
    # 2026-08-12 onwards, whose cases open on the manuscript citation: the word
    # itself is in the heading there rather than on a line of its own.
    "Image Location",
    "Image",
    # The 1 Samuel 28:12 message of 2026-08-23, a single-case message whose two
    # form lines are "Current" and "Change" and whose values sit on the line
    # BELOW the label -- see VALUE_ON_NEXT_LINE and _parse_case_region.
    "Current",
)
OTHER_FIELD_LABELS = (
    "Manuscript Image",
    "UXLC Image Location",
    "Location",
    # The Psalms messages' spelling. R and L are the recto and verso of the
    # leaf, not part of a column number.
    "Location R/L",
    "Suggested Correction",
    "Correction",
    "Corrected Text",
    "Target Text",
    # The 1 Samuel 28:12 message's spelling of the proposed form, a third
    # alongside "Corrected Text" and "Target Text"; uxlc_holman_forms names all
    # three in SUGGESTED_TEXT_LABELS.
    "Change",
    "Critical Note",
    "Note",
)
KNOWN_FIELD_LABELS = frozenset(FIRST_FIELD_LABELS + OTHER_FIELD_LABELS)

# Labels whose value names the Leningrad Codex image and column Holman worked
# from, e.g. "069_Exo_7.9b-8.3a / Col. 2 middle".
#
# The Psalms and Proverbs messages split that citation across two lines, the
# scan file under "Image" and the column under "Location" or "Location R/L",
# where every other message puts both on one. ``image_location`` joins whichever
# of these a case has, so the two halves reach the folio and column readers as
# the single string they are everywhere else.
IMAGE_LOCATION_LABELS = frozenset(
    (
        "Manuscript Image",
        "Image Location",
        "UXLC Image Location",
        "Image",
        "Location",
        "Location R/L",
    )
)

ADDRESS_REDACTION = "[address removed]"
BODY_SUFFIX = ".txt"
META_SUFFIX = ".json"

_ADDRESS_RE = re.compile(r"<?[\w.+-]+@[\w-]+(?:\.[\w-]+)+>?")
_LABEL_RE = re.compile(r"^\*?\s*(?P<label>[A-Za-z][A-Za-z /]*?):\s*(?P<value>.*)$")
# A heading's declared lead-in phrase, matched instead of the leading ordinal.
# The 1 Samuel 28:12 message of 2026-08-23 has one case and heads it with its
# own subject line, "UXLC Correction for 1Samuel 28:12", where every earlier
# message heads a case with the bare reference or with an ordinal before it.
# Declared rather than allowed for generally: the book group below is
# non-greedy, so any prose left in front of the reference would be swallowed
# into it and reach _bk39id, which would then raise on a book spelling nobody
# wrote.
_HEADING_LEAD_IN = r"UXLC\s+Correction\s+for\s+"
_HEADING_RE = re.compile(
    rf"^(?:\d+\.\s*|{_HEADING_LEAD_IN})?"
    r"(?P<book>.+?)\s+(?P<chapter>\d+):(?P<verse>\d+)"
    r"(?:\.(?P<atom>\d+))?"
    r"(?:\s*\(Word\s+(?P<atom_paren>\d+)\))?"
    # The Chronicles and Jeremiah messages put the word in parentheses after
    # the reference, the Job and Ezra ones after an em dash. It is the only
    # statement of the form as it stands in those messages, which have no
    # Current UXLC line, so the heading is what carries it onto the card.
    r"(?P<word>\s*(?:\([^)]*\)|\N{EM DASH}\s*\S.*|\N{EN DASH}\s*\S.*))?$"
)
# The Proverbs message numbers its cases and states the reference nowhere but
# the Verse field, so its headings are a bare ordinal.
_ORDINAL_HEADING_RE = re.compile(r"^\d+\.?$")
# "Ex 7:20.19 UXLC (word)" in the earlier messages, a bare "Prov 8:13.1" in the
# Proverbs one, so the UXLC that follows the reference is optional.
_FIRST_FIELD_REF_RE = re.compile(
    r"^(?P<book>.+?)\s+(?P<chapter>\d+):(?P<verse>\d+)\.(?P<atom>\d+)"
    r"(?:\s+UXLC\b|\s*$)"
)
# Holman names an attachment after the case it belongs to, with any remainder
# serving as its caption: "Josh 20.4.12 Daat Miqra.png".
_ATTACHMENT_REF_RE = re.compile(
    r"^(?P<book>(?:[12]\s?)?[A-Za-z]+)\s+"
    r"(?P<chapter>\d+)\.(?P<verse>\d+)\.(?P<atom>\d+)"
    r"(?P<caption>.*)$"
)
# One word in the Leviticus message, מַה־נֹּאכַל of Lev 25:20, carries the UXLC's
# note letter 'c' inside it, wrapped in the bidi controls Holman's mail client
# used to keep the Latin letter upright in a right-to-left word: LEFT-TO-RIGHT
# EMBEDDING, the letter, POP DIRECTIONAL FORMATTING, RIGHT-TO-LEFT MARK. The
# letter is the note's name, not part of the word, and it renders as a stray
# Latin letter mid-word, so it comes out along with the controls that carry it.
# Written as a named escape rather than a raw literal, which for an invisible
# character would be unreadable in the source and undiffable.
#
# The opener matched is any of the seven that start a directional run, not only
# the embedding this one message happens to use: another mail client wrapping
# the same single Latin letter in an isolate or an override is the same thing,
# and a shape that is genuinely different -- a control with no lone letter
# inside it -- still reaches the check below and raises.
_DIRECTIONAL_RUN_OPENERS = (
    "\N{LEFT-TO-RIGHT EMBEDDING}\N{RIGHT-TO-LEFT EMBEDDING}"
    "\N{LEFT-TO-RIGHT OVERRIDE}\N{RIGHT-TO-LEFT OVERRIDE}"
    "\N{LEFT-TO-RIGHT ISOLATE}\N{RIGHT-TO-LEFT ISOLATE}\N{FIRST STRONG ISOLATE}"
)
_DIRECTIONAL_RUN_CLOSERS = "\N{POP DIRECTIONAL FORMATTING}\N{POP DIRECTIONAL ISOLATE}"
_DIRECTION_MARKS = "\N{LEFT-TO-RIGHT MARK}\N{RIGHT-TO-LEFT MARK}"
_EMBEDDED_NOTE_LETTER_RE = re.compile(
    f"[{_DIRECTIONAL_RUN_OPENERS}]"
    r"\s*[A-Za-z]\s*"
    f"[{_DIRECTIONAL_RUN_CLOSERS}]"
    f"[{_DIRECTION_MARKS}]?"
)
# Every bidi formatting control, checked for after the removal above so that a
# future message embedding something in a shape this module does not know about
# raises rather than reaching the page as an invisible character.
_BIDI_CONTROL_RE = re.compile(
    f"[{_DIRECTIONAL_RUN_OPENERS}{_DIRECTIONAL_RUN_CLOSERS}{_DIRECTION_MARKS}]"
)
# A book divider in the Jeremiah message: capitals and spaces, alone on a line.
_SECTION_DIVIDER_RE = re.compile(r"^[A-Z][A-Z ]*$")
# The one divider that names a section of the canon rather than a single book.
_SECTION_DIVIDER_NAMES = frozenset(("MINOR PROPHETS",))
# Reading an HTML-only body as text. Every tag Holman's mail client emits that
# ends a line of what he typed, then everything else, which is font declarations.
_SCRIPT_OR_STYLE_RE = re.compile(
    r"(?s)<\s*(script|style)\b.*?</\s*\1\s*>", re.IGNORECASE
)
_LINE_ENDING_TAG_RE = re.compile(
    r"</\s*(?:div|p|tr|li|h[1-6]|table|blockquote)\s*>|<\s*br\s*/?\s*>", re.IGNORECASE
)
_ANY_TAG_RE = re.compile(r"<[^>]+>")
_BLANK_RUN_RE = re.compile(r"\n{3,}")
_NON_SLUG_RE = re.compile(r"[^a-z0-9]+")
_NORMALIZED_BOOK_TEXT_RE = re.compile(r"[^a-z0-9]")
_BK39ID_BY_NORMALIZED = {
    _NORMALIZED_BOOK_TEXT_RE.sub("", bk39id.lower()): bk39id
    for bk39id in tbn.ALL_BK39_IDS
}
# Tsefaniah is the one bk39 id that transliterates rather than anglicizes, so
# no prefix relates it to the "Zephaniah" Holman would write. This entry also
# reaches "Zeph" and "Zep" through the prefix branch of _bk39id.
_BK39ID_BY_NORMALIZED["zephaniah"] = tbn.BK_TSEF


def book_slug(book: str) -> str:
    """A bk39 id reduced to characters safe in an HTML id and a CSS class.

    "Song of Songs" is the one id with a space in it, which would otherwise
    split a whitespace-separated filter-id attribute and break a class selector.
    """
    return _NORMALIZED_BOOK_TEXT_RE.sub("", book.lower())


@dataclass(frozen=True)
class CaseRef:
    """An atom-level reference: book (a bk39 id), chapter, verse, atom index."""

    book: str
    chapter: int
    verse: int
    atom: int

    @property
    def key(self) -> str:
        """The stable key a commentary entry is filed under, e.g. Levit 7:25.6."""
        return f"{self.book} {self.chapter}:{self.verse}.{self.atom}"

    @property
    def sort_key(self) -> tuple[int, int, int, int]:
        return (tbn.get_bknu(self.book), self.chapter, self.verse, self.atom)


@dataclass(frozen=True)
class CaseImage:
    """One PNG Holman attached, assigned to the case its filename names.

    ``caption`` is what both the page and the JSON extract show, so it is
    settled here rather than in either of them: the remainder of the
    attachment's filename after the case reference, or the whole stem when the
    filename adds nothing to the reference or names no case at all.

    ``names_case_only`` marks that last-but-one kind -- a filename that is just
    the case reference, which is Holman's plain crop of the word. It orders
    first on the card, ahead of the companions he captions.
    """

    source_filename: str
    caption: str
    file_name: str
    names_case_only: bool


@dataclass(frozen=True)
class CorrectionCase:
    email_key: str
    index_in_email: int
    heading: str
    ref: CaseRef
    fields: tuple[tuple[str, str], ...]
    images: tuple[CaseImage, ...]

    @property
    def image_location(self) -> str | None:
        """Holman's manuscript citation, rejoined where his message split it.

        The Psalms and Proverbs messages put the scan file and the column on
        separate lines; everywhere else they are one line. Joining in the order
        the message states them puts the scan file first either way, which is
        what ``manuscript_page`` anchors on.
        """
        parts = [
            value for label, value in self.fields if label in IMAGE_LOCATION_LABELS
        ]
        return " ".join(part for part in parts if part) or None


@dataclass(frozen=True)
class SourceEmail:
    """One message, carrying no address.

    This repo is public, so nothing derived from a message here may hold a
    correspondent's address: only the sender's display name survives, the
    recipients are named in the page's prose rather than scraped from the To
    header, and every address in the body is replaced before the body is
    written out. Addresses live only in the .eml files, which is why those are
    kept outside the repo.
    """

    key: str
    source_file_name: str
    subject: str
    sender_name: str
    date_utc: datetime
    date_iso: str
    date_display: str
    preamble: tuple[str, ...]
    closing: tuple[str, ...]


def redact_addresses(text: str) -> str:
    """Replace every email address with a marker.

    Applied to a body the moment it is read, so no later stage can put an
    address on the page: one of these messages is a forward and quotes the
    original To and From lines in its body text. The replacement is visible
    rather than silent, because a reader should be able to tell that a line was
    edited.
    """
    return _ADDRESS_RE.sub(ADDRESS_REDACTION, text)


# ---------------------------------------------------------------- ingest


def ingest_eml_files(
    *, eml_dir: Path, emails_dir: Path, image_dir: Path
) -> dict[str, object]:
    """Write the tracked derivative of every .eml under eml_dir."""
    paths = sorted(eml_dir.glob("*.eml"))
    if not paths:
        raise ValueError(f"no .eml files found under {eml_dir}")

    emails_dir.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)

    written_keys: dict[str, str] = {}
    written_images: dict[str, str] = {}
    all_attachment_names: list[str] = []
    body_count = 0
    image_count = 0
    for path in paths:
        with path.open("rb") as stream:
            message = email.message_from_binary_file(
                stream, policy=email.policy.default
            )
        key = _email_key(path)
        previous = written_keys.get(key)
        if previous is not None:
            raise ValueError(
                f"{path.name} and {previous} both reduce to the email key "
                f"{key!r}; rename one of them"
            )
        written_keys[key] = path.name

        # The .eml carries CRLF; .gitattributes normalizes this repo to LF, so
        # write LF rather than leave a tracked file that differs from its own
        # checkout.
        body = redact_addresses(_plain_text_body(message, path)).replace("\r\n", "\n")
        (emails_dir / f"{key}{BODY_SUFFIX}").write_text(
            body, encoding="utf-8", newline="\n"
        )
        body_count += 1

        attachments = []
        for source_filename, data in _png_attachments(message, path):
            all_attachment_names.append(source_filename)
            if source_filename in IMAGES_WITH_NO_CASE:
                # Declared as belonging to no case in its message, so it is not
                # written out and nothing later has to decide what to do with it.
                continue
            file_name = f"{_NON_SLUG_RE.sub('_', Path(source_filename).stem.lower()).strip('_')}.png"
            owner = written_images.get(file_name)
            if owner is not None and owner != source_filename:
                raise ValueError(
                    f"{path.name}: attachments {source_filename!r} and {owner!r} "
                    f"both reduce to the image file {file_name!r}"
                )
            written_images[file_name] = source_filename
            (image_dir / file_name).write_bytes(data)
            attachments.append({"attachment": source_filename, "file": file_name})
            image_count += 1

        date_utc = _utc(email.utils.parsedate_to_datetime(message["Date"]))
        meta = {
            "source_file_name": path.name,
            "subject": str(message["Subject"]),
            "sender_name": _sender_display_name(message["From"]),
            "date_utc": date_utc.isoformat(),
            "body_file": f"{key}{BODY_SUFFIX}",
            "attachments": attachments,
        }
        (emails_dir / f"{key}{META_SUFFIX}").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    # Both checks below are whole-corpus invariants, and the mailbox is not the
    # corpus: a .eml is untracked, so it exists only on the machine the message
    # was read on, and any other machine has whichever ones were forwarded to
    # it. The tracked derivative is the complete record, so the orphan check is
    # made against that and holds on a partial mailbox as well as a full one.
    tracked = _tracked_attachments(emails_dir)
    orphans = sorted(
        path.name for path in image_dir.glob("*.png") if path.name not in tracked
    )
    if orphans:
        raise ValueError(
            f"{image_dir} holds PNGs no message names: {orphans}. A renamed "
            "attachment leaves the file it was written under behind, tracked "
            "and served but referenced by nothing; delete them and rerun."
        )

    # The attachment tables cannot be checked that way, because the images they
    # declare are the ones the derivative deliberately does not record:
    # IMAGES_WITH_NO_CASE is written to no metadata file at all. So this one
    # runs only when the mailbox held every message, and the summary says which
    # of the two happened rather than leaving a silent pass.
    mailbox_is_complete = len(written_keys) == len(
        list(emails_dir.glob(f"*{META_SUFFIX}"))
    )
    if mailbox_is_complete:
        require_known_attachments(all_attachment_names)

    return {
        "eml_count": len(paths),
        "body_count": body_count,
        "image_count": image_count,
        "mailbox_is_complete": mailbox_is_complete,
        "attachment_tables_checked": mailbox_is_complete,
    }


def _tracked_attachments(emails_dir: Path) -> set[str]:
    """Every image file name the tracked derivative names, across all messages."""
    written: set[str] = set()
    for meta_path in emails_dir.glob(f"*{META_SUFFIX}"):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        written.update(entry["file"] for entry in meta["attachments"])
    return written


def _sender_display_name(from_header: object) -> str:
    """The From header's display name, never its address."""
    display_name, address = email.utils.parseaddr(str(from_header))
    if not display_name or "@" in display_name:
        raise ValueError(
            f"From header has no address-free display name: {address!r}. "
            "This repo is public; supply the name rather than letting an "
            "address reach the derivative."
        )
    return display_name


def _email_key(path: Path) -> str:
    key = _NON_SLUG_RE.sub("-", path.stem.lower()).strip("-")
    if not key:
        raise ValueError(f"{path.name}: filename reduces to an empty email key")
    return key


def _plain_text_body(message: email.message.EmailMessage, path: Path) -> str:
    """The message's one text/plain part, or its one text/html part read as text.

    Two of either would mean a forward carrying the original as a real
    message/rfc822 attachment rather than as the inline quoted text the Samuel
    message uses, and taking the first would silently drop the other. That wants
    deciding rather than guessing, so it raises.

    Holman's messages through the Samuel one of 2026-08-08 are
    multipart/alternative and carry his own plain text beside the HTML; the
    seven from Psalms Part I onwards are multipart/mixed with no plain-text
    part at all. For those there is no original to prefer, so the body is read
    out of the HTML by ``_text_from_html`` and that reading is what the tracked
    derivative holds.
    """
    bodies = _parts_of_type(message, "text/plain")
    if len(bodies) > 1:
        raise ValueError(
            f"{path.name}: {len(bodies)} text/plain parts; decide which is the "
            "message body before ingesting it"
        )
    if bodies:
        return bodies[0]

    html_bodies = _parts_of_type(message, "text/html")
    if not html_bodies:
        raise ValueError(f"{path.name}: no text/plain part and no text/html part")
    if len(html_bodies) > 1:
        raise ValueError(
            f"{path.name}: no text/plain part and {len(html_bodies)} text/html "
            "parts; decide which is the message body before ingesting it"
        )
    return _text_from_html(html_bodies[0])


def _parts_of_type(message: email.message.EmailMessage, content_type: str) -> list[str]:
    """Every non-attachment part of one content type, decoded."""
    return [
        part.get_content()
        for part in message.walk()
        if part.get_content_type() == content_type and part.get_filename() is None
    ]


def _text_from_html(source: str) -> str:
    """An HTML-only body read as the line-based text the case parser expects.

    Holman's HTML is one ``<div>`` or ``<br>`` per line of what he typed, so
    ending a line at each of those recovers his layout: a case's heading and its
    ``Label: value`` lines come back one to a line, which is the whole of what
    the parser needs. Nothing else in the markup carries meaning -- the tags are
    his mail client's per-span font declarations.

    A no-break space becomes an ordinary one, because he uses it for the blank
    lines between cases and a line holding just ``&nbsp;`` should read as blank.
    Runs of blank lines collapse to one, so the tracked derivative looks like
    the plain-text bodies the earlier messages supplied.
    """
    text = _SCRIPT_OR_STYLE_RE.sub("", source)
    text = _LINE_ENDING_TAG_RE.sub("\n", text)
    text = _ANY_TAG_RE.sub("", text)
    text = html.unescape(text)
    text = text.replace("\N{NO-BREAK SPACE}", " ")
    lines = [line.strip() for line in text.split("\n")]
    return _BLANK_RUN_RE.sub("\n\n", "\n".join(lines)).strip() + "\n"


def _png_attachments(
    message: email.message.EmailMessage, path: Path
) -> list[tuple[str, bytes]]:
    """Every attached PNG. A named attachment of another type is an error.

    Dropping it silently would hand the renderer a case with fewer images than
    the message has, one step before the code that would have complained.
    """
    attachments: list[tuple[str, bytes]] = []
    for part in message.walk():
        file_name = part.get_filename()
        content_type = part.get_content_type()
        if content_type != "image/png":
            if file_name is not None:
                raise ValueError(
                    f"{path.name}: attachment {file_name!r} is {content_type}, "
                    "not image/png"
                )
            continue
        if file_name is None:
            raise ValueError(f"{path.name}: image/png attachment without a filename")
        attachments.append((file_name, part.get_payload(decode=True)))
    return attachments


def _utc(when: datetime) -> datetime:
    """An aware UTC datetime, tolerating the naive result of a -0000 header."""
    if when.tzinfo is None:
        return when.replace(tzinfo=timezone.utc)
    return when.astimezone(timezone.utc)


# ---------------------------------------------------------------- read back


def read_emails(
    emails_dir: Path, image_dir: Path
) -> tuple[list[SourceEmail], list[CorrectionCase]]:
    """Parse the tracked derivative, oldest message first."""
    meta_paths = sorted(emails_dir.glob(f"*{META_SUFFIX}"))
    if not meta_paths:
        raise ValueError(
            f"no {META_SUFFIX} files under {emails_dir}; run the ingest step first"
        )

    parsed = [_read_one(meta_path, emails_dir, image_dir) for meta_path in meta_paths]
    parsed.sort(key=lambda pair: pair[0].date_utc)
    emails = [source_email for source_email, _cases in parsed]
    cases = [case for _source_email, email_cases in parsed for case in email_cases]
    cases.sort(key=lambda case: case.ref.sort_key)
    _require_distinct_refs(cases)
    require_known_cases(
        {
            (case.email_key, case.ref.book, case.ref.chapter, case.ref.verse)
            for case in cases
        }
    )
    return emails, cases


def _read_one(
    meta_path: Path, emails_dir: Path, image_dir: Path
) -> tuple[SourceEmail, list[CorrectionCase]]:
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    key = meta_path.stem
    body_path = emails_dir / meta["body_file"]
    body = body_path.read_text(encoding="utf-8")
    preamble, raw_cases, closing = _split_body_into_cases(body, body_path)
    cases = [
        _build_case(
            email_key=key,
            index_in_email=index,
            heading=heading,
            fields=fields,
            path=body_path,
        )
        for index, (heading, fields) in enumerate(raw_cases, start=1)
    ]
    attachments = [
        (entry["attachment"], entry["file"]) for entry in meta["attachments"]
    ]
    for _source_filename, file_name in attachments:
        if not (image_dir / file_name).is_file():
            raise ValueError(
                f"{meta_path.name} names the image {file_name!r}, which is not "
                f"in {image_dir}; rerun the ingest step"
            )
    cases = _assign_images(cases, attachments, meta_path)

    date_utc = datetime.fromisoformat(meta["date_utc"])
    source_email = SourceEmail(
        key=key,
        source_file_name=meta["source_file_name"],
        subject=meta["subject"],
        sender_name=meta["sender_name"],
        date_utc=date_utc,
        date_iso=date_utc.isoformat(),
        date_display=date_utc.strftime("%d %B %Y"),
        preamble=preamble,
        closing=closing,
    )
    return source_email, cases


def _labelled(line: str) -> tuple[str, str] | None:
    match = _LABEL_RE.match(line)
    if match is None:
        return None
    label = match.group("label").strip()
    if label not in KNOWN_FIELD_LABELS:
        return None
    return label, match.group("value").strip()


def _split_body_into_cases(
    body: str, path: Path
) -> tuple[
    tuple[str, ...], list[tuple[str, tuple[tuple[str, str], ...]]], tuple[str, ...]
]:
    lines = [
        _without_embedded_note_letter(line.rstrip(), path) for line in body.splitlines()
    ]
    lines = _without_section_dividers(lines, path)
    starts = _case_start_indexes(lines)
    if not starts:
        raise ValueError(f"{path.name}: no cases found")
    _require_no_unopened_case(lines[: starts[0]], path)

    preamble = tuple(line.strip() for line in lines[: starts[0]] if line.strip())
    cases: list[tuple[str, tuple[tuple[str, str], ...]]] = []
    closing: tuple[str, ...] = ()
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        heading = lines[start].strip()
        fields, trailing = _parse_case_region(lines[start + 1 : end], heading, path)
        cases.append((heading, fields))
        if not trailing:
            continue
        if position + 1 < len(starts):
            raise ValueError(
                f"{path.name}: unexpected prose after case {heading!r}: {trailing[0]!r}"
            )
        closing = trailing
    return preamble, cases, closing


def _without_section_dividers(lines: list[str], path: Path) -> list[str]:
    """Drop the all-capitals book dividers, having checked each names a book.

    The Jeremiah message of 2026-08-12 groups its 24 cases under ``JEREMIAH``,
    ``EZEKIEL``, ``MINOR PROPHETS`` and ``DANIEL``, each alone on a line between
    two cases. They are dropped rather than shown because each one repeats the
    book of every case beneath it, which the card already states and the page
    already filters on; they are dropped here, before the case scan, because a
    line between two cases would otherwise be read as prose after the earlier
    one and raise.

    Each divider is checked against ``_bk39id`` first, so a capitalized line
    that is not a book name reaches the ordinary parse and raises there rather
    than being swallowed. ``MINOR PROPHETS`` names the section rather than one
    book and is the reason for the declared set beside it.
    """
    kept = []
    for line in lines:
        stripped = line.strip()
        if _SECTION_DIVIDER_RE.match(stripped) is None:
            kept.append(line)
            continue
        if stripped in _SECTION_DIVIDER_NAMES:
            continue
        try:
            _bk39id(stripped, path)
        except ValueError as exc:
            raise ValueError(
                f"{path.name}: {stripped!r} stands alone in capitals like the "
                "book dividers of the Jeremiah message, but names no book. Add "
                "it to _SECTION_DIVIDER_NAMES, or say what it is."
            ) from exc
    return kept


def _without_embedded_note_letter(line: str, path: Path) -> str:
    """Drop a bidi-embedded Latin note letter, and raise on any control left.

    Applied to every line of a body as it is split, so the heading, the fields,
    the greeting and the sign-off are all read from cleaned text and no later
    stage has to know about this. The tracked ``emails/<key>.txt`` still holds
    the message as it arrived; this is a reading of it, and the page says so.
    """
    cleaned = _EMBEDDED_NOTE_LETTER_RE.sub("", line)
    leftover = _BIDI_CONTROL_RE.search(cleaned)
    if leftover is not None:
        raise ValueError(
            f"{path.name}: bidi formatting control "
            f"U+{ord(leftover.group()):04X} survives in {cleaned.strip()!r}. "
            "Widen _EMBEDDED_NOTE_LETTER_RE, or decide what this one means, "
            "rather than letting an invisible character reach the page."
        )
    return cleaned


def _require_no_unopened_case(preamble_lines: list[str], path: Path) -> None:
    """Raise on a case the start scan failed to open, rather than read it as prose.

    A case opens only when the line after its heading is a label in
    FIRST_FIELD_LABELS, so a message introducing a new spelling for its FIRST
    field opens no case at all: the heading and every field line fall before
    the first case and would be shown as the message's greeting.
    ``_parse_case_region``'s unrecognized-label check cannot see them, because
    it only runs inside a case that did open.

    The rule has to be narrow, because the forwarded Samuel message quotes
    Sent/From/To/Subject lines in its real preamble. What distinguishes a
    dropped case is that its label-shaped line sits directly under a
    heading-shaped one, which is true of none of those four.
    """
    previous_nonblank: str | None = None
    for line in preamble_lines:
        stripped = line.strip()
        if not stripped:
            continue
        if (
            _LABEL_RE.match(line) is not None
            and _labelled(line) is None
            and previous_nonblank is not None
            and _HEADING_RE.match(previous_nonblank) is not None
        ):
            raise ValueError(
                f"{path.name}: {stripped!r} under the heading "
                f"{previous_nonblank!r} looks like the first field of a case, "
                "but its label is not one of FIRST_FIELD_LABELS, so no case "
                "opened. Add the spelling to FIRST_FIELD_LABELS."
            )
        previous_nonblank = stripped


def _case_start_indexes(lines: list[str]) -> list[int]:
    starts: list[int] = []
    for index, line in enumerate(lines):
        if not line.strip() or _labelled(line) is not None:
            continue
        following = next(
            (later for later in range(index + 1, len(lines)) if lines[later].strip()),
            None,
        )
        if following is None:
            continue
        field = _labelled(lines[following])
        if field is not None and field[0] in FIRST_FIELD_LABELS:
            starts.append(index)
    return starts


def _parse_case_region(
    region: list[str], heading: str, path: Path
) -> tuple[tuple[tuple[str, str], ...], tuple[str, ...]]:
    """Split one case's lines into its labelled fields and any trailing prose.

    A field value is one line, either the label's line or -- where that is
    empty -- the line directly below. Prose after the fields is the message's sign-off,
    and only the last case in a message may have any. An unrecognized label
    raises here rather than being absorbed into that sign-off, which is what
    would otherwise happen to a new label spelling in a future message. The
    check has to live in this function: applied to a whole body it would reject
    the forwarded Sent/From/To/Subject block one of these messages quotes in
    its preamble. It reaches only a case that opened, so the same mistake in a
    message's FIRST field is caught by ``_require_no_unopened_case`` instead.
    """
    fields: list[tuple[str, str]] = []
    trailing: list[str] = []
    after_blank = True
    awaiting_value: str | None = None
    for line in region:
        stripped = line.strip()
        if not stripped:
            after_blank = True
            awaiting_value = None
            continue
        field = _labelled(line)
        if field is not None:
            if trailing:
                raise ValueError(
                    f"{path.name}: field {field[0]!r} follows the prose "
                    f"{trailing[0]!r} in case {heading!r}"
                )
            fields.append(field)
            after_blank = False
            # An empty value may be continued on the line directly below; see
            # the note beside awaiting_value's other use.
            awaiting_value = field[0] if not field[1] else None
            continue
        if awaiting_value is not None and _LABEL_RE.match(line) is None:
            # The 1 Samuel 28:12 message of 2026-08-23 writes "Current:" and
            # "Change:" alone on a line and the Hebrew under each, where every
            # earlier message puts label and value on one line. Only the line
            # DIRECTLY below an empty value is read this way, and only when it
            # is not itself label-shaped, which is what keeps the two existing
            # shapes intact: the empty "Corrected Text:" of the Ps 8:9.6 case is
            # followed by "Note: ...", a labelled line, and stays empty; and a
            # sign-off is separated from the last field by a blank line, which
            # clears awaiting_value above. A label-shaped line that is not a
            # known label still reaches the raise below rather than being
            # swallowed as a value.
            fields[-1] = (awaiting_value, stripped)
            awaiting_value = None
            after_blank = False
            continue
        if _LABEL_RE.match(line) is not None:
            raise ValueError(
                f"{path.name}: unrecognized field label in case {heading!r}: "
                f"{stripped!r}. Add it to FIRST_FIELD_LABELS or OTHER_FIELD_LABELS."
            )
        if not after_blank and not trailing:
            raise ValueError(
                f"{path.name}: unlabelled line inside case {heading!r}: {stripped!r}"
            )
        trailing.append(stripped)
    if not fields:
        raise ValueError(f"{path.name}: case {heading!r} has no labelled fields")
    return tuple(fields), tuple(trailing)


def _build_case(
    *,
    email_key: str,
    index_in_email: int,
    heading: str,
    fields: tuple[tuple[str, str], ...],
    path: Path,
) -> CorrectionCase:
    field_ref = _ref_from_first_field(fields[0][1], path)

    if _ORDINAL_HEADING_RE.match(heading) is not None:
        # A bare ordinal names no verse, so the first field has to.
        if field_ref is None:
            raise ValueError(
                f"{path.name}: case heading {heading!r} is a bare ordinal and "
                f"its {fields[0][0]} field {fields[0][1]!r} states no "
                "reference, so nothing says which atom this case is about"
            )
        return CorrectionCase(
            email_key=email_key,
            index_in_email=index_in_email,
            heading=heading,
            ref=field_ref,
            fields=fields,
            images=(),
        )

    match = _HEADING_RE.match(heading)
    if match is None:
        raise ValueError(f"{path.name}: unparsable case heading {heading!r}")
    book = _bk39id(match.group("book"), path)
    chapter = int(match.group("chapter"))
    verse = int(match.group("verse"))
    atom_text = match.group("atom") or match.group("atom_paren")

    if field_ref is not None:
        if (field_ref.book, field_ref.chapter, field_ref.verse) != (
            book,
            chapter,
            verse,
        ):
            raise ValueError(
                f"{path.name}: heading {heading!r} disagrees with its "
                f"{fields[0][0]} field {fields[0][1]!r}"
            )
        if atom_text is not None and int(atom_text) != field_ref.atom:
            raise ValueError(
                f"{path.name}: heading {heading!r} atom index disagrees with "
                f"its {fields[0][0]} field"
            )
        atom_text = str(field_ref.atom)

    declared_atom = atom_index_for_verse_case(email_key, book, chapter, verse)
    if atom_text is None:
        if declared_atom is None:
            raise ValueError(
                f"{path.name}: case {heading!r} names no atom index. Add one to "
                "hkq_cmn/uxlc_atom_index_notes.ATOM_INDEX_BY_VERSE_CASE, with "
                "the evidence for it, if the message really states none."
            )
        atom_text = str(declared_atom)
    elif declared_atom is not None:
        raise ValueError(
            f"{path.name}: case {heading!r} names the atom index {atom_text}, "
            "and ATOM_INDEX_BY_VERSE_CASE names it too; drop the table entry "
            "rather than keeping a second answer beside the message's own."
        )

    return CorrectionCase(
        email_key=email_key,
        index_in_email=index_in_email,
        heading=heading,
        ref=CaseRef(book=book, chapter=chapter, verse=verse, atom=int(atom_text)),
        fields=fields,
        images=(),
    )


def _ref_from_first_field(value: str, path: Path) -> CaseRef | None:
    match = _FIRST_FIELD_REF_RE.match(value)
    if match is None:
        return None
    return CaseRef(
        book=_bk39id(match.group("book"), path),
        chapter=int(match.group("chapter")),
        verse=int(match.group("verse")),
        atom=int(match.group("atom")),
    )


def _bk39id(book_text: str, path: Path) -> str:
    """Resolve Holman's book spelling to a bk39 id, by exact or unique prefix.

    Matching runs both ways because it has to. Holman's abbreviations are
    prefixes of the id -- Ex, Lev, Josh, Judg, 1Sa, "2 Samuel" -- but two bk39
    ids are themselves truncations, so his "Deuteronomy" and "Leviticus" have
    the id (Deuter, Levit) as their prefix instead. Either direction resolving
    to exactly one book is a match; anything else raises, rather than guessing.
    """
    wanted = _NORMALIZED_BOOK_TEXT_RE.sub("", book_text.lower())
    exact = _BK39ID_BY_NORMALIZED.get(wanted)
    if exact is not None:
        return exact
    matched = sorted(
        set(
            bk39id
            for normalized, bk39id in _BK39ID_BY_NORMALIZED.items()
            if normalized.startswith(wanted) or wanted.startswith(normalized)
        )
    )
    if len(matched) == 1:
        return matched[0]
    if not matched:
        raise ValueError(f"{path.name}: unrecognized book name {book_text!r}")
    raise ValueError(
        f"{path.name}: ambiguous book name {book_text!r} (matches {matched})"
    )


def _assign_images(
    cases: list[CorrectionCase],
    attachments: list[tuple[str, str]],
    path: Path,
) -> list[CorrectionCase]:
    """Attach each PNG to the case its filename names.

    A filename such as "Josh 20.4.12 Daat Miqra.png" names its case outright and
    its remainder becomes the caption. A filename naming no case (Holman's
    "Sassoon 1053.png") belongs to a single-case message; in a multi-case
    message it is an error rather than a guess.
    """
    by_ref: dict[str, list[CaseImage]] = {case.ref.key: [] for case in cases}
    unreferenced: list[CaseImage] = []
    for source_filename, file_name in attachments:
        stem = Path(source_filename).stem
        declared = COMPANION_IMAGE_CASES.get(source_filename)
        if declared is not None:
            if declared not in by_ref:
                raise ValueError(
                    f"{path.name}: COMPANION_IMAGE_CASES assigns "
                    f"{source_filename!r} to {declared}, which is not a case in "
                    "this message"
                )
            by_ref[declared].append(
                CaseImage(
                    source_filename=source_filename,
                    caption=stem.strip(),
                    file_name=file_name,
                    names_case_only=False,
                )
            )
            continue
        match = _ATTACHMENT_REF_RE.match(stem)
        if match is None:
            unreferenced.append(
                CaseImage(
                    source_filename=source_filename,
                    caption=stem.strip(),
                    file_name=file_name,
                    names_case_only=False,
                )
            )
            continue
        ref = CaseRef(
            book=_bk39id(match.group("book"), path),
            chapter=int(match.group("chapter")),
            verse=int(match.group("verse")),
            atom=int(match.group("atom")),
        )
        if ref.key not in by_ref:
            raise ValueError(
                f"{path.name}: attachment {source_filename!r} names {ref.key}, "
                "which is not a case in this message"
            )
        # Holman's "2Sa 5.21.1 .png" has a space before the extension, so the
        # stem needs stripping too, not only the remainder after the reference.
        remainder = match.group("caption").strip()
        by_ref[ref.key].append(
            CaseImage(
                source_filename=source_filename,
                caption=remainder or stem.strip(),
                file_name=file_name,
                names_case_only=not remainder,
            )
        )
    if unreferenced:
        if len(cases) != 1:
            raise ValueError(
                f"{path.name}: attachments "
                f"{[image.source_filename for image in unreferenced]} name no "
                f"case, and this message has {len(cases)} cases"
            )
        by_ref[cases[0].ref.key].extend(unreferenced)

    return [
        CorrectionCase(
            email_key=case.email_key,
            index_in_email=case.index_in_email,
            heading=case.heading,
            ref=case.ref,
            fields=case.fields,
            images=tuple(_ordered_images(by_ref[case.ref.key])),
        )
        for case in cases
    ]


def _ordered_images(images: list[CaseImage]) -> list[CaseImage]:
    """The plain crop of the word first, then Holman's companions by caption."""
    return sorted(images, key=lambda image: (not image.names_case_only, image.caption))


def _require_distinct_refs(cases: list[CorrectionCase]) -> None:
    seen: dict[str, CorrectionCase] = {}
    for case in cases:
        previous = seen.get(case.ref.key)
        if previous is not None:
            where = (
                f"both in {case.email_key}"
                if previous.email_key == case.email_key
                else f"in {previous.email_key} and {case.email_key}"
            )
            raise ValueError(
                f"two cases share the reference {case.ref.key}: "
                f"case {previous.index_in_email} {previous.heading!r} and "
                f"case {case.index_in_email} {case.heading!r}, {where}"
            )
        seen[case.ref.key] = case
