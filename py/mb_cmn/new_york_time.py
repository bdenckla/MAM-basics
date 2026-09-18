"""Generated clock dates and timestamps shown on pages use New York time and say so.

Ben's decision, 2026-09-14: a date or timestamp that repository code generates from a clock for
display on a page or report is the date or time in New York (``America/New_York``) and is followed
by the label “, New York time”. Historical decision dates, citations, quotations, release or
revision dates, and date-like names—including release names, change ids and dated filenames—take
no label. A timestamp stored in data keeps its full ISO 8601 form with its offset.

WHY NEW YORK RATHER THAN UTC. The seven dates stored in
``MAM-parsed/historical/manifest.json`` are New York dates: each equals the New York date of
GitHub's UTC committer time for its commit, checked on 2026-09-14. In UTC, commit 1880cbbd,
the boundary of the release named 2026-03-16, committed at 20:09 EDT that day, would read
2026-03-17.

On Windows ``zoneinfo`` has no zone data of its own, so ``requirements.txt`` names the
``tzdata`` package.
"""

import datetime
import zoneinfo

NEW_YORK = zoneinfo.ZoneInfo("America/New_York")
LABEL = "New York time"


def new_york_date(moment: datetime.datetime) -> datetime.date:
    """Return the New York date of a moment that states its own offset."""
    if moment.utcoffset() is None:
        raise ValueError(f"{moment!r} states no time zone")
    return moment.astimezone(NEW_YORK).date()


def labelled(date_text: str) -> str:
    """Return a displayed date followed by the name of its zone."""
    return f"{date_text}, {LABEL}"
