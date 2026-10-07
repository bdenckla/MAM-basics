"""The record of approved corrections to the Phonetic MAM display.

``in/phonetic_mam_display_corrections.json`` lists each chapter page whose display
Ben approved correcting while its MAM-parsed input was unchanged, with the approval
and the reason (the 2026-10-04 review's item 4.7). Until Ben retired the legacy
projection comparison on 2026-10-07, a listed chapter left that comparison and its
rendered diff was reviewed instead; the list now records his approvals. The
record's ``marker_labels`` are the approved corrections of a layout marker's label,
which the export applies: each names a verse's layout element, counted from 0, the
label the adapter gives it and the label MAM-parsed has. No code writes the record.
"""

import json

from mb_cmn import bib_locales, paths
from phonetic_mam.display_schema import LAYOUT_MARKERS, require

SCHEMA = "phonetic-mam-display-corrections-v1"
_MARKER_LABEL_FIELDS = {"book", "chapter", "verse", "marker", "from", "to"}


def chapter_page(book, chapter):
    """A chapter page's path in the site, as the record's chapters key it."""
    return f"tnkh/{bib_locales.ordered_short_dash_full_39(book)}/{chapter:02d}.html"


def read():
    """Read and validate the tracked record."""
    path = paths.in_dir() / "phonetic_mam_display_corrections.json"
    return validate(json.loads(path.read_text(encoding="utf-8")))


def validate(record):
    """Return the record after checking its closed shape."""
    require(
        isinstance(record, dict)
        and set(record) == {"schema", "chapters", "marker_labels"},
        "unknown display-corrections fields",
    )
    require(record["schema"] == SCHEMA, "unknown display-corrections record")
    chapters = record["chapters"]
    require(isinstance(chapters, dict), "corrected chapters must be an object")
    for page, approval in chapters.items():
        require(
            page.startswith("tnkh/") and page.endswith(".html"),
            f"unknown corrected chapter page: {page!r}",
        )
        require(
            isinstance(approval, str) and bool(approval.strip()),
            f"{page}: missing approval",
        )
    entries = record["marker_labels"]
    require(isinstance(entries, list), "marker-label corrections must be a list")
    seen = set()
    for entry in entries:
        require(
            isinstance(entry, dict) and set(entry) == _MARKER_LABEL_FIELDS,
            "unknown marker-label correction fields",
        )
        require(entry["book"] in bib_locales.ALL_BK39_IDS, "unknown corrected book")
        for key in ("chapter", "verse"):
            require(
                type(entry[key]) is int and entry[key] > 0,
                f"marker-label correction: bad {key}",
            )
        require(
            type(entry["marker"]) is int and entry["marker"] >= 0,
            "marker-label correction: bad marker index",
        )
        require(
            entry["from"] in LAYOUT_MARKERS
            and entry["to"] in LAYOUT_MARKERS
            and entry["from"] != entry["to"],
            "marker-label correction: bad labels",
        )
        page = chapter_page(entry["book"], entry["chapter"])
        require(
            page in chapters, f"{page}: a marker-label correction's chapter is unlisted"
        )
        identity = (entry["book"], entry["chapter"], entry["verse"], entry["marker"])
        require(identity not in seen, f"duplicate marker-label correction: {identity}")
        seen.add(identity)
    return record
