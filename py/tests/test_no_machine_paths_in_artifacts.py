"""Lint: a generated artifact must not spell out the path of the machine that made it.

WHAT THIS GUARDS.  The paths in ``_SCANNED_PATHS`` hold git-tracked generated files, and in
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

SCOPE IS THE GENERATED TREES, not the whole repo.  A machine path is perfectly
legitimate in a workspace file, in a ``doc/`` plan recording what someone ran, in
``in/repo_maintenance_policy.json`` as declared configuration, and in a docstring giving
an example command. Such paths outside the declared generated trees are not automatically
defects. The generated trees differ because a program rewrites them. The two saved-search
files directly under ``uxlc/out/`` are Ben-written records, so the scan names the generated
``UXLC-misc`` directory and two generated JSON files instead of all of ``uxlc/out/``.
The landed MAM products follow the same rule: path-bearing provenance, copied code,
and analysis products are scanned, while the large verse-text JSON, XML, and CSV
families are not reread merely because a generator wrote them.
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

_ORIGINAL_SCANNED_PATHS = (
    "out",
    "gh-pages",
    "book-of-job/out",
    "doc/mp-claims.md",
    "doc/vendoring-inventory.md",
    "holman/data",
    "holman/docs-not-served",
    "holman/emails",
    "holman/out",
    "leningrad/lenin-wiki",
    "py-examples-out",
    "uxlc/out/UXLC-misc",
    "uxlc/out/uxlc-words-fragile.json",
    "uxlc/out/uxlc-words.json",
)

_PROGRAM_WRITTEN_GROUPS = {
    "Aleppo": (
        "aleppo/column-coordinates",
        "aleppo/ds-flat-stream",
        "aleppo/line-breaks",
        "aleppo/aleppo-wiki/index-flat.json",
        "aleppo/aleppo-wiki/index-grouped-by-book.json",
        "aleppo/aleppo-wiki/index.wiki",
        "aleppo/check_line_breaks.html",
        "aleppo/index-flat-annotated.json",
    ),
    "Cambridge 1753": (
        "cam1753/cam1753-col-quads",
        "cam1753/cam1753-line-breaks",
        "cam1753/cam1753-spread-splits-doc",
        "cam1753/check_line_breaks.html",
    ),
    "MAM-simple": (
        "MAM-simple/misc/unicode-names-vtrad-bhs",
        "MAM-simple/misc/unicode-names-vtrad-mam",
        "MAM-simple/misc/unicode-names-vtrad-sef",
        "MAM-simple/py-examples",
        "MAM-simple/py-examples-out/sefaria/csv/_provenance.md",
        "MAM-simple/py-examples-out/sefaria/misc/unicode-names/_provenance.md",
    ),
    "MAM-parsed": (
        "MAM-parsed/plain/provenance.md",
        "MAM-parsed/plus/provenance.md",
        "MAM-parsed/py-examples",
        "MAM-parsed/py-examples-out",
    ),
    "MAM-for-Sefaria": (
        "MAM-for-Sefaria/csv/_provenance.md",
        "MAM-for-Sefaria/csv-ajf/_provenance.md",
        "MAM-for-Sefaria/misc",
    ),
}

_SCANNED_PATHS = _ORIGINAL_SCANNED_PATHS + tuple(
    path for group_paths in _PROGRAM_WRITTEN_GROUPS.values() for path in group_paths
)

# A scan that silently matches nothing reports green having checked nothing, which is the
# failure mode CLAUDE.md's testing section is built around. The original ``out/`` and
# ``gh-pages/`` trees held 626 tracked files when this was written -- 341 under out/, 285
# under gh-pages/ -- of which 500 survive the binary filter below. 400 leaves room for the
# trees to shrink without tripping this, and is far above anything a broken enumeration
# would return.
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

# Intentionally empty since 2026-09-01.  The one exclusion this held from its arrival
# (86c87d2) was out/accgram/goerwitz-stderr/_summary.stderr.json, a fossil recording the
# departed wlc-utils clone's absolute path.  Nothing in py/ wrote it any more, so it
# could not regenerate wrongly because it could not regenerate at all; 86c87d2 called
# deleting it "a decision for its author", and Ben made that decision on 2026-09-01
# (doc/review-findings-2026-09-01.md's open ends): the file is deleted -- git history
# keeps it -- and the carve-out dropped, so the scan covers the two trees whole.  The 37
# empty .stderr.txt files beside it remain tracked and in scope.  The set stays so a
# future exception is documented here explicitly rather than carved out silently
# elsewhere.
_EXCLUDED = frozenset()

# Exact documentation excerpts, not excluded files or directories. The copied
# ``paths.py`` records the historical absolute-path defect that this lint prevents;
# removing that one sentence before matching preserves the explanation while still
# checking every other byte in the copied module.
_DOCUMENTED_PATH_EXCERPTS = {
    "MAM-simple/py-examples/mb_cmn/paths.py": (
        "C:/Users/BenDe/GitRepos/...",
        "/home/user/...",
    ),
}


def _tracked_text_files(pathspecs=_SCANNED_PATHS) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", *pathspecs],
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
            f"only {len(scanned)} tracked text files found under {_SCANNED_PATHS};"
            " the enumeration is broken, so the scan below verifies nothing",
        )

    def test_each_program_written_group_has_tracked_text(self):
        empty_groups = [
            label
            for label, pathspecs in _PROGRAM_WRITTEN_GROUPS.items()
            if not _tracked_text_files(pathspecs)
        ]
        self.assertEqual(
            empty_groups,
            [],
            "a declared program-written product group matched no tracked text; "
            f"coverage silently disappeared: {empty_groups}",
        )

    def test_documented_path_excerpts_still_name_exact_text(self):
        missing = []
        for name, excerpts in _DOCUMENTED_PATH_EXCERPTS.items():
            text = (paths.repo_root() / name).read_text(encoding="utf-8")
            for excerpt in excerpts:
                if excerpt not in text:
                    missing.append(f"{name}: {excerpt}")
        self.assertEqual(
            missing,
            [],
            "a documented-path allowlist entry no longer matches exact text; "
            f"review or remove the entry: {missing}",
        )

    def test_no_generated_artifact_records_a_machine_path(self):
        offenders = []
        for name in _tracked_text_files():
            path = paths.repo_root() / name
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for excerpt in _DOCUMENTED_PATH_EXCERPTS.get(name, ()):
                text = text.replace(excerpt, "")
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
