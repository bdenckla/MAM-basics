"""
Render the subtitle table for MAM-parsed-plus diff reports.

Exports:
    render_subtitle_table — HTML table with commit hashes or tree ids, Gregorian
                            dates in New York time, and Hebrew dates
"""

import datetime

from pyluach import dates as heb_dates

from mb_cmn.new_york_time import labelled


def _esc(text):
    """HTML-escape a string."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _greg_to_heb(date_str):
    """Convert a 'YYYY-MM-DD' string to a Hebrew date string."""
    gd = datetime.date.fromisoformat(date_str)
    return heb_dates.HebrewDate.from_pydate(gd).hebrew_date_string()


def _date_cell(date_str):
    """One side's date cell: the date with its zone named, or empty."""
    return _esc(labelled(date_str)) if date_str else ""


def _id_cell(label):
    """One side's first-row cell: a bare commit hash, or a labelled tree id."""
    kind, value = label
    if kind == "tree":
        return f"MAM-parsed/plus tree {value}"
    return value


def _tree_sentence(side, tree_id):
    """Say what one side's tree id is, and how to get from it to commits."""
    return (
        f'<p class="subtitle">The {side} is the git tree id of MAM-parsed/plus,'
        " which is the same in every clone. In a MAM-basics clone with full history,"
        f" <code>git log --full-history --find-object={_esc(tree_id)}"
        " -- MAM-parsed/plus</code> lists the commits that introduced or removed that"
        " tree.</p>"
    )


def render_subtitle_table(old_label, new_label, old_date, new_date, total):
    """Render the revision range as an HTML table.

    Each side is a ``mpplus_revisions.Revision.label`` pair. A tree side -- a MAM-basics
    ref, recorded by the git tree id of MAM-parsed/plus since 2026-09-14 -- has no date,
    so its date cells stay empty, and a sentence under the table says what its id is.
    The date rows appear when either side has a date.
    """
    old_cell = _esc(_id_cell(old_label))
    new_cell = _esc(_id_cell(new_label))
    rows = [
        '<table class="subtitle">',
        "<thead><tr><th>Start</th><th>End</th></tr></thead>",
        "<tbody>",
        f"<tr><td>{old_cell}</td><td>{new_cell}</td></tr>",
    ]
    if old_date or new_date:
        old_heb = _greg_to_heb(old_date) if old_date else ""
        new_heb = _greg_to_heb(new_date) if new_date else ""
        old_date_cell = _date_cell(old_date)
        new_date_cell = _date_cell(new_date)
        rows.append(f"<tr><td>{old_date_cell}</td><td>{new_date_cell}</td></tr>")
        rows.append(
            f'<tr><td dir="rtl">{_esc(old_heb)}</td>'
            f'<td dir="rtl">{_esc(new_heb)}</td></tr>'
        )
    rows.append("</tbody>")
    rows.append("</table>")
    for side, (kind, value) in (("start", old_label), ("end", new_label)):
        if kind == "tree":
            rows.append(_tree_sentence(side, value))
    suffix = "change" if total == 1 else "changes"
    rows.append(f'<p class="subtitle">{total} {suffix} found</p>')
    return "\n".join(rows)
