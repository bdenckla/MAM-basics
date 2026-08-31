"""Lint: the landing page's own links, and the ten titles it copies from other pages.

WHY THIS EARNS ITS PLACE.  ``doc/agent-planning-principles.md`` allows two test shapes, and
this is the second: a mechanical lint over the tree, both sides derived from tracked source,
with no hand-picked example pinned anywhere.  It is also the check the history asked for.
``gh-pages/index.html`` took over from ``document-index/README.md``, whose 41 commits
include three that are pure link repair AFTER a page moved -- ``4d756b0`` "Update WLC links
to new GitHub Pages URLs", ``aca96fd`` "Point the URWOTM series at the generated pages",
``8f9a353`` "Repoint the four wlc-utils links at MAM-basics/wlc".  Each of those broke
silently first and was noticed later, because the index lived in a different repository from
the pages it named.  Now that the index is here, half of it can be checked.

WHAT IS CHECKED, AND WHAT DELIBERATELY IS NOT.  Only the links that point back into THIS
repo's ``gh-pages/``.  The rest of the index names MAM-with-doc, book-of-job, phonetic-hbo,
Taamey_D, two gists' worth of former reviews, Google Docs and hakirah.org, and checking
those would need either the network or a sibling clone.  A sibling clone is the harder
objection: under this repo's missing-input rule a test may not skip when its input is
absent, so a sibling-aware check would have to FAIL on any machine without the clone.  So
this file checks the half whose both sides are in this repo -- the same reasoning
``py/tests/test_wlc_redirect_manifest.py``'s docstring gives for hoisting one check out of a
program that cannot run here.

THE DERIVED HALF NEEDS NO LINT, AND ITS ABSENCE HERE IS NOT AN OVERSIGHT.  The manifest
section's own links -- ``<subtree>/index.html`` -- are built by
``author_site/published_subtrees.py`` from the set of tracked ``gh-pages/<name>/index.html``
files, so a manifest link names a tracked page BY CONSTRUCTION and cannot go stale the way
an authored one can.  What this file checks is the authored half, which is the half a human
types.

TRACKED, NOT MERELY PRESENT.  ``.github/workflows/pages.yml`` deploys what is committed, so
a link to a generated-but-untracked page would 404 for every reader while resolving fine on
the machine that generated it.  ``git ls-files`` is therefore the right oracle, and it is the
one ``author_site/published_subtrees.py`` uses to build the manifest.

A GREEN RUN THAT VERIFIED NOTHING IS A FAILURE.  Both tests assert their input is the size it
should be before asserting anything about it.
"""

from __future__ import annotations

from pathlib import Path
import re
import subprocess

from mb_cmn import paths
from author_site import published_subtrees
from author_site import site_data
from author_site.entries import Anchor, anchors_in

_SITE_URL = "https://bdenckla.github.io/MAM-basics/"
_PAGES_PREFIX = "gh-pages/"
_MISC_MODULE_DIR = "py/author_misc"
_TITLE_RE = re.compile(r'^_TITLE = "(.*)"$', re.M)

# document-index carried 25 links and this page carries more; if the walk ever returns a
# handful, it is walking the wrong thing.
_MIN_AUTHORED_ANCHORS = 30


def _tracked_pages(repo_root: Path) -> set[str]:
    """Every file tracked under ``gh-pages/``, as its path below that prefix."""
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", _PAGES_PREFIX],
        cwd=repo_root,
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    return {entry[len(_PAGES_PREFIX) :] for entry in result.stdout.split("\0") if entry}


def _authored_anchors() -> list[Anchor]:
    """Every link the landing page's authored data holds, the manifest's included."""
    sections = [*site_data.BY_ME, *site_data.NOT_BY_ME]
    subtrees = published_subtrees.published_subtrees(paths.repo_root())
    return [*anchors_in(sections), *anchors_in(subtrees)]


def _in_site_target(href: str) -> str | None:
    """The ``gh-pages/``-relative path an href names, or None if it leaves this site."""
    if href.startswith(_SITE_URL):
        target = href[len(_SITE_URL) :]
    elif "://" in href or href.startswith("#"):
        return None
    else:
        target = href
    return f"{target}index.html" if target.endswith("/") else target


def test_every_in_site_link_names_a_tracked_page():
    """A link into this site's own gh-pages must name a file that is published."""
    anchors = _authored_anchors()
    assert len(anchors) >= _MIN_AUTHORED_ANCHORS, len(anchors)
    tracked = _tracked_pages(paths.repo_root())
    assert tracked, "no files tracked under gh-pages/: wrong repo root?"
    targets = {
        anchor.href: _in_site_target(anchor.href)
        for anchor in anchors
        if _in_site_target(anchor.href) is not None
    }
    assert (
        targets
    ), "no link points into this site's own gh-pages: the walk found nothing"
    missing = sorted(
        f"{href} -> {_PAGES_PREFIX}{target}"
        for href, target in targets.items()
        if target not in tracked
    )
    assert not missing, (
        "the landing page links page(s) this repo does not publish, so the published"
        f" index would 404 on them: {missing}. Either the page moved and the entry in"
        " py/author_site/site_data.py wants repointing, or the page was dropped and the"
        " entry with it."
    )


def test_the_misc_titles_are_the_pages_own_titles():
    """Each Misc entry's link text is still the _TITLE of the module that renders it."""
    modules = site_data.MISC_SOURCE_MODULES
    assert len(modules) == 10, modules
    misc = next(one for one in site_data.BY_ME if one.heading == "Misc")
    assert len(misc.entries) == len(modules)
    drifted = []
    for entry, module in zip(misc.entries, modules):
        source = (paths.repo_root() / _MISC_MODULE_DIR / f"{module}.py").read_text(
            encoding="utf-8"
        )
        match = _TITLE_RE.search(source)
        assert match, f"{module}.py has no _TITLE line for this lint to compare against"
        if match.group(1) != entry.anchor.text:
            drifted.append((module, match.group(1), entry.anchor.text))
    assert not drifted, (
        "Misc entries whose link text no longer matches the title of the page they name:"
        f" {drifted}. Copy the module's _TITLE rather than editing it here -- these"
        " titles carry Hebrew, a precomposed U+1E24 and curly apostrophes."
    )
