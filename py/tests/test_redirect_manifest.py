"""Guard: every frozen redirect URL is still published in MAM-basics.

WHY THIS IS A TEST AND THE REST OF THE LINT IS NOT

``py/main_redirect_stubs.py check`` lints each source repo's stub tree, and it cannot run
here without a clone. One of its four checks needs no stub tree at all, because both sides
are in this repo -- the frozen list of old URLs and the MAM-basics pages those URLs
redirect to. That check is the one hoisted here, into a suite that runs all the time,
rather than left in a program nothing schedules and nothing can currently run.

WHAT BREAKS IT, AND WHY THAT MATTERS

A stub sends an old URL to its MAM-basics subtree at the same relative path, a pure prefix
rewrite. It goes on working only while a page is published at that path here. Rename a
frozen page, or drop it, and its stub keeps redirecting -- to a URL that 404s. Nothing in
the target subtree knows the manifest exists, so the break is silent, and it is exactly
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

import pytest

from mb_cmn import paths
from redirect_stubs import stubs


@pytest.mark.parametrize(
    "repo", stubs.REDIRECT_REPOS, ids=lambda repo: repo.source_repo
)
def test_every_frozen_url_is_still_published_here(repo: stubs.RedirectRepo) -> None:
    frozen = stubs.redirected_pages(paths.repo_root(), repo)
    published = set(stubs.published_pages(paths.repo_root(), repo))
    gone = sorted(page for page in frozen if page not in published)
    assert not gone, (
        f"{len(gone)} URLs frozen in {repo.manifest_path} name a page no longer published"
        f" under {repo.pages_prefix}, so {repo.source_repo}'s stub for each still redirects,"
        f" to a MAM-basics URL that 404s: {gone}."
        " Republish each page at that exact path -- the redirect is a pure prefix"
        " rewrite and can point nowhere else -- or drop the URL from the manifest and"
        f" delete its stub in {repo.source_repo}, which leaves the old citation to the 404.html"
        " catch-all."
    )
