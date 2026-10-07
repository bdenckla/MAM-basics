"""Lint: no occurrence of ב2 under in/mam-ws/ may be a sigil.

WHAT MAKES THE TWO USES DECIDABLE, and it is nothing about the two characters
themselves. MAM's manuscript sigil ב2 and the aliyah template's named parameter
of the same spelling are told apart by their delimiters: the parameter is
always preceded by "|" and followed by "=", the sigil always preceded by ",".
So this lint states the positive rule -- every surviving occurrence is a
parameter -- rather than trying to describe the sigil, which is what makes it
decidable from the source text alone. That is the second of the two sanctioned
test shapes: a mechanical lint over a decidable property of the corpus.

The scan reads every file Git tracks under in/mam-ws/, as UTF-8, and one test asserts that
there is such a file, so that finding no sigils cannot mean finding nothing.
"""

import subprocess
import unittest

from mb_cmn import paths

_B2 = "\N{HEBREW LETTER BET}2"

# The two delimiters that make the aliyah parameter what it is.
_PARAM_PREFIX = "|"
_PARAM_SUFFIX = "="

# The whole of the scanned corpus: the Wikisource download.
_SCANNED_DIRS = ("in/mam-ws",)


def _scanned_files():
    """Every file Git tracks under the scanned directories, by repository-relative name."""
    root = paths.repo_root()
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", *_SCANNED_DIRS],
        cwd=root,
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    return [(name, root / name) for name in result.stdout.split("\0") if name]


def _occurrences(text):
    start = 0
    while (i := text.find(_B2, start)) != -1:
        yield i
        start = i + 1


def _is_aliyah_param(text, i):
    before = text[i - 1] if i else ""
    after = text[i + len(_B2) : i + len(_B2) + 1]
    return before == _PARAM_PREFIX and after == _PARAM_SUFFIX


def _line_no(text, i):
    return text.count("\n", 0, i) + 1


class SigilB2NotASigilAnywhereTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scanned = _scanned_files()
        cls.sigils = []
        for rel, path in cls.scanned:
            text = path.read_text(encoding="utf-8")
            for i in _occurrences(text):
                if not _is_aliyah_param(text, i):
                    cls.sigils.append(f"{rel}:{_line_no(text, i)}")

    def test_the_scan_reads_tracked_files(self):
        """So that finding no sigils cannot mean finding nothing."""
        self.assertTrue(self.scanned)

    def test_no_occurrence_of_b2_is_a_sigil(self):
        summary = f"{len(self.sigils)} sigil-shaped occurrence(s)"
        self.assertEqual(
            self.sigils,
            [],
            f"{summary} of {_B2!r} remain under {' and '.join(_SCANNED_DIRS)}."
            " Each is preceded by ',' rather than by '|', so it is the"
            " manuscript sigil rather than the aliyah template's named"
            " parameter."
            f" First few: {self.sigils[:8]}",
        )


if __name__ == "__main__":
    unittest.main()
