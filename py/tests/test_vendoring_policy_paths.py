"""Guard: every path ``in/vendoring_policy.json`` configures still resolves on disk.

WHAT WENT WRONG, AND WHY A LINT IS THE RIGHT SHAPE OF ANSWER

Phase 4 of ``doc/PLAN-evacuate-python-from-wlc-utils.md`` deleted wlc-utils' ``py/``
tree on 2026-08-01.  The vendoring policy still named ``wlc-utils`` with a
``pkg_scan_roots`` entry of ``py/mb_cmn``, so from that moment
``py/main_vendoring.py --all`` died with ``ValueError: Configured scan root does not
exist``.  Nothing routine ran that program, so nothing reported it; it was found a day
later by hand, and fixed in ``ea9f199`` by dropping the entry.

The policy is a hand-maintained manifest naming directories in this repo and in nine
sibling repos, and nothing in those repos knows the manifest exists.  Any rename,
move or deletion over there breaks it silently.  That makes "does each configured
path resolve?" a decidable property of the source text -- a mechanical lint over the
tree, the second of the two test shapes CLAUDE.md sanctions -- and both sides are
derived, so adding or removing a repo never needs this file edited.

WHAT IT CHECKS, AND WHY THESE THREE

Exactly the three lookups ``vendoring/discover.py`` raises ``ValueError`` on, hoisted
out of a program run nothing schedules into a suite run all the time:

* ``test_every_source_pkg_dir_exists`` -- ``global.source_pkg_dirs``, against
  ``discover._source_file_names``'s "Missing source package dir".
* ``test_every_non_ignored_dest_repo_is_present`` -- the repo clones, against
  ``discover._scanned_dest_paths``'s "Missing destination repo".
* ``test_every_pkg_scan_root_exists`` -- the ``pkg_scan_roots``, against that same
  function's "Configured scan root does not exist", which is the one that actually
  fired.

An override's ``dest_path`` is deliberately NOT checked here.  A vanished override
target is not a crash: ``vendoring/compare.py`` reports it as ``MISSING-DEST`` in
``out/vendoring_compare_out.txt``, and that report is git-tracked, so it surfaces as a
diff.  Only the three above stop the audit dead, and only those belong in a lint whose
whole job is to say "the manifest no longer describes the disk".

WHY A MISSING SIBLING FAILS HERE RATHER THAN SKIPPING

An absent clone is a misconfiguration, not a reason to check less -- see
``mb_cmn.paths.require_sibling``, whose message names both env-var overrides.  Skips
are a semantic channel in this suite (a skip reports that a page diverges from its
strand), so an environment-shaped skip mixed in corrupts that signal.  The
``or [...]`` fallbacks on the parametrize lists are the mechanism that makes an empty
policy fail too, since pytest reports an empty parameter set as a SKIP.

The drift half of the same gap -- an inventory nobody regenerates -- is not a lint's
business and is handled elsewhere: ``py/main_vendoring.py``'s ``almost_main`` is a step
of ``py/main_0_mega.py``, so a rebuild rewrites the tracked artifacts and stale ones
show up as an unexplained diff.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_vendoring_policy_paths.py
"""

from __future__ import annotations

import pytest

from mb_cmn import paths
from vendoring.discover import destination_repo_path
from vendoring.repo_policy import load_policy

_POLICY_PATH = paths.repo_root() / "in" / "vendoring_policy.json"

# Reading nothing out of the policy is a failure, not a skip.  Each sentinel names a
# directory that cannot exist, so it fails by the same route a genuine breakage does,
# and its text says which list came back empty.
_NOTHING = "(the policy declares none -- discovery here is broken)"


def _source_pkg_dirs() -> list[tuple[str, str]]:
    return sorted(load_policy().source_pkg_dirs.items())


def _dest_repos() -> list[str]:
    return sorted(
        repo_name for repo_name, repo in load_policy().repos.items() if not repo.ignore
    )


def _scan_roots() -> list[tuple[str, str, str]]:
    """Every ``(repo, src_pkg, root)`` triple the discovery scan will visit."""
    return sorted(
        (repo_name, src_pkg, root)
        for repo_name, repo in load_policy().repos.items()
        if not repo.ignore
        for src_pkg, roots in repo.pkg_scan_roots.items()
        for root in roots
    )


_SOURCE_PKG_DIRS = _source_pkg_dirs() or [("source_pkg_dirs", _NOTHING)]
_DEST_REPOS = _dest_repos() or [_NOTHING]
_SCAN_ROOTS = _scan_roots() or [(_NOTHING, "pkg_scan_roots", _NOTHING)]


@pytest.mark.parametrize("src_pkg,rel_dir", _SOURCE_PKG_DIRS)
def test_every_source_pkg_dir_exists(src_pkg: str, rel_dir: str) -> None:
    pkg_dir = paths.repo_root() / rel_dir
    assert pkg_dir.is_dir(), (
        f"{_POLICY_PATH.name}: global.source_pkg_dirs.{src_pkg} names {rel_dir!r},"
        f" but there is no such directory at {pkg_dir}."
        " The vendoring audit reads its source files from there, so"
        " py/main_vendoring.py --all dies on this before it can report anything."
        " Update the policy to the package's new home, or drop the entry if the"
        " package is gone."
    )


@pytest.mark.parametrize("repo_name", _DEST_REPOS)
def test_every_non_ignored_dest_repo_is_present(repo_name: str) -> None:
    repo_path = destination_repo_path(repo_name)
    if repo_name != paths.repo_root().name:
        # require_sibling rather than a bare is_dir() so the failure carries the two
        # overrides that fix a clone living somewhere else.
        repo_path = paths.require_sibling(repo_name, repo_path)
    assert repo_path.is_dir(), f"Missing destination repository: {repo_path}"


@pytest.mark.parametrize("repo_name,src_pkg,root", _SCAN_ROOTS)
def test_every_pkg_scan_root_exists(repo_name: str, src_pkg: str, root: str) -> None:
    repo_path = destination_repo_path(repo_name)
    if repo_name != paths.repo_root().name:
        repo_path = paths.require_sibling(repo_name, repo_path)
    root_path = repo_path / root
    assert root_path.is_dir(), (
        f"{_POLICY_PATH.name}: repos.{repo_name}.pkg_scan_roots.{src_pkg} names"
        f" {root!r}, but there is no such directory at {root_path}."
        " This is the failure that took a day to notice on 2026-08-01, when"
        " wlc-utils' py/ tree was deleted out from under this entry: every"
        " py/main_vendoring.py run raises"
        f' ValueError("Configured scan root does not exist: {root_path}")'
        " until the policy is corrected."
        " Point the entry at the directory's new home, or -- if that repo no longer"
        " holds vendored copies of this package at all -- remove the entry, as"
        " ea9f199 did for wlc-utils."
    )
