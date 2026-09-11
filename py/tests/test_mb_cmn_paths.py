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
import subprocess
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
    "REPO_WLC_UTILS_DIR",
    "REPO_WLC_UTILS_PRIVATE_DIR",
    "REPO_MAM_PRIVATE_DIR",
)


def _clean_env(**overrides: str) -> dict:
    env = {k: v for k, v in os.environ.items() if k not in _ENV_VARS}
    env.update(overrides)
    return env


def _home_clone_by_git() -> Path:
    """This checkout's home clone, as git itself reports it: the independent oracle.

    ``git rev-parse --git-common-dir`` names the main clone's ``.git`` in a linked
    worktree and ``.git`` itself in an ordinary clone, so its parent is the home clone in
    both.  ``mb_cmn.provenance`` reads the same fact out of git's files without running
    git, which is what makes the tests below a comparison rather than a restatement.
    """
    out = subprocess.run(
        ["git", "-C", str(paths.repo_root()), "rev-parse", "--git-common-dir"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    ).stdout.strip()
    common = Path(out)
    if not common.is_absolute():
        common = paths.repo_root() / common
    return common.resolve().parent


class TestMbCmnPaths(unittest.TestCase):
    def test_repo_root_is_module_anchored(self):
        # py/mb_cmn/paths.py -> mb_cmn -> py -> repo root; the repo root contains py/.
        self.assertTrue((paths.repo_root() / "py" / "mb_cmn" / "paths.py").is_file())

    def test_default_repos_root_is_the_home_clones_parent(self):
        # Ben's decision, 2026-09-10: a worktree finds its siblings beside its home clone
        # with nothing exported.  In an ordinary clone the home clone is the checkout
        # itself, so there this is the historical repo_root().parent.
        with mock.patch.dict(os.environ, _clean_env(), clear=True):
            self.assertEqual(paths.repos_root(), _home_clone_by_git().parent)

    def test_default_sibling_is_beside_the_home_clone(self):
        with mock.patch.dict(os.environ, _clean_env(), clear=True):
            self.assertEqual(
                paths.sibling_repo("MAM-parsed"),
                _home_clone_by_git().parent / "MAM-parsed",
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

    # The two tests below keep "wlc-utils-private" only as inert input to the
    # env-var name mapper.  They perform no directory lookup or filesystem access;
    # live WLC generation no longer uses this private-repo name.
    def test_env_name_mapping_non_alnum_to_underscore(self):
        # wlc-utils-private -> REPO_WLC_UTILS_PRIVATE_DIR: each run of
        # non-alphanumerics collapses to one underscore.
        env = _clean_env(REPO_WLC_UTILS_PRIVATE_DIR="/priv")
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(paths.sibling_repo("wlc-utils-private"), Path("/priv"))

    def test_env_name_mapping_is_a_prefix_of_no_other(self):
        # wlc-utils and wlc-utils-private are distinct variables, not one shadowing
        # the other -- the case a naive prefix lookup would get wrong.
        env = _clean_env(REPO_WLC_UTILS_DIR="/pub", REPO_WLC_UTILS_PRIVATE_DIR="/priv")
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(paths.sibling_repo("wlc-utils"), Path("/pub"))
            self.assertEqual(paths.sibling_repo("wlc-utils-private"), Path("/priv"))

    def test_env_name_mapping_of_the_repo_that_now_holds_the_private_tree(self):
        # The live override for the private al-hatorah tree.
        env = _clean_env(REPO_MAM_PRIVATE_DIR="/mp")
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(paths.sibling_repo("MAM-private"), Path("/mp"))

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

    def test_repos_root_override_wins_over_the_home_clone_default(self):
        """``REPOS_ROOT`` still wins over the default, whatever the checkout.

        Until 2026-09-10 this was the only way a worktree found its siblings: the default
        was ``repo_root().parent``, which in a worktree is the worktrees directory, where no
        sibling has ever been.  The default now looks beside the worktree's home clone
        (``test_default_repos_root_is_the_home_clones_parent``), so the variable is for a
        layout where the siblings sit somewhere else entirely.
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
