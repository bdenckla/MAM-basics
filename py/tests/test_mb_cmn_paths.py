"""Tests for the sibling-repo path resolver in ``mb_cmn.paths``.

These exercise the resolution precedence and env-var name mapping without requiring any
real sibling directory to exist on disk.

BLESSED EXAMPLE-BASED BAND.  This repo's testing rule admits only differential and
lint-shaped tests, and the ``require_sibling`` failure-message tests below are neither:
they pin a hand-picked absent path and read the words of the exception it raises.  Kept,
because that message IS the mechanism the whole no-skip policy rests on -- a cross-repo
check with a missing sibling has to FAIL, and fail naming both overrides and the root it
searched.  Nothing else in either tree checks that it does, and the only identifiers
pinned are the env-var names, which are the contract rather than an implementation detail.

Ported from wlc-utils' ``py/tests/test_repo_paths.py`` when the override chain moved here
(2026-08-01), which is what makes it the oracle that the chain arrived intact rather than
in name only.  The env prefix changed with it: ``WLC_SIBLINGS_ROOT``/``WLC_<NAME>_DIR``
became the repo-agnostic ``REPOS_ROOT``/``REPO_<NAME>_DIR``, because a module six repos
vendor should not advertise a seventh repo's name.
"""

import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

from mb_cmn import paths

# Every variable the tests below set or clear.  Each test runs inside a patched copy of
# os.environ built by _clean_env, so nothing leaks between tests and nothing depends on
# what happens to be exported in the shell that started the run.
_ENV_VARS = (
    "REPOS_ROOT",
    "REPO_MAM_PARSED_DIR",
    "REPO_MAM_SIMPLE_DIR",
    "REPO_CODEX_INDEX_DIR",
    "REPO_CODEX_INDEX_ALEPPO_DIR",
    "REPO_MAM_PRIVATE_DIR",
)


def _clean_env(**overrides: str) -> dict:
    env = {k: v for k, v in os.environ.items() if k not in _ENV_VARS}
    env.update(overrides)
    return env


class TestMbCmnPaths(unittest.TestCase):
    def test_repo_root_is_module_anchored(self):
        # py/mb_cmn/paths.py -> mb_cmn -> py -> repo root; the repo root contains py/.
        self.assertTrue((paths.repo_root() / "py" / "mb_cmn" / "paths.py").is_file())

    def test_default_repos_root_is_repo_parent(self):
        with mock.patch.dict(os.environ, _clean_env(), clear=True):
            self.assertEqual(paths.repos_root(), paths.repo_root().parent)

    def test_default_sibling_is_repo_parent(self):
        with mock.patch.dict(os.environ, _clean_env(), clear=True):
            self.assertEqual(
                paths.sibling_repo("MAM-parsed"),
                paths.repo_root().parent / "MAM-parsed",
            )

    def test_repos_root_env_honored(self):
        with mock.patch.dict(
            os.environ, _clean_env(REPOS_ROOT="/some/base"), clear=True
        ):
            self.assertEqual(paths.repos_root(), Path("/some/base"))
            self.assertEqual(
                paths.sibling_repo("MAM-parsed"), Path("/some/base") / "MAM-parsed"
            )

    def test_per_repo_override_wins_over_repos_root(self):
        env = _clean_env(REPOS_ROOT="/some/base", REPO_MAM_PARSED_DIR="/elsewhere/mp")
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(paths.sibling_repo("MAM-parsed"), Path("/elsewhere/mp"))

    def test_per_repo_override_wins_over_default(self):
        env = _clean_env(REPO_MAM_PARSED_DIR="/elsewhere/mp")
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(paths.sibling_repo("MAM-parsed"), Path("/elsewhere/mp"))

    def test_env_name_mapping_non_alnum_to_underscore(self):
        # codex-index-aleppo -> REPO_CODEX_INDEX_ALEPPO_DIR: each run of
        # non-alphanumerics collapses to one underscore.
        env = _clean_env(REPO_CODEX_INDEX_ALEPPO_DIR="/aleppo")
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(paths.sibling_repo("codex-index-aleppo"), Path("/aleppo"))

    def test_env_name_mapping_is_a_prefix_of_no_other(self):
        # codex-index and codex-index-aleppo are distinct variables, not one shadowing
        # the other -- the case a naive prefix lookup would get wrong.
        env = _clean_env(
            REPO_CODEX_INDEX_DIR="/index", REPO_CODEX_INDEX_ALEPPO_DIR="/aleppo"
        )
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(paths.sibling_repo("codex-index"), Path("/index"))
            self.assertEqual(paths.sibling_repo("codex-index-aleppo"), Path("/aleppo"))

    def test_env_name_mapping_of_the_repo_that_now_holds_the_private_tree(self):
        # The live override for the private al-hatorah tree.
        env = _clean_env(REPO_MAM_PRIVATE_DIR="/mp")
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(paths.sibling_repo("MAM-private"), Path("/mp"))

    def test_default_matches_legacy_repo_root_parent_formula(self):
        # Byte-identical to the old `repo_root().parent / "MAM-parsed"`, which is what
        # makes adding the override chain a no-op for every unconfigured caller.
        with mock.patch.dict(os.environ, _clean_env(), clear=True):
            legacy = paths.repo_root().parent / "MAM-parsed"
            self.assertEqual(paths.sibling_repo("MAM-parsed"), legacy)

    def test_require_sibling_returns_a_present_directory(self):
        # Any directory that certainly exists; the check is is_dir, not the name.
        root = paths.repo_root()
        self.assertEqual(paths.require_sibling("MAM-parsed", root / "py"), root / "py")

    def test_require_sibling_failure_advertises_both_overrides(self):
        """The message IS the feature: a missing sibling is a misconfiguration, and the fix
        has to travel with the failure.  A cross-repo check that skipped here would report
        green having verified nothing, so this path must raise -- and raise something
        actionable."""
        with TemporaryDirectory() as tmp:
            missing = Path(tmp) / "MAM-parsed" / "plus"
            with mock.patch.dict(os.environ, _clean_env(), clear=True):
                with self.assertRaises(FileNotFoundError) as ctx:
                    paths.require_sibling("MAM-parsed", missing)
                message = str(ctx.exception)
                repos_root = str(paths.repos_root())
            self.assertIn(str(missing), message)  # the path actually looked for
            self.assertIn("REPO_MAM_PARSED_DIR", message)  # per-repo, correctly derived
            self.assertIn("REPOS_ROOT", message)  # the all-siblings override
            # The clone-here advice names the siblings root the lookup searches -- not
            # repo_root(), which in a worktree checkout is exactly the wrong "beside".
            self.assertIn(repos_root, message)

    def test_require_sibling_reports_the_overridden_path_not_the_default(self):
        """The accessor checks what it resolves, overrides included -- so pointing the env
        var at a wrong path fails naming that path, not the default one."""
        with TemporaryDirectory() as tmp:
            nowhere = Path(tmp) / "nowhere"
            env = _clean_env(REPO_MAM_PARSED_DIR=str(nowhere))
            with mock.patch.dict(os.environ, env, clear=True):
                resolved = paths.sibling_repo("MAM-parsed")
                self.assertEqual(resolved, nowhere)
                with self.assertRaises(FileNotFoundError) as ctx:
                    paths.require_sibling("MAM-parsed", resolved)
            self.assertIn("nowhere", str(ctx.exception))

    def test_repos_root_override_fixes_the_worktree_case(self):
        """The whole point of the chain, stated as the case that motivated it.

        In a git worktree ``repo_root()`` is ``.../.claude/worktrees/<name>``, so the
        default ``repo_root().parent`` is the worktrees directory and every sibling lookup
        resolves under it -- to paths that have never existed.  ``REPOS_ROOT`` is what
        makes such a checkout able to find the real clones.
        """
        with TemporaryDirectory() as tmp:
            real_clones = Path(tmp) / "GitRepos"
            (real_clones / "MAM-parsed").mkdir(parents=True)
            env = _clean_env(REPOS_ROOT=str(real_clones))
            with mock.patch.dict(os.environ, env, clear=True):
                resolved = paths.sibling_repo("MAM-parsed")
                self.assertEqual(resolved, real_clones / "MAM-parsed")
                # And it passes the check rather than merely resolving plausibly.
                self.assertEqual(
                    paths.require_sibling("MAM-parsed", resolved), resolved
                )


if __name__ == "__main__":
    unittest.main()
