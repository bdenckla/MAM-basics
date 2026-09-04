"""One card per suggested correction to MAM, for the shared findings report.

A sibling of ``rt_record_card``, which builds the ketiv/qere review's cards, and
deliberately not an extension of it: the two record kinds share a page, a
stylesheet and a filter mechanism, and share nothing else.  A ketiv/qere row has a
finding label, a ketiv/qere pair, a GitHub issue and two manuscript crops; a MAM
suggestion has two forms of one atom, Holman's description of the difference, one
crop, and no issue.  Threading both through one builder would mean a function
whose every other line asked which kind it had.

WHAT A CARD SHOWS THAT THE EXTRACT DOES NOT SAY OUTRIGHT.  The comparison table
puts MAM's form and the comparison edition's on adjacent rows, which is the
contrast the case is about and is one mark wide; the notes below it carry Holman's
own description and, where he gave one, his suggestion.  Where the extract
corrected something -- an atom index, or a suggestion -- the card says so and
names the corrector, because a reader looking at a form has no other way to know
that the record differs from the message it came from.
"""

from __future__ import annotations

from html import escape
import os
from pathlib import Path
import re
from typing import Any

from py_render.rt_external_links import verse_external_links
from py_render.rt_html_utils import (
    external_link_html,
    join_nonempty_html_blocks,
    note_line_html,
    record_category_badge_html,
)
from py_render.rt_render_utils import as_optional_text, as_text
from py_render.rt_suggestion_context import ContextLink
from py_render.rt_suggestion_kinds import (
    kind_display_text,
    kind_filter_id,
    suggestion_kind,
)

MAM_ROW_NAME = "MAM"

# Cases whose comparison table is set with extra letter spacing, so that WHICH
# LETTER an accent belongs to can be seen.  Ben Denckla asked for these two on
# 2026-09-02: in וַיֹּ֥אמֶר against וַ֥יֹּאמֶר the merkha moves between adjacent
# letters, and in זֵ֣רוּ against זֵר֣וּ the munax does, and at normal spacing a
# reader cannot tell which letter carries the mark in either.
#
# Per case rather than for every card, because the spacing is a fix for a
# specific difficulty and looks like a typographic tic where there is no such
# difficulty.  Keyed by the reference as Holman sent it, as the corrections and
# dispositions tables are, so a derived atom index moving does not orphan an entry.
#
# The class and its rule are not invented here: ``*.extra-letter-spacing {
# letter-spacing: 0.1em; }`` is one line, identical in seven stylesheets across
# these repos, and ``py/author_misc/rocc_2_pre_vowel_accents_in_ctr.py`` already
# uses it for this same purpose -- showing where an accent sits relative to a
# vowel.  Its comment there reads "span or bdi", and a bdi is what these are.
EXTRA_LETTER_SPACING_REFS = frozenset({"Judg 10:11.1", "Zech 2:4.11"})


def suggestion_fragment_id(case_number: int) -> str:
    """The card's anchor, e.g. ``mam007``.

    Deliberately not of the ``row<N>`` shape the ketiv/qere cards use: the report's
    two pages carry a redirect script that sends an unknown ``row<N>`` fragment to
    the other page, and a MAM suggestion is on one page only, so it must not match
    that pattern.
    """
    return f"mam{case_number:03d}"


def suggestion_card_html(
    *,
    case: dict[str, Any],
    output_html_path: Path,
    data_root: Path,
    source_message_dates: dict[str, str],
    context_links: dict[str, ContextLink] | None = None,
) -> str:
    case_number = int(as_text(case.get("case_number", "0")))
    fragment_id = suggestion_fragment_id(case_number)
    mam_form = as_text(case.get("mam_form", ""))
    comparison_form = as_text(case.get("comparison_form", ""))
    comparison_edition = as_text(case.get("comparison_edition", ""))
    kind = suggestion_kind(mam_form, comparison_form)
    filter_id = kind_filter_id(kind)

    verse_text = (
        f"{as_text(case.get('std_book_name', ''))} "
        f"{as_text(case.get('chapter', ''))}:{as_text(case.get('verse', ''))}"
        f".{as_text(case.get('atom', ''))}"
    )
    verse_ref_html = _verse_ref_html(verse_text)

    ref_as_sent = as_text(case.get("ref_as_sent") or case.get("ref", ""))
    comparison_html = _comparison_table_html(
        [
            (MAM_ROW_NAME, mam_form),
            (comparison_edition, comparison_form),
        ],
        extra_letter_spacing=ref_as_sent in EXTRA_LETTER_SPACING_REFS,
    )

    notes_html = join_nonempty_html_blocks(
        _disposition_html(case),
        _optional_note("Holman:", as_optional_text(case.get("description"))),
        _suggestion_html(case),
        _corrected_form_html(case),
        _as_sent_html(case),
        _atom_note_html(case),
        _source_note_html(case, source_message_dates),
        _context_link_html((context_links or {}).get(ref_as_sent)),
    )

    images_html = _image_paths_html(
        image_paths=case.get("image_files"),
        label=comparison_edition,
        output_html_path=output_html_path,
        data_root=data_root,
    )

    badge_html = record_category_badge_html(
        filter_id=filter_id, label=kind_display_text(kind)
    )

    return f"""<article
id="{fragment_id}"
class="record-card"
data-filter-ids="{escape(filter_id)}"
>
<div class="record-head">
<a class="record-ref" href="#{fragment_id}">M{case_number}</a>
<span class="record-verse">
{verse_ref_html}
</span>
<span class="category-badges">
{badge_html}
</span>
</div>
<div class="record-grid">
<div>
{comparison_html}
{notes_html}
</div>
<div>
<div class="image-panel">
<div class="image-caption">{escape(comparison_edition)}</div>
<div class="image-strip">
{images_html}
</div>
</div>
</div>
</div>
</article>"""


def _context_link_html(link: ContextLink | None) -> str:
    """A neutral pointer to a page giving this case's mark some background, or nothing.

    LAST on the card, under the notes, because it is the only line that is not about this
    case: everything above it is Holman's message and what the ingest derived from it, and
    this points at a page written afterwards about the kind of mark the case is about.

    The label and the href are escaped and nothing is interpreted: unlike the prose notes,
    which honour one markdown-style link convention, a context link is a pair of fields from
    ``rt_suggestion_context`` and carries no text from the extract at all.
    """
    if link is None:
        return ""
    return (
        '<div class="note-line"><span class="label">Background:</span> '
        f'<a href="{escape(link.href)}">{escape(link.label)}</a></div>'
    )


def _comparison_table_html(
    rows: list[tuple[str, str]], extra_letter_spacing: bool = False
) -> str:
    """Two columns, and every Hebrew cell declared ``dir="rtl"``.

    The declaration says what the cell holds, and right-justification follows from
    that; a literal ``text-align`` would say only how it should look.  The name
    column is English and is left alone.

    ``extra_letter_spacing`` widens the gaps between letters so that which letter
    an accent belongs to can be seen -- see ``EXTRA_LETTER_SPACING_REFS`` for which
    cases get it and why it is not simply always on.
    """
    value_class = (
        "pointed-heb extra-letter-spacing" if extra_letter_spacing else "pointed-heb"
    )
    body = "\n".join(
        (
            "<tr>\n"
            f'<td class="comparison-name-col">{escape(name)}</td>\n'
            f'<td class="comparison-value-col" dir="rtl">'
            f'<bdi class="{value_class}">{escape(value)}</bdi></td>\n'
            "</tr>"
        )
        for name, value in rows
    )
    return (
        '<table class="comparison-table">\n'
        "<thead>\n<tr>\n<th>name</th>\n<th>value</th>\n</tr>\n</thead>\n"
        f"<tbody>\n{body}\n</tbody>\n</table>"
    )


def _disposition_html(case: dict[str, Any]) -> str:
    """The ruling on this suggestion, where one has been made, FIRST on the card.

    First because it changes how everything below it is read: a reader who does
    not know a suggestion has been ruled on will take the lines under it as
    still standing.  Two lines, the short statement and then the reasoning with
    whoever reached it named -- ``mam_suggestion_dispositions`` says why naming
    them is right where storing the surrounding correspondence is not.
    """
    disposition = case.get("disposition")
    if not isinstance(disposition, dict):
        return ""
    summary = as_optional_text(disposition.get("summary"))
    reason = as_optional_text(disposition.get("reason"))
    # The label is the outcome -- "Suggestion not taken" -- and NOT the state.
    # The state is "suppressed" for every ruling, so labelling the line with it
    # said only what the page it sits on already says, and prefixing the outcome
    # to the summary instead would give a line with two colons in it.
    outcome = as_optional_text(disposition.get("outcome")) or "Handled"
    # BOTH lines are English prose and both go through _prose_note_html, for the
    # reason that function gives.  The summary needs it as much as the reason
    # does: "MAM now has the pashta repeated over the ש" names one Hebrew letter,
    # which was enough for note_line_html to set the whole sentence in a Hebrew
    # font.  Only the summaries that happened to quote no letter looked right,
    # which is the worst way for a bug like this to present.
    return join_nonempty_html_blocks(
        "" if summary is None else _prose_note_html(label=f"{outcome}:", value=summary),
        "" if reason is None else _prose_note_html(label="Why:", value=reason),
    )


def _prose_note_html(label: str, value: str) -> str:
    """A note line whose value is English prose, Hebrew letters included.

    NOT ``note_line_html``, whose "does this contain a Hebrew character" test is
    right for a value that IS a Hebrew form and wrong for a sentence with a letter
    or two quoted inside it: that test wrapped this whole reason in
    ``<bdi class="pointed-heb">``, setting an English paragraph in a Hebrew font
    because it named the כ and the ו.  Hebrew in the middle of an English line
    needs no wrapper at all -- what needs one is a line that STARTS on Hebrew, and
    this one starts on a name.
    """
    return (
        f'<div class="note-line"><span class="label">{escape(label)}</span> '
        f"<span>{_prose_with_links_html(value)}</span></div>"
    )


# A markdown-style inline link inside a prose field. These accept only an external
# https URL or an M-card fragment on this generated page: everything outside a match
# is escaped as before, the href is escaped, and no other scheme or fragment matches.
_PROSE_LINK_RE = re.compile(r"\[([^\]\n]+)\]\((https://[^\s)]+|#mam[0-9]{3})\)")


def _prose_with_links_html(value: str) -> str:
    """Escape prose, turning an approved markdown-style link into a real link.

    The alternative was a bare URL in the text, and Ben Denckla ruled against that
    on 2026-09-02: a Hebrew Wikisource diff URL is a massive percent-encoded
    string, and printing it raw is both unreadable and faintly alarming to look
    at.  A link under an ordinary word -- "the change" -- says the same thing.

    The data stays data: a reason is plain text with this one lightweight
    convention, never raw HTML, so nothing in the extract can put markup on a page.
    """
    parts: list[str] = []
    position = 0
    for match in _PROSE_LINK_RE.finditer(value):
        parts.append(escape(value[position : match.start()]))
        href = match.group(2)
        target = "" if href.startswith("#") else ' target="_blank" rel="noopener"'
        parts.append(f'<a href="{escape(href)}"{target}>{escape(match.group(1))}</a>')
        position = match.end()
    parts.append(escape(value[position:]))
    return "".join(parts)


def _optional_note(label: str, value: str | None) -> str:
    if not value:
        return ""
    return note_line_html(label=label, value=value)


def _corrector_of(case: dict[str, Any], field: str) -> str | None:
    """Who corrected one field of this case, or None if nobody did."""
    corrections = case.get("corrections")
    if not isinstance(corrections, list):
        return None
    for correction in corrections:
        if (
            isinstance(correction, dict)
            and as_text(correction.get("field", "")) == field
        ):
            return as_text(correction.get("corrected_by", "")) or None
    return None


def _suggestion_html(case: dict[str, Any]) -> str:
    """Holman's suggestion, annotated where somebody has corrected it.

    THE ANNOTATION GOES HERE AND NOT ON THE "AS SENT" LINE, which is Ben Denckla's
    correction of 2026-09-02 and is a point about honesty rather than layout: an
    "as sent" field must hold exactly what was sent, and "Place Mereka on first
    syllable — corrected by Ben Denckla" is not what Holman sent.  The corrected
    value is the one that carries who changed it and a pointer to the original.
    """
    value = as_optional_text(case.get("suggestion"))
    if value is None:
        return ""
    corrected_by = _corrector_of(case, "suggestion")
    if corrected_by is not None:
        label = _corrected_field_label("suggestion")
        value = f'{value} — corrected by {corrected_by} (see "{label} as sent")'
    return note_line_html(label="Suggestion:", value=value)


# Reader-facing names for the fields a correction can replace.  Capitalizing the
# field name is not good enough: it put "Comparison_form as sent" on the card when
# the second entry was added on 2026-09-02, an identifier on a page written for
# Hebrew-Bible readers.  A field with no entry raises, because this table and the
# corrections table are both short and hand-maintained.
_CORRECTED_FIELD_LABELS = {
    "suggestion": "Suggestion",
    "comparison_form": "Comparison form",
}


def _corrected_field_label(field: str) -> str:
    label = _CORRECTED_FIELD_LABELS.get(field)
    if label is None:
        raise ValueError(
            f"no reader-facing label for corrected field {field!r}; add one to "
            "_CORRECTED_FIELD_LABELS rather than letting the field name render"
        )
    return label


def _corrected_form_html(case: dict[str, Any]) -> str:
    """Say that the comparison form shown above is not verbatim Holman.

    The suggestion line carries its attribution inline, appended to its own text.
    A form cannot: it sits in a Hebrew cell of the comparison table, where an
    English clause does not belong.  So a corrected form gets this line instead,
    and the bare "as sent" line below still holds exactly what Holman sent.
    """
    corrected_by = _corrector_of(case, "comparison_form")
    if corrected_by is None:
        return ""
    label = _corrected_field_label("comparison_form")
    return note_line_html(
        label=f"{label}:",
        value=f'corrected by {corrected_by} (see "{label} as sent")',
    )


def _as_sent_html(case: dict[str, Any]) -> str:
    """What Holman actually sent, verbatim, for each field somebody corrected.

    Bare: no attribution and no commentary, for the reason the function above
    gives.  A reader comparing the card against his message finds this line
    identical to it.
    """
    corrections = case.get("corrections")
    if not isinstance(corrections, list):
        return ""
    lines: list[str] = []
    for correction in corrections:
        if not isinstance(correction, dict):
            continue
        field = as_text(correction.get("field", ""))
        as_sent = as_optional_text(case.get(f"{field}_as_sent"))
        if as_sent is None:
            continue
        lines.append(
            note_line_html(
                label=f"{_corrected_field_label(field)} as sent:", value=as_sent
            )
        )
    return "\n".join(lines)


def _atom_note_html(case: dict[str, Any]) -> str:
    """The atom index, and Holman's where the derivation corrected it."""
    atom = as_text(case.get("atom", ""))
    check = case.get("mam_plus_check")
    atom_count = as_text(check.get("atom_count", "")) if isinstance(check, dict) else ""
    as_sent = as_optional_text(case.get("atom_as_sent"))
    value = f"{atom} of {atom_count}" if atom_count else atom
    if as_sent is not None:
        value = f"{value} (as sent: {as_sent})"
    return note_line_html(label="Atom:", value=value)


def _source_note_html(
    case: dict[str, Any], source_message_dates: dict[str, str]
) -> str:
    keys = case.get("source_message_keys")
    if not isinstance(keys, list) or not keys:
        return ""
    dates = sorted(
        {source_message_dates[key] for key in keys if key in source_message_dates}
    )
    if not dates:
        return ""
    label = "Message:" if len(dates) == 1 else "Messages:"
    return note_line_html(label=label, value=", ".join(dates))


def _image_paths_html(
    image_paths: object,
    label: str,
    output_html_path: Path,
    data_root: Path,
) -> str:
    if not isinstance(image_paths, list) or not image_paths:
        return f'<span class="label">No {escape(label)} image</span>'

    output_dir = output_html_path.parent.resolve()
    rendered: list[str] = []
    for index, path_obj in enumerate(image_paths, start=1):
        if not isinstance(path_obj, str) or not path_obj.strip():
            continue
        absolute_asset = (data_root / path_obj.replace("\\", "/")).resolve()
        rel_asset = escape(
            os.path.relpath(absolute_asset, output_dir).replace("\\", "/")
        )
        rendered.append(
            f"<a\n"
            f'href="{rel_asset}"\n'
            f'target="_blank"\n'
            f'rel="noopener"\n'
            f">\n"
            f"<img\n"
            f'class="image-thumb"\n'
            f'src="{rel_asset}"\n'
            f'alt="{escape(label)} image {index}"\n'
            f">\n"
            f"</a>"
        )
    if not rendered:
        return f'<span class="label">No {escape(label)} image</span>'
    return "\n".join(rendered)


def _verse_ref_html(verse_text: str) -> str:
    links = verse_external_links(verse_text)
    return "\n".join(
        [
            escape(verse_text),
            external_link_html(href=links.mgketer_url, label="mgketer"),
            external_link_html(href=links.mwd_url, label="MwD"),
            external_link_html(href=links.mam_ws_url, label="MAM-ws"),
        ]
    )
