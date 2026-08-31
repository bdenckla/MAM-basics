"""Lint: a generated artifact must not spell out the path of the machine that made it.

WHAT THIS GUARDS.  ``out/`` and ``gh-pages/`` hold git-tracked generated files, and in
this repo the tracked generated artifact IS the test (CLAUDE.md): you regenerate and read
the diff, and an unexplained diff is a failure until explained.  An absolute path baked
into such a file breaks that outright -- the artifact then encodes the author's home
directory, so it can only ever regenerate identically on the author's own machine, and
everywhere else it shows a permanent diff that says nothing about the data.

FOUND 2026-08-31, by the first run of ``main_0_mega.py`` in a cloud sandbox.  Every one of
the 38 steps that ran reproduced its artifacts byte-for-byte except
``out/accgram/research-oddballs.json``, whose 96 oddballs were identical and whose four
recorded input paths read ``C:\\Users\\BenDe\\GitRepos\\...`` against a regenerated
``/home/user/...``.  ``mb_cmn.paths.display_path`` is the fix, and this is the guard that
keeps the next such key from arriving unnoticed.

SCOPE IS THE TWO GENERATED TREES, not the whole repo.  A machine path is perfectly
legitimate in a workspace file, in a ``doc/`` plan recording what someone ran, in
``in/repo_maintenance_policy.json`` as declared configuration, and in a docstring giving
an example command -- twelve tracked files outside ``out/`` and ``gh-pages/`` carry one,
and none of them is a defect.  What makes these two trees different is that a program
rewrites them.
"""

import re
import subprocess
import unittest

from mb_cmn import paths

# One or more separators after the drive letter, because a Windows path inside JSON
# arrives with its backslashes doubled: the bytes on disk read C:\\Users\\BenDe.  A
# pattern written for the display form matches neither the JSON nor, therefore, the
# file that prompted this lint.
_MACHINE_PATH_RE = re.compile(
    r"C:[\\/]+Users[\\/]|/home/[a-z][a-z0-9_-]*/|/Users/[A-Za-z][A-Za-z0-9_-]*/"
)

_SCANNED_DIRS = ("out", "gh-pages")

# A scan that silently matches nothing reports green having checked nothing, which is the
# failure mode CLAUDE.md's testing section is built around.  These two trees held 626
# tracked files when this was written -- 341 under out/, 285 under gh-pages/ -- of which
# 500 survive the binary filter below.  400 leaves room for the trees to shrink without
# tripping this, and is far above anything a broken enumeration would return.
_FILE_FLOOR = 400

_BINARY_SUFFIXES = (
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".pdf",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".zip",
    ".xlsx",
    ".docx",
    ".pptx",
    ".mp3",
    ".midi",
    ".mid",
)

# out/accgram/goerwitz-stderr/_summary.stderr.json records the directory it was written
# to, and records it as C:\Users\BenDe\GitRepos\wlc-utils\... -- a clone whose corpus came
# home on 2026-08-12 and which left this disk on 2026-08-22.  It is excluded rather than
# fixed because NOTHING IN py/ WRITES IT ANY MORE: grepping "goerwitz" finds only page
# assembly and CSS class names, and the file's last commit merely carried it along.  So it
# is a fossil, not drift -- it cannot regenerate wrongly because it cannot regenerate at
# all.  Deleting it, or restoring a generator for it, is a decision for its author; until
# then this lint should not be held hostage to it.
_EXCLUDED = frozenset({"out/accgram/goerwitz-stderr/_summary.stderr.json"})


def _tracked_text_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", *_SCANNED_DIRS],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=paths.repo_root(),
        check=True,
    )
    names = [name for name in result.stdout.split("\0") if name]
    return [
        name
        for name in names
        if not name.lower().endswith(_BINARY_SUFFIXES) and name not in _EXCLUDED
    ]


class TestNoMachinePathsInArtifacts(unittest.TestCase):
    def test_scan_actually_covers_the_generated_trees(self):
        scanned = _tracked_text_files()
        self.assertGreaterEqual(
            len(scanned),
            _FILE_FLOOR,
            f"only {len(scanned)} tracked text files found under {_SCANNED_DIRS};"
            " the enumeration is broken, so the scan below verifies nothing",
        )

    def test_no_generated_artifact_records_a_machine_path(self):
        offenders = []
        for name in _tracked_text_files():
            path = paths.repo_root() / name
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            match = _MACHINE_PATH_RE.search(text)
            if match is not None:
                offenders.append(f"{name}: {match.group(0)}")
        self.assertEqual(
            offenders,
            [],
            "generated artifacts must record repo-qualified paths, not machine paths."
            " Use mb_cmn.paths.display_path at the point the value is written."
            f" Offenders: {offenders}",
        )


if __name__ == "__main__":
    unittest.main()
