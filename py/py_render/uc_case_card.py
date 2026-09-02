"""Render one of Holman's suggestions as a card."""

from __future__ import annotations

from html import escape
import os
from pathlib import Path

from py_render.rt_html_utils import external_link_html, record_category_badge_html
from py_render.uc_comments import comments_html
from py_render.uc_hebrew_runs import inline_text_html
from hkq_cmn.uxlc_atom_locations import AtomLocation
from hkq_cmn.uxlc_change_records import change_record_links
from hkq_cmn.uxlc_email_extract import (
    CorrectionCase,
    FIRST_FIELD_LABELS,
    IMAGE_LOCATION_LABELS,
    KNOWN_FIELD_LABELS,
    SourceEmail,
    book_slug,
)
from hkq_cmn.uxlc_external_links import book_display_name, verse_links
from hkq_cmn.uxlc_holman_forms import (
    HolmanForms,
    SUGGESTION_LABEL,
    forms_for_case,
)
from hkq_cmn.uxlc_manuscript_page import (
    manuscript_page,
    manuscript_position,
    sefaria_image_url,
)

# The label the derived "as it stands" row is given. Holman spells his own such
# line "Current UXLC" on five cases and "Current Text" on six, and Ben asked on
# 2026-08-11 that those two be left as he wrote them; this row is not his, so it
# takes the commoner of the two rather than inventing a third spelling.
DERIVED_CURRENT_LABEL = "Current Text"

# The labels are Holman's, verbatim from his emails, and the parser keeps them
# that way. These two are relabelled for display only: the page says
# "suggestion" where it has the choice, and "Corrected Text" and "Suggested
# Correction" are the two labels where it has one.
# The messages from Chronicles onwards spell the same two lines "Target Text"
# and "Correction", so they take the same two display labels: the page says
# "suggestion" wherever it has the choice, and a shorter spelling of Holman's
# does not change which line it is. "Change", the 1 Samuel 28:12 message's
# spelling of the proposed form, is a third of the same kind.
#
# His own "Current" line, that message's spelling of the form as it stands, is
# NOT relabelled: Ben asked on 2026-08-11 that the two spellings Holman had then
# -- "Current UXLC" and "Current Text" -- be left as he wrote them, and this is
# a third of those rather than a second name for the suggested-text row.
DISPLAY_FIELD_LABELS = {
    "Corrected Text": "Suggested Text",
    "Target Text": "Suggested Text",
    "Change": "Suggested Text",
    "Suggested Correction": "Suggestion",
    "Correction": "Suggestion",
}

# Holman spells the image-location label three ways, and the value under it is
# no longer his citation but an estimate derived here, so the three collapse to
# one label of our own.
MANUSCRIPT_LOCATION_LABEL = "Manuscript location"

# The rank a case with no citation of its own borrows, so that its estimate-only
# manuscript-location row sits where a citation would have put it. Any of the
# image-location labels would do -- _FIELD_ORDER holds them as one contiguous
# block -- and this is that block's first member.
_LOCATION_RANK_LABEL = sorted(IMAGE_LOCATION_LABELS)[0]

# The order the fields are shown in. This is the message's own order with ONE
# field moved: Holman writes the current text, then where he read it, then what
# he proposes, then the resulting text, and Ben asked on 2026-08-11 for the
# current text and the suggested text next to each other. So the suggested text
# moves up to sit under the current one, and nothing else moves.
#
# Do not tidy this into a "sensible" order. A first pass also moved the
# manuscript location below the suggestion, which reads well enough and was not
# asked for; Ben's reply the same day was that the card changes "seemed to go
# way beyond what I asked". The nine cases whose message has no Corrected Text
# field are therefore shown in exactly their message order.
_FIELD_ORDER = (
    *FIRST_FIELD_LABELS,
    "Corrected Text",
    "Target Text",
    "Change",
    *sorted(IMAGE_LOCATION_LABELS),
    "Suggested Correction",
    "Correction",
    "Critical Note",
    "Note",
)
_FIELD_RANK = {label: rank for rank, label in enumerate(_FIELD_ORDER)}
_UNRANKED_LABELS = KNOWN_FIELD_LABELS - set(_FIELD_RANK)
if _UNRANKED_LABELS:
    raise AssertionError(
        f"no display rank for the field labels {sorted(_UNRANKED_LABELS)}; add "
        "them to _FIELD_ORDER, which decides what a card shows first"
    )


def case_fragment_id(case_number: int) -> str:
    return f"case{case_number:02d}"


def book_filter_id(book: str) -> str:
    return f"book-{book_slug(book)}"


def email_fragment_id(email_key: str) -> str:
    return f"src-{email_key}"


def case_filter_ids(case: CorrectionCase) -> tuple[str, ...]:
    return (book_filter_id(case.ref.book),)


def case_card_html(
    *,
    case_number: int,
    case: CorrectionCase,
    source_email: SourceEmail,
    location: AtomLocation,
    standard_atom: int,
    image_hrefs: list[tuple[str, str, int, int]],
    comment_entries: tuple[dict[str, object], ...],
) -> str:
    fragment_id = case_fragment_id(case_number)
    filter_ids = case_filter_ids(case)
    badges = record_category_badge_html(
        filter_id=book_filter_id(case.ref.book),
        label=book_display_name(case.ref.book),
    )
    fields = _fields_html(case, location)
    provenance = (
        '<p class="case-source">Holman\'s case '
        f"{case.index_in_email} in "
        f'<a href="#{email_fragment_id(case.email_key)}">'
        f"{escape(source_email.subject)}</a>, "
        f"{escape(source_email.date_display)}.</p>"
    )
    return f"""<article
id="{fragment_id}"
class="record-card"
data-filter-ids="{escape(' '.join(filter_ids))}"
>
<div class="record-head">
<a class="record-ref" href="#{fragment_id}">#{case_number}</a>
<span class="record-verse">{_verse_ref_html(case, standard_atom)}</span>
<span class="category-badges">
{badges}
</span>
</div>
<div class="record-grid">
<div>
<dl class="case-fields">
{fields}
</dl>
{provenance}
</div>
<div class="image-panel">
{_images_html(image_hrefs)}
</div>
</div>
{comments_html(comment_entries)}
</article>"""


def _verse_ref_html(case: CorrectionCase, standard_atom: int) -> str:
    """The reference at the head of the card, numbered as the UXLC numbers it.

    Holman's number follows in parentheses on the few cases where his count and
    the UXLC's disagree, and nowhere else -- on the other cases there is nothing
    to record, the two being the same number. The intro says what the two counts
    are; ``hkq_cmn.uxlc_standard_atoms`` says how that was established.
    """
    ref = case.ref
    reference = (
        f"{book_display_name(ref.book)} {ref.chapter}:{ref.verse}, atom {standard_atom}"
    )
    if standard_atom != ref.atom:
        reference += f" (Holman's {ref.atom})"
    links = "\n".join(
        external_link_html(href=link.href, label=link.label, title=link.title)
        for link in verse_links(ref.book, ref.chapter, ref.verse)
    )
    return f"{escape(reference)}\n{links}\n{_change_record_links_html(case)}"


def _change_record_links_html(case: CorrectionCase) -> str:
    """The change list's records for this case, or nothing when it has none.

    Labelled with the record's own id, which is the date it was entered and its
    sequence number within that date, so the Judges record's April date shows
    on the link that it is older than the message the card quotes.
    """
    return "\n".join(
        external_link_html(
            href=link.href, label=f"Change {link.record_id}", title=link.title
        )
        for link in change_record_links(case.ref.key)
    )


def _fields_html(case: CorrectionCase, location: AtomLocation) -> str:
    """One row per field, with the manuscript location always a single row.

    The Psalms and Proverbs messages state the citation on two lines, the scan
    file under "Image" and the column under "Location" or "Location R/L". Both
    are image-location fields and the row is the same row, so the first of them
    carries it -- built from ``case.image_location``, which is the two rejoined
    -- and the rest are dropped rather than repeating it.

    The row is shown on a case that cites no image at all as well. What it
    states is the estimate, which every case has -- ``uxlc_atom_locations``'
    ``require_full_coverage`` raises otherwise -- and a citation only ever adds
    the "Holman gives ..." clause to it and the folio link's neighbours. The 1
    Samuel 28:12 message of 2026-08-23 is the first with no citation, and
    without this the card would have lost the estimate and the folio link that
    every other card carries.
    """
    forms = forms_for_case(case)
    displayed = _displayed_fields(case, forms)
    if not any(label in IMAGE_LOCATION_LABELS for label, _value in displayed):
        displayed = [*displayed, (_LOCATION_RANK_LABEL, "")]
    ordered = sorted(displayed, key=lambda field: _FIELD_RANK[field[0]])
    image_location = case.image_location
    rows = []
    location_shown = False
    for label, value in ordered:
        if label in IMAGE_LOCATION_LABELS:
            if location_shown:
                continue
            location_shown = True
            rows.append(
                _field_html(
                    MANUSCRIPT_LOCATION_LABEL,
                    _manuscript_location_html(image_location or value, location),
                )
            )
            continue
        rows.append(
            _field_html(DISPLAY_FIELD_LABELS.get(label, label), inline_text_html(value))
        )
    return "\n".join(rows)


def _displayed_fields(
    case: CorrectionCase, forms: HolmanForms | None
) -> list[tuple[str, str]]:
    """The message's fields, or the same with the two forms given rows of their own.

    Holman's Exodus, Leviticus and Deuteronomy messages state neither form on a
    line of its own: the form as it stands is in parentheses on the Word / Verse
    line, after a reference the card's heading already carries, and the form he
    proposes is in parentheses inside his suggestion sentence. Ben asked on
    2026-08-11 that those cases read like the Joshua, Judges and Samuel ones, so
    the Word / Verse line -- which holds nothing else the card does not already
    show -- gives way to a row per form, and the sentence loses the form now
    printed above it.

    Returned under Holman's own labels rather than the display ones, so that the
    single ranking in _FIELD_ORDER still decides the order.
    """
    if forms is None:
        return list(case.fields)
    fields: list[tuple[str, str]] = [(DERIVED_CURRENT_LABEL, forms.current)]
    if forms.suggested is not None:
        fields.append(("Corrected Text", forms.suggested))
    for label, value in case.fields:
        if label in FIRST_FIELD_LABELS:
            continue
        fields.append((label, forms.suggestion if label == SUGGESTION_LABEL else value))
    return fields


def _field_html(label: str, value_html: str) -> str:
    return (
        f'<div class="case-field">\n'
        f"<dt>{escape(label)}</dt>\n"
        f"<dd>{value_html}</dd>\n"
        f"</div>"
    )


def _manuscript_location_html(image_location: str, location: AtomLocation) -> str:
    """The estimated folio, column and line, with Holman's where they differ.

    Holman's citation names the scan file he worked from and puts the atom in a
    band of a column of it. The file name says nothing a reader can use, so it
    is not shown; the column and the folio his ordinal decodes to are both
    discrete facts the estimate states too, so both are compared and his reading
    is given whenever they disagree. The band is not compared: top, middle and
    bottom are a gloss that a line number supersedes, and testing them against
    equal nine-line thirds would report disagreements a line wide as real ones.

    The folio was the card's own answer until 2026-08-12, when five citations
    turned out to name a scan whose file name says outright that it cannot hold
    the case's verse. ``uxlc_manuscript_page`` names the five and records Ben's
    decision that the card stop echoing them.
    """
    text = f"Column {location.column}, line {location.rounded_line} or thereabouts."
    holman_position = manuscript_position(image_location)
    if holman_position is not None and holman_position.column != location.column:
        text += f" Holman gives {holman_position.display}."
    holman_page = manuscript_page(image_location)
    if holman_page is not None and holman_page.folio_label != location.folio:
        text += f" Holman cites folio {holman_page.folio_label}."
    return escape(text) + _folio_link_html(location)


def _folio_link_html(location: AtomLocation) -> str:
    """The Sefaria image of the estimated leaf.

    Every case has an estimate -- ``uxlc_atom_locations.require_full_coverage``
    raises otherwise -- so unlike the citation this once decoded, this link is
    on every card.
    """
    link = external_link_html(
        href=sefaria_image_url(location.folio), label=f"folio {location.folio}"
    )
    return f'\n<span class="folio-links">{link}</span>'


def _images_html(image_hrefs: list[tuple[str, str, int, int]]) -> str:
    """The attached crops, uncaptioned.

    The caption Holman's filenames carry stays in the data and reaches the alt
    attribute, which is not what a caption is: it is read only where the image
    itself cannot be seen, so it is not the clutter on every card that the
    visible caption was.
    """
    if not image_hrefs:
        return '<p class="no-image">No image attached</p>'
    figures = "\n".join(
        (
            "<figure>\n"
            f'<a href="{escape(href)}" target="_blank" rel="noopener">'
            f'<img class="image-thumb" src="{escape(href)}"'
            f' width="{width}" height="{height}" loading="lazy" decoding="async"'
            f' alt="{escape(caption)}"></a>\n'
            "</figure>"
        )
        for href, caption, width, height in image_hrefs
    )
    return f'<div class="image-strip">\n{figures}\n</div>'


def relative_href(asset_path: Path, output_html_path: Path) -> str:
    return os.path.relpath(asset_path, output_html_path.parent).replace("\\", "/")
