# MAM-basics-specific accentuation prose

Read this reference when prose about Hebrew accentuation is written or edited in MAM-basics.
General terminology and rendered-page rules remain in the other skill references rather than
being repeated here.

## The post-stress-meteg pages say plain "word"

Ben's decision, 2026-09-08: `gh-pages/post-stress-meteg*.html` and its eight subdocuments are an
exception to the skill's “Never a loose word” rule. The main page defines both “word” and “atom”
in its second expository paragraph, and the opening sentence already uses “word”. Plain “word” is
therefore the declared term in visible prose, headings, tooltips, and alt text on all nine pages.
Never replace it with “chanted word”.

`py/tests/test_post_stress_meteg_plain_word.py` enforces the exception: “chanted” must not appear
in the rendered pages. The source identifiers `census_chanted_word_summary`,
`chanted_word_difference`, and `_case_chanted_word_cell` retain the survey's vocabulary; the
exception governs reader-facing prose rather than identifiers and docstrings.

## Accgram rendered prose

Before writing or editing prose on an accgram page, read
`py/accgram/printed_decalogue_strands.py`'s module docstring as well as
`references/rendered-prose.md`. The docstring's SCOPE paragraph distinguishes trio-only rules
from repository-wide rules. Keep the docstring's established strand names, signal words,
single-sourced romanizations, terminology, and sentence shape.

Some accgram docstrings and comments deliberately retain historical sibling spellings. A path
written as `../masorah-books/...` now resolves conceptually to
`../MAM-private/masorah-books/...`; a path written as `../al-hatorah/...` now resolves
conceptually to `../MAM-private/al-hatorah/...`. Ben chose to document those stale citations
rather than churn them solely for the move. For live source research, use the current MAM-private
paths in `references/sources-and-corpora.md` and search the full Yeivin OCR before concluding that
Yeivin is silent.
