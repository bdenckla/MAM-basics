"""Lint: the landing page's own links, and the titles it copies from other pages.

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

THERE IS NO DERIVED HALF ANY MORE, and the lint got wider when it went.  A last section
headed "Pages published from this repository" used to be built by an
``author_site/published_subtrees.py`` from the set of tracked ``gh-pages/<name>/index.html``
files, so its links named a tracked page BY CONSTRUCTION and this file deliberately let them
be.  Ben deleted that section on 2026-08-31 and asked for the pages it reached to be
distributed to the authored sections instead, so the four that moved into ``site_data``'s
``_WLC`` and ``_MISC`` became typed links, checked here like every other typed link.  Three
of those four left the page again with that day's Misc trim, which cut every Misc entry
another listed document reaches; ``almost-errors`` is the one that stayed.

TRACKED, NOT MERELY PRESENT.  ``.github/workflows/pages.yml`` deploys what is committed, so
a link to a generated-but-untracked page would 404 for every reader while resolving fine on
the machine that generated it.  ``git ls-files`` is therefore the right oracle.

A GREEN RUN THAT VERIFIED NOTHING IS A FAILURE.  Both tests assert their input is the size it
should be before asserting anything about it.
"""

from __future__ import annotations

from pathlib import Path
import re
import subprocess

from mb_cmn import paths
from author_site import site_data
from author_site.entries import Anchor, anchors_in

_SITE_URL = "https://bdenckla.github.io/MAM-basics/"
_PAGES_PREFIX = "gh-pages/"
_MISC_MODULE_DIR = "py/author_misc"
_TITLE_RE = re.compile(r'^_TITLE = "(.*)"$', re.M)

# document-index carried 25 links and this page carries 28 after the 2026-08-31 Misc trim;
# if the walk ever returns a handful, it is walking the wrong thing.  Do not raise this to
# the exact count: it is a floor guarding against a broken walk, not an inventory.
_MIN_AUTHORED_ANCHORS = 25


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
    """Every link the landing page's authored data holds."""
    return anchors_in([*site_data.BY_ME, *site_data.NOT_BY_ME])


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
    assert len(modules) == 2, modules
    # Every Misc entry is a MAM-with-doc page since the 2026-08-31 trim, so the filtered
    # half is the whole section today.  Pair with the filtered half anyway: Misc has twice
    # held an entry naming a page published from this repo, whose link text copies no
    # module's _TITLE, and zipping the whole section against the modules would then compare
    # such an entry to a MAM-with-doc module and report drift that is the pairing's fault.
    entries = site_data.MISC_MWD_ENTRIES
    assert len(entries) == len(modules)
    misc = next(one for one in site_data.BY_ME if one.heading == "Misc")
    assert set(entries) <= set(misc.entries), "MISC_MWD_ENTRIES left the Misc section"
    drifted = []
    for entry, module in zip(entries, modules):
        source = (paths.repo_root() / _MISC_MODULE_DIR / f"{module}.py").read_text(
            encoding="utf-8"
        )
        match = _TITLE_RE.search(source)
        assert match, f"{module}.py has no _TITLE line for this lint to compare against"
        if match.group(1) != entry.anchor.text:
            drifted.append((module, match.group(1), entry.anchor.text))
    assert not drifted, (
        "Misc entries whose link text no longer matches the title of the page they name:"
        f" {drifted}. Copy the module's _TITLE rather than editing it here, and copy it"
        " rather than retyping it: a py/author_misc/ title can carry Hebrew, a precomposed"
        " U+1E24 or a curly apostrophe."
    )
