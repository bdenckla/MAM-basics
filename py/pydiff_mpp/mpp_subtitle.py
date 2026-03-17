"""
Render the subtitle table for MPP diff reports.

Exports:
    render_subtitle_table — HTML table with commit hashes, Gregorian dates,
                            and Hebrew dates
"""

import datetime

from pyluach import dates as heb_dates


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


def render_subtitle_table(old_rev, new_rev, old_date, new_date, total):
    """Render the commit/date range as an HTML table."""
    rows = [
        f'<table class="subtitle">',
        "<thead><tr><th>Start</th><th>End</th></tr></thead>",
        "<tbody>",
        f"<tr><td>{_esc(old_rev)}</td><td>{_esc(new_rev)}</td></tr>",
    ]
    if old_date:
        old_heb = _greg_to_heb(old_date)
        new_heb = _greg_to_heb(new_date)
        rows.append(f"<tr><td>{_esc(old_date)}</td><td>{_esc(new_date)}</td></tr>")
        rows.append(
            f'<tr><td dir="rtl">{_esc(old_heb)}</td>'
            f'<td dir="rtl">{_esc(new_heb)}</td></tr>'
        )
    rows.append("</tbody>")
    rows.append("</table>")
    suffix = "change" if total == 1 else "changes"
    rows.append(f'<p class="subtitle">{total} {suffix} found</p>')
    return "\n".join(rows)
