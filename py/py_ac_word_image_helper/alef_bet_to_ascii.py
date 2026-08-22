"""Convert Hebrew letter text to an ASCII word-identifier.

Strips all niqqud and accents, then transliterates each Hebrew letter
to a single ASCII character.  Same scheme as MAM-basics'
``py/author_boj_util/author.py`` -- which was book-of-job's
``pyauthor_util/author.py`` until that repo's Python moved to MAM-basics on
2026-08-19 -- and mgketer's ``py/python_modules/hebrew_word_id.py``.

This docstring is one blob with codex-index-aleppo's copy of this file, which the
programme's Phase 0 reconciled on 2026-08-19; edit the two together or not at all.

    >>> heb_alef_bet_to_ascii("לֶֽאֱנ֣וֹשׁ")
    'LANVJ'
"""

import re

# fmt: off
_HEBREW_TO_ASCII_FROM = (
    "אבגדה"   # ABGDH
    "וזחטי"   # VZXEY
    "כלמנס"   # KLMNO
    "עפצקר"   # 3PCQR
    "שת"      # JF
    "ךםןףץ"   # 56789  (final forms)
    "־ "      # 0_  (maqaf, space)
)
_HEBREW_TO_ASCII_TO = (
    "ABGDH" "VZXEY" "KLMNO" "3PCQR" "JF" "56789" "0_"
)
# fmt: on

_HEBREW_TO_ASCII = str.maketrans(_HEBREW_TO_ASCII_FROM, _HEBREW_TO_ASCII_TO)
_KEEP_RE = re.compile(f"[{re.escape(_HEBREW_TO_ASCII_FROM)}]+")


def heb_alef_bet_to_ascii(hebrew_text):
    """Strip niqqud/accents from *hebrew_text*, transliterate to ASCII.

    Only Hebrew letters (incl. final forms), maqaf, and space are
    kept; everything else is discarded.  The result is safe for use in
    filenames and HTML identifiers.
    """
    kept = "".join(_KEEP_RE.findall(hebrew_text))
    return kept.translate(_HEBREW_TO_ASCII)
