"""Build gh-pages/uxlc_corrections.html from the emails under emails/."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
import json
from pathlib import Path
import struct

from py_render.rt_assets import PALETTE
from py_render.uc_case_card import (
    case_card_html,
    case_filter_ids,
    case_fragment_id,
    email_fragment_id,
    relative_href,
)
from py_render.uc_hebrew_runs import inline_text_html
from py_render.uc_summary import all_filter_ids, summary_html
from hkq_cmn.uxlc_atom_locations import (
    AtomLocation,
    read_locations,
    require_full_coverage,
)
from hkq_cmn.uxlc_bracketed_corrections import (
    apply_bracketed_corrections,
    bracketed_correction_phrases,
)
from hkq_cmn.uxlc_change_records import (
    CHANGES_PAGE_DESCRIPTION,
    CHANGES_PAGE_LABEL,
    CHANGES_PAGE_URL,
    change_record_links,
    require_known_refs,
)
from hkq_cmn.uxlc_email_extract import (
    ADDRESS_REDACTION,
    CorrectionCase,
    SourceEmail,
    read_emails,
)
from hkq_cmn.uxlc_external_links import book_display_name
from hkq_cmn.uxlc_holman_forms import (
    forms_for_case,
    require_full_coverage as require_form_shapes,
)
from hkq_cmn.uxlc_manuscript_page import manuscript_page, manuscript_position
from hkq_cmn.uxlc_standard_atoms import (
    read_standard_atoms,
    require_full_coverage as require_standard_atoms,
)
from uxlc_comments.all_comments import BY_REF as COMMENTS_BY_REF, comments_for_ref

PAGE_TITLE = "Holman UXLC suggestions"
PAGE_HEADING = "Daniel Holman's suggestions for the UXLC"
# The nav reaches this report and the hand-written landing page, and stops
# there. It used to carry two more links, to the ketiv/qere review and its
# suppressed companion; Ben had them removed on 2026-08-11, the two bodies of
# work being separate and not to be cross-linked. index.html is where both are
# reachable from.
INDEX_PAGE = "index.html"
INDEX_NAV_LABEL = "Index"
THIS_NAV_LABEL = "UXLC suggestions"

# The intro is these, then the four generated paragraphs
# _atom_numbering_paragraph, _forms_paragraph, _manuscript_location_paragraph,
# _brackets_paragraph and _change_items_paragraph build, then
# INTRO_CLOSING_PARAGRAPHS.
INTRO_OPENING_PARAGRAPHS = (
    "Daniel Holman has been sending Chris Kimball and Ben Denckla suggested"
    " changes to the UXLC, a book at a time, and this page collects them. Most"
    " are places where he reads the Leningrad Codex images differently from the"
    " text as it stands; the rest ask the UXLC for a note on a reading Holman"
    " and the UXLC agree about.",
    "Each card is one case, and its labelled lines are Holman's, quoted from the"
    " email as he wrote them, including his spellings of the accent names. Four"
    " things on a card are not: the atom number at its head, which is the UXLC's"
    " and only usually his as well; the manuscript location, which is estimated"
    " here rather than quoted; the Current Text and Suggested Text rows on the"
    " cases whose message gives the two forms no lines of their own; and one"
    " word of his Lev 25:20 case, which had the UXLC's note letter c sitting"
    " inside it. That letter is the note's name rather than part of the word, so"
    " it and the invisible marks his mail client wrapped it in are dropped here.",
)

INTRO_CLOSING_PARAGRAPHS = (
    # uxlc_comments holds no entries yet, so no card has a commentary section.
    # When the first one lands, add to the sentence below: "; the commentary
    # section on a card is a reader's remark and carries no more weight than
    # that".
    "Nothing here is a decision. The suggestions are Chris Kimball's to accept or"
    " decline for the UXLC.",
)


@dataclass(frozen=True)
class RenderedCase:
    number: int
    case: CorrectionCase
    image_hrefs: list[tuple[str, str, int, int]]


def render_uxlc_corrections_html(
    *,
    emails_dir: Path,
    output_html_path: Path,
    image_dir: Path,
    assets_dir: Path,
    data_dir: Path,
    json_output_path: Path,
) -> dict[str, object]:
    emails, cases = apply_bracketed_corrections(*read_emails(emails_dir, image_dir))
    locations = read_locations(data_dir)
    standard_atoms = read_standard_atoms(data_dir)
    require_full_coverage(locations, [case.ref.key for case in cases])
    require_standard_atoms(standard_atoms, [case.ref.key for case in cases])
    require_form_shapes(cases)
    require_known_refs([case.ref.key for case in cases])
    _require_commented_cases_exist(cases)

    rendered = _rendered_cases(cases, image_dir, output_html_path)
    _write_assets(
        assets_dir=assets_dir,
        output_html_path=output_html_path,
        filter_ids=all_filter_ids(cases),
    )
    _write_page(
        emails=emails,
        cases=cases,
        locations=locations,
        standard_atoms=standard_atoms,
        rendered=rendered,
        output_html_path=output_html_path,
    )
    return _write_json(
        emails=emails,
        rendered=rendered,
        standard_atoms=standard_atoms,
        json_output_path=json_output_path,
    )


def _require_commented_cases_exist(cases: list[CorrectionCase]) -> None:
    known = {case.ref.key for case in cases}
    unmatched = sorted(set(COMMENTS_BY_REF) - known)
    if unmatched:
        raise ValueError(
            "uxlc_comments names cases that no email contains: "
            f"{unmatched}. Case keys look like {sorted(known)[0]!r}."
        )


def _rendered_cases(
    cases: list[CorrectionCase], image_dir: Path, output_html_path: Path
) -> list[RenderedCase]:
    """Pair each case with its images' hrefs, captions and pixel dimensions.

    The images are already on disk, written by the ingest step and tracked;
    this only reads each one's size so the markup can reserve its space and a
    #caseNN link lands on a target that does not then drift.
    """
    rendered: list[RenderedCase] = []
    for number, case in enumerate(cases, start=1):
        hrefs: list[tuple[str, str, int, int]] = []
        for image in case.images:
            path = image_dir / image.file_name
            width, height = _png_size(path)
            hrefs.append(
                (relative_href(path, output_html_path), image.caption, width, height)
            )
        rendered.append(RenderedCase(number=number, case=case, image_hrefs=hrefs))
    return rendered


def _png_size(path: Path) -> tuple[int, int]:
    """Width and height straight out of the PNG's IHDR chunk.

    Read by hand because this repo's venv deliberately has no Pillow, and the
    two numbers sit at a fixed offset in every PNG.
    """
    header = path.read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def _write_assets(
    *, assets_dir: Path, output_html_path: Path, filter_ids: list[str]
) -> None:
    colour_rules = "\n".join(
        f".cat-{filter_id} {{ background: {PALETTE[index % len(PALETTE)]}; }}"
        for index, filter_id in enumerate(filter_ids)
    )
    css_text = (assets_dir / "uxlc_corrections.css").read_text(encoding="utf-8")
    css_text = css_text.replace("/* __FILTER_COLORS__ */", colour_rules)
    output_html_path.with_suffix(".css").write_text(
        css_text, encoding="utf-8", newline=""
    )
    output_html_path.with_suffix(".js").write_text(
        (assets_dir / "uxlc_corrections.js").read_text(encoding="utf-8"),
        encoding="utf-8",
        newline="",
    )


def _write_page(
    *,
    emails: list[SourceEmail],
    cases: list[CorrectionCase],
    locations: dict[str, AtomLocation],
    standard_atoms: dict[str, int],
    rendered: list[RenderedCase],
    output_html_path: Path,
) -> None:
    email_by_key = {source_email.key: source_email for source_email in emails}
    cards = "\n".join(
        case_card_html(
            case_number=item.number,
            case=item.case,
            source_email=email_by_key[item.case.email_key],
            location=locations[item.case.ref.key],
            standard_atom=standard_atoms[item.case.ref.key],
            image_hrefs=item.image_hrefs,
            comment_entries=comments_for_ref(item.case.ref.key),
        )
        for item in rendered
    )
    intro = "\n".join(
        f"<p>{escape(text)}</p>"
        for text in _intro_paragraphs(emails, cases, locations, standard_atoms)
    )
    css_href = escape(output_html_path.with_suffix(".css").name)
    js_src = escape(output_html_path.with_suffix(".js").name)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(PAGE_TITLE)}</title>
<link rel="stylesheet" href="{css_href}">
</head>
<body>
<nav class="top-nav">
<a class="nav-link" href="{INDEX_PAGE}">{INDEX_NAV_LABEL}</a>
<a class="nav-link active" href="{escape(output_html_path.name)}">{THIS_NAV_LABEL}</a>
</nav>
<h1>{escape(PAGE_HEADING)}</h1>
<div class="intro">
{intro}
</div>
{_meta_grid_html(cases, emails)}
{summary_html(cases)}
<h2 class="section-title">Cases</h2>
<div class="records">
{cards}
</div>
{_emails_section_html(emails, rendered)}
<script src="{js_src}" defer></script>
</body>
</html>
"""
    output_html_path.parent.mkdir(parents=True, exist_ok=True)
    output_html_path.write_text(html, encoding="utf-8", newline="")


def _intro_paragraphs(
    emails: list[SourceEmail],
    cases: list[CorrectionCase],
    locations: dict[str, AtomLocation],
    standard_atoms: dict[str, int],
) -> tuple[str, ...]:
    return (
        *INTRO_OPENING_PARAGRAPHS,
        _atom_numbering_paragraph(cases, standard_atoms),
        _forms_paragraph(cases),
        _manuscript_location_paragraph(cases, locations),
        _brackets_paragraph(emails, cases),
        _change_items_paragraph(cases),
        *INTRO_CLOSING_PARAGRAPHS,
    )


def _atom_numbering_paragraph(
    cases: list[CorrectionCase], standard_atoms: dict[str, int]
) -> str:
    """The intro's paragraph on the two ways of numbering a verse's atoms.

    Generated because it counts the cards where the two disagree and names them.
    Written out, that list would go quietly wrong the first time a message
    raised a word in a verse with a ketiv/qere pair or a dividing samekh before
    it, and a reader comparing the card against his email is exactly the reader
    who needs it right.
    """
    renumbered = _chapter_verse_list(
        [case for case in cases if standard_atoms[case.ref.key] != case.ref.atom]
    )
    if not renumbered:
        disagreement_sentence = (
            " On every case here the two counts give the same number, so nothing"
            " on a card turns on the difference."
        )
    else:
        disagreement_sentence = (
            f" Holman's number follows the UXLC's in parentheses on the"
            f" {_and_list(renumbered)} "
            + ("card" if len(renumbered) == 1 else "cards")
            + ", and nowhere else."
        )
    return (
        "The atom number at the head of a card is the UXLC's, and on"
        f" {len(renumbered)} of the {len(cases)} cases it is not the number"
        " Holman wrote. Where a verse has a ketiv and a qere, the UXLC numbers"
        " each of them and Holman numbers the pair once; where a samekh divides"
        " a verse, the UXLC numbers that too and Holman does not. Everywhere"
        " else the two counts agree. The UXLC's number is the one shown, because"
        " it is the one that finds the word at tanach.us, whose change list and"
        " note pages both use it." + disagreement_sentence
    )


def _forms_paragraph(cases: list[CorrectionCase]) -> str:
    """The intro's paragraph on the two forms read out of Holman's prose.

    Generated because it counts the cases it applies to and names their books.
    Both would go quietly wrong the first time a message arrived in a shape the
    table in uxlc_holman_forms had to be extended for, which is exactly when a
    reader would want to know how many cards the reading touches.
    """
    read_out = [case for case in cases if forms_for_case(case) is not None]
    books = _and_list(
        sorted(
            {book_display_name(case.ref.book) for case in read_out},
            key=lambda name: min(
                case.ref.sort_key
                for case in read_out
                if book_display_name(case.ref.book) == name
            ),
        )
    )
    note_only = _chapter_verse_list(
        [case for case in read_out if forms_for_case(case).suggested is None]
    )
    note_only_sentence = (
        ""
        if not note_only
        else (
            f" The {_and_list(note_only)} "
            + ("case asks" if len(note_only) == 1 else "cases ask")
            + " only for a note and propose no form, so they have no Suggested"
            " Text row."
        )
    )
    return (
        f"On {len(read_out)} of the {len(cases)} cases, the {books} ones,"
        " Holman's message gives the two forms no lines of their own. The form"
        " as it stands is in parentheses on his Word / Verse line, after a"
        " reference this page already gives at the head of the card, and the"
        " form he proposes is in parentheses inside his suggestion sentence."
        " Both are read out here and given rows of their own, so that every card"
        " reads alike, and where that sentence held the proposed form it no"
        " longer repeats what is now printed above it." + note_only_sentence
    )


def _manuscript_location_paragraph(
    cases: list[CorrectionCase], locations: dict[str, AtomLocation]
) -> str:
    """The intro's paragraph on the estimated manuscript location.

    Generated because it counts the cases where the estimate and Holman's
    reading of the column disagree. Written out, that figure would go quietly
    wrong the first time a message arrived, which is the one moment a reader
    would most want it right.

    The count is over the cases that state a column, not over all of them. Every
    case did state one until the 1 Samuel 28:12 message of 2026-08-23, which
    cites no image at all; counting that one in with the agreeing cases would
    say the estimate agreed with a column Holman never gave, which is the very
    kind of quietly wrong figure the paragraph is generated to avoid.
    """
    with_column = [case for case in cases if _holman_column(case) is not None]
    disagreeing = _chapter_verse_list(
        [
            case
            for case in with_column
            if _holman_column(case) != locations[case.ref.key].column
        ]
    )
    agreeing = len(with_column) - len(disagreeing)
    disagreement_sentence = (
        " It agrees with his column on every case that names one."
        if not disagreeing
        else (
            f" It agrees with his column on {agreeing} of the {len(with_column)}"
            f" cases that name a column, and the {_and_list(disagreeing)} "
            + ("card gives" if len(disagreeing) == 1 else "cards give")
            + " his reading beside the estimate."
        )
    )
    uncited = _chapter_verse_list(
        [case for case in cases if case.image_location is None]
    )
    uncited_sentence = (
        ""
        if not uncited
        else (
            f" The {_and_list(uncited)} "
            + ("case cites" if len(uncited) == 1 else "cases cite")
            + " no scan file, so the estimate stands there with nothing of"
            " Holman's beside it."
        )
    )
    return (
        "The manuscript location on a card is not Holman's. He names the scan"
        " file he worked from and puts the atom in a band of a column of it, as"
        " Col. 2 middle; the file name says nothing a reader can use, so the"
        " card reports an estimated column and line instead, worked out from"
        " the page breaks the UXLC's Leningrad Codex index records and the"
        " count of atoms between them." + disagreement_sentence + " The band is left"
        " out of that comparison, top, middle and bottom being a gloss that a"
        " line number supersedes. The folio link under the line is decoded from"
        " the page ordinal Holman's citation begins with, so the folio number"
        " is not his either." + uncited_sentence
    )


def _holman_column(case: CorrectionCase) -> int | None:
    """The column Holman's citation names, or None where his case names none."""
    image_location = case.image_location
    if image_location is None:
        return None
    position = manuscript_position(image_location)
    return None if position is None else position.column


def _brackets_paragraph(emails: list[SourceEmail], cases: list[CorrectionCase]) -> str:
    """The intro's paragraph on the square brackets, listing what is in them.

    The list is generated, so the page cannot describe a set of corrections it
    is not making. What the brackets mean is the fixed part, because the
    notation says an editor's word is standing in a quotation but not whose.
    """
    return (
        "A word in square brackets is Ben Denckla's, put there afterwards in"
        " place of the word the message has: "
        + "; ".join(bracketed_correction_phrases(emails, cases))
        + f". The one other bracketed phrase on the page is not a correction of"
        f" that kind: {ADDRESS_REDACTION} stands wherever a message gave an"
        " email address."
    )


def _change_items_paragraph(cases: list[CorrectionCase]) -> str:
    """The intro's paragraph about the change-item links, counts and all.

    Generated rather than written out because it counts cases: a message
    arriving, or the UXLC's editor reaching one of the six cases with no change
    item yet, would otherwise leave a written-out figure quietly wrong.
    """
    linked = [case for case in cases if change_record_links(case.ref.key)]
    doubled = _chapter_verse_list(
        [case for case in linked if len(change_record_links(case.ref.key)) > 1]
    )
    doubled_sentence = (
        ""
        if not doubled
        else (
            f" The {_and_list(doubled)} "
            + ("case has" if len(doubled) == 1 else "cases have")
            + " two, one per word of a compound whose two marks the case asks to"
            " exchange."
        )
    )
    return (
        "A card also links whatever the UXLC's editor has entered for that word"
        f" in {CHANGES_PAGE_LABEL}, {CHANGES_PAGE_DESCRIPTION}. Of the"
        f" {len(cases)} cases, {len(linked)} have such a change item and"
        f" {len(cases) - len(linked)} have none.{doubled_sentence} A change item"
        " is the editor's wording rather than Holman's, and the Judges 11:24 one"
        " is older than the message quoted beside it: Ben Denckla entered it in"
        " April, on the same word and about the same indistinct mark."
    )


def _and_list(items: list[str]) -> str:
    if len(items) < 2:
        return "".join(items)
    return f"{', '.join(items[:-1])} and {items[-1]}"


def _chapter_verse_list(cases: list[CorrectionCase]) -> list[str]:
    """The cases named "Leviticus 7:25", in canonical order.

    In canonical order because sorting the rendered strings does not give it:
    "Leviticus 16:21" precedes "Leviticus 7:25" alphabetically, and did so on
    the page until 2026-08-11.
    """
    return [
        f"{book_display_name(case.ref.book)} {case.ref.chapter}:{case.ref.verse}"
        for case in sorted(cases, key=lambda case: case.ref.sort_key)
    ]


def _meta_grid_html(cases: list[CorrectionCase], emails: list[SourceEmail]) -> str:
    books = len({case.ref.book for case in cases})
    boxes = (
        ("Cases", str(len(cases))),
        ("Source emails", str(len(emails))),
        ("Books", str(books)),
        ("Visible/Filtered-out", str(len(cases)) + "/0"),
    )
    rendered = "\n".join(
        (
            '<div class="meta-box">\n'
            f'<div class="meta-label">{escape(label)}</div>\n'
            + (
                '<div class="meta-value" id="visible-filtered-count">'
                if label == "Visible/Filtered-out"
                else '<div class="meta-value">'
            )
            + f"{escape(value)}</div>\n</div>"
        )
        for label, value in boxes
    )
    return f'<div class="meta-grid">\n{rendered}\n</div>'


def _emails_section_html(
    emails: list[SourceEmail], rendered: list[RenderedCase]
) -> str:
    blocks: list[str] = []
    for source_email in emails:
        cases_here = [
            item for item in rendered if item.case.email_key == source_email.key
        ]
        case_links = ", ".join(
            f'<a class="case-link" href="#{case_fragment_id(item.number)}">'
            f"#{item.number}</a>"
            for item in cases_here
        )
        preamble = "\n".join(
            f"<p>{inline_text_html(line)}</p>" for line in source_email.preamble
        )
        closing = "\n".join(
            f"<p>{inline_text_html(line)}</p>" for line in source_email.closing
        )
        # A message stays visible under any filter that keeps one of its cases,
        # so filtering by book does not empty this section.
        filter_ids = sorted(
            {
                filter_id
                for item in cases_here
                for filter_id in case_filter_ids(item.case)
            }
        )
        blocks.append(
            f'<article class="source-email" id="{email_fragment_id(source_email.key)}"'
            f' data-filter-ids="{escape(" ".join(filter_ids))}">\n'
            f"<h3>{escape(source_email.subject)}</h3>\n"
            f'<p class="email-headers">{escape(source_email.sender_name)}, '
            f"{escape(source_email.date_display)}"
            f" &middot; {len(cases_here)} case"
            f"{'' if len(cases_here) == 1 else 's'}: {case_links}</p>\n"
            f'<div class="email-prose">\n{preamble}\n{closing}\n</div>\n'
            f'<p class="email-file">Source: <code>'
            f"{escape(source_email.source_file_name)}</code></p>\n"
            "</article>"
        )
    return (
        '<h2 class="section-title">Source emails</h2>\n'
        '<p class="section-note">The greeting and sign-off of each message, with its'
        " cases linked. The body of every case is on its card above. Email"
        f" addresses are replaced with {escape(ADDRESS_REDACTION)}, and a word in"
        " square brackets is Ben Denckla's in place of the message's own, as the"
        " intro above says; nothing else is edited. The date is the date of the"
        " message itself, so the one"
        " forwarded to supply attachments left off a first send carries the"
        " forwarding date, and the original send time stands in the forwarded"
        " header quoted below it.</p>\n"
        '<div class="source-emails">\n' + "\n".join(blocks) + "\n</div>"
    )


def _write_json(
    *,
    emails: list[SourceEmail],
    rendered: list[RenderedCase],
    standard_atoms: dict[str, int],
    json_output_path: Path,
) -> dict[str, object]:
    payload = {
        # Every case's change_record_ids below are anchors on this one page.
        "change_records_page_url": CHANGES_PAGE_URL,
        "source_emails": [
            {
                "key": source_email.key,
                "source_file_name": source_email.source_file_name,
                "subject": source_email.subject,
                "from": source_email.sender_name,
                "date": source_email.date_iso,
                "preamble": list(source_email.preamble),
                "closing": list(source_email.closing),
            }
            for source_email in emails
        ],
        "cases": [
            {
                "case_number": item.number,
                "ref": item.case.ref.key,
                "book": item.case.ref.book,
                "book_display": book_display_name(item.case.ref.book),
                "chapter": item.case.ref.chapter,
                "verse": item.case.ref.verse,
                # Holman's number, then the UXLC's, which is what the card
                # shows. They are the same on all but a few cases; see
                # hkq_cmn/uxlc_standard_atoms.
                "atom": item.case.ref.atom,
                "standard_atom": standard_atoms[item.case.ref.key],
                "email_key": item.case.email_key,
                "index_in_email": item.case.index_in_email,
                "heading": item.case.heading,
                "fields": [
                    {"label": label, "value": value}
                    for label, value in item.case.fields
                ],
                # The two forms read out of the prose of a message that gives
                # them no lines of their own, absent on a case that does. Kept
                # here so that regenerating and reading the diff tests the
                # reading, the way it tests the parse of everything above.
                **_forms_json(item.case),
                "manuscript_folio": _folio_or_none(item.case.image_location),
                "change_record_ids": [
                    link.record_id for link in change_record_links(item.case.ref.key)
                ],
                "images": [
                    {
                        "attachment": image.source_filename,
                        "caption": image.caption,
                        "file": image.file_name,
                    }
                    for image in item.case.images
                ],
            }
            for item in rendered
        ],
    }
    json_output_path.parent.mkdir(parents=True, exist_ok=True)
    json_output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="",
    )
    return {
        "email_count": len(emails),
        "case_count": len(rendered),
        "image_count": sum(len(item.image_hrefs) for item in rendered),
        "change_record_count": sum(
            len(change_record_links(item.case.ref.key)) for item in rendered
        ),
        "commented_case_count": sum(
            1 for item in rendered if comments_for_ref(item.case.ref.key)
        ),
    }


def _forms_json(case: CorrectionCase) -> dict[str, object]:
    forms = forms_for_case(case)
    if forms is None:
        return {}
    return {
        "forms_read_from_prose": {
            "current": forms.current,
            "suggested": forms.suggested,
            "suggestion_without_form": forms.suggestion,
        }
    }


def _folio_or_none(image_location: str | None) -> str | None:
    if image_location is None:
        return None
    page = manuscript_page(image_location)
    return None if page is None else page.folio_label
