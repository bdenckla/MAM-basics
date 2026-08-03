"""Strip a Hebrew word/phrase to its bare letter skeleton (issue #48).

``strip_to_bare_letters`` keeps only the base letters (U+05D0–U+05EA) plus the three
punctuation-like marks maqaf (U+05BE), sof pasuq (U+05C3), and legarmeh/paseq (U+05C0)
— and whitespace, so a multi-word target does not collapse into one run. Everything else
is dropped: vowel points, cantillation marks, meteg/gaʿya, dagesh, rafe, shin/sin dots,
CGJ, and any other diacritic. So פָּנָֽ͏ַ֗י → פני, כָּל־ → כל־ (maqaf kept), תִרְצָ֖ח׃ → תרצח׃
(sof pasuq kept).

The legarmeh/paseq glyph (U+05C0) is kept UNCONDITIONALLY, in either its narrow-sense
paseq or its legarmeh sense — the two are graphically identical, and for a bare-letter
skeleton they read the same either way, so no accgram grammar lookup is needed to tell
them apart (design doc §7.16; issue #48 open Q3). Shin/sin dots are stripped like any
other diacritic (issue #48 general rule), leaving a bare ש.

The three keep-marks are word-level PUNCTUATION, not diacritics hanging on a letter:
maqaf joins words, sof pasuq ends a verse, and the paseq/legarmeh vertical bar separates
— which is why they survive a strip meant only to remove per-letter pointing.

First consumer: the combined-row divergence-note headings (§7.7, clc_render) — the note's
target word becomes a bare-letter heading while the text column still shows it fully
pointed. Built to be reusable by issue #48's other intended consumer (the reiterated word
inside a tanach.us <h2> note line, clc_note_pages), an editor-invokable per-note opt-in
not yet wired up.
"""

import mb_cmn.hebrew_punctuation as hpu
import mb_diff_mpu.describe_diff as describe_diff

_KEEP_MARKS = frozenset((hpu.MAQ, hpu.SOPA, hpu.PASOLEG))


def strip_to_bare_letters(text):
    """``text`` reduced to base letters + maqaf/sof-pasuq/legarmeh (whitespace kept)."""
    return "".join(
        ch
        for ch in text
        if describe_diff.is_letter(ch) or ch in _KEEP_MARKS or ch.isspace()
    )
