"""Mechanical lints for the topical landing-page model.

Every anchor reachable from ``site_data.SECTIONS`` is walked, including linked headings
and entries nested in a group.  Links into this repository must name tracked files.  In
the reverse direction, each HTML page at the deployment root must be named by the index or
listed explicitly as an intentional indirect destination.

External destinations are not fetched: doing so would turn a deterministic repository
lint into a network and sibling-repository check.  The title-copy lint separately compares
the three translated Introduction-to-MAM entries with the source modules that render them.
Each check asserts a minimum input size so a broken walk cannot report green.
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

# The landing page carries well over 25 links; if the walk ever returns a handful, it is
# walking the wrong thing.  Do not raise this to
# the exact count: it is a floor guarding against a broken walk, not an inventory.
_MIN_LANDING_PAGE_ANCHORS = 25

# The deploy root held index.html and unicode-proposals.html when this floor was set on
# 2026-09-03. Two remains the floor: the index itself, and at least one page it names. Like the anchor floor
# above it guards against a broken walk rather than inventorying the root.
_MIN_DEPLOY_ROOT_PAGES = 2

# Deploy-root pages that no authored entry names, each with the reason it does not.
_UNLISTED_DEPLOY_ROOT_PAGES = (
    # The index itself.  An entry for it would be the page linking to itself.
    "index.html",
    # These eight child pages are reachable from post-stress-meteg pages, not the index.
    "post-stress-meteg-2chr-8-11.html",
    "post-stress-meteg-cases.html",
    "post-stress-meteg-lacks-mas.html",
    "post-stress-meteg-methods.html",
    "post-stress-meteg-misc.html",
    "post-stress-meteg-next-conjunctive.html",
    "post-stress-meteg-not-fit.html",
    "post-stress-meteg-post-silluq.html",
    # The post-silluq case pages sit a level further down: the case register of
    # post-stress-meteg-post-silluq.html links each one, and the index does not.  Their
    # names come from the dict that generates the pages, so a case page added there needs
    # no entry here.
    *(
        fname
        for fname, _ref in site_data.POST_STRESS_METEG_POST_SILLUQ_IMAGE_PAGES.values()
    ),
)


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


def _landing_page_anchors() -> list[Anchor]:
    """Every link the landing page's ordered section data holds."""
    return anchors_in(site_data.SECTIONS)


def _in_site_target(href: str) -> str | None:
    """The ``gh-pages/``-relative path an href names, or None if it leaves this site."""
    if href.startswith(_SITE_URL):
        target = href[len(_SITE_URL) :]
    elif "://" in href or href.startswith("#"):
        return None
    else:
        target = href
    return f"{target}index.html" if target.endswith("/") else target


def _deploy_root_pages(tracked: set[str]) -> set[str]:
    """The tracked pages at the top of ``gh-pages/``: an HTML file with no directory."""
    return {name for name in tracked if name.endswith(".html") and "/" not in name}


def _in_site_targets() -> set[str]:
    """Every ``gh-pages/``-relative path the landing page's authored data names."""
    return {
        _in_site_target(anchor.href)
        for anchor in _landing_page_anchors()
        if _in_site_target(anchor.href) is not None
    }


def test_every_in_site_link_names_a_tracked_page():
    """A link into this site's gh-pages must name a file that is published."""
    anchors = _landing_page_anchors()
    assert len(anchors) >= _MIN_LANDING_PAGE_ANCHORS, len(anchors)
    tracked = _tracked_pages(paths.repo_root())
    assert tracked, "no files tracked under gh-pages/: wrong repo root?"
    targets = {
        anchor.href: _in_site_target(anchor.href)
        for anchor in anchors
        if _in_site_target(anchor.href) is not None
    }
    assert targets, "no link points into this site's gh-pages: the walk found nothing"
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


def test_every_deploy_root_page_is_named_by_an_entry_or_excluded_by_name():
    """A page published at the deploy root must be reachable from the index."""
    tracked = _tracked_pages(paths.repo_root())
    assert tracked, "no files tracked under gh-pages/: wrong repo root?"
    pages = _deploy_root_pages(tracked)
    assert len(pages) >= _MIN_DEPLOY_ROOT_PAGES, (
        "fewer deploy-root pages than gh-pages/ has ever held, so the walk is walking"
        f" the wrong thing: {sorted(pages)}"
    )
    excluded = set(_UNLISTED_DEPLOY_ROOT_PAGES)
    stale = sorted(excluded - pages)
    assert not stale, (
        "_UNLISTED_DEPLOY_ROOT_PAGES names page(s) this repo no longer publishes at the"
        f" deploy root: {stale}. Drop the entry, or repoint it at the page's new name;"
        " a register nothing prunes stops saying anything."
    )
    unreachable = sorted(pages - _in_site_targets() - excluded)
    assert not unreachable, (
        "page(s) published at the deploy root that no authored entry names, so a reader"
        f" of the index cannot reach them: {unreachable}. Either add an entry in"
        " py/author_site/site_data.py, or, if the page is deliberately unlisted, add it"
        " to _UNLISTED_DEPLOY_ROOT_PAGES above with the reason beside it."
    )


def test_the_translated_introduction_titles_match_the_source_pages():
    """Each translated excerpt still copies the title of the module that renders it."""
    modules = site_data.INTRO_MAM_SOURCE_MODULES
    assert len(modules) == 3, modules
    entries = site_data.INTRO_MAM_MWD_ENTRIES
    assert len(entries) == len(modules)
    excerpts = next(
        one
        for one in site_data.SECTIONS
        if one.heading == "Excerpts from the Introduction to MAM"
    )
    assert set(entries) <= set(
        excerpts.entries
    ), "INTRO_MAM_MWD_ENTRIES left the Introduction-to-MAM excerpts section"
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
        "Introduction-to-MAM entries whose link text no longer matches the title of the"
        " page they name:"
        f" {drifted}. Copy the module's _TITLE rather than editing it here, and copy it"
        " rather than retyping it: a py/author_misc/ title can carry Hebrew, a precomposed"
        " U+1E24 or a curly apostrophe."
    )
