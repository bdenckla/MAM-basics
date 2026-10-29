"""Lint: every COMBINING GRAPHEME JOINER in MAM's text stands between two marks.

A COMBINING GRAPHEME JOINER (CGJ) only keeps the marks on either side of it in their
stored order, so one that is not between two marks does nothing. This lint therefore
requires that each CGJ have, immediately before it and immediately after it, a
character of Unicode category Mn that is not itself a CGJ. A failure names its file and
its line.

The scan reads every file Git tracks under the three Wikisource mirrors, in/mam-ws/,
in/mam-ws-intro/ and in/mam-ws-special/, and under each product directory that
py/product_scopes.py declares, except Taamey-D/. Each product directory is named below
as scanned or skipped, and one named as neither fails, so that a new product gets a
decision. Each file is text, read as strict UTF-8, or one of MAM-parsed's frozen
releases, the .zip files under MAM-parsed/historical/, which are skipped; any other
file fails. One test asserts that the scan read files and another that it found a CGJ,
so that neither an empty scan nor an encoding change such as escaped JSON can make this
lint pass by finding nothing.

A failure in the Wikisource mirrors is in MAM's text on Wikisource. The fix is a
Wikisource edit, made by a bot run that Ben approves, never an edit of the mirror; the
products' copies of the failure go away when they are regenerated from the corrected
text. A refresh that brings one in holds its push in the meantime, as the
mam-wikisource-refresh runbook holds the push for any failed check. A failure in a
product with no counterpart in the mirror it was built from is in the pipeline, which
inserts most of the products' CGJs as it expands MAM's templates. A failure in
Yeivin-ITM is in its own source, py/yeivin_itm/content/.
"""

import subprocess
import unicodedata
import unittest
from pathlib import PurePosixPath

import product_scopes
from mb_cmn import paths

_CGJ = "\N{COMBINING GRAPHEME JOINER}"

# The Wikisource mirrors, which are inputs rather than products.
_MIRROR_DIRS = ("in/mam-ws", "in/mam-ws-intro", "in/mam-ws-special")

# Every directory product_scopes.product_dirs() returns is named in one of these two.
_SCANNED_PRODUCT_DIRS = (
    "MAM-parsed",
    "MAM-simple",
    "MAM-for-Sefaria",
    "MAM-with-doc",
    "MAM-OSIS",
    "Phonetic-MAM",
    "Yeivin-ITM",
    "out/near-aleppo",
)
_SKIPPED_PRODUCT_DIRS = (
    # A font: its sources are not MAM's text, and the test cases of its shaping checks,
    # though drawn partly from MAM's words, are samples, any of which may hold an
    # unusual sequence on purpose.
    "Taamey-D",
)

# What the scanned directories held on 2026-10-29: text files with these suffixes,
# text files with these two names, which have no suffix, and the frozen releases.
_TEXT_SUFFIXES = frozenset(
    {".conf", ".csv", ".json", ".md", ".mediawiki", ".py", ".txt", ".xml"}
)
_TEXT_NAMES = frozenset({".gitattributes", ".gitignore"})
_FROZEN_RELEASE_DIR = "MAM-parsed/historical/"
_FROZEN_RELEASE_SUFFIX = ".zip"


def _scanned_dirs():
    """The mirrors, then each product directory named as scanned, repository-relative."""
    root = paths.repo_root()
    scanned, unnamed = list(_MIRROR_DIRS), []
    for product_dir in product_scopes.product_dirs():
        rel = product_dir.relative_to(root).as_posix()
        if rel in _SCANNED_PRODUCT_DIRS:
            scanned.append(rel)
        elif rel not in _SKIPPED_PRODUCT_DIRS:
            unnamed.append(rel)
    assert not unnamed, (
        "py/product_scopes.py declares product directories this lint names as"
        f" neither scanned nor skipped: {unnamed}. Name each in _SCANNED_PRODUCT_DIRS,"
        " or in _SKIPPED_PRODUCT_DIRS with the reason in a comment."
    )
    return scanned


def _scanned_files():
    """Every text file Git tracks under the scanned directories, by repository-relative name."""
    root = paths.repo_root()
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", *_scanned_dirs()],
        cwd=root,
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    texts, others = [], []
    for name in result.stdout.split("\0"):
        if not name:
            continue
        path = PurePosixPath(name)
        if path.suffix in _TEXT_SUFFIXES or path.name in _TEXT_NAMES:
            texts.append((name, root / name))
        elif not (
            path.suffix == _FROZEN_RELEASE_SUFFIX
            and name.startswith(_FROZEN_RELEASE_DIR)
        ):
            others.append(name)
    assert not others, (
        f"{len(others)} tracked file(s) under the scanned directories are of no type"
        " this lint names. Add a text file's suffix to _TEXT_SUFFIXES or its name to"
        f" _TEXT_NAMES; anything else needs a decision. First few: {others[:8]}"
    )
    return texts


def _occurrences(text):
    start = 0
    while (i := text.find(_CGJ, start)) != -1:
        yield i
        start = i + 1


def _is_mark(ch):
    """A character of category Mn other than a CGJ; the empty string is not one."""
    return bool(ch) and ch != _CGJ and unicodedata.category(ch) == "Mn"


def _is_between_marks(text, i):
    before = text[i - 1] if i else ""
    after = text[i + 1 : i + 2]
    return _is_mark(before) and _is_mark(after)


def _line_no(text, i):
    return text.count("\n", 0, i) + 1


class CgjBetweenMarksTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scanned = _scanned_files()
        cls.cgj_count = 0
        cls.failures = []
        for rel, path in cls.scanned:
            text = path.read_text(encoding="utf-8", errors="strict")
            for i in _occurrences(text):
                cls.cgj_count += 1
                if not _is_between_marks(text, i):
                    cls.failures.append(f"{rel}:{_line_no(text, i)}")

    def test_the_scan_reads_tracked_files(self):
        """So that finding no failure cannot mean finding nothing."""
        self.assertTrue(self.scanned)

    def test_the_scan_finds_a_cgj(self):
        """So that an encoding change, such as escaped JSON, cannot pass vacuously."""
        self.assertGreater(self.cgj_count, 0)

    def test_every_cgj_is_between_two_marks(self):
        summary = f"{len(self.failures)} CGJ(s) not between two marks"
        self.assertEqual(
            self.failures,
            [],
            f"{summary}: each lacks, immediately before or after it, a character of"
            " category Mn other than a CGJ. This file's docstring says where each"
            f" is repaired. First few: {self.failures[:8]}",
        )


if __name__ == "__main__":
    unittest.main()
