"""Differential check: each urwotm page against the source it was ported from.

The four-part series "Undoing and redoing the work of the Masoretes" was
ported from published Google Docs into ``py/author_misc/urwotm_[1-4]_*.py``
on 2026-07-27.  This is what keeps the port honest: every word of the source
document, against every word of the page MAM-with-doc now generates.  It is
a differential check against an independent oracle -- the first of the two
test shapes ``doc/agent-planning-principles.md`` sanctions -- and it found
four real defects while the port was being made.

THE ORACLE IS FROZEN, AND THAT IS THE POINT.  ``py/urwotm_check/src/urwotm_N.gdoc.txt``
holds the words of the published document as of the pinned 2026-07-26
snapshot, one word per line.  It is a tracked file rather than a re-fetch
because a re-fetch would let an upstream edit to a Google Doc silently
redefine what the pages are being checked against -- and because the
snapshot it came from lived in ``.novc/``, which ``main_repo_maintenance.py``
step 1 wipes.  A deliberate change to a page is recorded in
``py/urwotm_check/expected_divergences.py``; re-vendoring the source is not
how a difference gets resolved.

NOTHING HERE SKIPS.  The parametrize list is the literal ``PART_NUMS``, so it
can never come out empty (pytest reports an empty parameter set as a SKIP,
and skips are a semantic channel in this suite).  MAM-with-doc is reached
through ``mb_cmn.paths.require_sibling``, so an absent sibling FAILS naming
both env-var overrides rather than quietly reporting green.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_urwotm_difftext.py
"""

import pytest

from urwotm_check import difftext
from urwotm_check import parts


@pytest.mark.parametrize("part", parts.PART_NUMS)
def test_page_says_what_its_source_document_says(part: int) -> None:
    lines = difftext.unexpected_lines(part)
    assert not lines, (
        f"py/author_misc/urwotm_{part}_*.py generates a page that differs from the"
        f" document it was ported from, {parts.pub_url(part)}, in a way"
        " py/urwotm_check/expected_divergences.py does not allow.  Fix the page (or"
        " record the difference there, if it is deliberate) -- do NOT re-vendor"
        f" {parts.src_path(part).name}:\n\n" + "\n".join(lines)
    )
