"""Extract Daniel Holman's suggested corrections TO MAM from his emails.

NOT the same body of work as ``uxlc_email_extract`` beside this file, and the
distinction is the whole reason for a second module.  That one reads his
suggested corrections to the UXLC, a book at a time, addressed to the UXLC's
editor.  This one reads his suggested corrections to MAM itself, addressed to
MAM's editor.  Neither is about ketiv/qere, which is a third body of work again
-- the 77-row review extracted from a tracked ``.docx`` by
``extract_docx_pipeline``.

THE PRIVACY BOUNDARY HERE IS STRICTER THAN THE UXLC ONE, by Ben Denckla's
instruction of 2026-09-02, and the difference is worth stating because the
looser rule is right next door and easy to copy.  The UXLC ingest tracks each
message BODY verbatim, with addresses replaced.  This ingest tracks NO body at
all.  What becomes public is the suggestions themselves -- a reference, the two
forms Holman compares, and his one-line description of the difference --
plus the message's subject, date and sender display name.  The threads around
those messages, in which Ben Denckla and Seth (Avi) Kadish discuss the
suggestions, are read by nobody here and stored nowhere: they may inform how a
suggestion is presented, but no sentence of theirs is kept.

That boundary is enforced structurally rather than by redaction.  A message is a
source of suggestions only if ``SUGGESTION_SENDER_NAME`` sent it; everything
else in the mailbox is skipped and named in the run summary, which goes to
stdout and is not tracked.  So a reply, and equally a third party's forward of
one of Holman's own messages, cannot contribute text even though the forward
quotes the suggestions verbatim.

TWO MESSAGE SHAPES, and a caller must not assume either.

``prose-list`` -- the "30 More Corrections for MAM" message of 2026-08-31.  A
numbered list in the plain-text body, each item a heading line
``<Book> <ch>:<v>.<atom> - <description>`` followed by ``MAM:`` and a
comparison-edition line.  Its crops arrive as ordinary message attachments whose
filenames restate the case, so image-to-case is recoverable from the filename.

``workbook`` -- the two HUB messages of 2026-08-21 and 2026-08-27.  The cases are
cells of an attached ``.xlsx`` and the crops are embedded INSIDE that workbook,
so the message has no image attachments at all and the crops are named
``image1.png``..``image4.png``, which says nothing about which case each belongs
to.  ``xlsx_xml_utils.anchored_image_targets_by_row`` recovers the mapping from
the drawing anchors; that module's docstring says why nothing else can.

HOLMAN'S OWN WORDS FOR HIS COMPARISON SOURCES ARE KEPT AS HE WROTE THEM.  The
prose-list message says "Aleppo"; both workbook messages say "HUB" and nothing
else.  "HUB" was identified as a particular printed edition in the reply thread,
by a correspondent -- which is exactly the material this module does not store,
so the identification is not applied here and ``comparison_source`` holds his
label verbatim.  Deciding what MAM should call that edition is an editorial
question for Ben Denckla, not a parsing question for this module.

THE TWO WORKBOOK MESSAGES CARRY THE SAME FOUR CASES, so ingesting both would
double-count.  ``_merge_cases`` folds duplicates by reference and raises when two
messages disagree about a case rather than picking one, since a disagreement
means his forms changed between messages and that wants deciding.  The later
message adds a recommendation per case that the earlier lacks; a recommendation
present in one and absent in the other is a merge rather than a conflict.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import email
import email.policy
import io
from pathlib import Path
import re
import zipfile

from hkq_cmn import xlsx_xml_utils
from hkq_cmn.holman_email_common import (
    email_key,
    message_date,
    plain_text_body,
    sender_display_name,
)

SUGGESTION_SENDER_NAME = "Daniel Holman"

# Holman's own abbreviations, mapped to the standard 39-book names of
# mb_cmn/bib_locales.py.  Deliberately a closed table rather than a fuzzy
# matcher: an abbreviation nobody has seen before is a message whose shape
# changed, and guessing at it would put a case under the wrong book silently.
STD_BOOK_NAME_BY_HOLMAN_ABBREV = {
    "Josh": "Joshua",
    "Judg": "Judges",
    "1Sa": "1Samuel",
    "2Sa": "2Samuel",
    "1Ki": "1Kings",
    "2Ki": "2Kings",
    "Isa": "Isaiah",
    "Zech": "Zechariah",
    "2Ch": "2Chronicles",
}

MAM_LABEL = "MAM:"

# A heading line of the prose-list shape, after the forward's quote markers are
# stripped: "Judg 1:7.21 - Aleppo has no Meteg under Resh".
_CASE_HEADING_RE = re.compile(
    r"^(?P<book>[A-Za-z0-9]+)\s+(?P<chapter>\d+):(?P<verse>\d+)\.(?P<atom>\d+)"
    r"\s*[-–—]\s*(?P<description>\S.*?)\s*$"
)

# "Judg 1:7.21" as it appears in a workbook's reference cell.
_REFERENCE_RE = re.compile(
    r"^(?P<book>[A-Za-z0-9]+)\s+(?P<chapter>\d+):(?P<verse>\d+)\.(?P<atom>\d+)$"
)

# An attachment filename of the prose-list shape:
# "01 Judg 1.7.21 Aleppo has no Meteg under Resh.png".  The ordinal is the
# case's position in the message; the rest restates the heading with the verse
# separator written "." rather than ":".
_ATTACHMENT_NAME_RE = re.compile(
    r"^(?P<ordinal>\d+)\.?\s+(?P<book>[A-Za-z0-9]+)\s+"
    r"(?P<chapter>\d+)\.(?P<verse>\d+)\.(?P<atom>\d+)\s+(?P<description>.+)$"
)

_QUOTE_PREFIX_RE = re.compile(r"^[>\s]*")


@dataclass(frozen=True)
class CaseRef:
    """One case's location: Holman's book abbreviation plus chapter, verse and atom.

    ``atom`` counts maqaf-joined atoms separately, which was established twice
    independently on 2026-09-02 -- by hand against the page crops, and against
    ``MAM-parsed/plus`` -- and is NOT the numbering his UXLC correspondence uses,
    where a ketiv/qere pair counts as one.  Nothing here assumes the two agree.
    """

    book_abbrev: str
    chapter: int
    verse: int
    atom: int

    @property
    def std_book_name(self) -> str:
        try:
            return STD_BOOK_NAME_BY_HOLMAN_ABBREV[self.book_abbrev]
        except KeyError as exc:
            raise ValueError(
                f"unknown book abbreviation {self.book_abbrev!r}; add it to "
                "STD_BOOK_NAME_BY_HOLMAN_ABBREV rather than guessing"
            ) from exc

    def __str__(self) -> str:
        return f"{self.book_abbrev} {self.chapter}:{self.verse}.{self.atom}"


@dataclass(frozen=True)
class ImageTarget:
    """Where one page crop is to be read from, once the mailbox is at hand.

    TWO KINDS, because the two message shapes carry their crops differently.
    ``attachment`` names a part of the message itself, which is how the
    prose-list message ships its 30 crops.  ``workbook-member`` names a zip
    member inside the message's attached ``.xlsx``, which is the only place the
    HUB messages' crops exist -- see ``xlsx_xml_utils``' module docstring.
    """

    eml_name: str
    kind: str
    locator: str

    def payload(self) -> dict[str, str]:
        return {"eml_name": self.eml_name, "kind": self.kind, "locator": self.locator}


@dataclass
class SuggestionCase:
    ref: CaseRef
    comparison_source: str
    mam_form: str
    comparison_form: str
    description: str
    recommendation: str | None = None
    image_targets: list[ImageTarget] = field(default_factory=list)
    source_message_keys: list[str] = field(default_factory=list)

    def payload(self) -> dict[str, object]:
        return {
            "ref": str(self.ref),
            "book_abbrev": self.ref.book_abbrev,
            "std_book_name": self.ref.std_book_name,
            "chapter": self.ref.chapter,
            "verse": self.ref.verse,
            "atom": self.ref.atom,
            "comparison_source": self.comparison_source,
            "mam_form": self.mam_form,
            "comparison_form": self.comparison_form,
            "description": self.description,
            "recommendation": self.recommendation,
            "source_message_keys": list(self.source_message_keys),
        }


@dataclass
class SourceMessage:
    key: str
    subject: str
    date_iso: str
    sender_name: str
    shape: str
    case_count: int

    def payload(self) -> dict[str, object]:
        return {
            "key": self.key,
            "subject": self.subject,
            "date": self.date_iso,
            "sender_name": self.sender_name,
            "shape": self.shape,
            "case_count": self.case_count,
        }


# ------------------------------------------------------------------ reading


def _strip_quote_prefix(line: str) -> str:
    return _QUOTE_PREFIX_RE.sub("", line).rstrip()


def _ref_from_match(match: re.Match[str]) -> CaseRef:
    return CaseRef(
        book_abbrev=match.group("book"),
        chapter=int(match.group("chapter")),
        verse=int(match.group("verse")),
        atom=int(match.group("atom")),
    )


def _parse_prose_list(body: str, path: Path) -> list[SuggestionCase]:
    """Cases from a message whose body is the numbered list.

    The comparison-edition label is read off the line itself rather than assumed
    to be "Aleppo": the label is Holman's, and a later message comparing against
    something else would otherwise be recorded under the wrong source.
    """
    lines = [_strip_quote_prefix(line) for line in body.splitlines()]
    cases: list[SuggestionCase] = []

    for index, line in enumerate(lines):
        heading = _CASE_HEADING_RE.match(line)
        if heading is None:
            continue
        if heading.group("book") not in STD_BOOK_NAME_BY_HOLMAN_ABBREV:
            continue

        mam_form = None
        comparison_form = None
        comparison_source = None
        for follower in lines[index + 1 : index + 12]:
            if not follower:
                continue
            if follower.startswith(MAM_LABEL):
                mam_form = follower[len(MAM_LABEL) :].strip()
                continue
            label, separator, value = follower.partition(":")
            if separator and value.strip() and label.isalpha():
                if comparison_form is None:
                    comparison_source = label.strip()
                    comparison_form = value.strip()
                continue
            if _CASE_HEADING_RE.match(follower):
                break

        if mam_form is None or comparison_form is None:
            raise ValueError(
                f"{path.name}: case {_ref_from_match(heading)} has no "
                f"{'MAM' if mam_form is None else 'comparison'} form line"
            )

        cases.append(
            SuggestionCase(
                ref=_ref_from_match(heading),
                comparison_source=comparison_source or "",
                mam_form=mam_form,
                comparison_form=comparison_form,
                description=heading.group("description"),
            )
        )

    return cases


def _assign_prose_list_images(
    message: email.message.EmailMessage,
    cases: list[SuggestionCase],
    path: Path,
) -> None:
    """Attach each image part of a prose-list message to the case its filename names.

    The filenames restate the case -- "01 Judg 1.7.21 Aleppo has no Meteg under
    Resh.png" -- so the mapping is read off the name rather than off the message
    order, which would silently misalign if a part were dropped in transit.  The
    verse separator is written "." in a filename and ":" in the body, since a
    colon cannot appear in a Windows filename; that is the only difference, and
    ``_ATTACHMENT_NAME_RE`` is written around it.

    An image naming a case the message does not contain RAISES rather than being
    dropped, matching what ``uxlc_attachment_notes`` does for the other ingest: a
    crop with no case is either a case that failed to parse or a message shape
    that changed, and both want looking at.
    """
    by_ref = {str(case.ref): case for case in cases}
    for part in message.walk():
        filename = part.get_filename()
        if not filename or part.get_content_maintype() != "image":
            continue
        match = _ATTACHMENT_NAME_RE.match(Path(filename).stem)
        if match is None:
            raise ValueError(
                f"{path.name}: attachment {filename!r} does not name a case; "
                "add it to a disposition table rather than letting it pass"
            )
        ref = CaseRef(
            book_abbrev=match.group("book"),
            chapter=int(match.group("chapter")),
            verse=int(match.group("verse")),
            atom=int(match.group("atom")),
        )
        case = by_ref.get(str(ref))
        if case is None:
            raise ValueError(
                f"{path.name}: attachment {filename!r} names case {ref}, "
                "which this message does not contain"
            )
        case.image_targets.append(ImageTarget(path.name, "attachment", filename))


def _workbook_attachment(
    message: email.message.EmailMessage,
) -> tuple[str, bytes] | None:
    for part in message.walk():
        filename = part.get_filename()
        if filename and filename.lower().endswith(".xlsx"):
            payload = part.get_payload(decode=True)
            if payload is None:
                raise ValueError(f"workbook attachment {filename!r} has no payload")
            return filename, payload
    return None


def _header_index(
    cells: dict[tuple[int, str], str],
    header_row: int,
) -> tuple[dict[str, str], dict[str, str]]:
    """Two views of the header row: lowered label to column, and lowered label to raw label.

    The raw label is kept because it is Holman's own spelling of the comparison
    edition -- "HUB", not "Hub" -- and that spelling is what reaches the record.
    Matching is done on the lowered form so that a later message capitalizing a
    header differently still parses.
    """
    column_by_header: dict[str, str] = {}
    raw_by_header: dict[str, str] = {}
    for (row_number, column), text in cells.items():
        if row_number != header_row:
            continue
        raw = text.strip()
        column_by_header[raw.lower()] = column
        raw_by_header[raw.lower()] = raw
    return column_by_header, raw_by_header


def _parse_workbook(payload: bytes, path: Path) -> list[SuggestionCase]:
    """Cases from a message whose suggestions are cells of an attached workbook.

    Columns are found by their header text rather than by position, since the two
    workbooks differ: the later one adds a "HUB Images" column between the
    comparison form and the recommendation.  The comparison column's own header
    supplies ``comparison_source``, which is how Holman's label reaches the record
    without this module naming an edition of its own.
    """
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        sheet_part = xlsx_xml_utils.first_sheet_part(archive)
        strings = xlsx_xml_utils.shared_strings(archive)
        cells = xlsx_xml_utils.sheet_cells(archive, sheet_part, strings)

        drawing_part = xlsx_xml_utils.drawing_part_for_sheet(archive, sheet_part)
        images_by_row = (
            xlsx_xml_utils.anchored_image_targets_by_row(archive, drawing_part)
            if drawing_part
            else {}
        )

        header_row = min(row for row, _ in cells)
        columns, raw_headers = _header_index(cells, header_row)
        reference_column = columns.get("verse")
        mam_column = columns.get("mam")
        if reference_column is None or mam_column is None:
            raise ValueError(
                f"{path.name}: workbook header row {header_row} has no "
                f"{'Verse' if reference_column is None else 'MAM'} column; "
                f"headers were {sorted(columns)}"
            )

        comparison_header = _comparison_header(columns)
        recommendation_column = _recommendation_column(columns)

        cases: list[SuggestionCase] = []
        for row_number in sorted({row for row, _ in cells} - {header_row}):
            raw_reference = cells.get((row_number, reference_column))
            if raw_reference is None:
                continue
            match = _REFERENCE_RE.match(raw_reference.strip())
            if match is None:
                raise ValueError(
                    f"{path.name}: row {row_number} reference {raw_reference!r} "
                    "is not a Book chapter:verse.atom reference"
                )
            mam_form = (cells.get((row_number, mam_column)) or "").strip()
            comparison_form = (
                cells.get((row_number, columns[comparison_header])) or ""
            ).strip()
            if not mam_form or not comparison_form:
                raise ValueError(
                    f"{path.name}: row {row_number} is missing a MAM or "
                    f"{comparison_header} form"
                )
            recommendation = None
            if recommendation_column is not None:
                recommendation = (
                    cells.get((row_number, recommendation_column)) or ""
                ).strip() or None

            targets = _images_for_row(images_by_row, row_number, header_row)
            cases.append(
                SuggestionCase(
                    ref=_ref_from_match(match),
                    comparison_source=raw_headers[comparison_header],
                    mam_form=mam_form,
                    comparison_form=comparison_form,
                    description="",
                    recommendation=recommendation,
                    image_targets=[
                        ImageTarget(path.name, "workbook-member", target)
                        for target in targets
                    ],
                )
            )

    return cases


def _comparison_header(columns: dict[str, str]) -> str:
    """The header naming the edition MAM is compared against.

    Everything that is not the reference, the MAM form, an images column or a
    recommendation column is the comparison column.  Written as an exclusion so
    that a message using a new label -- Holman has used "HUB" so far and could
    use another -- is read rather than rejected.
    """
    ignored = {"verse", "mam"}
    candidates = [
        header
        for header in columns
        if header not in ignored
        and "image" not in header
        and not header.startswith("suggestion")
    ]
    if len(candidates) != 1:
        raise ValueError(
            "expected exactly one comparison-edition column, found "
            f"{sorted(candidates)}"
        )
    return candidates[0]


def _recommendation_column(columns: dict[str, str]) -> str | None:
    for header, column in columns.items():
        if header.startswith("suggestion"):
            return column
    return None


def _images_for_row(
    images_by_row: dict[int, list[str]],
    row_number: int,
    header_row: int,
) -> list[str]:
    """The crops anchored to a case's row, or to the blank row beneath it.

    The earlier workbook spaces its cases two rows apart and anchors each picture
    to the case's own row; the later one has them contiguous and does the same.
    Both are covered by taking the case row and, when it has none, the row below,
    which is where a picture anchored to a spacer row would sit.
    """
    if row_number in images_by_row:
        return images_by_row[row_number]
    if row_number + 1 in images_by_row and row_number + 1 != header_row:
        return images_by_row[row_number + 1]
    return []


# ------------------------------------------------------------------ merging


def _merge_cases(
    merged: dict[str, SuggestionCase],
    cases: list[SuggestionCase],
    message_key: str,
) -> None:
    for case in cases:
        key = str(case.ref)
        case.source_message_keys = [message_key]
        existing = merged.get(key)
        if existing is None:
            merged[key] = case
            continue

        for name in ("comparison_source", "mam_form", "comparison_form"):
            was = getattr(existing, name)
            now = getattr(case, name)
            if was != now:
                raise ValueError(
                    f"case {key} disagrees between messages "
                    f"{existing.source_message_keys} and {message_key}: "
                    f"{name} was {was!r}, now {now!r}"
                )

        if case.description and not existing.description:
            existing.description = case.description
        if case.recommendation and not existing.recommendation:
            existing.recommendation = case.recommendation
        if case.image_targets and not existing.image_targets:
            existing.image_targets = case.image_targets
        existing.source_message_keys.append(message_key)


def read_suggestion_messages(
    eml_dir: Path,
) -> tuple[list[SourceMessage], list[SuggestionCase], list[dict[str, str]]]:
    """Read a mailbox and return its source messages, merged cases, and what was skipped.

    The skipped list is returned rather than logged so that the caller can print
    it; it names messages by filename and reason, and nothing from a skipped
    message reaches any tracked file.
    """
    if not eml_dir.is_dir():
        raise FileNotFoundError(f"mailbox directory not found: {eml_dir}")

    sources: list[SourceMessage] = []
    merged: dict[str, SuggestionCase] = {}
    skipped: list[dict[str, str]] = []

    for path in sorted(eml_dir.glob("*.eml")):
        message = email.message_from_bytes(
            path.read_bytes(), policy=email.policy.default
        )
        sender = sender_display_name(message.get("From"))
        if sender != SUGGESTION_SENDER_NAME:
            skipped.append({"file": path.name, "reason": f"sender is {sender!r}"})
            continue

        key = email_key(path)
        workbook = _workbook_attachment(message)
        if workbook is not None:
            shape = "workbook"
            cases = _parse_workbook(workbook[1], path)
        else:
            shape = "prose-list"
            cases = _parse_prose_list(plain_text_body(message, path), path)
            _assign_prose_list_images(message, cases, path)

        if not cases:
            skipped.append({"file": path.name, "reason": "no cases found"})
            continue

        _merge_cases(merged, cases, key)
        sources.append(
            SourceMessage(
                key=key,
                subject=str(message.get("Subject", "")),
                date_iso=message_date(message, path).isoformat(),
                sender_name=sender,
                shape=shape,
                case_count=len(cases),
            )
        )

    return sources, list(merged.values()), skipped
