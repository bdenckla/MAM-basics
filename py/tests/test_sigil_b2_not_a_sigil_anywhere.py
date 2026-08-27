"""Lint: no occurrence of ב2 under in/mam-ws/ or in/mam-go/ may be a sigil.

THIS TEST IS EXPECTED TO FAIL UNTIL PHASE 5 OF
doc/PLAN-replace-sigil-b2-with-t451.md COMPLETES. It is that plan's completion
criterion, added with Phase 1 so that the criterion exists before the work that
satisfies it, and it goes green only when both halves of the corpus have been
repointed -- Wikisource by the bot (Phase 3) and the Google Sheet by the
auto-edit round trip (Phase 5). A red result here is the plan reporting that it
is unfinished; it is not a break, and it must not be "fixed" by weakening the
assertion or by excluding the file that fails.

WHAT MAKES THE TWO USES DECIDABLE, and it is nothing about the two characters
themselves. MAM's manuscript sigil ב2 and the aliyah template's named parameter
of the same spelling are told apart by their delimiters: the parameter is
always preceded by "|" and followed by "=", the sigil always preceded by ",".
So this lint states the positive rule -- every surviving occurrence is a
parameter -- rather than trying to describe the sigil, which is what makes it
decidable from the source text alone. That is the second of the two sanctioned
test shapes: a mechanical lint over a decidable property of the corpus.

WHY BOTH DIRECTORIES, and why the Sheet half is the half that matters. in/mam-ws/
is the Wikisource download and in/mam-go/ the Google Sheet download, and MAM-parsed
derives from the Sheet, not from Wikisource (main_0_mega.py's first step is
parse-go). So a Wikisource edit that the Sheet never receives changes nothing that
is published, and the Sheet holds its own copy of these cells, which arrives again
on every download -- finding 1 of doc/review-findings-2026-08-26.md is the standing
example of exactly that recurrence channel. Scanning in/mam-go/ is what would catch
the replacement being undone from the Sheet side later.

The 216 aliyah parameters across the five Torah books are asserted present as
well as unflagged, so that a filter which quietly stopped reading the Torah
files could not pass this test by finding nothing at all.
"""

import unittest

from mb_cmn import paths

_B2 = "\N{HEBREW LETTER BET}2"

# The two delimiters that make the aliyah parameter what it is.
_PARAM_PREFIX = "|"
_PARAM_SUFFIX = "="

# The whole of the scanned corpus: the Wikisource download and the Sheet download.
_SCANNED_DIRS = ("in/mam-ws", "in/mam-go")

# Aliyah parameters counted 2026-08-27: 216 in in/mam-ws/ -- Genesis 48, Exodus
# 44, Leviticus 40, Numbers 40, Deuteronomy 44 -- and the same 216 again in
# in/mam-go/A-Torah.csv, so 432 across the two directories scanned here. This is
# a FLOOR rather than that total, deliberately: its job is to catch a scan that
# has stopped reading the Torah files and so finds no sigils by finding nothing
# at all, not to pin a number that a Sheet refresh could legitimately move.
_MIN_ALIYAH_PARAMS = 216


def _scanned_files():
    root = paths.repo_root()
    for rel_dir in _SCANNED_DIRS:
        for path in sorted((root / rel_dir).rglob("*")):
            if path.is_file():
                yield path.relative_to(root).as_posix(), path


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
        cls.sigils = []
        cls.aliyah_params = 0
        for rel, path in _scanned_files():
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for i in _occurrences(text):
                if _is_aliyah_param(text, i):
                    cls.aliyah_params += 1
                else:
                    cls.sigils.append(f"{rel}:{_line_no(text, i)}")

    def test_the_scan_reaches_the_torah_aliyah_parameters(self):
        """A floor, so that finding no sigils cannot mean finding nothing."""
        self.assertGreaterEqual(self.aliyah_params, _MIN_ALIYAH_PARAMS)

    def test_no_occurrence_of_b2_is_a_sigil(self):
        summary = f"{len(self.sigils)} sigil-shaped occurrence(s)"
        self.assertEqual(
            self.sigils,
            [],
            f"{summary} of {_B2!r} remain under {' and '.join(_SCANNED_DIRS)}."
            " Each is preceded by ',' rather than by '|', so it is the"
            " manuscript sigil rather than the aliyah template's named"
            " parameter. Expected to fail until Phase 5 of"
            " doc/PLAN-replace-sigil-b2-with-t451.md completes; see that plan"
            " before treating this as a regression."
            f" First few: {self.sigils[:8]}",
        )


if __name__ == "__main__":
    unittest.main()
