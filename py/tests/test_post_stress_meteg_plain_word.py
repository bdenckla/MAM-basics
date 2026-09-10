"""Lint: the post-stress-meteg pages say plain "word", never "chanted word".

WHY THIS EXISTS

The ``hebrew-prose`` skill's first rule is "Never a loose 'word'": say **atom** or **chanted
word**, because the two come apart exactly where a maqaf matters.  That is the right default
and it is not in question here.

**Ben's decision of 2026-09-08 is that this document and its sub-documents are an exception
to it.**  These nine pages define their two senses once, in the main page's second paragraph
-- "by 'word' we mean either a simple word (having just one atom) or a compound word (having
two or more atoms connected by maqaf marks). By 'atom' we mean a sequence of pointed letters
uninterrupted by space, maqaf, or any other punctuation" -- and then use plain "word" in that
declared sense throughout.  The skill's own rule allows for this: plain "word" survives
"wherever the context already settles which sense is meant", and a page that states the sense
in its opening has settled it for every sentence after.

WHAT WENT WRONG WITHOUT THIS LINT, AND WHY A COMMENT WOULD NOT HAVE STOPPED IT

The exception was recorded nowhere a sweep could see.  Between 2026-09-07 and 2026-09-08 two
branches fixed the *same* defect -- an alt text saying "chanted word" where the visible prose
said "word" -- in opposite directions.  This branch made the alt text say "word"; ``main``'s
review-remediation Waves 2 and 5 made the visible prose say "chanted word", 440 times across
the eight pages that existed there.  Neither side was careless: each applied a rule it had.
The merge then conflicted in 13 files and 32 hunks of ``author_site/post_stress_meteg.py``
alone, and no amount of care in resolving it could have decided which rule won, because that
was Ben's to decide.

A ``# pragma`` comment per line, or a ``plain_word_implying_chanted()`` wrapper around the
string, were both considered and rejected on 2026-09-08.  A comment is advisory: a bulk
terminology sweep edits string literals and need never read the line above.  A wrapper is
worse -- "word" appears mid-sentence inside long prose literals, so wrapping each occurrence
would shred readable sentences into fragments to defend a rule that a test can defend for
free.  A lint is the only one of the three that a sweep **cannot** miss, and it is one of the
two test shapes ``doc/agent-planning-principles.md`` says have ever paid here: a mechanical
lint over a decidable property of the text.

WHAT IT COVERS

The rendered pages only, and the whole of them -- visible prose, headings, ``title``
attributes and ``alt`` text alike, since the defect this replaces was in alt text.  The
**source** is deliberately not covered: ``chanted_word_difference``,
``census_chanted_word_summary`` and ``_case_chanted_word_cell`` are the survey's vocabulary
and the skill's rule is about reader-facing prose, not about identifiers or docstrings.

A MISSING PAGE FAILS RATHER THAN SKIPS, so a renamed or dropped page is reported here rather
than quietly reducing the lint's scope to nothing.
"""

import unittest
from pathlib import Path

from author_site import site_data
from mb_cmn import paths

# Matched against the page text LOWERCASED, so a "Chanted" opening a heading or a table
# cell is caught too.  The merge of 2026-09-08 left one such table header standing
# because this counted the word case-sensitively.
_FORBIDDEN = "chanted"

# Every page covered by the terminology decision. The membership check compares this tuple
# with both the rendered filenames and the filename constants declared in site_data.
_PAGE_FNAMES = (
    site_data.POST_STRESS_METEG_FNAME,
    site_data.POST_STRESS_METEG_METHODS_FNAME,
    site_data.POST_STRESS_METEG_CASES_FNAME,
    site_data.POST_STRESS_METEG_MISC_FNAME,
    site_data.POST_STRESS_METEG_LACKS_MAS_FNAME,
    site_data.POST_STRESS_METEG_NOT_FIT_FNAME,
    site_data.POST_STRESS_METEG_POST_SILLUQ_FNAME,
    site_data.POST_STRESS_METEG_2CHRONICLES_8_11_FNAME,
    site_data.POST_STRESS_METEG_NEXT_CONJUNCTIVE_FNAME,
)


def _page_path(fname: str) -> Path:
    return paths.repo_root() / "gh-pages" / fname


class TestPostStressMetegPlainWord(unittest.TestCase):
    """The nine post-stress-meteg pages use plain "word" in their declared sense."""

    def test_every_page_is_present(self):
        missing = [fname for fname in _PAGE_FNAMES if not _page_path(fname).is_file()]
        self.assertEqual(
            missing,
            [],
            "post-stress-meteg pages are missing, so this lint would check nothing: "
            f"{missing}",
        )
        expected = set(_PAGE_FNAMES)
        rendered = {
            path.name
            for path in (paths.repo_root() / "gh-pages").glob("post-stress-meteg*.html")
            if path.is_file()
        }
        declared = {
            value
            for name, value in vars(site_data).items()
            if name.startswith("POST_STRESS_METEG") and name.endswith("_FNAME")
        }
        self.assertEqual(rendered, expected, "Rendered MAS page membership differs")
        self.assertEqual(declared, expected, "Declared MAS page membership differs")

    def test_no_page_qualifies_word_as_chanted(self):
        offenders = []
        for fname in _PAGE_FNAMES:
            path = _page_path(fname)
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8").lower()
            count = text.count(_FORBIDDEN)
            if count:
                offenders.append(f"{fname}: {count}")
        self.assertEqual(
            offenders,
            [],
            f'"{_FORBIDDEN}" appears in these pages, which state their sense of "word" in'
            " the main page's opening and use it plainly thereafter (Ben's decision,"
            f" 2026-09-08). Occurrences: {offenders}",
        )
