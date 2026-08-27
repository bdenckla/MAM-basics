"""Lint: every workspace repo is classified public or private, and the guard holds.

Lint-shaped, per CLAUDE.md's "differential and lint-shaped only": these are
decidable properties of two tracked source files -- all-repos.code-workspace and
in/repo_maintenance_policy.json -- and of one module's behaviour on paths built
from them. Nothing here pins a hand-picked example, and nothing reaches the
network: the visibility of a repo on GitHub is not what is being checked, the
completeness and the consequences of the DECLARATION are.

Why it earns its keep. The declaration is what
py/repo_util/report_destination.py consults to decide whether a report may be
written into this public repo. A repo cloned later and added to the workspace
file, with no entry added here, is the failure this catches: --visibility would
then raise mid-sweep, and, worse, an --visibility-less run would treat the sweep
as covering nothing private and let the guard pass.
"""

from pathlib import Path
import unittest

from mb_cmn import paths
from repo_util import maintenance_policy
from repo_util.common import read_json
from repo_util.report_destination import (
    ReportDestinationError,
    assert_report_destination_ok,
    describe_destination,
)

REPO_ROOT = paths.repo_root()
WORKSPACE_FILE = REPO_ROOT / "all-repos.code-workspace"


def _workspace_repo_names() -> list[str]:
    payload = read_json(WORKSPACE_FILE)
    names = []
    for folder in payload["folders"]:
        raw = folder["path"]
        names.append(REPO_ROOT.name if raw == "." else Path(raw).name)
    return sorted(names)


class TestRepoVisibilityDeclared(unittest.TestCase):
    def test_every_workspace_repo_is_classified(self):
        declared = maintenance_policy.repo_visibility()
        missing = [name for name in _workspace_repo_names() if name not in declared]
        self.assertEqual(
            [],
            missing,
            "all-repos.code-workspace lists repo(s) with no entry in"
            " in/repo_maintenance_policy.json's repo_visibility map. Add one for"
            " each; a missing entry is what lets a private repo's findings reach"
            " this public repo's tree.",
        )

    def test_no_declared_visibility_is_unrecognized(self):
        bad = {
            name: kind
            for name, kind in maintenance_policy.repo_visibility().items()
            if kind not in ("public", "private")
        }
        self.assertEqual({}, bad)

    def test_this_repo_is_declared_public(self):
        # The guard's whole premise. If MAM-basics were ever declared private the
        # refusal would stop firing, silently, for every destination inside it.
        self.assertEqual("public", maintenance_policy.repo_visibility()[REPO_ROOT.name])

    def test_private_repos_are_declared(self):
        self.assertNotEqual([], maintenance_policy.private_repos())


class TestReportDestinationGuard(unittest.TestCase):
    """The guard's decisions on paths built from the declaration, not on fixtures."""

    def setUp(self):
        self.private = maintenance_policy.private_repos()

    def test_tracked_path_in_this_repo_is_public_tracked(self):
        kind = describe_destination(REPO_ROOT / "doc" / "some-report.md", self.private)
        self.assertEqual("public-tracked", kind)

    def test_novc_in_this_repo_is_ignored(self):
        kind = describe_destination(
            REPO_ROOT / ".novc" / "some-report.txt", self.private
        )
        self.assertEqual("ignored", kind)

    def test_private_covered_report_into_this_repo_raises(self):
        with self.assertRaises(ReportDestinationError):
            assert_report_destination_ok(
                REPO_ROOT / "doc" / "some-report.md",
                covered_repo_names=[REPO_ROOT.name, *self.private],
                private_repo_names=self.private,
                option_name="--report-txt",
            )

    def test_public_only_report_into_this_repo_is_allowed(self):
        assert_report_destination_ok(
            REPO_ROOT / "doc" / "some-report.md",
            covered_repo_names=maintenance_policy.public_repos(),
            private_repo_names=self.private,
            option_name="--report-txt",
        )

    def test_private_covered_report_into_novc_is_allowed(self):
        assert_report_destination_ok(
            REPO_ROOT / ".novc" / "some-report.txt",
            covered_repo_names=[*self.private],
            private_repo_names=self.private,
            option_name="--report-txt",
        )

    def test_no_destination_is_allowed(self):
        assert_report_destination_ok(
            None,
            covered_repo_names=[*self.private],
            private_repo_names=self.private,
            option_name="--report-txt",
        )


if __name__ == "__main__":
    unittest.main()
