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
own description and, where he gave one, his recommendation.  Where the extract
corrected something -- an atom index, or a recommendation -- the card says so and
names the corrector, because a reader looking at a form has no other way to know
that the record differs from the message it came from.
"""

from __future__ import annotations

from html import escape
import os
from pathlib import Path
from typing import Any

from py_render.rt_external_links import verse_external_links
from py_render.rt_html_utils import (
    external_link_html,
    join_nonempty_html_blocks,
    note_line_html,
    record_category_badge_html,
)
from py_render.rt_render_utils import as_optional_text, as_text
from py_render.rt_suggestion_kinds import (
    kind_display_text,
    kind_filter_id,
    suggestion_kind,
)

MAM_ROW_NAME = "MAM"


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

    comparison_html = _comparison_table_html(
        [
            (MAM_ROW_NAME, mam_form),
            (comparison_edition, comparison_form),
        ]
    )

    notes_html = join_nonempty_html_blocks(
        _optional_note("Holman:", as_optional_text(case.get("description"))),
        _optional_note("Suggestion:", as_optional_text(case.get("recommendation"))),
        _corrections_html(case),
        _atom_note_html(case),
        _source_note_html(case, source_message_dates),
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


def _comparison_table_html(rows: list[tuple[str, str]]) -> str:
    """Two columns, and every Hebrew cell declared ``dir="rtl"``.

    The declaration says what the cell holds, and right-justification follows from
    that; a literal ``text-align`` would say only how it should look.  The name
    column is English and is left alone.
    """
    body = "\n".join(
        (
            "<tr>\n"
            f'<td class="comparison-name-col">{escape(name)}</td>\n'
            f'<td class="comparison-value-col" dir="rtl">'
            f'<bdi class="pointed-heb">{escape(value)}</bdi></td>\n'
            "</tr>"
        )
        for name, value in rows
    )
    return (
        '<table class="comparison-table">\n'
        "<thead>\n<tr>\n<th>name</th>\n<th>value</th>\n</tr>\n</thead>\n"
        f"<tbody>\n{body}\n</tbody>\n</table>"
    )


def _optional_note(label: str, value: str | None) -> str:
    if not value:
        return ""
    return note_line_html(label=label, value=value)


def _corrections_html(case: dict[str, Any]) -> str:
    """Say that a field was corrected, and by whom, wherever one was.

    A reader comparing the card against Holman's message would otherwise find a
    difference and have no way to tell a correction from a transcription error.
    """
    corrections = case.get("corrections")
    if not isinstance(corrections, list):
        return ""
    lines: list[str] = []
    for correction in corrections:
        if not isinstance(correction, dict):
            continue
        field = as_text(correction.get("field", ""))
        corrected_by = as_text(correction.get("corrected_by", ""))
        as_sent = as_optional_text(case.get(f"{field}_as_sent"))
        if as_sent is None:
            continue
        lines.append(
            note_line_html(
                label=f"{field.capitalize()} as sent:",
                value=f"{as_sent} — corrected by {corrected_by}",
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
