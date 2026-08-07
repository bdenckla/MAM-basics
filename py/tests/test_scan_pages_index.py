"""Lint the tracked scan-pages indexes. See doc/scan-pages.md.

This is the mechanical-lint shape the repo's test rules allow: a decidable property of
tracked data, checked against an independent derivation of the same fact, with no
hand-picked example pinned anywhere.  It needs no scans folder -- the indexes are
self-contained -- but it does need MAM-parsed, and it FAILS rather than skips without
it, per the repo's missing-input rule.
"""

from scan_pages import check
from scan_pages import editions
from scan_pages import index_io


def test_tracked_indexes_pass_every_lint():
    """Every check in scan_pages.check, over all five tracked indexes."""
    counts = check.check_all()
    # Guard against a green run that verified nothing: the five indexes exist and hold
    # thousands of pages, so a run reporting a handful means the data went missing.
    assert counts["editions"] == len(editions.ALL_EDITION_IDS)
    assert counts["pages"] > 5000, counts


def test_every_edition_has_a_tracked_index():
    """A new edition must arrive with its index, not merely with its folder name."""
    for edition_id in editions.ALL_EDITION_IDS:
        index = index_io.read_index(edition_id)
        assert index["edition"] == edition_id
        assert index["pages"], edition_id
