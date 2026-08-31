"""Guard: every URL ``in/wlc_redirect_pages.json`` freezes is still published here.

WHY THIS IS A TEST AND THE REST OF THE LINT IS NOT

``py/main_wlc_redirect_stubs.py check`` lints the stub tree wlc-utils publishes, and it
cannot run here: that tree is another repository's, and no machine is expected to hold a
clone of it (2026-08-22).  One of its four checks needs no stub tree at all, because both
sides of it are in this repo -- the frozen list of old URLs, and the pages under
``gh-pages/wlc/`` those URLs redirect to.  That check is the one hoisted here, into a
suite that runs all the time, rather than left in a program nothing schedules and nothing
can currently run.

WHAT BREAKS IT, AND WHY THAT MATTERS

A stub sends ``bdenckla.github.io/wlc-utils/<path>`` to
``bdenckla.github.io/MAM-basics/wlc/<path>``, a pure prefix rewrite, so the stub goes on
working only while a page is published at that same path here.  Rename one of the 154
frozen pages, or drop it, and its stub keeps redirecting -- to a URL that 404s.  Nothing
in ``gh-pages/wlc/`` knows the manifest exists, so the break is silent, and it is exactly
the shape ``py/tests/test_vendoring_policy_paths.py`` was written for after a manifest
went stale unnoticed for a day.

The repair is a decision rather than a rewrite, which is why this reports rather than
fixes: republish the page at its old path, or, if the content is genuinely gone, drop the
URL from the manifest and delete its stub in wlc-utils, accepting that an old citation now
lands on the ``404.html`` catch-all.

A MISSING OR EMPTY MANIFEST FAILS, IT DOES NOT SKIP.  ``stubs.redirected_pages`` raises
on an empty list and ``read_text`` raises on an absent file, so neither can report green
having verified nothing.
"""

from __future__ import annotations

from mb_cmn import paths
from wlc_redirect import stubs

_MANIFEST_NAME = "wlc_redirect_pages.json"


def test_every_frozen_url_is_still_published_here() -> None:
    frozen = stubs.redirected_pages(paths.repo_root())
    published = set(stubs.published_pages(paths.repo_root()))
    gone = sorted(page for page in frozen if page not in published)
    assert not gone, (
        f"{len(gone)} URLs frozen in {_MANIFEST_NAME} name a page no longer published"
        " under gh-pages/wlc/, so wlc-utils' stub for each still redirects, to a"
        f" MAM-basics URL that 404s: {gone}."
        " Republish each page at that exact path -- the redirect is a pure prefix"
        " rewrite and can point nowhere else -- or drop the URL from the manifest and"
        " delete its stub in wlc-utils, which leaves the old citation to the 404.html"
        " catch-all."
    )
