"""The site's own publication manifest: one entry per subtree published from this repo.

DERIVED, NOT LISTED.  ``doc/PLAN-evacuate-python-programme.md``'s decision of 2026-08-22
requires the subtree list to come from the site rather than from a literal, "the way
``py/main_wlc_redirect_stubs.py`` derives its stub set by filtering ``git ls-files``".
``subtree_ids`` is that derivation, and ``py/wlc_redirect/stubs.py``'s ``published_pages``
is the shape it copies, raise-on-empty guard included: a manifest of nothing is a failure,
not an empty run.

WHAT IS DERIVED AND WHAT IS NOT.  The same decision says "the descriptions cannot be
derived and stay authored", so ``_DESCRIPTIONS`` below is hand-kept, and a subtree with no
entry there raises rather than being emitted bare -- "a gap to fill, not a link to emit
bare".  That is the whole division: the site says WHICH subtrees exist, a human says what
each one is.

TRACKED, NOT PRESENT.  The derivation reads ``git ls-files``, so a subtree reaches the
manifest at the commit that TRACKS its ``index.html``, not at the run that generates it.
That is right rather than incidental: ``.github/workflows/pages.yml`` deploys what is
committed, so an untracked directory is not published and does not belong on a list of
what is published.  Do not "fix" it into a filesystem walk.

WHY ONLY ONE LEVEL DOWN.  A subtree is ``gh-pages/<name>/index.html`` exactly; nothing
deeper and nothing at the deploy root.  ``gh-pages/unicode-proposals.html`` is a loose
page at the root, reached from the index's authored data like any other document, and it
is correctly invisible here.  ``gh-pages/index.html`` is the page this module helps write.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess

from author_site.entries import Anchor, Part

_PAGES_PREFIX = "gh-pages/"
_INDEX_NAME = "index.html"

# Authored, one per subtree, as a run of parts so a description can carry a link.  The
# register to match is the hand-written page this generator replaced, whose single entry
# read "Westminster Leningrad Codex reports and accent-grammar analyses, published here
# from the MAM-basics repository": a noun phrase saying what the subtree holds, not a
# sentence.  The anchor on "MAM-basics" is that page's, reproduced rather than invented.
_DESCRIPTIONS: dict[str, tuple[Part, ...]] = {
    "wlc": (
        "Westminster Leningrad Codex reports and accent-grammar analyses,"
        " published here from the ",
        Anchor("MAM-basics", "https://github.com/bdenckla/MAM-basics"),
        " repository",
    ),
}


@dataclass(frozen=True)
class Subtree:
    """One published subtree: its directory name, its href, and what it holds."""

    subtree_id: str
    description: tuple[Part, ...]

    @property
    def href(self) -> str:
        return f"{self.subtree_id}/{_INDEX_NAME}"


def subtree_ids(repo_root: Path) -> list[str]:
    """Every ``gh-pages/<name>/index.html`` tracked here, as its ``<name>``."""
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", _PAGES_PREFIX],
        cwd=repo_root,
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    ids = sorted(
        {
            parts[0]
            for parts in (
                entry[len(_PAGES_PREFIX) :].split("/")
                for entry in result.stdout.split("\0")
                if entry.endswith(f"/{_INDEX_NAME}")
            )
            if len(parts) == 2
        }
    )
    if not ids:
        raise AssertionError(
            f"no <subtree>/{_INDEX_NAME} tracked under {_PAGES_PREFIX} in {repo_root}:"
            " the site this manifest describes is not where this module looks for it, so"
            " the landing page would be published claiming to publish nothing."
        )
    return ids


def published_subtrees(repo_root: Path) -> list[Subtree]:
    """The manifest: every derived subtree, paired with its authored description."""
    ids = subtree_ids(repo_root)
    undescribed = [one_id for one_id in ids if one_id not in _DESCRIPTIONS]
    if undescribed:
        raise AssertionError(
            f"published subtree(s) with no description in {__name__}: {undescribed}."
            " A subtree with no description is a gap to fill, not a link to emit bare"
            " (doc/PLAN-evacuate-python-programme.md, the 2026-08-22 decision). Add one"
            " sentence to _DESCRIPTIONS saying what the subtree holds."
        )
    return [Subtree(one_id, _DESCRIPTIONS[one_id]) for one_id in ids]
